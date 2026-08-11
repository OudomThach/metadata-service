"""Global audit log + settings — Romdoul Data Sharing admin surface."""

from __future__ import annotations

from fastapi import APIRouter, Depends, Query
from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from .. import models, schemas
from ..audit_log import log_event
from ..db import get_session
from ..errors import APIError
from ..security import Actor, require_auth

router = APIRouter(prefix="/api/v1", tags=["admin"])


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
