# Magnus — Source of Truth

## Purpose

This file defines the **authoritative systems** for Magnus infrastructure and development.

If another document conflicts with this file on **infrastructure ownership**, this document wins unless an accepted ADR explicitly supersedes it.

Product philosophy: `docs/starter-kit/CORE_PROBLEM.md` and `PRODUCT_CONTRACT.md`.

---

## 1. Source code

| Item | Value |
|------|--------|
| Authoritative GitHub repository | https://github.com/sakshamgoyal06/magnus-ai |
| Production branch | `main` |
| Git remote name | `origin` → `https://github.com/sakshamgoyal06/magnus-ai` |
| Secondary remotes | Not allowed |

---

## 2. Development environment

- Cursor (desktop or Cloud Agents) connected to the authoritative GitHub repository.
- Source changes land on GitHub (`main` or PR into `main`).
- Local clone is supported; production does not depend on one machine.
- Cloud Agent install: `.cursor/environment.json` (`uv sync --extra dev`, optional `GITHUB_TOKEN`, rewrite stale `origin.cursor.com` to GitHub).

---

## 3. Application runtime

- **Railway** is the production runtime.
- One Python service: FastAPI + Telegram long-polling (`magnus.api.main`).
- Start command (repo): `uv run uvicorn magnus.api.main:app --host 0.0.0.0 --port $PORT`
- Deploy health (Railway): `GET /health/live`
- Operational health (DB): `GET /health`
- **Exactly one** production replica while polling is active.

`REQUIRES MANUAL VERIFICATION: Railway project/service name, GitHub connection, branch, auto-deploy, replica count`

---

## 4. Database

- **Supabase PostgreSQL** is the only production database.
- Project name: **`magnus-ai`**
- Project ref: **`uktsxijrewbqjcjnrfdv`**
- Application access: **`DATABASE_URL`** (SQLAlchemy 2.x async + **asyncpg**). No Supabase SDK in application code.
- Day 1: **no Magnus application tables** in `public`; `/health` uses `SELECT 1`.
- Local optional: Docker Postgres `magnus_dev` for tests only — not production.

`REQUIRES MANUAL VERIFICATION: Railway DATABASE_URL uses Supabase session pooler for this project`

---

## 5. Schema migration authority

```text
GitHub repository → supabase/migrations/
```

- **`supabase/config.toml`** links CLI to project `uktsxijrewbqjcjnrfdv`.
- Day 1 baseline: `supabase/migrations/20260917051947_day1_baseline.sql` (no application DDL; hosted version `20260917051947`).
- Apply to hosted DB: Supabase CLI `supabase db push` (see [SUPABASE_MIGRATIONS.md](SUPABASE_MIGRATIONS.md)). **Railway does not run migrations.**
- Dashboard schema editing is not the normal workflow.

---

## 6. Runtime secrets / environment variables

| Variable | Purpose | Host | Secret? |
|----------|---------|------|---------|
| `DATABASE_URL` | Async Postgres URL | Railway / `.env` | Yes |
| `TELEGRAM_BOT_TOKEN` | Long-polling | Railway (required if `APP_ENV=production`) | Yes |
| `APP_ENV` | `production` fail-fast rules | Railway | No |
| `LOG_LEVEL` | Logging | Railway / `.env` | No |
| `PORT` | HTTP port | Railway | No |

Not used by `magnus-api`: `OPENAI_API_KEY`, `SUPABASE_URL`, `SUPABASE_ANON_KEY`. Cloud-only: `GITHUB_TOKEN`.

---

## 7. Telegram MVP surface

- Only MVP user surface during the 21-day build.
- **Long polling**; webhooks not implemented.
- Adapter: `magnus/telegram/` → `magnus/application/` only.
- **One** production polling instance.

---

## 8. Product intelligence boundary

- Domain/application logic is authoritative; **no Day 2 domain model in repo yet**.
- `LLMProvider` is provisional; no concrete LLM on Day 1.
- LLMs must not silently own authoritative state mutations.

---

## 9. Deployment flow

```text
Cursor Web / Cursor Cloud
        ↓
GitHub  sakshamgoyal06/magnus-ai  (main)
        ↓
Supabase CLI  supabase db push   (schema; not Railway)
        ↓
Railway  →  Magnus (FastAPI + Telegram polling)
        ↓
Supabase PostgreSQL  (magnus-ai)
        ↓
Telegram Bot API
```

---

## 10. Authoritative documents

| Role | Document |
|------|----------|
| Infrastructure | `docs/SOURCE_OF_TRUTH.md` |
| Schema workflow | `docs/SUPABASE_MIGRATIONS.md` |
| Product | `docs/starter-kit/CORE_PROBLEM.md`, `PRODUCT_CONTRACT.md` |
| Build gates | `docs/starter-kit/BUILD_GATES.md` |
| Build plan | `docs/starter-kit/MVP_BUILD_PLAN.md` |
| Layout | `docs/ARCHITECTURE.md` |
| Migrations decision | `docs/adr/0002-supabase-persistence-and-migrations.md` |
| Railway runbook | `docs/DEPLOYMENT_RAILWAY.md` |
| Day 1 audit / handoff | `docs/DAY_1_AUDIT.md` |

---

## 11. Day 1 foundation status

Verified against hosted Supabase project `uktsxijrewbqjcjnrfdv` (2026-09-18):

- Migration history contains version **`20260917051947`**, name **`day1_baseline`** (matches git `supabase/migrations/20260917051947_day1_baseline.sql`).
- **`public`** has **no Magnus application tables** (manual probe table removed; Day 2 DDL starts clean).
- Production **`GET /health`** returned **`database: connected`** (re-check after deploys).

Day 2 may add new files under `supabase/migrations/` and domain code under `magnus/domain/` and `magnus/repositories/` without revisiting Day 1 infra choices.

---

## 12. Manual verification checklist

- [ ] Railway project/service connected to GitHub `sakshamgoyal06/magnus-ai`, branch `main`, auto-deploy
- [ ] Railway **one** replica; deploy health path `/health/live`
- [ ] Railway vars: `DATABASE_URL` → Supabase session pooler, `TELEGRAM_BOT_TOKEN`, `APP_ENV=production`
- [x] `supabase db push` applied; migration history includes `20260917051947` / `day1_baseline`
- [x] Supabase `public` has no Day 2 domain tables (no Magnus DDL in `public`)
- [ ] Telegram `/start` works against production bot
- [x] Live `GET /health` → 200, `database: connected` (last verified 2026-09-18; re-check after changes)
