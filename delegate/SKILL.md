---
name: delegate
description: Coordinate explicitly requested Codex subagents, route tasks by difficulty and verifiability, and accept their work without duplicating it.
---

# Delegate

Use for explicitly requested delegation or delegation authorized by a workflow such as ultraplan or ultragoal.
The parent owns integration and acceptance. Each worker owns its assigned scope until acceptance or explicit transfer.

Optimize for accepted results within the user's Codex allowance. Consider elapsed time, parent review effort, and errors that survive review. Honor requested models and efforts; otherwise choose among configurations the runtime exposes.

## Route the task

Choose by task difficulty, how reliably the result can be checked, and whether the worker blocks other work. A short answer can require difficult judgment. Route by the task, not a role label such as researcher or reviewer.

| Task | Starting model and effort | Assignment boundary |
| --- | --- | --- |
| Mechanical lookup or extraction | `gpt-6-luna`, `low` | Locate definitions and callers, inventory files, extract explicit facts, classify with supplied rules, or summarize test output. Require direct evidence. |
| Bounded investigation or small implementation | `gpt-6-luna`, `high` | Investigate one isolated failure, implement a specified change, or add tests for explicit behavior. Use when reliable checks or a short review can detect mistakes. |
| Well-specified implementation or focused investigation | `gpt-6.1-sol`, `low` | Implement a clear change or trace a focused repository question with reliable checks. Use when Luna requires too much supervision or blocks other work. |
| General implementation or verifiable hard work | `gpt-6.1-sol`, `medium` | Implement features, debug a reproduction, refactor a defined scope, or synthesize evidence across files. Default for general implementation and well-framed hard tasks with objective checks. |
| Difficult debugging or substantive review | `gpt-6.1-sol`, `high` | Diagnose uncertain causes, change interacting components, review patches, or resolve conflicting requirements. Use when explicit requirements and reliable acceptance checks make the result verifiable. |
| Persistent reasoning or complex deliverables | `gpt-6.1-sol`, `xhigh` | Trace long execution paths, resolve conflicting evidence, or produce polished deliverables with interacting requirements. Use when reliable checks support acceptance and task evidence justifies the extra time. |
| Specialist knowledge | `gpt-6-astra`, `low` | Apply obscure specialist knowledge, analyze unfamiliar mechanisms, or connect evidence across domains when broader model capability is useful. |
| Ambiguous or consequential judgment, including errors that are difficult to detect | `gpt-6-astra`, `medium` | Identify hidden assumptions, choose between architectural approaches, or independently review permissions, data, and concurrency decisions. Use when plausible consequential errors can survive review. |
| Critical reasoning | `gpt-6-astra`, `high` | Resolve interacting high-risk constraints or exceptionally demanding reasoning and security judgments. |

Luna high and GPT-6.1 Sol medium are the main economical starting points. Use Sol low for well-specified work and Sol high/xhigh for harder work with reliable acceptance checks. Use Astra low for specialist knowledge and Astra medium when consequential errors are difficult to detect. Favor Luna when acceptance is cheap and objective. Lower token prices do not establish faster completion.

## Manage Codex usage

Treat the routes as defaults. Adjust them using observed allowance consumption, elapsed time, review effort, and errors that survive acceptance.

- Included Codex usage depends on context, reasoning, tools, and caching. API token-price ratios do not translate into fixed message counts or completed tasks. Purchased Codex credits track token consumption more directly.
- Workers consume allowance too. Include coordination, retries, and parent review when judging savings.
- Keep Sol max outside routine routes. Higher effort can increase cost and latency without improving coding results.
- Use Codex usage information when making budget decisions.
- Increase effort to address a specific reasoning problem, then evaluate the result. Higher effort does not guarantee better results. Check both unsupported claims and omitted requirements before acceptance.

Use available experience to refine routing; proceed with these defaults when no task history exists.

## Dispatch and ownership

