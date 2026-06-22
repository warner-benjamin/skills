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

`plan.md` is the reviewed design document and source of truth for the goal, design, constraints, risks, hard stops, additional user approvals, implementation steps, verification strategy, execution slices, orchestration notes, integration policy, and commit policy. It must describe one chosen path, not unresolved decisions, options, alternate paths, TODOs, or open questions.

`checklist.md` is a status ledger only. Do not duplicate the plan there. Track phase gates, reviewer identity, review notes, slice statuses, decision-log entries, commit SHAs, verification evidence, and final-quality details.

`slices/<slice-id>.md` stores the prompt or work packet for a delegated or substantial local slice. `results/<slice-id>.md` stores the worker or local implementation report. These files are required when work crosses an agent/workspace boundary and optional for main-agent coding slices where the checklist, commit, and verification evidence are enough. `reviews/<slice-id>-review.md` stores slice review findings when a review lane runs or findings affect commit readiness.

Do not create or require slice artifact directories merely because a workflow exists. For direct local implementation, the plan should say `Execution mode: single-agent local` and `Main agent role: coding`, then record that no delegated slice prompts, worker reports, or slice-review artifacts are expected unless the risk-gated review policy escalates.

The `## Phase Gates` block is the only authoritative home for cross-phase status. Detail sections can record reviewers, findings, notes, paths, evidence, and reasons, but must not contain a second status field for the same gate.

Keep the scaffold lean. After `Phase Gates`, prefer these checklist sections: `Plan Review`, `Decision Log`, `Slices`, `Verification`, `Final Quality Review`, and `Commits`. Use `Decision Log` for hard stops, additional-approval decisions, reviewer-unavailable caveats, worker-import notes, user overrides, and other events that do not need a permanent table.

## Required Plan Shape

Use a small set of anchor headings and let the content be organic and domain-specific:

```text
Goal
Design
Implementation Steps
Verification / Acceptance
Execution Slices
Orchestration Notes
```

Write the plan in problem-solving mode, not form-filling mode. The headings are anchors for review and resume; they are not boxes that need equal weight. Spend most detail where the problem is hard, risky, or ambiguous, and keep obvious sections short.

Before review, apply the skeptical-engineer test: a competent engineer should be able to implement the chosen design without asking a planning question or inventing a core decision. If not, deepen the design, interview the user, or research more before review.

`Goal` states the objective, non-goals, success criteria, hard stops, additional user approvals, and workflow artifact path when they matter.

`Design` carries the full reviewed design, not final implementation code. Include observed facts, user requirements, resolved assumptions, constraints, risks, behavior/API/config/data contracts, invariants, edge cases, ownership boundaries, and the decisions behind the approach. Use domain-specific subsections when they communicate the design better than generic headings.

`Implementation Steps` is the ordered technical work. For code changes, name files, functions, tests, migrations, data/config shapes, and contract deltas when known. Steps answer what must change.

`Verification / Acceptance` gives concrete commands, expected artifacts, acceptance criteria, primary verifier, completion proof, and honest fallback or skip rules.

`Execution Slices` defines the execution mode, main agent role, and implementation/review/verification/commit units. A slice may contain one step, part of a large step, or several small steps. Slices answer how the work is safely executed, reviewed, verified, and committed.

Use one execution mode:

- `single-agent local`: the main agent directly implements slices in the current workspace.
- `multi-agent delegated`: worker lanes own implementation slices and the main agent coordinates, imports, verifies, and commits.
- `hybrid`: some slices are implemented directly by the main agent and others are delegated.

Use one main agent role:

- `coding`: the main agent edits, tests, stages, commits, and reports directly.
- `manager`: the main agent coordinates workers/reviewers, imports delegated work, verifies, stages, commits, and reports.
- `hybrid`: the main agent acts as coding agent for some slices and manager/integrator for others.

For a simple single-agent implementation, use one slice with `Owner: main agent as coding agent` and explicitly avoid delegated artifact requirements. For delegated or hybrid work, each slice should state whether the main agent is acting as coding agent or manager/integrator for that slice.

`Orchestration Notes` records slice order, dependency readiness, artifact creation mode, retry/re-slice rules, reviewer-unavailable behavior, failed-check behavior, integration policy, final-quality routing, and reusable artifacts.

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

