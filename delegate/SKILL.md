---
name: delegate
description: Coordinate explicitly requested Codex subagents, route tasks by difficulty and verifiability, and accept their work without duplicating it.
---

# Delegate

Use for explicitly requested delegation or delegation authorized by a workflow such as ultraplan or ultragoal. The parent owns integration and acceptance. Each worker owns its assigned scope until acceptance or explicit transfer.

Optimize for accepted results within the user's Codex allowance. Consider elapsed time, parent review effort, and errors that survive review. Honor requested models and efforts; otherwise choose among configurations the runtime exposes.

## Route the task

Choose by the delegated assignment's difficulty, how reliably the result can be checked, and the cost of supervision. A hard project can contain assignments suitable for Luna. A short answer can require difficult judgment. Route by the assignment, not the overall project or a role label such as researcher or reviewer. For development tasks, Luna/Terra roughly cover junior-developer work and Sol/Astra senior or expert work. Use this as shorthand for the task table below. Terra remains a good and cost effective choice for technical communication and visual work.

| Task | Starting model and effort | Assignment boundary |
| --- | --- | --- |
| Mechanical lookup or extraction | `gpt-6-luna`, `low` | Locate definitions and callers, inventory files, extract explicit facts, classify with supplied rules, or summarize test output. |
| Investigations or implementations with a clear approach | `gpt-6-luna`, `high` | Investigate an isolated failure, implement a change, or add tests when the approach is clear and few decisions remain. Use when reliable checks or a short review can detect mistakes. |
| Visual interpretation, defined workflows, or technical communication | `gpt-6.1-terra`, `medium` | Interpret or create images, charts, and technical drawings; complete app workflows with defined outcomes; write or revise documentation grounded in code, verified findings, or supplied references. Route unresolved technical investigation by its difficulty. |
| Well-specified outcomes requiring local implementation choices | `gpt-6.1-terra`, `high` | Implement a change or investigate a focused repository question when the outcome is clear but the worker must choose an approach or reconcile multiple local constraints. |
| Implementation or investigation across interacting components | `gpt-6.1-sol`, `medium` | Implement features, debug reproductions, or refactor when the assignment requires reasoning across interacting components, reconciling conflicting evidence, or decisions that cheaper workers would need substantial help to make. |
| Difficult debugging or substantive review | `gpt-6.1-sol`, `high` | Diagnose difficult failures or review interacting invariants when task evidence indicates a specific reasoning-depth need beyond medium. Review status or interacting components alone do not justify high effort. |
| Persistent reasoning or complex deliverables | `gpt-6.1-sol`, `xhigh` | Trace long execution paths, resolve conflicting evidence, or produce polished deliverables with interacting requirements. Use when reliable checks support acceptance and task evidence justifies the extra time. |
| Specialist knowledge | `gpt-6-astra`, `low` | Apply obscure specialist knowledge, analyze unfamiliar mechanisms, or connect evidence across domains when broader model capability is useful. |
| Ambiguous or consequential judgment, including errors that are difficult to detect | `gpt-6-astra`, `medium` | Identify hidden assumptions, choose between architectural approaches, or independently review permissions, data, and concurrency decisions. Use when plausible consequential errors can survive review. |
| Critical reasoning | `gpt-6-astra`, `high` | Resolve interacting high-risk constraints or exceptionally demanding reasoning and security judgments. |

Start with the least expensive model suited to the assignment.

## Manage Codex usage

Treat the routes as defaults. Adjust them using observed allowance consumption, elapsed time, review effort, and errors that survive acceptance.

- Included Codex usage depends on context, reasoning, tools, and caching. API token-price ratios do not translate into fixed message counts or completed tasks. Purchased Codex credits track token consumption more directly.
- Workers consume allowance too. Include coordination, retries, and parent review when judging savings.
- Do not use max effort. Higher effort can increase cost and latency without improving coding results.
- Use Codex usage information when making budget decisions.
- Increase effort to address a specific reasoning problem, then evaluate the result. Higher effort does not guarantee better results.

## Dispatch and ownership

