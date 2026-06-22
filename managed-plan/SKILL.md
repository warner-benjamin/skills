---
name: managed-plan
description: Research a codebase, local docs, and relevant external sources to create or update an organic managed workflow design plan, interview the user to resolve open questions before review, run the selected low-level or high-level plan review, revise valid findings, and hand the reviewed plan to the user before implementation. Use when the user explicitly invokes $managed-plan, asks for the planning phase of a managed workflow, or wants a reviewed plan/checklist artifact for later execution. Do not use for ordinary informal planning or small one-shot tasks.
---

# Managed Plan

Research, draft, review, and hand off the planning phase for a managed workflow. Stop before implementation; this phase only creates safe planning artifacts and review handoff.

## Shared Setup

`PHASE_SKILL_DIR` is the absolute directory of this `SKILL.md`. Resolve `WORKFLOW_SKILL_DIR` before reading shared references or running scripts: a user-provided `managed-workflow` path if given, else the sibling `managed-workflow` directory next to `PHASE_SKILL_DIR`. Always use an absolute path, never `../managed-workflow/...` relative to the shell cwd.

Read:

- `$WORKFLOW_SKILL_DIR/references/workflow-contract.md`
- `$WORKFLOW_SKILL_DIR/references/agents.md` before spawning reviewers
- `$WORKFLOW_SKILL_DIR/references/hard-stops.md` before risky or ambiguous operations
- `$PHASE_SKILL_DIR/references/plan-review.md` for review levels, reviewer prompts, Claude CLI review, and report content

If no workflow directory exists, create one with:

```bash
python3 "$WORKFLOW_SKILL_DIR/scripts/new_workflow.py" "Task title"
```

## Planning Loop

### Research

1. Research code, local instructions, existing plans, tests, and ownership boundaries.
2. Research external primary sources only when current facts, third-party docs/APIs, regulations, pricing, or referenced pages affect the plan.
3. Separate grounding into observed facts, user requirements, resolved assumptions, and evidence gaps.
4. Identify unresolved decisions, options, alternate paths, missing preferences, or approval questions, and interview the user until they're resolved before drafting.

### Draft

1. Draft or update `workflows/<slug>/plan.md` in problem-solving mode, as a standalone design doc for a skeptical engineer. Use the contract's anchor headings (`Goal`, `Design`, `Implementation Steps`, `Verification / Acceptance`, `Execution Slices`, `Orchestration Notes`) and state one chosen path — no unresolved decisions, options, alternate paths, TODOs, or open questions.
2. Put the full design in `Design`, not in slice prompts: behavior/API/config/data contracts, invariants, ownership boundaries, edge cases, concrete files/functions/tests when known, and the decisions behind the approach. Spend depth where risk or ambiguity is highest; don't paste final code.
3. Before review, apply the skeptical-engineer test: a competent engineer could implement the design without asking a planning question or inventing a core decision. If not, deepen the plan, interview the user, or research more.
4. Define ordered `Implementation Steps` for what must change. Steps can be larger or smaller than slices.
5. Define `Verification / Acceptance`: concrete commands, expected artifacts, acceptance criteria, primary verifier, completion proof, and honest fallback/skip rules.
6. Define `Execution Slices`, picking one execution mode and one main agent role per the contract's `Execution Slices` rules. Give each slice objectives, referenced steps, ownership, dependencies, verification, review gate, artifact expectations, and commit boundaries. For single-agent local work, don't pre-authorize worker prompts, reports, or slice-review artifacts; checklist plus commit/test evidence is enough unless risk-gated review requires a reviewer.
7. Define additional user approvals only for consequential actions that still need sign-off after implementation starts; otherwise keep implementation autonomous after approval.
8. Define orchestration notes: slice order, dependency readiness, artifact creation mode, delegated worker/reviewer agent levels from `agents.md` when agents are planned, retry/re-slice rules, reviewer-unavailable and failed-check behavior, integration policy, and final-quality cleanup routing.

### Review

1. Update `checklist.md` for research status, user-interview status, plan draft status, review level, reviewer identity/thread id, and final-quality gate details.
2. Run the selected review level from `plan-review.md`.
3. Fix valid findings with the smallest change that resolves them. Treat reviewer comments as suggestions: accept only findings that are correct in context and don't undo user-decreed requirements.

### Handoff

Present the reviewed plan to the user with the review level, verdicts, accepted fixes, rejected findings, and a distinct implementation-approval question. Ask whether to start implementation now or revise the plan, then stop and wait for that direct answer. Leave `Implementation approval` as `waiting` until the user directly answers it.

Do not start implementation during this phase. Safe research, scaffolding, plan review, local drafts, and non-destructive checks can proceed autonomously.

## Review Requirement

Plan review is complete only after the selected review level in `plan-review.md` runs. Never present a local self-review as independent review.

If no separate reviewer is available, mark `Plan review: unavailable`, tell the user independent review didn't run, and start implementation only if the user approves after seeing that caveat.

If the user edits or critiques the plan after review, apply the fixes. For high-level review, send materially changed areas back to the same Codex reviewer/thread (don't run a second Claude review unless asked). For low-level review, don't add an automatic re-review loop; upgrade to high-level only on user request or material new risk.

Plan feedback is not implementation approval: edits, critiques, approving comments, and reviewer-fix discussions keep the workflow in planning. After applying feedback, re-present the changed areas and ask the approval question again. Only an affirmative choice to start counts; treat praise, an ambiguous reply, or a new question as still `waiting`.

## Handoff

Before stopping, ensure:

- `plan.md` is the source of truth for the goal, reviewed design, implementation steps, verification/acceptance, execution mode/role, slices, orchestration notes, additional user approvals, and hard stops.
- `checklist.md` records plan-review status, reviewer identity/status, rejected findings, implementation-approval state, and approval evidence when present.
- The user has seen the reviewed plan, review level, verdicts, material fixes, rejected findings, any skipped-review caveat, and the implementation-approval question.

Only mark `Implementation approval: approved` when the user directly answers the approval question, or the original request explicitly pre-authorized skipping it. If plan review is unavailable, approval must follow the skipped-review caveat.
