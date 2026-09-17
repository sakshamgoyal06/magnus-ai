# ADR 0002: Supabase persistence and migrations

## Status

Accepted

## Context

Production Magnus uses managed Supabase PostgreSQL. Schema changes must be versioned in git and applied outside the Railway deploy step.

## Decision

- Supabase PostgreSQL is the production database.
- Schema migrations live in `supabase/migrations/`.
- Git is the authoritative schema-history source.
- SQLAlchemy remains the application persistence layer.
- Magnus application code consumes a generic `DATABASE_URL`.
- Domain/application logic must remain independent of Supabase-specific SDK features unless separately justified.
- Direct Supabase Dashboard schema editing is not the normal migration workflow.

## Consequences

- Managed database infrastructure (Supabase) for production; local Docker Postgres remains optional for dev/tests only.
- Production schema must stay synchronized with committed migration files (via Supabase CLI `db push`, linked CI, or documented manual apply before/after deploy).
- Day 2 schema changes must originate from new files under `supabase/migrations/`.
- Supabase Auth, Storage, Realtime, and Edge Functions are **not** adopted by this decision unless a future ADR says otherwise.
- Day 1 does not require application tables; `/health` uses `SELECT 1`.
