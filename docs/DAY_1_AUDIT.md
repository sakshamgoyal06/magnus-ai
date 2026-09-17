# Magnus V2 — Day 1 Audit

**Audit date:** 2026-09-18  
**Repository HEAD (at audit time):** `48125c5` on `main`  
**Auditor scope:** Full repository read; production HTTP checks on `https://magnus-ai-production.up.railway.app` (no Railway dashboard access).

---

## 1. Executive Summary

Magnus V2 Day 1 is a **small, clean-room Python service**: one FastAPI app (`magnus.api.main:app`) with two HTTP health routes, async SQLAlchemy/asyncpg to Supabase Postgres via `DATABASE_URL`, and in-process Telegram long-polling for `/start` only. Schema authority lives in `supabase/migrations/`; the app does not run migrations at boot. There is **no Alembic**, **no Supabase Python SDK**, **no domain tables**, and **no persistence of Telegram chats**.

**Confirmed at audit time:** Production `GET /health` returns `200` with `database: connected`; `GET /health/live` returns `200`.

The codebase contains **no second Telegram poller path** within a single process. Observed `telegram.error.Conflict` in deploy logs is **not wired to `/health` 503**; it indicates **two consumers of the same bot token** (typically overlapping Railway deploy replicas and/or a local `magnus-api` with the same token).

Documentation was recently aligned to Day 1 Supabase-only infrastructure (`48125c5`). Residual items are mostly **manual Railway/Supabase verification**, **operational hygiene** (one replica, token rotation after leaks), and **non-blocking** placeholders (empty packages, unused `get_db_session`, default FastAPI `/docs`).

**Verdict for handoff:** Foundation is **internally consistent and deployable**; suitable for **independent validation** and Day 2 planning with the caveats in §19–§22.

---

## 2. Day 1 Intended Scope

Per `docs/starter-kit/BUILD_GATES.md` (Day 1 gate) and implemented repo state:

| Area | Intended |
|------|----------|
| Repository | Clean layout, no copied legacy domain |
| Runtime | Documented start command, FastAPI, PostgreSQL connectivity |
| Migrations | Git-backed `supabase/migrations/`, applied via Supabase CLI |
| Health | Real DB ping on `/health` |
| Telegram | `/start` response via adapter → application layer |
| Secrets | Not in git |
| Tests | Pytest suite runnable |
| Docs | README, architecture, infrastructure source of truth |

**Explicitly not Day 1:** domain model, repositories with I/O, LLM providers, chat persistence, webhooks, Supabase Auth/Storage SDK, CI pipeline (not present in repo).

---

## 3. Current Technology Stack

| Component | Version / detail | Source |
|-----------|------------------|--------|
| Python | `>=3.12,<3.14` (Railway logs showed 3.13) | `pyproject.toml`, deploy logs |
| Package manager | **uv** + `uv.lock` | repo |
| FastAPI | 0.141.1 (locked) | `uv.lock` |
| Uvicorn | 0.53.0 (locked) | `uv.lock` |
| SQLAlchemy | 2.0.53 + asyncio | `uv.lock` |
| asyncpg | 0.31.0 | `uv.lock` |
| pydantic-settings | 2.15.0 | `uv.lock` |
| python-telegram-bot | 21.11.1 | `uv.lock` |
| PostgreSQL (prod) | Supabase project `magnus-ai`, ref `uktsxijrewbqjcjnrfdv` | docs + config |
| PostgreSQL (local optional) | Postgres 16 via Docker Compose | `docker-compose.yml` |
| Deploy | Railway, Railpack | `railway.toml`, `railpack.json` |
| Schema tool | Supabase CLI (not a Python dep) | `supabase/` |

---

## 4. Current Repository Structure

