---
name: ultragoal
description: >-
  Run durable Codex goals from activation through verified completion. Use native goal and plan state, dependency-ordered implementation, bounded delegation, parent-owned integration, verification, fresh subagent review, and completion proof. Use only for explicit $ultragoal requests, persistent goals, or long managed implementations. The request must require goal state and completion evidence.
---
# Ultragoal

Own one durable objective from activation through verified completion. Use native goal and plan state. Do not create a second workflow state machine. Set `SKILL_DIR` to the absolute directory that contains this file. Set `QUALITY_REVIEW_SKILL` to `$SKILL_DIR/../quality-review/SKILL.md`. If review requires the missing sibling file, report an incomplete installation. Do not use a different quality skill.

## Keep implementation proportionate

Treat the plan as a scope limit. Use the smallest implementation that satisfies its work items and project conventions.
Do not add abstractions, compatibility layers, cleanup, refactors, or tests unless the plan or current evidence requires them.
Run targeted checks during implementation. Do not add tests for hypothetical risks or the appearance of rigor.
Preserve the declared final verifier, acceptance criteria, and required risk reviews.
Stop when the outcome and completion conditions are satisfied.

## Write clearly

Use simple, literal language in commentary, plan entries, worker instructions, review requests, and final reports. Use one term for each concept. State the conclusion first. Then give the evidence and consequence. Name each actor, action, target, and condition. Define unfamiliar technical terms. Revise important instructions and reports twice. First, remove ambiguity, filler, slogans, and unnecessary jargon. Then read the text without the conversation context. Remove useless clauses. Restore details that are necessary for correct execution or verification. Plain writing must preserve the contract and show the risk.
## Select the execution entry

- **Activate:** Reconcile the request and governing sources. Validate readiness. Call `create_goal`. Initialize the native plan. Then start the work.
- **Resume:** Reconcile the active goal, native plan, governing sources, repository state, and completion evidence. Then continue the work.

Treat a concrete `$ultragoal` implementation request as Activate. Do not request approval again after the user requests implementation. Pause only for a material unresolved choice or authority outside the request.

Ultragoal is execution-only.

Do not activate it for research, inspection, criticism, discussion, or possible-goal design. For these requests, explain that activation requires an execution-ready objective. Do not change native state.
## Validate activation readiness

Before activation:

1. Read the named repository instructions, governing sources, existing plan, relevant code, tests, and current state.
2. Validate an existing activation packet or plan against the live repository. Preserve valid decisions and evidence. Reject stale assumptions.
3. Identify one observable outcome, meaningful exclusions, the strongest feasible verifier, completion proof, ordered work, risks, and approval gates.
4. Make sure that required environments, credentials, tools, devices, and authenticated surfaces are available.
5. Do not replace an unavailable test on the user surface with a weaker test.
6. State the rules that prevent false success.
7. Do not weaken tests. Do not narrow acceptance. Do not hide failures. Do not replace declared surfaces with mocks. Do not change benchmarks without approval.
8. Keep the objective compact. Name the outcome, governing source, strongest verifier, and completion condition.

If no execution-ready source exists, do only the grounding that these requirements need. If material design choices, incompatible outcomes, or unclear work remain, report the exact readiness gaps. Do not activate. Do not create a goal from vague planning language. Set a token budget only after an explicit user request. If an answer changes the finish line, grants authority, or selects an incompatible outcome, ask a question. Otherwise, make the smallest reversible assumption and continue.
## Use one durable state model

Use these sources in this order:

1. Use the canonical repository documents and task plans that the user named.
2. Use the native active goal for the finish line and completion condition.
3. Use the native plan for ordered work, status, verification, and the next action.

Create additional goal, plan, checklist, worklog, or report files only for requested artifacts or an external handoff. Do not copy an authoritative runbook into new workflow files. Activate only after readiness validation. Then start the first safe plan step immediately. Inspect the active goal before `create_goal`. If it governs the same objective, resume it. Do not create a duplicate. If another unfinished goal prevents activation, report the conflict. Ask the user to cancel, replace, or finish that goal. Do not mark an unrelated goal completed to clear the goal slot.

For a resume or relevant user change, read the active goal and governing sources again. Inspect the tree and relevant commits. Preserve valid completion evidence. Update the native plan. Continue with the next dependency-ready step. Record compatible user changes in the native plan.

The goal API cannot edit an active objective.

