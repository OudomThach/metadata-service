"""Datasets â€” first-class entities for Romdoul Data Sharing.

A dataset is created from an extraction record + the post-OCR dataset form,
then managed through draft -> published -> archived. The public read path
(?public=1) exposes ONLY published datasets without authentication so the
Explore page can browse/download without login.
"""

from __future__ import annotations

import datetime as dt
import uuid
from datetime import datetime, timezone

from fastapi import APIRouter, Depends, Query
from sqlalchemy import func, or_, select
from sqlalchemy.ext.asyncio import AsyncSession

from .. import models, schemas
from ..audit_log import log_event
from ..db import get_session
from ..errors import APIError
from ..security import Actor, require_auth, require_auth_optional

router = APIRouter(prefix="/api/v1/datasets", tags=["datasets"])

STATUSES = ("draft", "published", "archived")


def _out(d: models.Dataset) -> schemas.DatasetOut:
    return schemas.DatasetOut(
        id=d.id, record_id=d.record_id, name=d.name, description=d.description,
        organization_id=d.organization_id, category_id=d.category_id, collection_id=d.collection_id,
        coverage_start=d.coverage_start, coverage_end=d.coverage_end, frequency=d.frequency,
        url=d.url, status=d.status, published_at=d.published_at,
        file_name=d.file_name, file_size=d.file_size, file_type=d.file_type,
        file_base64=d.file_base64, created_at=d.created_at, updated_at=d.updated_at,
    )


