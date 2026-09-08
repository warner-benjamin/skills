---
name: ultragoal
description: Activate or resume a durable Codex goal and carry it through verified completion with independent review. Use when explicitly asked to execute with ultragoal.
---

# Ultragoal

Own one objective through implementation, verification, independent review, and completion. Use the native goal for the finish line and the native plan for progress.

## Establish or resume the objective

Activate only for an authorized execution request. Discussion, inspection, or planning about a possible goal does not activate it.

Read the governing instructions, existing plan, and repository state needed to establish the observable outcome, scope, acceptance criteria, and strongest required verifier. Validate existing decisions against current evidence. Confirm that required environments, tools, and review capabilities are available. Resolve material design or readiness gaps before activation; make reasonable reversible assumptions for routine details.

Inspect the active goal before calling `create_goal`. Resume it if it governs the same objective. If another unfinished goal occupies the slot, report the conflict without completing it to make room. For a new goal, record a compact objective with its governing source, outcome, verifier, and completion condition. Set a token budget only when explicitly requested. Initialize the native plan and start the first ready item.

On resume, reconcile the goal, governing sources, plan, repository, and existing completion evidence. Preserve valid work and continue from the next dependency-ready item. Keep status, evidence, and next actions in the native plan; create additional tracking files only for requested artifacts or an external handoff.

Record compatible changes in the plan. If the finish line must change, use the supported goal-editing mechanism; when the runtime cannot edit an active objective, ask the user to change or replace it through product controls. Do not simulate an edit by marking unfinished work complete.

## Execute and adapt

Use the simplest design that satisfies the agreed outcome and project conventions. Reuse existing owners, APIs, and data models. Keep related behavior together and control flow explicit. Before adding branches, flags, wrappers, or layers, consider whether changing the data shape or placing behavior with its owner removes the need. Introduce abstractions only for current requirements or demonstrated duplication that they materially simplify. Do not build speculative extension points, configuration, compatibility paths, or fallback behavior. When replacing behavior, remove obsolete paths within the agreed scope; retain parallel paths only for an explicit compatibility or migration need, with a clear retirement condition when temporary.

Prefer established, maintained libraries with evidence of production use over custom implementations of solved problems. Check existing project dependencies first. Assess fit, compatibility, maintenance, licensing, and integration cost before adding a dependency; use a small local implementation when it is simpler overall. Verify relied-on behavior against the project's exact dependency version. Justify consequential custom implementations when a suitable library exists.

Preserve settled backward-compatibility decisions. If compatibility is not already settled by the user or governing requirements, ask the user whether it is needed unless the evidence clearly shows it is unnecessary. Identify affected callers, public APIs, persisted data, or deployed versions and explain the tradeoff. Continue independent work while awaiting the answer, but do not implement compatibility-dependent changes until it is resolved. Record the required scope and any migration or retirement conditions in the plan; when compatibility is unnecessary, implement the direct change without compatibility machinery.

Order work by dependencies and give each item observable completion criteria and appropriate checks. Revalidate planned delegation against current scope, tools, and available workers. Keep small or tightly coupled work local; parallelize independent work with separate ownership. The parent owns scope, architecture, integration, verification, and acceptance.

Inspect delivered changes and verify the integrated behavior before accepting an item or starting work that depends on it. Preserve unrelated work. Make required commits and artifacts within the authorized scope, and record concise evidence in the plan.

Replan when evidence invalidates the approach, accepted behavior regresses, or repeated corrections stop reducing the failure or improving the diagnosis. Gather related findings and correct the cause. Update dependencies, ownership, and acceptance checks before continuing. Ask the user only when a decision changes the agreed outcome or requires additional authority.

## Delegate with clear ownership

Explicit ultragoal execution authorizes bounded implementation delegation and the required independent review, subject to user and runtime limits. Delegate only when the benefit exceeds transfer and integration costs.

Honor requested models and efforts. Otherwise use these starting points among available configurations:

| Work | Model and effort | Typical use |
| --- | --- | --- |
| Mechanical execution | `gpt-5.6-luna`, `low` | Exact lookup, specified command, obvious edits, or checking an explicit condition |
| Cheap bounded scout | `gpt-5.6-luna`, `medium` | Scouting, evidence extraction, or mapping with explicit questions and cheap verification |
| Clear bounded implementation | `gpt-5.6-luna`, `high` | Small feature scopes, tests, and clear fixes with explicit acceptance criteria |
| Code exploration | `gpt-5.6-terra`, `medium` | Retrieve and connect evidence across unfamiliar code, trace dependencies, and ask the parent for guidance or decisions |
| Moderately difficult work | `gpt-5.6-terra`, `high` | Bounded reasoning or implementation benefiting parent guidance on major decisions |
| Substantial coder | `gpt-5.6-sol`, `medium` | Substantial but bounded implementation, tests, repository fixes, or moderately difficult reasoning |
| Frontier knowledge | `gpt-6-astra`, `low` | Obscure cross-domain knowledge or a hard task with a clear approach and checks |
| Ambiguous or consequential judgment | `gpt-6-astra`, `medium` | Synthesis, diagnosis, design, independent review, or permissions, data, and concurrency decisions |
| Critical reasoning | `gpt-6-astra`, `high` | Interacting high-risk constraints or a consequential reasoning or security decisions |

