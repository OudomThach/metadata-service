from typing import Any

from fastapi import APIRouter, Depends, Response
from sqlalchemy.ext.asyncio import AsyncSession

from .. import crud
from ..db import get_session
from ..schemas import MetaOut
from ..security import require_auth

router = APIRouter(prefix="/api/v1", tags=["stats"], dependencies=[Depends(require_auth)])


@router.get("/stats")
async def get_stats(session: AsyncSession = Depends(get_session), response: Response = None) -> dict[str, Any]:  # type: ignore[assignment]
    response.headers["Cache-Control"] = "public, max-age=10"
    return await crud.stats(session)


@router.get("/meta", response_model=MetaOut)
async def get_meta(session: AsyncSession = Depends(get_session), response: Response = None) -> MetaOut:  # type: ignore[assignment]
    response.headers["Cache-Control"] = "public, max-age=60"
    return MetaOut(types=await crud.get_types(session), domains=await crud.get_domains(session))
