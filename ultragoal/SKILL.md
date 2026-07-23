---
name: ultragoal
description: Design, critique, activate, and run durable Codex goals through grounded planning, dependency-ordered implementation, bounded delegation, manager-owned integration, verification, review, and completion proof. Use only when the user explicitly invokes $ultragoal, asks to set or run a persistent goal, or requests a long-running managed implementation with goal state and verifiable completion.
---

# Ultragoal

Own one durable objective from grounding through verified completion. Use native goal and plan state; do not build a second workflow state machine.

## Choose the mode

- **Design:** Ground and critique a proposed goal. Do not call `create_goal` or implement.
- **Activate:** Ground the goal, define its verifier and plan, call `create_goal`, then continue the work.
- **Resume:** Reconcile the active goal, current plan, governing documents, repository state, and completed evidence before continuing.

Treat an explicit request to use `$ultragoal` and complete, build, implement, or pursue a concrete objective as Activate. Stay in Design only when the user asks to draft, critique, or discuss the goal without starting it.

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

Give each worker one objective, governing context, ownership boundary, invariants, non-goals, behavioral exit condition, checks, and stop condition. Require it to preserve unrelated work, avoid commits, and report behavior, changed paths, checks, deviations, and concrete risks. Use isolated workspaces or disjoint write sets for parallel coding. Keep ownership of scope, integration, architecture, verification, and completion in the parent; treat every result as an untrusted draft.

Immediately after dispatch, call `wait_agent` with the active IDs and `timeout_ms: 1500000`. The timeout is only an upper bound and returns immediately when any target finishes. Do no commentary, polling, repository inspection, context rereading, or side work while pending. For parallel lanes, collect completed results and immediately wait on remaining active IDs with the same timeout; do not integrate until every coding lane is terminal.

Keep an implementer open through parent inspection, one focused correction pass, verification, required review, and acceptance. Reuse it with `send_input`; do not resume a closed agent. Use one fresh read-only reviewer when independence or a risk-bearing boundary matters, keep it open for focused confirmation, and do not create a reviewer chain.

## Review at the right boundaries

Require focused review to pass before crossing a risk-bearing boundary such as authorization, privacy, destructive data changes, migrations, concurrency, or external effects. The parent may perform it unless the user or governing instructions require independence; if required independence is unavailable, stop before the boundary and report the capability gap.

When maintained implementation code, tests, user-interface code, or agent instructions changed, run the sibling `quality-review` skill before final completion. Announce why it is being used. For integrated multi-worker or consequential changes, prefer one fresh read-only aggregate reviewer when subagents are authorized; otherwise apply the skill directly. Quality review complements rather than replaces risk-specific review.

Before aggregate review, freeze the intended change and pass an explicit inventory covering staged, unstaged, deleted, renamed, and relevant untracked files. A branch diff alone is not proof of complete scope.

Resolve accepted findings, inspect the resulting diff again, and rerun affected checks plus the strongest final verifier.

## Complete honestly

Mark the goal complete only when:

- the observable outcome exists;
- every required work item and requested commit or artifact is complete;
- every blocking risk-specific or quality finding is resolved or explicitly accepted by the user;
- verification passes on the final state after the last maintained change;
- the declared completion proof is available;
- no required work remains.

Report the outcome, strongest evidence, important review-driven changes, unresolved advisory findings, and remaining concrete risk. Mark the goal blocked only under the platform blocker rule when a true external condition prevents meaningful progress.
