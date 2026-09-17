# ADR 0002: Supabase persistence and migrations

## Status

Accepted

## Context

Day 1 initially used standalone PostgreSQL + Alembic.

Before Day 2, infrastructure was intentionally revised to use Supabase PostgreSQL and Supabase migrations because the production MVP will use managed Supabase infrastructure and Git-backed schema history.

## Decision

- Supabase PostgreSQL is the production database.
- Schema migrations live in `supabase/migrations/`.
- Git is the authoritative schema-history source.
- Alembic is no longer active.
- SQLAlchemy remains allowed as the application persistence layer.
- Magnus application code consumes a generic `DATABASE_URL`.
- Domain/application logic must remain independent of Supabase-specific SDK features unless separately justified.
- Direct Supabase Dashboard schema editing is not the normal migration workflow.

## Consequences

- Single migration authority in git (`supabase/migrations/`) instead of Alembic revisions.
- Managed database infrastructure (Supabase) for production; local Docker Postgres remains optional for dev/tests only.
- Production schema must stay synchronized with committed migration files (via Supabase CLI `db push`, linked CI, or documented manual apply before/after deploy).
- Day 2 schema changes must originate from new files under `supabase/migrations/`.
- Supabase Auth, Storage, Realtime, and Edge Functions are **not** adopted by this decision unless a future ADR says otherwise.
- Day 1 does not require application tables; `/health` uses `SELECT 1`.

## Supersedes

ADR 0001 **Alembic**, **sync `postgresql+psycopg` URLs**, and **`app_metadata` probe table** decisions are superseded by this ADR. Other ADR 0001 decisions (FastAPI layout, Telegram adapter, provisional `LLMProvider`) remain accepted.
