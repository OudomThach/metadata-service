"""Shared dataset-promotion logic.

Both entry points (the manual `POST /datasets/from-record/{id}` endpoint and the
auto-promote on verify) funnel through promote_record_to_dataset(), so a
promoted dataset always carries the same payload: the record's dataset fields
plus its columns and references.
"""

from __future__ import annotations

import datetime as dt
import uuid

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from . import models


def _date(v: str | None) -> dt.date | None:
    if not v:
        return None
    try:
        return dt.date.fromisoformat(str(v)[:10])
    except ValueError:
        return None


async def find_dataset_for_record(session: AsyncSession, record_id: str) -> models.Dataset | None:
    row = await session.execute(select(models.Dataset).where(models.Dataset.record_id == record_id))
    return row.scalar_one_or_none()


async def promote_record_to_dataset(
    session: AsyncSession,
    record: models.Record,
    actor_label: str,
    *,
    auto: bool = False,
) -> models.Dataset:
    """Create a draft Dataset from a record's post-OCR payload. Caller commits."""
    ds_payload = (record.data or {}).get("dataset") or {}
    file_meta = ds_payload.get("file") or {}
    dataset = models.Dataset(
        id=uuid.uuid4().hex,
        record_id=record.id,
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
        columns=(record.data or {}).get("columns"),
        references=(record.data or {}).get("references"),
        status="draft",
    )
    session.add(dataset)
    await session.flush()
    session.add(
        models.AuditEventGlobal(
            actor=actor_label,
            action="create",
            entity_type="dataset",
            entity_id=dataset.id,
            detail={"name": dataset.name, "from_record": record.id, "auto": auto},
        )
    )
    return dataset
