# ADR 0001: Day 1 foundation stack and layout

## Status

Accepted (Day 1)

## Context

Magnus is a clean-room MVP with a 21-day plan. Day 1 requires a reproducible Python service, PostgreSQL, migrations, health checks, and a Telegram `/start` path without intelligence or domain modelling yet.

## Decision

- **Python 3.12+**, **FastAPI**, **SQLAlchemy 2.x (async)**, **Alembic**, **Pydantic Settings**, **python-telegram-bot**, **pytest**.
- Package layout under `magnus/` with explicit `telegram/` adapter and empty `domain/` for Day 2.
- Async runtime DB URL (`postgresql+asyncpg://`); sync `postgresql+psycopg://` for Alembic only.
- Minimal `app_metadata` table to prove migrations; no life-model schema until Day 2.
- `LLMProvider` ABC in `intelligence/` with no concrete implementation on Day 1.

### Provisional LLM boundary (Day 1)

`LLMProvider` is a provisional infrastructure boundary. Its current methods are not part of the permanent Magnus domain contract and may be revised once concrete semantic use cases are implemented. Product intelligence must live in explicit application/domain services rather than a generic LLM reasoning method. `reason()` must not become a catch-all for trajectory, diagnosis, prioritization, review, or strategy logic.

## Consequences

- Developers need PostgreSQL locally (package install or `docker compose up db`).
- Telegram polling runs in-process with the API; production may later split processes or use webhooks.
- CrewAI scaffold removed; not part of Magnus MVP.
