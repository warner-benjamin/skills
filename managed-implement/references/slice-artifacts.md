# Slice Artifacts

Use durable slice artifacts when work is delegated, crosses a workspace boundary, needs independent review context, or is substantial enough that resume would otherwise lose important state. For a tiny main-agent coding slice, the checklist row, diff, commit, and verification evidence can be enough.

When a worker or reviewer has workspace write access, instruct it to write its report or review artifact directly to the named path. When the runner cannot write to the workflow workspace, the agent should return concise text and the main agent should persist it.

## Slice Prompts

Before delegation, write `slices/<slice-id>.md`. For substantial local slices, write it when it helps review or resume.

The prompt should give the worker or future reviewer enough context to act without inventing core design: objective, relevant `plan.md` design/steps/slice references, files or sources, ownership boundary, dependencies, do/do-not guidance, expected output, verification, review expectation, report path, and commit boundary.

Slice prompts may add local execution context, but must not change the reviewed design. If a slice needs a new design decision, pause and route back to `managed-plan` for a targeted plan update and review.

## Reports

Every worker lane must produce a report saved as `results/<slice-id>.md`. Local reports are useful for substantial slices and optional for tiny main-agent coding slices.

Reports must be actionable, not ceremonial. Include changed paths, workspace or branch when applicable, what changed, verification run and result, blockers, remaining risks, and anything the main agent or reviewer must inspect. Exact field names are not important. Do not accept a vague "done" report as integration-ready.

## Reviews

When a reviewer agent runs, save findings under `reviews/<slice-id>-review.md`. The review should include a verdict plus any critical findings, important non-blocking findings, missing context or unresolved questions, and required fixes.

Review the slice prompt when present, report when present, diff, targeted check evidence, alignment with the plan's `Design`, `Implementation Steps`, and `Execution Slices`, ownership boundary, and unrelated-change risk.

Block commit readiness when the slice:

- changes files outside its ownership without a recorded reason
- skips targeted checks without a credible reason
- lacks required delegated-work artifacts
- diverges from the reviewed design or invents unreviewed core design
- mixes unrelated user or concurrent-agent changes into the slice
- leaves material review findings unfixed and unrejected
- needs a local simplification to preserve correctness, plan alignment, ownership boundaries, or commit safety

After material fixes, ask the same reviewer/thread for re-review when available.

Record clear local simplifications in `checklist.md`'s `Decision Log` for final quality unless they affect correctness, plan alignment, ownership boundaries, or commit safety.
