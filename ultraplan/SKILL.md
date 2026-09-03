---
name: ultraplan
description: Research, challenge, develop directions, and decompose complex work into one evidence-based Markdown execution plan. Include work contracts, verification, completion proof, independent subagent review, and an optional activation packet. Use only for explicit $ultraplan requests, rigorous pre-work planning, critique, or execution handoffs without implementation.
---

# Ultraplan

Investigate the problem and identify decisions that need the user. Resolve other details independently. Produce the smallest execution-complete plan.

## Stay design-only

Do not call `create_goal`, update the native plan, implement changes, or change external state. Read-only research is permitted. Always create or update exactly one authoritative Markdown plan. If the user requests implementation, finish the plan first. State that execution requires separate activation.

## Keep the plan proportionate

Assume that your first plan is too large. Remove work until every item is necessary for the requested outcome.
Do not add architecture, abstractions, compatibility layers, recovery systems, delegation, or tests without a specific requirement or evidenced risk.
Match the design and verification effort to the size and risk of the task. Use normal project checks unless evidence requires more.
Preserve tests that acceptance criteria or evidenced risks require. Do not add tests for hypothetical risks or the appearance of rigor.
For a small change, prefer one direct implementation item and one targeted check. Stop when the plan satisfies the request.

## Research the real problem

Read repository instructions, named documents, relevant code, callers, tests, history, and live state. Separate the requested outcome from the proposed mechanism. Obey current higher-authority instructions and canonical project constraints. A current informed decision can replace an older decision at the same authority. Separate requirements, observations, assumptions, preferences, and unresolved choices. Research consequential details until more research cannot change the plan, verifier, or risk. Prefer repository evidence and primary sources.

### Get version-matched dependency evidence

If a substantial dependency shapes the direction, examine its exact release. Resolve the version from project files or governing constraints first.
If a pinned version exists, use it. For a new unpinned dependency, use the latest stable release that meets compatibility limits.
Download, unpack, or install research copies only under `<project-root>/.external_resources/`. Obey active network and permission controls.
Keep downloads, caches, prefixes, virtual environments, temporary files, and generated files in that directory. Do not use another location.
Prefer official archives, source distributions, registries, and upstream repositories. If direct acquisition is impractical, use a package manager.
If possible, disable install or lifecycle scripts. Do not execute downloaded code only to examine it.
Do not change project manifests, lockfiles, vendored sources, the active environment, or user and global package state.
Do not treat a research copy as a project dependency or implementation change.
Before acquisition, examine `<project-root>/.git/info/exclude`. If `/.external_resources/` is absent, add it. Do not change a tracked ignore file.
If the required repository-local location is unavailable, request approval or report the evidence gap. Do not download to another location.
Organize each acquisition by package and exact version. Record the version, source URL or registry identity, date, and checksum or immutable revision.
Cite exact source files, bundled documentation, release notes, tests, or examples. Use official web documentation only as version-scoped supplementary evidence.
Keep a compact evidence ledger before you choose a direction. For each consequential claim, record:

- Its evidence type: documented fact, repository observation, experiment, inference, user decision, or unresolved assumption
- Its exact source anchor
- What the source establishes
- What the source does not establish.

Do not base the architecture on an unresolved inference that can invalidate it. Treat review findings as hypotheses. Make sure that the governing source supports each finding. Revise the plan instead of accumulating mechanisms. Try to disprove the proposed mechanism. Make sure that the problem exists, the mechanism corrects its cause, and constraints permit it. Also make sure that no simpler existing feature produces the outcome. If a test fails, identify the fault and show the evidence. Explain the consequence and plan a compatible solution. Handle conflicts as follows:

- If the user did not knowingly authorize a change to a binding constraint, preserve the requested outcome. Mark the conflicting mechanism `not ready`. Quote the constraint and its recorded rationale. If the source gives no rationale, state that fact. Propose a compatible alternative. Before a reversal, the user must identify the constraint and accept the material consequence.
- If the current request identifies the conflict and accepts its tradeoff, plan the reversal. Reconcile all governing sources in the same plan.
- If current evidence supersedes an older decision, obey current authority. Record the reconciliation.
- If a feasible mechanism is materially inferior, recommend the better direction once with evidence. Honor the requested direction after the user accepts its tradeoff.

