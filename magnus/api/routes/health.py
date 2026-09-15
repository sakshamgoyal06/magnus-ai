from fastapi import APIRouter, Request
from fastapi.responses import JSONResponse
from sqlalchemy.ext.asyncio import AsyncEngine

from magnus.infrastructure.database import check_database_connection

router = APIRouter(tags=["health"])


@router.get("/health")
async def health(request: Request) -> JSONResponse:
    engine: AsyncEngine = request.app.state.db_engine
    try:
        await check_database_connection(engine)
    except Exception as exc:  # noqa: BLE001 — surface DB failure in health payload
        return JSONResponse(
            status_code=503,
            content={"status": "unhealthy", "database": "disconnected", "detail": str(exc)},
        )
    return JSONResponse(content={"status": "ok", "database": "connected"})