```text
magnus-ai/
├── .cursor/
│   ├── environment.json          # Cloud Agent: uv sync, optional GITHUB_TOKEN
│   └── rules/                    # clean-room + starter-kit Cursor rules
├── .env.example                  # Documented env names (no secrets)
├── .gitignore                    # .env, .venv, caches, supabase/.temp
├── PRODUCT_CONTRACT.md           # Product authority (Day 1)
├── README.md                     # Setup, run, test, deploy pointers
├── docker-compose.yml            # Optional local Postgres only
├── docs/
│   ├── ARCHITECTURE.md           # Module layout + boundaries
│   ├── CURSOR_AND_GITHUB.md      # GitHub-only remote workflow
│   ├── DEPLOYMENT_RAILWAY.md     # Railway runbook
│   ├── SOURCE_OF_TRUTH.md        # Infrastructure authority
│   ├── SUPABASE_MIGRATIONS.md    # Schema workflow
│   ├── DAY_1_AUDIT.md            # This file
│   ├── adr/0001, 0002            # Foundation + Supabase migrations ADRs
│   └── starter-kit/              # Product/build plan (authoritative product)
├── magnus/                       # Application package
│   ├── api/                      # FastAPI app + health routes
│   ├── application/              # Use cases (start message only)
│   ├── domain/                   # Empty placeholder (Day 2+)
│   ├── infrastructure/           # config, DB, production validation
│   ├── intelligence/             # LLMProvider ABC only
│   ├── telegram/                 # Bot builder, /start handler
│   ├── repositories/             # Empty placeholder
│   ├── prompts/, evaluations/, jobs/  # Empty placeholders
│   └── tests/                    # Pytest
├── output/, skills/, tools/      # .gitkeep only (no code)
├── pyproject.toml, uv.lock
├── railpack.json, railway.toml
└── supabase/
    ├── config.toml               # CLI project link
    └── migrations/               # Day 1 baseline SQL
```

**Not tracked (correctly ignored):** `.venv/`, `.pytest_cache/`, `.ruff_cache/`, `.env`.

**No** `alembic/`, `scripts/`, `.github/workflows/`, or committed database files.

---

## 5. Runtime Architecture

```text
                    ┌─────────────────────────────────────┐
                    │  Single OS process (Railway)        │
                    │  uvicorn → magnus.api.main:app      │
                    └─────────────────────────────────────┘
                                      │
          ┌───────────────────────────┼───────────────────────────┐
          │                           │                           │
          ▼                           ▼                           ▼
   FastAPI lifespan            HTTP routers                 asyncio.Task
   (startup/shutdown)          /health, /health/live        run_telegram_polling
          │                           │                           │
          ▼                           │                           ▼
   create_engine(DATABASE_URL)        │                  python-telegram-bot
   session_factory on app.state       │                  Application.updater
          │                           │                  .start_polling()
          ▼                           ▼                           │
   asyncpg → Supabase Postgres    JSON responses                  ▼
   (SELECT 1 in /health)                                    CommandHandler("start")
                                                                    │
                                                                    ▼
                                                          magnus.application.start
                                                          (static welcome text)
```

**Facts:** One FastAPI app instance per process; one `polling_task` created in lifespan when `TELEGRAM_BOT_TOKEN` is set; no worker pool configured in repo.

---

## 6. Deployment Architecture

```text
User
  │
  ▼
Telegram client
  │
  ▼
Telegram Bot API (HTTPS)
  │
  ▼
Railway public URL (magnus-ai-production.up.railway.app → container :8080)
  │
  ├── GET /health/live  (Railway deploy gate — no DB)
  ├── GET /health       (DB SELECT 1)
  └── Long-poll getUpdates (outbound HTTPS to Telegram)
  │
  ▼
DATABASE_URL (session pooler) ──TLS ssl=require──► Supabase PostgreSQL
```

**External services used at runtime:** Telegram API, Supabase Postgres. **Not used:** Supabase REST/SDK, OpenAI, Railway Postgres plugin (documented as forbidden).

**Manual verification required:** Railway replica count = 1; GitHub auto-deploy branch; exact service linked to public domain.

---

## 7. Application Startup Sequence

1. **Process start:** Railway runs  
   `uv run uvicorn magnus.api.main:app --host 0.0.0.0 --port $PORT`  
   (`railway.toml`, `railpack.json`).