If the user changes the finish line, verifier, or completion condition, stop. Ask the user to use a product control to edit, cancel, or replace the goal. Do not use `update_goal` or an unrelated completion to simulate an objective edit.
## Execute dependency-ordered work

For each work item:

1. Define its objective, ownership, dependencies, direction, invariants, exit condition, and targeted checks.
2. Keep only dependency-ready work active. Revalidate existing lane assignments against the repository, models, tools, open agents, and dependencies. If an assignment remains valid, preserve it.
3. If no valid assignment exists, select local work, sequential delegation, or parallel delegation from the work structure.
4. Implement locally for small changes, coupled integration work, or work with high context-transfer cost.
5. Inspect every changed file and the complete change. Inventory staged, unstaged, deleted, renamed, and relevant untracked files.
6. Treat worker output as an untrusted draft. Run the relevant checks from the integration workspace.
7. Accept the item only after its exit condition and checks pass. Tests alone do not prove architecture, privacy, security, or maintainability.
8. If the user or governing instructions require commits, commit at this boundary. Exclude unrelated changes.
9. Update the native plan with concise evidence. Advance only after dependent contracts are stable.

Treat plan waves as groups of dependency-ready work, not durable state. Dispatch eligible lanes in the current wave together. Do only independent parent work during a wave. Integrate returned work before the next dependent wave. Then validate it. If live dependencies differ from the plan, resequence the wave. If evidence invalidates a material design choice, revise the work item in the native plan. Include its objective, dependencies, ownership, invariants, exit condition, and checks. Do not assign a stronger model to repair an unclear work item.
## Coordinate subagents without losing ownership

If bounded subagents materially help, use them. Use no implementation subagents for small or tightly coupled work.

Every Ultragoal requires one fresh read-only subagent for the final aggregate review. This rule also applies to small and parent-only implementations.

Explicit Ultragoal activation authorizes this bounded delegation.

Use sequential agents for dependent or overlapping work. Use parallel agents only for independent work with separate ownership.

If implementation delegation changes the permitted cost or accepted outcome, ask the user. If agent tools are unavailable, do the implementation locally.

The required reviewer is not implementation delegation. A plan or activation packet cannot use a no-subagent rule to remove this requirement.

If the current user request or higher-priority instructions prohibit all subagents, report the conflict. Do not activate the goal. If active, do not complete it.

If reviewer tools are unavailable, stop before completion. Report the capability gap. Do not replace the reviewer with parent review.

If the user, governing source, or activation packet selects suitable available values, use them. Otherwise, inherit model and effort from the parent. Resolve their exact values before dispatch. If the runtime hides them, pass explicit compatible values for accurate reporting. If an override materially helps, use it. Increase Luna effort for depth. Use Terra for breadth. Use Sol for consequential decisions or reviews. Complete the work packet before you select a stronger model. Do not assign competing models to the same task.
### Available agents guide

| Need | Model and effort | Typical use |
| --- | --- | --- |
| Mechanical execution | `gpt-5.6-luna`, `low` | Exact lookup, running a specified command, applying obvious edits, or checking an explicit condition |
| Cheap bounded scout | `gpt-5.6-luna`, `medium` | Disposable mapping or mechanical research with inexpensive failure |
| Default bounded worker | `gpt-5.6-luna`, `high` | Feature scopes, tests, and clear fixes |
| Difficult bounded reasoning | `gpt-5.6-luna`, `xhigh` | Coupled reasoning or diagnosis with sufficient local knowledge |
| Knowledge breadth | `gpt-5.6-terra`, `high` | Unfamiliar frameworks, protocols, languages, or cross-layer synthesis |
| Difficult broad synthesis | `gpt-5.6-terra`, `xhigh` | Quality-first cross-layer work that requires maximum breadth and reasoning |
| Frontier knowledge | `gpt-5.6-sol`, `high` | Obscure cross-domain knowledge outside the normal breadth lane |
| High-consequence decision | `gpt-5.6-sol`, `xhigh` | Security, permissions, destructive data work, or consequential concurrency |
| Critical decision | `gpt-5.6-sol`, `max` | Critical assurance or unresolved high-risk reasoning. You should rarely need `max` reasoning. |
Improve an unclear task packet before you select a stronger model. Do not run serial model tournaments.

