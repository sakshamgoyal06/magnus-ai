import pytest


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
