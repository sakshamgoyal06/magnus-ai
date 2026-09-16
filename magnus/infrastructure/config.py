from functools import lru_cache

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )

    database_url: str = Field(
        default="postgresql+asyncpg://magnus:magnus@localhost:5432/magnus_dev",
        description="Async SQLAlchemy database URL",
    )
    telegram_bot_token: str | None = Field(
        default=None,
        description="Telegram bot token; polling starts when set",
    )
    app_env: str = Field(default="development", alias="APP_ENV")
    log_level: str = Field(default="INFO")
    port: int = Field(default=8000, alias="PORT")

    @property
    def sync_database_url(self) -> str:
        """Alembic uses a synchronous driver."""
        url = self.database_url
        if url.startswith("postgresql+asyncpg://"):
            return url.replace("postgresql+asyncpg://", "postgresql+psycopg://", 1)
        return url


@lru_cache
def get_settings() -> Settings:
    return Settings()
