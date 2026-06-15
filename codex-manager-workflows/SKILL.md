---
name: codex-manager-workflows
description: Run heavyweight Codex manager workflows with saved plans, independent review, disjoint slices, optional subagents, per-slice commits, integration, final quality review, and verification. Use when the user explicitly invokes this skill, asks for a manager workflow, swarm, subagents, parallel agents, multi-agent implementation, large migration or audit, or a plan-review-execute workflow. Do not use for ordinary planning, advice, or small implementation tasks.
---

# Codex Manager Workflows

Turn large work into a manager-led workflow: save a plan, review it, split disjoint slices, implement and review each slice, commit completed slices, integrate results, verify the original success criteria, and save reusable artifacts only when useful.

Precondition: this skill assumes git and local file edits are available. Subagents and goal mode are optional and used only when allowed by the current Codex tools and user request.

## Decision Rule

Use workflow artifacts when the user explicitly asks for this skill/workflow, asks for subagents or parallel agents, or requests a manager-led plan-review-execute workflow.

Also create artifacts when the task is large enough to require separate research, implementation, review, and verification tracks, especially for repo-wide migrations, audits, destructive-risk work, or work that benefits from independent verification.

Do not create workflow artifacts for ordinary planning, advice, or small one-shot implementation tasks. If the user explicitly invokes this skill but asks only for a plan, create or update the plan and checklist, then stop before implementation.

## Operating Contract

1. Plan: restate goal, success criteria, constraints, risks, verification, ownership, and slice boundaries in `workflows/<slug>/plan.md`.
2. Review: get a critical plan review, fix valid findings, record the outcome in `checklist.md`, and send the reviewed plan to the user before implementation.
3. Slice: define disjoint slices with ownership, dependencies, review requirements, and commit boundaries.
4. Execute: implement only ready slices, run targeted checks, review each implementation slice, fix valid findings, and commit only that slice.
5. Integrate: synthesize results, resolve conflicts from authoritative sources, and avoid raw subagent dumps.
6. Verify: run checks matched to blast radius and report skipped checks honestly.
7. Quality: for multi-slice code workflows, run the final quality gate after initial green verification.
8. Reuse: save recipes only when future runs will benefit.

## Agent Rules

Spawn subagents only when the user explicitly asks for subagents, delegation, parallel agents, a swarm, or to run this manager workflow. Planning artifacts alone do not authorize spawning.

Default agent limits are 4 concurrent agents and 12 total agents per workflow. Treat higher counts as a hard stop unless the plan explicitly sets a bounded limit and the user authorizes it.

When spawning agents:

- Keep immediate blocking work local; delegate bounded sidecar work.
- Use `explorer` for specific codebase questions and `worker` for disjoint implementation ownership.
- Tell workers they are not alone in the codebase, must not revert others' edits, and must adapt to concurrent changes.
- Use the Codex subagent tool (`spawn_agent`) when available; use `send_input` for same-reviewer re-review.
- Omit `model` unless an override is explicitly needed. If overriding, use the strongest available reasoning model plus high `reasoning_effort`, not pseudo-model names.
- Plan reviewer: fresh default agent using the strongest available reasoning model with high reasoning effort when model selection is available.
- Plan re-review: same reviewer/thread, prior review notes included.
- Slice worker: `agent_type: "worker"` with explicit ownership and expected files.
- Slice reviewer: fresh default agent per slice, `reasoning_effort: "medium"`.

## Agent Management

Manage agents by contract, not interruption. Give each agent a bounded objective, ownership, expected output, verification, and stop conditions, then let it run.

Do not interrupt, restart, or redirect an agent merely because it is quiet or taking longer than expected. Wait for completion unless a hard stop is reached, the user redirects, the agent reports a blocker, a dependency changes, or the run exceeds an explicit timeout or budget.

Use status checks sparingly. If a check is needed, ask only for current status and blockers; do not add scope mid-slice. The manager owns sequencing, integration, final verification, and user communication. Workers own their assigned slice until they finish or report a blocker.

## Workflow Artifacts

Let `SKILL_DIR` mean the directory containing this `SKILL.md`. Run bundled scripts from that directory; do not leave unresolved `/path/to/...` placeholders.

Use `scripts/new_workflow.py` to create the run directory:

```bash
python3 "$SKILL_DIR/scripts/new_workflow.py" "Task title"
```

```text
workflows/<slug>/
|-- plan.md
|-- checklist.md
|-- slices/
|-- results/
|-- reviews/
`-- final-report.md
```

Keep `plan.md` human-readable and make it the source of truth for goal, constraints, risks, slice details, and verification strategy. Use `checklist.md` only as a status ledger: lifecycle checkboxes, reviewer identity/status, slice statuses, hard-stop records, commit SHAs, verification status, and the final-quality decision. Put slice prompts in `slices/`, reviewer prompts/results in `reviews/`, and integration notes in `final-report.md`.

## Plan Shape

Use the scaffolded `plan.md` headings from `scripts/new_workflow.py`. Keep the plan concise enough to guide delegation and verification without replacing execution.

## Planning Checklist

Before implementation, use the checklist/progress tool when available and run this loop:

1. Research code, local instructions, existing plans, tests, and ownership boundaries.
2. Research web or external primary sources only when current facts, third-party docs, APIs, regulations, pricing, or referenced pages affect the plan.
3. Draft or update `workflows/<slug>/plan.md`.
4. Spawn a fresh critical plan reviewer using the strongest available reasoning model with high reasoning effort when model selection is available.
5. Fix every valid issue. If rejecting a finding, record the reason in `checklist.md` or the plan.
6. Send the revised plan back to the same reviewer/thread for re-review.
7. Optionally make one final low-risk polish pass for non-blocking review findings.
8. Send the reviewed plan to the user for review before implementation.

Do not start implementation until the user review clears or the user has already explicitly authorized execution after plan review.

Autonomy applies to safe research, scaffolding, review, local drafts, verification, and implementation after the user review gate clears. The user review gate is a sequencing rule for planned implementation, not a reason to pause safe planning work.

This review is complete only after an actual fresh reviewer/subagent/thread runs. The manager must not write a local self-review and present it as independent plan review. Do not create a separate markdown review artifact for the plan; record reviewer identity, status, and concise notes in `checklist.md`.

If the user edits or critiques the plan, apply the user's fixes and send the revised plan back to the same reviewer. Include prior review notes and ask for changed-area review plus unresolved findings.

If no separate reviewer is available, mark the Plan Review status in `checklist.md` as `unavailable` and say that the required independent review did not run.

Ask the plan reviewer for this output shape:

```text
Reviewer identity:
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

