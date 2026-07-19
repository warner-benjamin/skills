# Plan review

Use independent plan review only for the strict path or when the user requests it. Normal managed plans use the readiness test in `managed-plan`.

Before dispatch, apply the independent plan review routing, disclosure, and continuity rules in `$WORKFLOW_SKILL_DIR/references/agents.md`.

## Review inputs

Give the reviewer the plan, relevant repository paths, user requirements, and known constraints. Ask for:

- a verdict of `passed` or `blocking`
- blocking findings with evidence and the smallest required change
- important findings that do not block only when they affect execution or verification
- any material decision that remains unresolved

Require the reviewer to inspect the named repository evidence rather than judge the prose alone. Check whether the approach fits the observed code, every non-mechanical item is execution-ready, ownership and dependencies are safe, important edge and failure behavior is resolved, the assurance path matches actual risk, and verification would expose a wrong implementation.

## Verdict and findings

Block only on a concrete correctness, scope, ownership, unresolved-decision, or verification gap. State the evidence and smallest plan change needed. Do not block on optional polish, speculative extensibility, personal preference, or detail that does not change implementation.

Treat findings as advice. Accept findings that are correct in context. Reject added scope or complexity with a short reason.

## Result and confirmation

Record the reviewer identity, model, effort, routing reason, verdict, blocking findings, and accepted fixes concisely in `checklist.md`. Do not create a separate review file unless the user explicitly requests it or an external handoff cannot use the checklist and final response.

Keep the reviewer open while accepted blocking findings are being fixed. After material fixes, ask that same open reviewer to confirm only the changed areas. Close it only after the plan verdict is final. Do not resume a closed reviewer or add another review loop for suggestions that do not block.

If no reviewer is available, apply the fallback in the shared workflow contract.
