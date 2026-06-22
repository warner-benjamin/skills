# Slice Artifacts

Use durable slice artifacts when work is delegated, crosses a workspace boundary, needs independent review context, or is substantial enough that resume would otherwise lose important state. For a tiny main-agent coding slice, the checklist row, diff, commit, and verification evidence can be enough.

When a worker or reviewer has workspace write access, have it write its report/review directly to the named path. When the runner can't write to the workflow workspace, the agent returns concise text and the main agent persists it.

## Slice Prompts

Before delegation, write `slices/<slice-id>.md`; for substantial local slices, write it when it helps review or resume.

Give the worker or future reviewer enough to act without inventing core design: objective, relevant `plan.md` design/steps/slice references, files or sources, ownership boundary, dependencies, do/do-not guidance, expected output, verification, review expectation, report path, and commit boundary.

Slice prompts may add local execution context but must not change the reviewed design. If a slice needs a new design decision, pause and route back to `managed-plan` for a targeted update and review.

## Reports

Every worker lane produces `results/<slice-id>.md`. Local reports help for substantial slices and are optional for tiny main-agent coding slices.

Reports must be actionable, not ceremonial: changed paths, workspace/branch when applicable, what changed, verification run and result, blockers, remaining risks, and anything the main agent or reviewer must inspect. Field names don't matter. Don't accept a vague "done" as integration-ready.

## Reviews

When a reviewer agent runs, save findings to `reviews/<slice-id>-review.md`: a verdict plus critical findings, important non-blocking findings, missing context/unresolved questions, and required fixes.

Review the slice prompt and report when present, the diff, targeted-check evidence, alignment with the plan's `Design`/`Implementation Steps`/`Execution Slices`, ownership boundary, and unrelated-change risk.

Block commit readiness when the slice:

- changes files outside its ownership without a recorded reason
- skips targeted checks without a credible reason
- lacks required delegated-work artifacts
- diverges from the reviewed design or invents unreviewed core design
- mixes unrelated user or concurrent-agent changes into the slice
- leaves material findings unfixed and unrejected
- needs a local simplification to preserve correctness, plan alignment, ownership boundaries, or commit safety

After material fixes, ask the same reviewer/thread for re-review when available. Record clear local simplifications in `checklist.md`'s `Decision Log` for final quality unless they affect correctness, plan alignment, ownership boundaries, or commit safety.
