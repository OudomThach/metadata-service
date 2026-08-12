"""Global audit log + settings + capture-ocr — Romdoul Data Sharing admin surface."""

from __future__ import annotations

import re
import uuid

from fastapi import APIRouter, Depends, Query
from pydantic import BaseModel
from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from .. import models, schemas
from ..audit_log import log_event
from ..db import get_session
from ..errors import APIError
from ..security import Actor, require_auth

router = APIRouter(prefix="/api/v1", tags=["admin"])


# --------------------------------------------------------------------------- #
# capture-ocr — server-side artifact generation + save (Option B)
# --------------------------------------------------------------------------- #
class CaptureOcrIn(BaseModel):
    document_name: str
    full_text: str = ""
    result: dict | None = None  # raw engine output (stored as data.json)
    num_pages: int = 1


def _normalize_table(text: str) -> str:
    """Tab-separated rows (vLLM structured_text) -> pipe-table markdown so
    markdown previews and the grid editors parse them as tables."""
    if "|" in text:
        return text
    lines = [ln for ln in text.split("\n") if "\t" in ln]
    if not lines:
        return text
    return "\n".join("| " + " | ".join(ln.split("\t")) + " |" for ln in lines)


def _build_csv(text: str) -> str:
    """Pipe-table text -> CSV with BOM (mirrors the SPA's buildCsv)."""
    def esc(s: str) -> str:
        return f'"{str(s or "").replace(chr(34), chr(34) * 2)}"'

    rows: list[list[str]] = []
    table_lines = [ln.strip() for ln in text.split("\n") if "|" in ln]
    if len(table_lines) >= 2:
        header = [c.strip() for c in table_lines[0].strip().strip("|").split("|")]
        body = []
        for ln in table_lines[1:]:
            if re.fullmatch(r"\|?\s*[-:]+\s*(\|\s*[-:]+\s*)+\|?\s*", ln):
                continue
            body.append([c.strip() for c in ln.strip().strip("|").split("|")])
        if header:
            rows = [header, *body]
    if not rows:
        rows = [[ln] for ln in text.split("\n") if ln.strip()]
    return "\ufeff" + "\r\n".join(",".join(esc(c) for c in r) for r in rows)


@router.post("/capture-ocr", status_code=201, response_model=schemas.RecordOut)
async def capture_ocr(
    payload: CaptureOcrIn,
    session: AsyncSession = Depends(get_session),
    actor: Actor = Depends(require_auth),
):
    """Save an OCR result with all artifacts generated server-side.

    Requires X-API-Key or a session token (the adapters call this with the
    service's own API key when an OCR request carries save=true). Generates
    markdown + csv (pipe tables -> CSV with BOM) and stores the raw result as
    data.json — the Option-B path for direct API callers.
    """
    text = (payload.full_text or "").strip()
    rid = uuid.uuid4().hex
    markdown = _normalize_table(text)
    record = models.Record(
        id=rid,
        type="document",
        status="raw",
        source_filename=payload.document_name,
        source_system="api",
        source_model=(payload.result or {}).get("model") or (payload.result or {}).get("decoder") or "ocr",
        data={
            "document_name": payload.document_name,
            "full_text": text,
            "markdown": markdown,
            "csv": _build_csv(markdown),
            "json": payload.result or {},
            "num_pages": int(payload.num_pages or 1),
        },
        envelope={
            "data": {
                "document_name": payload.document_name,
                "full_text": text,
                "markdown": markdown,
                "csv": _build_csv(markdown),
                "json": payload.result or {},
                "num_pages": int(payload.num_pages or 1),
            },
            "audit": {"created_at": __import__("datetime").datetime.now(__import__("datetime").timezone.utc).isoformat(),
                      "created_by": actor.label(), "status": "raw", "edit_count": 0},
            "source": {"filename": payload.document_name, "model": "ocr", "source_system": "api"},
        },
        created_by=actor.label(),
    )
    session.add(record)
    await session.flush()
    session.add(models.AuditEventGlobal(
        actor=actor.label(), action="create", entity_type="record",
        entity_id=rid, detail={"document_name": payload.document_name, "via": "capture-ocr"},
    ))
    await session.commit()
    await session.refresh(record)
    from .. import crud as _crud
    return _crud.to_out(record)


# --------------------------------------------------------------------------- #
# Audit log
# --------------------------------------------------------------------------- #
@router.get("/audit", response_model=list[schemas.AuditEventGlobalOut])
async def list_audit(
    session: AsyncSession = Depends(get_session),
    actor: Actor = Depends(require_auth),
    entity_type: str | None = Query(None),
    action: str | None = Query(None),
    actor_name: str | None = Query(None),
    limit: int = Query(100, ge=1, le=500),
    offset: int = Query(0, ge=0),
) -> list[schemas.AuditEventGlobalOut]:
    if actor.role != "admin":
        raise APIError(403, "forbidden", "Admin role required")
    stmt = select(models.AuditEventGlobal).order_by(models.AuditEventGlobal.at.desc())
    if entity_type:
        stmt = stmt.where(models.AuditEventGlobal.entity_type == entity_type)
    if action:
        stmt = stmt.where(models.AuditEventGlobal.action == action)
    if actor_name:
        stmt = stmt.where(models.AuditEventGlobal.actor.ilike(f"%{actor_name}%"))
    rows = (await session.scalars(stmt.offset(offset).limit(limit))).all()
    return [
        schemas.AuditEventGlobalOut(
            id=e.id, actor=e.actor, action=e.action, entity_type=e.entity_type,
            entity_id=e.entity_id, detail=e.detail, at=e.at,
        )
        for e in rows
    ]


# --------------------------------------------------------------------------- #
# Settings
# --------------------------------------------------------------------------- #
@router.get("/settings", response_model=list[schemas.SettingOut])
async def list_settings(session: AsyncSession = Depends(get_session)) -> list[schemas.SettingOut]:
    rows = (await session.scalars(select(models.Setting).order_by(models.Setting.key))).all()
    return [schemas.SettingOut(key=s.key, value=s.value, updated_at=s.updated_at) for s in rows]


@router.put("/settings/{key}", response_model=schemas.SettingOut)
async def upsert_setting(
    key: str,
    payload: schemas.SettingIn,
    session: AsyncSession = Depends(get_session),
    actor: Actor = Depends(require_auth),
) -> schemas.SettingOut:
    if actor.role != "admin":
        raise APIError(403, "forbidden", "Admin role required")
    s = await session.get(models.Setting, key)
    if s is None:
        s = models.Setting(key=key, value=payload.value)
        session.add(s)
    else:
        s.value = payload.value
    await log_event(session, actor=actor.label(), action="update", entity_type="setting",
                    entity_id=key, detail={"value": payload.value})
    await session.commit()
    await session.refresh(s)
    return schemas.SettingOut(key=s.key, value=s.value, updated_at=s.updated_at)


@router.delete("/settings/{key}", status_code=204)
async def delete_setting(
    key: str,
    session: AsyncSession = Depends(get_session),
    actor: Actor = Depends(require_auth),
) -> None:
    if actor.role != "admin":
        raise APIError(403, "forbidden", "Admin role required")
    s = await session.get(models.Setting, key)
    if s:
        await log_event(session, actor=actor.label(), action="delete", entity_type="setting", entity_id=key)
        await session.delete(s)
        await session.commit()
