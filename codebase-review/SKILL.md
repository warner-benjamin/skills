---
name: codebase-review
description: Review a codebase in delegated slices for simplification, unnecessary code, overtesting, performance, and maintainability. Preserve findings and consolidate a verified report. Use for broad codebase audits, not routine patch reviews or implementation.
---

# Codebase Review

Review a codebase in delegated slices and produce one verified, prioritized report. Focus on simplification, overengineering, tangled code, excessive abstraction, duplication, unnecessary code and setup, poor performance, and overtesting.

During review, keep implementation and tests unchanged. Write review artifacts and use temporary reproductions outside the source tree. Treat remediation as a separate request unless the user already authorized it.

Use [quality-review](../quality-review/SKILL.md) for review criteria, priorities, and finding format. Use [delegate](../delegate/SKILL.md) for routing, ownership, and acceptance. This workflow authorizes slice reviewers, subject to user and runtime limits. If delegation is unavailable, review sequentially and disclose that limitation.

## Plan slices

Review the current working tree unless the user specifies another baseline. Include relevant untracked files and hidden configuration. Set generated and vendored code apart. Divide the scope into coherent responsibilities, each with its tests, balanced by reasoning burden rather than file count.

Create a review directory at the requested location or under `docs/reviews/<date>-codebase-review/`. Add `index.md` with the baseline, slices, worker names, report paths, exclusions, and status. Keep it current enough to resume after compaction.

## Audit existing documentation

Include these two checks when the corresponding documents exist. Skip missing documents without creating replacements.

- Audit the code map against where the implementation actually lives within its stated scope. Trace important logic, settings, defaults, configuration overrides, and data or control flow to their owners and entry points. Identify stale paths, omissions, and misleading descriptions of where behavior is defined or changed.
- Audit the design document against current implementation, requirements, and recorded decisions. Identify outdated architecture or behavior claims. Distinguish stale documentation from planned work and implementation that violates the intended design.

Record supported discrepancies and recommended corrections in the review reports, with document and code references.

## Review emphasis

In addition to quality-review, apply these priorities in every slice and during consolidation:

- Look for simpler setups: fewer dependencies, services, build stages, adapters, and configuration steps for the same supported workflow.
- Examine performance: hot-path cost, repeated I/O or computation, serialization, startup, builds, and test runtime. Separate measured results from inferred costs.
- Look for overtesting: duplicate coverage, assertions tied to private implementation details, and heavy mocks, fixtures, or matrices for simple behavior. Consider expensive tests whose protection fits a smaller test, and tests of obsolete or unreachable behavior.
- Identify busywork and unnecessary error handling: defensive branches for unreachable states and recovery layers without real failure boundaries. Question production machinery used only by tests.

For proposed test removals, identify the retained protection and any meaningful coverage loss. Do not infer overtesting from test counts or coverage percentages alone.

Distinguish unnecessary machinery from missing or incorrect handling of real obligations. Size or rare use alone does not make handling unnecessary. If simplification requires removal of a supported feature, label that proposal as a product decision.

## Assign reviewers

Give each reviewer the baseline, owned scope, Markdown report path, resolved skill paths, and this review emphasis. Require each reviewer to:

- Apply quality-review to the slice and trace adjacent contracts as needed.
- Create its report early and update it as work progresses: coverage, remaining work, confirmed findings, open questions, and checks run.
- Use finding identifiers prefixed with the slice name.
- Preserve every supported finding in the saved report.
- Save an answer to: "How many of these findings, duplicated work, etc is due to overcomplicating the design with busywork and unneeded error handling?"

Ground that answer in finding identifiers and causal explanations. Distinguish clear cases from partial or uncertain cases.

## Consolidate

Accept completed slices under the delegate rules. Verify consequential claims against source evidence and spot-check other findings. Correct or reject unsupported claims.

Compare coverage with the plan and resolve or disclose gaps. Inspect interactions across slices for duplicated mechanisms, conflicting contracts, and missed simplifications. Merge findings that share a root cause and remedy.

Save brief parent notes on verification, consequential merges or rejections, and remaining work as consolidation progresses. Use the index or draft combined report so compaction does not erase these decisions.

Write `combined.md` with:

- A verdict, reviewed baseline, and strongest simplification opportunities.
- All supported findings, with blockers and material structural problems first.
- Test simplifications and their retained protection.
- Product decisions and verification gaps, separate from confirmed defects.
- An answer to the complexity question across the deduplicated findings, with counts and supporting examples.
- Coverage, exclusions, checks run, and links to slice reports.

Mark unfinished slices explicitly. Do not describe a partial review as complete. Finish with the report link, principal findings, and material limitations.
