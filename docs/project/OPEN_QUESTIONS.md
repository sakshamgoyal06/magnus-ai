# Magnus V2 — Open Questions

## Purpose

Questions here are **unresolved**. Cursor must not silently decide them because implementation needs an answer.

If implementation is blocked, surface the question for product/architecture review. When resolved, move to **Resolved** and link `DECISION_LOG.md` / ADR.

---

## Active

### Q-001 — Production OpenAPI exposure

**Question**  
Should production keep FastAPI `/docs` and `/openapi.json` public, disable them, or protect them?

**Why it matters**  
Public API surface before any auth story exists.

**Affected build day**  
Hardening (pre–wide release); not Day 2 domain modeling.

**Current options**

- Leave public (Day 1 default)
- Disable in production via config
- Gate behind auth / network

**Status**  
Open

---

### Q-002 — Supabase TLS verification strictness

**Question**  
Keep asyncpg `ssl=require` only, or move to full certificate verification on Railway?

**Why it matters**  
Security vs operational compatibility with pooler TLS chains.

**Affected build day**  
Infrastructure; not blocking Day 2 schema design.

**Current options**

- Keep `ssl=require`
- Use CA bundle (e.g. certifi) with verify-full

**Status**  
Open

---

### Q-003 — RLS on first user tables

**Question**  
When Day 2+ adds `public` tables, is RLS required on all user-scoped tables from the first migration?

**Why it matters**  
Supabase defaults and server-only `DATABASE_URL` access pattern.

**Affected build day**  
First persistence migration.

**Current options**

- RLS + policies from first user data table
- Server-only access via Railway URL initially, RLS later

**Status**  
Open

---

### Q-004 — Railway replica enforcement

**Question**  
Is runbook-only “one replica” enough, or should repo/CI enforce replica count for polling?

**Why it matters**  
`telegram.error.Conflict` when multiple consumers use one token.

**Affected build day**  
Ops / deploy hygiene.

**Current options**

- Manual checklist only
- Document in Railway + periodic audit
- Automated check (future)

**Status**  
Open

---

### Q-005 — Schema apply vs Railway deploy order

**Question**  
Must `supabase db push` always complete before a Railway deploy that depends on new DDL?

**Why it matters**  
Release process clarity.

**Affected build day**  
Day 2+ when DDL ships.

**Current options**

- Manual: push migrations then deploy
- CI pipeline ordering (not implemented)

**Status**  
Open

---

### Q-006 — CI for pytest

**Question**  
Add GitHub Actions for `uv run pytest` now or after Day 2 integration tests exist?

**Why it matters**  
Merge confidence vs setup cost.

**Affected build day**  
Engineering process.

**Current options**

- Add minimal CI now
- Defer until DB integration tests in CI

**Status**  
Open

---

### Q-007 — Placeholder directories

**Question**  
Keep `output/`, `skills/`, `tools/` (.gitkeep only) or remove until needed?

**Why it matters**  
Repo clarity.

**Affected build day**  
None.

**Current options**

- Keep
- Remove

**Status**  
Open

---

### Q-008 — Production logging configuration

**Question**  
Railway starts Uvicorn directly; `LOG_LEVEL` is wired in `magnus-api` CLI only. Unify app logging for Railway?

**Why it matters**  
Consistent log verbosity in production.

**Affected build day**  
Infrastructure polish.

**Current options**

- Configure in app startup for all entrypoints
- Uvicorn flags in `railway.toml`

**Status**  
Open

---

### Q-009 — Manual verification gaps

**Question**  
Confirm Railway auto-deploy, one replica, and production `/start` — who signs off and where is it recorded?

**Why it matters**  
Day 1 gate evidence.

**Affected build day**  
Day 1 close-out.

**Current options**

- Tick `SOURCE_OF_TRUTH.md` §10 after owner verify
- Record in `docs/daily/day-01.md`

**Status**  
Open

---

## Resolved

*(None yet.)*
