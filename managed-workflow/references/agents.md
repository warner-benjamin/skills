# Agent Management

Read this before spawning or coordinating subagents.

## Authorization

Spawn subagents only when the user explicitly asks for subagents, delegation, parallel agents, a swarm, or to run this managed workflow. Planning artifacts alone do not authorize spawning.

A request for `$managed-workflow`, `$managed-plan`, or a reviewed managed workflow plan authorizes the independent plan review lanes required by the selected review level, plus same-thread re-review when that level requires it. It does not authorize implementation workers, slice reviewers, final quality reviewers, or larger workgroups until the relevant workflow phase and implementation approval allow them.

Use subagents only when the current environment exposes a subagent runner. Do not claim that a local script can call subagent tools.

Default limits are 4 concurrent agents and 12 total agents per workflow. Treat higher counts as a user-visible escalation: proceed only when the plan sets a bounded limit and the user authorizes it.

## Runner Mapping

If subagent tools are not already visible, use tool discovery for multi-agent or subagent tools before marking review unavailable. Use the runner's native operations for spawning reviewers/workers, sending same-thread re-review input, waiting only when a result is on the critical path, and closing completed agents after their result is recorded.

Record each reviewer or worker id, nickname if available, role, and assigned slice in `checklist.md`. For same-thread re-review, reuse the recorded id rather than spawning a fresh reviewer.

## Delegation Rules

- Keep immediate blocking work local; delegate bounded sidecar work.
- Use explorer/research lanes for specific codebase or external-source questions.
- Use worker lanes only for disjoint implementation ownership with explicit files or modules.
- Choose the worker isolation model deliberately. Use runner-provided isolated workspaces when available, use git worktrees when the main agent decides local branch isolation is needed, and allow shared-tree edits only for sequential or strictly non-overlapping work. Workers never commit to the integration branch; the main agent imports and commits. See `managed-implement` Worker Integration.
- For worker lanes, require a final report suitable for `results/<slice-id>.md` with changed paths, verification evidence, blockers, and remaining risks.
- Tell workers they are not alone in the codebase, must not revert others' edits, and must adapt to concurrent changes.
- Omit model overrides for main-agent local coding work. When spawning a worker or reviewer, choose the lowest agent level that fits the slice risk from Agent Level Routing below.
- Use the same reviewer/thread for re-review when the workflow requires continuity.

## Agent Level Routing

Use agent levels to control cost when a worker or reviewer lane is actually spawned. Do not spawn an agent just because a level exists.

| Level | Use for | Avoid for |
| --- | --- | --- |
| `gpt-5.4 mini` | Easy bounded tasks with explicit files, obvious tests, and little judgment: mechanical edits, tiny fixtures, simple config, narrow bug fixes, straightforward UI copy or prop wiring. | Documentation synthesis, unclear contracts, cross-layer behavior, migrations, auth, concurrency, or any task needing much internal planning. |
| `gpt-5.5 low` | Easy-medium work, documentation, UI implementation, and multi-file changes when the plan is explicit and little internal planning is required. Good for focused refactors, predictable generated-output follow-up, small route/component changes, and low-risk reviewer passes. | Ambiguous architecture, high-risk data/auth/API work, hard debugging, or final quality. |
| `gpt-5.5 medium` | Default for implementation workers and ordinary slice reviewers when code judgment, tests, integration, or moderate planning is needed. | Very small mechanical tasks where mini/low is clearly enough, or complex/high-risk work needing deeper reasoning. |
| `gpt-5.5 high` | Complex or high-risk work: plan review, final quality review, schema/data migrations, auth/permissions, concurrency/background jobs, generated API/client contracts, cross-layer product behavior, security-sensitive changes, or a slice that failed once and needs deeper reasoning. | Routine implementation where medium or low is enough. |

If a requested exact model is unavailable, use the closest available model at the same capability/effort tier and record the substitution in `checklist.md`. Escalate a running lane's level only after a concrete blocker, failed review, failed checks, or newly discovered risk justifies the extra cost.

## Review Lanes

- Plan reviewer: fresh independent reviewer, use the `gpt-5.5 high` tier when model selection is available.
- Plan re-review: same reviewer/thread, prior review notes included.
- Slice reviewer: risk-gated by subsystem boundary, medium effort unless risk warrants more. Reuse the same reviewer for adjacent sequential slices when continuity reduces repeated context; use a fresh reviewer when independence matters, the risk boundary changes, a prior reviewer missed a material issue, or the plan/checklist explicitly requires it.
- Final quality reviewer: fresh `gpt-5.5 high` reviewer lane focused on maintainability and simplification, not execution.

## Reviewer Budget

Default to no more than one fresh implementation reviewer per major subsystem or risk boundary, plus same-thread re-reviews. Main-agent review is acceptable for docs, env examples, tiny CLI or test-only additions, and mechanical follow-up slices after green checks. Escalate above the default only when the plan sets a higher bar, the user asks for stricter review, or the checklist records why a fresh independent reviewer is worth the added cost.

## Management Style

Manage agents by contract, not interruption. Give each agent a bounded objective, ownership, expected output, artifact path, verification, and stop conditions, then let it run. Use the relevant phase artifact reference for persistence rules; for implementation slices, use `managed-implement/references/slice-artifacts.md`.

Do not interrupt, restart, or redirect an agent merely because it is quiet or taking longer than expected. Wait for completion unless a hard stop is reached, the user redirects, the agent reports a blocker, a dependency changes, or the run exceeds an explicit timeout or budget.

When a gate calls for multiple independent reviewers, start all required independent review lanes first, such as GPT/Codex and Claude plan reviews, then pause review work in the main thread and wait patiently for the reviewer results. Do not run a parallel main-agent review, draft findings, re-audit the same diff or plan, or spend tokens anticipating likely reviewer comments while reviewers are active. Use the wait only for necessary orchestration, such as recording reviewer ids, waiting on required tool calls, or handling an actual blocker/user redirect.

Use status checks sparingly. If a check is needed, ask only for current status and blockers; do not add scope mid-slice. In delegated work, the main agent acting as manager owns sequencing, integration, final verification, and user communication.