2. **Import `magnus.api.main`:** Module-level `app = create_app()` builds FastAPI with lifespan (no DB/Telegram yet).

3. **Uvicorn loads ASGI app** and runs **lifespan startup** (`magnus/api/main.py`):
   - `get_settings()` (cached) reads env + optional `.env`.
   - `validate_production_settings()` if `APP_ENV=production` (token required, no localhost DB).
   - `create_engine()` → stores `app.state.db_engine`, `app.state.session_factory`.
   - Logs database driver and host.
   - If `telegram_bot_token` set: `build_telegram_application` → `initialize()` → `start()` → `asyncio.create_task(run_telegram_polling)`.

4. **Ready:** Uvicorn accepts HTTP; Telegram task blocks on `asyncio.Future()` while updater polls.

5. **Shutdown:** Cancel polling task → `updater.stop()` → `telegram_app.stop/shutdown()` → `engine.dispose()`.

**Import side effects:** Only construction of FastAPI app object at import; DB/Telegram start only in lifespan (not at import).

**Local `magnus-api` entry:** `uvicorn.run(..., reload=True)` only when `APP_ENV=development` — still **one worker** unless operator adds workers manually.

---

## 8. FastAPI Structure

| Method | Path | Purpose | File |
|--------|------|---------|------|
| GET | `/health/live` | Liveness (always 200 if process up) | `magnus/api/routes/health.py` |
| GET | `/health` | DB connectivity via `SELECT 1` | `magnus/api/routes/health.py` |
| GET | `/docs` | Swagger UI (FastAPI default) | FastAPI built-in |
| GET | `/openapi.json` | OpenAPI schema | FastAPI built-in |

**No** admin/debug routes beyond health. **No** middleware registered in code. **No** dependency-injection DB session on routes yet.

### `/health` behaviour (code-derived)

- **200:** `check_database_connection(engine)` succeeds → `{"status":"ok","database":"connected"}`.
- **503:** Any exception from DB check → `{"status":"unhealthy","database":"disconnected","detail": "<exception str>", "host": "<parsed host>"}` (host omitted if unavailable).
- **Does not check:** Telegram, Supabase SDK, external LLM APIs.
- **Railway suitability:** Repo configures deploy probe on **`/health/live`** so deploy succeeds when Uvicorn is up even if DB is temporarily down; **`/health`** is for operational DB verification.

### Observed historical 503

Logs showing `GET /health HTTP/1.1" 503` during incident period align with **DB connection failures** (wrong URL, DNS, SSL), not Telegram. Telegram `Conflict` appears in **stderr** from polling loop, separate from health route.

---

## 9. Telegram Structure

**Flow:**

```text
Telegram /start
  → python-telegram-bot CommandHandler("start", start_command)
  → magnus/telegram/handlers/start.py (transport only)
  → magnus.application.start.build_start_reply()
  → reply_text(static string)
```

| Concern | Implementation |
|---------|----------------|
| Token | `Settings.telegram_bot_token` from env `TELEGRAM_BOT_TOKEN` |
| Builder | `ApplicationBuilder().token(token).build()` in `magnus/telegram/bot.py` |
| Handlers | Only `/start` |
| Polling | `application.updater.start_polling(drop_pending_updates=True)` in `run_telegram_polling` |
| Errors | Library logs exceptions (e.g. Conflict); not caught in app code |
| Shutdown | Lifespan cancels task, `updater.stop()`, app `stop/shutdown` |
| User ID / chat | Not read or stored |
| Persistence / memory | None |
| Business logic in handler | Minimal; message text lives in `application/start.py` (appropriate) |

**Duplicate poller in this codebase?** **No evidence.** Single `create_task(run_telegram_polling)` per lifespan. **External duplication** (second replica, local dev, old deploy) **can** cause `Conflict` with same token.

---

## 10. Database / Supabase Structure

