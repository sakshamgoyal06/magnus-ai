from magnus.infrastructure.config import Settings


def test_settings_load_defaults():
    settings = Settings(_env_file=None)
    assert "postgresql" in settings.database_url
    assert settings.sync_database_url.startswith("postgresql+psycopg://")


def test_sync_database_url_converts_async_driver():
    settings = Settings(
        database_url="postgresql+asyncpg://user:pass@localhost/db",
        _env_file=None,
    )
    assert settings.sync_database_url == "postgresql+psycopg://user:pass@localhost/db"
