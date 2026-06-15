---
name: codex-manager-workflows
description: Run Codex-specific manager workflows with saved plans, subagent slices, reviewer agents, per-slice git commits, integration, and verification. Use when the user invokes this skill, says "let's create a plan to ...", asks for a swarm, subagents, parallel agents, dynamic workflow, manager agent, multi-agent implementation, large migration or audit, or Claude Code-style workflow orchestration.
---

# Codex Manager Workflows

Use this skill to turn a large task into a manager-led Codex workflow: create a saved plan, get it critically reviewed by a `gpt-5.5-high` plan reviewer, repair the plan, delegate disjoint implementation slices, review each slice independently, fix review findings, commit each completed slice, integrate results, verify the outcome, and save reusable workflow artifacts.

Precondition: this skill assumes Codex goal mode, subagents, model selection, and git are available.

Use these reviewer roles consistently:

- Plan review: a fresh `gpt-5.5-high` plan reviewer.
- Plan re-review after user or manager changes: the same `gpt-5.5-high` plan reviewer with the prior review notes.
- Slice review: a fresh `gpt-5.5-medium` slice reviewer per slice.

## Decision Rule

Use this workflow whenever the user explicitly asks for this skill, says "let's create a plan to ...", asks for a swarm, subagents, parallel agents, a dynamic workflow, a manager agent, multi-agent implementation, or Claude Code-style workflow orchestration.

Also use dynamic orchestration when at least two are true:

- The task has independent research, coding, review, migration, QA, docs, or design tracks.
- The task is broad enough that an explicit success contract would reduce drift.
- The task has risk: destructive edits, external writes, deploys, secrets, production data, billing, user accounts, or large repo-wide changes.
- Verification benefits from a separate pass from implementation.
- The workflow could become a reusable recipe for future tasks.

If no explicit workflow trigger applies and the task is small, do it directly and mention that full workflow orchestration was unnecessary.

## Operating Contract

When using this skill:

1. Plan: restate the goal, success criteria, constraints, risks, verification, and slice boundaries in `workflows/<slug>/plan.md`.
2. Review: send the plan to the `gpt-5.5-high` plan reviewer, fix valid findings, and re-review user or manager changes.
3. Slice: split implementation into disjoint slices with clear ownership, dependencies, review requirements, and commit boundaries.
4. Review and commit: for each slice, implement, run checks, get a `gpt-5.5-medium` slice review, fix valid findings, sanity-check, and commit only that slice.
5. Integrate: synthesize slice results, resolve conflicts from authoritative sources, and avoid pasting raw subagent dumps.
6. Verify: run checks matched to the task's blast radius and report skipped checks honestly.
7. Reuse: save reusable artifacts only when they will help future work.

## Workflow Artifacts

Prefer creating a local run directory under `workflows/`:

