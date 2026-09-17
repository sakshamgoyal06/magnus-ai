# Magnus V2 — Current Build State

**Last updated:** 2026-09-18  
**Current completed build day:** Day 1 (foundation)

**Start here** for a new dev session or external review.

---

## Stable foundations

- GitHub repo `sakshamgoyal06/magnus-ai`, branch `main`, single `origin`.
- Python 3.12+ package `magnus`, `uv` + `uv.lock`.
- FastAPI app `magnus.api.main:app`; routes `/health`, `/health/live`.
- Async Postgres via `DATABASE_URL` + SQLAlchemy/asyncpg; Supabase session pooler + `ssl=require` on Railway.
- Schema authority: `supabase/migrations/` + CLI `supabase db push` (not at Railway boot).
- Hosted baseline migration **`20260917051947`** / **`day1_baseline`**; `public` has no Magnus app tables.
- Telegram long-polling in lifespan; `/start` → static welcome via `magnus/application/start.py`.
- Module boundaries: telegram → application (no domain persistence yet).
- Documentation operating system under `docs/project/`, `docs/adr/`, `docs/daily/`.

---

## Implemented product capability

- User sends **`/start`** → welcome message (no memory, no goals, no AI).
- Operator verifies **`GET /health`** → DB `SELECT 1`.

---

## Infrastructure state

| System | State |
|--------|--------|
| **GitHub** | Canonical code; HEAD includes Day 1 + doc system moves (pending push after this change set) |
| **Railway** | Production URL `https://magnus-ai-production.up.railway.app`; start via Uvicorn on `$PORT`; deploy health `/health/live` |
| **Supabase** | Project `uktsxijrewbqjcjnrfdv`; migration applied; `public` empty of app DDL |
| **Telegram** | Long-polling; token via `TELEGRAM_BOT_TOKEN` |
| **Migrations** | Supabase CLI; git SQL under `supabase/migrations/` |

---

## Known debt

### Blocking

None identified for starting Day 2 **domain work**, assuming production DB health holds.

### Non-blocking

- No CI workflow for pytest.
- FastAPI `/docs` public in production.
- `ssl=require` without full CA verify.
- Manual Railway checklist items (replica count, live `/start`) not verified in repo.
- Placeholder dirs `output/`, `skills/`, `tools/`.
- `LOG_LEVEL` not applied on Railway start command path.

---

## Provisional decisions

- `LLMProvider` method shapes (ADR 0001).
- TLS strictness long-term.
- RLS policy when first user tables ship (see `OPEN_QUESTIONS.md`).

---

## Open blockers

None for documentation setup. Operational: confirm **one Railway replica** and production **`/start`** manually.

---

## Next build day

**Day 2** — per `MVP_BUILD_PLAN.md` (domain model / persistence foundation; do not start until Day 1 gate signed off).

---

## Next build day may safely assume

- FastAPI lifespan, engine, session factory on `app.state`.
- Empty `magnus/domain/`, `magnus/repositories/` packages.
- Supabase migration workflow and empty `public` app schema.
- Telegram adapter pattern and `/start` path.

---

## Next build day must NOT assume

- Any domain entities, repositories with I/O, or chat persistence.
- LLM provider implementation.
- Supabase SDK or REST client in app code.
- Webhooks or multi-replica polling.
- Alembic or Railway-run migrations.

---

## Relevant accepted ADRs

- `docs/adr/0001-day1-foundation.md`
- `docs/adr/0002-supabase-persistence-and-migrations.md`
