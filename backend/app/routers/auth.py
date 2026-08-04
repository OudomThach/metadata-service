from fastapi import APIRouter, Depends, Header, HTTPException
from pydantic import BaseModel

from ..db import get_session
from ..models import User
from ..security import Actor, create_session, hash_password, require_auth, revoke_token, verify_password
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

router = APIRouter(prefix="/api/v1/auth", tags=["auth"])


class LoginIn(BaseModel):
    username: str
    password: str


class CreateUserIn(BaseModel):
    username: str
    password: str
    role: str = "viewer"


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


@router.post("/users", status_code=201, response_model=UserOut)
async def create_user(
    payload: CreateUserIn,
    actor: Actor = Depends(require_auth),
    session: AsyncSession = Depends(get_session),
) -> UserOut:
    if actor.role != "admin":
        raise HTTPException(status_code=403, detail="Admin role required")
    if payload.role not in ("admin", "viewer"):
        raise HTTPException(status_code=422, detail="role must be admin or viewer")
    if not payload.username.strip() or len(payload.password) < 8:
        raise HTTPException(status_code=422, detail="username required, password at least 8 chars")
    exists = await session.execute(select(User).where(User.username == payload.username.strip()))
    if exists.scalar_one_or_none():
        raise HTTPException(status_code=409, detail="username already exists")
    user = User(
        username=payload.username.strip(),
        password_hash=hash_password(payload.password),
        role=payload.role,
    )
    session.add(user)
    await session.commit()
    return UserOut(username=user.username, role=user.role)
