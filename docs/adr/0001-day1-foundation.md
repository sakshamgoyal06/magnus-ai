# ADR 0001: Day 1 foundation stack and layout

## Status

Accepted (Day 1)

## Context

Magnus is a clean-room MVP with a 21-day plan. Day 1 requires a reproducible Python service, PostgreSQL, schema history in git, health checks, and a Telegram `/start` path without intelligence or domain modelling yet.

## Decision

- **Python 3.12+**, **FastAPI**, **SQLAlchemy 2.x (async)**, **Pydantic Settings**, **python-telegram-bot**, **pytest**.
- Package layout under `magnus/` with explicit `telegram/` adapter and empty `domain/` for Day 2.
- Async runtime DB URL (`postgresql+asyncpg://`).
- Schema authority: `supabase/migrations/` on Supabase PostgreSQL ([ADR 0002](0002-supabase-persistence-and-migrations.md)).
- `LLMProvider` ABC in `intelligence/` with no concrete implementation on Day 1.

### Provisional LLM boundary (Day 1)

`LLMProvider` is a provisional infrastructure boundary. Its current methods are not part of the permanent Magnus domain contract and may be revised once concrete semantic use cases are implemented. Product intelligence must live in explicit application/domain services rather than a generic LLM reasoning method. `reason()` must not become a catch-all for trajectory, diagnosis, prioritization, review, or strategy logic.

## Consequences

- Developers may use local PostgreSQL (package install or `docker compose up db`) for tests; production uses Supabase.
- Telegram polling runs in-process with the API; production must keep a single polling replica while this mode is used. Webhooks are not implemented.
