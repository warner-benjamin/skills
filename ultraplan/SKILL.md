---
name: ultraplan
description: Ground, critique, and decompose proposed durable Codex goals into execution-ready activation packets with explicit outcomes, constraints, dependency-ordered parent and subagent ownership, risk gates, verifiers, and completion proof. Use only when the user explicitly invokes $ultraplan, asks to design or critique a persistent goal before activation, or wants a rigorous implementation plan without starting work or mutating native goal state.
---

# Ultraplan

Design one execution-ready durable objective without activating it. Produce a precise handoff that Ultragoal can validate against live state and execute.

## Remain design-only

Do not call `create_goal`, update the native plan, implement changes, or mutate external state. Do not create a plan, checklist, worklog, or report file unless the user explicitly requests a durable artifact. Read-only inspection and research are allowed when needed to ground the design.

Treat questions, investigations, suspected gaps, critiques, and planning requests as design work even when implementation could follow. If the user explicitly asks to start or continue implementation, finish the activation packet and hand off to `$ultragoal`; do not silently activate from this skill.

## Ground from evidence

1. Read the named repository instructions, governing sources, existing plans or runbooks, relevant code, tests, and current state.
2. Separate user requirements, observed facts, reversible assumptions, and unresolved choices.
3. Record the baseline: the current state, exact failure, or starting metric that completion must improve.
4. Define one observable outcome and meaningful non-goals. Reject objectives that combine independently valuable outcomes without a unifying completion condition.
5. Select the strongest feasible verifier closest to the user's real experience, plus supporting regression, safety, quality, and durability checks proportional to risk.
6. Confirm required environments, credentials, tools, devices, and authenticated surfaces. Do not silently replace an unavailable real-surface verifier with a weaker proxy.
7. Identify approval gates for public, shared, destructive, irreversible, costly, or otherwise consequential actions.
8. State anti-cheating rules: do not weaken tests, narrow acceptance, hide failures, substitute mocks for the declared surface, or change the benchmark without approval.
9. Define completion proof and the true blocker standard. Difficulty, uncertainty, or a long test is not a blocker.

Ask only when a missing answer changes the finish line, grants new authority, or chooses between incompatible outcomes. Otherwise state the smallest reversible assumption.

## Check durable-goal fit

Recommend a durable goal only when progress benefits from repeated attempts, waiting, recovery, or a long feedback loop; a verifier can reliably fail; the next repair can usually be chosen without another preference decision; and completion evidence is stronger than a claim of completion.

Prefer an ordinary task or plan when the work is one-shot, primarily taste-dependent, blocked on repeated human choices, lacks a credible verifier, or permits unbounded external action. If durable goal mode is not recommended, say so and propose the simpler execution shape instead of manufacturing an activation packet.

## Specify the verification loop

Define the loop as: inspect the baseline, change one meaningful thing, run the strongest relevant verifier, preserve the evidence, and choose the next repair. The primary verifier must both distinguish success from failure and return enough evidence to guide that repair.

When the outcome depends on rendered UI, browser or app state, authentication, permissions, native dialogs, files, clipboard, input, focus, notifications, media, accessibility, installation, restart behavior, OS integration, or a multi-app workflow, require verification on the actual interaction surface. Record the exact surface, build, URL, account type, machine or device, starting state, reproducible workflow, observable pass and fail criteria, and evidence to capture. Include clean-state, reload or restart, failure-recovery, and important negative-path checks proportional to risk, plus the fallback owner when Codex cannot access the surface. For flaky or stateful checks, require enough clean-state consecutive successes to distinguish a fix from luck.

## Design dependency-ordered work

Give each work item one immutable behavioral objective, ownership boundary, dependencies, invariants, non-goals, observable exit condition, and targeted checks. Reject an item as too broad when it contains multiple independently testable outcomes or could return useful partial completion. Split by behavioral invariant rather than merely by frontend, backend, repository layer, or milestone label.

Keep cross-item seams, generated artifacts, contract regeneration, and aggregate integration explicitly owned by the future parent executor. Identify which items are independent, dependent, or overlapping.

Order narrow checks before broad gates. Reserve the strongest aggregate verifier for a frozen final state. Place risk-specific review before consequential boundaries and the strict quality review on the frozen aggregate implementation by default.

Return to problem framing when the proposed decomposition requires shared mutable ownership, repeated correction to express, speculative abstractions, or a worker-sized item whose integration contract is still unknown.

## Assign parent and subagent ownership

Treat delegation as an explicit ownership decision for every work item, not as the default for a long plan. Keep an item with the parent when it is the immediate critical-path task, defines contracts for later work, remains architecturally unstable, is small relative to briefing and review cost, crosses several components, shares mutable state, owns integration seams, or could be verified only by substantially repeating the delegated work.

Assign an item to a subagent lane only when it has one execution-ready behavioral outcome, stable dependencies, isolated ownership, explicit non-goals, an independently observable exit condition, targeted checks, and enough work or assurance value to justify transfer and review. Delegation should provide a concrete benefit through independent parallelism, specialized knowledge, context isolation, or independent assurance. Use a single sequential subagent only for a substantial self-contained slice, a genuine specialization need, or required independent review. Use parallel subagents only for dependency-ready lanes with disjoint ownership and write sets.

