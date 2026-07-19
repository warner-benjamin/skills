# Agent routing

Read this before spawning or coordinating subagents.

## Contents

- Authorization and call contract
- Model routing
- Worker contract
- Isolation and parallel work
- Agent continuity
- Worker liveness and waits
- Review routing

## Authorization and call contract

Spawn agents only when the user requests this managed workflow, delegation, parallel work, or another instruction authorizes them. A request only for a plan authorizes a strict plan reviewer but not implementation workers.

Start one implementation worker by default. Add a second only for independent work. Respect the runner's concurrency limit and avoid creating agents merely because slots are available.

Use the `multi_agent_v1` tools for workers and reviewers.

<!-- spawn-agent-fields: fork_context, items, message, model, reasoning_effort, service_tier -->

Use only the current spawn arguments: `message` or `items`, `model`, `reasoning_effort`, `service_tier`, and `fork_context`. Immediately before every new worker or reviewer spawn, name the selected model and reasoning level in commentary. Announce any replacement combination before retrying a rejected spawn. Do not rely on the checklist as the only disclosure. Set `model`, `reasoning_effort`, and `fork_context` explicitly.

Use an action-oriented implementation prompt for coding and focused fixes. Use a read-only review prompt for research and independent review. Use `fork_context: false` by default and always for independent reviewers.

The plan and work item should contain the needed context. Use `fork_context: true` only when the task materially depends on current conversation that cannot reasonably be added to the plan. Pass an absolute plan path only when the agent can read it; otherwise include the complete item contract. Do not repeat the full conversation.

Leave `service_tier` unset unless the user explicitly requests a tier or the approved plan contains a concrete latency requirement. Do not infer a paid or accelerated tier merely because the tool exposes the field.

## Model routing

Classify the task on three independent axes. Use evidence from the plan, repository, and required behavior; never use the manager's own model, subjective confidence, or personal familiarity as the classifier.

- **Reasoning depth** is the difficulty of deriving a correct answer from facts and patterns already available in the work packet or repository. Signals include several plausible root causes, interacting invariants, a long dependency chain, conflicting local constraints, subtle edge cases, or a verdict that needs adversarial proof. More effort on the same model should help. File count, diff size, long tests, and production code alone are not depth.
- **Knowledge breadth** is the amount of relevant prior knowledge not supplied by the work packet or repository. Signals include an unfamiliar language or framework, an external or obscure protocol, legacy conventions with sparse local examples, or synthesis across distinct domains such as storage, networking, identity, and deployment. A larger base model should help even when the requested inference is bounded. Several files or layers that follow well-documented local patterns are not breadth.
- **Consequence** is the impact of a wrong decision or verdict, independent of how hard the reasoning is. Security, authorization, data loss, destructive migration, concurrency safety, and public or external effects raise consequence. A detailed plan can reduce depth but does not reduce consequence.

Use this decision test after improving any avoidably thin plan:

1. If the remaining uncertainty is “what follows from these known facts and constraints?”, classify it as depth and stay on Luna while moving from `high` to `xhigh`, then `max`.
2. If the remaining uncertainty is “what facts, conventions, or failure modes from this unfamiliar technology or domain apply?”, classify it as breadth and move to Terra; use Sol `high` only when the needed priors are genuinely obscure or cross-domain beyond Terra's likely coverage.
3. If the main reason for stronger assurance is “a wrong verdict would be costly,” classify it as consequence and put Sol `xhigh` or `max` on the risk-bearing decision or review rather than every implementation slice.

Use the Luna-first core ladder by default. Do not move from Luna to Terra or Sol merely because an item sounds difficult. Record the concrete breadth or consequence evidence; otherwise keep the work on Luna and select effort by depth.

### Dispatch gate

Classify the work packet before selecting a lane:

- **Mechanical**: the exact edit is known, no material choice remains, and deterministic checks expose failure. Luna `medium` is allowed.
- **Execution-ready**: the plan names the chosen design, ownership and integration points, important behavior and invariants, acceptance condition, and checks. Use Luna `high` for most implementation and bounded review.
- **Discovery-bearing**: even after planning, the worker must infer a material design, diagnose an unclear nonlocal failure, or synthesize coupled subsystems. Use Luna `xhigh` or a justified knowledge override.

If a packet is discovery-bearing only because the plan omitted available decisions or repository facts, return to planning and improve the packet. Do not use a higher reasoning level as a substitute for a detailed executable plan. Detail decisions and evidence, not narrative volume.

### Core ladder

