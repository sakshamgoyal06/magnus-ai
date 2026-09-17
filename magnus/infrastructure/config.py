from functools import lru_cache

from pydantic import Field, field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict

_ASYNC_DRIVER = "postgresql+asyncpg://"


def normalize_database_url(url: str) -> str:
    """Map Supabase/Railway-style URLs to SQLAlchemy asyncpg (we do not ship psycopg2)."""
    trimmed = url.strip()
    if trimmed.startswith(_ASYNC_DRIVER):
        return trimmed
    if trimmed.startswith("postgresql+psycopg://"):
        return _ASYNC_DRIVER + trimmed.removeprefix("postgresql+psycopg://")
    if trimmed.startswith("postgresql://"):
        return _ASYNC_DRIVER + trimmed.removeprefix("postgresql://")
    if trimmed.startswith("postgres://"):
        return _ASYNC_DRIVER + trimmed.removeprefix("postgres://")
    return trimmed


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
        populate_by_name=True,
    )

    database_url: str = Field(
        default="postgresql+asyncpg://magnus:magnus@localhost:5432/magnus_dev",
        description="Async SQLAlchemy database URL",
    )

    @field_validator("database_url", mode="before")
    @classmethod
    def _normalize_database_url(cls, value: object) -> object:
        if isinstance(value, str):
            return normalize_database_url(value)
        return value

    telegram_bot_token: str | None = Field(
        default=None,
        description="Telegram bot token; polling starts when set",
    )
    app_env: str = Field(default="development", alias="APP_ENV")
    log_level: str = Field(default="INFO")
    port: int = Field(default=8000, alias="PORT")


@lru_cache
def get_settings() -> Settings:
    return Settings()
