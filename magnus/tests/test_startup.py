import pytest

from magnus.infrastructure.config import Settings
from magnus.infrastructure.startup import validate_production_settings


def test_production_requires_telegram_token():
    settings = Settings(
        app_env="production",
        telegram_bot_token=None,
        database_url="postgresql+asyncpg://postgres:secret@db.example.supabase.co:5432/postgres",
        _env_file=None,
    )
    with pytest.raises(RuntimeError, match="TELEGRAM_BOT_TOKEN"):
        validate_production_settings(settings)


def test_production_rejects_local_database_url():
    settings = Settings(
        app_env="production",
        telegram_bot_token="123:abc",
        database_url="postgresql+asyncpg://magnus:magnus@localhost:5432/magnus_dev",
        _env_file=None,
    )
    with pytest.raises(RuntimeError, match="localhost"):
        validate_production_settings(settings)


def test_development_allows_missing_telegram_token():
    settings = Settings(
        app_env="development",
        telegram_bot_token=None,
        _env_file=None,
    )
    validate_production_settings(settings)


def test_sync_database_url_adds_sslmode_for_supabase():
    settings = Settings(
        database_url="postgresql+asyncpg://postgres:pass@db.uktsxijrewbqjcjnrfdv.supabase.co:5432/postgres",
        _env_file=None,
    )
    assert "sslmode=require" in settings.sync_database_url
    assert settings.sync_database_url.startswith("postgresql+psycopg://")
