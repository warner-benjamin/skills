---
name: ultraplan
description: Research, challenge, ideate, and decompose complex work into proportional execution plans, plan documents, or activation packets with a chosen direction, evidence, execution-ready work contracts, selective delegation, verification, and completion proof. Use only when the user explicitly invokes $ultraplan, requests rigorous implementation planning or critique before work starts, or wants an execution handoff without activation or implementation.
---

# Ultraplan

Investigate before committing to a solution, push back on faulty premises, choose a direction deliberately, and produce the smallest execution-complete plan that another agent can use immediately.

## Stay design-only

Do not call `create_goal`, update the native plan, implement changes, or mutate external state. Read-only grounding is allowed. Create or update only the single planning artifact selected for the handoff when the user requests a durable artifact. If implementation is requested, finish the plan and state that activation or execution must happen separately.

## Research the real problem

Read repository instructions, named documents, relevant code, callers, tests, history, and live state. Separate the user's desired outcome from their proposed mechanism. Apply normal instruction precedence: current higher-authority instructions and canonical project constraints are binding, while a current informed decision at the same authority may supersede an older one. Separate requirements, observations, assumptions, preferences, and unresolved choices.

Research unfamiliar or consequential details until the decisions they affect are grounded. Prefer repository evidence and primary sources. Stop when more research would not change the plan, verifier, or risk assessment.

Before choosing a direction, keep a compact evidence ledger for consequential claims. Distinguish documented facts, repository observations, experiments, inferences, user decisions, and unresolved assumptions. For each claim, record the exact source anchor, what it establishes, and what it does not establish. Do not base the architecture on an unresolved inference that could invalidate it.

Treat review findings as hypotheses, not requirements. Verify them against the governing source before accepting them, and revise the plan coherently instead of accumulating every suggested mechanism.

Before accepting the proposed mechanism, try to prove it wrong. Verify that the problem exists, the mechanism addresses its cause, the mechanism follows governing constraints, and no simpler existing feature can achieve the outcome. If any check fails, say what is wrong, show the evidence, explain the consequence, and plan a compatible solution for the original outcome.

Handle conflicts proportionally:

- For a current binding incompatibility the user has not knowingly authorized changing, quote the constraint and its recorded rationale, or state that no rationale was found; preserve the desired outcome, propose a compatible alternative, and mark the conflicting mechanism `not ready`. A request to implement the conflicting mechanism is not by itself informed authorization: the request must identify the constraint and accept the material consequence of reversing it.
- When the current request explicitly acknowledges the conflict and tradeoff and has authority to reverse it, plan the reversal and reconciliation of its governing sources without requiring another turn.
- When evidence shows an older decision is stale or superseded, follow current authority and record the reconciliation.
- When the requested mechanism is feasible but materially inferior, recommend the better direction once with evidence; honor the requested direction when the user has already accepted its concrete tradeoff.

Do not make rewriting a governing source a plan step merely to legitimize an unacknowledged contradiction, and do not quietly plan an ineffective, impossible, or needlessly complex solution.

Ask the user only when proceeding requires a different outcome, new authority, or a choice between materially incompatible directions; otherwise use the smallest reversible assumption. When a named target does not match the maintained artifact—or matches only generated, ignored, vendored, or external material—surface the mismatch rather than silently redirecting the plan.

## Explore and choose a direction

Define the observable outcome, baseline, governing sources, constraints, non-goals, and compatibility boundaries. Identify the canonical owners and existing primitives before introducing new ones.

Put the burden of proof on new abstractions, persistent state, coordinators, rollback machinery, and compatibility layers. Introduce one only when a concrete evidenced failure requires it, existing primitives or deterministic rerun cannot handle the failure, and the added mechanism is simpler than keeping behavior local. Prefer one working vertical path before extracting shared machinery; repeated-looking work is not yet a reusable abstraction.

When the direction is non-obvious, develop a small number of materially different approaches. Compare them on outcome fit, conceptual simplicity, local coherence, reversibility, integration work, verification cost, and material risk. Choose one, explain why it wins, and record rejected alternatives only when that prevents the executor from reopening the same decision. Prefer reframing that removes work over elaborate decomposition of avoidable work.

## Build an execution-ready plan

Use two planning layers:

- a concise, dependency-ordered plan of item IDs and one-sentence milestones that exposes the critical path and useful concurrency;
- a separate execution-complete contract for each work item.

Each work-item contract must contain:

- one behavioral objective and why it matters;
- the chosen direction with inline links to the exact governing documentation, repository paths, symbols, callers, tests, and history that constrain it;
- dependencies, stable inputs, ownership, and write boundary;
- invariants, non-goals, required behavior, important edge cases, and ordered pseudocode when sequencing or state transitions could otherwise be invented;
- observable exit condition, exact targeted checks or commands, returned evidence, and stop condition;
- cross-item integration work that the parent must keep.

An item is ready only when a less capable assigned agent can start immediately, work in the intended place and direction, recognize invalid assumptions, and prove completion without inventing requirements. Deepen, split, or return an item to the parent when that test fails. Split by behavioral invariant rather than repository layer. Keep generated artifacts, contract regeneration, work shared between items, and aggregate integration with the parent.

Keep evidence beside the decision or contract it governs rather than only in a detached bibliography. The authoritative artifact must be at least as specific as the conversational explanation; never shorten it by removing details the executor needs.

## Write the plan plainly

