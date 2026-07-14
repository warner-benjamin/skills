# Verification

Match checks to the requested behavior and the size of the change. Run narrow checks first, then broaden when integration risk warrants it.

Workers should run the targeted checks for their work item. The main agent should inspect the resulting diff and run implementation verification from the integration workspace before quality cleanup.

Record that result as `Implementation verification`. Keep it as evidence from before quality. `Verification` describes the current tree and becomes pending after any maintained code change.

Do not rerun every worker check automatically. Rerun it when:

- the change came from another workspace or patch stream
- later work could affect the result
- the worker evidence is incomplete or uncertain
- the check is part of the final acceptance criteria

After quality cleanup, rerun the affected checks and the final verifier that proves the cleaned result still meets the request.

When quality is not required and the tree has not changed since implementation verification, reuse that result as final verification. Do not rerun the same check only to create a second status entry.

For a flaky or stateful verifier, reproduce from a clean state and require enough repeated success to rule out a lucky pass. Do not add repetition to stable checks.

If implementation verification fails, set both verification fields to `failed` and keep implementation incomplete. After a code fix, set both to `pending` before rerunning the checks. If final verification after quality fails, set `Verification: failed`, keep the preserved implementation result, and keep quality pending during repair. Set `Quality: failed` only when the phase ends without a successful repair.

Do not weaken tests, narrow acceptance criteria, hide failures, or replace real verification with easier evidence. Record required checks and concise results in `checklist.md`. Report skipped checks with the reason.