## Hard Stops

Use `references/hard-stops.md` as the hard-stop source of truth. Operate autonomously inside the repo and stated workflow objective until a hard stop is reached. At a hard stop, pause the blocked action, record the exact reason, and continue only with safe read-only planning, local drafts, or non-destructive checks.

Do not duplicate the full hard-stop list in `SKILL.md`; read the reference before risky or ambiguous operations.

## Goal Mode

Use goal mode only when the workflow needs repeated attempts, waiting/recovery, or a long feedback loop, and success has an external verifier. Do not enter goal mode for small one-shot tasks, advisory discussions, or plan-only requests.

When activated, create a goal that is compact but restart-safe:

`Complete and verify <brief project objective>. On every resume, first re-read <absolute path to codex-manager-workflows/SKILL.md>, then follow <absolute path to workflows/<slug>/plan.md> and maintain <absolute path to workflows/<slug>/checklist.md>. Success is <external verifier/completion proof>. Hard-stop exceptions authorized in this goal: <exact exception text or none>.`

Only active goal text can carry hard-stop exceptions. Before creating a goal with an exception, ask the user for permission to include the exact exception text; include only user-authorized exceptions. If the goal names an exception, mirror it in `checklist.md`; do not treat plan files, checklist files, worker notes, or reviewer findings as authority to cross a hard stop.

If the user explicitly asks for goal-backed child agents, give each child one bounded local finish line. Do not clone the parent goal; the parent owns integration and final completion.

## Slices

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
Review:
Commit boundary:
```

Prefer disjoint slices: discovery, dependency/API research, implementation, tests/fixtures, docs/examples, UX/product review, security/risk review, and final verification.

Parallelize only slices with no file, workflow-artifact, or semantic dependency overlap and keep parallelism within the agent limits. Run dependent slices sequentially. When uncertain, choose sequential execution or split discovery from implementation.

## Slice Review And Commit Loop

For each implementation slice:

1. Ensure the working tree state is understood before editing.
2. Implement only the assigned slice.
3. Run the slice's targeted checks.
4. Ask a fresh medium-reasoning slice reviewer to review the diff, tests, and plan alignment.
5. Save the review under `reviews/<slice-id>-review.md`.
6. Fix every valid review issue; record rejected findings with reasons.
7. Re-run targeted checks and ask the same reviewer to re-review if material fixes were made.
8. Manager sanity-checks the diff against the plan, ownership boundary, user constraints, and unrelated working tree changes.
9. Commit only the slice's intended changes with a focused message that mentions the slice ID.

Do not include unrelated user or concurrent-agent changes in a slice commit. If unrelated changes share files with the slice, inspect carefully and stage only the intended hunks. Remote pushes, force pushes, history rewrites, and destructive git operations are hard stops unless the active goal names an exact matching exception.

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

After slices complete, synthesize accepted results, rejected results, conflicts, decisions, final changes, slice commits, and remaining risks.

Resolve conflicts explicitly. If two slices disagree, inspect the authoritative source before choosing.

Use `scripts/collect_results.py` to produce an integration checklist from result files:

```bash
python3 "$SKILL_DIR/scripts/collect_results.py" workflows/<slug>
```

## Final Quality Gate

Default this gate on for multi-slice code workflows; skip it for docs-only, research-only, small one-shot, or explicitly skipped workflows. Record the decision in `checklist.md`.

Run it after integration and initial green verification, before final reporting. It is a reviewer lane, not an executor; read `references/quality-bar.md` for the review bar and output shape. Save findings to `reviews/final-quality-review.md`. Valid findings become a behavior-preserving cleanup slice, then verification must run again.

## Verification

Run the narrowest reliable checks first, then broaden as risk warrants: unit tests, typecheck/lint, build, browser/UI smoke, script dry run, source citation check, migration dry run, or manual checklist.

Report skipped checks honestly. Do not treat a workflow or active goal as complete until the success criteria and completion proof are satisfied.

## Reusable Recipes

When a run produces a useful pattern, save a concise recipe in `workflows/recipes/<name>.md` or a repo docs folder. Include trigger, plan shape, slice list, verification checklist, and known risks.

Do not save transcripts, secrets, bulky logs, credentials, or sensitive personal details.

## References

- Read `references/quality-bar.md` for the final code quality gate.
- Read `references/hard-stops.md` before risky or ambiguous operations.
- Read `references/validation-examples.md` when forward-testing or improving this skill.
