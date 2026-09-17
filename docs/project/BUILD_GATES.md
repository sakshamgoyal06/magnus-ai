# MAGNUS — DAILY BUILD GATES

## Purpose

This document determines whether development can safely advance from one day of the 21-day Magnus MVP plan to the next.

A day is NOT complete merely because:

- code was written
- tests are green
- the bot responds
- Cursor says implementation is finished

Each day must satisfy four gates:

### 1. Functional Gate

Does the feature actually work?

### 2. Architecture Gate

Was it implemented in a way that does not compromise later development?

### 3. Product Gate

Does the behavior remain faithful to the Magnus product philosophy?

### 4. Evidence Gate

Do tests or real examples demonstrate that it works?

Every day ends with:

**PASS**

**PASS WITH DEBT**

or

**FAIL**

---

# PASS RULE

Move to the next day only when:

- all Critical criteria pass
- no known P0 defect exists
- architectural debt does not invalidate tomorrow's work
- automated tests exist for core behavior
- one realistic end-to-end example has been demonstrated

---

# PASS WITH DEBT RULE

Advance only when:

- missing issue is not required by tomorrow's architecture
- debt is documented
- concrete remediation exists
- product correctness is not compromised

Do not use PASS WITH DEBT repeatedly to hide fundamental problems.

---

# FAIL RULE

Do not proceed if:

- important state can become corrupted
- tests do not represent real behavior
- implementation contradicts CORE_PROBLEM.md
- later days would need to work around today's architecture
- behavior only succeeds for hard-coded demo examples

---

# DAY 1 GATE — FOUNDATION

## Critical

- clean repository exists
- old Magnus code was not copied into domain architecture
- application starts from documented command
- PostgreSQL connection works
- migrations framework works (`supabase/migrations/`; apply via Supabase CLI — see `docs/project/SUPABASE_MIGRATIONS.md`)
- FastAPI health endpoint works
- Telegram `/start` works
- secrets are excluded from version control
- tests execute successfully

## Architecture

Telegram code is isolated from domain/application code.

There is no premature "agent" abstraction.

Repository structure matches documented architecture.

## Product

`CORE_PROBLEM.md` and `PRODUCT_CONTRACT.md` are present and treated as authoritative.

`docs/project/SOURCE_OF_TRUTH.md` is present and treated as authoritative for infrastructure (GitHub, Railway, Supabase, `supabase/migrations/`, Telegram hosting, env var names).

## Test

Delete local environment and follow README from scratch.

If setup cannot be reproduced, Day 1 fails.

### Ask Cursor

> Audit Day 1 against BUILD_GATES.md. Do not modify anything initially. Give every criterion PASS/FAIL with evidence from files/tests. Then fix all failures and rerun the audit. Do not begin Day 2 until every Critical gate passes.

---

# DAY 2 GATE — DOMAIN MODEL

## Critical

The schema can cleanly represent:

- Outcome
- Standard
- Project
- Exploration
- Desired State
- Current State
- Strategy
- Leading Indicator
- Outcome Indicator
- Evidence
- Action
- Routine

Strategies can have historical versions.

Objects can be archived without deletion.

## Architecture

No single huge JSON column is being used as a substitute for modelling core concepts.

Goal, Strategy, Routine and Action are different entities/concepts.

## Product

An Outcome does not require a Routine.

A Standard does not need a target date.

An Exploration does not pretend the answer is already known.

## Test Scenario

Represent:

> Goal: 90 kg by July  
> Current: 112 kg  
> Strategy: deficit + gym + walking  
> Leading: diet, gym, steps  
> Outcome: weight trend.

Then represent:

> Exploration: Do I want to become a PM?

If both feel natural in the schema, pass.

### Cursor audit

Ask:

> Prove that the Day 2 domain model represents the health outcome and career exploration examples without hacks or generic metadata blobs. Show the instantiated objects and relationships. Flag any modelling choice that will make trajectory or diagnosis difficult later.

---

# DAY 3 GATE — HISTORY

## Critical

Every meaningful state change produces an immutable historical record.

Current state is still easy to query.

Changing a strategy preserves the previous strategy.

## Test

Create strategy A.

Change to strategy B.

Query:

> What strategy was active before B?

Must return A.

Update current weight several times.

Historical measurements must remain available.

## Architecture

Do not require replaying the entire event ledger just to load ordinary current state.

### Failure Condition

If future analysis cannot reconstruct what changed and when, Day 3 fails.

---

# DAY 4 GATE — TELEGRAM ADAPTER

## Critical

Telegram messages are persisted.

Telegram-specific IDs/types do not pollute domain entities.

