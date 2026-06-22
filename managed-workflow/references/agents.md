# Agent Management

Read this before spawning or coordinating subagents.

## Authorization

Spawn subagents only when the user explicitly asks for subagents, delegation, parallel agents, a swarm, or this managed workflow. Planning artifacts alone don't authorize spawning.

A `$managed-workflow`/`$managed-plan` request authorizes the plan-review lanes the selected review level needs, plus same-thread re-review — not implementation workers, slice reviewers, final-quality reviewers, or larger workgroups until the relevant phase and implementation approval allow them.

Spawn only when the environment exposes a subagent runner; never claim a local script can call subagent tools.

Default limits: 4 concurrent, 12 total per workflow. Higher counts are a user-visible escalation — proceed only with a bounded plan limit and user authorization.

## Runner Mapping

If subagent tools aren't visible, use tool discovery before marking review unavailable. Use the runner's native operations to spawn reviewers/workers, send same-thread re-review input, wait only when a result is on the critical path, and close agents after recording their result.

Record each reviewer/worker id, nickname, role, and assigned slice in `checklist.md`. For same-thread re-review, reuse the recorded id rather than spawning fresh.

## Delegation Rules

- Keep immediate blocking work local; delegate bounded sidecar work.
- Use explorer/research lanes for specific codebase or external-source questions.
- Use worker lanes only for disjoint ownership with explicit files or modules.
- Choose the isolation model deliberately: runner-provided workspaces when available, git worktrees when local branch isolation is needed, shared-tree edits only for sequential or strictly non-overlapping work. Workers never commit to the integration branch — the main agent imports and commits (see `managed-implement/references/delegated-work.md`).
- Require each worker lane to return a `results/<slice-id>.md` report: changed paths, verification evidence, blockers, remaining risks.
- Tell workers they aren't alone in the codebase: don't revert others' edits, adapt to concurrent changes.
- Omit model overrides for main-agent local coding; when spawning a worker/reviewer, pick the lowest level that fits the slice risk (see Agent Level Routing).
- Reuse the same reviewer/thread for re-review when continuity is required.

## Agent Level Routing

Use agent levels to control cost when a worker or reviewer lane is actually spawned. Do not spawn an agent just because a level exists.

| Level | Use for | Avoid for |
| --- | --- | --- |
| `gpt-5.4 mini` | Easy bounded tasks with explicit files, obvious tests, and little judgment: mechanical edits, tiny fixtures, simple config, narrow bug fixes, straightforward UI copy or prop wiring. | Documentation synthesis, unclear contracts, cross-layer behavior, migrations, auth, concurrency, or any task needing much internal planning. |
| `gpt-5.5 low` | Easy-medium work, documentation, UI implementation, and multi-file changes when the plan is explicit and little internal planning is required. Good for focused refactors, predictable generated-output follow-up, small route/component changes, and low-risk reviewer passes. | Ambiguous architecture, high-risk data/auth/API work, hard debugging, or final quality. |
| `gpt-5.5 medium` | Default for implementation workers and ordinary slice reviewers when code judgment, tests, integration, or moderate planning is needed. | Very small mechanical tasks where mini/low is clearly enough, or complex/high-risk work needing deeper reasoning. |
| `gpt-5.5 high` | Complex or high-risk work: plan review, final quality review, schema/data migrations, auth/permissions, concurrency/background jobs, generated API/client contracts, cross-layer product behavior, security-sensitive changes, or a slice that failed once and needs deeper reasoning. | Routine implementation where medium or low is enough. |

If an exact model is unavailable, use the closest at the same tier and record the substitution in `checklist.md`. Escalate a lane's level only after a concrete blocker, failed review/checks, or newly discovered risk justifies the cost.

## Review Lanes

- Plan reviewer: fresh independent reviewer, `gpt-5.5 high` tier when model selection is available.
- Plan re-review: same reviewer/thread, prior review notes included.
- Slice reviewer: risk-gated by subsystem boundary, medium effort unless risk warrants more. Reuse the same reviewer for adjacent sequential slices when continuity helps; use a fresh reviewer when independence matters, the risk boundary changes, a prior reviewer missed a material issue, or the plan/checklist requires it.
- Final quality reviewer: fresh `gpt-5.5 high` lane focused on maintainability and simplification, not execution.

## Reviewer Budget

Default: at most one fresh implementation reviewer per major subsystem or risk boundary, plus same-thread re-reviews. Main-agent review is fine for docs, env examples, tiny CLI/test-only additions, and mechanical follow-up after green checks. Exceed the default only when the plan sets a higher bar, the user asks for stricter review, or the checklist records why independence is worth the cost.

## Management Style

Manage agents by contract, not interruption. Give each a bounded objective, ownership, expected output, artifact path, verification, and stop conditions, then let it run. For persistence rules, use the relevant phase reference (implementation slices: `managed-implement/references/slice-artifacts.md`).

Don't interrupt a running agent for being slow or quiet. Wait for completion unless: a hard stop, user redirect, reported blocker, changed dependency, or an exceeded timeout/budget.

When a gate calls for multiple independent reviewers, start all required lanes first (e.g. Codex and Claude plan reviews), then stop reviewing in the main thread and wait. While reviewers run, don't self-review, draft findings, re-audit the diff/plan, or spend tokens anticipating comments — use the wait only for orchestration (recording ids, required tool calls, an actual blocker/redirect).

Use status checks sparingly: ask only for current status and blockers, never add scope mid-slice. In delegated work, the main agent as manager owns sequencing, integration, final verification, and user communication.
