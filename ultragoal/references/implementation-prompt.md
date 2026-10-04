# Implementation brief

Use [delegate](../../delegate/SKILL.md) for routing, ownership, communication instructions, and handoff mechanics.
Add this execution context to its worker packet. Omit inapplicable fields.
If native plan state is inaccessible, provide the relevant context inline instead of creating a duplicate plan file.

```text
Execution plan: <absolute path, or inline context>
Accepted updates: <decisions or progress that supersede the plan>
Assignment: <coherent component or behavior and observable outcome>
Context: <relevant evidence, entry points, and constraints>
Ownership: <permitted writes and exclusions>
Dependencies: <ready interfaces and downstream consumers>
Acceptance: <required behavior, early integration scenario, and necessary checks>
Parent: <direct parent's canonical task name and communication tool>

Establish how this assignment fits the outcome and accepted decisions.
If the plan is inaccessible or conflicts materially with the assignment, report the gap before dependent work.
Implement only the assigned scope. The full plan supplies context, not ownership of other tasks.

Use the smallest sufficient change within agreed interfaces and compatibility requirements.
Remove obsolete paths within scope. Do not implement optional ideas from the plan without authorization.
Exercise the relevant integration scenario early and run the assignment's necessary checks.
Preserve acceptance criteria. Before handoff, inspect the change for unnecessary mechanisms and redundant tests.
```

Append the applicable worker instructions from delegate, including the actual parent and runtime communication capability.
A model name alone does not establish whether messaging is available.
