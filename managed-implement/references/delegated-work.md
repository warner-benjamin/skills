# Delegated Work

Read this before delegating slices or running parallel/worker lanes. The single-agent local path in `SKILL.md` doesn't need it.

## Worker Integration

The main agent owns the current branch: it imports, stages, verifies, and commits every final change unless the plan assigns commit authority elsewhere. Never commit a worker diff you haven't inspected.

Choose the simplest isolation model that keeps changes attributable and safe, and record it in `plan.md` or `checklist.md`. Worktrees help but aren't required when slices are independent enough and the runner already isolates changes.

- Runner-provided workspace: prefer when the runner gives each worker a separate workspace or patch stream. The worker reports its workspace and changed paths; the main agent imports only intended changes.
- Worktree-per-worker: `git worktree add` on a per-worker branch when parallel lanes need local isolation and the runner provides none. Record branch, path, import method, and cleanup.
- Shared-tree with disjoint write scope: only when slices are independent — sequential, or parallel with strictly non-overlapping files and no shared uncommitted state. Never run parallel coding workers against one shared tree when edits can interleave.

Require each worker to report its workspace/branch, changed files, verification evidence, blockers, and remaining risks (see `slice-artifacts.md`). Before committing, inspect the worker diff, apply only intended changes, record the source in `checklist.md`, and re-run the slice checks in the main tree.

## Parallelism

Parallelize only slices with no file, workflow-artifact, or semantic dependency overlap, within the agent limits. Run dependent slices sequentially; when uncertain, go sequential or split discovery from implementation.

Spawn a workgroup only when it materially helps. For small or tightly coupled work, use one coding lane and one review lane.

A delegated worker that stalls past a timeout, returns unmergeable or off-scope work, or reverts others' edits: stop that lane, record it in `checklist.md`, and retry with a tighter prompt or take the slice local. See `SKILL.md` Failure Handling for the general non-convergence rules.
