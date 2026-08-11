"""Collections CRUD — Romdoul Data Sharing.

Reads open (public explore); writes editor+.
"""

from __future__ import annotations

from fastapi import APIRouter, Depends
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from .. import models, schemas
from ..audit_log import log_event
from ..db import get_session
from ..errors import APIError
from ..security import Actor, require_auth

router = APIRouter(prefix="/api/v1/collections", tags=["collections"])


def _out(c: models.Collection) -> schemas.CollectionOut:
    return schemas.CollectionOut(
        id=c.id, name=c.name, description=c.description,
        organization_id=c.organization_id, created_at=c.created_at,
    )


@router.get("", response_model=list[schemas.CollectionOut])
async def list_collections(session: AsyncSession = Depends(get_session)) -> list[schemas.CollectionOut]:
    rows = (await session.scalars(select(models.Collection).order_by(models.Collection.name))).all()
    return [_out(c) for c in rows]


@router.post("", status_code=201, response_model=schemas.CollectionOut)
async def create_collection(
    payload: schemas.CollectionIn,
    session: AsyncSession = Depends(get_session),
    actor: Actor = Depends(require_auth),
) -> schemas.CollectionOut:
    if actor.role not in ("admin", "editor"):
        raise APIError(403, "forbidden", "Admin or editor role required")
    if payload.organization_id is not None and not await session.get(models.Organization, payload.organization_id):
        raise APIError(422, "bad_request", f"organization {payload.organization_id} not found")
    existing = await session.scalar(select(models.Collection).where(models.Collection.name == payload.name))
    if existing:
        raise APIError(409, "duplicate", f"collection '{payload.name}' already exists")
    col = models.Collection(name=payload.name, description=payload.description,
                            organization_id=payload.organization_id)
    session.add(col)
    await session.flush()
    await log_event(session, actor=actor.label(), action="create", entity_type="collection",
                    entity_id=str(col.id), detail={"name": col.name})
    await session.commit()
    await session.refresh(col)
    return _out(col)


@router.patch("/{collection_id}", response_model=schemas.CollectionOut)
async def update_collection(
    collection_id: int,
    payload: schemas.CollectionIn,
    session: AsyncSession = Depends(get_session),
    actor: Actor = Depends(require_auth),
) -> schemas.CollectionOut:
    if actor.role not in ("admin", "editor"):
        raise APIError(403, "forbidden", "Admin or editor role required")
    col = await session.get(models.Collection, collection_id)
    if not col:
        raise APIError(404, "not_found", f"collection {collection_id} not found")
    col.name = payload.name
    col.description = payload.description
    col.organization_id = payload.organization_id
    await log_event(session, actor=actor.label(), action="update", entity_type="collection",
                    entity_id=str(collection_id), detail={"name": col.name})
    await session.commit()
    await session.refresh(col)
    return _out(col)


@router.delete("/{collection_id}", status_code=204)
async def delete_collection(
    collection_id: int,
    session: AsyncSession = Depends(get_session),
    actor: Actor = Depends(require_auth),
) -> None:
    if actor.role != "admin":
        raise APIError(403, "forbidden", "Admin role required")
    col = await session.get(models.Collection, collection_id)
    if not col:
        raise APIError(404, "not_found", f"collection {collection_id} not found")
    await log_event(session, actor=actor.label(), action="delete", entity_type="collection",
                    entity_id=str(collection_id), detail={"name": col.name})
    await session.delete(col)
    await session.commit()
