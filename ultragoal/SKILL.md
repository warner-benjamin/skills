---
name: ultragoal
description: Activate, resume, and run durable Codex goals through readiness validation, native goal and plan state, dependency-ordered implementation, bounded delegation, manager-owned integration, verification, review, and completion proof. Use only when the user explicitly invokes $ultragoal, asks to start or continue a persistent goal, or requests a long-running managed implementation with goal state and verifiable completion.
---

# Ultragoal

Own one durable objective from activation through verified completion. Use native goal and plan state; do not build a second workflow state machine.

Set `SKILL_DIR` to the absolute directory containing this file. Resolve `QUALITY_REVIEW_SKILL` directly as `$SKILL_DIR/../quality-review/SKILL.md`. Do not search the skills tree for it. If that sibling file is missing when review is required, report an incomplete installation instead of substituting another quality skill.

## Choose the execution entry

- **Activate:** Reconcile an activation packet, canonical plan, or direct implementation request; validate readiness; call `create_goal`; initialize the native plan; then continue the work.
- **Resume:** Reconcile the active goal, current plan, governing documents, repository state, and completed evidence before continuing.

Treat an explicit request to use `$ultragoal` and complete, build, implement, or pursue a concrete objective as Activate. Do not force a second approval turn when the user already requested implementation; pause only for a material unresolved choice or authority outside the request.

Ultragoal is execution-only. If the request is solely to research, inspect, critique, discuss, or design a possible goal, do not activate or mutate native state; explain that activation requires an execution-ready objective.

## Validate activation readiness

Before activation:

1. Read the named repository instructions, governing sources, existing plan or activation packet, relevant code, tests, and current state.
2. Validate any existing activation packet or plan against the live repository. Preserve valid decisions and evidence, but do not replay stale assumptions blindly.
3. Confirm one observable outcome, meaningful exclusions, the strongest feasible verifier, completion proof, dependency-ordered work, and material risk or approval gates.
4. Confirm that required environments, credentials, tools, devices, and authenticated surfaces are available. Do not silently replace an unavailable real-surface verifier with a weaker proxy.
5. State anti-cheating rules: do not weaken tests, narrow acceptance, hide failures, substitute mocks for the declared surface, or change the benchmark without approval.
6. Keep the exact objective compact: name the outcome, governing source, strongest verifier, and completion condition.

When no execution-ready source exists, perform only the minimum grounding needed to satisfy these checks. If material design choices, incompatible outcomes, or an underspecified work decomposition remain, do not activate; report the exact readiness gaps. Never create a goal from vague planning language or set a token budget unless the user explicitly requests one.

Ask only when a missing answer changes the finish line, grants new authority, or chooses between incompatible outcomes. Otherwise make the smallest reversible assumption and continue.

## Use one durable state model

Prefer, in order:

1. Canonical repository design documents, delivery runbooks, and task plans already named by the user.
2. The native active goal for the finish line and completion condition.
3. The native plan for ordered work, current status, verification, and the next action.

Create additional goal, plan, checklist, worklog, or report files only when the user requests durable artifacts or an external handoff cannot use the repository documents and native state. Never duplicate an existing authoritative runbook into generated workflow files.

Activate only after readiness validation. After activation, continue immediately with the first safe plan step.

Inspect the active goal before creating one. Resume it when it governs the same objective; never create a duplicate. If a different unfinished goal prevents activation, report the conflict and ask the user to cancel, replace, or finish it. Do not falsely complete an unrelated goal to clear the slot.

On resume or after material steering, reread the active goal and governing sources, inspect the actual tree and relevant commits, preserve valid completed evidence, update the plan, and continue from the next dependency-ready step. Keep compatible steering in the native plan. The goal API cannot edit an active objective: when steering materially changes the finish line, verifier, or completion condition, ask the user to edit, cancel, or replace the goal through an available product control before continuing. Never misuse `update_goal` or mark an unrelated goal complete to simulate an edit.

## Execute dependency-ordered work

For each work item:

1. Confirm its objective, ownership boundary, dependencies, chosen direction, invariants, observable exit condition, and targeted checks.
2. Keep only dependency-ready work active. Preserve an execution-ready lane assignment from a governing source or activation packet when it remains valid, but revalidate it against the live repository, available models and tools, open compatible agents, and current dependencies. When no valid assignment exists, choose no subagents, sequential delegation, or parallel delegation from the work structure.
3. Implement locally when the change is small, tightly coupled to active integration, or cheaper than transferring context.
4. Inspect every changed file and the complete change before acceptance. Inventory staged, unstaged, deleted, renamed, and relevant untracked files instead of assuming one diff command is complete. Treat worker output as an untrusted draft.
5. Run the relevant checks from the integration workspace. Passing tests are necessary but do not prove architecture, privacy, security, or maintainability.
6. Accept the item only when its behavioral exit condition and checks pass. Commit at that boundary only when the user or governing instructions request commits, and never include unrelated changes.
7. Update the native plan with concise evidence and advance only after dependent contracts are stable.

