# Magnus (clean-room MVP)

Adaptive personal intelligence system — **Telegram-first** 21-day MVP. Product direction lives in the [starter kit](docs/starter-kit/README.md); this repository is a clean-room implementation.

**Repository:** [github.com/sakshamgoyal06/magnus-ai](https://github.com/sakshamgoyal06/magnus-ai)

Clone, push, and pull use GitHub only. For Cursor Cloud Agents (web/phone) and secrets, see [docs/CURSOR_AND_GITHUB.md](docs/CURSOR_AND_GITHUB.md).

## Authoritative documents

| Document | Path |
|----------|------|
| Core problem | [docs/starter-kit/CORE_PROBLEM.md](docs/starter-kit/CORE_PROBLEM.md) |
| 21-day build plan | [docs/starter-kit/MVP_BUILD_PLAN.md](docs/starter-kit/MVP_BUILD_PLAN.md) |
| Daily build gates | [docs/starter-kit/BUILD_GATES.md](docs/starter-kit/BUILD_GATES.md) |
| Product contract | [PRODUCT_CONTRACT.md](PRODUCT_CONTRACT.md) |
| Architecture | [docs/ARCHITECTURE.md](docs/ARCHITECTURE.md) |

## Implementation status

**Day 1 (foundation)** — FastAPI health check, PostgreSQL + Alembic, Telegram `/start` skeleton, tests, and development tooling.

## Architecture tree

See [docs/ARCHITECTURE.md](docs/ARCHITECTURE.md).

## Prerequisites

- Python **3.12+**
- [uv](https://docs.astral.sh/uv/) (recommended) or `pip`
- PostgreSQL **16** (local install or Docker)

## Local setup

### 1. PostgreSQL

**Option A — Docker**

```bash
docker compose up -d db
```

**Option B — system PostgreSQL**

Create role and database (adjust credentials to match `.env`):

```bash
createuser magnus -P   # password: magnus
createdb magnus_dev -O magnus
```

### 2. Python environment

```bash
cp .env.example .env
uv sync --extra dev
```

### 3. Migrations

```bash
uv run alembic upgrade head
```

### 4. Run the API (and optional Telegram bot)

```bash
uv run magnus-api
```

- Health: [http://localhost:8000/health](http://localhost:8000/health)
- Set `TELEGRAM_BOT_TOKEN` in `.env` to enable long-polling for `/start`.

## Railway deployment

See [docs/DEPLOYMENT_RAILWAY.md](docs/DEPLOYMENT_RAILWAY.md) for required variables, Supabase `DATABASE_URL`, migrations, and Telegram replica constraints.

## Tests

```bash
uv run pytest
```

Requires a reachable PostgreSQL instance at `DATABASE_URL` (default: `magnus_dev` on localhost).

## Dependencies (Day 1)

| Package | Role |
|---------|------|
| fastapi | HTTP API |
| uvicorn | ASGI server |
| sqlalchemy[asyncio] | ORM and async DB access |
| asyncpg | Async PostgreSQL driver |
| psycopg[binary] | Sync driver for Alembic |
| alembic | Schema migrations |
| pydantic-settings | Typed configuration from environment |
| python-telegram-bot | Telegram adapter (`/start`) |
| pytest, pytest-asyncio, httpx | Tests (dev extra) |
| ruff | Lint/format (dev extra) |

Intelligence providers are not wired on Day 1; see `magnus/intelligence/llm_provider.py`.

## Project rules

Cursor rules in [`.cursor/rules/`](.cursor/rules/) enforce clean-room constraints and starter-kit alignment.
