---
name: delegate
description: Carry out an explicit user request to use one or more Codex subagents without the parent duplicating their assigned work. Use only when the user directly asks to use, spawn, delegate to, or run subagents or parallel agents. Covers bounded task packets, model and effort selection, efficient long waits, post-return spot-checking, focused correction, and cleanup.
---

# Delegate

Carry out the user's requested delegation without duplicating it. Give each subagent sole ownership of its assigned work until the slice is accepted. Keep parent ownership of integration, targeted verification, and the final answer.

## Honor the requested delegation

Do not use this skill to decide whether to delegate or to propose delegation. Start from the user's explicit request. Assign the requested subtask to the subagent; do not quietly retain the same subtask for the parent.

Before spawning, separate the delegated scope from any parent work. Keep parent work only when it is genuinely non-overlapping and does not depend on the delegated result. Move directly to the long wait when no independent parent work remains. Do not assign overlapping lanes to multiple agents unless the user explicitly requests independent duplicate analysis.

## Select the lane

Use the inherited model and effort by default. Override them only for a concrete task need.

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
- instructions to preserve unrelated work and avoid commits;
- the required report: outcome, changed paths, checks, deviations, and concrete risks.

Default to `fork_context: false`. Use `fork_context: true` only for work that genuinely requires conversation history which cannot be captured safely in the packet.

```js
const agent = await tools.multi_agent_v1__spawn_agent({
  fork_context: false,
  message: workPacket,
});
text(JSON.stringify(agent));
```

After dispatch, do not search, read, analyze, implement, or verify the files, questions, evidence, or code paths assigned to that agent. Continue only work outside its ownership boundary. Never redo a delegated task merely because the parent is waiting. Begin spot-checking only after the subagent returns.

## Wait without polling

At the wait point, start one long wait with the active agent IDs:

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

The matching outer yield and agent timeout keep one call open for up to 25 minutes and return immediately when any target finishes. Do not call `functions.wait`, start another `wait_agent`, or emit status commentary while this call is pending. After `timed_out:true`, run the same call again with the remaining active IDs. Remove completed and errored agents from the active set, then run the same call for the remaining IDs.

## Integrate without redoing

Treat every returned report and change as an untrusted draft, but do not repeat the full delegated investigation or implementation. Verification begins after the agent returns and stays targeted:

1. Compare the report with the assigned objective, boundaries, invariants, and exit condition.
2. Inspect the complete changed-file inventory and diff for an implementation lane.
3. Run the relevant checks from the parent workspace.
4. Spot-check claims, files, or code paths that are suspicious, surprising, high-risk, weakly evidenced, or outside the assigned boundary.
5. Double-check only the questionable part with a focused read, command, test, or reproduction. Do not independently reconstruct the worker's entire analysis.
6. Send concrete findings back to the same compatible open agent with `send_input` for focused correction.
7. Accept and integrate only after the targeted checks pass.

Suspicious parts include unexplained scope expansion, omitted or failing checks, unsupported claims, unexpected files, hidden compatibility layers, and security, authorization, privacy, migration, concurrency, or destructive-data boundaries.

Reuse the same open reviewer for materially related review, remediation confirmation, and follow-up checks. Use a separate reviewer only for required independence or a genuinely distinct review objective. Do not create a second agent to repeat the implementer's or reviewer's assignment.

## Reuse and close agents

Before spawning an agent, inventory the open agents. Reuse an open agent when its role, objective, ownership boundary, governing context, and artifact set remain compatible. Reuse the original implementer for related corrections and follow-up checks on its slice, and the original reviewer for remediation confirmation or materially related review. Do not create overlapping agents for substantially the same work.

Treat an agent's `completed` status as completion of its current prompt, not acceptance of its work slice or release of its ownership. Keep an implementer open through parent inspection, targeted verification, review findings, corrective work, and final acceptance. Keep a reviewer open through remediation and confirmation. Reuse has no numeric prompt or correction-round limit: batch related findings instead of drip-feeding them, keep follow-ups focused on the stable contract, and continue with the same compatible agent while the work converges.

Request a focused correction or clarification with:

```js
const submission = await tools.multi_agent_v1__send_input({
  target: agentId,
  message: focusedCorrectionRequest,
});
text(JSON.stringify(submission));
```

Close an agent only after the slice's exit condition and checks pass, all associated reviews are resolved, and no further response is expected. Then close it promptly to release the concurrency slot:

```js
const closed = await tools.multi_agent_v1__close_agent({ target: agentId });
text(JSON.stringify(closed));
```

Treat closing as terminal. Avoid `resume_agent` because resuming through the multi-agent tools may change the effective agent type and invalidate model, role, or continuity assumptions. If work appears after closure, prefer a fresh agent with a self-contained packet. Resume only when the closed thread contains essential context that cannot be reconstructed and a possible type change is harmless.

Reuse only within a stable role and ownership contract. When repeated corrections reveal that the objective, ownership boundary, or integration contract is unstable, stop extending the slice and return it for re-scoping.