| Question | Answer |
|----------|--------|
| Supabase Python client? | **No** |
| Connection | `DATABASE_URL` → SQLAlchemy `create_async_engine` + **asyncpg** |
| Sync access? | **No** |
| ORM models | `Base = DeclarativeBase` only; **no mapped tables** |
| Reads/writes in app | **Only** `SELECT 1` in health check |
| Migrations in app boot? | **No** |
| Alembic | **Absent** |
| Schema files | `supabase/migrations/20260917051947_day1_baseline.sql` (`SELECT 1;` comment-only baseline) |
| Pooling | SQLAlchemy pool with `pool_pre_ping=True` |
| Retries | None explicit beyond pool pre-ping |
| SSL | `connect_args={"ssl": "require"}` for Supabase hostnames (`database.py`) |
| Failure at startup | Production misconfig raises in `validate_production_settings`; bad DB does **not** block Uvicorn start — fails on `/health` only |

**Canonical persistence (Day 1):** There is **no application read/write path** yet. **Canonical connectivity check:** async Postgres via `DATABASE_URL`. **Canonical schema strategy:** new SQL files under `supabase/migrations/`, apply with `supabase db push` (documented).

**Unused but intentional:** `get_db_session`, `session_factory` on app state — prepared for Day 2+, not wired to routes.

---

## 11. Configuration

| Variable | Required | Consumed in | Railway | Local default | Fail-fast |
|----------|----------|-------------|---------|---------------|-----------|
| `DATABASE_URL` | de facto yes | `Settings.database_url`, engine | Yes | localhost docker URL in `.env.example` | Prod: no localhost if `APP_ENV=production` |
| `TELEGRAM_BOT_TOKEN` | prod yes | `Settings.telegram_bot_token`, lifespan | Yes | None (polling off) | Prod: missing → `RuntimeError` at startup |
| `APP_ENV` | prod yes | `Settings.app_env`, validation, reload | Yes | `development` | — |
| `LOG_LEVEL` | no | `uvicorn.run` log level (CLI entry only) | Optional | `INFO` | — |
| `PORT` | Railway auto | `Settings.port` | Injected | 8000 | — |
| `OPENAI_API_KEY` | no | **Not read** | No | — | — |
| `SUPABASE_URL` | no | **Not read** | No | commented in `.env.example` | — |
| `SUPABASE_ANON_KEY` | no | **Not read** | No | commented | — |
| `GITHUB_TOKEN` | Cloud Agent only | `.cursor/environment.json` install | No | — | — |

**Secrets in git:** **None** in tracked files (`.env` gitignored). **CRITICAL:** If tokens/passwords were ever committed to history, rotate and scan history separately — not verified in this audit.

**Settings cache:** `get_settings()` is `@lru_cache` — env changes require process restart.

---

## 12. Railway Configuration

| Item | Repo value |
|------|------------|
| Builder | `RAILPACK` (`railway.toml`) |
| Start | `uv run uvicorn magnus.api.main:app --host 0.0.0.0 --port $PORT` |
| Health path | `/health/live` |
| Health timeout | 120s |
| Workers | **Not set** → Uvicorn default **1 worker** |
| Replicas | **Not in repo** — docs require **1** for polling |

**Safe for 1 service / 1 replica / 1 process / 1 poller:** **Yes**, if Railway UI matches (no scale-out, no multi-worker uvicorn flags).

**Manual UI checks:** Replica count, health path override, env vars, active deployment commit, public domain → service mapping, PORT (observed 8080 in logs).

---

## 13. GitHub / Repository State

- **Canonical remote:** `origin` → `https://github.com/sakshamgoyal06/magnus-ai` only.
- **Branch:** `main` (production).
- **Tracked files:** 57 paths — application, docs, config, lockfile; no `.venv`, no `.env`.
- **Placeholders:** `output/`, `skills/`, `tools/` (.gitkeep only) — no functional code.
- **No** second project root or monorepo confusion.

**Risk:** None identified suggesting active code lives elsewhere; starter kit still references historical repo name `magnus-core` as a **suggested name only** in MVP_BUILD_PLAN (not this GitHub repo).

