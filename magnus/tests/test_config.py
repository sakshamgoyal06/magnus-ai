from magnus.infrastructure.config import Settings, normalize_database_url


def test_settings_load_defaults():
    settings = Settings(_env_file=None)
    assert settings.database_url.startswith("postgresql+asyncpg://")
    assert settings.app_env == "development"


def test_normalize_database_url_from_postgresql_scheme():
    raw = "postgresql://postgres:secret@aws-0-us-east-1.pooler.supabase.com:5432/postgres"
    assert normalize_database_url(raw) == raw.replace("postgresql://", "postgresql+asyncpg://", 1)


def test_normalize_database_url_from_postgres_scheme():
    raw = "postgres://postgres:secret@host:5432/postgres"
    assert normalize_database_url(raw) == "postgresql+asyncpg://postgres:secret@host:5432/postgres"


def test_settings_normalize_supabase_style_database_url():
    settings = Settings(
        database_url="postgresql://postgres:secret@db.example.supabase.co:5432/postgres",
        _env_file=None,
    )
    assert settings.database_url.startswith("postgresql+asyncpg://")


def test_port_reads_from_port_env(monkeypatch):
    monkeypatch.setenv("PORT", "3000")
    settings = Settings(_env_file=None)
    assert settings.port == 3000
