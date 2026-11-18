# Final review prompt

Use for a fresh read-only reviewer after implementation is stable. Supply evidence without prescribing a verdict. If native plan state is inaccessible, provide governing context inline. Omit inapplicable fields.

```text
User request: <original request and material user updates in their own words>
Execution plan: <absolute path, or inline outcome, approach, and acceptance criteria>
Implementation decisions: <choices made during execution and the evidence behind them>
Governing sources: <requirements and repository instructions>
Implementation: <absolute goal worktree path, starting commit, goal branch/final revision, and complete intended change inventory>
Evidence: <verification results, tested user workflows, and source/dependency versions>
Delivery: <artifacts, launch instructions, and any required user verification>
Known gaps: <unresolved issues or unavailable checks>
Required review: <absolute quality-review skill path and additional risk scopes>

Establish intent and accepted decisions before reviewing the complete stable implementation. Review all goal commits against the recorded starting commit, plus staged, unstaged, deleted, renamed, and relevant untracked files. Do not limit review to the latest commit or the working-tree diff. Report inaccessible or conflicting governing material as a review gap.

Apply the required review skill. Verify integration and whether the evidence proves the requested user workflow. Distinguish source approval from installed or deployed behavior. Verify that required artifacts and instructions make the delivery usable. Do not replace a required verifier with test totals or a weaker proxy.

Check the complete result against the user's request and accepted updates. For each correction, identify the unmet requirement or material risk and cite the evidence. If a simpler design would resolve a blocker, explain the consequence and how it preserves required behavior. Consider removing an unnecessary mechanism before adding safeguards or tests.

Remain read-only and do not spawn agents. The parent owns corrections. Return batched findings with source anchors, impact, and useful remedies. Separate correctness, safety, completion, and material quality blockers (P0/P1) from advisory improvements (P2). Report evidence you could not verify.

On rereview, inspect changed behavior, affected interfaces, and evidence invalidated by the corrections. Carry forward valid evidence for unchanged portions. Expand review when changes invalidate earlier conclusions. Do not reconstruct unchanged investigations or rerun checks without a specific reason.

The verdict covers the complete result, including retained evidence. Approve when blocking findings are resolved and the evidence required for your review is present. List any separate platform or user check still pending for goal completion. If review itself depends on a missing result, return not ready and name that result.
```