---

## 14. Documentation State

| Document | Role |
|----------|------|
| `docs/SOURCE_OF_TRUTH.md` | **Infrastructure authority** |
| `README.md` | Setup, run, test, deploy entry |
| `docs/ARCHITECTURE.md` | Module boundaries |
| `docs/DEPLOYMENT_RAILWAY.md` | Production runbook |
| `docs/SUPABASE_MIGRATIONS.md` | Schema workflow |
| `docs/starter-kit/*` | Product + 21-day plan + gates |
| `PRODUCT_CONTRACT.md` | Product authority |
| ADRs | Recorded stack/migration decisions |

**Hierarchy matches intended model.** Minor gap: `SOURCE_OF_TRUTH.md` does not have a dedicated “Day 1 non-goals / limitations” section (content spread across ARCHITECTURE, BUILD_GATES, PRODUCT_CONTRACT).

**Drift:** README local health URL uses port 8000; Railway uses `$PORT` (documented).

---

## 15. Tests

| File | Covers |
|------|--------|
| `test_config.py` | URL normalization |
| `test_startup.py` | SSL connect args, production validation rules |
| `test_health.py` | Health 503/200 mapping, live route, integration with DB if reachable |
| `test_start.py` | Application message + handler wiring |
| `test_telegram_boot.py` | Lifespan starts/stops Telegram when token set (mocked) |

**Not tested:** Live Telegram API, production Supabase, Railway deploy, SSL to real pooler in CI. **conftest** requires local Postgres for integration tests using `api_client`.

**No GitHub Actions** — tests not enforced on push in repo.

---

## 16. Known Runtime Issues

| Issue | Status | Notes |
|-------|--------|-------|
| `/health` 503 | **Resolved** (audit HTTP check: 200 connected) | Was DB URL/DNS/SSL during migration period |
| `telegram.error.Conflict` | **Intermittent / operational** | Two `getUpdates` on same token; codebase has one poller per process |
| `ssl=require` (no cert verify) | **Active design** | Tradeoff for Railway TLS chains; encrypts but does not verify server identity |
| FastAPI `/docs` public | **Open by default** | No auth; acceptable for Day 1 but note for hardening |

---

## 17. Migration Debt Audit

| Item | Location | Classification |
|------|----------|----------------|
| `postgresql+psycopg://` URL rewrite | `config.py` | **KEEP** (compat for pasted URLs) |
| psycopg2 mentioned in comments/docs | config, DEPLOYMENT | **KEEP** (explains no psycopg2 dep) |
| `normalize_database_url` | config | **KEEP** |
| Empty packages (domain, repos, jobs…) | magnus/ | **KEEP** (Day 1 skeleton) |
| `LLMProvider` ABC | intelligence | **KEEP** (ADR 0001) |
| `get_db_session` unused | database.py | **REMOVE LATER** or wire Day 2 |
| `output/`, `skills/`, `tools/` .gitkeep | root | **INVESTIGATE** (remove if unused) |
| Starter kit “legacy Magnus” wording | BUILD_GATES, rules | **KEEP** (process guardrail) |
| MVP_BUILD_PLAN `magnus-core` name | starter-kit | **KEEP** (historical suggestion, not infra) |
| Alembic / SQLite / Render / Heroku | — | **Absent** |

---

## 18. Day 1 Acceptance Checklist

