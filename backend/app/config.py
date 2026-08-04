from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", env_prefix="METADATA_", extra="ignore")

    app_name: str = "metadata-service"
    version: str = "1.0.0"
    database_url: str = "postgresql+asyncpg://metadata:metadata@localhost:5433/metadata"
    api_keys: str = ""  # comma-separated; empty = open access (dev mode)
    cors_origins: str = ""  # comma-separated, empty = same-origin only
    static_dir: str = "static"


settings = Settings()


def authorized_keys() -> list[str]:
    return [k.strip() for k in settings.api_keys.split(",") if k.strip()]


def cors_list() -> list[str]:
    return [o.strip() for o in settings.cors_origins.split(",") if o.strip()]
