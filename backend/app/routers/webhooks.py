import asyncio
import ipaddress
import logging
from typing import Any
from urllib.parse import urlparse

import httpx
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import Text, cast, select
from sqlalchemy.ext.asyncio import AsyncSession

from ..constants import WEBHOOK_EVENTS
from ..db import get_session
from ..errors import APIError
from ..models import Webhook
from ..schemas import WebhookIn, WebhookOut
from ..security import Actor, require_auth

log = logging.getLogger("metadata.webhooks")
router = APIRouter(prefix="/api/v1/webhooks", tags=["webhooks"])


def _validate_webhook_url(url: str) -> None:
    """Reject non-http(s) schemes and loopback/private/ULA targets (SSRF guard)."""
    parsed = urlparse(url)
    if parsed.scheme not in ("http", "https") or not parsed.hostname:
        raise HTTPException(status_code=422, detail="Webhook URL must be http(s) with a host")
    try:
        ip = ipaddress.ip_address(parsed.hostname)
    except ValueError:
        return  # hostname — DNS not resolved here
    if ip.is_private or ip.is_loopback or ip.is_link_local or ip.is_reserved:
        raise HTTPException(status_code=422, detail="Webhook URL must target a public address")


def _require_admin(actor: Actor) -> None:
    if actor.role != "admin":
        raise APIError(403, "forbidden", "Admin role required")


def _out(w: Webhook) -> WebhookOut:
    return WebhookOut(id=w.id, url=w.url, events=w.events, enabled=w.enabled)


@router.post("", status_code=201, response_model=WebhookOut)
async def create_webhook(
    payload: WebhookIn, actor: Actor = Depends(require_auth), session: AsyncSession = Depends(get_session)
) -> WebhookOut:
    _require_admin(actor)
    for e in payload.events:
        if e not in WEBHOOK_EVENTS:
            raise APIError(422, "invalid_event", f"Unknown event: {e}")
    _validate_webhook_url(payload.url)
    wh = Webhook(url=payload.url.strip(), events=payload.events, enabled=True)
    session.add(wh)
    await session.commit()
    return _out(wh)


@router.get("", response_model=list[WebhookOut])
async def list_webhooks(
    actor: Actor = Depends(require_auth), session: AsyncSession = Depends(get_session)
) -> list[WebhookOut]:
    _require_admin(actor)
    rows = await session.execute(select(Webhook).order_by(Webhook.id))
    return [_out(w) for w in rows.scalars()]


@router.delete("/{webhook_id:int}", response_model=None, status_code=204)
async def delete_webhook(
    webhook_id: int, actor: Actor = Depends(require_auth), session: AsyncSession = Depends(get_session)
) -> None:
    _require_admin(actor)
    wh = await session.get(Webhook, webhook_id)
    if not wh:
        raise APIError(404, "not_found", "Webhook not found")
    await session.delete(wh)
    await session.commit()


async def fire_webhooks(record_id: str, action: str, snapshot: dict[str, Any]) -> None:
    """Fire matching webhooks asynchronously (fire-and-forget, 5s cap).
    Uses its own session to avoid concurrent-access issues with the caller's session."""
    from ..db import SessionLocal

    async with SessionLocal() as session:
        stmt = select(Webhook).where(Webhook.enabled == True)  # noqa: E712
        dialect = session.get_bind().dialect.name
        if dialect == "postgresql":
            stmt = stmt.where(Webhook.events.contains([action]))
        else:
            stmt = stmt.where(cast(Webhook.events, Text).ilike(f'%"{action}"%'))
        rows = await session.execute(stmt)
        hooks = rows.scalars().all()
        if not hooks:
            return
        payload = {"event": action, "record_id": record_id, "snapshot": snapshot}

        async def _send(wh: Webhook) -> None:
            try:
                async with httpx.AsyncClient(timeout=httpx.Timeout(5.0)) as client:
                    await client.post(wh.url, json=payload)
            except Exception as exc:
                log.warning("webhook %s failed: %s", wh.id, exc)

        tasks = [asyncio.create_task(_send(wh)) for wh in hooks]
        for t in tasks:
            t.add_done_callback(lambda _: None)
