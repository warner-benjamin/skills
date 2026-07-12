# Plan review

Use independent plan review only for the strict path or when the user requests it. Normal managed plans use the readiness test in `managed-plan`.

## Strict review

Spawn one fresh reviewer through `multi_agent_v1` using `$WORKFLOW_SKILL_DIR/references/agents.md`. For ordinary strict review, set `model: gpt-5.6-terra`, `reasoning_effort: xhigh`, `agent_type: explorer`, and `fork_context: false`; raise Terra to `max` before changing models when the review remains difficult but is not high risk. Use Terra `high` only for a bounded knowledge-heavy review. Use Sol at `high` only when broad or obscure knowledge matters more than maximum task reasoning, Sol at `xhigh` for high-risk review, and Sol at `max` for critical or explicitly high-assurance review. Do not use Sol `medium` for a final high-risk verdict.

Give the reviewer the plan, relevant repository paths, user requirements, and known constraints. Ask for:

- a verdict of `passed` or `blocking`
- blocking findings with evidence and the smallest required change
- important findings that do not block only when they affect execution or verification
- any material decision that remains unresolved

Ask the reviewer to check whether the approach fits the observed code, work items have safe ownership, workers can act without inventing design, and verification proves the requested outcome.

Treat findings as advice. Accept findings that are correct in context. Reject added scope or complexity with a short reason.

Record the reviewer, verdict, blocking findings, and accepted fixes concisely in `checklist.md`. Do not create a separate review file unless the user explicitly requests it or an external handoff cannot use the checklist and final response.

After material fixes to blocking findings, ask the same reviewer to confirm only the changed areas. Do not add another review loop for suggestions that do not block.

If no reviewer is available, apply the fallback in the shared workflow contract.
