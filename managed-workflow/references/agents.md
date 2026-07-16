# Agent routing

Read this before spawning or coordinating subagents.

## Authorization and cost

Spawn agents only when the user requests this managed workflow, delegation, parallel work, or another instruction authorizes them. A request only for a plan authorizes a strict plan reviewer but not implementation workers.

Start one implementation worker by default. Add a second only for independent work. Respect the runner's concurrency limit and avoid creating agents merely because slots are available.

Use the legacy `multi_agent_v1` tools for workers and reviewers. Immediately before every spawn, tell the user in commentary which `model` and `reasoning_effort` will be used, for example: `Spawning gpt-5.6-luna at xhigh for P1.` Then set both fields explicitly in the tool call. If a rejected combination requires a substitution, announce the replacement model and effort before retrying. Do not rely on the checklist as the only disclosure. Also set:

- `agent_type: worker` for implementation and focused fixes
- `agent_type: explorer` for read-only research and independent review
- `agent_type: default` only for a deliberately mixed task that cannot be cleanly resliced
- `fork_context: false` by default, and always for independent reviewers

The plan and work item should contain the needed context. Use `fork_context: true` only when the task materially depends on current conversation that cannot reasonably be added to the plan. Pass an absolute plan path only when the agent can read it; otherwise include the complete item contract. Do not repeat the full conversation.

Leave `service_tier` unset unless the user explicitly requests a tier or the approved plan contains a concrete latency requirement. Do not infer a paid or accelerated tier merely because the tool exposes the field.

## Model routing

Choose on two axes:

- **reasoning depth**: how much task-specific inference, ambiguity resolution, and verification the item needs
- **knowledge breadth**: how much the item depends on unfamiliar frameworks, protocols, legacy systems, or cross-domain priors

Use the chart-efficient core ladder by default. Use a larger-model knowledge override only when breadth is the reason; a larger model at lower effort is not an automatic assurance promotion.

