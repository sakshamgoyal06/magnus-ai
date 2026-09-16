from magnus.infrastructure.config import Settings

_LOCAL_DB_MARKERS = ("localhost", "127.0.0.1")


def validate_production_settings(settings: Settings) -> None:
    """Fail fast when production is misconfigured (Railway deploy)."""
    if settings.app_env.lower() != "production":
        return

    if not settings.telegram_bot_token:
        raise RuntimeError(
            "TELEGRAM_BOT_TOKEN is required when APP_ENV=production "
            "(Telegram polling will not start without it)."
        )

    db_url = settings.database_url.lower()
    if any(marker in db_url for marker in _LOCAL_DB_MARKERS):
        raise RuntimeError(
            "DATABASE_URL must not point at localhost when APP_ENV=production. "
            "Set the Supabase (or other hosted) Postgres async URL in Railway variables."
        )
