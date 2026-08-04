from fastapi import Header, HTTPException

from .config import authorized_keys


def require_api_key(x_api_key: str | None = Header(default=None)) -> None:
    keys = authorized_keys()
    if not keys:
        return  # dev mode: open access
    if not x_api_key or x_api_key not in keys:
        raise HTTPException(status_code=401, detail="Invalid or missing X-API-Key")
