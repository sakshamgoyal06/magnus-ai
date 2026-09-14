# Magnus (clean-room MVP)

Adaptive personal intelligence system — **Telegram-first** 21-day MVP. This repository is a clean-room rebuild; product and engineering direction live in the starter kit, not in legacy Magnus repos.

## Starter kit (read this first)

| Document | Path |
|----------|------|
| Core problem definition | [docs/starter-kit/CORE_PROBLEM.md](docs/starter-kit/CORE_PROBLEM.md) |
| 21-day MVP build plan | [docs/starter-kit/MVP_BUILD_PLAN.md](docs/starter-kit/MVP_BUILD_PLAN.md) |
| Daily build gates | [docs/starter-kit/BUILD_GATES.md](docs/starter-kit/BUILD_GATES.md) |

Index and usage: [docs/starter-kit/README.md](docs/starter-kit/README.md).

## Project rules

Cursor rules in [`.cursor/rules/`](.cursor/rules/) include clean-room constraints and mandatory reference to the starter kit.

## Implementation status

Day 1 foundation (FastAPI, PostgreSQL, Telegram `/start`, `PRODUCT_CONTRACT.md`, etc.) is defined in the build plan — not yet implemented in this repo.

## Legacy scaffold note

An early [CrewAI](https://crewai.com) JSON-first sample (`crew.jsonc`, `agents/`) remains in the tree from initial project setup. It is **not** part of the Magnus MVP spec and will be replaced or removed as Magnus Day 1 work lands.
