---
name: managed-plan
description: Research a codebase, local docs, and relevant external sources to create or update a managed workflow plan, get independent critical plan review, revise valid findings, request re-review, and hand the reviewed plan to the user before implementation. Use when the user explicitly invokes $managed-plan, asks for the planning phase of a managed workflow, or wants a reviewed plan/checklist artifact for later execution. Do not use for ordinary informal planning or small one-shot tasks.
---

# Managed Plan

Research, draft, review, and hand off the planning phase for a managed workflow. Stop before implementation; this phase only creates safe planning artifacts and review handoff.

## Shared Setup

Let `PHASE_SKILL_DIR` mean the absolute directory containing this `SKILL.md`. Resolve `WORKFLOW_SKILL_DIR` before reading shared references or running shared scripts:

1. Use a user-provided `managed-workflow` path when given.
2. Otherwise use the sibling `managed-workflow` directory next to `PHASE_SKILL_DIR`.
3. Use an absolute path. Do not run `../managed-workflow/...` relative to the user's shell cwd.

Read:

- `$WORKFLOW_SKILL_DIR/references/workflow-contract.md`
- `$WORKFLOW_SKILL_DIR/references/agents.md` before spawning reviewers
- `$WORKFLOW_SKILL_DIR/references/hard-stops.md` before risky or ambiguous operations
- `$PHASE_SKILL_DIR/references/plan-review.md` for the reviewer prompt and output shape

If no workflow directory exists, create one with:

```bash
python3 "$WORKFLOW_SKILL_DIR/scripts/new_workflow.py" "Task title"
```

## Planning Loop

1. Research code, local instructions, existing plans, tests, and ownership boundaries.
2. Research web or external primary sources only when current facts, third-party docs, APIs, regulations, pricing, or referenced pages affect the plan.
3. Draft or update `workflows/<slug>/plan.md` using the contract headings.
4. Define implementation slices with objectives, ownership, dependencies, verification, review, and commit boundaries.
5. Update `checklist.md` for research status, plan draft status, reviewer identity/thread id, and final-quality gate details.
6. Spawn a fresh critical plan reviewer when subagents or an independent reviewer thread are available.
7. Fix every valid issue. If rejecting a finding, record the reason in `checklist.md` or `plan.md`.
8. Send the revised plan back to the same reviewer/thread for re-review.
9. Optionally make one final low-risk polish pass for non-blocking review findings.
10. Present the reviewed plan to the user with the review verdict, accepted fixes, rejected findings, open decisions, and a direct request for plan feedback. Leave `User implementation gate` as `pending` until the user clears execution.

Do not start implementation during this phase. Safe research, scaffolding, plan review, local drafts, and non-destructive checks can proceed autonomously.

## Review Requirement

The plan review is complete only after an actual fresh reviewer/subagent/thread runs. Do not write a local self-review and present it as independent review.

If no separate reviewer is available, mark `Plan review: unavailable` in `checklist.md` and tell the user that independent review did not run. Implementation may start only if the user explicitly clears execution after seeing that caveat.

If the user edits or critiques the plan, apply the user's fixes and send the revised plan back to the same reviewer. Include prior review notes and ask for changed-area review plus unresolved findings.

## Handoff

Before stopping, ensure:

- `plan.md` is the source of truth for goal, constraints, risks, slices, and verification.
- `checklist.md` records plan review status, reviewer identity/status, rejected findings, and user gate state.
- The user sees the reviewed plan, reviewer verdict, material fixes, rejected findings, open decisions, and any skipped-review caveat.

Only mark `User implementation gate: cleared` when the user explicitly clears implementation or had already authorized implementation after plan review. If plan review is unavailable, the clearance must happen after the skipped-review caveat is shown.
