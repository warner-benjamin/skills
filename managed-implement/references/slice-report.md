# Slice Report

Require this report from each worker lane and use it for local implementation slices when no worker ran. Save it as `results/<slice-id>.md`.

```text
Agent identity:
Agent id/thread:
Workspace or branch:
Slice ID:
Prompt path:
Files changed:
Summary:
Verification run:
Verification result:
Review notes needed:
Blockers:
Remaining risks:
```

For worker reports, require exact changed paths and enough verification evidence for the manager to reproduce checks in the manager workspace. Do not accept a vague "done" report as integration-ready.
