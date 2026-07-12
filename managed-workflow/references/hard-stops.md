# Scope and hard stops

Operate autonomously inside the user's requested repository and objective. Do not pause for ordinary design choices, local edits, tests, builds, or reversible cleanup.

Stop before an action that needs authority not already present in the user's request, including:

- accessing secrets, credentials, private customer data, production data, billing, or user accounts
- deploying, publishing, emailing, posting, or mutating an external system
- pushing to a remote, rewriting history, force pushing, or deleting branches or tags
- broad deletion, overwrite, or mass rename outside the approved scope
- changing files outside the requested repository or workspace
- starting unusually costly or unbounded work

Ask for the smallest missing authorization and continue safe local work when possible. Record consequential authorization in `checklist.md` for strict workflows.

Do not create an authority or exception system in goal text, plans, checklists, or worker reports. Those files may record what the user authorized, but they cannot expand it.
