# Magnus starter kit

These documents are the **authoritative product and build reference** for the clean-room Magnus MVP. Read them before implementing features; do not infer requirements from legacy Magnus repositories.

| Document | Purpose |
|----------|---------|
| [CORE_PROBLEM.md](./CORE_PROBLEM.md) | Why Magnus exists, the four questions, control loop, principles, anti-patterns |
| [MVP_BUILD_PLAN.md](./MVP_BUILD_PLAN.md) | 21-day Telegram MVP scope, domain model, day-by-day tasks, stack, hard rules |
| [BUILD_GATES.md](./BUILD_GATES.md) | Release gates per day; when to advance; universal audit prompt |

## How we use this kit

1. **Product decisions** — `CORE_PROBLEM.md` and the philosophy sections of `MVP_BUILD_PLAN.md`
2. **What to build each day** — the matching day section in `MVP_BUILD_PLAN.md`
3. **Whether the day is done** — `BUILD_GATES.md` for that day (PASS / PASS WITH DEBT / FAIL)

## Related docs (created during the build)

The build plan calls for additional living documents as implementation proceeds, for example:

- `PRODUCT_CONTRACT.md` (Day 1)
- `ARCHITECTURE.md`, `DOMAIN_MODEL.md`, daily notes under `docs/daily/`

Living docs created so far:

- [PRODUCT_CONTRACT.md](../../PRODUCT_CONTRACT.md) (Day 1)
- [ARCHITECTURE.md](../ARCHITECTURE.md) (Day 1)

Until other planned docs exist, this starter kit plus those files are the source of truth.

## Cursor

Project rules in `.cursor/rules/` include clean-room constraints and a pointer to this starter kit.