| # | Criterion | Score |
|---|-----------|-------|
| 1 | One canonical source of truth | **PASS** |
| 2 | GitHub canonical source control | **PASS** |
| 3 | Deterministic builds | **PASS** (`uv.lock`) |
| 4 | Application starts successfully | **PASS** (prod + code path) |
| 5 | FastAPI binds correctly | **PASS** |
| 6 | Railway-compatible PORT | **PASS** |
| 7 | `/health` behaviour understood | **PASS** |
| 8 | Supabase configuration exists | **PASS** |
| 9 | Persistent storage architecture unambiguous | **PASS** (no app persistence yet; strategy clear) |
| 10 | Telegram bot initialization exists | **PASS** |
| 11 | Telegram can receive messages | **PARTIAL** (code complete; live `/start` not re-verified in this audit) |
| 12 | Polling once per app process | **PASS** (code); **PARTIAL** (infra replicas manual) |
| 13 | Shutdown behaviour safe | **PASS** |
| 14 | Secrets not committed | **PASS** (current tree) |
| 15 | Environment variables documented | **PASS** |
| 16 | Deployment architecture understandable | **PASS** |
| 17 | Legacy DB architecture cleaned | **PASS** |
| 18 | No unexplained migration debt | **PASS** |
| 19 | SOURCE_OF_TRUTH reflects implementation | **PARTIAL** (missing explicit Day 1 non-goals block) |
| 20 | Day 2 can start without restructuring | **PASS** (with ssl/replica/docs caveats) |

---

## 19. Remaining Day 1 Fixes

### Blocking before Day 2

None identified from repository + successful production `/health` at audit time. **Owner should confirm:** Telegram `/start` on production bot, Railway replica = 1, `supabase db push` baseline on hosted project.

### Recommended but non-blocking

- Mark `SOURCE_OF_TRUTH` manual checklist items as done after verification.
- Rotate Telegram token and DB password if ever exposed in chat/logs.
- Add CI (pytest on push) when ready.
- Disable or protect `/docs` in production if desired.
- Document “do not run local bot with production token while Railway is up.”

### Cleanup backlog

- Remove or use `output/`, `skills/`, `tools/` placeholders.
- Wire or defer `get_db_session` when repositories land.

---

## 20. Day 2 Starting Boundary

**Day 2 may assume:**

- FastAPI app with lifespan, health routes, async engine + session factory on `app.state`.
- Telegram adapter pattern: handlers → application services.
- `supabase/migrations/` workflow and ADR 0002.
- Production on Railway + Supabase pooler `DATABASE_URL`.
- Empty `domain/`, `repositories/` packages ready for entities.

**Does not exist yet:**

- Domain entities, repositories with DB I/O, migrations with table DDL (beyond baseline).
- Message persistence, user identity storage, non-`/start` commands.
- LLM implementation, prompts in use, jobs, evaluations.
- Supabase SDK, webhooks, multi-replica strategy.

---

## 21. Important Architectural Decisions Already Made

- **Deploy:** Single Railway Python service; Uvicorn ASGI; no in-container migrations.
- **Persistence:** Generic `DATABASE_URL` + SQLAlchemy async; schema via Supabase CLI git migrations.
- **Telegram:** Long-polling in same process as API; one production replica while polling.
- **Boundaries:** Telegram/API → application → (future domain); no agent framework Day 1.
- **Config:** pydantic-settings; production fail-fast for token and localhost DB.
- **Health:** Split liveness (`/health/live`) vs DB readiness (`/health`).

---

## 22. Questions Requiring Owner Decision

1. **Production OpenAPI `/docs`:** leave public or restrict before wider exposure?
2. **`ssl=require` without certificate verification:** accept for MVP or invest in full CA verify on Railway?
3. **Placeholder directories** (`output/`, `skills/`, `tools/`): keep for future tooling or delete?

*(Replica count and bot token sharing are operational, not architectural forks — document as runbook discipline.)*

---

## 23. Handoff Snapshot

See section **COPY THIS SECTION INTO CHATGPT** below (also suitable for pasting to another engineer).

---

# COPY THIS SECTION INTO CHATGPT

## What Magnus is

Magnus is a **clean-room, Telegram-first personal intelligence MVP** (21-day plan). Day 1 establishes infrastructure only: users can hit `/start` and get a static welcome message; the system verifies Postgres connectivity; no goal tracking, AI, or chat persistence exists yet. Product philosophy lives in `PRODUCT_CONTRACT.md` and `docs/starter-kit/CORE_PROBLEM.md`.

## Day 1 scope (what was built)

