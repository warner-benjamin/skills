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

`plan.md` is the source of truth for goal, constraints, risks, slice details, integration policy, verification strategy, final quality decision, and commit policy.

`checklist.md` is a status ledger only. Do not duplicate the plan there. Track phase gates, reviewer identity, review notes, slice statuses, hard-stop records, commit SHAs, verification evidence, and final-quality details.

`slices/<slice-id>.md` stores the prompt or work packet for a slice before delegation or local implementation. `results/<slice-id>.md` stores the coding, research, or local implementation report. These files are required for every implementation slice. `reviews/<slice-id>-review.md` stores the slice review and is required when a review lane is available.

The `## Phase Gates` block is the only authoritative home for cross-phase status. Detail sections can record reviewers, findings, notes, paths, evidence, and reasons, but must not contain a second status field for the same gate.

## Required Plan Headings

Keep the plan concise enough to guide delegation and verification without replacing execution:

```text
Goal
Baseline
Success Criteria
Primary Verifier
Completion Proof
Current Context
Constraints
Anti-cheating Constraints
Risks
Hard Stops
Workflow Artifact Path
Implementation Slices
Integration Policy
Verification
Final Quality Review
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

- `Plan review: non-blocking`: independent review ran and no blocking findings remain.
- `Plan review: unavailable`: no independent reviewer was available; report this caveat to the user. Do not proceed to implementation unless the user explicitly clears implementation after seeing this caveat.
- `User implementation gate: cleared`: the user explicitly cleared implementation, or explicitly authorized execution after plan review in the original request. If `Plan review` is `unavailable`, this clearance must happen after the unavailable-review caveat is shown.
- `Initial verification: passed`: implementation verification matched the plan's blast radius and passed.
- `Final quality review: not-required`: docs-only, research-only, small one-shot, or explicitly skipped with a reason.
- `Final verification: passed`: verification was re-run after any final cleanup.

If a phase cannot satisfy its precondition, update `checklist.md` with the exact blocker and stop the blocked action.

## Phase Ownership

- `managed-plan` writes the plan, plan review outcome, rejected findings, and user gate state.
- `managed-implement` writes slice statuses, review statuses, commit SHAs, integration results, initial verification, and whether final quality is required.
- `managed-quality` writes the final quality decision, cleanup slice, re-verification evidence, and final verification.
- `managed-workflow` owns cross-phase routing, goal mode, reusable recipes, and final-report synthesis. Phase skills append evidence and phase summaries; the orchestrator owns the final read-through and completion narrative.

## Commit Policy

The manager owns staging and committing on the current branch. Worker agents may edit their assigned workspace when that is the active runner model, but they must not make final commits unless the plan explicitly assigns that authority.

For each implementation slice, commit only that slice's intended code, tests, docs, and workflow artifact updates that exist before the commit. Do not include unrelated user or concurrent-agent changes.

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

## Final Report

Use `final-report.md` for synthesized results, not raw subagent dumps:

```text
Outcome
Accepted Results
Rejected Results
Conflicts Resolved
Slice Commits
Verification Evidence
Final Quality Review
Completion Proof
Remaining Risks
Reusable Follow-up
```