Delegate only when the benefit exceeds transfer and integration costs. Keep small or tightly coupled work local. Delegate only independent, non-overlapping assignments that can finish from the supplied context without ongoing inter-agent communication. Settle shared interfaces and prerequisites before dispatch. Start dependent assignments only after their prerequisites are accepted. Keep work requiring shared edits, joint design, or repeated coordination with one owner.

Normally, one assignment and one final handoff suffice. Reserve intermediate messages for unexpected blockers or consequential decisions. Independent review examines a stable handoff and does not authorize concurrent implementation ownership.

Give capable workers coherent components, behaviors, or research questions. Avoid dividing one decision across many small assignments. Prefer a flat team with distinct ownership. Before permitting nested delegation, read [nested-delegation.md](references/nested-delegation.md).

Give each worker a focused packet. Adapt this checklist and omit fields that do not apply:

```text
Objective:
Owned scope and exclusions:
Relevant context and entry points:
Deliverable and acceptance checks:
Decisions requiring parent guidance:
Direct parent:
```

Include the instructions below in the assignment. Workers without inherited history do not receive the parent's guidance automatically:

- Preserve unrelated work and authorization limits. Resolve routine details independently.
- Before changing unsettled architecture, shared interfaces, scope, compatibility, or consequential risk, ask the direct parent for guidance.
- Include evidence and a recommendation with a decision request. Continue independent work while awaiting guidance, but wait on dependent work.
- Message for decisions, blockers, changed interfaces, consequential findings, or usable handoffs. Combine related updates.
- Omit acknowledgments, repeated plans, unchanged ownership reminders, tool narration, and heartbeat messages.
- Report the outcome, changed paths, checks and results, deviations, and unresolved issues. Identify stable portions ready for inspection.
- Do not spawn children without explicit parent permission and the applicable coordination instructions.

Specify the direct parent's task name and the available communication tool, normally `collaboration.send_message`. Use runtime capabilities rather than model names to determine tool access.

Prefer `fork_turns: "none"` with a self-contained packet. Use a full-history fork when the worker needs the surrounding conversation. A full-history fork inherits model and effort and cannot take overrides. Use collaboration tools directly.

Briefly announce the task and selected model/effort. Batch related dispatch notices and report unknown inheritance honestly.

While a worker owns active work, do only independent parent work. Do not inspect its files, diffs, or sources to monitor progress, duplicate research, or anticipate findings. Overlap requires an explicit user request for duplicate analysis or a coordinated ownership transfer.

Inspection requires completed work, an explicit stable handoff, or a concrete guidance request. Inspect only the delivered portion or what answers the question. Review access does not transfer implementation ownership. For unexpected dependencies, request the specific interface contract or bounded handoff instead of inspecting active work.

## Communicate and wait

Give the user material findings, decisions, blockers, and handoffs. Do not paraphrase every internal exchange or announce unchanged waiting states. Batch related corrections and updates. Follow higher-priority runtime update requirements without creating extra worker status requests.

When independent work is exhausted, use event-driven `collaboration.wait_agent` calls within runtime limits. An early return does not mean completion. A timeout does not authorize cancellation or restart. Handle actionable messages, then resume waiting until required handoffs and acceptance are complete. Avoid status polling, heartbeat requests, and invented side work. Do not end the turn promising to monitor.

## Accept and escalate

Check that the handoff covers the assignment. Spot-check routine work; verify consequential claims and authorization boundaries. Investigate further only when something warrants it.

Choose the next step from the failure:

- Missing information: obtain the evidence or narrow the task.
- Correct framing but insufficient reasoning: try higher effort and evaluate whether it resolves the problem.
- Repeated wrong assumptions or unresolved ambiguity: move to a stronger model.
- Incomplete deliverable: identify omitted requirements and request corrections before increasing effort.

Do not climb every effort level mechanically. For knowledge or taste limitations, favor a stronger model over more reasoning effort.

Batch corrections into a `followup_task` for the same compatible agent. Use `send_message` for guidance during active work. After handoff, take ownership of a local correction when that is simpler than delegating it. Verify the correction. Before changing workers, reconcile partial changes and explicitly transfer the remaining scope.