Do not rewrite a governing source only to hide an unacknowledged conflict. Do not plan an ineffective, impossible, or needlessly complex solution. If a named target does not match the maintained artifact, report the mismatch. Also report targets that are generated, ignored, vendored, or external. Do not silently redirect the plan.

## Divide decision work correctly

Use the user for consequential judgments. The AI owns research, repository discovery, technical details, feasibility, dependencies, tests, and implementation mechanics. Before direction selection, identify uncertainties that can materially change:

- The outcome or acceptance criteria
- Product behavior or user experience
- Scope, priority, cost, schedule, or quality tradeoffs
- Compatibility commitments
- Security, privacy, data-loss, or operational risk
- Irreversible actions or external effects
- The choice between materially different directions.

Do not replace a consequential user preference or authority decision with an assumption. Make and label only the smallest reversible assumption. Ask early enough to change the plan. Do not ask for information that research can find. Research enough context before you ask a question. For each question, give the finding, its importance, viable options, material consequences, your recommendation, and the delegated-choice assumption. Ask only questions that can materially change the outcome, direction, scope, acceptance criteria, or risk. Combine related questions. If the plan requires one of these decisions, get the user's decision before you continue:

- A consequential preference
- An incompatible direction
- New authority
- An irreversible consequence.

If `request_user_input` is available, use it. Then wait for the answer. If the tool is unavailable, ask in the final response. Then end the turn. Do not ask required questions in commentary or change modes. Do not continue as though the user accepted a recommendation. After a required question, stop research, acquisition, delegation, direction selection, and artifact writing. Continue only after the user answers. If no answer is required, use the smallest reversible assumption. Label it and state how another answer changes the plan. After initial research, audit each uncertainty. Separate research questions, user preferences, plan-changing answers, and reversible assumptions. Resolve research questions independently. Ask the user about high-impact preferences and authority decisions.

## Explore and choose a direction

Define the observable outcome, baseline, governing sources, constraints, non-goals, and compatibility limits. Find canonical owners and existing primitives first. Require evidence before you add abstractions, persistent state, coordinators, rollback systems, or compatibility layers. Add a mechanism only for a concrete evidenced fault that local behavior or deterministic reruns cannot correct. The added mechanism must be simpler than keeping the behavior local. Build one working vertical path before you extract shared machinery. Similar work does not prove that a reusable abstraction is necessary. If the direction is not obvious, compare a few materially different approaches. Compare outcome fit, simplicity, coherence, reversibility, integration, verification cost, and risk. Choose one direction and explain why it wins. If its rationale prevents repeated debate, record the rejected alternative. Prefer a direction that removes work over complex decomposition of unnecessary work.

## Build an execution-ready plan

Use two layers:

- Write a concise dependency-ordered list of item IDs and one-sentence milestones. Show the critical path and useful concurrency.
- Write a separate execution-complete contract for each work item.

Each work-item contract must include:

- State one behavioral objective and its importance.
- Link the chosen direction to exact governing documents, paths, symbols, callers, tests, and history.
- Record dependencies, stable inputs, ownership, and write limits.
- State invariants, non-goals, required behavior, and important edge cases.
- If sequence or state transitions can be unclear, include ordered pseudocode.
- Define an observable exit condition, exact checks or commands, returned evidence, and a stop condition.
- Keep cross-item integration work with the parent.

A ready item lets a less capable agent start immediately in the intended place and direction. It can detect invalid assumptions and prove completion without new requirements. If an item is not ready, deepen, split, or return it to the parent. Split work by behavioral invariant, not repository layer. Keep generated artifacts, contract regeneration, shared work, and aggregate integration with the parent. Keep evidence beside its decision or contract. The artifact must contain all details that an executor needs.

## Write the plan plainly

Use simple, literal language. Use one term for each concept. Start each section with its conclusion, then give evidence and consequences. Name the actor, action, target, and condition. If the executor needs an unfamiliar technical term, define it. Revise the handoff twice. First remove ambiguity, filler, slogans, and unnecessary jargon. Then read it as a new executor. Remove clauses without useful information. Restore details that implementation or verification requires.

## Design verification and risk controls

