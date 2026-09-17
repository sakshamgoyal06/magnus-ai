# Magnus V2 — Decision Log

## Purpose

This file records **accepted** product and architecture decisions that future build days may rely on.

Only explicitly accepted decisions belong here. Exploratory ideas belong in `OPEN_QUESTIONS.md`. Detailed rationale: `docs/adr/`.

---

## 2026-09-18 — Documentation operating system

### Decision

Canonical docs live under `docs/project/`, ADRs under `docs/adr/`, build-day records under `docs/daily/`. `CURRENT_STATE.md` is the primary handoff entry.

### Why

Keep product, architecture, build state, and decisions synchronized across Cursor, GitHub, review, and deploy targets.

### Implications

- No duplicate canonical copies at repo root or `docs/starter-kit/`
- After each build day: update daily file, `CURRENT_STATE.md`, `CHANGELOG.md`, and open questions as needed

### Related ADR

None

### Status

Accepted

---

## 2026-09-18 — Document authority order

### Decision

Resolve conflicts using the hierarchy in `SOURCE_OF_TRUTH.md` (product → build → infra ADRs → architecture → code → daily → chat).

### Why

Clean-room rebuild; prevent chat or implementation from overriding accepted contracts.

### Implications

- Chats lose to documents unless a document is explicitly revised
- `SOURCE_OF_TRUTH.md` wins for infrastructure ownership among engineering docs unless an ADR supersedes

### Related ADR

None

### Status

Accepted

---

## 2026-09-18 — Hosted migration version matches git filename

### Decision

Git baseline: `supabase/migrations/20260917051947_day1_baseline.sql`, matching Supabase `20260917051947` / `day1_baseline`.

### Why

CLI and hosted history must agree.

### Implications

- No second baseline timestamp for the same content
- Day 2+ uses new files under `supabase/migrations/`

### Related ADR

`docs/adr/0002-supabase-persistence-and-migrations.md`

### Status

Accepted

---

## 2026-09-17 — Supabase replaces Alembic

### Decision

Use Supabase PostgreSQL and Supabase migrations (`supabase/migrations/` + CLI).

### Why

Managed production database; one authoritative schema workflow; web-friendly ops.

### Implications

- Remove Alembic from active stack
- Retain SQLAlchemy application persistence
- Git migration SQL is authoritative; dashboard is not schema source of truth

### Related ADR

`docs/adr/0002-supabase-persistence-and-migrations.md`

### Status

Accepted

---

## 2026-09-17 — Application DB access via DATABASE_URL only

### Decision

Runtime uses generic `DATABASE_URL` (async SQLAlchemy + asyncpg). No Supabase Python SDK in `magnus-api`.

### Why

Keep application logic independent of Supabase-specific APIs.

### Implications

- `SUPABASE_URL` / keys are not app env vars today
- Schema apply outside Railway deploy

### Related ADR

`docs/adr/0002-supabase-persistence-and-migrations.md`

### Status

Accepted

---

## 2026-09-17 — Railway production runtime

### Decision

Single Railway Python service: FastAPI + Telegram polling; Uvicorn on `$PORT`; no migrations in deploy step.

### Why

Day 1 simplicity; one deploy surface.

### Implications

- `railway.toml` / `railpack.json` define start and deploy health
- `supabase db push` separate from Railway

### Related ADR

None

### Status

Accepted

---

## 2026-09-17 — Railway deploy health vs operational health

### Decision

Railway probes `GET /health/live`; DB verification uses `GET /health`.

### Why

Deploy should not fail solely on DB misconfiguration during fix.

### Implications

- `healthcheckPath = "/health/live"` in `railway.toml`

### Related ADR

None

### Status

Accepted

---

## 2026-09-17 — Supabase TLS on Railway (ssl=require)

### Decision

asyncpg uses `ssl=require` for Supabase hosts on Railway.

### Why

Strict CA verify failed on Railway pooler chains; encryption still required.

### Implications

- `magnus/infrastructure/database.py`
- May revisit full verify later (`OPEN_QUESTIONS.md`)

### Related ADR

None

### Status

Accepted

---

## 2026-09-17 — Telegram long-polling, one replica

### Decision

Telegram MVP uses in-process long-polling, not webhooks. One Railway replica while polling.

### Why

Avoid webhook/TLS setup on Day 1; one `getUpdates` consumer per token.

### Implications

- `TELEGRAM_BOT_TOKEN` required when `APP_ENV=production`
- Handlers stay thin; `/start` in application layer

### Related ADR

`docs/adr/0001-day1-foundation.md`

### Status

Accepted

---

## 2026-09-17 — Telegram-only MVP surface (Day 1–21 plan)

### Decision

Telegram is the MVP user interface; no web dashboard or mobile app in 21-day scope.

### Why

`PRODUCT_CONTRACT.md` non-goals and MVP build plan focus.

### Implications

- HTTP API is health (+ future hooks), not primary UX
- Web client env vars deferred

### Related ADR

None

### Status

Accepted

---

## 2026-09-17 — Clean-room GitHub repository

### Decision

Authoritative source: `github.com/sakshamgoyal06/magnus-ai`, branch `main`. No legacy Magnus repo as architecture source.

### Why

Starter kit clean-room rule.

### Implications

- Cursor clean-room rules apply
- Prior repos deprecated for design

### Related ADR

None

### Status

Accepted

---

## 2026-09-17 — Day 1 foundation stack and layout

### Decision

Python 3.12+, FastAPI, async SQLAlchemy, pydantic-settings, python-telegram-bot, pytest; modules `api/`, `telegram/`, `application/`, empty `domain/` / `repositories/`.

### Why

BUILD_GATES Day 1.

### Implications

- No Day 1 intelligence implementation
- Provisional `LLMProvider` ABC only

### Related ADR

`docs/adr/0001-day1-foundation.md`

### Status

Accepted

---

## 2026-09-17 — Intelligence layer, not system of record

### Decision

Magnus is an intelligence layer over user life data; it must not silently become the authoritative system of record without explicit product rules.

### Why

`PRODUCT_CONTRACT.md` and `CORE_PROBLEM.md` principles.

### Implications

- LLM output must not silently mutate authoritative state
- Facts vs inference must remain distinguishable in later days

### Related ADR

None

### Status

Accepted

---

## 2026-09-17 — LLMProvider is provisional

### Decision

`LLMProvider` in `magnus/intelligence/` is a provisional boundary; no concrete provider on Day 1.

### Why

ADR 0001; avoid premature vendor coupling.

### Implications

- Methods may change when real use cases land
- Product logic lives in application/domain services

### Related ADR

`docs/adr/0001-day1-foundation.md`

### Status

Accepted