- New GitHub repo **`sakshamgoyal06/magnus-ai`**, branch **`main`**, single `origin` remote.
- Python **3.12+** package **`magnus`** managed with **uv** and **`uv.lock`**.
- **FastAPI** application entry: **`magnus.api.main:app`**.
- **Health:** `GET /health/live` (process only, for Railway deploy gate); `GET /health` runs **`SELECT 1`** via async SQLAlchemy/asyncpg and returns **503** only on database errors (not Telegram failures).
- **Database:** Production **Supabase PostgreSQL** (project **`magnus-ai`**, ref **`uktsxijrewbqjcjnrfdv`**). App uses env **`DATABASE_URL`** only — **no Supabase Python SDK**. Connection uses **asyncpg** with **`ssl=require`** for `*.supabase.co` and `*.pooler.supabase.com` hosts.
- **Schema:** Authoritative SQL in **`supabase/migrations/`**; apply with **`supabase db push`**. Railway **does not** run migrations. Day 1 baseline migration is effectively empty (no app tables). **No Alembic** in repo.
- **Telegram:** **`python-telegram-bot`** v21; token from **`TELEGRAM_BOT_TOKEN`**. Long-polling starts in FastAPI **lifespan** as one **`asyncio` task** calling **`updater.start_polling()`**. Only command: **`/start`** → handler in **`magnus/telegram/handlers/start.py`** → **`magnus.application.start.build_start_reply()`** (static text). No user/chat storage.
- **Production validation:** When **`APP_ENV=production`**, startup **raises** if token missing or **`DATABASE_URL`** contains localhost.
- **Deploy:** **Railway** with **Railpack**; start command **`uv run uvicorn magnus.api.main:app --host 0.0.0.0 --port $PORT`**; health check path **`/health/live`** in **`railway.toml`**. Public URL used in testing: **`https://magnus-ai-production.up.railway.app`**.
- **Docs authority:** Infrastructure **`docs/SOURCE_OF_TRUTH.md`**; setup **`README.md`**; Railway **`docs/DEPLOYMENT_RAILWAY.md`**; schema **`docs/SUPABASE_MIGRATIONS.md`**; layout **`docs/ARCHITECTURE.md`**; ADRs **`0001`** (stack), **`0002`** (Supabase migrations).
- **Tests:** Pytest under **`magnus/tests/`** (config, startup rules, health mapping, start handler, mocked Telegram lifespan). Full suite expects local Postgres at default **`DATABASE_URL`** unless overridden. **No CI workflow** in repo.

## Repository layout (meaningful)

- **`magnus/api/`** — FastAPI app, lifespan, health routes.
- **`magnus/infrastructure/`** — **`config.py`** (Settings), **`database.py`** (engine, health query), **`startup.py`** (prod checks).
- **`magnus/telegram/`** — bot builder + **`/start`** handler.
- **`magnus/application/`** — use case **`start.py`** (welcome message).
- **`magnus/intelligence/llm_provider.py`** — abstract ABC only; no implementation.
- **`magnus/domain/`**, **`repositories/`**, **`jobs/`**, **`prompts/`**, **`evaluations/`** — empty **`__init__.py`** placeholders for later days.
- **`supabase/`** — CLI **`config.toml`** + **`migrations/`**.
- **`docker-compose.yml`** — optional local Postgres **`magnus_dev`** for tests.
- **`.cursor/`** — agent install + rules (clean-room, starter-kit).

## Startup flow (production)

1. Uvicorn loads **`magnus.api.main:app`**.
2. Lifespan: load settings → validate production env → create async SQLAlchemy engine → store on **`app.state`** → if token present, init Telegram Application, **`start()`**, spawn polling task.
3. HTTP ready on **`$PORT`** (8080 on Railway in observed logs).
4. Shutdown: cancel polling, stop updater, dispose engine.

**Single process design:** Repo does **not** configure Uvicorn **`--workers`**. Exactly **one** Telegram polling loop per process. **Do not scale Railway replicas above 1** while using long-polling with the same token.

## Environment variables (names only)

