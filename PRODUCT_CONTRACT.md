# Magnus — Product Contract

Authoritative product constraints for the Magnus MVP. Engineering and intelligence work must align with this document and with [docs/starter-kit/CORE_PROBLEM.md](docs/starter-kit/CORE_PROBLEM.md).

## Problem statement

People often know the life they want, but daily reality diverges from intention. Magnus exists to maintain an accurate picture of where the user stands, help decide what to do next, detect drift, and determine whether to change behavior, routine, strategy, or the goal itself — without reducing the product to a task list, habit tracker, or generic chatbot.

## Four Magnus questions

Magnus must continuously improve answers to:

1. **What do I want?** — outcomes, standards, projects, explorations, priorities, and constraints.
2. **Where do I stand?** — current state, evidence, progress, and uncertainty (facts vs inference).
3. **What should I do next?** — highest-value use of finite time, energy, and attention given current gaps.
4. **Should anything change?** — when progress stalls, which layer deserves reconsideration.

## Intelligence loop

Magnus implements a closed loop:

**Intent → Desired state → Current state → Strategy → Actions / routines → Execution → Evidence → Outcome → Trajectory → Diagnosis → Adaptation → (updated intent / strategy / action)**

The loop repeats. The product is the loop, not a collection of features.

## Diagnostic hierarchy

When execution or outcomes are off track, Magnus considers layers in order of fit (not always blaming “more discipline”):

| Layer | Typical question |
|-------|------------------|
| **Behaviour** | Is the user failing to execute the chosen action? |
| **Routine** | Does the surrounding system make the action unrealistic? |
| **Strategy** | Is the user executing but not moving the outcome? |
| **Goal** | Is the desired outcome outdated, conflicting, or no longer wanted? |
| **Information** | Is there insufficient evidence to decide responsibly? |

## Explicit non-goals (21-day MVP)

Do not build: mobile app, web dashboard, charts-as-product, dedicated finance/workout/calorie/journal modules, gamification, streaks, social features, full calendar/task replacement, multi-agent orchestration for its own sake, or integrations (wearables, Notion, brokers, etc.) unless explicitly scheduled later.

The MVP channel is **Telegram only**.

## Principles

### Intelligence layer, not database

Magnus is the **system of intelligence**, not the system of record. Calendars, banks, fitness apps, and task tools remain sources of truth; Magnus consumes evidence and reasons over it. During the Telegram MVP, conversational input stands in for integrations.

### Minimize user maintenance

The user should not maintain an “operating system.” Magnus maintains the model. Prefer inferring structure from natural messages over requiring repetitive structured forms.

### No advice without adequate evidence

Recommendations and diagnoses must be grounded in stored evidence and explicit uncertainty. When evidence is thin, Magnus says so (information layer) rather than inventing confidence.

### Observations vs inference

Distinguish what was **observed** from what was **inferred**. State and UI (later) must not blur the two.

### Goal ≠ strategy ≠ routine ≠ action

These are different concepts and must not be collapsed:

- **Goal / desired state** — what outcome or condition is sought or maintained.
- **Strategy** — hypothesis about how to move from current to desired state (versioned over time).
- **Routine** — recurring structure that supports execution.
- **Action** — concrete unit of doing.

Execution success is not the same as outcome success.

## Engineering alignment

- Domain and application logic stay independent of Telegram and LLM vendors.
- The LLM assists reasoning; it does not silently own authoritative state.
- See [docs/ARCHITECTURE.md](docs/ARCHITECTURE.md) for repository layout.
