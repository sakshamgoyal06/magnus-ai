# Magnus architecture (Day 1 foundation)

Infrastructure ownership (GitHub, Railway, database host, Telegram transport, env vars) is defined in [SOURCE_OF_TRUTH.md](SOURCE_OF_TRUTH.md). This file describes module layout. If the two disagree on infrastructure, SOURCE_OF_TRUTH wins.

## Module tree

```text
magnus/
    api/              # HTTP surface (FastAPI)
    telegram/         # Telegram adapter only — no domain rules here
    domain/           # Entities and domain rules (Day 2+)
    application/      # Use cases / orchestration
    intelligence/     # LLM provider abstraction and reasoning (later days)
    repositories/     # Persistence (Day 2+)
    infrastructure/   # Config, DB engine
    prompts/          # Prompt assets
    evaluations/      # Eval harness
    jobs/             # Scheduled / background work
    tests/            # Pytest suite
supabase/
    migrations/       # Authoritative schema history (ADR 0002)
docs/
    SOURCE_OF_TRUTH.md
    starter-kit/      # Product spec (authoritative)
    adr/              # Architecture decision records
```

## Boundaries

- **Telegram** handlers call **application** services; they do not import domain persistence directly.
- **API** routes follow the same rule for future REST hooks.
- **Intelligence** holds a provisional `LLMProvider` infrastructure boundary (see below). Application/domain services own product logic; they may call an LLM where semantic reasoning is needed.
- No “agent framework” or multi-agent shell in Day 1.
- No Day 2 domain entities exist in code yet.

## `LLMProvider` (provisional)

`LLMProvider` is a provisional infrastructure boundary. Its current methods (`generate`, `extract_structured`, `reason`) are **not** part of the permanent Magnus domain contract and may be revised once concrete semantic use cases exist (Day 5+).

Product intelligence must live in explicit application/domain services (e.g. future `TrajectoryService`, `AdherenceService`, `DiagnosisService`, `PriorityService`, `ReviewService`). Those services own deterministic logic; LLM calls are capabilities they use where needed. Structured validation must sit between LLM output and authoritative state mutation.

`reason()` must **not** become a god-interface for trajectory, diagnosis, prioritization, review, or strategy logic. If the interface encourages that, redesign the provider when real use cases land.

## Runtime

- `magnus-api` (or `uv run magnus-api`) starts Uvicorn with FastAPI.
- Optional `TELEGRAM_BOT_TOKEN` starts python-telegram-bot **long-polling** in the app lifespan. Production must run **one** polling instance.
- PostgreSQL is required for `/health`. Application code uses generic `DATABASE_URL` (SQLAlchemy async + asyncpg). Production database is **Supabase PostgreSQL**; optional local Docker `magnus_dev` for dev/tests.
- Schema authority: **`supabase/migrations/`** (Alembic superseded by ADR 0002). Day 1 has no application tables; connectivity uses `SELECT 1`.

## ADRs

- [0001-day1-foundation.md](adr/0001-day1-foundation.md) (accepted; migration portions superseded)
- [0002-supabase-persistence-and-migrations.md](adr/0002-supabase-persistence-and-migrations.md) (accepted)
