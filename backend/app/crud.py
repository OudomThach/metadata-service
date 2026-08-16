import datetime as dt
from typing import Any

from sqlalchemy import Select, Text, cast, func, or_, select
from sqlalchemy.ext.asyncio import AsyncSession

from . import models, schemas


def apply_filters(
    stmt: Select[tuple[models.Record]],
    *,
    dialect: str,
    type: str | None,
    domain: str | None,
    status: str | None,
    tag: str | None,
    business_from: dt.date | None,
    business_to: dt.date | None,
    created_from: dt.datetime | None,
    created_to: dt.datetime | None,
    edited_from: dt.datetime | None,
    edited_to: dt.datetime | None,
    q: str | None,
) -> Select[tuple[models.Record]]:
    if type:
        stmt = stmt.where(models.Record.type == type)
    if domain:
        stmt = stmt.where(models.Record.domain == domain)
    if status:
        stmt = stmt.where(models.Record.status == status)
    if tag:
        if dialect == "postgresql":
            stmt = stmt.where(models.Record.tags.contains([tag]))
        else:
            stmt = stmt.where(cast(models.Record.tags, Text).ilike(f'%"{tag}"%'))
    if business_from:
        stmt = stmt.where(models.Record.business_date >= business_from)
    if business_to:
        stmt = stmt.where(models.Record.business_date <= business_to)
    if created_from and edited_from:
        # CDC sync window: pull records that are NEW since the watermark OR
        # UPDATED since it (a never-edited record has edited_at=null and must
        # still match via created_at).
        stmt = stmt.where(or_(models.Record.created_at >= created_from, models.Record.edited_at >= edited_from))
    else:
        if created_from:
            stmt = stmt.where(models.Record.created_at >= created_from)
        if edited_from:
            stmt = stmt.where(models.Record.edited_at >= edited_from)
    if created_to and edited_to:
        stmt = stmt.where(or_(models.Record.created_at <= created_to, models.Record.edited_at <= edited_to))
    else:
        if created_to:
            stmt = stmt.where(models.Record.created_at <= created_to)
        if edited_to:
            stmt = stmt.where(models.Record.edited_at <= edited_to)
    if q:
        # Full-text-ish search across the extraction data (incl. full_text)
        # AND the envelope (business metadata, tags, titles, ...).
        stmt = stmt.where(
            or_(
                cast(models.Record.data, Text).ilike(f"%{q}%"),
                cast(models.Record.envelope, Text).ilike(f"%{q}%"),
            )
        )
    return stmt


def sort_stmt(stmt: Select[tuple[models.Record]], sort: str) -> Select[tuple[models.Record]]:
    col, _, direction = sort.partition(":")
    if col not in ("created_at", "business_date", "edited_at", "type", "status"):
        col = "created_at"
    column = getattr(models.Record, col)
    if direction == "desc":
        return stmt.order_by(column.desc().nullslast())
    if col == "business_date":
        return stmt.order_by(column.is_(None), column.asc())
    return stmt.order_by(column.asc())


def to_out(rec: models.Record) -> schemas.RecordOut:
    env = rec.envelope or {}
    src = env.get("source") or {}
    aud = env.get("audit") or {}
    pl = env.get("pipeline") or {}
    rcd = env.get("record") or {}
    biz = env.get("business") or {}
    return schemas.RecordOut(
        id=rec.id,
        schema_version=rec.schema_version,
        type=rec.type,
        domain=rec.domain,
        status=rec.status,
        business_date=rec.business_date,
        tags=rec.tags,
        source=schemas.SourceIn(**src) if src else None,
        audit=schemas.AuditIn(**aud) if aud else None,
        pipeline=schemas.PipelineIn(**pl) if pl else None,
        record=schemas.RecordIn(**rcd) if rcd else None,
        business=schemas.BusinessIn(**biz) if biz else None,
        data=rec.data,
        envelope=env,
        created_at=rec.created_at,
        created_by=rec.created_by,
        edited_at=rec.edited_at,
        edited_by=rec.edited_by,
        edit_count=rec.edit_count,
        source_model=rec.source_model,
        source_system=rec.source_system,
    )


def dataset_to_out(d: models.Dataset) -> schemas.DatasetOut:
    return schemas.DatasetOut(
        id=d.id,
        record_id=d.record_id,
        name=d.name,
        description=d.description,
        organization_id=d.organization_id,
        category_id=d.category_id,
        collection_id=d.collection_id,
        coverage_start=d.coverage_start,
        coverage_end=d.coverage_end,
        frequency=d.frequency,
        url=d.url,
        status=d.status,
        published_at=d.published_at,
        file_name=d.file_name,
        file_size=d.file_size,
        file_type=d.file_type,
        file_base64=d.file_base64,
        columns=d.columns,
        references=d.references,
        created_at=d.created_at,
        updated_at=d.updated_at,
    )


async def log_audit(session: AsyncSession, record_id: str, action: str, actor: str, snapshot: dict[str, Any]) -> None:
    session.add(
        models.AuditEvent(
            record_id=record_id,
            action=action,
            actor=actor,
            envelope_snapshot=snapshot,
        )
    )


async def get_types(session: AsyncSession) -> list[str]:
    res = await session.execute(select(models.Record.type).distinct().order_by(models.Record.type))
    return [r[0] for r in res]


async def get_domains(session: AsyncSession) -> list[str]:
    res = await session.execute(
        select(models.Record.domain).distinct().where(models.Record.domain.is_not(None)).order_by(models.Record.domain)
    )
    return [r[0] for r in res]


async def stats(session: AsyncSession) -> dict[str, Any]:
    total = (await session.execute(select(func.count()).select_from(models.Record))).scalar() or 0
    by_status: dict[str, int] = {
        k: int(v)
        for k, v in (
            await session.execute(select(models.Record.status, func.count()).group_by(models.Record.status))
        ).all()
    }
    by_type: dict[str, int] = {
        k: int(v)
        for k, v in (
            await session.execute(
                select(models.Record.type, func.count()).group_by(models.Record.type).order_by(models.Record.type)
            )
        ).all()
    }
    by_domain: dict[str, int] = {
        k: int(v)
        for k, v in (
            await session.execute(
                select(models.Record.domain, func.count())
                .where(models.Record.domain.is_not(None))
                .group_by(models.Record.domain)
            )
        ).all()
    }
    by_model: dict[str, int] = {
        (k or "unknown"): int(v)
        for k, v in (
            await session.execute(
                select(models.Record.source_model, func.count())
                .where(models.Record.source_model.is_not(None))
                .group_by(models.Record.source_model)
            )
        ).all()
    }
    edited = (
        await session.execute(select(func.count()).select_from(models.Record).where(models.Record.edit_count > 0))
    ).scalar() or 0
    verified = by_status.get("verified", 0)
    coverage_avg = (
        await session.execute(select(func.avg(models.Record.coverage)).where(models.Record.coverage.is_not(None)))
    ).scalar()
    recent = (
        await session.execute(
            select(func.date(models.Record.created_at), func.count())
            .group_by(func.date(models.Record.created_at))
            .order_by(func.date(models.Record.created_at).desc())
            .limit(30)
        )
    ).all()
    return {
        "total": total,
        "by_status": by_status,
        "by_type": by_type,
        "by_domain": by_domain,
        "by_model": by_model,
        "edited": int(edited),
        "verified": int(verified),
        "coverage_avg": float(coverage_avg) if coverage_avg is not None else None,
        "per_day": [{str(d): int(c)} for d, c in recent],
    }
