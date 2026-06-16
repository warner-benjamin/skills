# Plan Review

Use this reference during the `managed-plan` phase.

## Plan Shape

`plan.md` must contain enough detail to guide delegation and verification without becoming a substitute for execution.

Include:

- clear goal and non-goals
- baseline/current behavior
- success criteria
- primary verifier and completion proof
- current context from local research, separated into observed facts, user requirements, and resolved assumptions
- external source assumptions, if any
- constraints and anti-cheating constraints
- risks and hard stops
- approval gates and autonomous execution boundaries
- implementation slices with ownership, dependencies, verification, review, and commit boundaries
- orchestration sequence and branching rules
- integration and verification policy, including when final quality is required or skipped

The plan must contain one chosen path. Do not leave unresolved decisions, options, alternate paths, TODOs, or open questions in `plan.md`. During research, interview the user until these are resolved before running plan review.

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

Ask the reviewer for critical plan review, not implementation. Give the reviewer the plan, relevant local context, known constraints, and expected output shape.

Tell the reviewer that user-decreed requirements are binding. Reviewer comments are suggestions that may be wrong in context; the reviewer may flag conflicts with safety, hard stops, or feasibility, but must not ask to undo user-decreed requirements merely as a preference.

Require this output:

```text
Reviewer identity:
Reviewer agent/thread id:
Verdict: blocking | non-blocking
Critical findings:
Important non-blocking findings:
Missing context or unresolved questions:
Required plan changes:
```

Use this same review format for Codex reviewers, Claude CLI review, and re-review. For Claude, write the response to `reviews/claude-plan-review.md`; record requested model, fallback, skip reason, and related execution metadata in `checklist.md`, not in a separate review schema.

The prompt should still ask reviewers to check grounding, user-decreed requirements, approval gates, slice boundaries, orchestration, verification, and commit boundaries. The reviewer should surface those only when they create an actual finding.

## Responding To Findings

Apply the smallest change that resolves each valid finding. Reviewers tend to suggest added scope, abstraction, or defensive branches; prefer the simplest plan that still meets the goal, and treat "rejected: adds complexity without proportional value" as a legitimate rejection reason. Keeping the plan simple is part of fixing it, not a separate concern.

Never let reviewer feedback override user-decreed requirements by default. If a reviewer appears to conflict with user instructions, either reject the finding with the user requirement cited, or pause for the user only when the reviewer surfaces a real safety, hard-stop, feasibility, or contradiction issue.

If a finding reveals an unresolved decision, option, alternate path, or missing user preference, do not bury that ambiguity in the plan. Interview the user, update the plan to one chosen path, then continue the selected review flow.

## Claude CLI Review

Use this only for high-level review after the fresh Codex plan review and before the manager fix/reject pass. Claude Code's `-p`/`--print` mode prints a non-interactive response and exits. The `--model` flag accepts aliases for the latest model family, including `opus` and, in current Claude Code versions, `fable`; `--fallback-model` works with `--print`.

Fable requires a recent Claude Code build. Before using Fable, check `claude --version` and `claude --help`. Prefer `--model fable --fallback-model opus` when Fable is supported; otherwise use `--model opus`. If the Fable command fails because the model or CLI version is unavailable, rerun once with `--model opus` and record the fallback.

If Claude review cannot run because of missing auth, quota/rate limits, server 5xx errors, unavailable models, or CLI failure, skip the Claude review, record the exact reason in `checklist.md`, and tell the user in the handoff. Do not block safe planning solely on unavailable Claude quota; continue with the manager fix/reject pass and Codex re-review.

Create `reviews/claude-plan-review-prompt.md` with:

- the plan
- relevant checklist state
- observed facts, user requirements, and resolved assumptions
- explicit user-decreed requirements
- Codex initial review findings
- the shared review output format above

Run from the target repository root:

```bash
claude -p \
  --model fable \
  --fallback-model opus \
  --effort high \
  --permission-mode plan \
  --tools "" \
  --no-session-persistence \
  --output-format text \
  < workflows/<slug>/reviews/claude-plan-review-prompt.md \
  > workflows/<slug>/reviews/claude-plan-review.md
```

If Fable is unavailable:

```bash
claude -p \
  --model opus \
  --effort high \
  --permission-mode plan \
  --tools "" \
  --no-session-persistence \
  --output-format text \
  < workflows/<slug>/reviews/claude-plan-review-prompt.md \
  > workflows/<slug>/reviews/claude-plan-review.md
```

## Re-review

Use the same reviewer/thread for re-review when available. Include:

- the original review
- the revised plan
- a short list of accepted fixes
- rejected findings with reasons
- changed areas that need focused review
- explicit confirmation that blocking findings are resolved or still open

Do not mark plan review complete until the selected review level is complete and blocking findings are fixed, explicitly rejected with reasons, or no required independent reviewer is available and the caveat is recorded.