| Name | Role |
|------|------|
| **`DATABASE_URL`** | Async Postgres URL (pooler recommended on Railway) |
| **`TELEGRAM_BOT_TOKEN`** | Bot token; required in production |
| **`APP_ENV`** | Set **`production`** on Railway |
| **`LOG_LEVEL`** | Logging (optional) |
| **`PORT`** | HTTP port (Railway-injected) |

**Not used by app:** **`SUPABASE_URL`**, **`SUPABASE_ANON_KEY`**, **`OPENAI_API_KEY`**. **`GITHUB_TOKEN`** only for Cursor Cloud Agent git push setup.

## HTTP routes

| Method | Path | Purpose |
|--------|------|---------|
| GET | **`/health/live`** | Liveness |
| GET | **`/health`** | DB **`SELECT 1`** |
| GET | **`/docs`**, **`/openapi.json`** | FastAPI defaults (unauthenticated) |

## Database & migrations (canonical)

- **Read/write in app Day 1:** none except health check.
- **Going forward:** add SQL files under **`supabase/migrations/`**, commit, **`supabase db push`** before/with deploy; app continues to use **`DATABASE_URL`** with SQLAlchemy.

## Telegram notes

- **Conflict error** (`terminated by other getUpdates request`): means **two bot instances** share a token — typically **deploy overlap** (old + new Railway container) and/or **local dev** running with production token. **Not caused by `/health` 503.** Code has **one** poller per process.

## Health status at audit (2026-09-18)

Independent HTTP check to production:

- **`GET /health`** → **`{"status":"ok","database":"connected"}`**
- **`GET /health/live`** → **`{"status":"ok"}`**

(Earlier **`503`** on **`/health`** was traced to **`check_database_connection`** failures: bad/misparsed **`DATABASE_URL`**, DNS, or SSL — fixed with session pooler URL and **`ssl=require`**.)

## Known limitations / debt

- No chat or user persistence; no LLM wired.
- **`ssl=require`** encrypts but does not verify server certificate (Railway/Supabase TLS workaround).
- **`get_db_session`** helper and **`session_factory`** on app state unused by routes yet.
- Empty root dirs **`output/`**, **`skills/`**, **`tools/`** (`.gitkeep` only).
- **`SOURCE_OF_TRUTH`** manual checklist items may still be unchecked in doc.
- No automated CI; production Telegram **`/start`** should be manually smoke-tested after deploy.

## Blockers before Day 2 feature work

**Repository/code:** none critical if production health stays green and owner confirms single replica + baseline migration applied on Supabase.

**Operational confirmation recommended:** Railway **one replica**; no duplicate local poller; Telegram **`/start`** works; hosted migration history includes **`20260917051947`** / **`day1_baseline`**; `public` has no Magnus app tables (probe table removed).

## What Day 2 builds on

Add **domain model**, **repositories**, **migrations with real tables**, and application services — using existing **engine/session factory**, **Telegram → application** boundary, and **Supabase migration workflow**. Do **not** reintroduce Alembic or Supabase SDK without a new ADR.

## Git state

- **Branch:** **`main`**
- **Recent infra commits include:** Railway **`/health/live`**, DB host in health errors, **`ssl=require`** for Supabase, doc alignment **`48125c5`**.

## Independent validation checklist for another engineer

1. Clone **`https://github.com/sakshamgoyal06/magnus-ai`**, **`uv sync --extra dev`**, optional **`docker compose up -d db`**, run **`uv run pytest`**.
2. Curl production **`/health`** and **`/health/live`**.
3. Message production bot **`/start`**.
4. Read **`docs/SOURCE_OF_TRUTH.md`** and confirm Railway env vars match (no secrets in repo).
5. Confirm **`grep -ri alembic`** (or equivalent) returns nothing material in application code.
6. Review **`magnus/api/main.py`** lifespan for single Telegram task.
7. Confirm **`railway.toml`** health path is **`/health/live`**.

This snapshot is self-contained and does not require repository access to understand Magnus V2 Day 1 foundation state.
