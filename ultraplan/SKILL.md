---
name: ultraplan
description: Research an objective and write a compact, independently reviewed execution plan. Use when explicitly asked to use ultraplan.
---

# Ultraplan

Resolve consequential uncertainty and produce the smallest executable handoff. Keep implementation separate unless the user already authorized execution.
Do not create a goal or duplicate native plan state during planning.

## Establish the outcome

Identify the intended user workflow, constraints, non-goals, and observable completion criteria. Read the repository instructions and evidence that can change the approach.
Verify consequential claims against code, callers, tests, and primary sources. Distinguish observations from inferences and unresolved assumptions.

Compare materially different approaches where the choice affects correctness, user effort, maintenance, or risk.
Evaluate the whole workflow, including setup, consumers, recovery, and delivery. Resolve those priorities before developing detailed tasks.
Prefer existing owners, APIs, and data models.
Remove scope and mechanisms without a requirement or evidenced risk. Preserve settled compatibility decisions and required behavior.
If compatibility is unresolved, identify affected callers, persisted data, and deployed versions before proposing migration machinery.
Ask the user only when evidence and existing authority cannot settle a consequential choice. Continue independent planning while awaiting the answer.

Prefer established, maintained packages with evidence of production use over custom code for solved problems.
Inspect existing project dependencies first. Assess functional fit, compatibility, maintenance, licensing, and integration cost before adding a package.
Verify relied-on behavior against the exact dependency version.
When a suitable package exists, justify a consequential custom implementation in the plan.
Use a small local implementation when it is simpler overall than adding a dependency.

## Gather useful evidence

When consequential claims need source inspection, obtain the relevant repository, documentation, or package version.
Keep research copies under `<project-root>/.external_resources/`, excluded through Git's local exclude file.
Keep those copies separate from project dependencies and the active environment. Avoid installation scripts used only to inspect source.
Record source URLs and exact versions or revisions. Stop research when further evidence cannot change the approach, work, verification, or risk.

For uncertain integration behavior, identify the smallest representative scenario that can disprove the approach.
Examples include first use, cancellation followed by reuse, or configured options reaching an external API.
Use available evidence or an authorized probe to resolve the uncertainty. Otherwise, schedule the scenario early in execution and state the remaining assumption.
Distinguish implementation readiness from required final verification. An unavailable final verifier remains an explicit completion gap.
If external access or user testing controls completion, settle the milestone and handoff before execution. Do not silently weaken acceptance criteria.

## Write the execution plan

Write one authoritative Markdown artifact at the designated path or under `<project-root>/.plans/`.
Exclude a default `.plans/` artifact through Git's local exclude file. Do not overwrite unrelated artifacts or commit the plan without authorization.

Keep the main plan sufficient to execute without reconstructing the conversation:

- State the outcome, chosen approach, constraints, settled decisions, and material assumptions.
- Order tasks by dependencies and identify relevant paths, interfaces, and ownership boundaries.
- Give observable completion criteria and the necessary checks for each task.
- Specify the final user workflow, required environment, and evidence that proves completion.
- Include deliverables and an actionable handoff for required user verification.

Keep detailed research in linked references only when it supports execution. Do not copy source inventories or repeat constraints across tasks.
Separate required work from optional ideas and deferred alternatives. Plan approval does not authorize those additions.
Scale detail to the task. A small change can need one implementation item and one targeted check.

## Delegate and review

Explicit ultraplan invocation authorizes research delegation and one independent plan reviewer, subject to user and runtime limits.
Use [delegate](../delegate/SKILL.md) for routing, briefs, communication, ownership, and acceptance mechanics.
Delegate research only when its value exceeds coordination costs. Prefer coherent questions over many small lookups.
Delegate only independent, non-overlapping questions answerable from the supplied context without ongoing inter-agent communication.
Resolve shared decisions before dispatch. Keep coupled research and synthesis with one owner.
Reserve intermediate messages for unexpected blockers or consequential decisions. Independent review starts from a stable plan handoff.
Record provisional execution scopes and dependencies only where delegation helps. Let execution select workers against current scope and runtime capabilities.

Once the draft is stable, dispatch one fresh read-only reviewer with `fork_turns: "none"`.
Use the [plan review prompt](references/plan-review-prompt.md) with the outcome, plan, evidence, and settled decisions.
Add reviewers only for distinct unresolved risks or explicit user requests.

Batch findings before corrections. Resolve correctness, evidence, and material complexity blockers. Treat optional wording and style suggestions as advisory.
After substantive corrections, reuse the reviewer to inspect changed decisions and affected dependencies or acceptance criteria.
Carry forward valid evidence for unchanged portions. Expand rereview when changes invalidate earlier conclusions.
Do not repeat a full investigation solely to renew approval. Meaning-preserving edits do not require rereview.

Mark the plan `ready` only after independent approval and resolution of decisions or evidence gaps that block execution.
If required review is unavailable, retain `not ready` and report the gap.

## Hand off

Link the plan and state its direction, important tradeoffs, readiness, and exact remaining gaps.
Keep execution details in the artifact. If execution is already authorized, continue without requesting permission again.
Otherwise, finish at the planning handoff.
