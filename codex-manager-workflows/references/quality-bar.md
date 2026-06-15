# Final Code Quality Review

Use this for the final quality gate after integrated code changes already pass verification.

Purpose: catch structural drift that per-slice reviews miss. Passing tests is required, but not enough if the implementation makes the codebase harder to maintain.

## Review Charge

Perform a deep maintainability audit of the workflow's final diff. Rethink whether the implementation can preserve behavior while becoming smaller, clearer, more direct, or better aligned with the existing architecture.

Be ambitious about simplification. Look for changes that delete branches, helpers, modes, layers, casts, wrappers, or special cases rather than merely rearranging them.

## Non-Negotiable Standards

1. Flag structural regressions.
   - Block changes that make a cohesive module more coupled, stateful, indirect, or harder to scan.
   - Do not approve because behavior works if the structure clearly got worse.

2. Push for simpler reframings.
   - Ask whether a different ownership boundary, data model, or default flow would remove complexity.
   - Prefer deleting concepts over centralizing the same complexity in a new helper.

3. Block random branching growth.
   - Be suspicious of one-off flags, nullable modes, scattered feature checks, and ad-hoc conditionals inserted into unrelated flows.
   - Prefer a dedicated abstraction, policy, state model, or module when the logic has become a concept.

4. Keep logic in the canonical layer.
   - Prefer existing helpers, services, packages, and ownership boundaries over bespoke near-duplicates.
   - Flag feature logic leaking into shared paths or implementation details leaking through APIs.

5. Demand clean type and contract boundaries.
   - Question unnecessary optionality, casts, `any`, `unknown`, silent fallbacks, or loosely shaped objects when a clearer invariant is available.
   - Prefer explicit typed models or shared contracts when they make control flow simpler.

6. Watch file size and decomposition.
   - Treat a change that pushes a file from below about 1000 lines to above it as a presumptive design smell.
   - Prefer focused modules, helpers, or components when the split follows a real ownership boundary.

7. Check orchestration and atomicity.
   - Flag obviously independent work that is serialized in a way that makes the implementation more brittle.
   - Flag related updates that can leave state half-applied when a more atomic flow is clear.

8. Avoid magical or thin abstractions.
   - Block wrappers, registries, generic mechanisms, or reflection-like handling that hide simple structure without buying clarity.
   - Prefer direct, boring code when the abstraction does not pay rent.

## What To Flag Aggressively

- A complicated implementation where a simpler reframing could delete whole categories of complexity.
- Refactors that move complexity around without reducing the number of concepts a reader must hold.
- A file crossing about 1000 lines because of this workflow without a strong structural reason.
- Feature-specific checks scattered across shared code.
- Narrow edge-case handling inserted into an already busy function.
- Duplicate helpers or logic in the wrong package, service, or layer.
- Unnecessary wrappers, casts, nullable params, flags, or generic mechanisms.
- Copy-pasted logic where a local helper or existing canonical helper fits.
- Sequential or partial-update orchestration that is harder to reason about than the obvious alternative.

## Preferred Remedies

- Delete an unnecessary layer of indirection.
- Reframe the state model so conditionals disappear.
- Move logic to the package, module, service, or component that already owns the concept.
- Extract a focused helper or pure function.
- Split a large file along a real ownership boundary.
- Replace condition chains with a typed model, dispatcher, or policy object when it reduces complexity.
- Separate orchestration from business logic.
- Collapse duplicate branches into one clearer flow.
- Reuse the canonical helper instead of adding a near-duplicate.
- Make type boundaries explicit so control flow gets simpler.
- Parallelize independent work when it also simplifies orchestration.
- Make related updates atomic when partial state would be harder to reason about.

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
Orchestration/atomicity concerns:
Required cleanup slices:
Hard-stop recommendations:
Re-review required: yes | no
```

## Completion Bar

Block completion when there is a clear structural regression, avoidable branching growth, wrong-layer logic, duplicate canonical helper, needless wrapper/cast/optionality churn, unjustified file-size growth, brittle orchestration, or an obvious simpler behavior-preserving design.

Do not block on cosmetic nits when larger structural issues are absent. Prefer a small number of high-conviction findings over a long list of style comments.
