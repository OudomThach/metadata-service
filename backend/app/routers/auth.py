from typing import Any

from fastapi import APIRouter, Depends, Header
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from ..constants import USER_ROLES
from ..db import get_session
from ..errors import APIError
from ..models import User
from ..schemas import CreateUserIn, LoginIn, PasswordChangeIn, UpdateUserIn, UserOut
from ..security import Actor, create_session, hash_password, require_auth, revoke_token, verify_password

router = APIRouter(prefix="/api/v1/auth", tags=["auth"])


def _require_admin(actor: Actor) -> None:
    if actor.role != "admin":
        raise APIError(403, "forbidden", "Admin role required")


def _validate_role(role: str) -> None:
    if role not in USER_ROLES:
        raise APIError(422, "invalid_role", f"role must be one of {sorted(USER_ROLES)}")


@router.post("/login", response_model=dict)
async def login(payload: LoginIn, session: AsyncSession = Depends(get_session)) -> dict[str, Any]:
    row = await session.execute(select(User).where(User.username == payload.username))
    user = row.scalar_one_or_none()
    if not user or not verify_password(payload.password, user.password_hash):
        raise APIError(401, "invalid_credentials", "Invalid username or password")
    token = await create_session(session, user)
    return {"token": token, "user": {"username": user.username, "role": user.role}}


@router.post("/logout", response_model=dict)
async def logout(
    actor: Actor = Depends(require_auth),
    x_session_token: str | None = Header(default=None),
    session: AsyncSession = Depends(get_session),
) -> dict[str, Any]:
    if actor.kind == "user" and x_session_token:
        await revoke_token(session, x_session_token)
    return {"ok": True}


@router.get("/me", response_model=UserOut)
async def me(actor: Actor = Depends(require_auth)) -> UserOut:
    if actor.kind == "key":
        return UserOut(id=0, username=f"key:{actor.name}", role="admin")
    return UserOut(id=0, username=actor.name, role=actor.role)


@router.post("/me/password", response_model=dict)
async def change_password(
    payload: PasswordChangeIn,
    actor: Actor = Depends(require_auth),
    session: AsyncSession = Depends(get_session),
) -> dict[str, Any]:
    if actor.kind != "user":
        raise APIError(403, "forbidden", "API-key actors cannot change passwords")
    row = await session.execute(select(User).where(User.username == actor.name))
    user = row.scalar_one_or_none()
    if not user or not verify_password(payload.current_password, user.password_hash):
        raise APIError(401, "invalid_credentials", "Current password is incorrect")
    user.password_hash = hash_password(payload.new_password)
    await session.commit()
    return {"ok": True}


@router.post("/users", status_code=201, response_model=UserOut)
async def create_user(
    payload: CreateUserIn,
    actor: Actor = Depends(require_auth),
    session: AsyncSession = Depends(get_session),
) -> UserOut:
    _require_admin(actor)
    _validate_role(payload.role)
    username = payload.username.strip()
    if not username or len(payload.password) < 8:
        raise APIError(422, "validation_error", "username required, password at least 8 chars")
    exists = await session.execute(select(User).where(User.username == username))
    if exists.scalar_one_or_none():
        raise APIError(409, "duplicate", "username already exists")
    user = User(
        username=username,
        password_hash=hash_password(payload.password),
        role=payload.role,
        organization_id=payload.organization_id,
    )
    session.add(user)
    await session.commit()
    return UserOut(id=user.id, username=user.username, role=user.role, organization_id=user.organization_id)


@router.get("/users", response_model=list[UserOut])
async def list_users(
    actor: Actor = Depends(require_auth),
    session: AsyncSession = Depends(get_session),
) -> list[UserOut]:
    _require_admin(actor)
    rows = await session.execute(select(User).order_by(User.username))
    return [
        UserOut(id=u.id, username=u.username, role=u.role, organization_id=u.organization_id) for u in rows.scalars()
    ]


@router.patch("/users/{user_id:int}", response_model=UserOut)
async def update_user(
    user_id: int,
    payload: UpdateUserIn,
    actor: Actor = Depends(require_auth),
    session: AsyncSession = Depends(get_session),
) -> UserOut:
    _require_admin(actor)
    user = await session.get(User, user_id)
    if not user:
        raise APIError(404, "not_found", "user not found")
    if payload.role is not None:
        _validate_role(payload.role)
        user.role = payload.role
    if payload.organization_id is not None:
        user.organization_id = payload.organization_id
    await session.commit()
    return UserOut(id=user.id, username=user.username, role=user.role, organization_id=user.organization_id)


@router.delete("/users/{user_id:int}", response_model=None, status_code=204)
async def delete_user(
    user_id: int,
    actor: Actor = Depends(require_auth),
    session: AsyncSession = Depends(get_session),
) -> None:
    _require_admin(actor)
    user = await session.get(User, user_id)
    if not user:
        raise APIError(404, "not_found", "user not found")
    if user.username == actor.name:
        raise APIError(422, "validation_error", "cannot delete yourself")
    await session.delete(user)
    await session.commit()