| Lane | `model` | `reasoning_effort` | Use it for |
| --- | --- | --- | --- |
| Cheap scout | `gpt-5.6-luna` | `medium` | Disposable research, file mapping, or mechanical work with deterministic verification and a cheap retry. Never delegate a material design decision here. |
| Default managed worker or bounded reviewer | `gpt-5.6-luna` | `high` | Most work with a reviewed design, bounded ownership, explicit acceptance, and strong checks: feature slices, tests, focused refactors, and clear bug fixes. Start here. |
| Escalated bounded worker or reviewer | `gpt-5.6-luna` | `xhigh` | Autonomous issue resolution that still requires material design inference, diagnosis of an unclear failure, coupled cross-subsystem reasoning, or a consequential verdict. |
| Demanding bounded worker or reviewer | `gpt-5.6-luna` | `max` | Difficult but bounded work with evidence that `xhigh` is insufficient, or a critical depth requirement while Luna's knowledge remains sufficient. |
| Complex quality-first worker or reviewer | `gpt-5.6-terra` | `max` | Difficult cross-layer work where Terra's breadth and maximum reasoning are both justified. |
| High-risk decision-maker or reviewer | `gpt-5.6-sol` | `xhigh` | A lane that must reason about security, permissions, destructive migration, or another externally consequential boundary. |
| Critical decision-maker or reviewer | `gpt-5.6-sol` | `max` | A lane making a critical destructive or externally consequential decision, explicit critical assurance, or high-risk reasoning still unresolved after `xhigh`. |

Start new managed implementation workers at Luna `high`. Do not raise them to `xhigh` merely because they edit production code, span several files, add tests, run long checks, or belong to a strict workflow. Raise to `xhigh` only when the item itself retains material ambiguity, requires nonlocal diagnosis or coupled reasoning, carries a consequential verdict, or a well-scoped `high` attempt exposed a reasoning limitation. Raise to `max` only for a difficult bounded item that meets the stronger lane above. A strict or high-consequence run may still use Luna `high` for execution-ready slices; put Sol on the risk-bearing design or independent review unless the worker itself must make the consequential judgment. Do not prepay for hypothetical difficulty.

Do not use `none` or `low` for managed implementation or a material verdict. Luna `medium` is the managed floor and only for work whose failure is cheap and easy to detect.

### Knowledge overrides

Use these lanes when a larger base model's breadth is the material requirement:

| Lane | `model` | `reasoning_effort` | Use it for |
| --- | --- | --- | --- |
| Knowledge-heavy bounded worker or scout | `gpt-5.6-terra` | `high` | An unfamiliar language, framework, protocol, or repository where the reasoning contract is still bounded. |
| Complex worker or strict reviewer | `gpt-5.6-terra` | `xhigh` | Cross-layer design, migration planning, ambiguous implementation, or strict review that benefits from Terra's broader priors. This remains the default when Terra is selected. |
| Frontier-knowledge worker or reviewer | `gpt-5.6-sol` | `high` | Truly obscure or broad cross-domain diagnosis where Terra's priors are insufficient but the work is not high-consequence. |

When the user selects Luna without naming effort, use `high`. When the user selects Terra or Sol without naming effort, use `xhigh`. Move to `max` when the selected model still fits but the task needs its hardest quality-first setting. Move to a larger model below `max` only under a knowledge override and record the breadth reason in the checklist. Treat `max` as the highest reasoning level in this routing policy.

Use `gpt-5.5` or `gpt-5.4` only when the user explicitly requests that model or a compatibility constraint requires it. Reasoning levels vary by model. If a selected model rejects the intended effort, retry with the closest supported level that preserves the lane's intent; do not silently omit `reasoning_effort`. Record any model or effort substitution in the checklist.

### Independent plan review

Select one lane from the plan's required assurance, breadth, and depth. Do not start with a cheap review and automatically run stronger reviewers afterward.

| Review lane | Model and effort | Use when |
| --- | --- | --- |
| Economy independent review | `gpt-5.6-luna` at `xhigh` | A user-requested review of a bounded familiar plan when the path is otherwise managed. |
| Default strict familiar review | `gpt-5.6-luna` at `max` | The plan needs a strict or high-assurance verdict, but the repository, domain, and subsystem interactions are familiar and no high-consequence boundary selects Sol. |
| Bounded breadth review | `gpt-5.6-terra` at `xhigh` | An otherwise bounded plan depends on an unfamiliar framework, protocol, language, legacy system, or several layers whose interaction is the main challenge. |
| Strict breadth or cross-layer review | `gpt-5.6-terra` at `max` | A strict plan needs both broad priors and difficult synthesis across layers or independent subsystems, without a high-consequence boundary that selects Sol. |
| High-consequence review | `gpt-5.6-sol` at `xhigh` | The verdict must validate security, authentication, permissions, destructive or data migration safety, concurrency correctness, or another externally consequential boundary. |
| Critical review | `gpt-5.6-sol` at `max` | The verdict is critical, explicitly requests critical assurance, or high-risk reasoning remains unresolved after Sol `xhigh`. |

When several lanes apply, consequence overrides breadth, and breadth overrides the familiar-domain lane. Choose once from evidence available before dispatch. A strict label raises a familiar review from Luna `xhigh` to Luna `max`; it does not by itself require Terra or Sol.