Use simple, literal language and the same term for the same concept throughout the plan. Start each section with its conclusion, then give the evidence and consequences. Name the actor, action, target, and condition instead of using a clever label or vague summary. Define an unfamiliar technical term when the executor needs it, and explain enough to prevent the executor from guessing.

Revise the handoff twice. First remove ambiguity, filler, slogans, and unnecessary jargon. Then read the plan as a new executor, remove every clause that adds no useful information, and restore any detail required to implement or verify the work correctly. Plain writing must not make the plan less specific.

## Design verification and risk controls

Select the strongest feasible verifier on the actual user surface, then add regression, safety, quality, and durability checks proportional to risk. Define an iteration loop that inspects evidence, changes one meaningful thing, reruns the relevant verifier, preserves results, and chooses the next repair.

Record required environments, credentials, tools, devices, authenticated surfaces, and approval gates. Never weaken tests, narrow acceptance, hide failures, substitute mocks for the declared surface, or change the benchmark without approval. Difficulty or uncertainty is not a blocker.

For interactive outcomes, specify the exact surface, build, URL, account type, starting state, reproducible workflow, pass and fail criteria, evidence, negative and recovery paths, and fallback owner. Require enough clean-state successes to distinguish a fix from luck. Never silently replace an unavailable real-surface verifier with a weaker proxy.

## Assign execution ownership

Keep work with the parent when it is small, unstable, shared across items, or expensive to review. Delegate substantial and isolated work when parallel work, specialized knowledge, separate context, or independent review provides more value than the briefing and review cost.

For a large plan, let the parent define shared contracts first. Then look for a complete implementation and test lane that one agent can own without making more design decisions. Related work inside one lane is acceptable. Parallel lanes must have ready dependencies and separate write boundaries. Group related sequential items into one lane, and name dispatch groups only when work can actually run at the same time.

Assign every delegated lane an exact model and effort. Honor user or governing-source choices; otherwise use this guide. Increase Luna effort for deeper local reasoning, use Terra when the work needs broader knowledge, and use Sol for consequential decisions or reviews. Make the work contract complete before assigning a stronger model. Do not assign several models to compete on the same task.

| Need | Model and effort | Typical use |
| --- | --- | --- |
| Cheap bounded scout | `gpt-5.6-luna`, `medium` | Disposable mapping or mechanical research with cheap failure |
| Default bounded worker | `gpt-5.6-luna`, `high` | Execution-ready feature slices, tests, and clear fixes |
| Difficult bounded reasoning | `gpt-5.6-luna`, `xhigh` or `max` | Coupled reasoning or diagnosis where local knowledge is sufficient |
| Knowledge breadth | `gpt-5.6-terra`, `high` or `xhigh` | Unfamiliar framework, protocol, language, or cross-layer synthesis |
| Difficult broad synthesis | `gpt-5.6-terra`, `max` | Quality-first cross-layer work requiring breadth and maximum reasoning |
| Frontier knowledge | `gpt-5.6-sol`, `high` | Obscure cross-domain priors beyond the normal breadth lane |
| High-consequence decision or review | `gpt-5.6-sol`, `xhigh` | Security, permissions, destructive data work, or consequential concurrency |
| Critical decision or review | `gpt-5.6-sol`, `max` | Explicit critical assurance or unresolved high-risk reasoning |

For each delegated lane, add its role, model and effort, ordered item IDs, dependencies or dispatch group, ownership, checks, and returned evidence. Also state how later work reuses the lane and who reviews it. If delegation does not help, state `parent-owned; no subagents` once. Assignments remain provisional until execution revalidates live models, tools, open compatible agents, and dependencies. Ultraplan never spawns agents.

## Produce one authoritative handoff

Use the form the user requests. Update a named plan document or canonical repository runbook when one governs the work; otherwise return a conversational execution plan or activation packet. Do not create parallel planning state or duplicate an authoritative document.

Return these concerns, combining them when clarity permits:

1. **Decision:** corrected problem framing, outcome, baseline, chosen direction, material pushback, assumptions, and rejected alternatives whose rationale the executor would otherwise reconsider.
2. **Evidence and boundaries:** governing sources, relevant findings, constraints, non-goals, unresolved choices, and approvals.
3. **Execution plan:** concise dependency-ordered milestones followed by execution-ready work-item contracts.
4. **Execution map:** parent-owned work and only justified agent lanes, model assignments, dispatch groups, reuse, review, and cross-item integration.
5. **Verification and risk:** strongest verifier, supporting checks, iteration loop, rules that prevent a weaker test from passing, completion proof, and material risks.
6. **Handoff:** artifact location or conversational authority, readiness gaps, and the exact next action.

Before marking the handoff ready, check the final artifact, not an earlier revision, for source support, internal consistency, contract completeness, verification feasibility, and agreement with the chosen direction. A formatting check or review of a superseded draft is not readiness evidence. After a material rewrite, rerun the checks affected by that rewrite. If any consequential claim, contract, test on the actual user surface, or durable artifact is missing, report the precise readiness gap instead of saying `ready`.

For small work, collapse these concerns to the few lines needed for immediate execution. Do not manufacture alternatives, headings, lanes, models, or review detail. The plan must still resolve every decision a less capable executor would otherwise have to invent.

Add persistent-goal details only when the work benefits from recovery, waiting, or repeated verification, a verifier can fail reliably, and the next repair usually does not require another preference decision. Include an exact objective, blocker standard, completion proof, and either `ready` or the precise readiness gap. Otherwise return the smallest useful ordinary execution plan.
