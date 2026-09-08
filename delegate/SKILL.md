---
name: delegate
description: Coordinate explicitly requested subagents, select models, and accept their work without duplicating it.
---

# Delegate

Use for an explicit request to delegate work. The parent owns integration and acceptance; each worker owns its assigned scope until accepted or explicitly transferred.

## Choose a worker

Honor requested models and efforts; otherwise use these starting points among configurations the runtime exposes.

| Work | Model and effort | Typical use |
| --- | --- | --- |
| Mechanical execution | `gpt-5.6-luna`, `low` | Exact lookup, specified command, obvious edits, or checking an explicit condition |
| Cheap bounded scout | `gpt-5.6-luna`, `medium` | Scouting, evidence extraction, or mapping with explicit questions and cheap verification |
| Clear bounded implementation | `gpt-5.6-luna`, `high` | Small feature scopes, tests, and clear fixes with explicit acceptance criteria |
| Code exploration | `gpt-5.6-terra`, `medium` | Retrieve and connect evidence across unfamiliar code, trace dependencies, and ask the parent for guidance or decisions |
| Moderately difficult work | `gpt-5.6-terra`, `high` | Bounded reasoning or implementation benefiting parent guidance on major decisions |
| Substantial coder | `gpt-5.6-sol`, `medium` | Substantial but bounded implementation, tests, repository fixes, or moderately difficult reasoning |
| Frontier knowledge | `gpt-6-astra`, `low` | Obscure cross-domain knowledge or a hard task with a clear approach and checks |
| Ambiguous or consequential judgment | `gpt-6-astra`, `medium` | Synthesis, diagnosis, design, independent review, or permissions, data, and concurrency decisions |
| Critical reasoning | `gpt-6-astra`, `high` | Interacting high-risk constraints or a consequential reasoning or security decisions |

In the Codex runtime, Luna cannot use `send_message`; Terra can ask the parent for help, review, or decisions. Use Luna for cheap fire-and-forget assignments that can finish without that dialogue. Give it a final-report exit for blockers. Terra's stronger long-context retrieval results also support exploration across many files. Use Terra medium for exploration and high for moderately difficult reasoning or implementation over Luna where back-and-forth matters; use Sol or Astra when the worker needs greater independent reasoning. Fire-and-forget still requires parent acceptance.

## Dispatch

Use the matching [task prompt](references/task-prompt.md): the Luna version for `gpt-5.6-luna`, or the interactive version for Terra, Sol, and Astra. Fill in the task-specific context and send only that version as the worker's message. The templates carry the scope, acceptance, and model-specific communication instructions. The parent resolves major decisions within existing authority and asks the user only when necessary.

Prefer a self-contained packet with `fork_turns: "none"`. Use a partial history fork when immediate context is useful; a full-history fork inherits model and effort and cannot take overrides. Use the runtime's collaboration tools directly. Briefly announce the task and selected model/effort; report inheritance honestly when exact values are hidden. Related dispatches may share a notice.

## Protect active work

While a worker owns active work, do only independent parent work. Do not read its files, diffs, sources, or implementation to duplicate research, monitor progress, anticipate findings, or verify unfinished work. Overlap requires an explicit user request for duplicate analysis or a coordinated ownership transfer.

Inspection requires an explicit handoff: completed work, a stable partial result, or a concrete request for guidance. Inspect only the delivered portion or what answers the question, then return to independent work or waiting. A progress update is not a handoff, and review access does not transfer implementation ownership.

Use agreed interfaces and worker messages for integration. For an unexpected dependency, request the specific contract or bounded handoff needed; do not inspect the active scope while waiting.

When independent work is exhausted, use long, event-driven `collaboration.wait_agent(timeout_ms)` calls within runtime limits. The wait wakes on an agent message, completion, or timeout; messages arrive separately from the wait result. Handle material questions or handoffs, then resume waiting if work remains. An early return does not mean the worker has finished, and a timeout does not authorize cancellation or restart. Avoid status polling, heartbeat requests, and invented side work. Keep working until required handoffs and acceptance are complete; do not end the turn promising to monitor.

## Accept and reuse

Worker completion is not acceptance. Compare the deliverable against the full behavioral requirements, review changed paths and diffs, and perform focused verification of consequential or unsupported claims. Use reported checks where sufficient; do not repeat the investigation or broaden testing without a reason.

Batch omissions and corrections into a `followup_task` for the same compatible agent. Use `send_message` for guidance during active work. Keep ownership through corrections and acceptance; an idle agent remains reusable.

Before transferring ownership after a blocker or interruption, reconcile the worker's partial changes and explicitly assign the remaining scope.

Read [nested-delegation.md](references/nested-delegation.md) before permitting a worker to spawn children.
