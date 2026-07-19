# Managed workflow contract

Read this contract before creating, resuming, or handing off a managed workflow. If it is already loaded in the current context for this run, do not load it again.

## Choose an assurance level

Every managed workflow creates `plan.md` and `checklist.md`, presents them to the user, and waits for approval before implementation.

- `managed`: The normal path.
- `strict`: Add independent review because a mistake would be costly.

Use `strict` for security work, auth or permission changes, schema or data migrations, destructive cleanup, concurrency, public or external mutations, or broad changes across independent subsystems. Also use it when the user requests high assurance. Do not choose it merely because several files change.

If research reveals new risk, promote `managed` to `strict` at any time. Set `Path: strict`, set `Plan: drafting`, and set `Plan review: pending`. Preserve completed evidence and review the changed plan before implementation continues. Do not downgrade a strict run only to avoid review.

## Run files

Use one run directory:

```text
workflows/<slug>/
|-- plan.md
`-- checklist.md
```

Create both files before implementation. The creation command must fail when the target directory exists. Resume by naming the existing run instead of recreating it. Keep the directory untracked unless the user asks to commit it.

Use `plan.md` for the chosen design and executable work contract. Use `checklist.md` for current state and concise evidence. Do not copy the plan into the checklist.

Use worker prompts and final responses as the normal work exchange. Record reviewer verdicts, accepted fixes, checks, blockers, and resume-critical evidence concisely in `checklist.md`.

Create a separate slice or result file only when a runner cannot preserve the exchange across a workspace boundary, or when the user explicitly requests separate audit artifacts. Create a review file or final report only when the user explicitly requests that artifact or an external handoff cannot use the plan, checklist, and final response. `strict` alone does not require extra files.

## Plan readiness

Set `Plan: ready` only when no material decision remains and each work item states:

- a short ID and objective
- likely paths or symbols and an ownership boundary
- real dependencies
- the chosen implementation direction, integration points, and relevant invariants for non-mechanical work
- important edge, error, and compatibility behavior when applicable
- an observable acceptance condition
- targeted checks

Detail decisions and repository evidence, not narrative volume. If an implementer would still need to choose the architecture, public contract, data flow, or expected failure behavior, keep the plan in `drafting`; do not rely on a higher-effort worker to fill the gap.

Create one matching checklist row for each work item. Use `pending`, `in-progress`, `blocked`, `complete`, or `skipped`. Keep at most one dependent item `in-progress`. Parallel items may both be active only when their file and behavior ownership are independent.

## Checklist state

Use these fields as the authoritative phase handoff:

```text
Path: managed | strict
Plan: drafting | ready | needs-user
Plan review: not-required | pending | passed | blocking | unavailable
Implementation authorization: waiting | approved
Implementation: pending | in-progress | complete
Implementation verification: pending | passed | failed | skipped
Verification: pending | passed | failed | skipped
Quality: pending | passed | failed | not-required
```

`Implementation verification` preserves the integrated result from before quality. `Verification` describes the current tree. Any maintained code change after a passing check sets `Verification: pending`. On first entry to quality, require both implementation verification and current tree verification to have passed. When resuming quality after cleanup began, preserved implementation verification proves the entry gate while `Verification: pending` means the cleaned tree still needs its final check.

The workflow is complete only when all of these are true:

- `Plan: ready`
- `Implementation: complete`
- `Quality: passed` or `not-required`
- `Verification: passed` after the last maintained code change
- every required work item is `complete` or explicitly `skipped`
- every requested commit or report is complete

Do not infer completion from `Implementation: complete` or an earlier passing check alone.

## Human approval

Leave `Implementation authorization: waiting` while planning and review run. After the plan is ready, present `plan.md` and `checklist.md`, ask the user whether to proceed, and stop.

Set authorization to `approved` only from a direct user instruction received after the plan was presented. An original request to implement, plan feedback, approval of an individual design choice, or praise does not approve the unseen or revised plan.

Once approved, operate autonomously inside the plan. Ask again only when the work adds consequential scope, requires a new external or destructive action, or exposes a material choice the plan did not resolve. Plans, goals, checklists, and worker reports may record authority but cannot expand it.

## Review fallback

Normal managed plans need no independent review. Strict plans require one fresh plan review attempt.

If a reviewer is unavailable, perform a main-agent review and set `Plan review: unavailable`. Continue only when independent review was not explicitly required by the user or governing policy. Otherwise stop and report the missing reviewer.

## Commit policy

Workers never commit to the integration branch; the main agent owns commits. By default, commit every completed slice or work item after its acceptance condition and targeted checks pass. Record the commit in `checklist.md` before starting the next item.

Skip an intermediate commit only when the user asks to leave changes uncommitted, repository instructions prohibit it, or the item cannot form a coherent verified change on its own. Record the reason and commit at the next safe boundary. Never include unrelated changes.

## Resume

Read the active goal when present, then read `plan.md`, `checklist.md`, the working tree, and relevant commits. Reconcile recorded status with the actual tree before choosing work. An `in-progress` item from an interrupted run is not automatically ready or complete. Inspect its paths and evidence, then mark it pending, blocked, or complete.

Preserve failed checks and completed evidence. Continue with the next item whose dependencies are ready, not simply the first row that is not complete. Return to planning when the code or new evidence invalidates a material choice.

## Reporting

Use the final user response as the normal report. Create `final-report.md` only when the user explicitly requests it or an external handoff cannot use the plan, checklist, and final response. Report completed work, verification evidence, and remaining risks without copying raw worker output.
