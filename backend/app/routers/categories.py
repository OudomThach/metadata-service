"""Categories CRUD (tree via parent_id) — Romdoul Data Sharing.

Reads open (public explore + dataset form pickers); writes editor+.
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

router = APIRouter(prefix="/api/v1/categories", tags=["categories"])


def _out(c: models.Category) -> schemas.CategoryOut:
    return schemas.CategoryOut(
        id=c.id, parent_id=c.parent_id, name=c.name, description=c.description,
        sort=c.sort, created_at=c.created_at,
    )


@router.get("", response_model=list[schemas.CategoryOut])
async def list_categories(session: AsyncSession = Depends(get_session)) -> list[schemas.CategoryOut]:
    rows = (await session.scalars(select(models.Category).order_by(models.Category.sort, models.Category.name))).all()
    return [_out(c) for c in rows]


@router.post("", status_code=201, response_model=schemas.CategoryOut)
async def create_category(
    payload: schemas.CategoryIn,
    session: AsyncSession = Depends(get_session),
    actor: Actor = Depends(require_auth),
) -> schemas.CategoryOut:
    if actor.role not in ("admin", "editor"):
        raise APIError(403, "forbidden", "Admin or editor role required")
    if payload.parent_id is not None and not await session.get(models.Category, payload.parent_id):
        raise APIError(422, "bad_request", f"parent category {payload.parent_id} not found")
    cat = models.Category(parent_id=payload.parent_id, name=payload.name,
                          description=payload.description, sort=payload.sort)
    session.add(cat)
    await session.flush()
    await log_event(session, actor=actor.label(), action="create", entity_type="category",
                    entity_id=str(cat.id), detail={"name": cat.name, "parent_id": cat.parent_id})
    await session.commit()
    await session.refresh(cat)
    return _out(cat)


@router.patch("/{category_id}", response_model=schemas.CategoryOut)
async def update_category(
    category_id: int,
    payload: schemas.CategoryIn,
    session: AsyncSession = Depends(get_session),
    actor: Actor = Depends(require_auth),
) -> schemas.CategoryOut:
    if actor.role not in ("admin", "editor"):
        raise APIError(403, "forbidden", "Admin or editor role required")
    cat = await session.get(models.Category, category_id)
    if not cat:
        raise APIError(404, "not_found", f"category {category_id} not found")
    if payload.parent_id is not None and payload.parent_id != category_id:
        if not await session.get(models.Category, payload.parent_id):
            raise APIError(422, "bad_request", f"parent category {payload.parent_id} not found")
    cat.parent_id = payload.parent_id
    cat.name = payload.name
    cat.description = payload.description
    cat.sort = payload.sort
    await log_event(session, actor=actor.label(), action="update", entity_type="category",
                    entity_id=str(category_id), detail={"name": cat.name})
    await session.commit()
    await session.refresh(cat)
    return _out(cat)


@router.delete("/{category_id}", status_code=204)
async def delete_category(
    category_id: int,
    session: AsyncSession = Depends(get_session),
    actor: Actor = Depends(require_auth),
) -> None:
    if actor.role != "admin":
        raise APIError(403, "forbidden", "Admin role required")
    cat = await session.get(models.Category, category_id)
    if not cat:
        raise APIError(404, "not_found", f"category {category_id} not found")
    await log_event(session, actor=actor.label(), action="delete", entity_type="category",
                    entity_id=str(category_id), detail={"name": cat.name})
    await session.delete(cat)
    await session.commit()
