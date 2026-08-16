"""Global audit logging for the Romdoul Data Sharing portal.

Every meaningful action across entities (records, datasets, users, categories,
collections, organizations, settings) appends an AuditEventGlobal row so the
Audit logs page can answer "who did what, when".
"""

from __future__ import annotations

from typing import Any

from sqlalchemy.ext.asyncio import AsyncSession

from . import models


async def log_event(
    session: AsyncSession,
    *,
    actor: str,
    action: str,
    entity_type: str,
    entity_id: str | None = None,
    detail: dict[str, Any] | None = None,
) -> None:
    session.add(
        models.AuditEventGlobal(
            actor=actor,
            action=action,
            entity_type=entity_type,
            entity_id=entity_id,
            detail=detail,
        )
    )
