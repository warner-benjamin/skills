# Implementation prompt

Fill in this brief and append the applicable communication paragraph below. Omit fields that do not apply. Provide the execution plan's absolute path and any accepted updates. If the plan exists only in native state inaccessible to the worker, include its outcome, chosen approach, constraints, work sequence, dependencies, and acceptance criteria in the brief instead of creating a duplicate plan file.

```text
Execution plan: <absolute path, or inline plan context>
Accepted updates: <decisions or progress that supersede the plan>
Assignment: <plan item and concrete outcome>
Context: <relevant instructions, evidence, and entry points>
Ownership: <permitted writes and exclusions>
Dependencies: <ready interfaces, handoffs, and downstream consumers>
Acceptance: <observable requirements and necessary checks>
Parent: <direct parent's agent ID or canonical task name>

Read the execution plan and accepted updates first. Understand the overall outcome, chosen approach, constraints, dependencies, and where your assignment fits before inspecting implementation details or editing. If the plan is inaccessible or conflicts materially with the assignment or repository, report the gap before proceeding with dependent work.

Implement only your assigned scope. The full plan provides context, not ownership of other items. Preserve agreed interfaces, unrelated work, and authorization limits. Use the smallest sufficient change and verify the assignment's acceptance criteria without weakening them.

Prefer existing patterns, direct control flow, and clear ownership. Every new abstraction and test must address a concrete requirement or evidenced need. Before handoff, inspect the complete change for unnecessary indirection, duplicated state, scattered conditions, and redundant tests; simplify what you introduced.

Check existing project dependencies before writing custom solutions. Prefer suitable maintained libraries when they simplify the implementation overall;  verify the exact version's behavior and justify consequential custom alternatives. Honor settled dependency and backward-compatibility decisions. Report unresolved compatibility needs to the parent before implementing dependent changes. Remove obsolete paths within scope; retain parallel paths only for agreed compatibility or migration needs, honoring any retirement conditions.

Do not spawn children unless the parent explicitly permits it and supplies the applicable coordination instructions.

Report the outcome, changed paths, checks and results, deviations from the plan, and unresolved issues. If blocked, distinguish completed work from what remains. The parent owns integration and final acceptance.
```

## Luna

Assign work that can finish without parent dialogue. Include:

```text
You cannot use send_message. Resolve routine details locally. If a missing decision or dependency prevents completion, return a final report with the blocker, evidence, and what the parent must resolve. Do not make major architecture, interface, scope, compatibility, or risk decisions on the parent's behalf. Do not spawn children.
```

## Terra, Sol, and Astra

Include:

```text
Resolve routine details locally. Before making a major architecture, interface, scope, compatibility, or risk decision not already settled by the task packet, ask the direct parent through collaboration.send_message with evidence, options, and a recommendation. Continue independent work while awaiting guidance; do not proceed with work that depends on the unanswered decision. Message for blockers and stable handoffs, avoiding routine heartbeats.
```
