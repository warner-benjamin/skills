# Task prompts

Choose the version for the selected worker model, fill in the placeholders, and send only the completed prompt. Omit fields that do not apply. Keep the objective and behavioral acceptance criteria concrete.

## Luna

Use for `gpt-5.6-luna` at any effort. Assign work that can finish without parent dialogue.

```text
Objective: <outcome and purpose>
Acceptance: <observable requirements for completion>
Context: <relevant instructions, paths, and evidence>
Ownership: <assigned scope, permitted writes, and exclusions>
Contracts: <agreed interfaces and ready dependencies>
Verification: <necessary checks>

Complete the assigned work within these boundaries. Preserve unrelated work and existing authorization limits. Do not spawn child agents.

You cannot use send_message. Resolve routine implementation details locally. If a missing decision or dependency prevents completion within the agreed scope, return a final report explaining the blocker, evidence, and what the parent must resolve. Do not wait for a message exchange or make a major architecture, interface, scope, compatibility, or risk decision on the parent's behalf.

Report the outcome, changed paths, checks and results, and unresolved issues. If blocked, distinguish completed work from what remains.
```

## Terra / Sol / Astra

Use for `gpt-5.6-terra`, `gpt-5.6-sol`, or `gpt-6-astra` at any effort.

```text
Objective: <outcome and purpose>
Acceptance: <observable requirements for completion>
Context: <relevant instructions, paths, and evidence>
Ownership: <assigned scope, permitted writes, and exclusions>
Contracts: <agreed interfaces and ready dependencies>
Verification: <necessary checks>
Parent: <direct parent's agent ID or canonical task name>

Complete the assigned work within these boundaries. Preserve unrelated work and existing authorization limits. Resolve routine implementation details locally.

Before making a major decision not already settled by the task packet that affects architecture, shared interfaces, scope, compatibility, or consequential risk, use collaboration.send_message to ask the parent for guidance. Include the decision, relevant evidence, options, and your recommendation. Continue independent work while awaiting the answer; wait if none remains. Do not proceed with work that depends on the unanswered decision.

Message the parent for blockers or useful stable handoffs; identify the specific question or completed portion ready for inspection. Avoid routine heartbeats. Resume the assigned work when guidance resolves the issue.

Report the outcome, changed paths, checks and results, and unresolved issues. If blocked, distinguish completed work from what remains.
```

If permitting nested delegation, add the applicable instructions from
[nested-delegation.md](nested-delegation.md) to the interactive prompt.