Application services can be tested without Telegram.

Duplicate Telegram updates do not create obvious duplicate messages.

## Test

Simulate a Telegram update through tests without contacting Telegram.

Then invoke the same application service directly.

Both must reach the same underlying logic.

---

# DAY 5 GATE — CAPTURE ENGINE

THIS IS A MAJOR GATE.

Do not advance casually.

## Critical

At least these intents work:

- create goal/object
- update object
- record evidence
- create action
- complete action
- reflection
- strategy change candidate
- unknown

## Product

LLM output cannot directly modify database state.

Ambiguous statements are not treated as irreversible decisions.

## Mandatory Test Set

Test at least 30 natural-language utterances.

Including:

> Gym done.

Expected:

record completion/evidence.

Not:

create gym goal.

---

> Maybe I don't want to change jobs anymore.

Expected:

candidate goal review / ambiguity.

Not:

archive goal.

---

> I weighed 111.2 this morning.

Expected:

numeric evidence.

---

> Remind me to renew passport.

Expected:

action.

---

> I think four workouts is too much.

Expected:

potential routine/strategy change requiring interpretation.

## Quality Threshold

≥90% of simple cases correctly routed.

All dangerous mutations require confirmation if ambiguous.

### If not

Do not proceed.

Days 6–21 depend heavily on capture quality.

---

# DAY 6 GATE — ONBOARDING

## Critical

Fresh user can create 3 meaningful LifeObjects conversationally.

Maximum reasonable onboarding time:

~10 minutes.

Magnus does not require every field.

## Product

Magnus asks only questions whose answers materially improve its ability to help.

## Test

Run onboarding with three simulated personas.

### Persona A

Precise:

> Lose 20 kg by July.

### Persona B

Vague:

> I want to be healthier.

### Persona C

Exploratory:

> I'm not sure whether I should change careers.

Magnus must handle all three differently.

## Failure

If onboarding feels like filling a form through chat, redesign it.

---

# DAY 7 GATE — `/NOW`

THIS IS ANOTHER MAJOR GATE.

## Critical

Blocked actions cannot rank first.

Urgency alone cannot dominate importance.

Goal importance affects priority.

Trajectory risk can influence priority.

Duration/context can influence feasibility.

## Test Set

Create 10 competing actions including:

- overdue low-value task
- strategic important task
- blocked urgent task
- health action
- optional Magnus-development action

Inspect ranking.

## Human Evaluation

Ask:

> If I actually had 45 free minutes right now, would I trust this recommendation?

Run at least 10 scenarios.

Target:

≥8/10 recommendations judged sensible.

If not:

do not move on without understanding why.

---

# DAY 8 GATE — TODAY

## Critical

Magnus returns maximum 3 true priorities.

It does not simply list the first three `/now` actions.

DailyPlan is persisted.

Revised plan keeps history.

## Product

The output should reduce overwhelm rather than create another task list.

## Test

Give user 25 outstanding actions.

`/today` must still produce ≤3 meaningful priorities.

---

# DAY 9 GATE — EVIDENCE

## Critical

Evidence supports:

- numeric
- binary
- textual
- behavioral
- self-reported

Each item has source/time/confidence.

Evidence can be linked to indicators.

## Test

Feed:

> Weight 111.4  
> Gym done  
> Slept badly  
> Interview went poorly

Ensure each becomes different appropriate evidence.

## Failure

If Evidence becomes an unstructured dumping ground, fix it now.

Trajectory depends on it.

---

# DAY 10 GATE — TRAJECTORY

MAJOR GATE.

## Critical

Magnus separates routine adherence from actual outcome movement.

Numeric expected-vs-observed trajectory works.

UNKNOWN exists when evidence is insufficient.

## Mandatory Scenario

Target:

112 → 90 kg.

Gym adherence:

90%.

Weight:

flat.

Expected result:

**Outcome trajectory = OFF_TRACK/AT_RISK**

not:

ON_TRACK because gym adherence is high.

## Test

Test:

- ahead
- on track
- at risk
- off track
- unknown

against deterministic data.

No LLM should be required for basic numeric trajectory math.

---

# DAY 11 GATE — ADHERENCE

## Critical

Magnus can independently calculate strategy adherence.

Trajectory and adherence produce separate outputs.

## Mandatory Matrix

Test all four:

1. High adherence / good outcome
2. Low adherence / bad outcome
3. High adherence / bad outcome
4. Low adherence / good outcome

The system must distinguish all four.

If trajectory and adherence have become conflated anywhere, stop.

---

# DAY 12 GATE — DIAGNOSIS

