# Agent Management

Read this before spawning or coordinating subagents.

## Authorization

Spawn subagents only when the user explicitly asks for subagents, delegation, parallel agents, a swarm, or to run this managed workflow. Planning artifacts alone do not authorize spawning.

A request for `$managed-workflow`, `$managed-plan`, or a reviewed managed workflow plan authorizes exactly one independent plan reviewer plus same-thread re-review when the selected plan review level requires it. It does not authorize implementation workers, slice reviewers, final quality reviewers, parallel agents, or larger workgroups until the relevant workflow phase and user gate allow them.

Use subagents only when the current environment exposes a subagent runner. Do not claim that a local script can call subagent tools.

Default limits are 4 concurrent agents and 12 total agents per workflow. Treat higher counts as a hard stop unless the plan explicitly sets a bounded limit and the user authorizes it.

## Runner Mapping

If subagent tools are not already visible, use tool discovery for multi-agent or subagent tools before marking review unavailable. In Codex environments with `multi_agent_v1`, use:

- `spawn_agent` for fresh plan reviewers, slice reviewers, final quality reviewers, explorers, and workers.
- `send_input` for same-thread plan re-review and same-thread slice re-review.
- `wait_agent` only when the result is needed for the next critical-path step.
- `close_agent` after a completed agent's result is recorded and no further re-review is needed.

Record each reviewer or worker id, nickname if available, role, and assigned slice in `checklist.md`. For same-thread re-review, reuse the recorded id rather than spawning a fresh reviewer.

## Delegation Rules

- Keep immediate blocking work local; delegate bounded sidecar work.
- Use explorer/research lanes for specific codebase or external-source questions.
- Use worker lanes only for disjoint implementation ownership with explicit files or modules.
- Choose the worker isolation model deliberately. Use runner-provided isolated workspaces when available, use git worktrees when the manager decides local branch isolation is needed, and allow shared-tree edits only for sequential or strictly non-overlapping work. Workers never commit to the manager's current branch; the manager imports and commits. See `managed-implement` Worker Integration.
- For worker lanes, require a final report suitable for `results/<slice-id>.md` with changed paths, verification evidence, blockers, and remaining risks.
- Tell workers they are not alone in the codebase, must not revert others' edits, and must adapt to concurrent changes.
- Omit model overrides unless an override is explicitly needed. If overriding, use the strongest available reasoning model plus high reasoning effort, not pseudo-model names.
- Use the same reviewer/thread for re-review when the workflow requires continuity.

## Review Lanes

- Plan reviewer: fresh independent reviewer, strongest available reasoning model with high effort when model selection is available.
- Plan re-review: same reviewer/thread, prior review notes included.
- Slice reviewer: fresh reviewer per slice, medium effort unless risk warrants more.
- Final quality reviewer: fresh reviewer lane focused on maintainability and simplification, not execution.

## Management Style

Manage agents by contract, not interruption. Give each agent a bounded objective, ownership, expected output, verification, and stop conditions, then let it run.

Do not interrupt, restart, or redirect an agent merely because it is quiet or taking longer than expected. Wait for completion unless a hard stop is reached, the user redirects, the agent reports a blocker, a dependency changes, or the run exceeds an explicit timeout or budget.

Use status checks sparingly. If a check is needed, ask only for current status and blockers; do not add scope mid-slice. The manager owns sequencing, integration, final verification, and user communication.
