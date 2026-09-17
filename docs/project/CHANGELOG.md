# Magnus V2 — Project Changelog

Meaningful product, architecture, infrastructure, and build changes (not every git commit).

---

## 2026-09-18 — Documentation operating system

### Added

- `docs/project/` canonical doc pack (product, build, decisions, questions, current state, changelog).
- `docs/daily/day-01.md` build-day record.
- `.cursor/rules/magnus-project-governance.mdc`.

### Changed

- Moved canonical docs from repo root and `docs/starter-kit/` into `docs/project/`.
- Retired `docs/starter-kit/` as active path; ADRs remain in `docs/adr/`.

### Decisions

- Document authority model in `SOURCE_OF_TRUTH.md` (product / infra / build / daily / ADR / open questions).

### Debt introduced/resolved

- Resolved: scattered doc paths and duplicate navigation in README.
- Resolved: retired `docs/DAY_1_AUDIT.md` in favor of `docs/daily/day-01.md` and `CURRENT_STATE.md`.

---

## 2026-09-18 — Day 1 close-out (infra)

### Changed

- Supabase git migration id aligned to hosted `20260917051947`.
- Removed manual `magnus_connectivity_probe` table from hosted `public`.

### Decisions

- See `DECISION_LOG.md` (migration id alignment, authority order).

---

## 2026-09-17 — Day 1 foundation

### Added

- FastAPI health (`/health`, `/health/live`), async DB check, Railway deploy config.
- Telegram `/start` long-polling.
- Supabase baseline migration; ADR 0002 Supabase migrations.
- Tests for config, startup, health, Telegram lifespan.

### Removed

- Alembic from active architecture (superseded by Supabase migrations).

### Decisions

- Clean-room GitHub repo, Railway runtime, `DATABASE_URL` + asyncpg, no Supabase SDK, one polling replica, `ssl=require` for pooler on Railway.

### Debt introduced/resolved

- Non-blocking: CI, OpenAPI exposure, strict TLS verify, replica enforcement in repo.