Delegate only when the benefit exceeds transfer and integration costs. Keep small or tightly coupled work local.
Delegate only independent, non-overlapping assignments that can finish from the supplied context without ongoing inter-agent communication.
Settle shared interfaces and prerequisites before dispatch. Start dependent assignments only after their prerequisites are accepted.
Keep work requiring shared edits, joint design, or repeated coordination with one owner.
Normally, one assignment and one final handoff suffice. Reserve intermediate messages for unexpected blockers or consequential decisions.
Independent review examines a stable handoff and does not authorize concurrent implementation ownership.
Give capable workers coherent components, behaviors, or research questions. Avoid dividing one decision across many small assignments.
Prefer a flat team with distinct ownership. Before permitting nested delegation, read [nested-delegation.md](references/nested-delegation.md).

Give each worker a focused packet. Adapt this checklist and omit fields that do not apply:

```text
Objective:
Owned scope and exclusions:
Relevant context and entry points:
Deliverable and acceptance checks:
Decisions requiring parent guidance:
Direct parent:
```

Include these instructions in the assignment. Workers without inherited history do not receive the parent's guidance automatically:

- Preserve unrelated work and authorization limits. Resolve routine details independently.
- Before changing unsettled architecture, shared interfaces, scope, compatibility, or consequential risk, ask the direct parent for guidance.
- Include evidence and a recommendation with a decision request. Continue independent work while awaiting guidance, but wait on dependent work.
- Message for decisions, blockers, changed interfaces, consequential findings, or usable handoffs. Combine related updates.
- Omit acknowledgments, repeated plans, unchanged ownership reminders, tool narration, and heartbeat messages.
- Report the outcome, changed paths, checks and results, deviations, and unresolved issues. Identify stable portions ready for inspection.
- Do not spawn children without explicit parent permission and the applicable coordination instructions.

Specify the direct parent's task name and the available communication tool, normally `collaboration.send_message`.
Use runtime capabilities rather than model names to determine tool access.
If messaging is unavailable, require a final blocker report with completed work, evidence, and the needed decision.
Do not let missing messaging authorize an unresolved consequential decision.

Prefer `fork_turns: "none"` with a self-contained packet. Use a partial history fork when useful.
A full-history fork inherits model and effort and cannot take overrides. Use collaboration tools directly.
Briefly announce the task and selected model/effort. Batch related dispatch notices and report unknown inheritance honestly.

While a worker owns active work, do only independent parent work.
Do not inspect its files, diffs, or sources to monitor progress, duplicate research, or anticipate findings.
Overlap requires an explicit user request for duplicate analysis or a coordinated ownership transfer.
Inspection requires completed work, an explicit stable handoff, or a concrete guidance request.
Inspect only the delivered portion or what answers the question. Review access does not transfer implementation ownership.
For unexpected dependencies, request the specific interface contract or bounded handoff instead of inspecting active work.

## Communicate and wait

Give the user material findings, decisions, blockers, and handoffs. Do not paraphrase every internal exchange or announce unchanged waiting states.
Batch related corrections and updates. Follow higher-priority runtime update requirements without creating extra worker status requests.

When independent work is exhausted, use event-driven `collaboration.wait_agent` calls within runtime limits.
An early return does not mean completion. A timeout does not authorize cancellation or restart.
Handle actionable messages, then resume waiting until required handoffs and acceptance are complete.
Avoid status polling, heartbeat requests, and invented side work. Do not end the turn promising to monitor.

## Accept and escalate

Worker completion is not acceptance. Check the full requirements, review delivered changes, and verify consequential or unsupported claims. Use reported checks where sufficient; do not reconstruct the investigation or repeat tests without a reason. If acceptance routinely requires reconstructing the work, improve the task packet or use a stronger worker.

Choose the next step from the failure:

- Missing information: obtain the evidence or narrow the task.
- Correct framing but insufficient reasoning: try higher effort and evaluate whether it resolves the problem.
- Repeated wrong assumptions or unresolved ambiguity: move to a stronger model.
- Incomplete deliverable: identify omitted requirements and request corrections before increasing effort.

Do not climb every effort level mechanically. Luna high to Sol low/medium and Sol medium/high/xhigh to Astra low/medium are normal escalation routes. Choose by the cause of failure and the difficulty of acceptance.

Batch corrections into a `followup_task` for the same compatible agent. Use `send_message` for guidance during active work.
After handoff, take ownership of a local correction when that is simpler than delegating it. Verify the correction.
Before changing workers, reconcile partial changes and explicitly transfer the remaining scope. Keep ownership clear through acceptance.
