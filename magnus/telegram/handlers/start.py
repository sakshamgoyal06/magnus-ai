from telegram import Update
from telegram.ext import ContextTypes

from magnus.application.start import build_start_reply


async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    if update.message is None:
        return
    await update.message.reply_text(build_start_reply())