Use the [implementation prompt](references/implementation-prompt.md) for implementation workers, adapting it to the assignment and worker. For other delegated tasks, adapt it to the requested deliverable.

Use collaboration tools directly. Prefer `fork_turns: "none"` with a complete brief; use history when needed. Full-history forks inherit model and effort and cannot take overrides.

Before dispatching any subagent, including implementation workers and independent reviewers, briefly announce its task, selected model, and reasoning effort level in the commentary channel. Report inheritance honestly when exact values are hidden. Related dispatches may share a notice.

Keep the user informed through the commentary channel as coordination happens, including during independent review. Use one short sentence to summarize what you are messaging agents about, questions or blockers subagents raised, and the guidance, decisions, or follow-up you send back. Include material handoffs and review findings; related exchanges may share an update. Summarize the substance instead of copying agent transcripts.

While a worker owns active work, do only independent parent work. Do not inspect its files or sources to monitor progress, duplicate research, or anticipate its result. Inspection requires completed work, an explicit stable handoff, or a concrete guidance request; inspect only the delivered portion or what answers the question. Review access does not transfer implementation ownership. Coordinate unexpected dependencies through messages and bounded handoffs.

When independent work is exhausted, call `collaboration.wait_agent(timeout_ms: 1500000)` to wait up to 25 minutes. Agent messages, updates, completion notifications, or new user input return the wait early; messages arrive separately from the wait result. Handle material questions and handoffs, then wait again if needed. An early return does not mean the worker has finished, and a timeout does not authorize cancellation or restart. Continue until required handoffs and acceptance are complete.

Worker completion is not acceptance. Inspect the deliverable against the behavioral requirements and verify consequential or unsupported claims. Use reported checks where sufficient; run integration checks where needed. Batch related corrections into `followup_task` for the same compatible agent, keeping ownership through acceptance. If a fix is simpler to make locally than to explain and delegate, take ownership of that correction after the worker's handoff, make it, and verify it. Use `send_message` for active-work guidance. If work becomes unsafe or invalid, interrupt and reconcile partial results before transferring ownership.

Permit nested delegation only when it helps and the worker can manage children within shared capacity and user limits. Give each child a non-overlapping subset of the worker's scope and carry these briefing, ownership, communication, waiting, and acceptance rules into its instructions. The worker remains responsible for the full deliverable. Relay child task and model/effort notices through direct parents to the root for a concise user update.

## Verify the result

Add tests for changed behavior, meaningful failure modes, or demonstrated regressions that existing checks do not adequately cover. Prefer observable behavior over private implementation details. Avoid tests that mirror the implementation, duplicate existing coverage without a distinct purpose, or require production abstractions solely for mocking. Once appropriate checks and required gates pass, stop testing unless new changes, failures, or unresolved evidence justify more.

Run targeted checks during implementation. Run broader gates when the integrated state is ready or acceptance and risk require them. Continue an existing verifier session instead of launching duplicates. After a broad failure, diagnose and fix it narrowly before repeating the broad check.

Run the declared final verifier on the finished state. Preserve acceptance criteria: do not weaken tests, hide failures, change benchmarks without authorization, or substitute mocks or weaker proxies for the required user surface. Report an unavailable required verifier as a completion gap.

## Obtain independent review

Every goal requires a fresh read-only subagent to review the complete stable change, including parent-only implementations. At initial dispatch, the reviewer must be created with `fork_turns: "none"`. Reuse that reviewer for rereviews so it retains the review context. Use the same `collaboration.wait_agent(timeout_ms: 1500000)` to wait for the reviewer.

Use the [final-review prompt](references/final-review-prompt.md) to have the reviewer read the plan before assessing the complete implementation. Supply the governing sources, evidence, unresolved issues, and intended change inventory, including staged, unstaged, deleted, renamed, and relevant untracked files; a branch diff alone may omit work.

For changes to maintained code, tests, UI, or agent instructions, require the reviewer to apply [quality-review](../quality-review/SKILL.md) directly, providing its absolute path in the brief. A missing required skill is an installation gap. Include dedicated security, privacy, migration, concurrency, or external-effect review where the work requires it; perform such reviews before the consequential action. Quality review does not replace them.

Collect findings before making corrections. Resolve correctness, safety, completion, and other blocking findings, including `P0` and `P1`. Treat `P2` findings as advisory unless acceptance requirements make them necessary.

After substantive corrections, rerun affected checks and use `followup_task` with the same reviewer to reassess the complete revised change. Meaning-preserving wording, formatting, and recording approval do not require rereview. If the reviewer is unavailable, use a new fresh reviewer. Keep the reviewed implementation stable through final verification and completion.

## Complete with evidence

Mark the goal complete only when the observable outcome exists, required work and artifacts are finished, blocking findings are resolved, final verification passes, and independent review approves the final substantive state. Reconcile outstanding agent work and current repository or external state before changing goal status.

Follow the runtime's blocked-status rules; temporary difficulty or unfinished useful work is not a blocker. Preserve user-controlled goal status. Report the outcome, strongest completion evidence, important review changes, and remaining advisory risks. Include final token usage for a budgeted goal when the runtime supplies it.
