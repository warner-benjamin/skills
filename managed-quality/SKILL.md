---
name: managed-quality
description: Run the final managed workflow quality phase after implementation passes initial verification, with a strict maintainability and simplification review, behavior-preserving cleanup slices, and re-verification. Use when the user explicitly invokes $managed-quality, asks for final simplification/refactoring after a managed workflow, or a multi-slice managed code workflow reaches the final quality gate. Do not use for ordinary lightweight code review.
---

# Managed Quality

Perform the final quality gate for a managed workflow. This phase catches structural drift from multi-agent or multi-slice implementation and drives behavior-preserving simplification before final completion.

## Shared Setup

Let `PHASE_SKILL_DIR` mean the absolute directory containing this `SKILL.md`. Resolve `WORKFLOW_SKILL_DIR` before reading shared references:

1. Use a user-provided `managed-workflow` path when given.
2. Otherwise use the sibling `managed-workflow` directory next to `PHASE_SKILL_DIR`.
3. Use an absolute path. Do not read `../managed-workflow/...` relative to the user's shell cwd.

Read:

- `$WORKFLOW_SKILL_DIR/references/workflow-contract.md`
- `$WORKFLOW_SKILL_DIR/references/hard-stops.md` before risky or ambiguous operations
- `$WORKFLOW_SKILL_DIR/references/verification.md` before re-verification
- `$PHASE_SKILL_DIR/references/quality-bar.md`

Read `$WORKFLOW_SKILL_DIR/references/agents.md` if using a reviewer agent or cleanup worker.
Read the sibling `managed-implement/references/slice-artifacts.md` if creating a delegated or substantial cleanup slice.

## Preconditions

Before starting, inspect `plan.md`, `checklist.md`, `final-report.md`, and the final implementation diff. Do not run this phase until:

- `Implementation status` is `complete`.
- `Initial verification` is `passed`.
- `Final quality review` is `pending` or explicitly requested by the user.

If the workflow is docs-only, research-only, small one-shot, or explicitly skipped, mark `Final quality review: not-required` with the reason and stop.

## Quality Loop

1. Review the final diff against the plan, accepted slice results, and quality bar.
2. Ask a fresh reviewer lane for strict maintainability and simplification findings when reviewer agents are available.
3. Save findings to `reviews/final-quality-review.md`.
4. Treat valid blocking findings as a behavior-preserving cleanup slice with `slices/final-quality-cleanup.md` and `results/final-quality-cleanup.md`.
5. Implement the smallest cleanup that materially reduces complexity and preserves behavior.
6. Re-run relevant targeted checks and broad verification.
7. Ask the same reviewer/thread for re-review when material cleanup changes were made.
8. Update `checklist.md` with final quality status, cleanup slice, re-verification evidence, and final verification status.
9. Update `final-report.md` with the cleanup summary, verification evidence, completion proof, and remaining risks.

This is a reviewer lane first, not an excuse to invent new scope. Cleanup must remain behavior-preserving and aligned with the reviewed plan.

## Completion Bar

Do not approve final completion when there is a clear structural regression, avoidable branching growth, wrong-layer logic, duplicate canonical helper, needless wrapper/cast/optionality churn, unjustified file-size growth, brittle orchestration, or an obvious simpler behavior-preserving design.

Do not block on cosmetic nits when larger structural issues are absent. Prefer a small number of high-conviction findings over a long list of style comments.
