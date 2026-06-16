---
name: managed-implement
description: Implement an approved managed workflow plan through self-contained slices, per-slice prompts, worker or local reports, optional bounded subagents, targeted checks, fresh per-slice review, focused commits, integration, and initial verification. Use when the user explicitly invokes $managed-implement or asks to execute an existing reviewed workflow plan. Do not use before plan review and the user implementation gate are clear.
---

# Managed Implement

Execute the approved implementation phase for a managed workflow. Keep implementation bounded by the reviewed `plan.md` and use `checklist.md` as the phase ledger.

## Shared Setup

Let `PHASE_SKILL_DIR` mean the absolute directory containing this `SKILL.md`. Resolve `WORKFLOW_SKILL_DIR` before reading shared references or running shared scripts:

1. Use a user-provided `managed-workflow` path when given.
2. Otherwise use the sibling `managed-workflow` directory next to `PHASE_SKILL_DIR`.
3. Use an absolute path. Do not run `../managed-workflow/...` relative to the user's shell cwd.

Read:

- `$WORKFLOW_SKILL_DIR/references/workflow-contract.md`
- `$WORKFLOW_SKILL_DIR/references/agents.md` before spawning workers or reviewers
- `$WORKFLOW_SKILL_DIR/references/hard-stops.md` before risky or ambiguous operations
- `$WORKFLOW_SKILL_DIR/references/verification.md` before initial verification
- `$PHASE_SKILL_DIR/references/slice-template.md`
- `$PHASE_SKILL_DIR/references/slice-report.md`
- `$PHASE_SKILL_DIR/references/slice-review.md`

## Preconditions

Before editing, inspect `plan.md`, `checklist.md`, and the working tree. Do not implement until:

- Plan review is `non-blocking`; or it is `unavailable` and `checklist.md` records that the caveat was shown to the user and the user explicitly cleared execution after seeing it.
- `User implementation gate` is `cleared`, or the user has explicitly authorized implementation after review.
- Slice boundaries, ownership, verification, and commit policy are clear enough to avoid unrelated changes.

If a precondition is missing, pause implementation, update `checklist.md` with the blocker, and ask for the smallest needed user decision.

## Slice Loop

For each ready implementation slice:

1. Confirm the current working tree state and unrelated changes.
2. Write or update `slices/<slice-id>.md` before local work or delegation.
3. Implement only the assigned slice locally, or delegate it to a worker only when ownership is disjoint and useful.
4. Save a concise implementation report under `results/<slice-id>.md`; if a worker ran, use the worker's final report and changed-path list.
5. Import worker changes into the manager's current branch when needed, inspecting the worker diff and applying only intended changes.
6. Run the slice's targeted checks in the manager workspace.
7. Ask a fresh medium-effort slice reviewer to review the diff, tests, and plan alignment when reviewer agents are available.
8. Save the review under `reviews/<slice-id>-review.md`.
9. Fix every valid review issue; record rejected findings with reasons.
10. Re-run targeted checks and ask the same reviewer to re-review if material fixes were made.
11. Manager sanity-checks the diff against the plan, ownership boundary, user constraints, and unrelated working tree changes.
12. Update `checklist.md` with slice status, prompt path, report path, review status, and targeted check evidence before committing.
13. Commit only the slice's intended changes with a focused message that mentions the slice ID.
14. Record the resulting commit SHA in `checklist.md` after the commit.

Do not include unrelated user or concurrent-agent changes in a slice commit. If unrelated changes share files with the slice, inspect carefully and stage only intended hunks.

## Worker Integration

The manager owns the current branch. Worker agents may edit only their assigned workspace or write scope, but the manager imports, stages, verifies, and commits final changes unless the plan explicitly says otherwise.

Require each worker to report changed files, verification evidence, blockers, and remaining risks in the shape from `slice-report.md`. Before committing, inspect the worker diff, apply only intended changes to the manager workspace, update `checklist.md` with the source workspace or branch, and run the slice checks locally.

## Parallelism

Parallelize only slices with no file, workflow-artifact, or semantic dependency overlap and keep parallelism within the agent limits. Run dependent slices sequentially. When uncertain, choose sequential execution or split discovery from implementation.

Spawn a workgroup only when it materially helps. For small or tightly coupled implementation, use one coding lane and one review lane.

## Integration

After slices complete, synthesize accepted results, rejected results, conflicts, decisions, final changes, slice commits, and remaining risks.

Resolve conflicts explicitly. If two slices disagree, inspect the authoritative source before choosing.

Use `collect_results.py` when result files exist:

```bash
python3 "$WORKFLOW_SKILL_DIR/scripts/collect_results.py" workflows/<slug>
```

Run initial verification before handing off to `managed-quality`. Update `Implementation status`, `Initial verification`, and `Final quality review` in the Phase Gates block.

## Handoff

When implementation and initial verification are complete, update `final-report.md` with accepted results, rejected results, conflicts, slice commits, verification evidence, and remaining risks. If this was a multi-slice code workflow, route to `managed-quality` before final completion.
