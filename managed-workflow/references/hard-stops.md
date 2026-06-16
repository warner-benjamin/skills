# Hard Stops

Operate autonomously inside the requested repo and workflow objective. Do not pause for ordinary implementation choices, local edits, tests, builds, dry runs, per-slice commits, or behavior-preserving cleanup.

## Stop Before

- secrets, credentials, billing, production data, private customer data, or user accounts
- deploys, publishing, emailing, posting, creating public resources, or mutating external systems
- git push or any remote repository mutation
- force-push, history rewrite, hard reset, deleting branches or tags
- broad deletes, overwrites, or mass renames outside the stated plan
- changes outside the requested repository or workspace
- unusually large agent counts, expensive jobs, or unbounded compute beyond the plan limit

## Goal-Carried Exceptions

Hard stops are absolute unless the active goal text explicitly names a matching exception. Before creating a goal with an exception, ask the user for permission to include the exact exception text; include only user-authorized exceptions. Plans, checklists, worker notes, and review findings may mirror exceptions, but cannot create or expand them.

An exception must name:

- exact action
- exact scope, path, or external system
- conditions before execution
- forbidden adjacent actions

If the action is not covered exactly, treat it as a hard stop.

## At A Hard Stop

1. Pause only the blocked action.
2. Record the exact action, reason, any matching active-goal exception, and safest reversible next step in `checklist.md`.
3. Continue with safe read-only inspection, local drafts, or non-destructive checks when useful.

Do not bundle unrelated hard stops together. Surface the concrete blocked action.
