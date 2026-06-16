# Managed Workflow Contract

Read this before creating, resuming, or handing off a managed workflow.

## Artifact Layout

Use one run directory:

```text
workflows/<slug>/
|-- plan.md
|-- checklist.md
|-- slices/
|-- results/
|-- reviews/
`-- final-report.md
```

`plan.md` is the source of truth for goal, grounding, constraints, risks, approval gates, slice details, orchestration sequence, integration policy, verification strategy, and commit policy. It must describe one chosen path, not unresolved decisions, options, alternate paths, TODOs, or open questions.

`checklist.md` is a status ledger only. Do not duplicate the plan there. Track phase gates, reviewer identity, review notes, slice statuses, decision-log entries, commit SHAs, verification evidence, and final-quality details.

`slices/<slice-id>.md` stores the prompt or work packet for a slice before delegation or local implementation. `results/<slice-id>.md` stores the coding, research, or local implementation report. These files are required for every implementation slice. `reviews/<slice-id>-review.md` stores the slice review and is required when a review lane is available.

The `## Phase Gates` block is the only authoritative home for cross-phase status. Detail sections can record reviewers, findings, notes, paths, evidence, and reasons, but must not contain a second status field for the same gate.

Keep the scaffold lean. After `Phase Gates` and `Lifecycle`, prefer these checklist sections: `Plan Review`, `Decision Log`, `Slices`, `Verification`, `Final Quality Review`, and `Commits`. Use `Decision Log` for hard stops, approval-gate decisions, reviewer-unavailable caveats, worker-import notes, user overrides, and other events that do not need a permanent table.

## Required Plan Headings

Keep the plan concise enough to guide delegation and verification without replacing execution:

```text
Goal
Baseline
Success Criteria
Primary Verifier
Completion Proof
Current Context
Observed Facts
User Requirements
Resolved Assumptions
Constraints
Anti-cheating Constraints
Risks
Hard Stops
Approval Gates
Workflow Artifact Path
Implementation Slices
Orchestration Sequence
Integration Policy
Verification
Commit Policy
Reusable Artifacts
```

## Phase Gates

Use these checklist fields as handoffs between phase skills:

```text
Plan review: pending | blocking | non-blocking | unavailable
User implementation gate: pending | cleared
Implementation status: pending | in-progress | complete
Initial verification: pending | passed | failed | skipped
Final quality review: pending | passed | failed | not-required
Final verification: pending | passed | failed | skipped
```

Allowed gate meanings:

- `Plan review: non-blocking`: the selected low-level or high-level review flow ran and no blocking findings remain.
- `Plan review: unavailable`: no independent reviewer was available; report this caveat to the user. Do not proceed to implementation unless the user explicitly clears implementation after seeing this caveat.
- `User implementation gate: cleared`: the user explicitly cleared implementation, or explicitly authorized execution after plan review in the original request. If `Plan review` is `unavailable`, this clearance must happen after the unavailable-review caveat is shown.
- `Initial verification: passed`: implementation verification matched the plan's blast radius and passed.
- `Final quality review: not-required`: docs-only, research-only, small one-shot, or explicitly skipped with a reason.
- `Final verification: passed`: verification was re-run after any final cleanup.

If a phase cannot satisfy its precondition, update `checklist.md` with the exact blocker and stop the blocked action.

## Resume From Existing Plan

When resuming or restarting implementation from an existing workflow, do not create a duplicate run directory unless the user asks for a new plan. Re-read `plan.md`, `checklist.md`, recent commits, and the working tree. Continue from the first incomplete or failed phase gate, preserving recorded approvals, skipped-review caveats, slice reports, and commit SHAs.

If the plan is stale against the codebase, route back to `managed-plan` for a targeted plan update and same-reviewer re-review before implementation continues.

## Phase Ownership

- `managed-plan` writes the plan, observed facts, user requirements, resolved assumptions, approval gates, plan review outcome, rejected findings, and user gate state.
- `managed-implement` writes slice statuses, review statuses, commit SHAs, integration results, initial verification, and whether final quality is required.
- `managed-quality` writes the final quality decision, cleanup slice, re-verification evidence, and final verification.
- `managed-workflow` owns cross-phase routing, goal mode, reusable recipes, and final-report synthesis. Phase skills append evidence and phase summaries; the orchestrator owns the final read-through and completion narrative.

## Commit Policy

The manager owns staging and committing on the current branch. Worker agents may edit their assigned workspace when that is the active runner model, but they must not make final commits unless the plan explicitly assigns that authority.

For each implementation slice, commit only that slice's intended code, tests, docs, and workflow artifact updates that exist before the commit. Do not include unrelated user or concurrent-agent changes.

Aim for one focused, independently green commit per slice: each commit should build and pass its checks on its own so history stays bisectable. Split a slice into multiple commits when that keeps each commit coherent, and keep a change in one commit when it genuinely cannot be split. Prefer smaller self-contained commits, but never split a change into commits that individually break the build.

Update review notes, targeted-check evidence, and checklist slice status before committing when those artifacts are part of the repo. Record the resulting commit SHA in `checklist.md` after the commit; that SHA ledger update can be included in the next workflow-artifact commit, a final metadata commit, or left uncommitted when the workflow directory is intentionally local-only.

## Slice Artifacts

Before starting a slice, write `slices/<slice-id>.md` with the objective, context, ownership, dependencies, do/do-not list, expected output, verification, review requirement, report path, and commit boundary.

Each implementation, coding-agent, or research-agent report must be saved as `results/<slice-id>.md` and include:

```text
Agent identity:
Agent id/thread:
Workspace or branch:
Slice ID:
Prompt path:
Files changed:
Summary:
Verification run:
Verification result:
Review notes needed:
Blockers:
Remaining risks:
```

If a worker returns changes from a forked workspace, inspect the worker's diff, import only intended changes into the manager's current branch, run the slice checks locally, and record the source workspace or branch in the slice report or checklist.

## Approval And Branching

The plan must distinguish hard stops from approval gates. Planned implementation always waits for user feedback and implementation clearance after planning. After that gate is cleared, operate autonomously inside the approved plan until a hard stop, failed approval gate, or uncovered decision is reached.

Use `Approval Gates` for consequential actions that still need user approval after planning, such as irreversible local deletes, broad codemods, costly jobs, public or external mutations, or already-identified hard-stop exceptions. Do not use approval gates to leave ordinary design decisions, path choices, or implementation options unresolved.

Use `Orchestration Sequence` to record slice order, dependencies, readiness rules, retry/re-slice rules, reviewer-unavailable behavior, failed-check behavior, and how final-quality findings become cleanup slices.

## Final Report

Use `final-report.md` for synthesized results, not raw subagent dumps:

```text
Outcome
Changes
Completion Proof
Remaining Risks
Follow-up
```
