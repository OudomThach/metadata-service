import asyncio
import logging
import os
from collections.abc import AsyncIterator, Awaitable, Callable
from contextlib import asynccontextmanager
from datetime import datetime, timedelta, timezone

from anyio import Path as AsyncPath
from fastapi import FastAPI, Request, Response
from fastapi.exceptions import RequestValidationError
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse, HTMLResponse
from fastapi.staticfiles import StaticFiles
from sqlalchemy import CursorResult, delete
from starlette.exceptions import HTTPException as StarletteHTTPException

from .config import cors_list, settings
from .db import SessionLocal
from .errors import APIError, api_error_handler, http_exception_handler, validation_error_handler
from .models import Record
from .routers import (
    admin,
    auth,
    categories,
    collections,
    datasets,
    export,
    health,
    organizations,
    records,
    stats,
    webhooks,
)
from .security import seed_admin

log = logging.getLogger("metadata.main")

_CLEANUP_INTERVAL_SECONDS = 24 * 60 * 60


async def _purge_raw_drafts() -> None:
    """Nightly sweep: delete unverified `raw` drafts older than the TTL so the
    queue never fills with abandoned extractions. Logs the purge count."""
    ttl = settings.draft_ttl_days
    if ttl <= 0:
        return
    cutoff = datetime.now(timezone.utc) - timedelta(days=ttl)
    try:
        async with SessionLocal() as session:
            result = await session.execute(delete(Record).where(Record.status == "raw", Record.created_at < cutoff))
            await session.commit()
            deleted = result.rowcount if isinstance(result, CursorResult) else None
            if deleted:
                log.info("purged %d raw draft(s) older than %d days", deleted, ttl)
    except Exception as exc:  # noqa: BLE001
        log.warning("cleanup sweep failed: %s", exc)


async def _cleanup_loop() -> None:
    while True:
        await asyncio.sleep(_CLEANUP_INTERVAL_SECONDS)
        await _purge_raw_drafts()


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncIterator[None]:
    await seed_admin()
    task = asyncio.create_task(_cleanup_loop())
    yield
    task.cancel()


app = FastAPI(
    title=settings.app_name,
    version=settings.version,
    docs_url="/api/docs",
    openapi_url="/api/openapi.json",
    lifespan=lifespan,
)

origins = cors_list()
if origins:
    app.add_middleware(
        CORSMiddleware,
        allow_origins=origins,
        allow_methods=["*"],
        allow_headers=["*"],
    )

app.add_exception_handler(APIError, api_error_handler)
app.add_exception_handler(RequestValidationError, validation_error_handler)
app.add_exception_handler(StarletteHTTPException, http_exception_handler)

app.include_router(health.router)
app.include_router(auth.router)
app.include_router(records.router)
app.include_router(export.router)
app.include_router(stats.router)
app.include_router(webhooks.router)
app.include_router(organizations.router)
app.include_router(categories.router)
app.include_router(collections.router)
app.include_router(datasets.router)
app.include_router(admin.router)


@app.middleware("http")
async def api_meta_alias(request: Request, call_next: Callable[[Request], Awaitable[Response]]) -> Response:
    # The portal is served under /portal on the shared Romdoul host, where the
    # metadata API lives behind /api-meta (romdoul nginx). The same /api-meta
    # prefix must also work when the service is hit directly (:8095), so the
    # portal can use one base URL everywhere. Strip the prefix internally.
    if request.url.path.startswith("/api-meta/"):
        request.scope["path"] = request.url.path[len("/api-meta") :]
        request.scope["raw_path"] = request.scope["path"].encode()
    return await call_next(request)


INDEX = AsyncPath(settings.static_dir) / "index.html"


@app.get("/", include_in_schema=False, response_model=None)
async def index() -> FileResponse | HTMLResponse:
    if await INDEX.exists():
        return FileResponse(str(INDEX))
    return HTMLResponse("<h3>metadata-service API</h3><p>Docs: <a href='/api/docs'>/api/docs</a></p>")


if os.path.isdir(settings.static_dir):
    # Portal assets (built with base /portal/ so they don't collide with the
    # Romdoul SPA's own /assets on the shared nginx host).
    app.mount("/portal", StaticFiles(directory=settings.static_dir, html=True), name="portal")
    app.mount("/assets", StaticFiles(directory=os.path.join(settings.static_dir, "assets")), name="assets")
