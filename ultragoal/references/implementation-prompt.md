# Implementation brief

Use [delegate](../../delegate/SKILL.md) for routing, ownership, communication instructions, and handoff mechanics. Add this execution context to its worker packet. Omit inapplicable fields. If native plan state is inaccessible, provide the relevant context inline instead of creating a duplicate plan file.

```text
Execution plan: <absolute path, or inline context>
Accepted updates: <decisions or progress that supersede the plan>
Assignment: <coherent component or behavior and observable outcome>
Context: <relevant evidence, entry points, and constraints>
Repository: <absolute goal worktree path, goal branch, and starting commit>
Ownership: <permitted writes and exclusions>
Dependencies: <ready interfaces and downstream consumers>
Acceptance: <required behavior, early integration scenario, and necessary checks>
Parent: <direct parent's canonical task name and communication tool>

Establish how this assignment fits the outcome and accepted decisions. If the plan is inaccessible or conflicts materially with the assignment, report the gap before dependent work. Implement only the assigned scope. If blocked, send the parent the evidence and the decision or dependency you need. Continue any independent part.

Work in the supplied goal worktree. Other workers may be editing this checkout. Keep edits and formatting within your assigned files and preserve others’ changes. Report problems outside your ownership to the parent. The parent handles staging and commits. Stay on the assigned branch and hand off changed files and verification evidence.

Use the smallest sufficient change within agreed interfaces and compatibility requirements. Remove obsolete paths within scope. Do not implement optional ideas from the plan without authorization. Exercise the relevant integration scenario early and run the assignment's necessary checks. Preserve acceptance criteria. Before handoff, inspect the change for unnecessary mechanisms and redundant tests.

Tie added safeguards and test cases to a concrete requirement or evidence-backed risk. Do not invent edge cases or expand the assignment after its acceptance checks pass; hand off the result and any material unresolved gaps.
```

Include any applicable routing or handoff instructions from delegate. Fill in the parent and communication tool available to this worker.
