# Validation Examples

Use these examples to forward-test this skill.

## Small Task

Prompt:

```text
Use $codex-manager-workflows to fix a typo in README.md.
```

Expected behavior:

- Decide full orchestration is unnecessary.
- Make the edit directly.
- Verify the diff.
- Do not create a `workflows/` workflow directory unless the user insists.

## Risky Migration

Prompt:

```text
Use $codex-manager-workflows to migrate all API clients from REST to GraphQL and delete the old client.
```

Expected behavior:

- Draft plan, baseline, primary verifier, success criteria, and completion proof.
- Save the plan under `workflows/<slug>/plan.md`.
- Request a high-reasoning plan review and fix valid findings before implementation.
- Mark deletion and broad migration as hard-stop scope.
- Create slices for discovery, implementation, tests, docs, and verification.
- Mark final quality review required if code changes span multiple slices.
- Park destructive edits unless the active goal names an exact matching user-authorized hard-stop exception.

## Parallel Research And Implementation

Prompt:

```text
Use $codex-manager-workflows to add SSO support. Research the provider docs, implement backend changes, update UI, and add tests.
```

Expected behavior:

- Create a workflow artifact.
- Enter goal mode only if the user wants sustained execution and the fit gate passes.
- Split provider research, backend, frontend, tests, and docs into disjoint slices.
- Review each implementation slice with a medium-reasoning slice reviewer, fix valid findings, sanity-check, and commit the slice.
- Integrate results, run green verification, run the final quality gate, route valid findings into a cleanup slice, then re-verify.

## Codebase Audit

Prompt:

```text
Use $codex-manager-workflows to audit this repo for slow startup and fix the biggest issue.
```

Expected behavior:

- Create audit slices for entrypoint tracing, dependency loading, test/build evidence, and fix candidates.
- Keep immediate blocking investigation local.
- Use subagents only for sidecar analysis.
- Implement one highest-confidence fix, review it, commit it, verify it, and run the final quality gate if the fix is a multi-slice code change.

## Security And Reliability Review

Prompt:

```text
Use $codex-manager-workflows to review this feature for security and reliability risks.
```

Expected behavior:

- If subagents are authorized, spawn separate security and reliability review lanes with isolated slice notes under `results/`.
- Keep security and reliability findings separate until integration.
- Record an explicit final-quality-review decision: set `required: false` with a reason (e.g. review-only, no implementation changes) rather than leaving it undecided.
- Produce a synthesized final report.
