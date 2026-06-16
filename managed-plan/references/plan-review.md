# Plan Review

Use this reference during the `managed-plan` phase.

## Plan Shape

`plan.md` must contain enough detail to guide delegation and verification without becoming a substitute for execution.

Include:

- clear goal and non-goals
- baseline/current behavior
- success criteria
- primary verifier and completion proof
- current context from local research
- external source assumptions, if any
- constraints and anti-cheating constraints
- risks and hard stops
- implementation slices with ownership, dependencies, verification, review, and commit boundaries
- integration and verification policy
- final quality review decision or default

## Reviewer Prompt

Ask the reviewer for critical plan review, not implementation. Give the reviewer the plan, relevant local context, known constraints, and expected output shape.

Require this output:

```text
Reviewer identity:
Reviewer agent/thread id:
Verdict: blocking | non-blocking
Blocking findings:
Non-blocking findings:
Unsafe assumptions:
Missing context:
Slice boundary issues:
Verification gaps:
Commit boundary issues:
Required plan changes:
Re-review required: yes | no
```

## Re-review

Use the same reviewer/thread for re-review when available. Include:

- the original review
- the revised plan
- a short list of accepted fixes
- rejected findings with reasons
- changed areas that need focused review
- explicit confirmation that blocking findings are resolved or still open

Do not mark plan review complete until blocking findings are fixed, explicitly rejected with reasons, or no independent reviewer is available and the caveat is recorded.
