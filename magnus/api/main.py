import asyncio
import logging
from contextlib import asynccontextmanager

import uvicorn
from fastapi import FastAPI

from magnus.api.routes.health import router as health_router
from magnus.infrastructure.config import get_settings
from magnus.infrastructure.database import create_engine, create_session_factory
from magnus.infrastructure.startup import validate_production_settings
from magnus.telegram.bot import build_telegram_application, run_telegram_polling

logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    settings = get_settings()
    validate_production_settings(settings)
    engine = create_engine(settings)
    app.state.db_engine = engine
    app.state.session_factory = create_session_factory(engine)
    logger.info("Database driver: %s", engine.url.drivername)
    logger.info("Database host: %s", engine.url.host)

    polling_task: asyncio.Task | None = None
    if settings.telegram_bot_token:
        tg_app = build_telegram_application(settings.telegram_bot_token)
        await tg_app.initialize()
        await tg_app.start()
        polling_task = asyncio.create_task(run_telegram_polling(tg_app))
        app.state.telegram_app = tg_app
        logger.info("Telegram bot polling started")
    else:
        app.state.telegram_app = None
        logger.warning("TELEGRAM_BOT_TOKEN not set; Telegram polling disabled")

    yield

    if polling_task is not None:
        polling_task.cancel()
        try:
            await polling_task
        except asyncio.CancelledError:
            pass
    tg_app = getattr(app.state, "telegram_app", None)
    if tg_app is not None:
        await tg_app.stop()
        await tg_app.shutdown()
    await engine.dispose()


def create_app() -> FastAPI:
    app = FastAPI(title="Magnus", version="0.1.0", lifespan=lifespan)
    app.include_router(health_router)
    return app


app = create_app()


def run() -> None:
    settings = get_settings()
    uvicorn.run(
        "magnus.api.main:app",
        host="0.0.0.0",
        port=settings.port,
        reload=settings.app_env == "development",
        log_level=settings.log_level.lower(),
    )


if __name__ == "__main__":
    run()