Give each worker one fixed objective, governing context, ownership boundary, invariants, non-goals, exit condition, checks, and stop condition. If a packet has multiple independent outcomes, reject it as too broad. If partial completion can produce a useful result, reject the packet as too broad. Split packets by behavioral invariant, not by technology layer or plan section. Do not repurpose an agent across incompatible roles, ownership boundaries, or independent outcomes.

Require workers to preserve unrelated work. Require them to make no commits. Require reports of behavior, changed paths, checks, deviations, and concrete risks. Allow messages only for blockers, stable dependency handoffs, material scope changes, and completion. Prohibit routine heartbeats.

Call `functions.collaboration.spawn_agent` directly. Pass a unique `task_name`, the packet as `message`, and `fork_turns: "none"`. If the packet cannot safely contain required history, use `fork_turns: "all"` or a positive integer.

A full-history fork inherits model and effort.

Use another fork mode for a model or effort override. Never call collaboration tools through `functions.exec`. Use isolated workspaces or disjoint write sets for parallel coding.

The parent owns scope, integration, architecture, verification, and completion.

Treat every agent result as an untrusted draft. After each successful root spawn, immediately report the task name, objective, exact model, and effort in commentary. Report each agent separately.

Only Sol and Terra workers can delegate bounded child tasks.

Before delegation, load this skill. Apply its ownership, task-packet, wait, verification, reuse, and dispatch-notice rules as the parent of the child. Keep nested delegation inside the active goal and worker scope. Preserve authority, write boundaries, invariants, and concurrency limits. Do not expand the task. Do not overlap other work.

After a nested spawn, send the direct parent a dispatch notice immediately. Include lineage, objective, exact model, and effort. Each non-root parent must forward the notice immediately. The root must report the nested dispatch in commentary. Include this relay rule in every packet that permits nested delegation.

Dispatch notices are material events, not heartbeats.

Keep shared work, generated artifacts, contract regeneration, merge fixes, and small integrated changes with the parent. If transfer and review cost more than local implementation, do not delegate a small known fix.

After dispatch, do only dependency-ready parent work outside all agent ownership. Do not depend on agent work. Do not interfere with agent work. Do not inspect delegated work. Do not do delegated work again. Do not preempt it.

If no independent work remains, call `functions.collaboration.wait_agent` directly. Use no targets and normally wait at least 900,000 milliseconds.

The wait returns early for mailbox activity.

During a pending wait, do not request progress. Do not start another wait. Do not add commentary. Do not inspect work. Do not read context again. Do not start other work.

Treat each update as an event. Answer blockers. Forward one stable dependency contract. Reconcile material scope changes. If integration cannot affect active agent files or dependencies, integrate the completed lane immediately. Otherwise, defer only that integration boundary.

Call `functions.collaboration.list_agents` only for reuse discovery, ambiguous updates, timeouts, or final completion decisions. If required agents remain active and no independent work exists, wait again.
### Manage agent lifecycle and reuse

If existing agents can do the work, call `functions.collaboration.list_agents` once before a spawn. Reuse an agent only for a compatible role, objective, ownership boundary, context, and artifact set. Reuse the implementer for related corrections and checks. Reuse the reviewer for related review or remediation confirmation. Do not create overlapping agents for substantially identical work.

An agent `completed` status ends only its current prompt. Parent acceptance or ownership release requires inspection and verification. Idle agents release execution capacity and remain available by task name.

Keep ownership through review, correction, and final acceptance. Use `functions.collaboration.send_message` for blockers or stable contracts during active work. Use `functions.collaboration.followup_task` for completed-prompt corrections, new actions, or checks. Send urgent safe instructions during active work only.

If work becomes unsafe, invalid, or materially out of scope, call `functions.collaboration.interrupt_agent`. Reconcile partial work before reassignment.

If an agent errors or stops, reconcile its report. Reconcile its changes. Update the plan. Release its ownership explicitly. If its contract remains stable, reuse the agent. Otherwise, assign the remaining work to a compatible owner.

Reuse has no numeric prompt or correction limit.

Group related findings. Keep each follow-up within the stable contract. Require measurable progress after each correction.

Evidence includes fewer failed checks, fewer failed cases, a smaller gap, or a stronger diagnosis.

If the same fault recurs without progress, re-plan. Also re-plan after oscillating fixes or moved faults.
## Re-plan unstable work

Stop incremental correction and re-plan for these conditions:

- A correction repeats a verifier failure without fewer cases or a narrower diagnosis.
- Fixes oscillate or move the fault without reducing the behavioral gap.
- New work causes an accepted item to fail its broad verifier.
- Aggregate review finds blocking causes that invalidate the contract or ownership.
- Successive small fixes repeatedly invalidate review approval.

Collect all known findings before implementation resumes. Replace symptom fixes with work items that correct the cause. Define new ownership and exit conditions. Update the native plan before dispatch. If the revised plan changes the finish line, authority, or accepted outcome, ask the user. At each accepted boundary, reconcile agents, ownership, review rounds, broad verifiers, and advisory findings. Record required replanning before continuation.
## Control verification cost

Run targeted checks during implementation. Run a broad repository gate only after the intended state stops changing and no known fixes remain. Before a broad gate, make sure that no goal verifier still runs. If a tool returns a process session, continue that session. After a broad failure, reproduce it narrowly. Diagnose it. Then run the broad gate again. If acceptance checks or risk require the broad suite at a slice boundary, run it. Always run the declared strongest final verifier on the final frozen state.
## Review at the right boundaries

Require focused review before material authorization, privacy, destructive data, migration, concurrency, or external-effect risks.

The parent can do a preliminary review. Parent review does not satisfy a required risk review or the final aggregate review.

Use a fresh read-only subagent at each required review boundary. One reviewer can cover all required scopes at the same frozen boundary.

Use one fresh read-only subagent for the final aggregate review. Dispatch this reviewer after the aggregate implementation stops changing.

Before this review, the reviewer must not have planned, implemented, integrated, or reviewed the goal. Do not reuse a prior agent.

The reviewer must examine the complete frozen change. This rule is mandatory when the parent implemented some or all of the plan.

Before review, define the scope, source and dependency versions, unresolved choices, governing documents, and intended change inventory.

Do not review an artifact that still changes. Freeze the change before aggregate review.

Inventory staged, unstaged, deleted, renamed, and relevant untracked files. Pass this inventory to the reviewer. A branch diff is insufficient.

If maintained code, tests, user-interface code, or agent instructions changed, read `QUALITY_REVIEW_SKILL` completely. Announce the reason for this review.

Include the absolute `QUALITY_REVIEW_SKILL` path in the reviewer prompt. Require the reviewer to apply that skill directly.

Add each required risk-specific scope to the reviewer packet. Quality review does not replace security, privacy, migration, concurrency, or external-effect review.

Ask the reviewer to challenge new abstractions, persisted discriminators, and compatibility layers. Compare challenged designs with existing library features and the smallest sufficient design.

Collect all review findings before editing. Classify them. Resolve all blockers together. Inspect the change. Run affected checks again.

Any change to the reviewed inventory invalidates approval. Freeze the corrected aggregate. Request a complete rereview from the same reviewer.

Use `functions.collaboration.followup_task` for this rereview. Require the reviewer to examine the complete final inventory, not only the corrections.

If the rereview finds new blocking causes, re-plan the unstable work. Treat `P0` and `P1` findings as blockers.

Keep `P2` findings as advisory risk. Fix them only for user requests, acceptance requirements, or blocking-fix side effects.

The same reviewer remains independent for this rereview. If that reviewer is unavailable, dispatch a new fresh reviewer for the complete frozen change.

Do not mark the goal completed without approval from the required reviewer.
## Complete honestly

Completion requires all these conditions:

- The observable outcome exists.
- All required work, commits, and artifacts are completed.
- All `P0`, correctness, safety, and completion blockers are resolved.
- All blocking risk findings and all `P1` findings are resolved.
- Verification passes on the final state after the last maintained change.
- A fresh read-only subagent reviewed the complete frozen change.
- The reviewer had no earlier planning, implementation, integration, or review role in the goal.
- The reviewer approved the complete final state after the last change to the reviewed inventory.
- The completion proof is available.
- No required work remains.

When all completion conditions are true, mark the goal completed. Report the outcome, strongest evidence, important review changes, unresolved advisory findings, and remaining concrete risk. Mark the goal blocked only after the same external condition prevents meaningful progress for three consecutive goal turns. The condition must meet the blocker standard of the active goal. No active or ambiguous agent can have useful remaining work. Immediately before `update_goal`, reconcile the current goal status, latest agent notices, and active or ambiguous worker ownership. Then reconcile the authoritative worktree and external state. While an unreconciled worker can help, do not mark blocked. Do not overwrite a user-controlled paused or cancelled state.