- `Plan review: non-blocking`: the selected low-level or high-level review flow ran and no blocking findings remain.
- `Plan review: unavailable`: no independent reviewer was available; report this caveat to the user. Do not proceed to implementation unless implementation approval is given after this caveat is shown.
- `Implementation approval: waiting`: planning may continue, but implementation must not start.
- `Implementation approval: approved`: the user directly answered the required implementation-approval question, or the original request explicitly instructed Codex not to stop for implementation approval after planning/review. Invoking the workflow, giving plan feedback, approving plan content, accepting reviewer fixes, or saying a plan edit looks good does not approve implementation. Record the approval evidence as the user's own approving words (a short quote) or the exact pre-authorization instruction, not a Codex paraphrase such as "user approved".
- `Initial verification: passed`: implementation verification matched the plan's blast radius and passed.
- `Final quality review: not-required`: docs-only, research-only, small one-shot, or explicitly skipped with a reason.
- `Final verification: passed`: verification was re-run after any final cleanup.

If a phase cannot satisfy its precondition, update `checklist.md` with the exact blocker and stop the blocked action.

## Resume From Existing Plan

When resuming or restarting implementation from an existing workflow, do not create a duplicate run directory unless the user asks for a new plan. Re-read `plan.md`, `checklist.md`, recent commits, and the working tree. Continue from the first incomplete or failed phase gate, preserving recorded approvals, skipped-review caveats, slice reports, and commit SHAs.

If the plan is stale against the codebase, route back to `managed-plan` for a targeted plan update and same-reviewer re-review before implementation continues.

## Phase Ownership

- `managed-plan` writes the reviewed design, implementation steps, verification/acceptance strategy, execution slices, additional user approvals, plan review outcome, rejected findings, and implementation approval state.
- `managed-implement` writes slice statuses, review statuses, commit SHAs, integration results, initial verification, and whether final quality is required.
- `managed-quality` writes the final quality decision, cleanup slice, re-verification evidence, and final verification.
- `managed-workflow` owns cross-phase routing, reusable recipes, and final-report synthesis. `managed-implement` owns implementation goal-mode fit and activation. Phase skills append evidence and phase summaries; the orchestrator owns the final read-through and completion narrative.

## Commit Policy

The main agent owns staging and committing on the current branch unless the plan explicitly assigns commit authority elsewhere. Worker agents may edit their assigned workspace when that is the active runner model, but they must not make final commits to the integration branch unless the plan explicitly assigns that authority.

For each implementation slice, commit only that slice's intended code, tests, docs, and workflow artifact updates that exist before the commit. Do not include unrelated user or concurrent-agent changes.

Aim for one focused, independently green commit per slice: each commit should build and pass its checks on its own so history stays bisectable. Split a slice into multiple commits when that keeps each commit coherent, and keep a change in one commit when it genuinely cannot be split. Prefer smaller self-contained commits, but never split a change into commits that individually break the build.

Update review notes, targeted-check evidence, and checklist slice status before committing when those artifacts are part of the repo. Record the resulting commit SHA in `checklist.md` after the commit; that SHA ledger update can be included in the next workflow-artifact commit, a final metadata commit, or left uncommitted when the workflow directory is intentionally local-only.

## Slice Artifacts

Use `managed-implement/references/slice-artifacts.md` as the authoritative contract for slice prompts, reports, and reviews.

If a worker returns changes from a forked workspace, inspect the worker's diff, import only intended changes into the main agent's current branch, run the slice checks locally, and record the source workspace or branch in the slice report or checklist.

## Approval And Branching

The plan must distinguish hard stops, additional user approvals, and implementation approval. Planned implementation always waits for a direct implementation-approval answer after planning unless the original request explicitly instructed Codex not to stop for implementation approval after planning/review. After implementation approval is recorded, operate autonomously inside the reviewed plan until a hard stop, failed additional approval, or uncovered decision is reached.

Plan feedback is not implementation approval. Plan edits, critiques, approving comments about plan content, and reviewer-fix discussions keep the workflow in planning unless the user directly answers the implementation-approval question.

Record additional user approvals in the plan for consequential actions that still need user approval after implementation starts, such as irreversible local deletes, broad codemods, costly jobs, public or external mutations, or already-identified hard-stop exceptions. Do not use additional user approvals to leave ordinary design decisions, path choices, or implementation options unresolved.

Use `Execution Slices` and `Orchestration Notes` to record execution mode, main agent role, slice order, dependencies, artifact creation mode, readiness rules, retry/re-slice rules, reviewer-unavailable behavior, failed-check behavior, and how final-quality findings become cleanup slices.

## Final Report

Use `final-report.md` for synthesized results, not raw subagent dumps:

```text
Outcome
Changes
Completion Proof
Remaining Risks
Follow-up
```
