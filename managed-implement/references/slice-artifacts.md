# Exceptional worker files

Use `plan.md`, `checklist.md`, the worker prompt, and the worker's final response as the normal record. The checklist is sufficient for routine review and resume state.

Create `slices/<id>.md` and `results/<id>.md` only when:

- work crosses a workspace or branch boundary and the runner does not preserve the exchange
- the user explicitly requests separate audit artifacts

A durable work packet should contain the objective, plan references, ownership boundary, dependencies, checks, stop condition, and expected result path. Do not repeat the full plan.

A durable result should contain changed paths, what changed, checks and results, blockers, and remaining risks.

Record reviewer identity, verdict, blocking findings, accepted fixes, and unresolved risk concisely in `checklist.md`. Create a separate review file only when the user explicitly requests it or an external handoff cannot use the checklist and final response.
