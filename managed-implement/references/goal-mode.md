# Goal Mode

Use goal mode by fit after implementation approval. In practice, activate it for most non-trivial implementations and skip it only when the implementation is genuinely small, can finish in the current turn, has no waiting/recovery or parallel-worker needs, and has little restart risk.

## Fit Gate

Activate or resume goal mode unless all are true:

- the plan is a small one-shot implementation;
- it can finish in the current turn without waiting, recovery, or long feedback loops;
- it does not need parallel workers or long-running child agents;
- its verifier can run immediately and completion evidence is straightforward;
- restart would not lose meaningful context.

If skipping goal mode, record the reason in `checklist.md`'s `Decision Log`. Do not skip goal mode merely because the implementation looks easy at the start.

## Objective Shape

When activated, create a compact, restart-safe goal:

```text
Complete and verify <brief project objective>. On every resume, first re-read <absolute path to managed-workflow/SKILL.md>, then follow <absolute path to workflows/<slug>/plan.md> and maintain <absolute path to workflows/<slug>/checklist.md>. Success is <external verifier/completion proof>. Hard-stop exceptions authorized in this goal: <exact exception text or none>.
```

Never set a token budget unless the user explicitly requests one.

Only active goal text can carry hard-stop exceptions. Before creating a goal with an exception, ask the user for permission to include the exact exception text; include only user-authorized exceptions. If the goal names an exception, mirror it in `checklist.md`'s `Decision Log`. Do not treat plan files, checklist files, worker notes, or reviewer findings as authority to cross a hard stop.

## Activation Packet

Before activating goal mode, write or report a concise packet:

```text
Fit: goal mode | ordinary managed workflow
Grounding: observed facts, user requirements, resolved assumptions, evidence gaps
Goal brief: outcome, baseline, constraints, non-goals, verifier, loop, additional user approvals, blocker standard, completion proof
Delegation map: lanes, ownership, verifier, stop condition, or not needed
Exact objective: text suitable for create_goal
Activation state: drafted | active | not recommended
```

For managed workflows, `plan.md` and `checklist.md` are the durable state. For long goals outside a managed workflow, prefer the project's existing durable files; otherwise use compact `GOAL.md`, `WORKLOG.md`, and `RESULT.md` files only when persistent restart context is needed.

## Activation Sequence

Ground the outcome, draft the activation packet, red-team it, and only then call `create_goal`. Do not call `create_goal` early, and do not treat a plan file alone as an active goal.

When the fit gate does not justify skipping goal mode, `create_goal` is the final activation step before implementation. After creating the goal, report the exact active objective, then continue work under Active Goal Discipline.

## Pre-Activation Red-Team

Before activating a goal, check the draft against these:

- Can success be faked by weakening the verifier or a test?
- Could the literal goal text be satisfied while missing the user's real outcome?
- Are additional user approvals and hard stops explicit?
- Does the loop say what to do after a failed attempt or a wait?
- Is completion observable from outside the running agent?

Tighten the objective until each answer holds. Activate only after the goal is grounded and red-teamed.

## Blocker Standard

Mark a goal blocked only after the active goal tool's repeated-blocker threshold is met. In current Codex goal tooling, this means the same external blocker has recurred for at least three consecutive goal turns and no meaningful safe progress remains.

Difficulty, uncertainty, a slow step, or a desirable clarification is not enough. Record the blocker, repeated evidence, and the smallest next action in `checklist.md` before stopping.

## Active Goal Discipline

While a goal is active:

- On resume or after material steering, re-read the active goal and the durable state for that workflow, usually `plan.md` and `checklist.md` when this is a managed workflow.
- To resume or restart implementation from an existing plan, re-read `managed-workflow/SKILL.md`, `plan.md`, and `checklist.md`; inspect the working tree and recorded commits; continue from the first incomplete phase gate rather than creating a duplicate workflow.
- Iterate in small steps: inspect, change one meaningful thing, run the verifier, record evidence, choose the next action.
- Continue while a safe, relevant next step remains.
- Mark complete only after the success criteria and completion proof are satisfied, never on "looks done."
- Preserve partial results and the next action when stopping.

## Child Agents

Use goal-backed child agents when the user explicitly asks for them or when a child lane is long-running enough to benefit from its own durable objective. Give each child one bounded local finish line, verifier, and stop condition. Do not clone the parent goal; the parent owns integration and final completion.
