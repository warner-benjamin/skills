# Goal mode

Use goal mode to keep managed implementation durable across long work, waits, compaction, and the final quality phase.

## Fit

For a `managed` or `strict` run, activate goal mode when persistence is useful because any of these apply:

- implementation is likely to span turns or context compaction
- a long wait, repeated repair loop, or parallel worker is expected
- the final verifier cannot run promptly
- interruption would make the checklist alone an awkward continuation point

Otherwise skip goal mode. Do not activate when the user asked only for a plan or while implementation authorization is waiting.

## Activate

After the plan is ready and implementation is authorized, resume the active goal for this run when one exists. Otherwise call `create_goal` before the first edit. Do not only draft an objective, and do not create a duplicate goal. Do not set a token budget unless the user requests one.

Use a compact objective that names the requested outcome, the absolute `plan.md` and `checklist.md` paths, the final verifier, and this completion condition:

```text
Complete the requested outcome by executing and maintaining <plan path> and <checklist path>. Keep their work state and evidence current. Continue while a safe relevant step remains. Treat only an external condition that prevents meaningful progress as a blocker. Finish only after implementation is complete, quality has passed or is not required, verification has passed on the final tree, and every requested commit or extra artifact is complete.
```

Continue implementation after activation. The parent goal owns scope, integration, conflicts, quality, final verification, and completion. Create child goals only when the user explicitly requests goals for subagents.

Goal persistence does not require one turn to remain alive while a worker runs. Follow the shared worker-liveness protocol: avoid polling, rely on final notifications, and resume from durable state when the worker result arrives.

## Maintain and resume

At the start of each resumed turn, read the active goal, plan, checklist, working tree, and relevant commits. Reconcile interrupted work before selecting the next item whose dependencies are ready.

Treat user steering, material new evidence, a failed verifier, and a changed constraint as state update events. Update the plan when the route or acceptance contract changes. Update the checklist when work state, evidence, or the next action changes. Preserve failed checks and completed evidence instead of replacing them with the latest attempt.

Do not mark the goal complete at implementation handoff. `managed-workflow` owns completion after quality, final verification, and any required final commit. Follow the platform goal rules for genuine blockers.
