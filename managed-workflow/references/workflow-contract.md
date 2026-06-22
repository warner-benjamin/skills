# Managed Workflow Contract

Read this before creating, resuming, or handing off a managed workflow.

## Artifact Layout

Use one run directory:

```text
workflows/<slug>/
|-- plan.md
|-- checklist.md
|-- slices/       # created on demand for delegated or substantial slice packets
|-- results/      # created on demand for worker or substantial local reports
|-- reviews/      # created on demand when a review artifact is produced
`-- final-report.md
```

`plan.md` is the reviewed design document and single source of truth. It carries:

- the goal, design, constraints, risks, and hard stops
- additional user approvals
- implementation steps and verification strategy
- execution slices and orchestration notes
- integration policy and commit policy

It must describe one chosen path, not unresolved decisions, options, alternate paths, TODOs, or open questions.

`checklist.md` is a status ledger only; do not duplicate the plan there. Track:

- phase gates
- reviewer identity and review notes
- slice statuses and commit SHAs
- decision-log entries
- verification evidence and final-quality details

`slices/<id>.md` (work packet) and `results/<id>.md` (worker/local report) are required when work crosses an agent/workspace boundary; optional for local coding slices where the checklist, commit, and checks suffice. `reviews/<id>-review.md` is required when a review lane runs or findings affect commit readiness. Do not create these directories just because a workflow exists: for direct local work, set `Execution mode: single-agent local` / `Main agent role: coding` and record that no slice prompts or reports are expected unless review/resume context makes them useful.

The `## Phase Gates` block is the only authoritative home for cross-phase status. Detail sections may record reviewers, findings, paths, evidence, and reasons, but never a second status field for the same gate.

Keep the scaffold lean. After `Phase Gates`, prefer these sections: `Plan Review`, `Decision Log`, `Slices`, `Verification`, `Final Quality Review`, `Commits`. Use `Decision Log` for one-off events that don't need a permanent table (hard stops, approvals, reviewer-unavailable caveats, overrides).

## Required Plan Shape

Use these anchor headings; keep content organic and domain-specific:

```text
Goal
Design
Implementation Steps
Verification / Acceptance
Execution Slices
Orchestration Notes
```

Write in problem-solving mode, not form-filling mode. Headings are anchors, not boxes that need equal weight — spend detail where the problem is hard or ambiguous and keep obvious sections short.

Before review, apply the skeptical-engineer test: a competent engineer should be able to implement the chosen design without asking a planning question or inventing a core decision. If not, deepen the design, interview the user, or research more.

- `Goal`: objective, non-goals, success criteria, hard stops, additional user approvals, and workflow artifact path when they matter.
- `Design`: the full reviewed design (not final code) — observed facts, user requirements, resolved assumptions, constraints, risks, behavior/API/config/data contracts, invariants, edge cases, ownership boundaries, and the decisions behind the approach. Use domain-specific subsections when they communicate better than generic headings.
- `Implementation Steps`: the ordered technical work — what must change. For code, name files, functions, tests, migrations, data/config shapes, and contract deltas when known.
- `Verification / Acceptance`: concrete commands, expected artifacts, acceptance criteria, primary verifier, completion proof, and honest fallback/skip rules.
- `Execution Slices`: the execution mode, main agent role, and implementation/review/verification/commit units — how the work is safely executed. A slice may be one step, part of a step, or several small steps.
- `Orchestration Notes`: slice order, dependency readiness, artifact creation mode, retry/re-slice rules, reviewer-unavailable and failed-check behavior, integration policy, final-quality routing, and reusable artifacts.

Execution mode (pick one):

- `single-agent local`: the main agent implements slices directly in the current workspace.
- `multi-agent delegated`: worker lanes own implementation slices; the main agent coordinates, imports, verifies, and commits.
- `hybrid`: some slices direct, others delegated.

Main agent role (pick one):

- `coding`: edits, tests, stages, commits, and reports directly.
- `manager`: coordinates workers/reviewers, imports delegated work, verifies, stages, commits, and reports.
- `hybrid`: coding for some slices, manager/integrator for others.

For simple single-agent work, use one slice with `Owner: main agent as coding agent` and no delegated artifacts. For delegated or hybrid work, each slice states whether the main agent codes or manages it.

### Example: a single-agent local plan (abridged)

The lean common case — most managed work looks like this, not a multi-agent swarm.

```text
## Goal
Add rate limiting to the public `/search` endpoint. Non-goal: limiting authed routes.
Success: anonymous callers over 60 req/min get HTTP 429; existing tests stay green.

## Design
`SearchController.handle` calls `SearchService` directly today. Add a `RateLimiter`
(token bucket, 60/min/IP) in `middleware/rate_limit.py`, wired in `app.py` before the
search route. Counters live in the existing Redis client (`cache.redis`); key
`rl:search:<ip>`, TTL 60s. On limit, return 429 with `Retry-After`. Edge case:
missing/forwarded IP -> fall back to the socket peer address.

## Implementation Steps
1. Add `middleware/rate_limit.py` with `RateLimiter` and a `limit()` decorator.
2. Wire it onto the `/search` route in `app.py`.
3. Tests in `tests/test_rate_limit.py`: under-limit passes, over-limit 429, TTL reset.

## Verification / Acceptance
`pytest tests/test_rate_limit.py` green, then full `pytest` green. Primary verifier: pytest.

## Execution Slices
Execution mode: single-agent local. Main agent role: coding.
- Slice rl-1 (steps 1-3): owner main agent as coding agent; checks = pytest;
  review = main-agent (test-backed, low risk); commit = one focused commit.

## Orchestration Notes
Single slice, no dependencies, no workers or slice artifacts.
Final quality review: not-required (single low-risk slice).
```

