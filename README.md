# Magnus (clean-room MVP)

Adaptive personal intelligence system — **Telegram-first** 21-day MVP.

**Repository:** [github.com/sakshamgoyal06/magnus-ai](https://github.com/sakshamgoyal06/magnus-ai)

**New session?** Start with [docs/project/CURRENT_STATE.md](docs/project/CURRENT_STATE.md).

## Project documentation

```text
docs/project/   Current canonical product, build, and infrastructure truth
docs/adr/       Architecture decision history
docs/daily/     Build-day records and gate results
```

| Document | Path |
|----------|------|
| Current build state (handoff) | [docs/project/CURRENT_STATE.md](docs/project/CURRENT_STATE.md) |
| Infrastructure source of truth | [docs/project/SOURCE_OF_TRUTH.md](docs/project/SOURCE_OF_TRUTH.md) |
| Core problem | [docs/project/CORE_PROBLEM.md](docs/project/CORE_PROBLEM.md) |
| Product contract | [docs/project/PRODUCT_CONTRACT.md](docs/project/PRODUCT_CONTRACT.md) |
| Build gates | [docs/project/BUILD_GATES.md](docs/project/BUILD_GATES.md) |
| 21-day build plan | [docs/project/MVP_BUILD_PLAN.md](docs/project/MVP_BUILD_PLAN.md) |
| Architecture | [docs/project/ARCHITECTURE.md](docs/project/ARCHITECTURE.md) |
| Decision log | [docs/project/DECISION_LOG.md](docs/project/DECISION_LOG.md) |
| Open questions | [docs/project/OPEN_QUESTIONS.md](docs/project/OPEN_QUESTIONS.md) |
| Changelog | [docs/project/CHANGELOG.md](docs/project/CHANGELOG.md) |
| Supabase migrations | [docs/project/SUPABASE_MIGRATIONS.md](docs/project/SUPABASE_MIGRATIONS.md) |
| Railway deploy | [docs/project/DEPLOYMENT_RAILWAY.md](docs/project/DEPLOYMENT_RAILWAY.md) |
| Cursor + GitHub | [docs/project/CURSOR_AND_GITHUB.md](docs/project/CURSOR_AND_GITHUB.md) |

Cursor governance: [`.cursor/rules/magnus-project-governance.mdc`](.cursor/rules/magnus-project-governance.mdc).

## Implementation status

**Day 1 (foundation)** complete with debt — see [docs/daily/day-01.md](docs/daily/day-01.md). Production: Railway → Supabase PostgreSQL; Telegram `/start`; `/health` DB ping.

## Local setup

```bash
cp .env.example .env
uv sync --extra dev
docker compose up -d db   # optional, for pytest
uv run magnus-api
```

Health: http://localhost:8000/health

Schema: `supabase link --project-ref uktsxijrewbqjcjnrfdv` then `supabase db push` — see [docs/project/SUPABASE_MIGRATIONS.md](docs/project/SUPABASE_MIGRATIONS.md).

## Tests

```bash
uv run pytest
```

## Railway

See [docs/project/DEPLOYMENT_RAILWAY.md](docs/project/DEPLOYMENT_RAILWAY.md).