When a governing source or activation packet groups work into waves, treat each wave as a dispatch grouping of dependency-ready items, not as a separate durable state model. Dispatch eligible lanes in the current wave together, permit only genuinely independent parent work, integrate and verify the returned work before advancing to a dependent wave, and resequence the grouping when live dependency state differs from the packet.

When implementation evidence invalidates a material design choice, re-plan the affected work inline in the native plan before continuing: revise its objective, dependencies, ownership, invariants, exit condition, and checks. Do not buy a stronger worker to compensate for an underspecified work item.

## Coordinate subagents without losing ownership

Explicit Ultragoal activation authorizes bounded subagents when they materially help. Use no subagents for small or tightly coupled work, sequential agents for dependent or overlapping slices, and parallel agents only for independent lanes with disjoint ownership. Poll the user only when topology changes explicit cost authority, required review independence, or the accepted outcome. If agent tools are unavailable, work locally unless the user explicitly requires delegation or independence.

Use a user-selected, governing-source-selected, or activation-packet-selected model and effort when it remains available and appropriate after live revalidation. Otherwise prefer the inherited lane and use this table only when an override materially helps. Increase Luna effort for reasoning depth, use Terra for missing knowledge breadth, and use Sol for consequential decisions or reviews. Improve an underspecified work packet before buying a stronger lane; do not run a serial model tournament.

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

Give each worker one immutable objective, governing context, ownership boundary, invariants, non-goals, behavioral exit condition, checks, and stop condition. Reject a packet as too broad when it contains multiple independently testable outcomes or could return useful partial completion; split it by behavioral invariant rather than merely by frontend, backend, or plan slice. Do not repurpose an agent across incompatible roles, ownership boundaries, or independently testable outcomes.

Require workers to preserve unrelated work, avoid commits, and report behavior, changed paths, checks, deviations, and concrete risks. Default to `fork_context: false` with a self-contained packet and exact governing-document paths; fork context only when the bounded task genuinely requires conversation history that the packet cannot safely capture. Use isolated workspaces or disjoint write sets for parallel coding. Keep ownership of scope, integration, architecture, verification, and completion in the parent; treat every result as an untrusted draft.

Keep cross-worker seams, generated artifacts, contract regeneration, merge fixes, and localized changes in already-integrated code with the parent. Do not delegate a small known fix when transferring context and reviewing the result is likely to cost more than implementing it locally.

After dispatch, continue only dependency-ready parent work that is outside every agent's ownership boundary, does not depend on an agent result, and cannot interfere with an agent's files or state. Never inspect, repeat, or preempt the delegated work. When no such independent parent work remains, start one long wait with this exact Code Mode call:

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

The `1,500,000` millisecond values are maximum wait ceilings, not fixed delays. `wait_agent` resolves as soon as any target reaches a final status, so the enclosing call returns immediately with `timed_out:false`; it remains open for the full 25 minutes only when no target finishes. Do not call `functions.wait`, start another `wait_agent`, add commentary, inspect the repository, reread context, or do side work while it is pending. After `timed_out:true`, run the same call again with the remaining active IDs. For parallel lanes, collect completed results and immediately run the same call for the remaining active IDs; do not integrate until every coding lane has returned `completed` or `errored`.

### Manage agent lifecycle and reuse

Before spawning an agent, inventory the open agents. Reuse an open agent when its role, objective, ownership boundary, governing context, and artifact set remain compatible. Reuse the original implementer for related corrections and follow-up checks on its slice, and reuse the original reviewer for remediation confirmation or materially related review. Do not create overlapping agents for substantially the same work.

Treat an agent's `completed` status as completion of its current prompt, not acceptance of its work slice or release of its ownership. Keep an implementer open through parent inspection, targeted verification, review findings, corrective work, and final acceptance. Keep a reviewer open through remediation and confirmation. Close an agent only after the slice's exit condition and checks pass, all associated reviews are resolved, and no further response is expected; then close it promptly to release the concurrency slot.

Treat closing as terminal. Avoid `resume_agent` because resuming through the multi-agent tools may change the effective agent type and invalidate model, role, or continuity assumptions. If work appears after closure, prefer a fresh agent with a self-contained packet. Resume only when the closed thread contains essential context that cannot be reconstructed and a possible type change is harmless.

