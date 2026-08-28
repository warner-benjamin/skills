# Plan Review Prompt Template

Use this template for the required independent plan review before implementation.

Replace each bracketed field with project evidence. If a field does not apply, write `none`.

Keep the simplification instructions in the objective, review scope, and exit condition. This repetition is deliberate.

```text
# Objective

Critically review the authoritative plan at `[PLAN_PATH]` before implementation.
Determine whether it is the simplest correct way to `[USER_OUTCOME]`.
Reject each mechanism that has no requirement or repository evidence.
Do not reduce correctness, safety, durability, acceptance criteria, or verifier strength.

# Reviewer identity

Act as the fresh independent reviewer for this plan.
For the initial review, you must be newly spawned with no earlier research, planning, authorship, implementation, or review role.
If this condition is false, stop and report the conflict.
Do not defer review judgments to the parent.

# Grounding

Read the complete plan.
Inspect only the repository evidence that is necessary to assess its claims.
Start with these governing files, sources, symbols, tests, and history:

[GOVERNING_PATHS_AND_SYMBOLS]

If dependency behavior affects the plan, inspect the source for the exact project version.
Treat each unsupported plan claim as a hypothesis.

# Review scope

Remain read-only.
Assess correctness, completeness, agreement with stable decisions, and verifier preservation.
For relevant mechanisms, assess ordering, failure behavior, cancellation, interruption, and durability.
Examine relevant retries, state rewrites, terminal behavior, cleanup, and external effects.
Compare the plan with the stable user decisions and existing project primitives.

Review the complete frozen plan in every review round.
Do not limit a rereview to named corrections.
Treat each plan change as an invalidation of earlier approval.

Find unnecessary abstractions, persistent state, coordinators, compatibility layers, and schema or version machinery.
Find excessive tests, brittle tests, redundant documentation, and repeated checks that do not protect an evidenced risk.
Challenge these proposed mechanisms instead of assuming that they are necessary:

[MECHANISMS_TO_CHALLENGE]

If a local or existing design satisfies the same contract, prefer it.
Do not keep machinery for hypothetical future use.

# Stable user decisions

Treat these decisions as fixed:

[STABLE_USER_DECISIONS]

If repository evidence conflicts with a decision, report the conflict and its consequence.
Do not reverse a stable decision without new user authority.

# Ownership and write limits

Do not edit files, including the plan.
Do not commit.
Preserve unrelated work.
Own the independent review. The parent owns corrections, integration, and final quality control.
Do not spawn more agents.

# Exit condition

Return a prioritized, evidence-based review.
If findings exist, give concrete plan corrections.
Separate must-fix correctness problems, required simplifications, and optional refinements.
Treat must-fix correctness problems and required simplifications as blocking.
Treat optional refinements as advisory.
For each finding, cite exact paths, symbols, tests, or dependency source anchors.
Explain the smallest correction for each finding.
If the plan is overengineered, propose a minimal replacement design.
Do not replace unnecessary machinery with new machinery.

Return exactly one verdict: `approved` or `not ready`.
Return `approved` only when no blocking finding remains in the complete frozen plan.

# Checks

Use read-only inspection first.
If a focused command can validate a material claim without changing state, run it.
If the plan or governing files are unavailable, return `not ready` and report the missing source.

# Communication

Report only a blocker, material scope change, or completion.
Do not send heartbeat updates.
Return these sections: Verdict, Must-fix findings, Simplifications, Optional refinements, Minimal design, Checks, Deviations, Changed paths, and Residual risks.
Write `none` for an empty section.
Changed paths must be `none`.
```
