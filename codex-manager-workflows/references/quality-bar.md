# Final Code Quality Bar

Use this for the final quality gate after integrated code changes already pass verification.

Purpose: catch AI-shaped structural drift that per-slice reviews miss. Passing tests is required, but not enough if the implementation makes the codebase harder to maintain.

## Review Focus

- Find simpler reframings that delete branches, helpers, modes, or layers.
- Flag ad-hoc conditionals, special cases, one-off flags, nullable modes, and scattered feature checks.
- Prefer canonical helpers, ownership boundaries, and existing architecture over bespoke near-duplicates.
- Question thin wrappers, magic generic mechanisms, cast-heavy contracts, unnecessary optionality, and unclear type boundaries.
- Flag file-size growth, especially changes pushing a file past about 1000 lines without a strong structural reason.
- Check that orchestration is not needlessly sequential and related updates are not left half-applied.
- Prefer behavior-preserving simplification over broad rewrite.

## Output Shape

```text
Verdict: blocking | non-blocking
Files reviewed:
Structural regressions:
Simpler reframing opportunities:
Spaghetti or branching risks:
Boundary/type/abstraction issues:
Canonical helper or ownership misses:
File-size/decomposition concerns:
Required cleanup slices:
Hard-stop recommendations:
Re-review required: yes | no
```

## Completion Bar

Block completion when there is a clear structural regression, avoidable spaghetti growth, wrong-layer logic, duplicate canonical helper, needless wrapper/cast/optionality churn, unjustified file-size blowup, or an obvious simpler behavior-preserving design.

Do not block on cosmetic nits when larger structural issues are absent.
