from unittest.mock import AsyncMock, MagicMock

import pytest

from magnus.application.start import build_start_reply
from magnus.telegram.handlers.start import start_command


def test_build_start_reply_is_non_empty():
    text = build_start_reply()
    assert "Magnus" in text
    assert len(text) > 40


@pytest.mark.asyncio
async def test_start_command_replies():
    update = MagicMock()
    update.message = MagicMock()
    update.message.reply_text = AsyncMock()
    context = MagicMock()

    await start_command(update, context)

    update.message.reply_text.assert_awaited_once()
    args, _ = update.message.reply_text.await_args
    assert args[0] == build_start_reply()
