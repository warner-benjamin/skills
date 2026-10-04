# Nested delegation

Read before permitting a worker to spawn children.

Prefer a flat team. Permit nesting when a worker can manage independent child scopes with less coordination than the parent.
Respect user limits and shared runtime capacity. Do not add a management layer for one tightly coupled decision.
Tell the worker to load and follow [delegate](../SKILL.md) when coordinating children.

Give each child a non-overlapping subset of the worker's scope.
Require each child assignment to finish from supplied context without ongoing communication with other agents.
If work requires shared edits or repeated coordination, keep it with the worker instead of spawning children.
Carry forward authority, write boundaries, invariants, acceptance criteria, and stop conditions.
Establish dependencies before dispatch. Nesting must not expand scope.

The worker remains accountable for integration and delivery to its parent. Child completion is not acceptance at either level.
Escalate beyond the direct parent only when a decision exceeds that parent's authority.

Report child lineage, objective, and selected model/effort to the direct parent after dispatch.
Batch related notices and relay them to the root for a concise user update.
After dispatch, relay only material decisions, blockers, changed interfaces, findings, and handoffs.
