---
name: quality-review
description: Perform an unusually strict, evidence-backed quality review or cleanup of backend, general, test, and frontend code. Use when the user explicitly invokes $quality-review, requests a thermo-nuclear or deep maintainability audit, wants AI-shaped code de-slopped, asks for ambitious structural simplification, or needs a final aggregate quality gate after implementation.
---

# Quality Review

Review for implementation quality, structural simplicity, maintainability, local coherence, and frontend product quality. Be ambitious in diagnosis and controlled in execution.

## Select the operation

- For a review, remain read-only and return prioritized findings plus a verdict.
- For a cleanup or fix request, audit first, implement accepted high-confidence repairs, inspect the resulting diff, and verify behavior.
- When called by an Ultragoal parent, review the frozen aggregate change inventory. The parent may select one fresh read-only reviewer when independence is useful. A dispatched reviewer must apply this skill directly and must not delegate the review again; the parent owns fixes and integration.

Do not infer authorship from style. Treat AI-shaped code as a quality smell whose findings still require repository evidence.

## Establish scope and intent

1. Inspect repository instructions and inventory the complete intended change: status, staged and unstaged changes, deletions, renames, and relevant untracked files. Use the requested base/head when supplied, but never assume one diff view contains the whole scope. Ask one narrow question only when the intended file set remains ambiguous.
2. Read the requirements, plan, real callers, data and state models, error rules, non-goals, tests, and relevant adjacent code.
3. Identify the canonical owners, APIs, helpers, components, tokens, and local conventions before judging the change.
4. State the implementation contract: behavior to preserve, supported states and variation, ownership boundaries, failure behavior, and intentionally unsupported flexibility.
5. Load [references/code.md](references/code.md) for backend, CLI, library, service, data, script, tests, and general implementation code.
6. Load [references/frontend.md](references/frontend.md) for components, routes, pages, styles, browser behavior, or other user-interface changes. Load both for mixed changes.

Verify unfamiliar APIs, packages, defaults, and volatile external facts against lockfiles, repository sources, or primary documentation before relying on them.

## Search for code-judo simplification

Do not stop at local cleanup. For every meaningful change, ask whether a different owner, state model, data shape, or control flow would make whole branches, wrappers, modes, flags, helpers, or layers disappear.

Push hard when the diff:

- preserves incidental complexity despite a plausible simpler framing;
- moves complexity between files without reducing the concepts a reader must hold;
- adds special-case branches to an already busy flow;
- scatters feature checks through shared code;
- introduces thin wrappers, identity helpers, speculative factories, registries, extension points, fallback paths, or broad option bags without a concrete need;
- obscures an invariant with optionality, casts, loose objects, boolean modes, or stringly typed state;
- duplicates a canonical helper, DTO, projection, cache, or source of truth;
- places behavior outside the module, layer, or component that owns it;
- serializes independent work or makes related updates non-atomic when a cleaner structure is evident;
- shapes production behavior around fixtures, mocks, sample values, or private test decomposition;
- pushes a file from below 1,000 lines to above it without a compelling cohesive reason.

Prefer the design that feels inevitable in hindsight: direct, boring, typed, explicit, and smaller in concepts. Delete complexity rather than redistribute it.

Treat comments and docstrings as part of the implementation, not decoration. Keep them only when concise and needed to communicate a non-obvious current contract, invariant, boundary, or behavior that clearer code cannot. They must describe the code as it exists, not edit history, prior behavior, review discussion, or why a patch was made. Remove narration of obvious code and prefer clearer names or structure. Preserve required public-API documentation, but keep it terse, accurate, and current.

## Balance ambition with evidence

Recommend a broad restructuring when it is the clearest behavior-preserving remedy. Do not soften a structural problem into naming or line-level nits merely because the larger fix is less convenient.

When implementing, make the smallest change that fully removes the root cause. Preserve public contracts and intended behavior unless the user authorizes a redesign. Do not perform unrelated rewrites, speculative generalization, novelty-driven frontend changes, or broad style churn.

For every suspected AI tell, consider a normal explanation such as an established local convention, generated output, compatibility requirement, or deliberate public API. Reject findings that rest only on taste or provenance guesses.

## Verify the real result

Match verification to the change and run narrow checks before broader integration checks. Reopen the final diff and confirm the repair removed complexity rather than moving it.

For interactive UI, inspect the real browser surface when available. Exercise representative loading, empty, error, long-content, disabled, permission, keyboard, narrow-screen, and recovery states proportional to the change. Distinguish observed browser or accessibility evidence from screenshot-only or source-based inference.

Do not weaken tests, delete meaningful assertions, replace the declared interaction surface with mocks, or introduce a new verification framework solely for the review.

## Output findings

Return every supported P0 and P1 finding for review-only requests, plus up to eight P2 findings. Disclose when additional P2 findings were suppressed. Return fewer when the evidence supports fewer, and return none when the diff is clean. Merge repeated symptoms under their root cause and prioritize:

1. Structural regressions and missed code-judo simplifications.
2. Spaghetti growth, ownership leaks, and state-model problems.
3. Boundary, type, atomicity, safety, and canonical-API problems that harm maintainability.
4. File cohesion, modularity, tests, frontend resilience, accessibility, and product-specific design quality.

For each finding include:

- **Issue**
- **Evidence** with file and line
- **Class:** `P0` for a correctness, safety, or completion blocker; `P1` for a material structural or maintainability regression; `P2` for a worthwhile bounded improvement
- **Root cause**
- **Why it matters**
- **Possible deliberate rationale**
- **Recommended remedy**
- **Acceptance check**
- **Confidence:** `High`, `Medium`, or `Low`

Do not flood the result with cosmetic nits while a structural issue remains. If no blocking finding exists, say so directly and name any residual risk.

For implementation requests, summarize what was structurally simplified, what was deliberately left unchanged, checks run, and remaining concrete risk.

## Approval bar

Do not approve merely because tests pass or behavior appears correct. Block approval on a high-confidence example of:

- a clear behavior-preserving reframing that removes meaningful complexity;
- unjustified spaghetti growth or architecture drift;
- duplicated ownership or a shadow API;
- an unnecessary abstraction, wrapper, cast-heavy contract, fallback, or option bag that makes the design more indirect;
- an avoidable file-size or cohesion regression;
- production behavior coupled to fake cases;
- a frontend that bypasses established product primitives, lacks required real states, or fails basic responsive or accessibility behavior.

Do not block on personal taste, cosmetic naming, or a theoretical abstraction with no current use. This review is a maintainability and product-quality gate, not a substitute for dedicated security, privacy, migration, or concurrency review.

Treat high-confidence `P0` and `P1` findings as blocking. Treat `P2` findings as advisory: disclose them as residual risk without requiring user disposition before approval.
