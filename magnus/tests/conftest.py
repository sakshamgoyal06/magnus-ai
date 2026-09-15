import os
import subprocess
import sys

import pytest
from httpx import ASGITransport, AsyncClient

# Tests assume local PostgreSQL; override via DATABASE_URL in CI if needed.
os.environ.setdefault(
    "DATABASE_URL",
    "postgresql+asyncpg://magnus:magnus@localhost:5432/magnus_dev",
)
os.environ.pop("TELEGRAM_BOT_TOKEN", None)


@pytest.fixture(scope="session", autouse=True)
def apply_migrations() -> None:
    result = subprocess.run(
        [sys.executable, "-m", "alembic", "upgrade", "head"],
        capture_output=True,
        text=True,
        check=False,
    )
    if result.returncode != 0:
        pytest.fail(
            "alembic upgrade head failed:\n"
            f"{result.stdout}\n{result.stderr}\n"
            "Ensure PostgreSQL is running and DATABASE_URL is correct."
        )


@pytest.fixture
async def api_client():
    from magnus.api.main import create_app

    app = create_app()
    async with app.router.lifespan_context(app):
        transport = ASGITransport(app=app)
        async with AsyncClient(transport=transport, base_url="http://test") as client:
            yield client
