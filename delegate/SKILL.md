---
name: delegate
description: Carry out an explicit user request to use one or more Codex subagents without the parent duplicating their assigned work. Use only when the user directly asks to use, spawn, delegate to, or run subagents or parallel agents. Uses multi-agent v2 for bounded task packets, compatible model selection, efficient waits, focused correction, and reusable task identities.
---

# Delegate

Carry out the user's requested subagent delegation without duplicating it. Give each subagent sole ownership of its assigned work until the slice is accepted. Keep parent ownership of integration, targeted verification, and the final answer.

## Honor the requested delegation

Do not use this skill to decide whether to delegate or to propose delegation. Start from the user's explicit request. Assign the requested subtask to the subagent; do not quietly retain the same subtask for the parent.

Before spawning, separate the delegated scope from any parent work. Keep parent work only when it is genuinely non-overlapping and does not depend on the delegated result. Move directly to the long wait when no independent parent work remains. Do not assign overlapping lanes to multiple agents unless the user explicitly requests independent duplicate analysis.

## Select the lane

Use the inherited model and effort by default. Resolve their exact values before dispatch; when the runtime does not expose them, pass an explicit compatible model and effort so the dispatch can be reported accurately. Otherwise override them only for a concrete task need, and use only models advertised by `functions.collaboration.spawn_agent`.

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

Improve an underspecified task packet before choosing a stronger model. Do not run serial model tournaments.

## Dispatch bounded work

Give every agent a self-contained packet containing:

- one objective and the reason it matters;
- exact governing files and context;
- ownership and write boundaries;
- dependencies and stable contracts;
- invariants and non-goals;
- the behavioral exit condition;
- required checks and stop conditions;
- communication rules: report only blockers, stable dependency handoffs, material scope changes, and completion; never send heartbeats;
- instructions to preserve unrelated work and avoid commits;
- the required report: outcome, changed paths, checks, deviations, and concrete risks.

Default to a context-free spawn with a self-contained packet. Use a history fork only when the task genuinely requires conversation history that the packet cannot safely capture.

Call `functions.collaboration.spawn_agent` directly with a unique `task_name`, the packet as `message`, and `fork_turns: "none"`. Use `fork_turns: "all"` or a positive integer string only when history is required. A full-history fork inherits the parent model and effort; when a model or effort override is needed, use `"none"` or a positive integer. Never call collaboration tools through `functions.exec`.

After every successful direct spawn from the root, immediately tell the user in commentary the agent's canonical task name, one-line objective, exact model, and reasoning effort. Report each agent separately and do not defer this notice until the final answer. A non-root agent uses the nested dispatch relay below instead.

After dispatch, do not search, read, analyze, implement, or verify the files, questions, evidence, or code paths assigned to that agent. Continue only work outside its ownership boundary. Never redo a delegated task merely because the parent is waiting. Begin spot-checking only after the subagent returns.

Sol and Terra subagents may delegate bounded child slices of their own assignment. Before spawning a child, they must load and apply this Delegate skill as that child's parent, including its ownership, task-packet, wait, verification, reuse, and dispatch-notice rules. Nested delegation must remain within the original delegation request and the worker's own scope, authority, write boundaries, invariants, and available concurrency; it must not expand the task or create overlapping work.

After a nested spawn succeeds, the spawning agent must immediately send its direct parent a dispatch notice with the parent-to-child task lineage, the child's one-line objective, exact model, and reasoning effort. Every non-root recipient must forward the notice to its direct parent without waiting for completion. The root agent must announce the nested dispatch to the user in commentary. Treat dispatch notices as material events, not heartbeats, and include this relay requirement in every packet that permits nested delegation.

## Wait without polling

Treat mailbox updates as events, not invitations to poll. Continue only independent parent work outside every agent's ownership. When none remains, call `functions.collaboration.wait_agent` directly with no targets and a long timeout, normally at least 900,000 milliseconds. It wakes early for mailbox activity and does not return the message content. Do not request routine progress, emit status commentary, inspect delegated work, or do side work while a wait is pending.

A long `wait_agent` call is an event-driven mailbox wait that wakes for agent updates or new user input.

Read each delivered update and act on the event. Answer a blocker, forward a stable dependency contract once, integrate a completed non-interfering lane, or re-scope invalid work. Call `functions.collaboration.list_agents` only when reusable-agent discovery matters before dispatch, after a timeout or ambiguous update, or before the final completion decision. If required agents remain active and no independent parent work exists, wait again.

## Integrate without redoing

Treat every returned report and change as an untrusted draft, but do not repeat the full delegated investigation or implementation. Verification begins after the agent returns and stays targeted:

1. Compare the report with the assigned objective, boundaries, invariants, and exit condition.
2. Inspect the complete changed-file inventory and diff for an implementation lane.
3. Run the relevant checks from the parent workspace.
4. Spot-check claims, files, or code paths that are suspicious, surprising, high-risk, weakly evidenced, or outside the assigned boundary.
5. Double-check only the questionable part with a focused read, command, test, or reproduction. Do not independently reconstruct the worker's entire analysis.
6. Send concrete findings back to the same compatible agent with `functions.collaboration.followup_task`.
7. Accept and integrate only after the targeted checks pass.

Suspicious parts include unexplained scope expansion, omitted or failing checks, unsupported claims, unexpected files, hidden compatibility layers, and security, authorization, privacy, migration, concurrency, or destructive-data boundaries.

Reuse the same open reviewer for materially related review, remediation confirmation, and follow-up checks. Use a separate reviewer only for required independence or a genuinely distinct review objective. Do not create a second agent to repeat the implementer's or reviewer's assignment.

## Reuse and release agents

Before spawning when existing agents may be reusable, call `functions.collaboration.list_agents` once to inventory them. Otherwise use the task identities already tracked by the parent. Reuse an agent when its role, objective, ownership boundary, governing context, and artifact set remain compatible. Reuse the original implementer for related corrections and follow-up checks on its slice, and the original reviewer for remediation confirmation or materially related review. Do not create overlapping agents for substantially the same work.

Treat an agent's `completed` status as completion of its current prompt, not acceptance of its work slice or release of its ownership. Keep the logical ownership contract through parent inspection, targeted verification, review findings, corrective work, and final acceptance. Reuse has no numeric prompt or correction-round limit: batch related findings instead of drip-feeding them and continue only while failures narrow, the behavioral gap shrinks, or the diagnosis materially improves. Re-scope when failures repeat unchanged, fixes oscillate, or repairs merely move the failure.

Use `functions.collaboration.send_message` to answer a blocker or pass a stable contract while an agent is still working. Use `functions.collaboration.followup_task` for a new actionable unit, correction, or check after its current prompt completes; send it during active work only when the new instruction is urgent and safe to incorporate. If work becomes unsafe, invalid, or materially mis-scoped, call `functions.collaboration.interrupt_agent`, reconcile its partial work, and then re-scope with `functions.collaboration.followup_task`. Idle agents release execution capacity automatically and can be reloaded by task name.

When an agent errors or is interrupted, reconcile its report and partial changes and explicitly release its ownership. Reuse it with `functions.collaboration.followup_task` only when the contract remains stable; otherwise assign a fresh task name.

Reuse only within a stable role and ownership contract. When repeated corrections reveal that the objective, ownership boundary, or integration contract is unstable, stop extending the slice and return it for re-scoping.
