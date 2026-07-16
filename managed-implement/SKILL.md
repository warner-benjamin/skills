---
name: managed-implement
description: Execute a human-approved managed workflow plan with cost-aware Luna-first multi_agent_v1 workers, escalation to Terra or Sol based on complexity and risk, main-agent integration, persistent goal state, and implementation verification. Use when the user explicitly invokes $managed-implement or asks to execute an existing ready managed plan. Do not use until the user has reviewed the plan and explicitly authorized implementation.
---

# Managed implement

Execute the ready plan while keeping the main agent responsible for scope, integration, and completion.

## Setup and preconditions

`PHASE_SKILL_DIR` is the absolute directory containing this file. Resolve `WORKFLOW_SKILL_DIR` from a user provided path or the sibling `managed-workflow` directory.

Read `$WORKFLOW_SKILL_DIR/references/workflow-contract.md` unless it is already loaded for this run. Then read:

- `$WORKFLOW_SKILL_DIR/references/agents.md` before spawning workers or reviewers
- `$WORKFLOW_SKILL_DIR/references/hard-stops.md` before consequential actions
- `$WORKFLOW_SKILL_DIR/references/verification.md` before implementation verification
- `references/goal-mode.md` before activating, skipping, or resuming goal mode

Read `references/slice-artifacts.md` only when a workspace boundary cannot preserve the worker exchange or the user explicitly requests separate audit artifacts.

Before editing, inspect the plan, checklist, working tree, and recorded commits. Require:

- `Plan: ready`
- `Plan review: not-required` or `passed`, or `unavailable` when the checklist records the main-agent fallback and independence was not required
- `Implementation authorization: approved`

Require the checklist to record approval given after the user saw the ready plan. Do not infer approval from the original implementation request or plan feedback.

Return to planning when the plan is stale, the path must become strict, or a worker would need to invent a material design choice.

## Dispatch

Delegate implementation through `multi_agent_v1` when the context transfer is worthwhile. Choose the lane at dispatch under the shared agent routing, and set `model`, `reasoning_effort`, `agent_type`, and `fork_context` explicitly. Use its chart-efficient core ladder for ordinary work and its knowledge overrides only when unfamiliar or cross-domain subject matter justifies a larger model below its maximum reasoning tier.

Immediately before every new worker or reviewer spawn, name the selected model and reasoning level in commentary. Announce any replacement combination before retrying a rejected spawn; recording it in the checklist is not a substitute for telling the user.

Allow the main agent to implement locally when no runner is available, the work is too small to justify transferring context, the work is tightly coupled to active integration, or one focused worker retry failed. Record the reason briefly when a checklist exists.

Before spawning or closing a worker, apply the worker continuity and liveness rules in `agents.md`. Reuse an accepted worker for a directly dependent adjacent item with overlapping files or behavior; use local main-agent integration when that overlap makes a new handoff wasteful.

Set `Implementation: in-progress` before starting the first item. Apply `references/goal-mode.md` before the first edit and continue immediately after activation.

## Work loop

For each work item whose dependencies are ready:

1. Reconcile its checklist status with the current tree. Confirm its ownership boundary, acceptance condition, and dependencies.
2. Mark it `in-progress`. Build the worker prompt from the plan item and the worker contract in `agents.md`. Pass an absolute accessible plan path, or include the complete item contract when an isolated worker cannot read the run directory. Record the dispatched model and effort in the checklist's worker field.
3. Let the worker implement and run targeted checks. Do not babysit it: pause parent work and use the increasing 2-, 5-, then 8-minute waits in `agents.md` without progress commentary, status polling, repository probes, context rereading, or side work. Resume a tool-yielded wait silently. A wait timeout alone is not evidence of a stall.
4. Inspect the changed paths and diff. Import only intended work when the worker used another workspace.
5. Use an independent implementation reviewer only at a boundary with high risk. A strict path alone does not require a reviewer for every item.
6. Rerun checks when import, later integration, or uncertain evidence warrants it.
7. Mark the item `complete` only when its acceptance condition and targeted checks pass. Record concise evidence, commit the accepted item before starting more work, and record the commit. Skip only under the shared commit-policy exceptions.
8. Inspect the next ready item before closing the worker. Reuse, resume, close, or take the next item local under the continuity rules.

For normal managed work, use the spawn prompt and worker's final response as the work packet and report. Record concise worker and reviewer evidence in the checklist. Create separate files only under the exceptions in `references/slice-artifacts.md`.

## Failure handling

After a concrete stall under `agents.md`, incomplete worker output, `not_found`, or work outside the assigned scope, make at most one tighter recovery attempt. Then close the lane and reslice, let the main agent take over, or return to planning. Never use unchanged file timestamps or repeated wait timeouts as the failure signal.

After two focused fixes fail to clear the same check or blocking finding, stop patching and revisit the approach, dependencies, and item boundary. Preserve the failed evidence. Never weaken tests or acceptance criteria to close an item.

Ask the user only when completion requires new authority, broader scope, or a material choice the plan does not cover.

## Integration and handoff

After all required items finish:

1. Inspect the whole integrated diff. Resolve small conflicts against the plan and authoritative code. Return to planning when the code disproves a material plan choice.
2. Run implementation verification from the integration workspace.
3. Set `Implementation: complete`, `Implementation verification: passed`, and `Verification: passed` only when the integrated outcome is proven.
4. Set `Quality: pending` when maintained source, test, or user interface code changed. Set it to `not-required` only when no maintained code changed, changed output was generated from unchanged source, or the user explicitly skips quality cleanup.
5. Follow the shared commit policy. Preserve accepted intermediate commits and make a final commit after quality only for remaining integration or cleanup.

Keep an active goal open across the quality handoff. Return to `managed-quality` when quality is pending. Otherwise return to `managed-workflow` for goal completion, any required commit, and reporting.
