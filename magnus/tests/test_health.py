import json
from unittest.mock import AsyncMock, MagicMock, patch

import pytest
from starlette.requests import Request

from magnus.api.routes.health import health
from magnus.infrastructure.config import Settings
from magnus.infrastructure.database import check_database_connection, create_engine


@pytest.mark.asyncio
async def test_check_database_connection_async_propagates_connect_errors():
    """Same async path /health uses; errors must surface, not hang or swallow."""
    settings = Settings(
        database_url="postgresql+asyncpg://u:p@nonexistent.invalid:5432/db",
        _env_file=None,
    )
    engine = create_engine(settings)
    try:
        with pytest.raises(OSError, match="Name or service not known|getaddrinfo"):
            await check_database_connection(engine)
    finally:
        await engine.dispose()


@pytest.mark.asyncio
async def test_health_maps_db_failure_to_503_json():
    mock_engine = MagicMock()
    mock_engine.url.host = "bad.example.com"
    mock_request = MagicMock(spec=Request)
    mock_request.app.state.db_engine = mock_engine

    with patch(
        "magnus.api.routes.health.check_database_connection",
        AsyncMock(side_effect=OSError(-2, "Name or service not known")),
    ):
        response = await health(mock_request)

    assert response.status_code == 503
    body = json.loads(response.body)
    assert body["status"] == "unhealthy"
    assert body["database"] == "disconnected"
    assert "Name or service not known" in body["detail"]
    assert body["host"] == "bad.example.com"


@pytest.mark.asyncio
async def test_health_returns_200_when_db_check_succeeds():
    mock_engine = MagicMock()
    mock_engine.url.host = "db.example.com"
    mock_request = MagicMock(spec=Request)
    mock_request.app.state.db_engine = mock_engine

    with patch(
        "magnus.api.routes.health.check_database_connection",
        AsyncMock(return_value=True),
    ):
        response = await health(mock_request)

    assert response.status_code == 200
    body = json.loads(response.body)
    assert body == {"status": "ok", "database": "connected"}


@pytest.mark.asyncio
async def test_health_live_returns_ok_without_database(api_client):
    response = await api_client.get("/health/live")
    assert response.status_code == 200
    assert response.json()["status"] == "ok"


@pytest.mark.asyncio
async def test_health_returns_ok_when_database_connected(api_client):
    response = await api_client.get("/health")
    assert response.status_code == 200
    body = response.json()
    assert body["status"] == "ok"
    assert body["database"] == "connected"
