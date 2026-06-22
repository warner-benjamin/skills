---
name: managed-workflow
description: Orchestrate a full managed Codex workflow through the managed-plan, managed-implement, and managed-quality phases, with durable plan/checklist artifacts, independent plan review, explicit implementation approval, risk-gated execution, focused commits, and verification. Use when the user explicitly invokes $managed-workflow, or asks for a managed workflow, swarm, subagents, parallel agents, multi-agent implementation, a large migration or audit, or a plan-review-execute workflow. Do not use for ordinary planning, advice, or small one-shot implementation tasks.
---

# Managed Workflow

Orchestrate a full managed workflow by routing through `managed-plan`, `managed-implement`, and `managed-quality` while keeping one durable artifact contract.

`SKILL_DIR` is the absolute directory of this `SKILL.md`. The phase skills `managed-plan`, `managed-implement`, and `managed-quality` are siblings of it.

## Decision Rule

Use workflow artifacts when the user explicitly asks for this skill/workflow, asks for subagents or parallel agents, or requests a managed plan-review-execute workflow. Also create them when the task needs separate research, implementation, review, and verification tracks — repo-wide migrations, audits, destructive-risk work, or work that benefits from independent verification.

Don't create workflow artifacts for ordinary planning, advice, or small one-shot tasks, even when this skill is explicitly invoked — do the small task directly and say full orchestration was unnecessary. If the user invokes this skill but asks only for a plan, run only `managed-plan` and stop before implementation.

## Shared Contract

Read `references/workflow-contract.md` before creating or resuming a workflow; it defines the artifact layout, status ledger, phase gates, and handoff rules.

Create a run directory with:

```bash
python3 "$SKILL_DIR/scripts/new_workflow.py" "Task title"
```

Keep the run directory untracked by git unless the user asks to check workflow artifacts in. Don't add it to commits just because slice work records status there.

## Operating Path

Create or resume one `workflows/<slug>/` run directory, then run the phases in order. Before each phase, read that phase's `SKILL.md` by absolute path from its sibling directory — phase skills aren't implicitly invoked, so the orchestrator must load them.

1. **Plan** (`managed-plan`): research, resolve user questions, draft one chosen design, run the selected review level, revise valid findings, present the plan.
2. **Approve**: don't start planned implementation until `checklist.md` shows `Implementation approval: approved` — a direct answer to the approval question, unless the original request pre-authorized skipping it.
3. **Implement** (`managed-implement`): run per the plan's execution mode and main agent role, activating goal mode for non-trivial work; execute slices, apply risk-gated review, run checks, commit focused changes, integrate. Create slice artifacts only when required.
4. **Quality** (`managed-quality`): for multi-slice or higher-risk code workflows after initial green verification, unless the plan/checklist marks it not-required.
5. **Verify**: run checks matched to blast radius; record skipped checks honestly.
6. **Report**: synthesize `final-report.md` — accepted/rejected results, conflicts, commits, verification evidence, final quality outcome, completion proof, remaining risks.

## Phase Routing

Run phases in order unless the user explicitly invokes one phase skill on an existing workflow:

- `managed-plan`: research, user-question resolution, plan drafting, the selected review level, fixes, and user handoff.
- `managed-implement`: only after plan review is non-blocking or properly caveated and implementation approval is approved.
- `managed-quality`: only after implementation is integrated and initial verification passes.

Each phase updates `checklist.md` — treat it as the status ledger, not a second plan.

## Shared References

- Read `references/workflow-contract.md` before creating, resuming, or handing off a workflow.
- Read `references/agents.md` before spawning or coordinating subagents.
- Read `references/hard-stops.md` before risky or ambiguous operations.
- Read `references/verification.md` before final or broad verification.
- Read `references/validation-examples.md` when forward-testing or improving this skill set.

## Goal Mode

For implementation, `managed-implement` owns goal-mode fit and activation. The orchestrator should not create a separate workflow-level goal unless the user explicitly asks for a goal outside the implementation phase.

## Reusable Recipes

When a run produces a useful pattern, save a concise recipe in a tracked repo docs folder; the default `workflows/` directory is untracked, so recipes saved there are local-only and easily lost. Include trigger, plan shape, slice list, verification checklist, and known risks. Do not save transcripts, secrets, bulky logs, credentials, or sensitive personal details.
