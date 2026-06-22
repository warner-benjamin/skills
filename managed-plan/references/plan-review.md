# Plan Review

Use this reference during the `managed-plan` phase.

## Plan Shape

`plan.md` reads like a reviewed design document, not a status form: it carries the full design and decisions needed for implementation, without final code or keystroke-level instructions. Headings are anchors, not boxes — follow the problem's shape, with extra depth where work is risky or subtle and brief grounding elsewhere.

Include:

- `Goal`: objective, non-goals, success criteria, hard stops, additional user approvals, workflow artifact path when relevant
- `Design`: domain-specific narrative — observed facts, user requirements, resolved assumptions, constraints, risks, behavior/API/config/data contracts, invariants, edge cases, ownership boundaries, decisions behind the approach
- `Implementation Steps`: ordered work; for code, name files, functions, tests, migrations, data/config shapes, contract deltas when known
- `Verification / Acceptance`: concrete commands, expected artifacts, acceptance criteria, primary verifier, completion proof, honest fallback/skip rules
- `Execution Slices`: execution mode, main agent role, and implementation/review/verification/commit units with ownership, dependencies, referenced steps, review, checks, commit boundaries
- `Orchestration Notes`: slice order, readiness rules, retry/re-slice rules, reviewer-unavailable and failed-check behavior, integration policy, final-quality routing, reusable artifacts

The plan contains one chosen path — no unresolved decisions, options, alternate paths, TODOs, open questions, or scaffold placeholders such as `<...>`; interview the user during research until they're resolved.

As the review gate, hold the plan to the skeptical-engineer test: a competent engineer could implement the design without asking a planning question or inventing a core decision. Block plans that fail it, including slices defined without enough design or step detail for safe implementation. Slice prompts add local execution context but must not invent core design after this gate.

## Review Level

Choose and record a review level in `checklist.md`:

- `low`: default for narrow, low-risk, single-lane, or familiar work.
- `high`: use when the user requests high assurance, the task is broad/risky, the plan spans multiple agents or subsystems, destructive-risk work is possible, or review failure would be costly.

Low-level review is one fresh Codex review pass plus one main-agent fix/reject pass — no re-review loop. If blocking findings remain after the fix/reject pass, mark the review blocking and ask the user whether to revise the goal, choose high-level review, or stop.

High-level review is:

1. Fresh Codex plan review and one Claude CLI review with `claude -p`, launched in parallel when both reviewer paths are available.
2. Main-agent fix/reject pass for valid Codex and Claude findings after both results return, or after one path is recorded unavailable.
3. Same Codex reviewer/thread re-review of the revised plan, including the Claude findings and main-agent decisions.

Don't run a second Claude review unless the user explicitly asks.

## Reviewer Wait Discipline

For high-level review, launch the fresh Codex reviewer and Claude CLI review in parallel when both are available, then stop and wait. For low-level or same-thread re-review, stop after launching the required reviewer and wait. Don't write a parallel self-review, pre-classify findings, re-read the plan for extra critique, or draft fix/reject notes before the reviewer result exists. The fix/reject pass starts only after the required reviewer output is available or a reviewer path is formally unavailable.

## Reviewer Prompt

Ask the reviewer for critical plan review, not implementation. Give them the plan, relevant local context, known constraints, and expected report content.

User-decreed requirements are binding: reviewer comments are suggestions that may be wrong in context. A reviewer may flag conflicts with safety, hard stops, or feasibility, but must not ask to undo a user-decreed requirement as mere preference.

Require a verdict plus critical findings, important non-blocking findings, missing context/unresolved questions, and required plan changes; include reviewer identity/thread when available. Same expectations for Codex reviewers, Claude CLI review, and re-review. For Claude, write the response to `reviews/claude-plan-review.md` and record model/fallback/skip metadata in `checklist.md`.

The prompt asks reviewers to check grounding, user-decreed requirements, design adequacy under the skeptical-engineer test, implementation-step specificity, additional user approvals, slice boundaries, orchestration, verification, and commit boundaries — surfacing each only when it's an actual finding.

## Responding To Findings

Apply the smallest change that resolves each valid finding. Reviewers tend to suggest added scope, abstraction, or defensive branches; prefer the simplest plan that meets the goal, and treat "rejected: adds complexity without proportional value" as legitimate. Keeping the plan simple is part of fixing it.

Never let reviewer feedback override user-decreed requirements by default. On apparent conflict, reject the finding citing the user requirement, or pause for the user only on a real safety, hard-stop, feasibility, or contradiction issue.

If a finding reveals an unresolved decision, option, alternate path, or missing preference, don't bury it — interview the user, update the plan to one chosen path, then continue the review flow.

## Claude CLI Review

Use only for high-level review, in parallel with the fresh Codex plan review and before the main-agent fix/reject pass. Claude Code's `-p`/`--print` mode prints a non-interactive response and exits.

Inspect `claude --help` first; prefer the latest Fable model with Opus fallback, otherwise Opus. Run in non-editing print mode, redirect to `reviews/claude-plan-review.md`, and give Claude no edit tools.

If Claude review can't run (missing auth, quota/rate limits, 5xx, unavailable models, CLI failure), skip it, record the exact reason in `checklist.md`, and tell the user at handoff. Don't block safe planning on Claude quota — continue with the fix/reject pass and Codex re-review.

Create `reviews/claude-plan-review-prompt.md` with the plan, relevant checklist state, observed facts, user requirements, resolved assumptions, explicit user-decreed requirements, and the shared review expectations above. Don't include Codex's findings — high-level Codex and Claude reviews are independent parallel passes.

Run from the target repo root:

```bash
claude -p --model fable --fallback-model opus \
  < workflows/<slug>/reviews/claude-plan-review-prompt.md \
  > workflows/<slug>/reviews/claude-plan-review.md
```

Adjust flags to the installed CLI if `claude --help` differs; if Fable or fallback flags are unavailable, retry once with Opus. Record any fallback/skip reason in `checklist.md`.

## Re-review

Use the same reviewer/thread when available. Include:

- the original review
- the revised plan
- a short list of accepted fixes
- rejected findings with reasons
- changed areas needing focused review
- explicit confirmation that blocking findings are resolved or still open

Don't mark plan review complete until the selected level is complete and blocking findings are fixed, explicitly rejected with reasons, or no required independent reviewer is available and the caveat is recorded.
