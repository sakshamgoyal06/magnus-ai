# Deploy Magnus on Railway with Supabase Postgres

Magnus uses **PostgreSQL only** from Supabase (not the Supabase JS client). The API and Telegram bot read `DATABASE_URL` from the environment.

## Supabase project

| Field | Value |
|-------|--------|
| Name | `magnus-ai` |
| Region | `us-east-1` |
| Project ref | `uktsxijrewbqjcjnrfdv` |
| Dashboard | https://supabase.com/dashboard/project/uktsxijrewbqjcjnrfdv |
| API URL | `https://uktsxijrewbqjcjnrfdv.supabase.co` |

Schema is applied with **Alembic** (not the Supabase SQL editor). After linking, run migrations once per deploy (see below).

### Tables (current scope)

- `app_metadata` — Day 1 connectivity marker (small; safe to keep).
- `chat_records` — Telegram conversation rows (Day 4 persistence target).

No other domain tables yet.

## 1. Get the database password

In Supabase: **Project Settings → Database → Database password**.

If you never saved it, use **Reset database password** and store the new value in Railway only.

## 2. Build `DATABASE_URL` for Magnus

Magnus expects an **async** SQLAlchemy URL (`asyncpg`).

**Direct connection (recommended for a single Railway service):**

```text
postgresql+asyncpg://postgres:YOUR_DB_PASSWORD@db.uktsxijrewbqjcjnrfdv.supabase.co:5432/postgres
```

**Session pooler (IPv4-friendly; use if direct connection fails from Railway):**

In Supabase: **Project Settings → Database → Connection string → URI**, mode **Session**, copy the host/port/user, then:

```text
postgresql+asyncpg://postgres.uktsxijrewbqjcjnrfdv:YOUR_DB_PASSWORD@aws-0-us-east-1.pooler.supabase.com:5432/postgres
```

If the password contains special characters (`@`, `#`, `%`, etc.), URL-encode them.

Supabase requires TLS. If you see SSL errors, append:

```text
?ssl=require
```

## 3. Railway variables

Open your Magnus **service** → **Variables**:

| Variable | Value |
|----------|--------|
| `DATABASE_URL` | Async URL from step 2 |
| `TELEGRAM_BOT_TOKEN` | From BotFather (secret) |
| `APP_ENV` | `production` |
| `LOG_LEVEL` | `INFO` |

Remove or unset any old **Railway Postgres** `DATABASE_URL` from a plugin so only Supabase is used.

Reference from another service (optional): `${{supabase.DATABASE_URL}}` only works if you wired a Supabase integration; manual paste of the async URL is fine.

## 4. Migrate on deploy

Run Alembic before or when the app starts.

**Option A — Railway custom start command:**

```bash
uv run alembic upgrade head && uv run magnus-api
```

**Option B — separate release / one-off command in Railway:**

```bash
uv run alembic upgrade head
```

Then start the service with `uv run magnus-api`.

Verify in Supabase **Table Editor**: `app_metadata` and `chat_records` exist.

## 5. Local project `.env`

```bash
cp .env.example .env
```

Set the same `DATABASE_URL` (or a Supabase **branch** URL for dev) and `TELEGRAM_BOT_TOKEN`. Never commit `.env`.

```bash
uv run alembic upgrade head
uv run magnus-api
```

## 6. Optional Supabase env vars (not required for Magnus API)

These are for a future web client using Supabase Auth/Realtime — **not** used by the current Python service:

- `SUPABASE_URL` = `https://uktsxijrewbqjcjnrfdv.supabase.co`
- Publishable key from **Project Settings → API**

## Security

- Do not commit database passwords or bot tokens.
- `chat_records` has **RLS enabled** with no public policies; the Magnus server uses the `postgres` DB role over `DATABASE_URL`, not the anon API key.
- Rotate the DB password if it was ever exposed in chat or logs.
