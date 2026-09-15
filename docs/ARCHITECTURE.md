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
- **Intelligence** implements `LLMProvider`; application services depend on the interface, not a vendor SDK.
- No “agent framework” or multi-agent shell in Day 1.

## Runtime

- `magnus-api` (or `uv run magnus-api`) starts Uvicorn with FastAPI.
- Optional `TELEGRAM_BOT_TOKEN` starts python-telegram-bot polling in the app lifespan.
- PostgreSQL is required; schema is managed with Alembic.

## ADRs

- [0001-day1-foundation.md](adr/0001-day1-foundation.md)
