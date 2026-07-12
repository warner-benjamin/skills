---
name: managed-plan
description: Research a repository and create or update a concise managed workflow plan and checklist for human review, with bounded work items, acceptance checks, verification, and review based on risk. Use when the user explicitly invokes $managed-plan, asks for the planning phase of a managed workflow, or wants a durable plan for later implementation. Present the artifacts and stop for approval before implementation.
---

# Managed plan

Create a plan that another capable agent can execute without inventing a material decision. Stop before implementation.

## Setup

`PHASE_SKILL_DIR` is the absolute directory containing this file. Resolve `WORKFLOW_SKILL_DIR` from a user provided path or the sibling `managed-workflow` directory.

Read `$WORKFLOW_SKILL_DIR/references/workflow-contract.md` unless it is already loaded for this run. Read `references/plan-review.md` and `$WORKFLOW_SKILL_DIR/references/agents.md` only when the path is strict or the user requests independent review.

If no run exists, create one with:

```bash
python3 "$WORKFLOW_SKILL_DIR/scripts/new_workflow.py" "Task title"
```

Add `--strict` when the known facts already require strict work. The command fails on an existing run, so resume by using the existing directory.

## Research

Inspect local instructions, relevant code, tests, existing plans, ownership boundaries, and the working tree. Use external primary sources only when current outside facts affect the design.

Make reasonable assumptions for reversible choices. Ask the user only when a missing choice would materially change the result, add scope, or require new authority. Set `Plan: needs-user` while such a decision is outstanding.

Recheck the path after research. If the work meets a strict condition, apply the contract's promotion transition before the plan becomes ready.

## Write the plan

Use these sections:

- `Goal`: State the requested outcome, success conditions, and meaningful exclusions.
- `Approach`: State one chosen design, the important observed facts, and the contracts or edge cases that affect implementation.
- `Work`: Define ordered work items with an objective, ownership boundary, dependencies, observable acceptance condition, and targeted checks.
- `Verification`: State the implementation checks, the final verifier, and the quality lane as `backend`, `frontend`, `mixed`, or `not-required`.

Add `Risks and approvals` only when needed. Keep the plan concise, but include enough detail that an implementer does not need to choose the architecture or invent expected behavior.

Create one checklist row for each work item with status `pending`. Do not choose a worker model in the plan. Model choice belongs to dispatch in `managed-implement`.

## Review

For `managed`, apply the plan readiness test and set `Plan review: not-required`. Do not create a separate self-review artifact.

For `strict`, follow `references/plan-review.md` and run one fresh review. Fix valid findings and update the plan. Use re-review only after material fixes to blocking findings.

## Human approval and handoff

Leave `Implementation authorization: waiting`. A request that also asks for implementation does not approve a plan the user has not seen.

Set `Plan: ready` only after material decisions are resolved, work rows exist, and the applicable review gate permits implementation. Update the checklist with concise review and authorization evidence.

Present both artifact paths, summarize the approach and material risks, ask the user whether to proceed, and stop. Plan feedback, approval of one design choice, or praise does not count as implementation approval. When this skill runs inside `managed-workflow`, return with authorization waiting so the orchestrator also stops.
