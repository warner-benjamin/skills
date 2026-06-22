---
name: managed-quality
description: Run the final managed workflow quality phase after implementation passes initial verification, with a strict maintainability and simplification review, behavior-preserving cleanup slices, and re-verification. Use when the user explicitly invokes $managed-quality, asks for final simplification/refactoring after a managed workflow, or a multi-slice managed code workflow reaches the final quality gate. Do not use for ordinary lightweight code review.
---

# Managed Quality

Perform the final quality gate for a managed workflow. This phase catches structural drift from multi-agent or multi-slice implementation and drives behavior-preserving simplification before final completion.

## Shared Setup

`PHASE_SKILL_DIR` is the absolute directory of this `SKILL.md`. Resolve `WORKFLOW_SKILL_DIR` before reading shared references: a user-provided `managed-workflow` path if given, else the sibling `managed-workflow` directory next to `PHASE_SKILL_DIR`. Always use an absolute path, never `../managed-workflow/...` relative to the shell cwd.

Read:

- `$WORKFLOW_SKILL_DIR/references/workflow-contract.md`
- `$WORKFLOW_SKILL_DIR/references/hard-stops.md` before risky or ambiguous operations
- `$WORKFLOW_SKILL_DIR/references/verification.md` before re-verification
- `$PHASE_SKILL_DIR/references/quality-bar.md`
- `$WORKFLOW_SKILL_DIR/references/agents.md` if using a reviewer agent or cleanup worker
- `managed-implement/references/slice-artifacts.md` if creating a delegated or substantial cleanup slice

## Preconditions

Before starting, inspect `plan.md`, `checklist.md`, `final-report.md`, and the final implementation diff. Do not run this phase until:

- `Implementation status` is `complete`.
- `Initial verification` is `passed`.
- `Final quality review` is `pending` or explicitly requested by the user.

If the workflow is docs-only, research-only, a single low-risk slice, or explicitly skipped, mark `Final quality review: not-required` with the reason and stop.

## Quality Loop

1. Prepare the final-quality context: final diff, plan, accepted slice results, verification evidence, and quality bar. This prep is not an independent main-agent review when a reviewer lane will run.
2. Ask a fresh reviewer lane for strict maintainability and simplification findings when reviewer agents are available, then wait. Don't run a parallel main-agent quality review, draft findings, or re-audit the diff while the reviewer is active.
3. If reviewer agents are unavailable, do the review locally, record `Reviewer: unavailable; local final-quality review used` in `checklist.md`, and save the verdict to `reviews/final-quality-review.md`.
4. Save reviewer findings to `reviews/final-quality-review.md` when a reviewer lane ran.
5. Treat valid blocking findings as a behavior-preserving cleanup slice (`slices/final-quality-cleanup.md`, `results/final-quality-cleanup.md`).
6. Implement the smallest cleanup that materially reduces complexity and preserves behavior.
7. Re-run relevant targeted checks and broad verification.
8. Ask the same reviewer/thread for re-review when a reviewer lane ran and material cleanup changed.
9. Update `checklist.md` with final quality status, cleanup slice, re-verification evidence, and final verification.
10. Update `final-report.md` with the cleanup summary, verification evidence, completion proof, and remaining risks.

This is a reviewer lane first, not an excuse to invent new scope. Cleanup must stay behavior-preserving and aligned with the reviewed plan.

## Completion Bar

Don't approve final completion when there's a clear structural regression, avoidable branching growth, wrong-layer logic, duplicate canonical helper, needless wrapper/cast/optionality churn, unjustified file-size growth, brittle orchestration, or an obvious simpler behavior-preserving design.

Don't block on cosmetic nits when larger structural issues are absent. Prefer a small number of high-conviction findings over a long list of style comments.
