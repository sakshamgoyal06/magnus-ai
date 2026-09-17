import os

import pytest
from httpx import ASGITransport, AsyncClient

# Tests assume local PostgreSQL; override via DATABASE_URL in CI if needed.
os.environ.setdefault(
    "DATABASE_URL",
    "postgresql+asyncpg://magnus:magnus@localhost:5432/magnus_dev",
)
os.environ.pop("TELEGRAM_BOT_TOKEN", None)


@pytest.fixture(scope="session")
def db_available() -> None:
    """Ensure DATABASE_URL is reachable (SELECT 1). No application tables required."""
    from magnus.infrastructure.config import get_settings
    from magnus.infrastructure.database import check_database_connection, create_engine

    engine = create_engine(get_settings())
    try:
        import asyncio

        asyncio.run(check_database_connection(engine))
    except Exception as exc:
        pytest.fail(
            f"Database not reachable at DATABASE_URL: {exc}\n"
            "Start PostgreSQL (e.g. docker compose up -d db) or set DATABASE_URL."
        )
    finally:
        import asyncio

        asyncio.run(engine.dispose())


@pytest.fixture
async def api_client(db_available):
    from magnus.api.main import create_app

    app = create_app()
    async with app.router.lifespan_context(app):
        transport = ASGITransport(app=app)
        async with AsyncClient(transport=transport, base_url="http://test") as client:
            yield client