Select the strongest feasible verifier on the real user surface. Add regression, safety, quality, and durability checks that match the risk.
Define an iteration loop. Examine evidence, change one meaningful item, operate the verifier again, preserve results, and select the next correction.
Record required environments, credentials, tools, devices, authenticated surfaces, and approval gates. Difficulty and uncertainty are not blockers.
Do not weaken tests, acceptance, or benchmarks. Do not hide errors or replace the declared surface with mocks without approval.
For interactive outcomes, specify the surface, build, URL, account, starting state, and reproducible workflow.
Also specify pass and fail criteria, evidence, negative paths, recovery paths, and a fallback owner.
Require enough clean-state successes to distinguish a correction from luck. Do not replace an unavailable real-surface verifier with a weaker proxy.

## Assign execution ownership

Keep small, unstable, shared, or expensive-to-review work with the parent. If delegation value exceeds coordination costs, delegate substantial isolated work.
Delegation can provide parallel work, specialized knowledge, separate context, or independent review.
For large plans, define shared contracts first. Then find complete implementation and test lanes that require no new design decisions.
Parallel lanes must have ready dependencies and separate write limits. Group related sequential items into one lane. Name dispatch groups only for concurrent work.
Assign each lane an exact model and effort. Obey user or governing choices. Otherwise, use this guide:

| Need | Model and effort | Typical use |
| --- | --- | --- |
| Mechanical execution | `gpt-5.6-luna`, `low` | Exact lookup, running a specified command, applying obvious edits, or checking an explicit condition |
| Cheap bounded scout | `gpt-5.6-luna`, `medium` | Disposable mapping or mechanical research with inexpensive failure |
| Default bounded worker | `gpt-5.6-luna`, `high` | Feature scopes, tests, and clear fixes |
| Difficult bounded reasoning | `gpt-5.6-luna`, `xhigh` | Coupled reasoning or diagnosis with sufficient local knowledge |
| Knowledge breadth | `gpt-5.6-terra`, `high` | Unfamiliar frameworks, protocols, languages, or cross-layer synthesis |
| Difficult broad synthesis | `gpt-5.6-terra`, `xhigh` | Quality-first cross-layer work that requires maximum breadth and reasoning |
| Frontier knowledge | `gpt-5.6-sol`, `high` | Obscure cross-domain knowledge outside the normal breadth lane |
| High-consequence decision | `gpt-5.6-sol`, `xhigh` | Security, permissions, destructive data work, or consequential concurrency |
| Critical decision | `gpt-5.6-sol`, `max` | Critical assurance or unresolved high-risk reasoning. You should rarely need `max` reasoning. |

Increase Luna effort for deeper local reasoning. Use Terra for breadth. Use Sol for consequential decisions or reviews.
Complete the work contract before you assign a stronger model. Do not assign competing models to the same task.
For each lane, record its role, model, effort, ordered items, dependencies, dispatch group, ownership, checks, evidence, reuse, and reviewer.
If implementation delegation adds no value, write `parent-owned implementation; no implementation subagents` once.
Assignments stay provisional until execution revalidates models, tools, compatible agents, and dependencies. Ultraplan never spawns implementation agents.

## Require independent plan review

Every Ultraplan plan requires one read-only subagent reviewer. Spawn a fresh agent for the initial review, then keep that reviewer for every rereview round. This rule includes small and parent-owned plans.

Explicit Ultraplan invocation authorizes this review delegation.

After the draft becomes coherent, freeze it. Read [references/plan-review-prompt.md](references/plan-review-prompt.md) completely.

Adapt the template with exact plan paths, evidence sources, stable decisions, and mechanisms to challenge. Keep its repeated simplification checks.

Call `functions.collaboration.spawn_agent` directly. Pass the adapted template and use `fork_turns: "none"`. Retain the returned agent ID or canonical task name as the plan's reviewer identity.

Do not give the reviewer the parent's intended verdict. Give only the draft, governing context, decisions, and required review scope.

Dispatch the reviewer after the draft stops changing. The reviewer must have no earlier research, planning, authorship, or review role.

Do not reuse a prior agent for the initial review. Parent self-review does not satisfy this requirement.

The reviewer must remain read-only and must not spawn more agents. The parent owns all plan changes.

Collect all findings before editing the plan. Resolve all must-fix problems and required simplifications together.

Treat must-fix correctness problems and required simplifications as blocking. Treat optional refinements as advisory.

