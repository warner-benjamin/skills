---
name: quality-review
description: Review or simplify implementation structure, maintainability, and frontend quality using repository evidence.
---

# Quality Review

Review for structural simplicity, maintainability, local coherence, and frontend product quality. Be ambitious in diagnosis and controlled in execution.

For a review, remain read-only and return prioritized findings plus a verdict. For a cleanup or fix request, investigate and implement high-confidence repairs within the authorized scope, inspect the resulting diff, and verify behavior. When another workflow dispatches this review, follow its review scope and orchestration rules.

## Establish scope and intent

Inspect repository instructions and establish the complete intended review scope. For change reviews, account for staged and unstaged changes, deletions, renames, and relevant untracked files. Honor a requested base/head; do not assume one diff view captures all intended work. Clarify only when the intended scope remains ambiguous.

Read the requirements, callers, tests, and adjacent code needed to understand behavior to preserve, ownership, supported states, and failure boundaries. Identify relevant canonical APIs and local conventions before judging the implementation. Make consequential assumptions explicit; scale this investigation to the change.

- Read [references/code.md](references/code.md) for backend, CLI, library, service, data, script, test, and general implementation code.
- Read [references/frontend.md](references/frontend.md) for components, routes, pages, styles, and browser behavior. Read both for mixed changes.

Verify unfamiliar APIs, packages, defaults, and volatile external facts against lockfiles, repository sources, or primary documentation before relying on them.

## Search for structural simplification

Compare the complete solution with the simplest design that satisfies current requirements, including its setup, operation, and tests. Question the need for mechanisms before recommending repairs or additional safeguards around them. Ask whether a different owner, state model, data shape, or control flow makes whole branches, wrappers, modes, or layers unnecessary. Delete complexity rather than redistribute it. Moving code between files helps only when it improves ownership, cohesion, or understanding.

Recommend a broad restructuring when it is the clearest behavior-preserving remedy. Do not soften a structural problem into naming or line-level nits merely because the larger fix is less convenient.

For a blocking simplification finding, describe the concrete alternative, which mechanisms disappear, and why supported behavior survives. A claim that something could be simpler is insufficient.

Consider deliberate explanations for apparent smells, including established conventions, generated output, compatibility requirements, and public APIs. Findings require repository evidence; do not infer authorship from style or report taste as a defect.

When implementing, make the smallest change that fully removes the root cause. Preserve public contracts and intended behavior unless the user authorizes a redesign. Avoid unrelated rewrites, speculative generalization, novelty-driven frontend changes, and broad style churn.

## Verify the real result

Match verification to the change, using narrow checks before broader integration checks when warranted. Reopen the final diff and confirm the repair removed complexity rather than moving it.

Challenge duplicate coverage, tests tied to private implementation details, and production machinery used only by tests. For proposed test removals, identify retained protection and any meaningful coverage loss.

Do not weaken tests, delete meaningful assertions, replace the declared interaction surface with mocks, or introduce a new verification framework solely for the review. Use the frontend reference for browser and accessibility verification.

## Findings and verdict

Merge repeated symptoms under their root cause. Lead with blocking issues and material structural problems; do not bury them under cosmetic nits.

For each finding, give its priority, file and line, evidence, consequence, recommended remedy, and acceptance check. Explain alternative rationale or uncertainty when it materially affects the conclusion; separate labeled fields are unnecessary.

| Priority | Meaning |
| --- | --- |
| **P0 — Critical** | A demonstrated critical failure requiring immediate attention, such as data loss or a serious security exposure. |
| **P1 — Must fix** | A material correctness, requirements, or structural problem that must be resolved before accepting the reviewed work. |
| **P2 — Improvement** | A supported, worthwhile improvement that does not block acceptance. |

Return all distinct, supported findings, ordered by priority and impact. Do not impose a numerical cap or add findings to fill a quota. Keep any overview brief without omitting findings from the full report. Return no findings when the change is clean.

Treat high-confidence P0 and P1 findings as blocking. Passing tests alone does not establish implementation quality. P2 findings are advisory and do not require user disposition before approval. Do not block on personal taste, cosmetic naming, or theoretical improvements without demonstrated current benefit.

Give a clear verdict and any concrete residual risk or verification gap. For implementation requests, summarize the structural simplification, checks run, and remaining concrete risk.

This review does not replace dedicated security, privacy, migration, or concurrency review where required.
