---
name: managed-implement
description: Implement a reviewed managed workflow plan after explicit implementation approval, executing the plan's slices through its execution mode and main agent role with risk-gated review, focused per-slice commits, and initial verification. Use when the user explicitly invokes $managed-implement or asks to execute an existing reviewed workflow plan. Do not use before plan review is complete and implementation approval is approved.
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
- `$PHASE_SKILL_DIR/references/slice-artifacts.md` before writing slice prompts, reports, or reviews

## Preconditions

Before editing, inspect `plan.md`, `checklist.md`, and the working tree. Do not implement until:

- Plan review is `non-blocking`; or it is `unavailable` and `checklist.md` records that the caveat was shown to the user before implementation approval.
- `Implementation approval` is `approved`, with evidence recorded in `checklist.md`.
- The reviewed `Design`, `Implementation Steps`, `Verification / Acceptance`, and `Execution Slices` are clear enough that workers do not need to invent core design decisions.
- Slice boundaries, ownership, verification, commit policy, execution mode, main agent role when relevant, and artifact policy are clear enough to avoid unrelated changes.

If a precondition is missing, pause implementation, update `checklist.md` with the blocker, and ask for the smallest needed user decision.

When resuming from an existing plan, preserve completed slice commits and reports. Continue from the first ready incomplete slice unless the plan is stale against the codebase; if stale, route back to `managed-plan` for a targeted update and re-review.

## Goal Mode

Use goal mode by fit after implementation approval. In practice, activate it for most non-trivial implementations, and skip it only for genuinely small one-shot work that can finish in the current turn without waiting, recovery, parallel workers, or meaningful restart risk.

Before slice work, read `references/goal-mode.md`. Either activate goal mode using its activation packet and `create_goal` sequence, resume the existing active goal, or record the small-work skip reason in `checklist.md`'s `Decision Log`.

For goal-backed child agents, use one bounded local finish line with its own verifier and stop condition. Do not clone the parent goal; the parent owns scope, integration, conflict resolution, and final completion.


## Execution Mode And Main Agent Role

Read the plan's `Execution Slices` and `Orchestration Notes` for the execution mode, main agent role, artifact policy, and slice ownership before slice work.

The default and most common shape is `single-agent local` with `Main agent role: coding`: the main agent implements slices sequentially in the current workspace with lean artifacts. The Slice Loop below is written for that path. `multi-agent delegated` with `Main agent role: manager` means worker lanes own implementation slices while the main agent coordinates, imports, verifies, and commits. `hybrid` means the main agent acts as coding agent for some slices and manager/integrator for others.

If the plan's labels are absent or informal, use the slice ownership and artifact policy already in the reviewed plan instead of blocking on terminology. If ownership, delegation, artifact expectations, or integration authority are genuinely ambiguous, pause and route back to `managed-plan` for a targeted update.

## Slice Loop

For each ready execution slice, the main-agent local path is:

1. Confirm the current working-tree state and any unrelated changes.
2. Implement only the assigned slice locally.
3. Run the slice's targeted checks.
4. Decide the review gate by risk (see "Review Gate"). Fix every valid finding, record rejected findings with reasons, then re-run checks and ask the same reviewer to re-review after material fixes.
5. Sanity-check the diff against the plan, ownership boundary, user constraints, and unrelated working-tree changes.
6. Update `checklist.md` with slice status, evidence, and review status before committing.
7. Commit only the slice's intended changes with a focused message that names the slice ID, then record the commit SHA in `checklist.md`.

Do not include unrelated user or concurrent-agent changes in a slice commit. If unrelated changes share files with the slice, inspect carefully and stage only intended hunks.

Default artifacts for a local slice are the checklist row, diff, commit, and verification evidence. Write `slices/<slice-id>.md`, `results/<slice-id>.md`, or review artifacts only when high-risk review, resume safety, or the plan's artifact policy makes them useful.

### Review Gate

