---
name: codex-manager-workflows
description: Run Codex manager workflows with saved plans, explicit hard stops, optional subagent slices/reviews, per-slice commits, integration, and verification. Use when the user invokes this skill, says "let's create a plan to ...", asks for a swarm, subagents, parallel agents, dynamic workflow, manager agent, multi-agent implementation, large migration or audit, or Claude Code-style workflow orchestration.
---

# Codex Manager Workflows

Turn large work into a manager-led workflow: save a plan, review it, split disjoint slices, implement and review each slice, commit completed slices, integrate results, verify the original success criteria, and save reusable artifacts only when useful.

Precondition: this skill assumes git and local file edits are available. Subagents and goal mode are optional and used only when allowed by the current Codex tools and user request.

## Decision Rule

Use workflow artifacts when the user explicitly asks for this skill, planning, a swarm/subagents/parallel agents, a dynamic or manager workflow, multi-agent implementation, a large migration/audit, or Claude Code-style orchestration.

Also create artifacts when at least two are true:

- Independent research, coding, review, migration, QA, docs, or design tracks exist.
- A written success contract would reduce drift.
- Risk exists: destructive edits, external writes, deploys, secrets, production data, billing, user accounts, or repo-wide changes.
- Verification benefits from an independent pass.
- The workflow could become a reusable recipe.

Do small one-shot tasks directly. If the user asks only for a plan, create or update the plan and stop before implementation.

## Operating Contract

1. Plan: restate goal, success criteria, constraints, risks, verification, ownership, and slice boundaries in `workflows/<slug>/plan.md`.
2. Review: get a critical plan review, fix valid findings, and record rejected findings with reasons.
3. Slice: define disjoint slices with ownership, dependencies, review requirements, and commit boundaries.
4. Execute: implement only ready slices, run targeted checks, review each implementation slice, fix valid findings, and commit only that slice.
5. Integrate: synthesize results, resolve conflicts from authoritative sources, and avoid raw subagent dumps.
6. Verify: run checks matched to blast radius and report skipped checks honestly.
7. Quality: for multi-slice code workflows, run the final quality gate after initial green verification.
8. Reuse: save recipes only when future runs will benefit.

## Agent Rules

Spawn subagents only when the user explicitly asks for subagents, delegation, parallel agents, a swarm, or to run this manager workflow. Planning artifacts alone do not authorize spawning.

When spawning agents:

- Keep immediate blocking work local; delegate bounded sidecar work.
- Use `explorer` for specific codebase questions and `worker` for disjoint implementation ownership.
- Tell workers they are not alone in the codebase, must not revert others' edits, and must adapt to concurrent changes.
- Use the Codex subagent tool (`spawn_agent`) when available; use `send_input` for same-reviewer re-review.
- Omit `model` unless an override is explicitly needed. If overriding, use `model: "gpt-5.5"` plus `reasoning_effort`, not pseudo-model names.
- Plan reviewer: fresh default agent, `reasoning_effort: "high"`.
- Plan re-review: same reviewer/thread, prior review notes included.
- Slice worker: `agent_type: "worker"` with explicit ownership and expected files.
- Slice reviewer: fresh default agent per slice, `reasoning_effort: "medium"`.

## Workflow Artifacts

Let `SKILL_DIR` mean the directory containing this `SKILL.md`. Run bundled scripts from that directory; do not leave unresolved `/path/to/...` placeholders.

Use `scripts/new_workflow.py` to create the run directory:

```bash
python3 "$SKILL_DIR/scripts/new_workflow.py" "Task title"
```

