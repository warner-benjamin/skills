---
name: delegate
description: Coordinate explicitly requested Codex subagents, route tasks by difficulty and verifiability, and accept their work without duplicating it.
---

# Delegate

Use for explicitly requested delegation or delegation authorized by a workflow such as ultraplan or ultragoal. The parent owns integration and acceptance. Each worker owns its assigned scope until acceptance or explicit transfer.

Optimize for accepted results within the user's Codex allowance. Consider elapsed time, parent review effort, and errors that survive review. Honor requested models and efforts. If a specifically requested configuration is unavailable, report that and use a substitute only with the user's authorization.

## Route the task

Choose the least expensive worker that can make the decisions the assignment requires. Consider how the parent will catch an error. A known fix can suit Terra across many files. A small change can need Astra if the worker must discover a missing requirement with serious consequences.

When choosing a worker's effort, every dispatcher, including a nested parent, is limited to `xhigh` or below. A higher effort requires the user's explicit request for that worker. This ceiling also applies to retries and inherited settings.

Use at least `medium` for Luna and Terra when choosing the effort yourself. The mechanical fallback below is the only exception.

| Task | Starting model and effort | Assignment boundary |
| --- | --- | --- |
| Mechanical lookup or extraction | `gpt-6-luna`, `medium` | Locate callers, inventory files, extract explicit facts, or classify records by supplied rules when the parent can spot-check the source. If Luna medium is unavailable for delegation, use `gpt-6.1-terra` at `low` for this work. |
| Investigation or implementation with a known approach | `gpt-6.1-terra`, `medium` | Follow supplied reproduction steps, apply an established fix, or add a test using an existing pattern. Use when the approach is settled and a focused test or short review can expose mistakes. |
| Visual interpretation, defined workflows, or technical communication | `gpt-6.1-terra`, `medium` | Interpret technical drawings, create charts from supplied data, complete a defined app workflow, or write documentation from verified findings. If the work also requires a diagnosis, route by the difficulty of that diagnosis. |
| Well-specified outcome with local implementation choices | `gpt-6.2-sol`, `medium` | The assignment specifies the required behavior. The worker chooses where and how to implement it and can verify the result against an acceptance criterion. |
| Implementation or investigation across components | `gpt-6.2-sol`, `medium` | Trace a request across services, implement a feature against a shared contract, or refactor several callers. Stay at medium when integration checks cover the required behavior. |
| Difficult debugging or substantive review | `gpt-6.2-sol`, `high` | Distinguish competing explanations for a failure, or review whether a change preserves a known invariant across retries or reordered events. High is the usual Sol ceiling for repository work, including long investigations. Use Sol xhigh for coding only when comparable tasks have shown enough improvement over high to justify its cost. |
| Constraint-heavy design or professional deliverables | `gpt-6.2-sol`, `xhigh` | Reconcile dimensions in a CAD assembly or keep calculations and conclusions consistent across a workbook and report. Use when requirements interact and the parent can check the result against measurements, source data, or a rubric. |
| Focused specialist inference or design judgment | `gpt-6.2-astra`, `medium` | Infer which mechanism best explains conflicting observations, identify a hidden assumption in a design, or assess a deliverable against professional conventions the rubric omits. Sol high suits specialist work whose answer can be checked against an authoritative specification. |
| Consequential judgment with hard-to-detect errors | `gpt-6.2-astra`, `high` | Identify missing invariants or choose between designs when several plausible failure modes could survive ordinary review. Examples include stale permissions after a retry and lost writes during recovery. |
| Critical reasoning | `gpt-6.2-astra`, `xhigh` | Resolve consequential constraints when satisfying one can break another. For example, determine how to roll back a partial migration without restoring revoked access or losing writes accepted during the migration. |

## Manage Codex usage

Treat the routes as defaults. Adjust them using observed allowance consumption, elapsed time, review effort, and errors that survive acceptance.

- Included Codex usage depends on context, reasoning, tools, and caching. API token-price ratios do not translate into fixed message counts or completed tasks. Purchased Codex credits track token consumption more directly.
- Workers consume allowance too. Include coordination, retries, and parent review when judging savings.
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
- For research, cite the sources you inspected and identify any missing evidence that could change your conclusion. For a mechanical lookup, citing the source is enough.
- Do not spawn children without explicit parent permission and the applicable coordination instructions.

Specify the direct parent's task name and the available communication tool, normally `collaboration.send_message`. Use runtime capabilities rather than model names to determine tool access.

By default, call `collaboration.spawn_agent` with `fork_turns: "none"`, set both `model` and `reasoning_effort`, and supply the context the worker needs. Use a full-history fork only when the worker needs the conversation and you know both inherited settings match the selected route. Omit both overrides for that fork.

Briefly announce the task, model, and effort. Group related dispatch notices.

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

Use `collaboration.send_message` for guidance during active work. Group related corrections in one `collaboration.followup_task`. The worker keeps its model and effort.

To change either setting, collect the worker's findings and identify its partial edits. End its ownership of the remaining scope before assigning that scope and evidence to a fresh worker. After handoff, the parent may take ownership of a small correction and verify it directly.
