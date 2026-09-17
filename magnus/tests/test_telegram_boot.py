import asyncio
from unittest.mock import AsyncMock, MagicMock, patch

import pytest

from magnus.api.main import create_app


async def _polling_until_cancelled(_application):
    try:
        await asyncio.Future()
    except asyncio.CancelledError:
        raise


@pytest.mark.asyncio
async def test_lifespan_starts_telegram_when_token_configured():
    mock_tg = MagicMock()
    mock_tg.initialize = AsyncMock()
    mock_tg.start = AsyncMock()
    mock_tg.stop = AsyncMock()
    mock_tg.shutdown = AsyncMock()

    mock_engine = MagicMock()
    mock_engine.dispose = AsyncMock()

    with (
        patch("magnus.api.main.get_settings") as settings_mock,
        patch("magnus.api.main.build_telegram_application", return_value=mock_tg) as build_mock,
        patch("magnus.api.main.run_telegram_polling", side_effect=_polling_until_cancelled),
        patch("magnus.api.main.create_engine", return_value=mock_engine),
    ):
        settings = MagicMock()
        settings.telegram_bot_token = "test-token"
        settings.app_env = "test"
        settings.log_level = "INFO"
        settings.port = 8000
        settings.database_url = "postgresql+asyncpg://magnus:magnus@localhost:5432/magnus_dev"
        settings_mock.return_value = settings

        app = create_app()
        async with app.router.lifespan_context(app):
            build_mock.assert_called_once_with("test-token")
            mock_tg.initialize.assert_awaited_once()
            mock_tg.start.assert_awaited_once()

        mock_tg.stop.assert_awaited_once()
        mock_tg.shutdown.assert_awaited_once()