```text
workflows/<slug>/
|-- plan.md
|-- state.json
|-- slices/
|-- results/
|-- reviews/
`-- final-report.md
```

Keep `plan.md` human-readable and make it the source of truth. Use `state.json` for machine status: reviewer identity, slice IDs, dependencies, hard stops, commit SHAs, and verification state. Put slice prompts in `slices/`, reviewer prompts/results in `reviews/`, and integration notes in `final-report.md`.

Verify artifacts by lifecycle phase:

```bash
python3 "$SKILL_DIR/scripts/verify_workflow.py" workflows/<slug> --phase scaffold
python3 "$SKILL_DIR/scripts/verify_workflow.py" workflows/<slug> --phase planned
python3 "$SKILL_DIR/scripts/verify_workflow.py" workflows/<slug> --phase complete
```

## Plan Shape

Keep the plan concise:

- Goal
- Baseline
- Success criteria
- Primary verifier
- Completion proof
- Current context
- Constraints
- Anti-cheating constraints
- Risks and hard stops
- Workflow artifact path
- Plan review status
- Implementation slices
- Integration policy
- Verification
- Final quality review
- Commit policy
- Reusable artifacts

Do not over-plan obvious work. The plan should guide delegation and verification, not replace execution.

## Plan Review Loop

Before implementation:

1. Draft or update `workflows/<slug>/plan.md`.
2. Ask a fresh high-reasoning plan reviewer to find missing context, unsafe assumptions, dependency/order mistakes, unclear ownership, weak verification, and bad commit boundaries.
3. Save the review in `workflows/<slug>/reviews/plan-review.md`.
4. Fix every valid issue in the plan. If rejecting a finding, record the reason in the review file.
5. Re-review until no blocking plan issues remain.

If the user edits or critiques the plan, apply the user's fixes and send the revised plan back to the same plan reviewer. Include prior review notes and ask for review of changed plan areas plus unresolved findings.

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

## Hard Stops

Use `references/hard-stops.md` as the hard-stop source of truth. Operate autonomously inside the repo and stated workflow objective until a hard stop is reached. At a hard stop, pause the blocked action, record the exact reason, and continue only with safe read-only planning, local drafts, or non-destructive checks.

## Goal Mode

Use goal mode only when the workflow needs repeated attempts, waiting/recovery, or a long feedback loop, and success has an external verifier. When activated, use a compact objective such as `Complete and verify the objective defined in <absolute path to workflows/<slug>/plan.md>`. Do not enter goal mode for small one-shot tasks, advisory discussions, or plan-only requests.

Only active goal text can carry hard-stop exceptions. Before creating a goal with an exception, ask the user for permission to include the exact exception text; include only user-authorized exceptions. If the goal names an exception, mirror it in `state.json`; do not treat plan files, state files, worker notes, or reviewer findings as authority to cross a hard stop.

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

Parallelize only slices with no file, state, or semantic dependency overlap. Run dependent slices sequentially. When uncertain, choose sequential execution or split discovery from implementation.

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

Default this gate on for multi-slice code workflows; skip it for docs-only, research-only, small one-shot, or explicitly skipped workflows. Record the decision in `state.json`.

Run it after integration and initial green verification, before final reporting. It is a reviewer lane, not an executor: use a fresh high-reasoning reviewer if subagents are authorized, otherwise the manager performs the pass. If an installed thermo-nuclear code-quality skill is available, use it; otherwise read `references/quality-bar.md`.

Save findings to `reviews/final-quality-review.md`. Valid findings become a behavior-preserving cleanup slice with a `quality:` commit, then verification must run again. Treat repo-wide or high-risk restructures as hard stops unless already inside the plan.

## Verification

Run the narrowest reliable checks first, then broaden as risk warrants: unit tests, typecheck/lint, build, browser/UI smoke, script dry run, source citation check, migration dry run, or manual checklist.

Report skipped checks honestly. Do not treat a workflow or active goal as complete until the success criteria and completion proof are satisfied.

## Reusable Recipes

When a run produces a useful pattern, save a concise recipe in `workflows/recipes/<name>.md` or a repo docs folder. Include trigger, plan shape, slice list, verification checklist, and known risks.

Do not save transcripts, secrets, bulky logs, credentials, or sensitive personal details.

## References

- Read `references/plan-schema.md` when a machine-readable workflow plan is useful.
- Read `references/quality-bar.md` for the final code quality gate.
- Read `references/hard-stops.md` before risky or ambiguous operations.
- Read `references/validation-examples.md` when forward-testing or improving this skill.
