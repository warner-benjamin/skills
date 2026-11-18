---
name: ultraplan
description: Research an objective and write a compact, independently reviewed execution plan. Use when explicitly asked to use ultraplan.
---

# Ultraplan

Resolve the decisions that matter and produce the smallest plan someone can execute. Implement only when the user has authorized execution. During planning, do not create a goal or duplicate the plan in the runtime's task list.

## Establish the outcome

Identify the intended user workflow, constraints, non-goals, and observable completion criteria. Read the repository instructions and evidence that can change the approach. Verify consequential claims against code, callers, tests, and primary sources. Distinguish observations from inferences and unresolved assumptions.

Start with the simplest design that supports the user's workflow, from setup through use, recovery, and delivery. Justify added complexity with a requirement or evidence of a risk. Distinguish user constraints from implementation choices and earlier reviewer suggestions.

Prefer existing owners, APIs, data models, and dependencies. Preserve settled compatibility decisions. If compatibility is unresolved, identify affected callers, persisted data, and deployed versions before proposing a migration. Ask the user only when evidence and existing authority cannot settle a consequential choice. Continue independent planning while awaiting the answer.

Compare external packages when one could remove substantial custom work or address a material limitation. Explain the tradeoffs that affect the choice, such as fit, compatibility, maintenance, licensing, and integration cost. Verify the behavior you rely on in the exact version.

If research will span handoffs or interruptions, start the execution plan now. Record the outcome, decisions so far, and the next open question.

## Gather useful evidence

Before a substantial investigation, name the decision it could change and identify the least costly credible check. Decide which result would change your next step. When evidence or user direction changes a decision, revise the affected tasks and acceptance checks and drop obsolete questions. Stop when more evidence would leave the plan and its checks unchanged.

When you need a source copy, keep it under `<project-root>/.external_resources/` and exclude it through Git's local exclude file. Keep research copies separate from project dependencies and the active environment. Avoid installation scripts used only to inspect source. Record source URLs and exact versions or revisions.

For uncertain integration behavior, identify the smallest representative scenario that can disprove the approach. Examples include first use, cancellation followed by reuse, or configured options reaching an external API. Use existing evidence or an authorized probe. If only execution can settle the decision, schedule that check before work that depends on its result and state how the result will guide that work.

If final verification requires external access or user testing, agree on the milestone and handoff. The plan can be ready for execution while that check is pending. Keep the original acceptance criterion and state who can verify it, when, and how.

## Write the execution plan

Write one Markdown plan at the designated path or under `<project-root>/.plans/`. Keep the default plan untracked through Git's local exclude file. If sandbox permissions block a required local exclude update, request escalation for that write. Do not overwrite unrelated artifacts or commit the plan without authorization.

Keep the main plan sufficient to execute without reconstructing the conversation:

- State the outcome, chosen approach, constraints, settled decisions, and material assumptions.
- Order tasks by dependencies and identify relevant paths, interfaces, and ownership boundaries.
- Give observable completion criteria and the necessary checks for each task.
- Specify the final user workflow, required environment, and evidence that proves completion.
- Include deliverables and an actionable handoff for required user verification.

Cite evidence beside the decision it supports. Point to the relevant code or test, documentation section, or measured result. State what it establishes and identify any assumption that still affects the plan. Link a separate research note only when the executor needs more detail.

Keep optional ideas and deferred alternatives outside required work. Plan approval does not authorize those additions. Scale detail to the task. A small change can need one implementation item and one targeted check.

## Delegate and review

Explicit invocation authorizes research delegation and independent plan review, subject to user and runtime limits. Use [delegate](../delegate/SKILL.md) for routing, briefs, and handoffs. Delegate research when the benefit warrants coordination. Give each agent a distinct question and enough context to investigate independently. Keep coupled questions with one owner. Leave worker selection for implementation to the executor.

Once the draft is stable, dispatch one fresh read-only reviewer with `fork_turns: "none"`. Use the [plan review prompt](references/plan-review-prompt.md). Include the user's original request and relevant updates in their own words, the plan path, and primary evidence. Identify which decisions the user made and which the planner chose. Add reviewers only for distinct unresolved risks or explicit user requests.

Collect the findings before making corrections. Resolve blockers involving correctness, evidence, or unnecessary complexity. Treat wording and style suggestions as advisory. After substantive corrections, ask the same reviewer to recheck the affected parts. Wording-only edits need no further review.

Mark the plan `ready` only after independent approval and resolution of execution blockers. If review is unavailable, report `not ready`, identify the pending review, and say whether any known decision or evidence gap also blocks execution.

## Hand off

Link the plan and state its direction, important tradeoffs, readiness, and exact remaining gaps. Keep execution details in the artifact. If execution is already authorized, continue without requesting permission again. Otherwise, finish at the planning handoff.
