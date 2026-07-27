---
name: ultragoal
description: Design, critique, activate, and run durable Codex goals through grounded planning, dependency-ordered implementation, bounded delegation, manager-owned integration, verification, review, and completion proof. Use only when the user explicitly invokes $ultragoal, asks to set or run a persistent goal, or requests a long-running managed implementation with goal state and verifiable completion.
---

# Ultragoal

Own one durable objective from grounding through verified completion. Use native goal and plan state; do not build a second workflow state machine.

Set `SKILL_DIR` to the absolute directory containing this file. Resolve `QUALITY_REVIEW_SKILL` directly as `$SKILL_DIR/../quality-review/SKILL.md`. Do not search the skills tree for it. If that sibling file is missing, report an incomplete installation instead of substituting another quality skill.

## Choose the mode

- **Design:** Ground and critique a proposed goal. Do not call `create_goal` or implement.
- **Activate:** Ground the goal, define its verifier and plan, call `create_goal`, then continue the work.
- **Resume:** Reconcile the active goal, current plan, governing documents, repository state, and completed evidence before continuing.

Treat an explicit request to use `$ultragoal` and complete, build, implement, or pursue a concrete objective as Activate. Questions, investigations, suspected gaps, and requests to research, inspect, draft, critique, or discuss remain Design unless the user explicitly asks to start implementation. Never infer activation merely because the investigation could lead to code changes.

In Design mode, do not update the native plan or write durable artifacts unless the user explicitly requests them. In Activate mode, do not force a second approval turn when the user already asked for implementation; pause only for a material unresolved choice or authority outside the request.

Return an execution-ready Design result: the outcome, constraints, non-goals, strongest verifier, completion proof, chosen approach, dependency-ordered work, important invariants, acceptance checks, material risks, and exact objective. Do not activate or mutate native state.

Never create a goal from vague planning language or set a token budget unless the user explicitly requests one.

## Ground the goal

Before activation:

1. Read the named repository instructions, governing documents, existing plan or runbook, relevant code, tests, and current state.
2. Separate user requirements, observed facts, and reversible assumptions.
3. Define one observable outcome, meaningful exclusions, and the strongest feasible verifier closest to the user's real experience.
4. Define supporting regression, safety, quality, and durability checks proportional to risk.
5. Confirm that required environments, credentials, tools, devices, or authenticated surfaces are available. Do not silently replace an unavailable real-surface verifier with a weaker proxy.
6. State anti-cheating rules: do not weaken tests, narrow acceptance, hide failures, substitute mocks for the declared surface, or change the benchmark without approval.
7. Identify approval gates for public, shared, destructive, irreversible, costly, or otherwise consequential actions.
8. Define completion proof and the true blocker standard. Difficulty, uncertainty, or a long test is not a blocker.

Ask only when a missing answer changes the finish line, grants new authority, or chooses between incompatible outcomes. Otherwise make the smallest reversible assumption and continue.

## Use one durable state model

Prefer, in order:

1. Canonical repository design documents, delivery runbooks, and task plans already named by the user.
2. The native active goal for the finish line and completion condition.
3. The native plan for ordered work, current status, verification, and the next action.

Create additional goal, plan, checklist, worklog, or report files only when the user requests durable artifacts or an external handoff cannot use the repository documents and native state. Never duplicate an existing authoritative runbook into generated workflow files.

Activate only after grounding. Keep the objective compact: name the outcome, governing source, strongest verifier, and completion condition. After activation, continue immediately with the first safe plan step.

Inspect the active goal before creating one. Resume it when it governs the same objective; never create a duplicate. If a different unfinished goal prevents activation, report the conflict and ask the user to cancel, replace, or finish it. Do not falsely complete an unrelated goal to clear the slot.

On resume or after material steering, reread the active goal and governing sources, inspect the actual tree and relevant commits, preserve valid completed evidence, update the plan, and continue from the next dependency-ready step. Keep compatible steering in the native plan. The goal API cannot edit an active objective: when steering materially changes the finish line, verifier, or completion condition, ask the user to edit, cancel, or replace the goal through an available product control before continuing. Never misuse `update_goal` or mark an unrelated goal complete to simulate an edit.

## Execute dependency-ordered work

For each work item:

