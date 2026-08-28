---
name: delegate
description: Carry out an explicit request for Codex subagents without duplicate parent work. Use only for direct user requests for subagents or parallel agents. Use multi-agent v2 for bounded work, compatible models, efficient waits, focused corrections, and reusable task identities.
---
# Delegate

Carry out the requested delegation without duplicate work. Give each subagent sole ownership until the parent accepts its work. Keep parent ownership of integration, targeted verification, and the final answer.
## Honor the requested delegation

Use this skill only for explicit user requests for delegation. Do not use it to propose or select delegation.
Assign the requested work to the subagent. Do not keep the same work for the parent.
Before dispatch, separate the subagent scope from the parent scope. Keep only independent parent work that does not require the subagent result.
If no independent parent work remains, start the long wait. If the user requests duplicate analysis, overlapping scopes are permitted.
## Select the lane

Use the inherited model and effort by default. Before dispatch, identify their exact values.
If the runtime hides these values, select an explicit compatible model and effort. This selection makes accurate reporting possible.
Override inherited values only for a concrete task requirement. Use only models that `functions.collaboration.spawn_agent` advertises.

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
## Dispatch bounded work

Give each agent a self-contained packet with these items:

- One objective and its purpose
- Exact governing files and context
- Ownership and write boundaries
- Dependencies and stable contracts
- Invariants and non-goals
- The behavioral exit condition
- Required checks and stop conditions
- Communication rules for blockers, stable handoffs, material scope changes, and completion
- Instructions to preserve unrelated work and prevent commits
- A required report with the outcome, changed paths, checks, deviations, and concrete risks.
Forbid heartbeats in the communication rules. Use a context-free spawn by default.
When the task needs context that the packet cannot safely include, use a history fork.
Call `functions.collaboration.spawn_agent` directly. Give it a unique `task_name`, the packet as `message`, and `fork_turns: "none"`.
If history is necessary, use `fork_turns: "all"` or a positive integer. A full-history fork inherits the parent model and effort.
If you override the model or effort, use `"none"` or a positive integer. Never call collaboration tools through `functions.exec`.
After each successful direct root spawn, immediately give the user a dispatch notice.
Include the canonical task name, a one-line objective, the exact model, and the exact effort.
Give a separate commentary notice for each agent. Non-root agents use the nested dispatch relay that follows.
After dispatch, do not search or read the files, questions, evidence, or code paths in the agent scope.
Do not analyze, implement, test, or examine work in the agent scope.
After the agent returns, start targeted spot-checks.
Sol and Terra agents can delegate bounded child work within their assigned scope. Before dispatch, each parent must load this skill.
The child packet must obey all ownership, dispatch, wait, verification, reuse, scope, authority, invariant, and concurrency rules. Do not expand the task or create overlapping work.
After a nested spawn, immediately send the direct parent a dispatch notice. Include the lineage, objective, exact model, and effort.
Each non-root recipient must immediately relay the notice to its parent. The root must announce the nested dispatch in commentary.
Treat dispatch notices as material events. Include this relay rule in each packet that permits nested delegation.
## Wait without polling

Treat mailbox updates as events. Continue only independent work outside all agent scopes.
If no independent work remains, call `functions.collaboration.wait_agent` directly without targets. Normally use at least 900,000 milliseconds.
The wait ends early for mailbox activity or new user input. It returns no message content. Do not poll or request progress. During the wait, do not give status commentary. Do not inspect delegated work. Do not invent side work.
Read each update and act on its event. Answer blockers and forward stable dependency contracts one time.
Integrate completed independent work. Rescope invalid work. Use `functions.collaboration.list_agents` only for reuse, unclear updates, timeouts, or final completion.
If required agents remain active and no independent work remains, wait again.
## Integrate without duplicate work

Treat each report and change as an untrusted draft. After the agent returns, review it with these steps:

1. Compare the report with the objective, boundaries, invariants, and exit condition.
2. For implementation work, inspect the complete changed-file list and diff.
3. Run the applicable checks in the parent workspace.
4. Spot-check claims or paths that are surprising, risky, unsupported, or outside the assigned boundary.
5. Examine only the questionable part. Use one focused read, command, test, or reproduction. Do not reconstruct the complete investigation.
6. Send concrete findings to the same compatible agent with `functions.collaboration.followup_task`.
7. After the targeted checks pass, accept the work.
Treat these items as suspicious: unexplained scope growth, missing or failed checks, unsupported claims, unexpected files, and hidden compatibility layers.
Also examine security, authorization, privacy, migration, concurrency, and destructive-data boundaries.
Reuse the same reviewer for related review, remediation, and follow-up checks. For required independence or a different objective, use another reviewer.
## Reuse and release agents

If an existing agent can be reused, list agents once before a spawn. Otherwise use the task identities that the parent tracks.
If its role, objective, scope, context, and artifacts remain compatible, reuse the agent.
Reuse the implementer for corrections and checks. Reuse the reviewer for related review and remediation confirmation.
Do not create overlapping agents for the same work.
The `completed` status of an agent ends its current prompt. It does not accept the work or release ownership.
Keep ownership through inspection, verification, findings, corrections, and final acceptance. Reuse has no numeric prompt or correction limit.
Batch related findings. While failures narrow, behavior improves, or diagnosis improves, continue.
If failures repeat, fixes oscillate, or faults move, stop and rescope the work.
Use `functions.collaboration.send_message` for a blocker answer or a stable contract during active work.
Use `functions.collaboration.followup_task` for completed-prompt corrections, new work, or new checks. Idle agents release capacity and remain reusable by task name.
If an instruction is urgent and safe to apply, send it during active work.
If work becomes unsafe or invalid, call `functions.collaboration.interrupt_agent`. Before you rescope it, reconcile the partial work.
If an agent stops or is interrupted, reconcile its report and changes. Then explicitly release its ownership.
If the contract remains stable, reuse the agent. Otherwise use a new task name.
If repeated corrections expose an unstable objective, ownership boundary, or integration contract, stop and return the work for rescoping.