When the plan contains delegated work or distinct integration and review stages, design execution in waves. A small parent-owned plan may use ordinary dependency order without naming waves:

1. **Parent preparation:** resolve choices, stabilize shared contracts, and complete immediate blockers.
2. **Concurrent execution wave:** dispatch independent subagent lanes together. Schedule dependency-ready parent work in the same wave only when it is outside every agent's ownership boundary, does not depend on their results, and cannot interfere with their files or state; otherwise the parent waits.
3. **Parent integration:** inspect returned work, reconcile seams, run checks, and integrate.
4. **Review wave:** use independent or aggregate reviewers after the intended artifact is frozen.
5. **Parent completion:** remediate, run the strongest final verifier, and assemble completion proof.

Group related sequential items into one reusable lane when they share a role, governing context, ownership boundary, and artifact set. Plan to reuse its implementer for corrections and follow-up checks and its reviewer for remediation confirmation or materially related review. Split lanes for incompatible roles, ownership boundaries, or independently testable outcomes. Keep implementer and reviewer roles separate when independence matters.

### Assign model and effort

Assign every planned subagent lane a model and effort. Honor a user-selected or governing-source selection. Otherwise use this table, increasing Luna effort for reasoning depth, using Terra for missing knowledge breadth, and using Sol for consequential decisions or reviews. Improve an underspecified work packet before choosing a stronger lane; do not plan a serial model tournament.

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

For each planned lane, name its role, exact model and effort, ordered work items, dispatch wave, dependencies, governing context, ownership and write boundaries, invariants, non-goals, exit condition, checks, returned evidence, parent-owned seams, and reviewer relationship. If no delegation is justified, state `parent-owned; no subagents` and explain why.

Do not spawn agents in Ultraplan. Treat every assignment as provisional: Ultragoal must revalidate it against the live repository, available models and tools, open compatible agents, and current dependency state. It may reuse an open agent, collapse a lane into parent work, change a model or effort, or resequence a wave when live evidence invalidates the plan.

## Red-team activation readiness

Before declaring the packet ready, challenge it:

- Can success be faked by weakening or changing the verifier?
- Could the stated outcome be satisfied while missing the user's real result?
- Is completion observable to someone other than the executing agent?
- Does an interactive outcome exercise the correct real surface with available capabilities?
- Are consequential actions separately approval-gated?
- Does the iteration loop define what happens after a failed attempt or external wait?
- Are delegated lanes genuinely bounded and beneficial compared with parent ownership?

Revise the packet or mark it not ready when any answer exposes a material gap.

## Preserve the state boundary

Prefer canonical repository design documents, delivery runbooks, and task plans already named by the user. Treat the activation packet as a conversational handoff, not a second workflow state machine. Do not duplicate an authoritative runbook into generated files.

When the user requests a durable plan artifact, update the named canonical document or create exactly one clearly governed artifact. State how Ultragoal should reconcile it with native goal and plan state.

## Return the activation packet

Scale the packet to the work. For a small parent-owned goal, keep each concern to a sentence where possible, combine adjacent concerns when clarity is preserved, state `parent-owned; no subagents` once, and omit inapplicable lane, model, wave, and reviewer detail. Expand sections only when complexity, delegation, risk, or handoff value justifies it; do not manufacture ceremony to fill the template.

Return these concerns in order:

1. **Fit:** recommend a durable goal or a simpler execution shape, with a concise rationale.
2. **Outcome and baseline:** the observable result, user requirements, and current failure or starting metric.
3. **Governing sources and current evidence:** authoritative documents, code, tests, and relevant state.
4. **Constraints and non-goals:** scope boundaries, authority, and excluded outcomes.
5. **Assumptions and unresolved choices:** distinguish reversible assumptions from activation blockers.
6. **Verifier, iteration loop, and completion proof:** exact strongest surface and workflow, supporting checks, anti-cheating rules, repair evidence, and evidence required to finish.
7. **Dependency-ordered work:** execution-ready work-item contracts and parent-owned integration seams.
8. **Execution ownership and subagent map:** the parent-owned items plus every planned lane's role, model and effort, work items, wave, dependencies, boundaries, checks, evidence, reuse, and review relationship; or `parent-owned; no subagents` with rationale.
9. **Risk and approval gates:** consequential boundaries and required review.
10. **Exact objective:** a compact native-goal objective naming the outcome, governing source, strongest verifier, and completion condition.
11. **Proposed native plan:** concise ordered steps suitable for `update_plan`, kept pending so activation can select the first dependency-ready step; add owner and wave labels only when the execution map uses them.
12. **Activation readiness:** state `ready`, `not recommended`, or name the exact unresolved choice, unavailable verifier, missing authority, or incomplete contract preventing activation.

Do not claim readiness when a material choice still changes the finish line. Do not activate or mutate native state.