THIS IS THE MOST IMPORTANT GATE IN THE MVP.

## Critical

Magnus can produce:

- EXECUTION_FAILURE
- ROUTINE_FAILURE
- STRATEGY_FAILURE
- GOAL_ISSUE
- INSUFFICIENT_INFORMATION
- NO_INTERVENTION_NEEDED

## Mandatory Scenarios

### Execution

Plan good, adherence temporarily low.

Expected:

EXECUTION_FAILURE candidate.

### Routine

Every Friday workout fails for six weeks.

Expected:

ROUTINE_FAILURE.

### Strategy

95% adherence but outcome flat.

Expected:

STRATEGY_FAILURE.

### Goal

Repeated deprioritization + explicit reduced interest.

Expected:

GOAL_ISSUE review candidate.

### Insufficient Data

Weight off track, exercise known, food completely unknown.

Expected:

INSUFFICIENT_INFORMATION or appropriately cautious diagnosis.

## Quality Rule

Diagnosis must cite evidence.

Diagnosis must include confidence.

Diagnosis must include plausible alternative explanations where meaningful.

## Human Evaluation

At least 20 diagnosis scenarios.

Target:

≥85% judged directionally correct.

No high-confidence catastrophic misclassification.

If this does not pass, do not proceed.

---

# DAY 13 GATE — ADAPTATION

## Critical

Magnus proposes changes without silently making major goal/strategy changes.

ReviewSessions persist.

User decisions are recorded.

Strategy modification creates a new version.

## Test

Run:

strategy review → new strategy chosen → old strategy remains queryable.

Goal review → user chooses to keep goal → Magnus respects decision.

## Product

Magnus should facilitate reasoning, not dictate life choices.

---

# DAY 14 GATE — WEEKLY REVIEW

MAJOR PRODUCT VALUE GATE.

## Critical

Weekly review does more than summarize metrics.

It interprets them.

## Test

Give one simulated week where:

- gym improved
- weight didn't
- weekend food worsened

Bad response:

> Gym 85%, weight flat, diet 60%.

Good response:

> Exercise improved materially without corresponding outcome improvement. Weekend diet inconsistency remains the stronger intervention candidate.

## Human Test

Ask:

> Did this review tell me something useful I might not have noticed myself?

At least 3 of 5 simulated reviews must clearly pass.

Eventually target much higher.

---

# DAY 15 GATE — MEMORY

## Critical

Magnus can retrieve relevant previous:

- decisions
- active strategies
- experiments
- evidence
- diagnoses

without inserting the entire conversation history into every prompt.

## Test

Simulate several weeks.

Ask:

> Why did we change my workout plan?

Magnus should retrieve the actual decision/evidence.

No hallucinated rationale.

---

# DAY 16 GATE — PROACTIVE INTERVENTION

MAJOR RETENTION/TRUST GATE.

## Critical

Magnus can decide to stay silent.

Repeated identical interventions are suppressed.

Low-confidence issues do not create aggressive alerts.

## Evaluation

Run at least 30 simulated state changes.

For each ask:

> Should Magnus interrupt?

Evaluate precision.

Priority is **precision over recall**.

A missed low-value intervention is preferable to annoying the user.

Initial target:

≥80% of sent interventions judged useful.

---

# DAY 17 GATE — CROSS-GOAL PRIORITIZATION

## Critical

Magnus can reason across competing areas.

It does not assume every goal should receive equal attention.

Minimum viable routines can protect important areas during temporary priority shifts.

## Mandatory Scenario

Career interview in 5 days.

Health slightly behind.

Magnus project optional.

Expected:

career temporarily dominates, health minimum viable routine preserved, Magnus deprioritized.

## Failure

If everything becomes P0, cross-goal prioritization fails.

---

# DAY 18 GATE — EVALUATION HARNESS

## Critical

At least 20 reusable scenarios exist.

One command runs evaluation.

Results are saved.

Important failures are inspectable.

## Coverage must include

- capture
- trajectory
- adherence
- diagnosis
- `/now`
- weekly reviews
- proactive interventions
- uncertainty

## Requirement

Changing prompts/models later must allow comparing before/after quality.

If evaluation remains subjective and manual only, Day 18 fails.

---

# DAY 19 GATE — RELIABILITY

## Critical

- duplicate messages safe
- model/provider failure handled
- database failure handled reasonably
- secrets protected
- user authorization works
- important decisions are auditable
- JSON data export works
- logs allow debugging
- no user-facing tracebacks

## Chaos Tests

Simulate:

- Telegram duplicate update
- LLM timeout
- malformed structured output
- DB failure
- unknown command
- long message
- concurrent messages

