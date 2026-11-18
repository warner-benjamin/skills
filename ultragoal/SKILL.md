---
name: ultragoal
description: Activate or resume a durable Codex goal and carry authorized execution through verified completion and independent review. Use when explicitly asked to execute with ultragoal.
---

# Ultragoal

Use the native goal to record what the user wants to achieve. Use one plan to carry the work through implementation, verification, independent review, and delivery.

## Establish the objective

Activate only when the user asks to execute with ultragoal. Identify the requested outcome, constraints, acceptance criteria, and final verifier (the check that demonstrates the user's workflow). Use the request to decide whether success requires a local milestone or verification on the target platform. Ask if that distinction changes the verifier and the request leaves it open.

Inspect the active goal before calling `create_goal`. Resume a matching goal. If a different unfinished goal occupies the slot, report the conflict and leave the existing goal in place. For a new goal, record the source of the requirements, outcome, final verifier, and completion condition. Set a token budget only when explicitly requested.

Identify who can run the required checks and what access they need. An unavailable environment or reviewer blocks only work that depends on it. Finish independent work and available checks. If the required check is still pending at handoff, deliver the usable artifact, name who can verify it and how, and keep the goal open.

## Work from the plan

Use the supplied execution plan and its existing items. If none exists, use the native plan when available, or keep one compact progress record. Take the next required item whose prerequisites are satisfied. Investigate a question when its answer could change that item, unblock required work, or affect acceptance.

At a milestone, a material change of direction, or before a long wait, update the plan with just enough to resume:

- The current item and the observable result that closes it.
- The last confirmed result and any commit, check, or running job needed to find it.
- The next concrete action. If blocked, record what would unblock it.

On resume, check the goal and checkpoint against the current repository and any running job. Reuse valid work and evidence. Answer intervening user questions. When the user redirects the work, drop superseded steps and update affected worker assignments before continuing.

When evidence invalidates an implementation choice, record why and revise the affected steps and checks. Keep the user's constraints and acceptance criteria unless the user changes them. If the finish line changes, use the supported goal-editing mechanism or ask the user to update it through product controls. Never mark unfinished work complete to simulate an edit.

## Isolate and commit repository work

For each new Git goal, default to a new `codex/<goal-slug>` branch in its own worktree so parallel goals can proceed independently. Honor the user's checkout choice. If none was given, state the default during initial inspection and proceed. On resume, reuse the recorded branch and worktree.

Inspect the starting checkout and record its path, branch (if any), and commit. When creating a worktree, branch from that commit and record the new branch name and path in the plan. Choose unused names for both. Work, test, and review in the chosen checkout. If worktree creation fails, fix the cause or ask before switching checkouts.

Preserve existing staged, unstaged, and untracked work. If the goal needs uncommitted edits from the original checkout, copy only the required changes, record their source, and keep them distinct in the commit history. Ask if ownership or inclusion is unclear.

Commit each coherent milestone after its checks, including accepted review corrections. Inspect the diff and stage only intended files or hunks. Keep secrets, generated debris, and locally excluded plans out of commits. Record the commit and its verification evidence.

## Implement and verify

Use the smallest design that meets the outcome and project conventions. Prefer existing APIs, owners, data models, and suitable maintained dependencies. Verify behavior you rely on against the dependency version in use. Preserve required compatibility and remove obsolete paths within scope. If compatibility is unclear, inspect affected callers, persisted data, and deployed versions. Resolve internal unknowns at their source. For example, if a worker’s output path is unclear, inspect its handoff or ask the worker. Make routine reversible choices yourself. Ask the user when you need their access, authority, or judgment about the outcome. Explain what their choice would change and give your recommendation when you have one.

When originality is part of the request, draw on the specific setting, mechanics, or audience. If the same idea would fit an unrelated project unchanged, explore a different premise before committing.

Exercise the smallest representative workflow that could disprove the approach before expensive validation. For example, if a CLI option must reach a service, inspect the request built through the CLI. Add tests where existing checks miss changed behavior or a demonstrated risk. For prompts, check the delivered data, roles, tool schemas, and effects. Assert exact wording only when the wording itself is required.

For optimization work, identify the primary measure and any secondary targets from the user’s priorities. Measure a representative baseline and compare candidates under the same conditions. If a secondary gain makes the primary result worse, keep the best verified version unless the user accepts the tradeoff.

If successive attempts leave the outcome unchanged, record what they ruled out. Repeat a check only when it could yield new evidence. Otherwise, try a different explanation or implementation. If none is supported, close that line of investigation and report the best result and remaining gap.

Keep optional ideas outside the accepted scope. Before adding a safeguard, test, or review round, identify the unmet requirement or material risk in the actual workflow. Repeated fixture repairs, safeguards around safeguards, or decisions reopened without new evidence are reasons to reassess and simplify.

Run targeted checks during implementation and broader checks once the work is integrated or acceptance requires them. Reconnect to a running check. After a failure, diagnose and correct the cause before repeating the broader check. Run the declared final verifier on the finished state. Report which user workflow it proves and any surface that still needs verification.

## Coordinate workers

Explicit ultragoal execution authorizes bounded delegation and independent review, subject to user and runtime limits. Keep small or tightly coupled work local. Delegate independent assignments with settled interfaces and one owner per change. Give each worker the absolute worktree path, scope, dependencies, acceptance check, and a way to reach the parent. Use [delegate](../delegate/SKILL.md) for routing and the [implementation brief](references/implementation-prompt.md) for handoff details.

Workers contact the parent when a blocker or decision affects the assignment. At handoff, report changed files, check results, and unresolved issues. Batch related updates. The parent owns scope, architecture, integration, acceptance, and all staging and commits in the worktree workers share. Inspect handed-off changes and verify their integration before starting dependent work.

Continue independent work while workers finish their assignments. When their handoffs are the only remaining dependency, wait for them.

## Review the stable result

Every goal requires a fresh read-only reviewer, including work completed entirely by the parent. Start the reviewer with `fork_turns: "none"`. Use the [final review prompt](references/final-review-prompt.md) and include the user's original request and material updates in their own words. Supply the plan, complete change inventory, evidence, and known gaps. Review all goal commits against the starting commit, plus staged, unstaged, deleted, renamed, and relevant untracked files.

For maintained code, tests, UI, or agent instructions, give the reviewer the absolute path to [quality-review](../quality-review/SKILL.md). Report an installation gap if it is missing. Add a risk-specific review before a consequential action when needed. Add other reviewers only for distinct unresolved risks or at the user's request.

Batch findings and assess their evidence, impact, and simplest sufficient remedy. Resolve critical (P0) and must-fix (P1) findings supported by evidence. Treat improvements (P2) as advisory. After substantive corrections, rerun affected checks and ask the same reviewer to recheck changed behavior and affected interfaces. Carry forward evidence that still holds. Wording or formatting edits that preserve meaning need no rereview. Use a fresh replacement if the reviewer becomes unavailable. If review itself depends on missing evidence, hand off the artifact with review pending. Return to the reviewer when that evidence arrives.

## Deliver and complete

Lead updates and the final handoff with the answer the user came for. In a diagnosis, name the cause in everyday language and give the strongest evidence. If the cause is uncertain, say what the evidence establishes. In an implementation, say what the user can now do and how you checked it. Include internal details when they help the user understand a tradeoff, use the result, or act on a remaining problem.

Provide the artifact or exact launch command and required setup. If the user must perform a check, provide the steps, expected result, and evidence still needed.

For repository work, commit all intended changes. Verify that a separate goal worktree is clean. When working in the user’s original checkout, verify that all goal changes are committed and preserve and report unrelated edits. Report the branch, worktree path, final commit, integration status, and intentional exclusions. By default, deliver the verified branch in its worktree. If a merge was authorized, carry it out when its conditions pass. Inspect the destination, preserve existing changes, and rerun checks affected by integration. Ask only if a consequential choice remains unresolved.

Mark the goal complete once the outcome exists, the required artifacts are delivered, the final verifier passes, and independent review approves the final substantive state. Reconcile outstanding worker and external state first. If only a user or external action remains, record what will unblock the goal and follow the runtime’s criteria for marking it blocked. Honor user-controlled goal status. For a budgeted goal, report final token usage when the runtime supplies it.
