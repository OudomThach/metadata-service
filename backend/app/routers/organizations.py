"""Organizations CRUD — Romdoul Data Sharing.

Reads are open (public explore lists orgs); writes require editor+.
"""

from __future__ import annotations

from fastapi import APIRouter, Depends
from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from .. import models, schemas
from ..audit_log import log_event
from ..db import get_session
from ..errors import APIError
from ..security import Actor, require_auth

router = APIRouter(prefix="/api/v1/organizations", tags=["organizations"])


def _out(o: models.Organization) -> schemas.OrganizationOut:
    return schemas.OrganizationOut(
        id=o.id, name=o.name, org_type=o.org_type, contact=o.contact, created_at=o.created_at
    )


@router.get("", response_model=list[schemas.OrganizationOut])
async def list_organizations(session: AsyncSession = Depends(get_session)) -> list[schemas.OrganizationOut]:
    rows = (await session.scalars(select(models.Organization).order_by(models.Organization.name))).all()
    return [_out(o) for o in rows]


@router.post("", status_code=201, response_model=schemas.OrganizationOut)
async def create_organization(
    payload: schemas.OrganizationIn,
    session: AsyncSession = Depends(get_session),
    actor: Actor = Depends(require_auth),
) -> schemas.OrganizationOut:
    if actor.role not in ("admin", "editor"):
        raise APIError(403, "forbidden", "Admin or editor role required")
    existing = await session.scalar(select(models.Organization).where(models.Organization.name == payload.name))
    if existing:
        raise APIError(409, "duplicate", f"organization '{payload.name}' already exists")
    org = models.Organization(name=payload.name, org_type=payload.org_type, contact=payload.contact)
    session.add(org)
    await session.flush()
    await log_event(session, actor=actor.label(), action="create", entity_type="organization",
                    entity_id=str(org.id), detail={"name": org.name})
    await session.commit()
    await session.refresh(org)
    return _out(org)


@router.patch("/{org_id}", response_model=schemas.OrganizationOut)
async def update_organization(
    org_id: int,
    payload: schemas.OrganizationIn,
    session: AsyncSession = Depends(get_session),
    actor: Actor = Depends(require_auth),
) -> schemas.OrganizationOut:
    if actor.role not in ("admin", "editor"):
        raise APIError(403, "forbidden", "Admin or editor role required")
    org = await session.get(models.Organization, org_id)
    if not org:
        raise APIError(404, "not_found", f"organization {org_id} not found")
    org.name = payload.name
    org.org_type = payload.org_type
    org.contact = payload.contact
    await log_event(session, actor=actor.label(), action="update", entity_type="organization",
                    entity_id=str(org_id), detail={"name": org.name})
    await session.commit()
    await session.refresh(org)
    return _out(org)


@router.delete("/{org_id}", status_code=204)
async def delete_organization(
    org_id: int,
    session: AsyncSession = Depends(get_session),
    actor: Actor = Depends(require_auth),
) -> None:
    if actor.role != "admin":
        raise APIError(403, "forbidden", "Admin role required")
    org = await session.get(models.Organization, org_id)
    if not org:
        raise APIError(404, "not_found", f"organization {org_id} not found")
    await log_event(session, actor=actor.label(), action="delete", entity_type="organization",
                    entity_id=str(org_id), detail={"name": org.name})
    await session.delete(org)
    await session.commit()
