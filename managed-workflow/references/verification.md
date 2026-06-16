# Verification

Run the narrowest reliable checks first, then broaden as risk warrants.

Common checks:

- unit tests for touched code
- typecheck or lint
- build
- browser or UI smoke test
- script dry run
- source citation check
- migration dry run
- manual checklist for non-code work

Match verification to the plan's success criteria, primary verifier, and blast radius. Do not weaken tests, narrow scope, hide failures, swap in mocks, or change benchmarks without approval.

Record each required check in `checklist.md` with status and evidence. Report skipped checks honestly with the reason.

For flaky or stateful checks, prefer clean-state reproduction and enough consecutive passes to rule out luck.

Do not treat a workflow or active goal as complete until the success criteria and completion proof are satisfied.