```text
workflows/<slug>/
|-- plan.md
|-- state.json
|-- orchestration.md
|-- slices/
|-- results/
|-- reviews/
`-- final-report.md
```

Use `scripts/new_workflow.py` to scaffold this structure:

```bash
python3 /path/to/codex-manager-workflows/scripts/new_workflow.py "Task title"
```

Keep `plan.md` human-readable and make it the source of truth. Use `state.json` for status, reviewer identity, slice IDs, dependencies, approval state, commit SHAs, and verification state. Use `orchestration.md` as the executable mental model: the sequence the manager will follow, the branching rules, and the slice prompts.

## Orchestration Plan

Draft a concise plan with:

```text
Goal:
Success criteria:
Current context:
Constraints:
Risks:
Approval required:
Workflow artifact path:
Plan review:
Implementation slices:
Integration policy:
Verification:
Commit policy:
Reusable artifacts:
```

Do not over-plan obvious work. The plan should be detailed enough to guide delegation and verification, not a substitute for execution.

## Plan Review Loop

Before implementation:

1. Draft or update `workflows/<slug>/plan.md`.
2. Ask a fresh `gpt-5.5-high` plan reviewer to critically review the plan for missing context, unsafe assumptions, dependency/order mistakes, unclear slice ownership, insufficient verification, and bad commit boundaries.
3. Save the review in `workflows/<slug>/reviews/plan-review.md`.
4. Fix every valid issue in the plan. If rejecting a finding, record the reason in the review file.
5. Re-review until no blocking plan issues remain.

If the user edits or critiques the plan, apply the user's fixes and send the revised plan back to the same `gpt-5.5-high` plan reviewer. Include the original review file and ask the reviewer to re-review only the changed plan plus any unresolved findings.

Plan review output shape:

```text
Verdict: blocking | non-blocking
Blocking findings:
Non-blocking findings:
Unsafe assumptions:
Missing context:
Slice boundary issues:
Verification gaps:
Commit boundary issues:
Required plan changes:
Re-review required: yes | no
```

## Approval Gates

Ask one clear approval question before:

- deleting, overwriting, mass-renaming, or force-pushing
- running migrations or broad codemods
- deploying, publishing, emailing, posting, or changing external systems
- touching credentials, secrets, production data, billing, or user accounts
- spawning many agents or long-running expensive jobs
- making irreversible Git or repository operations

If approval is denied, continue only with safe read-only planning, local drafts, or non-destructive checks.

Read `references/risk-gates.md` when risk is unclear.

## Goal Mode

When the user has asked this skill to run the workflow, enter goal mode with the full objective. Keep the objective intact; do not shrink it to the next step.

Do not enter goal mode for a small one-shot task, a purely advisory discussion, or when the user asks only for a plan.

## Implementation Slices

Each slice must be self-contained:

```text
Slice ID:
Objective:
Context:
Files / sources:
Ownership:
Dependencies:
Do:
Do not:
Expected output:
Verification:
Review model:
Commit boundary:
```

Prefer slices with disjoint ownership:

- codebase discovery
- dependency or API research
- implementation slice
- tests and fixtures
- docs and examples
- UX or product review
- security or risk review
- final verification

For code-edit slices, assign non-overlapping files or modules. Tell workers they are not alone in the codebase, must not revert others' edits, and must adapt to concurrent changes.

Parallelize only slices with no file, state, or semantic dependency overlap. Run dependent slices sequentially. When uncertain, choose sequential execution or split discovery from implementation.

## Subagents

- Spawn only concrete, bounded, materially useful subtasks.
- Keep immediate blocking work local.
- Delegate sidecar work that can run while the main agent makes progress.
- Avoid duplicate work across agents.
- Ask workers to edit directly only when their write scope is disjoint and clear.
- Wait for subagents only when their result is needed for the next critical-path step.

## Slice Review And Commit Loop

For each implementation slice:

1. Ensure the working tree state is understood before editing.
2. Implement only the assigned slice.
3. Run the slice's targeted checks.
4. Ask a fresh `gpt-5.5-medium` slice reviewer to critically review the slice diff, tests, and plan alignment.
5. Save the review under `reviews/<slice-id>-review.md`.
6. Fix every valid review issue; record rejected findings with reasons.
7. Re-run targeted checks and ask the same reviewer to re-review if material fixes were made.
8. Manager sanity-checks the diff against the plan, ownership boundary, user constraints, and unrelated working tree changes.
9. Commit only the slice's intended changes with a focused message that mentions the slice ID.

Do not include unrelated user or concurrent-agent changes in a slice commit. If unrelated changes share files with the slice, inspect carefully and stage only the intended hunks. Ask the user before force pushes, history rewrites, or destructive git operations.

Slice review output shape:

```text
Verdict: blocking | non-blocking
Plan alignment:
Files reviewed:
Blocking findings:
Non-blocking findings:
Test or verification gaps:
Unrelated-change risk:
Required fixes:
Re-review required: yes | no
Commit-ready: yes | no
```

## Integration

After slices complete, synthesize:

```text
Accepted:
Rejected:
Conflicts:
Decisions:
Final changes:
Slice commits:
Remaining risks:
```

Resolve conflicts explicitly. If two slices disagree, inspect the authoritative source before choosing.

Use `scripts/collect_results.py` to produce an integration checklist from result files:

```bash
python3 /path/to/codex-manager-workflows/scripts/collect_results.py workflows/<slug>
```

## Verification

Run the narrowest reliable checks first, then broaden as risk warrants:

- unit tests for touched code
- typecheck or lint
- build
- browser or UI smoke test
- script dry run
- source citation check
- migration dry run
- manual checklist for non-code work

Use `scripts/verify_workflow.py` to check workflow artifact completeness:

```bash
python3 /path/to/codex-manager-workflows/scripts/verify_workflow.py workflows/<slug>
```

Report skipped checks honestly. Do not treat a workflow as complete until the evidence proves the original success criteria.

## Reusable Recipes

When a run produces a useful pattern, save a concise recipe in a project-appropriate location, such as `workflows/recipes/<name>.md` or a repo docs folder. Include:

- trigger
- plan shape
- slice list
- verification checklist
- known risks

Do not save transcripts, secrets, bulky logs, credentials, or sensitive personal details.

## References

- Read `references/plan-schema.md` when a machine-readable workflow plan is useful.
- Read `references/risk-gates.md` before risky or ambiguous operations.
- Read `references/validation-examples.md` when forward-testing or improving this skill.
