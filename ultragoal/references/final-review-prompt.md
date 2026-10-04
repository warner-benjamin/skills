# Final review prompt

Use for a fresh read-only reviewer after implementation is stable.
Supply evidence without prescribing a verdict. If native plan state is inaccessible, provide governing context inline.
Omit inapplicable fields.

```text
Execution plan: <absolute path, or inline outcome, approach, and acceptance criteria>
Accepted updates: <settled decisions and scope changes>
Governing sources: <requirements and repository instructions>
Implementation: <workspace, base/revision, and complete intended change inventory>
Evidence: <verification results, tested user workflows, and source/dependency versions>
Delivery: <artifacts, launch instructions, and any required user verification>
Known gaps: <unresolved issues or unavailable checks>
Required review: <absolute quality-review skill path and additional risk scopes>

Establish intent and accepted decisions before reviewing the complete stable implementation.
Include staged, unstaged, deleted, renamed, and relevant untracked files.
Report inaccessible or conflicting governing material as a review gap.

Apply the required review skill. Verify integration and whether the evidence proves the requested user workflow.
Distinguish source approval from installed or deployed behavior.
Verify that required artifacts and instructions make the delivery usable.
Do not replace a required verifier with test totals or a weaker proxy.

Challenge missed requirements, unsupported claims, and unnecessary mechanisms using repository evidence.
Consider existing dependencies and settled compatibility requirements.
For a blocking simplification, give a concrete consequence and a smaller alternative that preserves required behavior.
Do not expand scope or turn advisory wording suggestions into approval gates.

Remain read-only and do not spawn agents. The parent owns corrections.
Return batched findings with source anchors, impact, and useful remedies.
Separate correctness, safety, completion, and material quality blockers (P0/P1) from advisory improvements (P2).
Report evidence you could not verify.

On rereview, inspect changed behavior, affected interfaces, and evidence invalidated by the corrections.
Carry forward valid evidence for unchanged portions. Expand review when changes invalidate earlier conclusions.
Do not reconstruct unchanged investigations or rerun checks without a specific reason.
The verdict covers the complete result, including retained evidence.
Return approved only with no blocking findings or required review evidence gaps. Otherwise, return not ready with exact gaps.
```