Reuse has no numeric prompt or correction-round limit. Batch related findings instead of drip-feeding them, keep each follow-up focused on the stable contract, and continue with the same compatible agent while corrections converge. After each correction, require concrete convergence evidence such as fewer failing checks or cases, a smaller remaining behavioral gap, or a materially stronger diagnosis. If the same failure recurs without narrowing, fixes oscillate, or repairs merely move the failure, treat the work as non-converging and re-plan rather than extending an invalid slice.

## Re-plan unstable work

Stop incremental correction and re-plan the affected work when:

- a correction repeats the same verifier failure without reducing the failing cases or narrowing the diagnosis;
- fixes oscillate between states or move the failure without shrinking the behavioral gap;
- two agents miss the same acceptance condition;
- a supposedly accepted item fails its broad verifier because of the new work;
- an aggregate review finds three or more unrelated blocking root causes;
- successive small fixes repeatedly invalidate review approval.

Batch every known finding before resuming implementation. Replace symptom-sized fixes with root-cause work items, define fresh ownership and exit conditions, and update the native plan before dispatching again. Do not ask the user unless re-planning changes the finish line, authority, or accepted outcome.

At each accepted boundary, reconcile active agents, agent ownership and lifecycle, review rounds, broad verifier runs, and known advisory findings. If any circuit breaker has fired, record the re-scoped approach in the native plan before continuing.

## Control verification cost

Run targeted checks while implementation is moving. Run a broad repository gate only when no known fixes remain and the intended item or aggregate state is frozen. Before starting it, confirm that no broad verifier from the goal is still running; if a tool call yields a process session, continue that same session instead of starting an overlapping run.

After a broad failure, reproduce and diagnose it narrowly before running the broad gate again. At ordinary slice boundaries, run the broad suite only when the governing acceptance checks or risk justify it. Always run the declared strongest final verifier on the final frozen state.

## Review at the right boundaries

Require focused review to pass before crossing a risk-bearing boundary such as authorization, privacy, destructive data changes, migrations, concurrency, or external effects. The parent may perform it unless the user or governing instructions require independence; if required independence is unavailable, stop before the boundary and report the capability gap.

Before declaring a design or implementation artifact frozen or dispatching its reviewer, confirm the exact scope, source and dependency versions, unresolved user choices, governing documents, and intended change inventory. Continue grounding instead of reviewing a knowingly moving target. Ask the reviewer to challenge every new abstraction, persisted discriminator, and compatibility layer against existing library primitives and the smallest sufficient design.

When maintained implementation code, tests, user-interface code, or agent instructions changed, read `QUALITY_REVIEW_SKILL` completely and follow it before final completion. Announce why it is being used. By default, run the strict quality review once on the frozen aggregate implementation rather than after every ordinary slice. Use earlier quality review only when the user or governing sources require it, or when a consequential slice is too large to defer safely. Quality review complements rather than replaces risk-specific review.

For integrated multi-worker or consequential changes, prefer one fresh read-only aggregate reviewer when subagents are authorized and include the resolved absolute `QUALITY_REVIEW_SKILL` path in its prompt; otherwise apply the skill directly.

Before aggregate review, freeze the intended change and pass an explicit inventory covering staged, unstaged, deleted, renamed, and relevant untracked files. A branch diff alone is not proof of complete scope.

Collect and classify the complete review result before editing. Resolve accepted blocking findings in consolidated remediation batches, inspect the resulting diff again, rerun affected checks, and request focused confirmation from the same open reviewer. Do not request review after each small repair. If confirmation finds new blocking root causes, trigger the unstable-work circuit breaker instead of dispatching symptom-sized corrections.

Treat `P0` and `P1` findings as blocking. Preserve `P2` findings as advisory residual risk and do not fix them during the active goal unless the user requested them, an explicit acceptance check requires them, or the repair is incidental to a blocking fix.

Any material change to a reviewed artifact invalidates its prior approval. Reuse the open reviewer for focused confirmation. Use a fresh reviewer only when independence requires it or the previous reviewer was already closed; do not resume a closed reviewer.

## Complete honestly

Mark the goal complete only when:

- the observable outcome exists;
- every required work item and requested commit or artifact is complete;
- every blocking risk-specific or quality finding is resolved or explicitly accepted by the user;
- verification passes on the final state after the last maintained change;
- the declared completion proof is available;
- no required work remains.

Report the outcome, strongest evidence, important review-driven changes, unresolved advisory findings, and remaining concrete risk. Mark the goal blocked only under the blocker standard declared in the active goal when a true external condition prevents meaningful progress.

Immediately before any `update_goal` completion or blocked transition, reconcile the current goal status, latest agent notifications, active or ambiguous worker ownership, authoritative worktree, and external state. Never mark blocked while an unreconciled worker may still return meaningful progress, and never overwrite a user-controlled paused or cancelled state.