Spawn one fresh reviewer with `fork_context: false`. Immediately before spawning, announce the selected model and effort plus the breadth, depth, or consequence reason for any lane above Luna `xhigh`. Leave `service_tier` unset unless the user explicitly requests it.

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

## Agent continuity

Before closing a completed worker or reviewer, inspect all remaining approved work and likely
confirmation passes. A completed turn is not a reason to close an agent.

- Keep the same worker open when a later item directly depends on its accepted work and overlaps the same files, behavior, or subsystem. Inspect and accept the prior item first, then use `send_input` with a separate bounded contract.
- Keep a reviewer open while valid blocking findings may require a focused confirmation. Close it only after its verdict is accepted and no material confirmation remains. A later review that requires independence must use a fresh reviewer.
- Do not use `resume_agent` for managed continuity. In the current runner, the first turn after close and resume can inherit the parent model and reasoning effort, while `resume_agent` provides no model or effort override. Once an agent is closed, spawn a fresh agent with an explicitly announced lane or take the work local.
- Start a fresh worker when independence matters, the prior worker failed or worked outside scope, the ownership boundary is unrelated, or a material risk change requires a different model. Record the reason when the overlap would otherwise favor reuse.
- Keep tightly coupled edits to the same hot files local when the main agent already holds the integration context or worker handoff would cost more than implementation. Do not make a fresh worker rediscover an accepted adjacent slice.

Keep an agent open whenever foreseeable later work will reuse its context. Close it only when no
planned reuse or focused confirmation remains, or when a fresh/local lane is already justified.

## Worker liveness and waits

Give coding workers an action-oriented start: inspect the named boundary, perform at most one bounded discovery pass, then edit and run the stated checks. If the contract still does not identify an implementation path, require a blocker report instead of open-ended exploration.

Call `wait_agent` with the active worker ID in `targets` and `timeout_ms: 1500000`. `wait_agent` returns as soon as the worker finishes, so the 25-minute timeout is only an upper bound and does not delay completed work. Await the call and do nothing else while it is pending: no progress commentary, status polling, repository probes, context rereading, or side work. If it times out while the worker is still running, repeat the same call with `timeout_ms: 1500000`; never omit the timeout or use an escalating sequence.

After dispatch:

1. Treat runner status, worker messages, and the final notification as the liveness evidence. Never infer progress or a stall from file modification times, diff size, process listings, or repeated repository probes.
2. Pause parent work while the coding worker runs. Do not reread its context, inspect its owned files, research later items, map the next slice, or invent other work to fill the wait. Handle only user steering, a hard stop, or a material external event until the worker returns.
3. Call `wait_agent` with `timeout_ms: 1500000`. It returns immediately when the worker finishes; the timeout is only the upper bound. Always set this value and never rely on the default or escalate through shorter waits. Await the call without doing other work. If it times out while the worker is still running, repeat the same call. Prefer the final notification over status polling. If an outer executor yields before the inner wait completes, resume that same wait without analysis, commentary, or repository probes. Do not publish an update merely because the wait timed out.
4. Treat the lane as stalled only after a runner error or `not_found`, an explicit worker blocker, a user or dependency change, or an explicit task timeout/budget. Quiet output and unchanged files are not stall evidence.
5. On a concrete stall, make one recovery attempt: reuse the addressable worker with a narrower action-first contract when its work is salvageable, otherwise close it. If that attempt does not converge, reslice or let the main agent implement locally. Do not run repeated interrupt-and-poll cycles.

Goal mode preserves the workflow across waits; it does not authorize busy waiting or filesystem surveillance.

## Review routing

Use the main agent's integration review for normal managed work. Use a fresh implementation reviewer only at a boundary with high risk. Start bounded implementation and quality reviewers with Luna at `high`; use Luna `xhigh` only when the verdict requires material ambiguity resolution or coupled cross-subsystem reasoning, and raise Luna to `max` only for the demanding bounded lane. Start cross-layer reviewers with Terra at `xhigh` and raise Terra to `max` when needed. Terra `high` and Sol `high` are knowledge overrides, not generic review escalations. Use Sol at `xhigh` for high-risk review and Sol at `max` for critical review. Independent plan review follows the dedicated table above; do not apply the Luna `high` bounded-review default or run serial reviewer escalation. The `managed-quality` phase owns final quality reviewer routing.

Freeze the artifact under review and record reviewer identity when material fixes may need confirmation. If the artifact changes materially before the verdict arrives, treat the verdict as stale. Reuse the same reviewer only when material fixes need confirmation.

Record the review verdict and material evidence in `checklist.md`. Do not create a separate review file unless the user explicitly requests it or an external handoff cannot use the checklist and final response.

If a required reviewer is unavailable, let the main agent perform the review and record the caveat. Stop only when the user or governing policy requires independence.