No silent state corruption.

---

# DAY 20 GATE — REAL DOGFOOD

This gate cannot be passed entirely by automated tests.

Use Magnus for a full real day.

## During the day

Use:

- `/today`
- multiple `/now`
- natural capture
- completion logs
- reflection
- evening review

## Score every meaningful interaction

0 — harmful/wrong

1 — useless

2 — acceptable

3 — useful

4 — surprisingly useful

## Minimum Gate

No P0 issues.

No repeated state corruption.

Average core interaction score ≥2.5.

At least one interaction scores 4.

If nothing feels surprisingly useful, Magnus has not yet demonstrated sufficient product magic.

Do not add features to compensate.

Improve the core loop.

---

# DAY 21 GATE — MVP FREEZE

Run complete clean-database simulation.

## Required end-to-end behavior

User establishes goals.

Magnus learns current state.

Strategy established.

Evidence accumulates.

`/today` works.

`/now` works.

Actions complete.

Trajectory changes.

Adherence assessed.

Drift detected.

Diagnosis produced.

Review triggered.

Strategy updated.

History preserved.

Weekly review reflects change.

Proactive intervention behaves responsibly.

## Final Product Questions

Answer YES/NO:

### Q1

Can Magnus accurately explain what the user currently wants?

### Q2

Can Magnus explain where they currently stand?

### Q3

Can Magnus provide a credible next action?

### Q4

Can Magnus detect meaningful divergence?

### Q5

Can Magnus explain whether the likely issue is execution, routine, strategy, goal or missing evidence?

### Q6

Can Magnus remember prior decisions?

### Q7

Can Magnus appropriately remain silent?

### Q8

Does using Magnus create less cognitive work than it removes?

### Q9

Would the user voluntarily keep using this version?

If Q1–Q6 fail:

MVP is not ready.

If Q8 fails:

the product architecture is wrong.

If Q9 fails:

do not solve it by immediately adding UI.

Understand why.

---

# UNIVERSAL DAILY AUDIT PROMPT

At the end of every day give Cursor this exact instruction:

> Perform the Day [X] release-gate audit from BUILD_GATES.md.
>
> Do not begin by fixing code.
>
> First independently inspect the implementation, tests, schema, logs and documentation and create a table containing:
>
> - Gate criterion
> - PASS / FAIL / PASS WITH DEBT
> - Concrete evidence
> - Risk if left unresolved
>
> Then run all relevant automated tests and the required realistic scenarios for this day's gate.
>
> Challenge the implementation rather than trying to prove it correct.
>
> Specifically look for:
>
> - hard-coded demo behavior
> - accidental coupling
> - state corruption risk
> - over-reliance on LLM reasoning where deterministic logic is possible
> - LLM mutations without validation
> - missing uncertainty handling
> - concepts that have been incorrectly collapsed together
> - violations of CORE_PROBLEM.md
> - violations of PRODUCT_CONTRACT.md
> - technical debt that will make tomorrow's work substantially harder
>
> Only after producing the audit should you fix failures.
>
> Rerun the entire audit after fixes.
>
> Finish with exactly one recommendation:
>
> **READY FOR DAY [X+1]**
>
> or
>
> **DO NOT PROCEED**
>
> If READY, explain what assumptions tomorrow's implementation may safely rely upon.
>
> If DO NOT PROCEED, list only the blocking issues.
>
> Do not implement any Day [X+1] features during this process.

---

# WEEKLY DEEP GATES

In addition to daily gates, perform deeper architecture reviews after Days:

**7, 14 and 21.**

Use this instruction:

> Perform a clean-room Magnus architecture review as if you did not write the code.
>
> Read CORE_PROBLEM.md and PRODUCT_CONTRACT.md first.
>
> Review everything built so far.
>
> Ask whether we are accidentally drifting toward:
>
> - task manager
> - habit tracker
> - generic chatbot
> - goal dashboard
> - LifeOS feature bundle
> - one giant autonomous agent
>
> Identify:
>
> 1. concepts that are becoming unnecessarily complex
> 2. abstractions introduced too early
> 3. missing abstractions now causing repeated hacks
> 4. features that should be deleted
> 5. data the user is being asked to manually maintain unnecessarily
> 6. reasoning that should be deterministic
> 7. deterministic logic that incorrectly requires semantic judgment
> 8. opportunities to reduce the codebase while preserving capability
>
> Then run the evaluation suite.
>
> Recommend one of:
>
> **CONTINUE**
>
> **REFACTOR BEFORE CONTINUING**
>
> **RETHINK PRODUCT ASSUMPTION**
>
> Do not add new features as part of this audit.