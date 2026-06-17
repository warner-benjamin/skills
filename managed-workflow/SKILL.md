---
name: managed-workflow
description: Run managed Codex workflows with saved plan/checklist artifacts, independent review of an organic design plan, explicit implementation approval, execution slices, delegated or substantial-slice prompts/reports, review and commits, integration, final simplification review, and verification. Use when the user explicitly invokes $managed-workflow, asks for a managed workflow, swarm, subagents, parallel agents, multi-agent implementation, large migration or audit, or a plan-review-execute workflow. Do not use for ordinary planning, advice, or small one-shot implementation tasks.
---

# Managed Workflow

Orchestrate a full managed workflow by routing through `managed-plan`, `managed-implement`, and `managed-quality` while keeping one durable artifact contract.

Let `SKILL_DIR` mean the absolute directory containing this `SKILL.md`. Resolve phase skill directories as siblings of `SKILL_DIR`: `managed-plan`, `managed-implement`, and `managed-quality`.

## Decision Rule

Use workflow artifacts when the user explicitly asks for this skill/workflow, asks for subagents or parallel agents, or requests a manager-led plan-review-execute workflow.

Also create artifacts when the task is large enough to require separate research, implementation, review, and verification tracks, especially for repo-wide migrations, audits, destructive-risk work, or work that benefits from independent verification.

Do not create workflow artifacts for ordinary planning, advice, or small one-shot implementation tasks, even when the user explicitly invokes this skill. In that case, do the small task directly and say full orchestration was unnecessary. If the user explicitly invokes this skill but asks only for a plan, run only `managed-plan` and stop before implementation.

## Shared Contract

Read `references/workflow-contract.md` before creating or resuming a workflow. It defines the artifact layout, status ledger, phase gates, and handoff rules.

Use `scripts/new_workflow.py` to create a run directory:

```bash
python3 "$SKILL_DIR/scripts/new_workflow.py" "Task title"
```

## Operating Contract

Before each phase, read the phase skill's `SKILL.md` by absolute path from the sibling phase directory. Phase skills are not implicitly invoked, so the orchestrator must load their instructions explicitly.

1. Plan: read `managed-plan/SKILL.md`, then run that phase to research, resolve user questions, draft one chosen organic design plan, run the selected review level, revise valid findings, and present the plan to the user.
2. Approval: do not start planned implementation until `checklist.md` shows `Implementation approval: approved`. This approval must come from a direct answer to the implementation-approval question, unless the original request explicitly instructed Codex not to stop for implementation approval after planning/review.
3. Implement: read `managed-implement/SKILL.md`, then run that phase to write delegated or substantial-slice prompts, execute planned slices, collect worker or substantial local reports, review each implementation slice, run checks, commit focused slice changes, and integrate results.
4. Quality: read `managed-quality/SKILL.md`, then run that phase for multi-slice code workflows after initial green verification, unless the plan/checklist explicitly marks it not required.
5. Verify: run checks matched to blast radius and record skipped checks honestly.
6. Report: update `final-report.md` with accepted results, rejected results, conflicts, commits, verification evidence, final quality outcome, completion proof, and remaining risks.

## Phase Routing

Run phases in order unless the user explicitly invokes one phase skill on an existing workflow:

- Use `managed-plan` for research, user-question resolution, plan drafting, selected plan review level, plan fixes, and user review handoff.
- Use `managed-implement` only after plan review is non-blocking or properly caveated, and implementation approval is approved.
- Use `managed-quality` only after implementation is integrated and initial verification passes.

Each phase updates `checklist.md`. Treat that file as the status ledger, not as a second plan.

## Shared References

- Read `references/workflow-contract.md` before creating, resuming, or handing off a workflow.
- Read `references/agents.md` before spawning or coordinating subagents.
- Read `references/hard-stops.md` before risky or ambiguous operations.
- Read `references/verification.md` before final or broad verification.
- Read `references/validation-examples.md` when forward-testing or improving this skill set.

## Goal Mode

For implementation, `managed-implement` owns goal-mode fit and activation. The orchestrator should not create a separate workflow-level goal unless the user explicitly asks for a goal outside the implementation phase.

## Reusable Recipes

When a run produces a useful pattern, save a concise recipe in `workflows/recipes/<name>.md` or a repo docs folder. Include trigger, plan shape, slice list, verification checklist, and known risks. Do not save transcripts, secrets, bulky logs, credentials, or sensitive personal details.
