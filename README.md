# Magnus (clean-room MVP)

Adaptive personal intelligence system — **Telegram-first** 21-day MVP. Product direction lives in the [starter kit](docs/starter-kit/README.md); this repository is a clean-room implementation.

**Repository:** [github.com/sakshamgoyal06/magnus-ai](https://github.com/sakshamgoyal06/magnus-ai)

Clone, push, and pull use GitHub only. For Cursor Cloud Agents (web/phone) and secrets, see [docs/CURSOR_AND_GITHUB.md](docs/CURSOR_AND_GITHUB.md).

Infrastructure ownership is defined in [docs/SOURCE_OF_TRUTH.md](docs/SOURCE_OF_TRUTH.md).

## Authoritative documents

| Document | Path |
|----------|------|
| Infrastructure source of truth | [docs/SOURCE_OF_TRUTH.md](docs/SOURCE_OF_TRUTH.md) |
| Supabase migrations workflow | [docs/SUPABASE_MIGRATIONS.md](docs/SUPABASE_MIGRATIONS.md) |
| Core problem | [docs/starter-kit/CORE_PROBLEM.md](docs/starter-kit/CORE_PROBLEM.md) |
| 21-day build plan | [docs/starter-kit/MVP_BUILD_PLAN.md](docs/starter-kit/MVP_BUILD_PLAN.md) |
| Daily build gates | [docs/starter-kit/BUILD_GATES.md](docs/starter-kit/BUILD_GATES.md) |
| Product contract | [PRODUCT_CONTRACT.md](PRODUCT_CONTRACT.md) |
| Architecture | [docs/ARCHITECTURE.md](docs/ARCHITECTURE.md) |

## Implementation status

**Day 1 (foundation)** — FastAPI `/health` (real DB ping), Supabase-backed schema authority in git (`supabase/migrations/`), Telegram `/start` long-polling, tests, Railway-ready runtime. Production: Railway → Supabase PostgreSQL. See [docs/SOURCE_OF_TRUTH.md](docs/SOURCE_OF_TRUTH.md).

## Prerequisites

- Python **3.12+**
- [uv](https://docs.astral.sh/uv/)
- Optional local Postgres for tests: [Docker Compose](#local-postgres-optional) or Supabase dev URL

## Local setup

### 1. Python environment

```bash
cp .env.example .env
uv sync --extra dev
```

Set `DATABASE_URL` in `.env` (local Docker default or Supabase session URL).

### 2. Local Postgres (optional)

For pytest against localhost:

```bash
docker compose up -d db
```

### 3. Schema (Supabase)

Production and shared schema history:

```bash
supabase link --project-ref uktsxijrewbqjcjnrfdv
supabase db push
```

See [docs/SUPABASE_MIGRATIONS.md](docs/SUPABASE_MIGRATIONS.md). Railway does **not** apply migrations.

### 4. Run the API (and optional Telegram bot)

```bash
uv run magnus-api
```

- Health: [http://localhost:8000/health](http://localhost:8000/health)
- Set `TELEGRAM_BOT_TOKEN` in `.env` to enable long-polling for `/start`.

## Railway deployment

See [docs/DEPLOYMENT_RAILWAY.md](docs/DEPLOYMENT_RAILWAY.md).

## Tests

```bash
uv run pytest
```

Requires a reachable PostgreSQL at `DATABASE_URL` (default: local `magnus_dev`). No application tables required — health uses `SELECT 1`.

## Dependencies (Day 1)

| Package | Role |
|---------|------|
| fastapi | HTTP API |
| uvicorn | ASGI server |
| sqlalchemy[asyncio] | ORM and async DB access |
| asyncpg | Async PostgreSQL driver |
| pydantic-settings | Typed configuration from environment |
| python-telegram-bot | Telegram adapter (`/start`) |
| pytest, pytest-asyncio, httpx | Tests (dev extra) |
| ruff | Lint/format (dev extra) |

Schema migrations: **Supabase CLI** + files in `supabase/migrations/` (not a Python package dependency).

Intelligence providers are not wired on Day 1; see `magnus/intelligence/llm_provider.py`.

## Project rules

Cursor rules in [`.cursor/rules/`](.cursor/rules/) enforce clean-room constraints and starter-kit alignment.
