# Plan Review

Use this reference during the `managed-plan` phase.

## Plan Shape

`plan.md` must read like a reviewed design document, not a status form. It should carry the full design and decisions needed for implementation while avoiding final implementation code or keystroke-level instructions.

Use the headings as anchors, not boxes to fill evenly. The plan should follow the problem's shape, with domain-specific subsections and extra depth where the work is risky, subtle, or easy to get wrong. Obvious grounding can stay brief.

Include:

- `Goal`: objective, non-goals, success criteria, hard stops, additional user approvals, and workflow artifact path when relevant
- `Design`: organic domain-specific narrative with observed facts, user requirements, resolved assumptions, constraints, risks, behavior/API/config/data contracts, invariants, edge cases, ownership boundaries, and decisions behind the approach
- `Implementation Steps`: ordered technical work items; for code changes, name files, functions, tests, migrations, data/config shapes, and contract deltas when known
- `Verification / Acceptance`: concrete commands, expected artifacts, acceptance criteria, primary verifier, completion proof, and honest fallback or skip rules
- `Execution Slices`: structured implementation/review/verification/commit units with ownership, dependencies, referenced steps, review, targeted checks, and commit boundaries
- `Orchestration Notes`: slice order, readiness rules, retry/re-slice rules, reviewer-unavailable behavior, failed-check behavior, integration policy, final-quality routing, and reusable artifacts

The plan must contain one chosen path. Do not leave unresolved decisions, options, alternate paths, TODOs, or open questions in `plan.md`. During research, interview the user until these are resolved before running plan review.

For non-trivial implementation, apply the skeptical-engineer test: could a competent engineer implement the chosen design without asking a planning question or inventing a core decision? Block plans that fail this test, including plans that define execution slices without enough design and implementation-step detail for safe implementation. Slice prompts may add local execution context, but they must not invent core design decisions after the plan review gate.

## Review Level

Choose and record a review level in `checklist.md`:

- `low`: default for narrow, low-risk, single-lane, or familiar work.
- `high`: use when the user requests high assurance, the task is broad/risky, the plan spans multiple agents or subsystems, destructive-risk work is possible, or review failure would be costly.

Low-level review is one fresh Codex review agent pass followed by one manager fix/reject pass. Do not run a low-level re-review loop. If blocking findings remain after the fix/reject pass, mark the review blocking and ask the user whether to revise the goal, choose high-level review, or stop.

High-level review is:

1. Fresh Codex plan review.
2. One Claude CLI review with `claude -p`.
3. Manager fix/reject pass for valid Codex and Claude findings.
4. Same Codex reviewer/thread re-review of the revised plan, including the Claude findings and manager decisions.

Do not run a second Claude review unless the user explicitly asks.

## Reviewer Prompt

Ask the reviewer for critical plan review, not implementation. Give the reviewer the plan, relevant local context, known constraints, and expected report content.

Tell the reviewer that user-decreed requirements are binding. Reviewer comments are suggestions that may be wrong in context; the reviewer may flag conflicts with safety, hard stops, or feasibility, but must not ask to undo user-decreed requirements merely as a preference.

Require the reviewer to return a verdict plus any critical findings, important non-blocking findings, missing context or unresolved questions, and required plan changes. Include reviewer identity/thread when available. Use the same content expectations for Codex reviewers, Claude CLI review, and re-review.

For Claude, write the response to `reviews/claude-plan-review.md`; record requested model, fallback, skip reason, and related execution metadata in `checklist.md`, not in a separate review schema.

The prompt should still ask reviewers to check grounding, user-decreed requirements, design adequacy under the skeptical-engineer test, implementation-step specificity, additional user approvals, execution-slice boundaries, orchestration, verification, and commit boundaries. The reviewer should surface those only when they create an actual finding.

## Responding To Findings

Apply the smallest change that resolves each valid finding. Reviewers tend to suggest added scope, abstraction, or defensive branches; prefer the simplest plan that still meets the goal, and treat "rejected: adds complexity without proportional value" as a legitimate rejection reason. Keeping the plan simple is part of fixing it, not a separate concern.

Never let reviewer feedback override user-decreed requirements by default. If a reviewer appears to conflict with user instructions, either reject the finding with the user requirement cited, or pause for the user only when the reviewer surfaces a real safety, hard-stop, feasibility, or contradiction issue.

If a finding reveals an unresolved decision, option, alternate path, or missing user preference, do not bury that ambiguity in the plan. Interview the user, update the plan to one chosen path, then continue the selected review flow.

## Claude CLI Review

Use this only for high-level review after the fresh Codex plan review and before the manager fix/reject pass. Claude Code's `-p`/`--print` mode prints a non-interactive response and exits.

Inspect `claude --help` in the current environment before running the command; prefer the latest available Fable model with Opus fallback, otherwise use Opus. Run Claude in non-editing/print mode and redirect output to `reviews/claude-plan-review.md`. Do not give Claude edit tools for plan review.

If Claude review cannot run because of missing auth, quota/rate limits, server 5xx errors, unavailable models, or CLI failure, skip the Claude review, record the exact reason in `checklist.md`, and tell the user in the handoff. Do not block safe planning solely on unavailable Claude quota; continue with the manager fix/reject pass and Codex re-review.

Create `reviews/claude-plan-review-prompt.md` with the plan, relevant checklist state, observed facts, user requirements, resolved assumptions, explicit user-decreed requirements, Codex initial review findings, and the shared review content expectations above.

Run from the target repository root:

```bash
claude -p --model fable --fallback-model opus \
  < workflows/<slug>/reviews/claude-plan-review-prompt.md \
  > workflows/<slug>/reviews/claude-plan-review.md
```

Adjust flags to the installed CLI if `claude --help` shows different names. If Fable or fallback flags are unavailable, retry once with Opus. Record any fallback or skip reason in `checklist.md`.

## Re-review

Use the same reviewer/thread for re-review when available. Include:

- the original review
- the revised plan
- a short list of accepted fixes
- rejected findings with reasons
- changed areas that need focused review
- explicit confirmation that blocking findings are resolved or still open

Do not mark plan review complete until the selected review level is complete and blocking findings are fixed, explicitly rejected with reasons, or no required independent reviewer is available and the caveat is recorded.
