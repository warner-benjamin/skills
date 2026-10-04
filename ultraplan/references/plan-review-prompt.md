# Independent plan review

Supply the plan path, intended outcome, relevant evidence, and settled decisions. Do not prescribe a verdict.

> Review [plan path] for [user outcome] using [governing sources] and [settled decisions].
> Verify consequential claims against evidence, including exact dependency versions where relevant.
>
> Assess correctness, executability, and simplicity across the whole user workflow, including consumers, setup, recovery, and delivery.
> Verify that tasks have clear dependencies and that acceptance checks prove the requested outcome.
> Identify the smallest representative scenario that can expose an integration error early.
> Keep optional ideas outside required execution scope.
>
> Challenge unsupported assumptions, unnecessary mechanisms, and custom implementations that suitable existing dependencies can simplify.
> Consider established, maintained packages with evidence of production use for solved problems beyond existing project dependencies.
> Require justification for consequential custom code when a suitable package exists, accounting for fit and integration cost.
> For a blocking simplification, state the concrete consequence, smaller alternative, and behavior it preserves.
> Do not block on style, wording, or theoretical improvements without demonstrated impact.
>
> Remain read-only and do not spawn agents. Return batched findings with source anchors, consequences, and the smallest useful corrections.
> Separate blockers from advisory refinements. Report evidence gaps that affect readiness.
>
> On rereview, inspect changed decisions and affected dependencies or acceptance criteria.
> Carry forward valid evidence for unchanged portions. Expand the scope when changes invalidate earlier conclusions.
> Do not reconstruct unchanged research or rerun checks without a specific reason.
> Return `approved` only when the whole plan has no blockers to execution. Otherwise, return `not ready` with exact gaps.
