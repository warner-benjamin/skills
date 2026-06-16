---
name: managed-plan
description: Research a codebase, local docs, and relevant external sources to create or update a managed workflow plan, interview the user to resolve open questions before review, run the selected low-level or high-level plan review, revise valid findings, and hand the reviewed plan to the user before implementation. Use when the user explicitly invokes $managed-plan, asks for the planning phase of a managed workflow, or wants a reviewed plan/checklist artifact for later execution. Do not use for ordinary informal planning or small one-shot tasks.
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
- `$PHASE_SKILL_DIR/references/plan-review.md` for review levels, reviewer prompts, Claude CLI review, and output shape

If no workflow directory exists, create one with:

```bash
python3 "$WORKFLOW_SKILL_DIR/scripts/new_workflow.py" "Task title"
```

## Planning Loop

1. Research code, local instructions, existing plans, tests, and ownership boundaries.
2. Research web or external primary sources only when current facts, third-party docs, APIs, regulations, pricing, or referenced pages affect the plan.
3. Separate grounding into observed facts, user requirements, resolved assumptions, and evidence gaps.
4. Identify any unresolved decisions, options, alternate paths, missing preferences, or approval questions. Interview the user during research until these are resolved before drafting the reviewed plan.
5. Draft or update `workflows/<slug>/plan.md` using the contract headings. The plan must state one chosen path and must not contain unresolved decisions, options, alternate paths, TODOs, or open questions.
6. Define implementation slices with objectives, ownership, dependencies, verification, review, and commit boundaries.
7. Define approval gates only for post-planning consequential actions that still require user approval; otherwise keep implementation autonomous after the user implementation gate.
8. Define orchestration sequence, including slice order, dependency readiness, retry/re-slice rules, reviewer-unavailable behavior, failed-check behavior, and final-quality cleanup routing.
9. Update `checklist.md` for research status, user-interview status, plan draft status, review level, reviewer identity/thread id, and final-quality gate details.
10. Run the selected review level from `plan-review.md`.
11. Fix valid findings with the smallest change that resolves them. Treat reviewer comments as suggestions: accept only findings that are correct in context and do not undo user-decreed requirements.
12. Present the reviewed plan to the user with the review level, review verdicts, accepted fixes, rejected findings, and a direct request for plan feedback. Leave `User implementation gate` as `pending` until the user clears execution.

Do not start implementation during this phase. Safe research, scaffolding, plan review, local drafts, and non-destructive checks can proceed autonomously.

## Review Requirement

The plan review is complete only after the selected review level in `plan-review.md` runs. Do not write a local self-review and present it as independent review.

If no separate reviewer is available, mark `Plan review: unavailable` in `checklist.md` and tell the user that independent review did not run. Implementation may start only if the user explicitly clears execution after seeing that caveat.

If the user edits or critiques the plan after review, apply the user's fixes. For high-level review, send material changed areas back to the same Codex reviewer/thread; do not run a second Claude review unless the user asks. For low-level review, do not add an automatic re-review loop; upgrade to high-level review only when the user requests it or the change introduces material new risk.

## Handoff

Before stopping, ensure:

- `plan.md` is the source of truth for goal, observed facts, user requirements, resolved assumptions, constraints, risks, approval gates, slices, orchestration sequence, and verification.
- `checklist.md` records plan review status, reviewer identity/status, rejected findings, and user gate state.
- The user sees the reviewed plan, review level, reviewer verdicts, material fixes, rejected findings, and any skipped-review caveat.

Only mark `User implementation gate: cleared` when the user explicitly clears implementation or had already authorized implementation after plan review. If plan review is unavailable, the clearance must happen after the skipped-review caveat is shown.