1. Confirm its objective, ownership boundary, dependencies, chosen direction, invariants, observable exit condition, and targeted checks.
2. Keep only dependency-ready work active. Choose no subagents, sequential delegation, or parallel delegation from the work structure.
3. Implement locally when the change is small, tightly coupled to active integration, or cheaper than transferring context.
4. Inspect every changed file and the complete change before acceptance. Inventory staged, unstaged, deleted, renamed, and relevant untracked files instead of assuming one diff command is complete. Treat worker output as an untrusted draft.
5. Run the relevant checks from the integration workspace. Passing tests are necessary but do not prove architecture, privacy, security, or maintainability.
6. Accept the item only when its behavioral exit condition and checks pass. Commit at that boundary only when the user or governing instructions request commits, and never include unrelated changes.
7. Update the native plan with concise evidence and advance only after dependent contracts are stable.

Return to planning when implementation evidence invalidates a material design choice. Do not buy a stronger worker to compensate for an underspecified work item.

## Coordinate subagents without losing ownership

Explicit Ultragoal activation authorizes bounded subagents when they materially help. Use no subagents for small or tightly coupled work, sequential agents for dependent or overlapping slices, and parallel agents only for independent lanes with disjoint ownership. Poll the user only when topology changes explicit cost authority, required review independence, or the accepted outcome. If agent tools are unavailable, work locally unless the user explicitly requires delegation or independence.

Use a user-selected or runbook-selected model and effort. Otherwise prefer the inherited lane and use this table only when an override materially helps. Increase Luna effort for reasoning depth, use Terra for missing knowledge breadth, and use Sol for consequential decisions or reviews. Improve an underspecified work packet before buying a stronger lane; do not run a serial model tournament.

### Available agents guide

| Need | Model and effort | Typical use |
| --- | --- | --- |
| Cheap bounded scout | `gpt-5.6-luna`, `medium` | Disposable mapping or mechanical research with cheap failure |
| Default bounded worker | `gpt-5.6-luna`, `high` | Execution-ready feature slices, tests, and clear fixes |
| Difficult bounded reasoning | `gpt-5.6-luna`, `xhigh` or `max` | Coupled reasoning or diagnosis where local knowledge is sufficient |
| Knowledge breadth | `gpt-5.6-terra`, `high` or `xhigh` | Unfamiliar framework, protocol, language, or cross-layer synthesis |
| Difficult broad synthesis | `gpt-5.6-terra`, `max` | Quality-first cross-layer work requiring breadth and maximum reasoning |
| Frontier knowledge | `gpt-5.6-sol`, `high` | Obscure cross-domain priors beyond the normal breadth lane |
| High-consequence decision or review | `gpt-5.6-sol`, `xhigh` | Security, permissions, destructive data work, or consequential concurrency |
| Critical decision or review | `gpt-5.6-sol`, `max` | Explicit critical assurance or unresolved high-risk reasoning |

Give each worker one immutable objective, governing context, ownership boundary, invariants, non-goals, behavioral exit condition, checks, and stop condition. Reject a packet as too broad when it contains multiple independently testable outcomes or could return useful partial completion; split it by behavioral invariant rather than merely by frontend, backend, or plan slice. Do not repurpose an agent thread for another objective or slice.

Require workers to preserve unrelated work, avoid commits, and report behavior, changed paths, checks, deviations, and concrete risks. Default to `fork_context: false` with a self-contained packet and exact governing-document paths; fork context only when the bounded task genuinely requires conversation history that the packet cannot safely capture. Use isolated workspaces or disjoint write sets for parallel coding. Keep ownership of scope, integration, architecture, verification, and completion in the parent; treat every result as an untrusted draft.

Keep cross-worker seams, generated artifacts, contract regeneration, merge fixes, and localized changes in already-integrated code with the parent. Do not delegate a small known fix when transferring context and reviewing the result is likely to cost more than implementing it locally.

Immediately after dispatch, start one long wait with this exact Code Mode call:

```js
// @exec: {"yield_time_ms": 1500000, "max_output_tokens": 30000}
const result = await tools.multi_agent_v1__wait_agent({
  targets: activeAgentIds,
  timeout_ms: 1500000,
});
for (const [id, status] of Object.entries(result.status ?? {})) {
  text(`${id}: ${JSON.stringify(status)}`);
}
text(`timed_out:${result.timed_out}`);
```

The matching outer yield and agent timeout keep this single call open for up to 25 minutes and return immediately when any target finishes. Do not call `functions.wait`, start another `wait_agent`, add commentary, inspect the repository, reread context, or do side work while it is pending. After `timed_out:true`, run the same call again with the remaining active IDs. For parallel lanes, collect completed results and immediately run the same call for the remaining active IDs; do not integrate until every coding lane has returned `completed` or `errored`.

Keep an implementer open through parent inspection, one focused correction pass, verification, required review, and acceptance. An implementer thread may receive at most two task prompts: its initial packet and one consolidated correction packet. A reviewer thread may receive its initial review and one focused confirmation. Before every `send_input`, count the task prompts already sent to that thread; never send a third task prompt. Do not resume a closed agent or create a reviewer chain.

