# Deploy Magnus on Railway

Canonical infrastructure facts live in [SOURCE_OF_TRUTH.md](SOURCE_OF_TRUTH.md). Schema workflow: [SUPABASE_MIGRATIONS.md](SUPABASE_MIGRATIONS.md).

Magnus on Railway is a **single Python service**: FastAPI (health + future HTTP) and **Telegram long-polling** in one process (`magnus.api.main` lifespan). PostgreSQL is **external** (Supabase project `magnus-ai` only). **Railway does not run migrations.**

## Repo layout (runtime-relevant)

| Path | Role |
|------|------|
| `magnus/api/main.py` | ASGI app, lifespan, Uvicorn entry (`magnus.api.main:app`) |
| `magnus/telegram/` | Telegram adapter only (`/start` → `application.start`) |
| `magnus/application/` | Use cases (no I/O) |
| `magnus/infrastructure/` | Config, DB engine, production validation |
| `supabase/migrations/` | Authoritative schema history (apply via Supabase CLI, not Railway) |
| `railpack.json` / `railway.toml` | Railpack start command, health check |

Empty packages (`domain/`, `repositories/`, `jobs/`, …) are Day 2+ placeholders — not a deploy blocker.

## Config in this repository

- **`railpack.json`** — `deploy.startCommand`.
- **`railway.toml`** — `startCommand`, `healthcheckPath=/health/live` (no pre-deploy migration command).

Railway injects **`PORT`**; the app reads it via settings (default 8000 locally).

## Required Railway variables

Set these on the **Magnus service** (not committed to git):

| Variable | Required | Purpose |
|----------|----------|---------|
| `DATABASE_URL` | **Yes** | Postgres URL for **asyncpg**. Prefer `postgresql+asyncpg://…`. Plain `postgresql://` / `postgres://` from Supabase Connect is rewritten at startup (Magnus does not install psycopg2). Use Supabase **session pooler** on Railway. |
| `TELEGRAM_BOT_TOKEN` | **Yes** in production | From BotFather; without it polling does not start. |
| `APP_ENV` | **Yes** | Set to `production` on Railway (enables production checks). |
| `LOG_LEVEL` | Recommended | e.g. `INFO` |
| `PORT` | Auto | Set by Railway; do not override unless debugging. |

### `DATABASE_URL` (Supabase)

Async form (Magnus runtime):

```text
postgresql+asyncpg://postgres:YOUR_PASSWORD@db.uktsxijrewbqjcjnrfdv.supabase.co:5432/postgres
```

If the password has special characters, URL-encode them. Supabase requires TLS; the app enables SSL for `*.supabase.co` and `*.pooler.supabase.com` hosts.

**Do not use the default Direct connection URI on Railway** unless your project has the Supabase IPv4 add-on. Direct hostnames are IPv6-first; Railway often fails with `[Errno -2] Name or service not known`. Use **Session pooler** from the Connect panel instead.

**Session pooler (IPv4-friendly):**

```text
postgresql+asyncpg://postgres.uktsxijrewbqjcjnrfdv:YOUR_PASSWORD@aws-0-us-east-1.pooler.supabase.com:5432/postgres
```

Remove any **Railway Postgres** plugin `DATABASE_URL` so only Supabase is used.

### Variables **not** used by the Python service today

- `OPENAI_API_KEY` / other LLM keys (Day 5+)
- `SUPABASE_URL` / Supabase anon key (future web client only, not `magnus-api`)

## Production startup checks

When `APP_ENV=production`, the app **refuses to start** if:

- `TELEGRAM_BOT_TOKEN` is missing
- `DATABASE_URL` still points at `localhost` / `127.0.0.1`

## Schema before or after deploy

1. Commit migration SQL under `supabase/migrations/`.
2. From a trusted environment: `supabase link --project-ref uktsxijrewbqjcjnrfdv` then `supabase db push`.
3. Push to the branch Railway tracks (`main`).
4. Railway **start only:** `uv run uvicorn magnus.api.main:app --host 0.0.0.0 --port $PORT`
5. Railway deploy health check: `GET /health/live` (process up only). After deploy, verify `GET /health` (includes DB `SELECT 1`).

## Telegram on Railway

- **Mode:** long-polling (`python-telegram-bot`), not webhooks.
- **Replicas:** keep **one replica**. During a deploy, Railway may briefly run **old + new** containers; both may poll until the old one stops → `telegram.error.Conflict` in logs. That does **not** cause `/health` 503 (DB check is separate). Conflicts should stop once only one replica remains.
- **Behavior today:** `/start` returns the welcome message from `application.start`. No chat persistence until later build days.

## Post-deploy verification

1. Railway deploy logs: `Telegram bot polling started` and no `TELEGRAM_BOT_TOKEN` warnings.
2. `GET https://<your-railway-domain>/health` → `{"status":"ok","database":"connected"}`.
3. Telegram: message your bot **`/start`** → welcome text.

## Common failures

| Symptom | Likely cause |
|---------|----------------|
| Build: `No start command detected` | Missing `railpack.json` / wrong builder (use Railpack). |
| Crash on boot: `TELEGRAM_BOT_TOKEN is required` | Token not set or `APP_ENV` not `production` mismatch. |
| App crash `No module named psycopg2` | `DATABASE_URL` used plain `postgresql://` on an old deploy. Redeploy latest code (URL normalization) or set `postgresql+asyncpg://…`. |
| Deploy fails health check | Was `/health` 503 (DB). Deploy gate uses `/health/live` (always 200 if Uvicorn bound). |
| `/health` 503 | Wrong `DATABASE_URL`, SSL, or database unreachable (fix pooler URL; bot can still run). |
| `telegram.error.Conflict` during deploy | Overlapping deploy instances or local bot + Railway; not a health-check failure. |
| API healthy, bot silent | Token missing/wrong, or scaled to >1 replica. |

### Disable Railway health checks entirely

Remove `healthcheckPath` and `healthcheckTimeout` from `railway.toml` (or clear the health check path in the Railway service **Settings**). Deployments will mark success when the container starts, without probing HTTP. You lose automatic rollback when the process crashes after boot; keep using `GET /health` manually for DB verification.

## Local parity

```bash
cp .env.example .env
# set DATABASE_URL (+ optional TELEGRAM_BOT_TOKEN)
docker compose up -d db   # optional local Postgres for tests
uv run magnus-api
```

See [docs/ARCHITECTURE.md](ARCHITECTURE.md) for module boundaries.
