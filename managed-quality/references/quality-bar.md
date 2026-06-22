# Final Code Quality Review

Use this for the final quality gate after integrated code changes already pass verification. Its job is to catch structural drift from multi-slice or multi-agent implementation, not to repeat per-slice correctness review.

## Review Charge

Review the final diff against the plan and ask whether the implementation can preserve behavior while becoming smaller, clearer, more direct, or better aligned with the existing architecture.

Do not accept a cleaner version of the same unnecessary idea. Hunt for the reframing that makes whole branches, modes, layers, helpers, or special cases disappear and leaves the result feeling inevitable.

Good cleanup usually deletes an unnecessary concept, changes the ownership boundary, reframes the state model, makes related updates atomic, or replaces scattered checks with one canonical flow.

## Primary Questions

- Is there a simpler behavior-preserving reframing that deletes meaningful complexity?
- Did the diff improve or worsen the local architecture?
- Did it add special-case branching where a clearer model or ownership boundary should exist?
- Is the logic in the canonical file, package, service, or component?
- Is any new abstraction earning its keep, or is it just a wrapper?
- Did the change introduce unnecessary casts, optionality, loose object shapes, flags, or silent fallbacks?
- Did it duplicate an existing helper or miss a canonical helper?
- Did this diff push a file from below 1000 lines to above 1000 lines without a real ownership reason?
- Is orchestration more sequential, partial, or brittle than it needs to be?

## Distinctive Flags

Flag aggressively when:

- a refactor moved complexity around without deleting concepts a reader must understand
- temporary flags, modes, or branches are likely to become permanent debt
- feature-specific checks are scattered through shared code
- magical generic handling, unnecessary registries, or reflection-like paths hide a simpler direct flow

## Blocking Bar

Block final completion for clear structural regression, avoidable branching growth, wrong-layer logic, duplicate canonical helpers, needless wrapper/cast/optionality churn, unjustified file-size growth, brittle orchestration, or an obvious simpler behavior-preserving design.

Do not block on cosmetic nits when larger structural issues are absent. Prefer a small number of high-conviction findings with concrete cleanup paths.

## Report Content

When a reviewer agent runs, save `reviews/final-quality-review.md` with a verdict, critical findings, important non-blocking findings, missing context or unresolved questions, and required cleanup changes. Exact field names are not important; the report must be actionable enough for the main agent to accept, reject, or turn valid findings into a cleanup slice.
