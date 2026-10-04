---
name: ultragoal
description: Activate or resume a durable Codex goal and carry authorized execution through verified completion and independent review. Use when explicitly asked to execute with ultragoal.
---

# Ultragoal

Preserve one objective through implementation, verification, independent review, and usable delivery.
Use the native goal for the finish line and one plan for progress.

## Establish or resume the objective

Activate only for an authorized execution request. Discussion or planning about a possible goal does not activate it.
Establish the outcome, constraints, acceptance criteria, and required final verifier from governing instructions and current evidence.
Preserve settled decisions unless new evidence invalidates them. Resolve routine reversible choices independently.

Before activation, verify access to required tools, environments, and review capabilities.
If external access or user testing controls completion, establish the deliverable and verification handoff.
Resolve whether the authorized objective is a local milestone or full platform acceptance. Do not remove an agreed gate to make completion easier.

Inspect the active goal before calling `create_goal`. Resume a matching objective.
If another unfinished goal occupies the slot, report the conflict without completing it to make room.
For a new goal, record the governing source, outcome, required verifier, and completion condition.
Set a token budget only when explicitly requested.

Keep progress, evidence, and next actions in the native plan when available.
Otherwise, update the existing execution plan or one compact progress artifact. Avoid parallel tracking files.
On resume, reconcile the goal, plan, repository, and completion evidence. Preserve valid work and start the next ready item.

Record compatible scope updates in the plan. If the finish line changes, use the supported goal-editing mechanism.
If that mechanism is unavailable, ask the user to change the objective through product controls.
Never mark unfinished work complete to simulate an edit.

## Execute the agreed scope

Use the smallest design that satisfies the outcome and project conventions. Prefer existing owners, APIs, data models, and suitable maintained dependencies.
Verify relied-on dependency behavior against the exact version. Remove obsolete paths within scope and preserve settled compatibility requirements.
Do not add speculative abstractions, configuration, fallback paths, or migrations.
If compatibility is unresolved, identify affected callers, persisted data, and deployed versions first.
Ask the user only when a consequential choice exceeds available evidence or authority. Continue independent work while awaiting the answer.

Order work by dependencies and observable completion criteria. Keep optional ideas outside the accepted scope.
Before expensive broad validation, exercise the smallest representative workflow that can invalidate the approach.
Include relevant transitions such as first use, cancellation and reuse, or actual request construction.
If the required environment is unavailable, preserve the verification gap and continue independent authorized work.

Explicit ultragoal execution authorizes bounded implementation delegation and independent review, subject to user and runtime limits.
Use [delegate](../delegate/SKILL.md) for routing, worker briefs, communication, ownership, and acceptance mechanics.
Keep small or tightly coupled work local. Give capable workers coherent components or behaviors with clear interfaces.
Delegate only independent, non-overlapping assignments that can finish without ongoing inter-agent communication.
Settle interfaces and prerequisites before dispatch. Start dependent work only after its prerequisites are accepted.
Keep shared edits, joint design, and work requiring repeated coordination with one owner.
Normally, one assignment and one final handoff suffice. Reserve intermediate messages for unexpected blockers or consequential decisions.
Independent review starts from a stable handoff and does not create overlapping implementation ownership.
Use the [implementation brief](references/implementation-prompt.md) for execution-specific context.
The parent owns scope, architecture, integration, and final acceptance.

Inspect delivered changes and verify integration before accepting dependent work.
If evidence invalidates the approach or corrections stop resolving the cause, revise the plan and ownership before continuing.
Preserve unrelated work. Produce required commits and artifacts within the authorized scope.
Answer intervening user questions without abandoning unfinished authorized execution.

## Limit coordination chatter

Keep parent commentary and inter-agent messages brief and limited to material findings, decisions, blockers, changed interfaces, and usable handoffs.
Batch related updates. Do not narrate every internal exchange.
Omit acknowledgments, repeated plans, unchanged ownership reminders, heartbeat messages, and "still waiting" updates.
Do not request worker status merely to produce a user update.
When independent work is exhausted, use event-driven waits within runtime limits and resume on actionable messages.
For long-running jobs or tests that require polling, use [quiet-polling](../quiet-polling/SKILL.md).
For subagents, use [delegate](../delegate/SKILL.md)'s event-driven waits.
Follow higher-priority runtime update requirements without adding worker chatter or repeating unchanged status.

## Verify the outcome

Add tests for changed behavior or demonstrated risks that existing checks do not cover.
Test observable contracts rather than private implementation details or incidental prompt wording.
For prompts, verify delivered data, roles, tool schemas, and behavioral consequences. Assert exact prose only when its bytes are the contract.

Run targeted checks during implementation. Run broader gates when the integrated state is ready or acceptance requires them.
Use existing evidence for unchanged portions. Continue an existing verifier session instead of launching duplicates.
After a broad failure, diagnose and correct the cause narrowly before rerunning the broad gate.
After appropriate checks pass, stop testing unless changes, failures, or unresolved evidence justify more.

Run the declared final verifier on the finished state. Do not weaken tests, hide failures, or substitute weaker proxies for required verification.
Report exactly which user workflow the evidence proves and which surfaces remain unverified.
Test totals and source approval alone do not establish installed or deployed behavior.

## Review the stable result

Every goal requires one fresh read-only reviewer of the complete stable change, including parent-only implementations.
Start that reviewer with `fork_turns: "none"` and use the [final review prompt](references/final-review-prompt.md).
Supply the governing intent, accepted updates, complete change inventory, verification evidence, and known gaps.
Include staged, unstaged, deleted, renamed, and relevant untracked files. A branch diff can omit intended work.

For maintained code, tests, UI, or agent instructions, require [quality-review](../quality-review/SKILL.md) and provide its absolute path.
If that required skill is missing, report an installation gap.
Add dedicated risk review before consequential actions when the work requires it. Add other reviewers only for distinct unresolved risks or user requests.

Batch findings before corrections. Resolve correctness, safety, completion, and material quality blockers, including P0 and P1 findings.
Keep P2 and advisory wording suggestions nonblocking unless acceptance requirements make them necessary.
Do not turn requested advice into an additional approval gate.

After substantive corrections, rerun affected checks and reuse the reviewer.
Focus rereview on changed behavior, affected interfaces, and evidence invalidated by the corrections.
Carry forward valid findings and verification for unchanged portions. Expand the scope when changes invalidate earlier conclusions.
The verdict still covers the complete result. Meaning-preserving wording and formatting do not require rereview.
If the reviewer is unavailable, use a fresh replacement. Keep the approved substantive state stable through final verification and completion.

## Deliver and complete

Provide the artifact or exact launch command, required setup, and concise verification results.
If user verification remains, provide a short checklist, expected results, and the exact action or evidence needed.
Distinguish completed delivery from pending platform verification. State relevant limitations and whether required changes are committed.

Mark the goal complete only after the outcome exists, required artifacts are delivered, and the declared final verification passes.
Independent review must approve the final substantive state with blocking findings resolved.
Reconcile outstanding agent work and repository or external state before changing goal status.
Follow runtime rules for blocked status and preserve user-controlled status. Required external verification remains incomplete until its evidence arrives.
For budgeted goals, report final token usage when supplied by the runtime.
