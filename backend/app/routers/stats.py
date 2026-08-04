from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from .. import crud
from ..db import get_session
from ..security import require_api_key

router = APIRouter(prefix="/api/v1", tags=["stats"], dependencies=[Depends(require_api_key)])


@router.get("/stats")
async def get_stats(session: AsyncSession = Depends(get_session)) -> dict:
    return await crud.stats(session)


@router.get("/meta")
async def get_meta(session: AsyncSession = Depends(get_session)) -> dict:
    return {
        "types": await crud.get_types(session),
        "domains": await crud.get_domains(session),
    }