@router.get("", response_model=schemas.DatasetPageOut)
async def list_datasets(
    session: AsyncSession = Depends(get_session),
    actor: Actor | None = Depends(require_auth_optional),
    page: int = Query(1, ge=1),
    page_size: int = Query(50, ge=1, le=200),
    status: str | None = Query(None),
    category_id: int | None = Query(None),
    collection_id: int | None = Query(None),
    organization_id: int | None = Query(None),
    q: str | None = Query(None),
    public: bool = Query(False, description="public=1 shows only published datasets, no auth"),
) -> schemas.DatasetPageOut:
    stmt = select(models.Dataset)
    if public:
        stmt = stmt.where(models.Dataset.status == "published")
    elif actor is None or actor.role not in ("admin", "editor"):
        raise APIError(403, "forbidden", "Login required to list non-public datasets")
    if status:
        stmt = stmt.where(models.Dataset.status == status)
    if category_id:
        stmt = stmt.where(models.Dataset.category_id == category_id)
    if collection_id:
        stmt = stmt.where(models.Dataset.collection_id == collection_id)
    if organization_id:
        stmt = stmt.where(models.Dataset.organization_id == organization_id)
    if q:
        stmt = stmt.where(or_(models.Dataset.name.ilike(f"%{q}%"), models.Dataset.description.ilike(f"%{q}%")))
    total = await session.scalar(select(func.count()).select_from(stmt.subquery()))
    rows = (await session.scalars(
        stmt.order_by(models.Dataset.created_at.desc())
        .offset((page - 1) * page_size).limit(page_size)
    )).all()
    total = int(total or 0)
    return schemas.DatasetPageOut(
        items=[_out(d) for d in rows], page=page, page_size=page_size,
        total=total, total_pages=max(1, -(-total // page_size)) if total else 1,
    )


@router.get("/{dataset_id}", response_model=schemas.DatasetOut)
async def get_dataset(
    dataset_id: str,
    session: AsyncSession = Depends(get_session),
    actor: Actor | None = Depends(require_auth_optional),
) -> schemas.DatasetOut:
    d = await session.get(models.Dataset, dataset_id)
    if not d:
        raise APIError(404, "not_found", f"dataset {dataset_id} not found")
    if d.status != "published" and (actor is None or actor.role not in ("admin", "editor")):
        raise APIError(403, "forbidden", "This dataset is not published")
    return _out(d)


@router.post("", status_code=201, response_model=schemas.DatasetOut)
async def create_dataset(
    payload: schemas.DatasetIn,
    session: AsyncSession = Depends(get_session),
    actor: Actor = Depends(require_auth),
) -> schemas.DatasetOut:
    if actor.role not in ("admin", "editor"):
        raise APIError(403, "forbidden", "Admin or editor role required")
    d = models.Dataset(
        id=payload.id or uuid.uuid4().hex,
        record_id=payload.record_id, name=payload.name, description=payload.description,
        organization_id=payload.organization_id, category_id=payload.category_id,
        collection_id=payload.collection_id, coverage_start=payload.coverage_start,
        coverage_end=payload.coverage_end, frequency=payload.frequency, url=payload.url,
        file_name=payload.file_name, file_size=payload.file_size, file_type=payload.file_type,
        file_base64=payload.file_base64,
        status="draft",
    )
    session.add(d)
    await session.flush()
    await log_event(session, actor=actor.label(), action="create", entity_type="dataset",
                    entity_id=d.id, detail={"name": d.name})
    await session.commit()
    await session.refresh(d)
    return _out(d)


@router.patch("/{dataset_id}", response_model=schemas.DatasetOut)
async def update_dataset(
    dataset_id: str,
    payload: schemas.DatasetIn,
    session: AsyncSession = Depends(get_session),
    actor: Actor = Depends(require_auth),
) -> schemas.DatasetOut:
    if actor.role not in ("admin", "editor"):
        raise APIError(403, "forbidden", "Admin or editor role required")
    d = await session.get(models.Dataset, dataset_id)
    if not d:
        raise APIError(404, "not_found", f"dataset {dataset_id} not found")
    for field in ("record_id", "name", "description", "organization_id", "category_id",
                  "collection_id", "coverage_start", "coverage_end", "frequency", "url",
                  "file_name", "file_size", "file_type", "file_base64"):
        value = getattr(payload, field)
        if value is not None:
            setattr(d, field, value)
    d.updated_at = datetime.now(timezone.utc)
    await log_event(session, actor=actor.label(), action="update", entity_type="dataset",
                    entity_id=d.id, detail={"name": d.name})
    await session.commit()
    await session.refresh(d)
    return _out(d)


@router.post("/from-record/{record_id}", status_code=201, response_model=schemas.DatasetOut)
async def create_dataset_from_record(
    record_id: str,
    session: AsyncSession = Depends(get_session),
    actor: Actor = Depends(require_auth),
) -> schemas.DatasetOut:
    """Lift a record's post-OCR dataset payload (data.dataset + embedded file)
    into a first-class Dataset row (status draft)."""
    if actor.role not in ("admin", "editor"):
        raise APIError(403, "forbidden", "Admin or editor role required")
    rec = await session.get(models.Record, record_id)
    if not rec:
        raise APIError(404, "not_found", f"record {record_id} not found")
    ds_payload = (rec.data or {}).get("dataset") or {}
    if not ds_payload.get("name"):
        raise APIError(422, "bad_request", "record has no dataset payload")
    existing = await session.scalar(select(models.Dataset).where(models.Dataset.record_id == record_id))
    if existing:
        raise APIError(409, "duplicate", "record already promoted to a dataset")

    def _date(v: str | None) -> dt.date | None:
        if not v:
            return None
        try:
            return dt.date.fromisoformat(str(v)[:10])
        except ValueError:
            return None

    file_meta = ds_payload.get("file") or {}
    d = models.Dataset(
        id=uuid.uuid4().hex,
        record_id=record_id,
        name=ds_payload.get("name") or "Untitled dataset",
        description=ds_payload.get("description"),
        coverage_start=_date(ds_payload.get("coverage_start")),
        coverage_end=_date(ds_payload.get("coverage_end")),
        frequency=ds_payload.get("frequency"),
        url=ds_payload.get("url"),
        file_name=file_meta.get("name"),
        file_size=file_meta.get("size"),
        file_type=file_meta.get("type"),
        file_base64=ds_payload.get("file_base64"),
        status="draft",
    )
    session.add(d)
    await session.flush()
    await log_event(session, actor=actor.label(), action="create", entity_type="dataset",
                    entity_id=d.id, detail={"name": d.name, "from_record": record_id})
    await session.commit()
    await session.refresh(d)
    return _out(d)


@router.post("/{dataset_id}/publish", response_model=schemas.DatasetOut)
async def publish_dataset(
    dataset_id: str,
    session: AsyncSession = Depends(get_session),
    actor: Actor = Depends(require_auth),
) -> schemas.DatasetOut:
    if actor.role not in ("admin", "editor"):
        raise APIError(403, "forbidden", "Admin or editor role required")
    d = await session.get(models.Dataset, dataset_id)
    if not d:
        raise APIError(404, "not_found", f"dataset {dataset_id} not found")
    d.status = "published"
    d.published_at = datetime.now(timezone.utc)
    d.updated_at = d.published_at
    await log_event(session, actor=actor.label(), action="publish", entity_type="dataset",
                    entity_id=d.id, detail={"name": d.name})
    await session.commit()
    await session.refresh(d)
    return _out(d)


@router.post("/{dataset_id}/unpublish", response_model=schemas.DatasetOut)
async def unpublish_dataset(
    dataset_id: str,
    session: AsyncSession = Depends(get_session),
    actor: Actor = Depends(require_auth),
) -> schemas.DatasetOut:
    if actor.role not in ("admin", "editor"):
        raise APIError(403, "forbidden", "Admin or editor role required")
    d = await session.get(models.Dataset, dataset_id)
    if not d:
        raise APIError(404, "not_found", f"dataset {dataset_id} not found")
    d.status = "draft"
    d.published_at = None
    d.updated_at = datetime.now(timezone.utc)
    await log_event(session, actor=actor.label(), action="unpublish", entity_type="dataset",
                    entity_id=d.id, detail={"name": d.name})
    await session.commit()
    await session.refresh(d)
    return _out(d)


@router.delete("/{dataset_id}", status_code=204)
async def delete_dataset(
    dataset_id: str,
    session: AsyncSession = Depends(get_session),
    actor: Actor = Depends(require_auth),
) -> None:
    if actor.role != "admin":
        raise APIError(403, "forbidden", "Admin role required")
    d = await session.get(models.Dataset, dataset_id)
    if not d:
        raise APIError(404, "not_found", f"dataset {dataset_id} not found")
    await log_event(session, actor=actor.label(), action="delete", entity_type="dataset",
                    entity_id=d.id, detail={"name": d.name})
    await session.delete(d)
    await session.commit()