Use reviewer agents for high-risk slices: schema or data migrations, auth or permissions, generated API/client contracts, cross-layer user behavior, concurrency or background jobs, and destructive cleanup. Reuse the same implementation reviewer for adjacent sequential slices when continuity reduces repeated context; use a fresh reviewer when independence matters, the risk boundary changes, a prior reviewer missed a material issue, or the plan/checklist requires it. Main-agent review is acceptable for docs, env examples, tiny CLI or test-only additions, and mechanical follow-up slices after green checks. Record the decision in `checklist.md`. When a reviewer runs, save findings to `reviews/<slice-id>-review.md` per `slice-artifacts.md`.

### Delegated Slices

When a slice is delegated to a worker (mode `multi-agent delegated`, or the delegated half of `hybrid`), add to the loop before the commit:

1. Before delegating, write `slices/<slice-id>.md` citing the relevant `Design`, `Implementation Steps`, verification, and execution-slice details from `plan.md`, and name the exact result path.
2. Require the worker to return `results/<slice-id>.md` per `slice-artifacts.md`; do not accept a vague "done".
3. Import the worker diff into the main agent's current branch, inspecting it and applying only intended changes, then run the slice's targeted checks locally.
4. Record the source workspace or branch in `checklist.md`.

When spawning workers or reviewers, use `agents.md` Agent Level Routing; do not override model/effort for main-agent local coding work. See "Worker Integration" for isolation models.

## Review Budget and Freeze

Default to no more than one fresh implementation reviewer per major subsystem or risk boundary, plus same-thread re-reviews. Exceed that only when the plan sets a higher review bar, the user asks for stricter review, a slice crosses a new high-risk boundary, or the checklist records why independence is worth the added cost.

Before spawning a reviewer, freeze the slice diff: the main agent should believe the code change is complete, workflow artifacts are current, targeted checks have run, and no known local cleanup remains. After a reviewer starts, wait patiently for the reviewer result. Do not keep implementing the slice, perform a parallel main-agent review, draft findings, or re-audit the same diff while the reviewer is active. If a material issue surfaces before the first verdict through an external event or tool result, fix it locally and send one consolidated same-thread update or restart the review; repeated pre-verdict updates are a process failure to record in `checklist.md`.

## Worker Integration

The main agent owns the current branch. The main agent imports, stages, verifies, and commits every final change unless the plan explicitly assigns commit authority elsewhere. Never commit a worker diff you have not inspected.

Choose the simplest isolation model that keeps changes attributable and safe, and record the decision in `plan.md` or `checklist.md`. The main agent decides per workflow or slice; worktrees are useful but not required when slices are independent enough and the runner model already keeps changes isolated.

- Runner-provided isolated workspace: prefer this when the agent runner already gives each worker a separate workspace or patch stream. Require the worker to report its workspace and changed paths; the main agent imports only intended changes.
- Worktree-per-worker: use `git worktree add` on a per-worker branch when parallel coding lanes need local isolation and no runner-provided isolation is available. Record branch, path, import method, and cleanup responsibility.
- Shared-tree with disjoint write scope: acceptable when the main agent judges slices independent enough, especially for sequential slices or parallel slices with strictly non-overlapping files and no shared uncommitted state. Do not run parallel coding workers against one shared working tree when their edits can interleave.

Require each worker to report its workspace or branch, changed files, verification evidence, blockers, and remaining risks as described in `slice-artifacts.md`. Before committing, inspect the worker diff, apply only intended changes, update `checklist.md` with the source workspace or branch, and re-run the slice checks in the main agent's tree.

## Parallelism

Parallelize only slices with no file, workflow-artifact, or semantic dependency overlap and keep parallelism within the agent limits. Run dependent slices sequentially. When uncertain, choose sequential execution or split discovery from implementation.

Spawn a workgroup only when it materially helps. For small or tightly coupled implementation, use one coding lane and one review lane.

## Failure Handling

A slice is not done until its targeted checks pass and its required review is non-blocking, or the recorded main-agent review gate is satisfied. When a slice does not converge, do not loop indefinitely or weaken the bar:

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
