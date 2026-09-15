# Magnus architecture (Day 1 foundation)

## Module tree

```text
magnus/
    api/              # HTTP surface (FastAPI)
    telegram/         # Telegram adapter only — no domain rules here
    domain/           # Entities and domain rules (Day 2+)
    application/      # Use cases / orchestration
    intelligence/     # LLM provider abstraction and reasoning (later days)
    repositories/     # Persistence (Day 2+)
    infrastructure/   # Config, DB engine, shared technical models
    prompts/          # Prompt assets
    evaluations/      # Eval harness
    jobs/             # Scheduled / background work
    tests/            # Pytest suite
alembic/              # Database migrations
docs/
    starter-kit/      # Product spec (authoritative)
    adr/              # Architecture decision records
```

## Boundaries

- **Telegram** handlers call **application** services; they do not import domain persistence directly.
- **API** routes follow the same rule for future REST hooks.
- **Intelligence** holds a provisional `LLMProvider` infrastructure boundary (see below). Application/domain services own product logic; they may call an LLM where semantic reasoning is needed.
- No “agent framework” or multi-agent shell in Day 1.

## `LLMProvider` (provisional)

`LLMProvider` is a provisional infrastructure boundary. Its current methods (`generate`, `extract_structured`, `reason`) are **not** part of the permanent Magnus domain contract and may be revised once concrete semantic use cases exist (Day 5+).

Product intelligence must live in explicit application/domain services (e.g. future `TrajectoryService`, `AdherenceService`, `DiagnosisService`, `PriorityService`, `ReviewService`). Those services own deterministic logic; LLM calls are capabilities they use where needed. Structured validation must sit between LLM output and authoritative state mutation.

`reason()` must **not** become a god-interface for trajectory, diagnosis, prioritization, review, or strategy logic. If the interface encourages that, redesign the provider when real use cases land.

## Runtime

- `magnus-api` (or `uv run magnus-api`) starts Uvicorn with FastAPI.
- Optional `TELEGRAM_BOT_TOKEN` starts python-telegram-bot polling in the app lifespan.
- PostgreSQL is required; schema is managed with Alembic.

## ADRs

- [0001-day1-foundation.md](adr/0001-day1-foundation.md)