When material work remains after the correction pass, end that worker's ownership and return the item to planning. Identify the root cause, then implement a bounded integration fix locally or dispatch one fresh, smaller packet with new ownership. Do not continue implementer-reviewer ping-pong.

## Re-plan unstable work

Stop incremental correction and re-plan the affected work when:

- an implementer exhausts its correction pass;
- two agents miss the same acceptance condition;
- a supposedly accepted item fails its broad verifier because of the new work;
- an aggregate review finds three or more unrelated blocking root causes;
- successive small fixes repeatedly invalidate review approval.

Batch every known finding before resuming implementation. Replace symptom-sized fixes with root-cause work items, define fresh ownership and exit conditions, and update the native plan before dispatching again. Do not ask the user unless re-planning changes the finish line, authority, or accepted outcome.

At each accepted boundary, reconcile active agents, prompts used per agent, review rounds, broad verifier runs, and known advisory findings. If any circuit breaker has fired, record the re-scoped approach in the native plan before continuing.

## Control verification cost

Run targeted checks while implementation is moving. Run a broad repository gate only when no known fixes remain and the intended item or aggregate state is frozen. Before starting it, confirm that no broad verifier from the goal is still running; if a tool call yields a process session, continue that same session instead of starting an overlapping run.

After a broad failure, reproduce and diagnose it narrowly before running the broad gate again. At ordinary slice boundaries, run the broad suite only when the governing acceptance checks or risk justify it. Always run the declared strongest final verifier on the final frozen state.

## Review at the right boundaries

Require focused review to pass before crossing a risk-bearing boundary such as authorization, privacy, destructive data changes, migrations, concurrency, or external effects. The parent may perform it unless the user or governing instructions require independence; if required independence is unavailable, stop before the boundary and report the capability gap.

Before declaring a design or implementation artifact frozen or dispatching its reviewer, confirm the exact scope, source and dependency versions, unresolved user choices, governing documents, and intended change inventory. Continue grounding instead of reviewing a knowingly moving target. Ask the reviewer to challenge every new abstraction, persisted discriminator, and compatibility layer against existing library primitives and the smallest sufficient design.

When maintained implementation code, tests, user-interface code, or agent instructions changed, read `QUALITY_REVIEW_SKILL` completely and follow it before final completion. Announce why it is being used. By default, run the strict quality review once on the frozen aggregate implementation rather than after every ordinary slice. Use earlier quality review only when the user or governing sources require it, or when a consequential slice is too large to defer safely. Quality review complements rather than replaces risk-specific review.

For integrated multi-worker or consequential changes, prefer one fresh read-only aggregate reviewer when subagents are authorized and include the resolved absolute `QUALITY_REVIEW_SKILL` path in its prompt; otherwise apply the skill directly.

Before aggregate review, freeze the intended change and pass an explicit inventory covering staged, unstaged, deleted, renamed, and relevant untracked files. A branch diff alone is not proof of complete scope.

Collect and classify the complete review result before editing. Resolve accepted blocking findings in one consolidated remediation batch, inspect the resulting diff again, rerun affected checks, and request one focused confirmation. Do not request review after each small repair. If confirmation finds new blocking root causes, trigger the unstable-work circuit breaker instead of dispatching symptom-sized corrections.

Treat `P0` and `P1` findings as blocking. Preserve `P2` findings as advisory residual risk and do not fix them during the active goal unless the user requested them, an explicit acceptance check requires them, or the repair is incidental to a blocking fix.

Any material change to a reviewed artifact invalidates its prior approval. Reuse the open reviewer for focused confirmation or, if it was closed or independence requires it, use one fresh reviewer before activation or completion.

## Complete honestly

Mark the goal complete only when:

- the observable outcome exists;
- every required work item and requested commit or artifact is complete;
- every blocking risk-specific or quality finding is resolved or explicitly accepted by the user;
- verification passes on the final state after the last maintained change;
- the declared completion proof is available;
- no required work remains.

Report the outcome, strongest evidence, important review-driven changes, unresolved advisory findings, and remaining concrete risk. Mark the goal blocked only under the platform blocker rule when a true external condition prevents meaningful progress.

Immediately before any `update_goal` completion or blocked transition, reconcile the current goal status, latest agent notifications, active or ambiguous worker ownership, authoritative worktree, and external state. Never mark blocked while an unreconciled worker may still return meaningful progress, and never overwrite a user-controlled paused or cancelled state.
