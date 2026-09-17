# Deploy Magnus on Railway

Magnus on Railway is a **single Python service**: FastAPI (health + future HTTP) and **Telegram long-polling** in one process (`magnus.api.main` lifespan). PostgreSQL is **external** (Supabase recommended); schema is applied with **Alembic** on each deploy.

## Repo layout (runtime-relevant)

| Path | Role |
|------|------|
| `magnus/api/main.py` | ASGI app, lifespan, Uvicorn entry (`magnus.api.main:app`) |
| `magnus/telegram/` | Telegram adapter only (`/start` → `application.start`) |
| `magnus/application/` | Use cases (no I/O) |
| `magnus/infrastructure/` | Config, DB engine, Alembic models, production validation |
| `alembic/` | Migrations (required before `/health` passes) |
| `railpack.json` / `railway.toml` | Railpack start command, pre-deploy migrate, health check |

Empty packages (`domain/`, `repositories/`, `jobs/`, …) are Day 2+ placeholders — not a deploy blocker.

## Config in this repository

- **`railpack.json`** — `deploy.startCommand` (fixes Railpack “No start command detected”).
- **`railway.toml`** — `preDeployCommand`, `startCommand`, `healthcheckPath=/health`.

Railway injects **`PORT`**; the app reads it via settings (default 8000 locally).

## Required Railway variables

Set these on the **Magnus service** (not committed to git):

| Variable | Required | Purpose |
|----------|----------|---------|
| `DATABASE_URL` | **Yes** | Async SQLAlchemy URL (`postgresql+asyncpg://…`). Use Supabase direct or session pooler. |
| `TELEGRAM_BOT_TOKEN` | **Yes** in production | From BotFather; without it polling does not start. |
| `APP_ENV` | **Yes** | Set to `production` on Railway (enables production checks). |
| `LOG_LEVEL` | Recommended | e.g. `INFO` |
| `PORT` | Auto | Set by Railway; do not override unless debugging. |

### `DATABASE_URL` (Supabase)

Async form (Magnus runtime):

```text
postgresql+asyncpg://postgres:YOUR_PASSWORD@db.<project-ref>.supabase.co:5432/postgres
```

If the password has special characters, URL-encode them. Supabase requires TLS; the app adds SSL for `*.supabase.co` hosts and Alembic uses `sslmode=require` on the sync URL.

**Session pooler (IPv4-friendly):**

```text
postgresql+asyncpg://postgres.<project-ref>:YOUR_PASSWORD@aws-0-<region>.pooler.supabase.com:5432/postgres
```

Remove any old **Railway Postgres** plugin `DATABASE_URL` so only Supabase is used.

### Variables **not** used by the Python service today

These are fine to omit for the Telegram MVP:

- `OPENAI_API_KEY` / other LLM keys (Day 5+)
- `SUPABASE_URL` / Supabase anon key (only for a future web client, not `magnus-api`)

## Production startup checks

When `APP_ENV=production`, the app **refuses to start** if:

- `TELEGRAM_BOT_TOKEN` is missing
- `DATABASE_URL` still points at `localhost` / `127.0.0.1`

This avoids a silent “API up, bot dead” deploy.

## Telegram on Railway

- **Mode:** long-polling (`python-telegram-bot`), not webhooks.
- **Replicas:** keep **one replica**. Multiple instances will fight over the same bot token.
- **Behavior today:** `/start` returns the welcome message from `application.start`. General chat is **not persisted** until later build days (no `chat_records` table on `main` yet).
- **Zero-downtime overlap:** brief dual polling during deploy overlap can happen; keep overlap small if you see duplicate handler quirks.

## Deploy flow

1. Push to the branch Railway tracks (usually `main`).
2. **Pre-deploy:** `uv run alembic upgrade head`
3. **Start:** `uv run uvicorn magnus.api.main:app --host 0.0.0.0 --port $PORT`
4. **Health:** Railway hits `GET /health` (DB `SELECT 1`).

## Post-deploy verification

1. Railway deploy logs: `Telegram bot polling started` and no `TELEGRAM_BOT_TOKEN` warnings.
2. `GET https://<your-railway-domain>/health` → `{"status":"ok","database":"connected"}`.
3. Telegram: message your bot **`/start`** → welcome text.

## Common failures

| Symptom | Likely cause |
|---------|----------------|
| Build: `No start command detected` | Missing `railpack.json` / wrong builder (use Railpack). |
| Crash on boot: `TELEGRAM_BOT_TOKEN is required` | Token not set or `APP_ENV` not `production` mismatch. |
| `/health` 503 | Wrong `DATABASE_URL`, SSL, or migrations not applied. |
| API healthy, bot silent | Token missing/wrong, or scaled to >1 replica. |
| Alembic pre-deploy fails | Sync URL / password / network to Supabase. |

## Local parity

```bash
cp .env.example .env
# set DATABASE_URL + TELEGRAM_BOT_TOKEN
uv run alembic upgrade head
uv run magnus-api
```

See [docs/ARCHITECTURE.md](ARCHITECTURE.md) for module boundaries.
