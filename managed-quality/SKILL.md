---
name: managed-quality
description: Run the final managed code cleanup after implementation to remove AI shaped residue, make each design choice traceable to a real requirement, simplify structure, and reverify behavior. Use when the user explicitly invokes $managed-quality, any managed workflow changes source or test code, a strict workflow reaches its quality phase, or integrated worker changes need a final human quality pass.
---

# Managed quality

Run this as the final code phase after implementation checks pass. Aim for deliberate code whose abstractions, boundaries, branches, and fallbacks follow from the requested behavior rather than generic model habits.

Treat AI shaped code as a quality smell, not a claim about authorship. Base every finding on the requirements, plan, diff, callers, tests, repository constraints, or observed UI behavior.

## Setup

`PHASE_SKILL_DIR` is the absolute directory containing this file. Resolve `WORKFLOW_SKILL_DIR` from a user provided path or the sibling `managed-workflow` directory. Resolve `IMPLEMENT_SKILL_DIR` as the sibling `managed-implement` directory when cleanup files are needed.

Always read:

- `$WORKFLOW_SKILL_DIR/references/workflow-contract.md`
- `$WORKFLOW_SKILL_DIR/references/verification.md`
- `references/quality-bar.md`

Then load the relevant internal reference:

- Read `references/backend-quality.md` for backend, CLI, library, data, service, script, test, and other general code.
- Read `references/frontend-quality.md` for components, pages, styles, browser behavior, and user interface code.
- Read both for a mixed change.

Do not load the external source skills at runtime. These internal references contain the distilled rules needed for this phase.

Read `$WORKFLOW_SKILL_DIR/references/agents.md` only when using a fresh reviewer or cleanup worker. Read `$IMPLEMENT_SKILL_DIR/references/slice-artifacts.md` only when durable cleanup files are needed.

## Preconditions

Inspect the plan, checklist, full integrated diff, and verification evidence. Require `Implementation: complete` and `Verification: passed`.

Run this phase for every managed change to source, test, or user interface code. Set `Quality: not-required` only when no maintained code changed, the changed output is generated from an unchanged source, or the user explicitly skips this phase.

## Audit and cleanup

1. Establish the intent contract. Start with the requested behavior, plan, real callers, data, states, failure rules, and non goals. Use nearby code and repository conventions when they provide relevant constraints.
2. When the code is new and has no useful precedent, write a short greenfield contract before judging it. State the owner, data model, supported states, error behavior, required extension points, and choices that are intentionally out of scope.
3. Review the whole integrated diff. Do not review each worker change in isolation because the combined result may duplicate concepts or contradict the intent contract.
4. Apply the shared quality bar first. Look for a simpler framing that deletes branches, wrappers, flags, modes, duplicate helpers, or layers.
5. Apply the backend or frontend reference. Group repeated symptoms under their common cause.
6. Let the main agent perform the normal final audit. Use one fresh reviewer when the path is strict, several independent worker changes interact, or the user asks for independent review.
7. Fix high confidence findings directly. Keep behavior and public contracts stable unless the reviewed plan authorizes a change.
8. Inspect the final diff again. Confirm that cleanup removed complexity instead of moving it into a new abstraction.
9. Set `Verification: pending`, rerun the affected checks, and run the broad verifier when integration could regress.
10. Ask the same reviewer to confirm only material fixes to blocking findings.
11. Set `Quality: passed` and `Verification: passed` only after the cleanup and checks succeed.

Apply small cleanup locally. Delegate a substantial cleanup only when it has a clear ownership boundary. Create packets, results, or review files only when strict evidence, workspace transfer, or resume safety needs them.

## Completion bar

Do not pass code that merely works while leaving a clear local quality regression. Block completion when the diff still contains a high confidence example of:

- a simpler design that would remove meaningful complexity
- generated looking scaffolding with no concrete need
- duplicated or shadow APIs instead of a canonical helper
- special cases, fallback branches, flags, or option bags that obscure the real rule
- code placed in the wrong owner, or a generic design choice with no support from requirements, callers, or repository constraints
- tests or fixtures that make production code handle fake cases
- frontend code that bypasses local components or uses generic visual defaults without product intent

Do not block on personal taste, cosmetic naming, or a theoretical abstraction with no current use.

Report the main cleanup decisions, checks run, and any remaining risk. Update `final-report.md` only when it exists.