Only a substantive change to the reviewed plan invalidates approval. A substantive change alters the chosen direction, a consequential claim or assumption, a requirement or boundary, a dependency or owner, a work-item contract, the verification strategy, a risk control, readiness evidence, or what an executor will do. After a substantive change, freeze the corrected plan and request a complete rereview from the same reviewer identity.

Do not rereview after an administrative or non-semantic edit. This includes changing the plan status to `ready` after approval, recording the review result, updating metadata or timestamps, formatting, correcting typos or grammar, and rewording that does not change meaning. The completed review authorizes the subsequent status-only change to `ready`.

Use `functions.collaboration.followup_task` with the retained reviewer ID or canonical task name for every rereview. A reviewer that completed its previous turn is idle and reusable; completion does not make it unavailable. Require the reviewer to examine the complete final plan, not only the corrections. Do not call `spawn_agent` for a rereview while that reviewer identity remains available.

If reviewer tools are unavailable, keep the artifact `not ready`. Report the capability gap and end the turn.

Do not replace the reviewer with parent review. Do not present the artifact as final or approved.

If the current user request or higher-priority instructions prohibit all subagents, keep the artifact `not ready`. Report the conflict and end the turn.

Do not mark the plan `ready` until the reviewer approves the complete final plan without blocking findings.

## Produce one authoritative handoff

Always write one Markdown plan. Create a new plan by default. Update an existing artifact only after explicit direction. Presence, tracking, age, or location does not make an existing plan authoritative.
Do not use conversation, native plan state, or another format as the only plan. Do not create parallel planning state.
Do not search for, open, summarize, compare, or reuse existing plans without explicit direction. Before storage selection, inspect only:

- The project root and repository instructions
- The existence and Git status of likely plan directories and `<project-root>/.plans/`
- `<project-root>/.git/info/exclude`.

File names can show a storage convention. Existing plan contents stay out of scope.
If the user or governing instructions name a Markdown artifact, use it. Preserve its tracked status.
Obey an explicit check-in choice. Otherwise, create a new descriptively named plan under `<project-root>/.plans/`. Keep it untracked. Do not ask about storage.
For a checked-in plan, infer the Markdown convention without opening plans. If no convention exists, select a routine location and clear filename.
Do not overwrite another artifact. Do not stage or commit the plan without separate authorization.
If `.plans/` is absent, create it. In a Git worktree, add `/.plans/` to `.git/info/exclude`.
Do not change a tracked ignore file. In a non-Git project, use `.plans/` without a Git exclusion.
If the required directory or exclusion is unavailable, request approval or report the artifact gap. Do not write the plan elsewhere.
The handoff must cover these concerns:

1. **Decision:** Give the corrected problem, outcome, baseline, direction, pushback, assumptions, and important rejected alternatives.
2. **Evidence and boundaries:** Give governing sources, findings, constraints, non-goals, unresolved choices, and approvals.
3. **Execution plan:** Give dependency-ordered milestones and complete work-item contracts.
4. **Execution map:** Give parent work, justified lanes, models, dispatch groups, reuse, review, and integration.
5. **Verification and risk:** Give the verifier, checks, iteration loop, completion proof, safeguards, and material risks.
6. **Handoff:** Give the artifact path, check-in state, readiness gaps, and exact next action.

After the artifact is final, summarize it in two to four prose paragraphs. Link the file and lead with the direction and outcome.
Include major decisions, tradeoffs, important rejected alternatives, boundaries, surprises, gaps, and the exact next action.
Do not make the summary a second plan. Omit routine details and do not list only the artifact sections.
Review the final artifact for source support, consistency, complete contracts, feasible verification, and direction agreement.
A formatting review or superseded draft is not readiness evidence. After a material rewrite, operate the affected checks again.
Report the exact gap for absent claims, contracts, real-surface tests, or durable artifacts.
For small work, keep the plan compact. Do not invent alternatives, headings, lanes, or models. The required independent review still applies.
Resolve all decisions that an executor cannot infer.
Add persistent-goal details only for work that benefits from recovery, waiting, or repeated verification. A reliable verifier must exist.
The next correction must not usually require another preference decision.
Include an objective, blocker standard, completion proof, and either `ready` or the exact readiness gap. Otherwise, use an ordinary execution plan.
