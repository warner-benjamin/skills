# Goal Mode

Use goal mode only when the workflow needs repeated attempts, waiting/recovery, or a long feedback loop, and success has an external verifier. Do not enter goal mode for small one-shot tasks, advisory discussions, or plan-only requests.

## Fit Gate

Goal mode is appropriate when most are true:

- progress needs repeated attempts, waiting, recovery, or long feedback cycles;
- success can be measured by a test, benchmark, workflow, artifact inspection, screenshot, readback, or other external signal;
- Codex can respond to the next failure without another preference decision;
- completion evidence is stronger than Codex saying "done."

Prefer an ordinary managed workflow without goal mode when the work is one-shot, taste-dependent, blocked on repeated human choices, lacks a credible verifier, or risks unbounded external action.

## Objective Shape

When activated, create a compact, restart-safe goal:

```text
Complete and verify <brief project objective>. On every resume, first re-read <absolute path to managed-workflow/SKILL.md>, then follow <absolute path to workflows/<slug>/plan.md> and maintain <absolute path to workflows/<slug>/checklist.md>. Success is <external verifier/completion proof>. Hard-stop exceptions authorized in this goal: <exact exception text or none>.
```

Only active goal text can carry hard-stop exceptions. Before creating a goal with an exception, ask the user for permission to include the exact exception text; include only user-authorized exceptions. If the goal names an exception, mirror it in `checklist.md`.

If the user explicitly asks for goal-backed child agents, give each child one bounded local finish line. Do not clone the parent goal; the parent owns integration and final completion.
