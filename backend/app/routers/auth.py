from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

from ..config import authorized_keys

router = APIRouter(prefix="/api/v1/auth", tags=["auth"])


class LoginIn(BaseModel):
    password: str


@router.post("/login")
async def login(payload: LoginIn) -> dict:
    keys = authorized_keys()
    if not keys:
        raise HTTPException(status_code=403, detail="Authentication is not configured on this instance")
    if payload.password not in keys:
        raise HTTPException(status_code=401, detail="Invalid password")
    return {"token": payload.password}
