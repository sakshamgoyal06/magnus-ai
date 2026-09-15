import asyncio
import logging

from telegram.ext import Application, ApplicationBuilder, CommandHandler

from magnus.telegram.handlers.start import start_command

logger = logging.getLogger(__name__)


def build_telegram_application(token: str) -> Application:
    app = ApplicationBuilder().token(token).build()
    app.add_handler(CommandHandler("start", start_command))
    return app


async def run_telegram_polling(application: Application) -> None:
    await application.updater.start_polling(drop_pending_updates=True)
    logger.info("Telegram updater polling")
    try:
        await asyncio.Future()
    except asyncio.CancelledError:
        await application.updater.stop()
        raise
