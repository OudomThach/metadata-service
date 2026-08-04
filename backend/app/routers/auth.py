from fastapi import APIRouter, Depends, Header, HTTPException
from pydantic import BaseModel

from ..db import get_session
from ..models import User
from ..security import Actor, create_session, require_auth, revoke_token, user_by_token, verify_password
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

router = APIRouter(prefix="/api/v1/auth", tags=["auth"])


class LoginIn(BaseModel):
    username: str
    password: str


class UserOut(BaseModel):
    username: str
    role: str


@router.post("/login")
async def login(payload: LoginIn, session: AsyncSession = Depends(get_session)) -> dict:
    row = await session.execute(select(User).where(User.username == payload.username))
    user = row.scalar_one_or_none()
    if not user or not verify_password(payload.password, user.password_hash):
        raise HTTPException(status_code=401, detail="Invalid username or password")
    token = await create_session(session, user)
    return {"token": token, "user": {"username": user.username, "role": user.role}}


@router.post("/logout", response_model=None)
async def logout(
    actor: Actor = Depends(require_auth),
    x_session_token: str | None = Header(default=None),
    session: AsyncSession = Depends(get_session),
) -> dict:
    if actor.kind == "user" and x_session_token:
        await revoke_token(session, x_session_token)
    return {"ok": True}


@router.get("/me", response_model=UserOut)
async def me(actor: Actor = Depends(require_auth)) -> UserOut:
    if actor.kind == "key":
        return UserOut(username=f"key:{actor.name}", role="admin")
    return UserOut(username=actor.name, role=actor.role)
