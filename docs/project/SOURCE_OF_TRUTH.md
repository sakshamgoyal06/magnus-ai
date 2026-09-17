# Magnus V2 — Source of Truth

## Document authority

Chat discussions are **not** authoritative unless reflected in canonical project documentation.

### Product authority

1. `docs/project/CORE_PROBLEM.md`
2. `docs/project/PRODUCT_CONTRACT.md`

### Infrastructure authority

1. `docs/project/SOURCE_OF_TRUTH.md` (this file)
2. Accepted ADRs in `docs/adr/`
3. `docs/project/ARCHITECTURE.md`

Operational runbooks (same folder): `DEPLOYMENT_RAILWAY.md`, `SUPABASE_MIGRATIONS.md`, `CURSOR_AND_GITHUB.md`.

### Build authority

1. `docs/project/BUILD_GATES.md`
2. `docs/project/MVP_BUILD_PLAN.md`
3. `docs/project/CURRENT_STATE.md`

### Decision history

- `docs/project/DECISION_LOG.md` — compact accepted decisions
- `docs/adr/` — detailed decision records

### Unresolved issues

- `docs/project/OPEN_QUESTIONS.md`

### Historical build records

- `docs/daily/`

### Global conflict resolution

When sources conflict, higher layers win. If a chat contradicts a document, the document wins unless we **explicitly** revise the document.

Extended ordering (includes implementation and chat): see `DECISION_LOG.md` entry **Document authority order** and `docs/project/CURRENT_STATE.md`.

---

## Purpose

This file defines **authoritative infrastructure and runtime systems** for Magnus V2.

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

- Cursor connected to the authoritative GitHub repository.
- Cloud Agent install: `.cursor/environment.json` (`uv sync --extra dev`, optional `GITHUB_TOKEN`).
- Governance: `.cursor/rules/magnus-project-governance.mdc`.

---

## 3. Application runtime

- **Railway** — production runtime.
- One Python service: FastAPI + Telegram long-polling (`magnus.api.main`).
- Start: `uv run uvicorn magnus.api.main:app --host 0.0.0.0 --port $PORT`
- Deploy health: `GET /health/live`
- Operational health: `GET /health`
- **One** production replica while long-polling.

---

## 4. Database

- **Supabase PostgreSQL** — production database (project `magnus-ai`, ref `uktsxijrewbqjcjnrfdv`).
- App access: **`DATABASE_URL`** (SQLAlchemy async + asyncpg). No Supabase SDK in `magnus-api`.
- Day 1: no Magnus application tables in `public`; `/health` uses `SELECT 1`.
- Local optional: Docker `magnus_dev` for tests.

---

## 5. Schema migration authority

```text
GitHub → supabase/migrations/ → supabase db push (not Railway)
```

- Baseline: `supabase/migrations/20260917051947_day1_baseline.sql`
- Hosted version: `20260917051947` / name `day1_baseline`

---

## 6. Runtime environment variables

| Variable | Purpose |
|----------|---------|
| `DATABASE_URL` | Async Postgres URL |
| `TELEGRAM_BOT_TOKEN` | Long-polling (required if `APP_ENV=production`) |
| `APP_ENV` | Production fail-fast rules |
| `LOG_LEVEL` | Logging (local CLI primarily) |
| `PORT` | HTTP port (Railway) |

Not used by `magnus-api`: `SUPABASE_URL`, `SUPABASE_ANON_KEY`, `OPENAI_API_KEY`.

---

## 7. Telegram

- Long-polling only (no webhooks Day 1).
- Adapter: `magnus/telegram/` → `magnus/application/`.

---

## 8. Documentation pack (review / handoff)

**Cursor and humans:** read `docs/project/CURRENT_STATE.md` **first** before every build day (see `.cursor/rules/magnus-current-state-first.mdc`).

Before or after each build day, share:

- `docs/project/CURRENT_STATE.md`
- `docs/daily/day-XX.md` (that day)
- `docs/project/CHANGELOG.md` (recent entry)
- `docs/project/OPEN_QUESTIONS.md` (active section)

---

## 9. Day 1 foundation status

Verified 2026-09-18 (re-check after infra changes):

- Migration history: **`20260917051947`** / **`day1_baseline`**
- `public`: no Magnus application tables
- Production `/health`: **`database: connected`** (last HTTP check 2026-09-18)

---

## 10. Manual verification checklist

- [ ] Railway ↔ GitHub `main`, auto-deploy
- [ ] Railway **one** replica; health `/health/live`
- [ ] Railway vars: pooler `DATABASE_URL`, `TELEGRAM_BOT_TOKEN`, `APP_ENV=production`
- [x] Migration `20260917051947` / `day1_baseline` on hosted Supabase
- [x] No Magnus DDL in `public`
- [ ] Production Telegram `/start`
- [x] `/health` DB connected (2026-09-18; re-check after deploys)