## Phase Gates

Use these checklist fields as handoffs between phase skills:

```text
Plan review: pending | blocking | non-blocking | unavailable
Implementation approval: waiting | approved
Implementation status: pending | in-progress | complete
Initial verification: pending | passed | failed | skipped
Final quality review: pending | passed | failed | not-required
Final verification: pending | passed | failed | skipped
```

Allowed gate meanings:

- `Plan review: non-blocking`: the selected review flow ran and no blocking findings remain.
- `Plan review: unavailable`: no independent reviewer was available; report the caveat. Do not implement unless approval is given after the caveat is shown.
- `Implementation approval: waiting`: planning may continue; implementation must not start.
- `Implementation approval: approved`: the user directly answered the approval question, or the original request explicitly pre-authorized skipping it. Invoking the workflow, giving plan feedback, approving plan content, or accepting reviewer fixes does not approve implementation. Record evidence as the user's own approving words (a short quote) or the exact pre-authorization, never a paraphrase like "user approved".
- `Initial verification: passed`: verification matched the plan's blast radius and passed.
- `Final quality review: not-required`: docs-only, research-only, a single low-risk slice, or explicitly skipped with a reason.
- `Final verification: passed`: verification was re-run after any final cleanup.

If a phase cannot satisfy its precondition, record the exact blocker in `checklist.md` and stop the blocked action.

## Resume From Existing Plan

When resuming, do not create a duplicate run directory unless the user asks for a new plan. Re-read `plan.md`, `checklist.md`, recent commits, and the working tree, then continue from the first incomplete or failed gate, preserving recorded approvals, skipped-review caveats, slice reports, and commit SHAs.

If the plan is stale against the codebase, route back to `managed-plan` for a targeted update and same-reviewer re-review before continuing.

## Phase Ownership

- `managed-plan`: reviewed design, implementation steps, verification/acceptance, execution slices, additional user approvals, plan-review outcome, rejected findings, implementation-approval state.
- `managed-implement`: slice statuses, review statuses, commit SHAs, integration results, initial verification, and whether final quality is required.
- `managed-quality`: final quality decision, cleanup slice, re-verification evidence, final verification.
- `managed-workflow`: cross-phase routing, reusable recipes, final-report synthesis, and the final read-through and completion narrative. `managed-implement` owns implementation goal-mode fit and activation. Phase skills append evidence and summaries.

## Commit Policy

The main agent owns staging and committing on the current branch unless the plan assigns commit authority elsewhere. Workers may edit their assigned workspace under the active runner model but must not commit to the integration branch unless the plan explicitly grants it.

Commit only the slice's intended code, tests, docs, and pre-existing workflow-artifact updates — never unrelated user or concurrent-agent changes.

Aim for one focused, independently green commit per slice so history stays bisectable. Split into multiple commits when that keeps each coherent, and keep a change whole when it genuinely can't be split, but never split into commits that individually break the build.

Update review notes, check evidence, and checklist slice status before committing when those artifacts are in the repo. Record the commit SHA in `checklist.md` after; that ledger update can ride the next artifact commit, a final metadata commit, or stay uncommitted when the workflow directory is local-only.

## Slice Artifacts

`managed-implement/references/slice-artifacts.md` is the authoritative contract for slice prompts, reports, and reviews.

If a worker returns changes from a forked workspace, inspect its diff, import only intended changes into the current branch, run the slice checks locally, and record the source workspace or branch.

## Approval And Branching

The plan must distinguish hard stops, additional user approvals, and implementation approval. Planned implementation always waits for a direct approval answer unless the original request explicitly pre-authorized skipping it. Once approval is recorded, operate autonomously inside the reviewed plan until a hard stop, failed additional approval, or uncovered decision.

Plan feedback is not implementation approval: edits, critiques, approving comments on plan content, and reviewer-fix discussions keep the workflow in planning until the user directly answers the approval question.

Record additional user approvals for consequential actions that still need sign-off after implementation starts (irreversible local deletes, broad codemods, costly jobs, public/external mutations, or named hard-stop exceptions). Don't use them to leave ordinary design or path decisions unresolved.

Use `Execution Slices` and `Orchestration Notes` to record execution mode, main agent role, slice order, dependencies, artifact creation mode, readiness rules, retry/re-slice rules, reviewer-unavailable and failed-check behavior, and how final-quality findings become cleanup slices.

## Final Report

Use `final-report.md` for synthesized results, not raw subagent dumps:

```text
Outcome
Changes
Completion Proof
Remaining Risks
Follow-up
```
