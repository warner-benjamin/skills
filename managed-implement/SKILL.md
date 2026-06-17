---
name: managed-implement
description: Implement a reviewed managed workflow design plan after explicit implementation approval, through self-contained execution slices, delegated or substantial-slice artifacts, optional bounded subagents, targeted checks, fresh per-slice review, focused commits, integration, and initial verification. Use when the user explicitly invokes $managed-implement or asks to execute an existing reviewed workflow plan. Do not use before plan review is complete and implementation approval is approved.
---

# Managed Implement

Execute the implementation phase after implementation approval. Keep implementation bounded by the reviewed `plan.md` and use `checklist.md` as the phase ledger.

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
- `$PHASE_SKILL_DIR/references/goal-mode.md` before activating, skipping, or resuming goal mode
- `$PHASE_SKILL_DIR/references/slice-artifacts.md`

## Preconditions

Before editing, inspect `plan.md`, `checklist.md`, and the working tree. Do not implement until:

- Plan review is `non-blocking`; or it is `unavailable` and `checklist.md` records that the caveat was shown to the user before implementation approval.
- `Implementation approval` is `approved`, with evidence recorded in `checklist.md`.
- The reviewed `Design`, `Implementation Steps`, `Verification / Acceptance`, and `Execution Slices` are clear enough that workers do not need to invent core design decisions.
- Slice boundaries, ownership, verification, and commit policy are clear enough to avoid unrelated changes.

If a precondition is missing, pause implementation, update `checklist.md` with the blocker, and ask for the smallest needed user decision.

When resuming from an existing plan, preserve completed slice commits and reports. Continue from the first ready incomplete slice unless the plan is stale against the codebase; if stale, route back to `managed-plan` for a targeted update and re-review.

## Goal Mode

Use goal mode by fit after implementation approval. In practice, activate it for most non-trivial implementations, and skip it only for genuinely small one-shot work that can finish in the current turn without waiting, recovery, parallel workers, or meaningful restart risk.

Before slice work, read `references/goal-mode.md`. Either activate goal mode using its activation packet and `create_goal` sequence, resume the existing active goal, or record the small-work skip reason in `checklist.md`'s `Decision Log`.

For goal-backed child agents, use one bounded local finish line with its own verifier and stop condition. Do not clone the parent goal; the parent owns scope, integration, conflict resolution, and final completion.

## Slice Loop

For each ready execution slice:

1. Confirm the current working tree state and unrelated changes.
2. Write or update `slices/<slice-id>.md` before delegated or substantial local work, citing the relevant `Design`, `Implementation Steps`, verification, and execution-slice details from `plan.md`. For delegated work, name the exact result path. For tiny manager-owned slices, record the needed context in `checklist.md` instead.
3. Implement only the assigned slice locally, or delegate it to a worker only when ownership is disjoint and useful.
4. Ensure a concise implementation report exists under `results/<slice-id>.md` for every delegated slice and for substantial local slices, following `slice-artifacts.md`. For tiny manager-owned slices, checklist evidence can be enough.
5. Import worker changes into the manager's current branch when needed, inspecting the worker diff and applying only intended changes.
6. Run the slice's targeted checks in the manager workspace.
7. Ask a fresh medium-effort slice reviewer to review the diff, tests, and plan alignment when reviewer agents are available. Give the reviewer the exact review path.
8. Ensure reviewer findings exist under `reviews/<slice-id>-review.md` when a reviewer ran or when findings affect commit readiness, following `slice-artifacts.md`.
9. Fix every valid review issue; record rejected findings with reasons.
10. Re-run targeted checks and ask the same reviewer to re-review if material fixes were made.
11. Manager sanity-checks the diff against the plan, ownership boundary, user constraints, and unrelated working tree changes.
12. Update `checklist.md` with slice status, artifacts or evidence, review status, and targeted check evidence before committing.
13. Commit only the slice's intended changes with a focused message that mentions the slice ID.
14. Record the resulting commit SHA in `checklist.md` after the commit.

Do not include unrelated user or concurrent-agent changes in a slice commit. If unrelated changes share files with the slice, inspect carefully and stage only intended hunks.

## Worker Integration

The manager owns the current branch. The manager imports, stages, verifies, and commits every final change unless the plan explicitly assigns commit authority elsewhere. Never commit a worker diff you have not inspected.

Choose the simplest isolation model that keeps changes attributable and safe, and record the decision in `plan.md` or `checklist.md`. The manager decides per workflow or slice; worktrees are useful but not required when slices are independent enough and the runner model already keeps changes isolated.

- Runner-provided isolated workspace: prefer this when the agent runner already gives each worker a separate workspace or patch stream. Require the worker to report its workspace and changed paths; the manager imports only intended changes.
- Worktree-per-worker: use `git worktree add` on a per-worker branch when parallel coding lanes need local isolation and no runner-provided isolation is available. Record branch, path, import method, and cleanup responsibility.
- Shared-tree with disjoint write scope: acceptable when the manager judges slices independent enough, especially for sequential slices or parallel slices with strictly non-overlapping files and no shared uncommitted state. Do not run parallel coding workers against one shared working tree when their edits can interleave.

Require each worker to report its workspace or branch, changed files, verification evidence, blockers, and remaining risks as described in `slice-artifacts.md`. Before committing, inspect the worker diff, apply only intended changes, update `checklist.md` with the source workspace or branch, and re-run the slice checks in the manager's tree.

## Parallelism

Parallelize only slices with no file, workflow-artifact, or semantic dependency overlap and keep parallelism within the agent limits. Run dependent slices sequentially. When uncertain, choose sequential execution or split discovery from implementation.

Spawn a workgroup only when it materially helps. For small or tightly coupled implementation, use one coding lane and one review lane.

## Failure Handling

A slice is not done until its targeted checks pass and its review is non-blocking. When a slice does not converge, do not loop indefinitely or weaken the bar:

- If a worker stalls past an explicit timeout, returns unmergeable or off-scope work, or reverts others' edits, stop that lane, record it in `checklist.md`, and either retry with a tighter prompt or take the slice local.
- If review stays blocking or checks stay red after about two fix attempts, stop editing. Re-read the plan's `Design`, `Implementation Steps`, and `Execution Slices`: the boundary, approach, or a missing dependency is the likely cause. Re-slice, sequence the missing dependency first, or take the slice local.
- Escalate to the user when a slice cannot pass without weakening tests, exceeding the plan's scope or hard stops, or making a decision the plan does not cover. Surface the concrete blocker and the smallest decision needed.

Never narrow scope, weaken or skip tests, or commit red checks to force a slice closed. Record abandoned or re-sliced work in `checklist.md` with the reason.

## Integration

After slices complete, synthesize accepted results, rejected results, conflicts, decisions, final changes, slice commits, and remaining risks.

Resolve conflicts explicitly. If two slices disagree, inspect the authoritative source before choosing.

Synthesize results directly from `plan.md`, `checklist.md`, slice reports, reviews, commits, and the final diff. Do not paste raw worker output into the final report.

Run initial verification before handing off to `managed-quality`. Update `Implementation status`, `Initial verification`, and `Final quality review` in the Phase Gates block.

## Handoff

When implementation and initial verification are complete, update `final-report.md` with accepted results, rejected results, conflicts, slice commits, verification evidence, and remaining risks. If this was a multi-slice code workflow, route to `managed-quality` before final completion.
