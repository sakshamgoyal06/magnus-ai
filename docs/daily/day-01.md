# Magnus V2 — Day 01

## Objective

Establish clean repository foundation: FastAPI health with real DB check, Supabase migration authority, Railway-ready runtime, Telegram `/start`, tests, and infrastructure documentation—without domain model or intelligence.

## Scope built

- Python package `magnus` (FastAPI, async SQLAlchemy/asyncpg, pydantic-settings, python-telegram-bot).
- Routes: `/health`, `/health/live`.
- Supabase baseline migration; Alembic removed from active architecture.
- Railway + Railpack config; production deploy to Supabase session pooler.
- Telegram adapter → application welcome for `/start`.
- ADRs 0001, 0002; product contract; starter kit content moved to `docs/project/`.
- Pytest suite (config, startup, health, start handler, Telegram lifespan mock).

## Explicitly not built

- Domain entities, repositories with I/O, chat persistence.
- LLM provider implementation, prompts in use, jobs, evaluations logic.
- Supabase SDK, webhooks, multi-replica strategy.
- CI workflow, authenticated admin API.

## Files materially changed

- `magnus/api/`, `magnus/infrastructure/`, `magnus/telegram/`, `magnus/application/`
- `supabase/migrations/20260917051947_day1_baseline.sql`
- `railway.toml`, `railpack.json`, `pyproject.toml`, `uv.lock`
- `docs/project/*`, `docs/adr/*`, `docs/daily/day-01.md`

## Architecture decisions

- Supabase migrations + `DATABASE_URL` asyncpg (ADR 0002).
- Single-process polling; deploy health split (see `DECISION_LOG.md`).
- `ssl=require` for Supabase on Railway.

## Product decisions

- Telegram-only MVP transport for build plan period.
- Intelligence layer principles; no authoritative state from LLM (contract).
- Provisional `LLMProvider` only.

## Tests / validation

- `uv run pytest` (requires local Postgres or `DATABASE_URL` for integration fixtures).
- Production: `GET /health` → `database: connected` (2026-09-18).
- Production `/start`: **manual verify pending** (SOURCE_OF_TRUTH §10).

## Release-gate result

**PASS WITH DEBT**

- Critical Day 1 capabilities implemented and production DB health verified.
- Debt: manual Railway replica/deploy checklist; live `/start` sign-off; no CI; OpenAPI public; TLS verify mode.

## Known debt

- Non-blocking items in `OPEN_QUESTIONS.md` Q-001–Q-009.
- See `docs/project/CURRENT_STATE.md`.

## Open questions created/resolved

- Created: see `docs/project/OPEN_QUESTIONS.md` (Active).
- Resolved: none formally closed in log yet.

## What Day 02 may safely rely on

- FastAPI lifespan, DB engine, session factory on `app.state`.
- Empty `domain/`, `repositories/`.
- Supabase migration workflow; empty `public` app schema.
- Telegram → application boundary.

## What remains provisional

- `LLMProvider` interface.
- TLS strictness, RLS strategy, OpenAPI exposure.
- Exact Day 2 scope per `MVP_BUILD_PLAN.md` (read before starting).

## Historical note

Detailed Day 1 repository audit was captured in commit `dc3fec3` (`docs/DAY_1_AUDIT.md`, since retired in favor of this daily record and `docs/project/CURRENT_STATE.md`).
