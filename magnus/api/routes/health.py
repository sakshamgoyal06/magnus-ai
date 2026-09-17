from fastapi import APIRouter, Request
from fastapi.responses import JSONResponse
from sqlalchemy.ext.asyncio import AsyncEngine

from magnus.infrastructure.database import check_database_connection

router = APIRouter(tags=["health"])


def _database_host(engine: AsyncEngine) -> str | None:
    try:
        return engine.url.host
    except Exception:  # noqa: BLE001 — diagnostics only
        return None


@router.get("/health")
async def health(request: Request) -> JSONResponse:
    engine: AsyncEngine = request.app.state.db_engine
    try:
        await check_database_connection(engine)
    except Exception as exc:  # noqa: BLE001 — surface DB failure in health payload
        payload: dict[str, str] = {
            "status": "unhealthy",
            "database": "disconnected",
            "detail": str(exc),
        }
        host = _database_host(engine)
        if host:
            payload["host"] = host
        return JSONResponse(status_code=503, content=payload)
    return JSONResponse(content={"status": "ok", "database": "connected"})
