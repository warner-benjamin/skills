# Nested delegation

Read before permitting a worker to spawn children.

Permit nesting when the authorized delegation benefits from a bounded child task, the worker has the tools to manage it and report to its parent, and the runtime has capacity. Respect any user limits on agent count or depth. In the Codex runtime, Luna lacks `send_message`; keep it a leaf worker.

The worker must load the Delegate skill and act as the child's parent. Give the child a non-overlapping subset of the worker's scope, carrying forward authority, write boundaries, invariants, acceptance criteria, and stop conditions. Establish dependencies before dispatch. Nesting must not expand scope or exceed the shared runtime concurrency limit.

The worker must protect active child work, respond to bounded handoffs, wait on events, verify deliverables, and reuse children for corrections. The worker remains accountable to its parent for the full assigned scope; a child completing does not constitute acceptance at either level.

Carry the skill's major-decision guidance into each non-Luna child packet: ask the direct parent through `collaboration.send_message` before making major decisions not already settled by the task packet, with evidence, options, and a recommendation. Resolve routine details locally. Escalate beyond the direct parent only when the decision exceeds that parent's scope or authority; a Luna child returns blocking decisions in its final report.

Include dispatch reporting in every packet that permits nesting: after a successful child spawn, send the direct parent the task lineage, objective, and selected model/effort, or inherited when unknown. Relay this material event to the root, which gives a concise user notice and may combine related dispatches. Do not require hidden runtime metadata or heartbeat reports.
