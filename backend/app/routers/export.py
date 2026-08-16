import csv
import datetime as dt
import io
import json
from collections.abc import AsyncIterator
from typing import Any

from fastapi import APIRouter, Depends, Query
from fastapi.responses import JSONResponse, StreamingResponse
from sqlalchemy import Select, select
from sqlalchemy.ext.asyncio import AsyncSession

from .. import crud, models
from ..db import get_session

router = APIRouter(prefix="/api/v1", tags=["export"])


def _csv_headers() -> list[str]:
    return [
        "id",
        "type",
        "domain",
        "status",
        "business_date",
        "tags",
        "created_at",
        "created_by",
        "edited_at",
        "edited_by",
        "edit_count",
        "ingested_at",
        "source_filename",
        "source_model",
        "source_system",
        "source_page",
        "extracted_at",
        "validation_status",
        "pipeline_run_id",
        "pipeline_batch_id",
        "is_duplicate",
        "coverage",
        "data",
    ]


def _csv_row(r: models.Record) -> list[str]:
    return [
        r.id,
        r.type,
        r.domain or "",
        r.status,
        r.business_date.isoformat() if r.business_date else "",
        json.dumps(r.tags or [], ensure_ascii=False),
        r.created_at.isoformat() if r.created_at else "",
        r.created_by or "",
        r.edited_at.isoformat() if r.edited_at else "",
        r.edited_by or "",
        str(r.edit_count),
        r.ingested_at.isoformat() if r.ingested_at else "",
        r.source_filename or "",
        r.source_model or "",
        r.source_system or "",
        str(r.source_page) if r.source_page is not None else "",
        r.extracted_at.isoformat() if r.extracted_at else "",
        r.validation_status or "",
        r.pipeline_run_id or "",
        r.pipeline_batch_id or "",
        str(r.is_duplicate) if r.is_duplicate is not None else "",
        f"{r.coverage:.3f}" if r.coverage is not None else "",
        json.dumps(r.data or {}, ensure_ascii=False),
    ]


def _json_row(r: models.Record) -> dict[str, Any]:
    return crud.to_out(r).model_dump(mode="json")


async def _stream_csv(session: AsyncSession, stmt: Select[tuple[models.Record]]) -> StreamingResponse:
    """Stream rows from the DB in chunks so memory stays flat at any scale."""

    async def generate() -> AsyncIterator[str]:
        yield "\ufeff"  # BOM once — Excel-safe UTF-8
        buf = io.StringIO()
        writer = csv.writer(buf)
        writer.writerow(_csv_headers())
        yield buf.getvalue()
        buf.seek(0)
        buf.truncate(0)
        result = await session.stream(stmt.execution_options(yield_per=500))
        async for r in result.scalars():
            writer.writerow(_csv_row(r))
            yield buf.getvalue()
            buf.seek(0)
            buf.truncate(0)

    return StreamingResponse(
        generate(),
        media_type="text/csv; charset=utf-8",
        headers={"Content-Disposition": f'attachment; filename="records-{dt.date.today().isoformat()}.csv"'},
    )


async def _stream_jsonl(session: AsyncSession, stmt: Select[tuple[models.Record]]) -> StreamingResponse:
    async def generate() -> AsyncIterator[str]:
        result = await session.stream(stmt.execution_options(yield_per=500))
        async for r in result.scalars():
            yield json.dumps(_json_row(r), ensure_ascii=False) + "\n"

    return StreamingResponse(
        generate(),
        media_type="application/x-ndjson; charset=utf-8",
        headers={"Content-Disposition": f'attachment; filename="records-{dt.date.today().isoformat()}.jsonl"'},
    )


async def _stream_parquet(session: AsyncSession, stmt: Select[tuple[models.Record]]) -> StreamingResponse:
    """Stream records as a single Parquet file, writing row-groups from DB
    batches so memory stays flat at any scale (same shape as JSONL streaming)."""
    import io as _io

    import pyarrow as pa  # type: ignore[import-untyped]
    import pyarrow.parquet as pq  # type: ignore[import-untyped]

    def _to_table(rows: list[models.Record]) -> pa.Table:
        rows_out = [_json_row(r) for r in rows]
        if not rows_out:
            return pa.Table.from_arrays([], names=[])
        first = _json_row(rows[0])
        schema = pa.schema([pa.field(k, pa.string()) for k in first])
        cols = {k: [str(r.get(k, "")) for r in rows_out] for k in first}
        return pa.Table.from_pydict(cols, schema=schema)

    async def generate() -> AsyncIterator[bytes]:
        buf = _io.BytesIO()
        result = await session.stream(stmt.execution_options(yield_per=500))
        writer = None
        try:
            batch: list[models.Record] = []
            async for r in result.scalars():
                batch.append(r)
                if len(batch) >= 500:
                    table = _to_table(batch)
                    if writer is None:
                        writer = pq.ParquetWriter(buf, table.schema)
                    writer.write_table(table)
                    batch = []
            if batch:
                table = _to_table(batch)
                if writer is None:
                    writer = pq.ParquetWriter(buf, table.schema)
                writer.write_table(table)
            if writer is not None:
                writer.close()
            else:
                # No rows at all — emit an empty parquet with a dummy schema.
                empty = pa.Table.from_pydict({"id": []})
                pq.write_table(empty, buf)
            yield buf.getvalue()
        finally:
            if writer is not None:
                writer.close()

    return StreamingResponse(
        generate(),
        media_type="application/vnd.apache.parquet",
        headers={"Content-Disposition": f'attachment; filename="records-{dt.date.today().isoformat()}.parquet"'},
    )


@router.get("/export", response_model=None)
async def export(
    format: str = Query(pattern=r"^(csv|json|jsonl|parquet)$"),
    session: AsyncSession = Depends(get_session),
    type: str | None = Query(default=None),
    domain: str | None = Query(default=None),
    status: str | None = Query(default=None),
    tag: str | None = Query(default=None),
    business_from: dt.date | None = Query(default=None),
    business_to: dt.date | None = Query(default=None),
    created_from: dt.datetime | None = Query(default=None),
    created_to: dt.datetime | None = Query(default=None),
    edited_from: dt.datetime | None = Query(default=None),
    edited_to: dt.datetime | None = Query(default=None),
    q: str | None = Query(default=None, max_length=256),
) -> StreamingResponse | JSONResponse:
    stmt = crud.apply_filters(
        select(models.Record),
        dialect=session.get_bind().dialect.name,
        type=type,
        domain=domain,
        status=status,
        tag=tag,
        business_from=business_from,
        business_to=business_to,
        created_from=created_from,
        created_to=created_to,
        edited_from=edited_from,
        edited_to=edited_to,
        q=q,
    ).order_by(models.Record.created_at.desc())

    if format == "json":
        rows = (await session.execute(stmt)).scalars().all()
        return JSONResponse(content=[_json_row(r) for r in rows])

    if format == "jsonl":
        return await _stream_jsonl(session, stmt)

    if format == "parquet":
        return await _stream_parquet(session, stmt)

    return await _stream_csv(session, stmt)
