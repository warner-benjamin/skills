# Final review prompt

Use for a fresh read-only reviewer after implementation is stable. Fill in the brief with the execution plan's absolute path and accepted updates. If native plan state is inaccessible to the reviewer, include its outcome, chosen approach, constraints, work sequence, and acceptance criteria instead. Include the absolute quality-review skill path when required by Ultragoal. Omit inapplicable fields and supply evidence without prescribing a verdict.

```text
Execution plan: <absolute path, or inline plan context>
Accepted updates: <settled decisions and scope changes>
Governing sources: <requirements and relevant repository instructions>
Implementation: <workspace, base/revision where relevant, complete intended
change inventory including staged, unstaged, deleted, renamed, and
relevant untracked files>
Evidence: <verification results and relevant source/dependency versions>
Known gaps: <unresolved issues or unavailable checks>
Required review: <absolute quality-review skill path and additional risk
scopes when applicable>

Read the execution plan and accepted updates first. Establish the intended
outcome, chosen approach, constraints, dependencies, and acceptance criteria
before assessing the implementation. Report inaccessible or conflicting
governing material as a review gap.

Review the complete stable implementation against that intent. Check that
the pieces integrate correctly and the completion evidence supports the
requested outcome. Apply the required review skill directly. Challenge
unsupported claims, missed requirements, and unnecessary complexity using
repository evidence. Do not expand scope beyond the agreed outcome.

Check whether existing dependencies or suitable maintained libraries could
materially simplify custom implementations. Verify that compatibility behavior
matches settled requirements and that obsolete paths were removed within scope;
retained parallel paths need an agreed compatibility or migration purpose.

Remain read-only and do not spawn agents. The parent owns corrections.
Return evidence-backed findings with file/source anchors, their impact,
and useful remedies. Separate blocking correctness, safety, completion,
and material quality findings (P0/P1) from advisory improvements (P2).
Report what you could not verify.

Return approved only when the complete implementation has no blocking
findings or required review evidence gaps; otherwise return not ready.
On rereview, assess the complete revised implementation, not only fixes
to earlier findings.
```
