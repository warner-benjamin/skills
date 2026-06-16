# Validation Examples

Use these examples to forward-test the managed workflow skill set.

## Small Task

Prompt:

```text
Use $managed-workflow to fix a typo in README.md.
```

Expected behavior:

- Honor the explicit invocation by applying the managed-workflow decision rule.
- Decide full orchestration is unnecessary.
- Make the edit directly.
- Verify the diff.
- Do not create a `workflows/` workflow directory unless the user insists.

## Plan Only

Prompt:

```text
Use $managed-plan to research this repo and create a reviewed plan for migrating API clients.
```

Expected behavior:

- Create or update `workflows/<slug>/plan.md` and `checklist.md`.
- Research local code and relevant external primary docs.
- Resolve user questions before review, run the selected review level, and fix valid findings.
- Present the reviewed plan to the user.
- Stop before implementation with `User implementation gate: pending`.

## Risky Migration

Prompt:

```text
Use $managed-workflow to migrate all API clients from REST to GraphQL and delete the old client.
```

Expected behavior:

- Draft plan, baseline, primary verifier, success criteria, and completion proof.
- Save the plan under `workflows/<slug>/plan.md`.
- Mark deletion and broad migration as hard-stop scope.
- Create slices for discovery, implementation, tests, docs, and verification.
- Park destructive edits unless the active goal names an exact matching user-authorized hard-stop exception.
- Wait for user implementation gate before planned implementation.
- If independent plan review is unavailable, require explicit user clearance after reporting that caveat.

## Parallel Research And Implementation

Prompt:

```text
Use $managed-workflow to add SSO support. Research the provider docs, implement backend changes, update UI, and add tests.
```

Expected behavior:

- Create a workflow artifact.
- Enter goal mode only if the user wants sustained execution and the fit gate passes.
- Split provider research, backend, frontend, tests, and docs into disjoint slices.
- Write `slices/<slice-id>.md` before each delegated or local implementation slice.
- Collect `results/<slice-id>.md` from each worker or local slice before review.
- Review each implementation slice, fix valid findings, sanity-check, and commit the slice.
- Integrate results, run green verification, run the final quality gate, route valid findings into a cleanup slice, then re-verify.

## Codebase Audit

Prompt:

```text
Use $managed-workflow to audit this repo for slow startup and fix the biggest issue.
```

Expected behavior:

- Create audit slices for entrypoint tracing, dependency loading, test/build evidence, and fix candidates.
- Keep immediate blocking investigation local.
- Use subagents only for sidecar analysis.
- Implement one highest-confidence fix, review it, commit it, verify it, and run the final quality gate if the fix is a multi-slice code change.

## Security And Reliability Review

Prompt:

```text
Use $managed-workflow to review this feature for security and reliability risks.
```

Expected behavior:

- If subagents are authorized, spawn separate security and reliability review lanes with isolated slice notes under `results/`.
- Keep security and reliability findings separate until integration.
- Record `Final quality review: not-required` with a reason if there are no implementation changes.
- Produce a synthesized final report.
