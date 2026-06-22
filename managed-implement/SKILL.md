---
name: managed-implement
description: Implement a reviewed managed workflow plan after explicit implementation approval, executing the plan's slices through its execution mode and main agent role with risk-gated review, focused per-slice commits, and initial verification. Use when the user explicitly invokes $managed-implement or asks to execute an existing reviewed workflow plan. Do not use before plan review is complete and implementation approval is approved.
---

# Managed Implement

Execute the implementation phase after implementation approval. Keep implementation bounded by the reviewed `plan.md` and use `checklist.md` as the phase ledger.

## Shared Setup

`PHASE_SKILL_DIR` is the absolute directory of this `SKILL.md`. Resolve `WORKFLOW_SKILL_DIR` before reading shared references or running scripts: a user-provided `managed-workflow` path if given, else the sibling `managed-workflow` directory next to `PHASE_SKILL_DIR`. Always use an absolute path, never `../managed-workflow/...` relative to the shell cwd.

Read:

- `$WORKFLOW_SKILL_DIR/references/workflow-contract.md`
- `$WORKFLOW_SKILL_DIR/references/agents.md` before spawning workers or reviewers
- `$WORKFLOW_SKILL_DIR/references/hard-stops.md` before risky or ambiguous operations
- `$WORKFLOW_SKILL_DIR/references/verification.md` before initial verification
- `$PHASE_SKILL_DIR/references/goal-mode.md` before activating, skipping, or resuming goal mode
- `$PHASE_SKILL_DIR/references/slice-artifacts.md` before writing slice prompts, reports, or reviews
- `$PHASE_SKILL_DIR/references/delegated-work.md` before delegating slices or running parallel/worker lanes

## Preconditions

Before editing, inspect `plan.md`, `checklist.md`, and the working tree. Do not implement until:

- Plan review is `non-blocking`; or it is `unavailable` and `checklist.md` records that the caveat was shown to the user before implementation approval.
- `Implementation approval` is `approved`, with evidence recorded in `checklist.md`.
- The reviewed `Design`, `Implementation Steps`, `Verification / Acceptance`, and `Execution Slices` are clear enough that workers don't invent core design decisions.
- Slice boundaries, ownership, verification, commit policy, execution mode/role, and artifact policy are clear enough to avoid unrelated changes.

If a precondition is missing, pause, record the blocker in `checklist.md`, and ask for the smallest needed user decision.

When resuming from an existing plan, preserve completed slice commits and reports. Continue from the first ready incomplete slice unless the plan is stale against the codebase; if stale, route back to `managed-plan` for a targeted update and re-review.

## Goal Mode

Use goal mode by fit after implementation approval: activate it for most non-trivial implementations, skip it only for genuinely small one-shot work that finishes this turn without waiting, recovery, parallel workers, or restart risk.

Before slice work, read `references/goal-mode.md`, then activate goal mode (its activation packet and `create_goal` sequence), resume the existing goal, or record the skip reason in `checklist.md`'s `Decision Log`.

For goal-backed child agents, give each one bounded local finish line with its own verifier and stop condition. Don't clone the parent goal — the parent owns scope, integration, conflict resolution, and completion.

## Execution Mode And Main Agent Role

Before slice work, read the plan's `Execution Slices` and `Orchestration Notes` for the execution mode, main agent role, artifact policy, and slice ownership (mode/role definitions live in `workflow-contract.md`).

The default shape is `single-agent local` / `coding`: the main agent implements slices sequentially in the current workspace with lean artifacts, and the Slice Loop below is written for it. `multi-agent delegated` / `manager` means worker lanes own slices while the main agent coordinates, imports, verifies, and commits; `hybrid` mixes both.

If the plan's labels are absent or informal, follow the slice ownership and artifact policy already in the reviewed plan rather than blocking on terminology. If ownership, delegation, artifact expectations, or integration authority are genuinely ambiguous, pause and route back to `managed-plan`.

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

When spawning workers or reviewers, use `agents.md` Agent Level Routing; do not override model/effort for main-agent local coding work. See `references/delegated-work.md` for worker integration, isolation models, and parallel lanes.

## Review Budget and Freeze

Default: at most one fresh implementation reviewer per major subsystem or risk boundary, plus same-thread re-reviews. Exceed that only when the plan sets a higher bar, the user asks for stricter review, a slice crosses a new high-risk boundary, or the checklist records why independence is worth the cost.

Before spawning a reviewer, freeze the slice: change complete, artifacts current, checks run, no known cleanup left. Then wait — don't keep editing, self-review, or re-audit the diff while the reviewer runs. If a material issue surfaces before the first verdict, fix it and send one consolidated same-thread update or restart the review; repeated pre-verdict updates are a process failure (record in `checklist.md`).

## Failure Handling

A slice is done only when its targeted checks pass and its required review is non-blocking (or the recorded main-agent review gate is satisfied). When a slice doesn't converge, don't loop or weaken the bar:

- If review stays blocking or checks stay red after ~2 fix attempts: stop editing and re-read the plan's `Design`, `Implementation Steps`, and `Execution Slices` — the boundary, approach, or a missing dependency is the likely cause. Re-slice, sequence the dependency first, or take the slice local.
- Escalate to the user when a slice can't pass without weakening tests, exceeding scope/hard stops, or making a decision the plan doesn't cover. Surface the concrete blocker and smallest decision needed.

Never narrow scope, weaken or skip tests, or commit red checks to force a slice closed. Record abandoned or re-sliced work in `checklist.md` with the reason. For worker-lane stalls, see `references/delegated-work.md`.

## Integration

After slices complete, synthesize accepted/rejected results, conflicts, decisions, final changes, slice commits, and remaining risks directly from `plan.md`, `checklist.md`, slice reports, reviews, commits, and the final diff — don't paste raw worker output.

Resolve conflicts explicitly: if two slices disagree, inspect the authoritative source before choosing.

Run initial verification before handing off to `managed-quality`. Update `Implementation status`, `Initial verification`, and `Final quality review` in Phase Gates.

## Handoff

When implementation and initial verification are complete, update `final-report.md` with accepted/rejected results, conflicts, slice commits, verification evidence, and remaining risks. For a multi-slice code workflow, route to `managed-quality` before final completion.
