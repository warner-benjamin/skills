# Independent plan review

```text
Review [plan path] against [original request and relevant updates in the user's words]. Respect [user decisions]. Check whether [primary evidence] supports the planner's consequential choices in the proposed environment. For example, a feature in the latest documentation may be absent from the project's pinned version.

Trace the user's workflow through setup, use, recovery, and delivery. Check that the tasks are in dependency order and that the acceptance checks prove the requested outcome. Identify the smallest representative scenario that can expose an integration error early. Flag optional ideas that have slipped into required work.

Compare the plan with the simplest design that meets the request. Before adding a safeguard or test, ask whether the mechanism that needs it can be removed. Apply the same scrutiny to earlier reviewer suggestions. Reopen a package choice only when it could remove substantial custom work or address a material limitation, accounting for integration cost.

Remain read-only and do not spawn agents. For each blocker, identify the affected plan step, the evidence or missing fact, the consequence, and the smallest correction that preserves required behavior. Keep wording and style suggestions advisory.

A plan can earn approval with an execution-time probe pending if it schedules the probe before dependent work and explains how the result guides that work. Final verification that requires external access or user testing can also remain pending at approval if the plan states who will verify the original acceptance criterion, when, and how.

On rereview, check changed decisions and any dependencies or acceptance criteria they affect. Carry forward earlier conclusions wherever their evidence still holds.

Return one verdict with the findings. Use `approved` when the whole plan has no execution blockers. Otherwise return `not ready` and name the exact gaps.
```