Cost basis, checked 2026-07-12 against the [Codex rate card](https://learn.chatgpt.com/docs/pricing#what-are-tokens-and-credits) and [API pricing](https://developers.openai.com/api/docs/pricing): Luna costs 1x, Terra 2.5x, and Sol 5x across input, cached input, and output credits. Codex credits preserve the same ratios as API dollars, so converting the chart's cost axis does not change its ordering. Current [GPT-5.6 model guidance](https://developers.openai.com/api/docs/guides/latest-model#update-api-and-model-parameters) names `none`, `low`, `medium`, `high`, `xhigh`, and `max` as the reasoning levels.

The user-supplied Artificial Analysis Coding Agent Index v1.1 chart shows a steep intelligence drop below Luna `high`, then useful gains through Luna `xhigh` and `max`. It makes Luna `max` the strongest bounded-work value, Terra `max` the next substantial capability step, and Sol `xhigh` and `max` the final quality-first steps. It also shows that Luna `max` beats Terra `high` and `xhigh` on aggregate score and cost, while Luna `max` and Terra `max` approximately match Sol `medium` and `high` at lower cost. Treat these as routing evidence, not guaranteed task scores, and use the larger-model lower-effort points only for knowledge breadth.

Do not recheck pricing during ordinary dispatch. Revisit this table when the Codex rate card, available model family, or representative coding evaluations materially change.

### Core ladder

| Lane | `model` | `reasoning_effort` | `agent_type` | Use it for |
| --- | --- | --- | --- | --- |
| Cheap scout | `gpt-5.6-luna` | `medium` | `explorer`, or `worker` for an exact mechanical contract | Disposable research, file mapping, or mechanical work with deterministic verification and a cheap retry. Never delegate a material design decision here. |
| Economy worker | `gpt-5.6-luna` | `high` | `worker` | Low-risk bounded implementation with an explicit design and strong checks. This is the normal lane below Luna `xhigh`. |
| Default worker or bounded reviewer | `gpt-5.6-luna` | `xhigh` | `worker` or `explorer` | Ordinary implementation, tests, focused refactors, moderate debugging, and bounded review. |
| Demanding bounded worker or reviewer | `gpt-5.6-luna` | `max` | `worker` or `explorer` | Difficult but bounded work that needs more depth while Luna's knowledge remains sufficient. |
| Complex quality-first worker or reviewer | `gpt-5.6-terra` | `max` | `worker` or `explorer` | Difficult cross-layer work where Terra's breadth and maximum reasoning are both justified. |
| High-risk worker or reviewer | `gpt-5.6-sol` | `xhigh` | `worker` or `explorer` | Security, permissions, migrations, difficult architecture, or hard debugging. |
| Critical worker or reviewer | `gpt-5.6-sol` | `max` | `worker` or `explorer` | Critical destructive or externally consequential work, explicit high assurance, or a high-risk task still unresolved after `xhigh`. |

Do not use `none` or `low` for managed implementation or a material verdict. Their charted intelligence loss is too large for the small savings. Luna `medium` is the managed floor and only for work whose failure is cheap and easy to detect.

### Knowledge overrides

Use these lanes when a larger base model's breadth is more important than its charted aggregate efficiency:

| Lane | `model` | `reasoning_effort` | `agent_type` | Use it for |
| --- | --- | --- | --- | --- |
| Knowledge-heavy bounded worker or scout | `gpt-5.6-terra` | `high` | `worker` or `explorer` | An unfamiliar language, framework, protocol, or repository where the reasoning contract is still bounded. |
| Complex worker or strict reviewer | `gpt-5.6-terra` | `xhigh` | `worker` or `explorer` | Cross-layer design, migration planning, ambiguous implementation, or strict review that benefits from Terra's broader priors. This remains the default when Terra is selected. |
| Frontier-knowledge scout or bounded worker | `gpt-5.6-sol` | `medium` | `explorer`, or `worker` with an explicit contract | Obscure, legacy, or cross-domain knowledge dominates and the required synthesis is bounded. Do not use it for a final high-risk verdict. |
| Knowledge-heavy worker or reviewer | `gpt-5.6-sol` | `high` | `worker` or `explorer` | Broad unfamiliar systems, cross-domain diagnosis, or architecture where Sol's priors matter but `xhigh` reasoning is not justified. |

When the user selects Luna, Terra, or Sol without naming effort, use `xhigh`. Move to `max` when the selected model still fits but the task needs its hardest quality-first setting. Move to a larger model below `max` only under a knowledge override and record the breadth reason in the checklist. Treat `max` as the highest reasoning level in this routing policy.

Use `gpt-5.5` or `gpt-5.4` only when the user explicitly requests that model or a compatibility constraint requires it. Reasoning levels vary by model. If a selected model rejects the intended effort, retry with the closest supported level that preserves the lane's intent; do not silently omit `reasoning_effort`. Record any model or effort substitution in the checklist.

## Worker contract

Give each worker:

- one work item and a clear ownership boundary
- an accessible plan path and relevant work item ID, or the complete work item contract
- expected behavior, acceptance condition, and checks
- a request to preserve unrelated changes and avoid commits
- a stop before external mutations, destructive actions, secret access, or other authority not present in the item
- a clear stop condition

Require a concise final response with changed paths, checks and results, blockers, and remaining risks. The response is enough for normal managed work. Persist it under `results/` only when a workspace transfer cannot preserve the exchange or the user explicitly requests a separate artifact.

## Isolation and parallel work

Prefer the runner's isolated workspace when available. Use a worktree only when local isolation is needed. Use a shared tree for one coding worker at a time, or for parallel workers with strictly disjoint files and behavior.

The main agent owns integration. Inspect worker changes before staging or committing. Rerun checks when importing from another workspace, when changes interact, or when evidence is uncertain.

## Worker continuity

Before closing a completed coding worker, inspect the next ready item.

- Reuse the same worker when the next item directly depends on its accepted work and overlaps the same files, behavior, or subsystem. Inspect and accept the prior item first, then send the next item as a separate bounded contract.
- If that worker was closed and the runner supports resume, resume it instead of spawning a fresh worker. Do not switch workers merely to select a cheaper lane; include rediscovery cost in the routing decision.
- Start a fresh worker when independence matters, the prior worker failed or worked outside scope, the ownership boundary is unrelated, or a material risk change requires a different model. Record the reason when the overlap would otherwise favor reuse.
- Keep tightly coupled edits to the same hot files local when the main agent already holds the integration context or worker handoff would cost more than implementation. Do not make a fresh worker rediscover an accepted adjacent slice.

Keep the worker open until this continuity decision is made. Close it when no related ready item remains or a fresh/local lane is justified.

## Worker liveness and waits

Give coding workers an action-oriented start: inspect the named boundary, perform at most one bounded discovery pass, then edit and run the stated checks. If the contract still does not identify an implementation path, require a blocker report instead of open-ended exploration.

After dispatch:

1. Treat runner status, worker messages, and the final notification as the liveness evidence. Never infer progress or a stall from file modification times, diff size, process listings, or repeated repository probes.
2. Pause parent work while the coding worker runs. Do not reread its context, inspect its owned files, research later items, map the next slice, or invent other work to fill the wait. Handle only user steering, a hard stop, or a material external event until the worker returns.
3. Wait in increasing intervals: 2 minutes, then 5 minutes, then 8 minutes, increasing later intervals by about 3 minutes up to the runner or platform maximum. Prefer the final notification over status polling. If an outer executor yields before the inner wait completes, resume that same wait without analysis, commentary, or repository probes. Do not publish an update merely because a wait interval elapsed.
4. Treat the lane as stalled only after a runner error or `not_found`, an explicit worker blocker, a user or dependency change, or an explicit task timeout/budget. Quiet output and unchanged files are not stall evidence.
5. On a concrete stall, make one recovery attempt: reuse the addressable worker with a narrower action-first contract when its work is salvageable, otherwise close it. If that attempt does not converge, reslice or let the main agent implement locally. Do not run repeated interrupt-and-poll cycles.

Goal mode preserves the workflow across waits; it does not authorize busy waiting or filesystem surveillance.

## Review routing

Use the main agent's integration review for normal managed work. Use a fresh implementation reviewer only at a boundary with high risk. Start bounded reviewers with Luna at `xhigh` and raise Luna to `max` when its knowledge is sufficient. Start strict or cross-layer reviewers with Terra at `xhigh` and raise Terra to `max` when needed. Terra `high` and Sol `medium` or `high` are knowledge overrides, not generic review escalations; do not use Sol `medium` for a final high-risk verdict. Use Sol at `xhigh` for high-risk review and Sol at `max` for critical review. The `managed-quality` phase owns final quality reviewer routing.

Freeze the artifact under review and record reviewer identity when material fixes may need confirmation. If the artifact changes materially before the verdict arrives, treat the verdict as stale. Reuse the same reviewer only when material fixes need confirmation.

Record the review verdict and material evidence in `checklist.md`. Do not create a separate review file unless the user explicitly requests it or an external handoff cannot use the checklist and final response.

If a required reviewer is unavailable, let the main agent perform the review and record the caveat. Stop only when the user or governing policy requires independence.
