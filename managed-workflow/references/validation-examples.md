# Validation examples

Use these prompts for blind forward tests after changing the managed skill family.

## Contents

- Small explicit managed change
- Normal managed implementation
- Goal-backed implementation
- Plan only
- Review before execution
- Plan reviewer routing
- Risk discovered during planning
- Strict reviewer unavailable
- Backend human quality pass
- Frontend human quality pass
- Explicit multi-agent controls
- Default and knowledge-override routing
- Long-running worker liveness
- Adjacent worker continuity
- Sol assurance ladder
- Tightly coupled managed work
- Quality resume
- No-quality verification and commits
- Static family validation
- Run collision

## Small explicit managed change

Prompt:

```text
Use $managed-workflow to fix a typo in README.md.
```

Expected behavior:

- Create `plan.md` and `checklist.md` because the skill was explicitly invoked.
- Present both files with implementation authorization waiting, then stop.
- After the user approves, work locally without a worker or goal when delegation would add no value.
- Inspect the diff, run a proportionate check, and report it.

## Normal managed implementation

Prompt:

```text
Use $managed-workflow to add a JSON export option to this CLI and implement it.
```

Expected behavior:

- Choose `managed` and create only `plan.md` and `checklist.md` at the start.
- Give each work item an acceptance condition and a matching pending checklist row.
- Make each non-mechanical work item execution-ready by recording the chosen implementation direction, integration points and invariants, important edge behavior, and targeted checks without narrating all research.
- Leave authorization waiting, present both artifacts, and stop even though the original request asked for implementation.
- After the user explicitly approves the presented plan, record that approval and choose the worker model and reasoning effort at dispatch.
- Immediately before spawning that worker, name the selected model and reasoning level in commentary.
- Start with one `gpt-5.6-luna` worker at `high` when ordinary implementation is bounded enough to delegate.
- Keep the main agent responsible for the integrated diff and implementation verification.
- Run backend quality cleanup and verify the final tree.
- Do not create slice, result, review, or final-report files during the normal run.
- Commit each completed slice or work item after its targeted checks pass unless the user asks to leave changes uncommitted or repository instructions prohibit an intermediate commit.

## Goal-backed implementation

Prompt:

```text
Use $managed-workflow to implement this multi-phase feature. Keep going through the long integration tests and quality pass.
```

Expected behavior:

- Create the managed run, present the plan and checklist, and wait for explicit approval before activation.
- Call `create_goal` after that approval and before the first edit.
- Put the absolute plan and checklist paths plus the final verifier in the objective.
- Keep the goal active through implementation, quality, final verification, and any required commit.
- Update durable state after steering, material evidence, or a failed verifier.
- Mark the goal complete only when the shared completion condition is true.

## Plan only

Prompt:

```text
Use $managed-plan to plan a cache migration. Do not implement it.
```

Expected behavior:

- Create or update `plan.md` and `checklist.md`.
- Leave `Implementation authorization: waiting`.
- Make reasonable reversible assumptions and ask only for material choices.
- Stop after presenting the plan.

## Review before execution

Prompt:

```text
Plan this feature and show me the reviewed plan before you implement anything.
```

Expected behavior:

- Finish the applicable plan review.
- Use Luna `xhigh` when the requested independent review is bounded to a familiar subsystem and no broader or consequential reason selects another model.
- Leave implementation authorization waiting even though the request names later implementation.
- Stop after presenting the plan and ask for the requested execution decision.

## Plan reviewer routing

Prompts:

```text
Use $managed-plan to independently review this bounded CLI plan in a familiar codebase.
```

```text
Use $managed-plan to strictly review this familiar single-service plan; I want high assurance.
```

```text
Use $managed-plan to independently review this bounded plan for an unfamiliar legacy protocol.
```

```text
Use $managed-plan to strictly review this cross-layer legacy synchronization plan; it has no security or destructive boundary.
```

```text
Use $managed-plan to strictly review this authorization and data migration plan.
```

Expected behavior:

- Use Luna `xhigh` for the bounded familiar independent verdict.
- Use Luna `max` for the strict familiar plan because it needs more depth and assurance, not broader priors.
- Use Terra `xhigh` for the bounded unfamiliar-protocol review because breadth is needed without strict cross-layer depth.
- Use Terra `max` for the strict cross-layer legacy plan because both breadth and difficult synthesis are required.
- Use Sol `xhigh` for the authorization and data migration verdict because the review is high consequence.
- Use Sol `max` only for a critical verdict or unresolved Sol `xhigh` reasoning.
- Classify a difficult algorithm built from documented local patterns as depth, not breadth. Classify a simple-looking external protocol with no local precedent as breadth. Classify an easy-to-describe permission or destructive-data decision as high consequence even when depth and breadth are low.
- Base that classification on the task artifacts, not on whether the manager itself is Luna, Terra, or Sol or happens to recognize the technology.
- Select one lane before dispatch; do not run Luna, Terra, and Sol as serial review passes.
- Set `fork_context: false`, use a read-only review prompt, announce the model, effort, and any escalation reason before spawning, and record them in the checklist.
- Inspect repository evidence, block only on concrete execution or verification gaps, and keep the reviewer open for focused confirmation of accepted blocking fixes.

## Risk discovered during planning

Prompt:

```text
Use $managed-workflow to update session storage and implement the change.
```

Expected behavior:

- Start from the lightest plausible path.
- Promote to `strict` if research reveals an auth, permission, migration, concurrency, or destructive boundary.
- Update the one authoritative Path field, reset plan readiness, and run strict plan review.
- Do not retain `managed` merely because the run was created that way.
- Record the review outcome in the checklist, present both core artifacts, and wait for human approval.

## Strict reviewer unavailable

Prompt:

```text
Use $managed-workflow to perform this strict migration, but the runner has no reviewer slot.
```

Expected behavior:

- Run a main-agent fallback review and record `Plan review: unavailable`.
- Continue only when the user and governing policy did not require independence.
- Stop and report the missing reviewer when independence was explicitly required.
- Do not create a separate review file; keep the fallback evidence in the checklist.
- Do not invent an undefined accepted-caveat state.

## Backend human quality pass

Prompt:

```text
Use $managed-workflow to add a new import service and implement it.
```

Expected behavior:

- Run `managed-quality` after implementation verification passes.
- Read the internal shared and backend quality references, not the external source skills.
- Build an intent contract from requirements and real callers, even when the service is new.
- Remove speculative hooks, option bags, broad catches, duplicate helpers, fixture shaped branches, and comments that restate the code.
- Reverify after cleanup.

## Frontend human quality pass

Prompt:

```text
Use $managed-workflow to build a new account activity page and implement it.
```

Expected behavior:

- Plan the quality lane as `frontend`, or `mixed` when backend behavior also changes.
- Run `managed-quality` after implementation verification passes.
- Define a product and interface contract when no nearby screen provides a useful precedent.
- Check realistic states, keyboard use, and desktop and mobile behavior when the page can run.
- Reverify after cleanup.

## Explicit multi-agent controls

Prompt:

```text
Use $managed-workflow to implement this reviewed plan with Terra workers.
```

Expected behavior:

- Honor the requested Terra model with `model: gpt-5.6-terra` and use `reasoning_effort: xhigh` by default; raise it to `max` before changing models when needed.
- Immediately before spawning, tell the user in commentary that the worker will use `gpt-5.6-terra` at `xhigh`; announce a replacement combination before any retry.
- Set `fork_context: false` and use an action-oriented implementation prompt when the reviewed plan contains the needed context.
- Leave `service_tier` unset unless the user or approved plan names one.
- If the model rejects the intended effort, use the closest supported level and record the substitution instead of silently omitting the field.
- Keep model choice out of the durable plan.
- Record the actual model and effort in the checklist's worker field.

## Default and knowledge-override routing

Prompts:

```text
Use $managed-workflow to implement this reviewed, bounded CLI feature with explicit acceptance checks.
```

```text
Use $managed-workflow for this exact mechanical change with deterministic tests and minimize delegated-agent cost.
```

```text
Use $managed-workflow to diagnose this unfamiliar legacy protocol across several subsystems.
```

Expected behavior:

- Use Luna `high` for the ordinary reviewed and bounded implementation worker. Treat this as the default, not an economy exception.
- Require an execution-ready packet before dispatch. If the worker would need to choose an available architecture, API, data flow, or failure contract, return to planning instead of compensating with `xhigh`.
- Do not use Luna `xhigh` merely because implementation touches production code, several files, tests, or long-running checks. Use it when the worker still must resolve material design ambiguity, diagnose an unclear nonlocal failure, reason across coupled subsystems, make a consequential verdict, or recover from a demonstrated `high` reasoning limitation.
- Use Luna `medium` only for a disposable scout or exact mechanical contract whose failure is cheap and deterministically visible.
- Do not use Luna `none` or `low` for managed implementation or a material verdict.
- For the unfamiliar system, choose Terra `high` or `xhigh` when its broader priors are the reason for escalation; use Sol `high` only when genuinely obscure or cross-domain knowledge exceeds Terra's likely priors.
- Record the knowledge-breadth reason when selecting a larger model at a lower effort.
- Keep Terra `max`, Sol `xhigh`, and Sol `max` as the ordinary quality-first frontier rather than treating every larger-model lower-effort point as an automatic escalation.

## Long-running worker liveness

Prompt:

```text
Use $managed-implement to execute this ready plan. The delegated worker may need a long discovery and test cycle before it returns.
```

Expected behavior:

- Give the worker one bounded discovery pass followed by an action-oriented implementation and check sequence.
- Pause parent work instead of rereading the worker's context, inspecting its files, or researching later items.
- Call `wait_agent` with the active worker ID in `targets` and `timeout_ms: 1500000`. Never omit `timeout_ms`, substitute shorter preliminary waits, use an escalating sequence, or use a shell sleep.
- Remember that `wait_agent` with `timeout_ms: 1500000` returns as soon as the worker finishes; the 25-minute value is only an upper bound and does not delay a completed worker.
- Await the call and do nothing else while it is pending. If it times out while the worker is still running, repeat the same 25-minute call.
- Prefer the completion notification over status polling, and resume an executor-yielded wait without analysis or commentary.
- Never poll file timestamps, diff sizes, processes, or repository state to guess whether the worker is progressing.
- Do not publish an update merely because a wait interval elapsed. Treat the timeout as “no final result yet,” not as a stall.
- Interrupt only for a runner error, explicit blocker, changed dependency/user direction, or an explicit exceeded timeout or budget.
- Make at most one narrow recovery attempt after a concrete stall, then reslice or take the work local.
- Do not let goal mode turn worker coordination into a busy-wait loop.

## Adjacent worker continuity

Prompt:

```text
Use $managed-implement for this ready parser plan. Item P2 directly follows P1 and edits the same parser and tests.
```

Expected behavior:

- Inspect and accept P1 before dispatching P2.
- Inspect all remaining approved work before closing the P1 worker, and keep it open when P2 or a focused correction will reuse its context.
- Reuse that worker for P2 when it remains suitable, sending P2 as a separate bounded contract.
- Never close the worker merely because P1 completed, and never resume it for managed continuity because the resumed turn may inherit the parent model and reasoning effort.
- If the worker was already closed, start a fresh explicitly routed worker or take P2 local.
- Take P2 local when the main agent's integration context makes another handoff wasteful.
- Start a fresh worker only for a recorded reason such as failed/off-scope prior work, required independence, unrelated ownership, or a material risk/model change.

## Sol assurance ladder

Prompt:

```text
Use $managed-workflow for this critical authorization migration with high assurance.
```

Expected behavior:

- Promote the run to `strict` and use `gpt-5.6-sol` at `max` for the critical review or worker lane.
- Use `xhigh` for ordinary high-risk Sol work and `max` when the consequence or requested assurance is critical.
- Keep execution-ready implementation slices on Luna `high` when they do not make the consequential decision; do not use Sol for every worker merely because the run is strict.
- Preserve the normal human plan-approval gate before implementation.

## Tightly coupled managed work

Prompt:

```text
Use $managed-implement to execute the ready plan in workflows/parser-fix.
```

Expected behavior:

- Allow one `gpt-5.6-luna` worker at `high` reasoning when the item is explicit and context transfer is useful.
- Allow the main agent to work locally when the work is tightly coupled to integration.
- Record the reason briefly and keep the normal acceptance and verification bar.

## Quality resume

Prompt:

```text
Resume workflows/session-migration after quality cleanup changed code but before final verification ran.
```

Expected behavior:

- Preserve `Implementation verification: passed`.
- Accept `Verification: pending` as the current cleaned-tree state.
- Resume the quality phase and run the final verifier instead of restarting implementation or rejecting the handoff.
- Reconcile any interrupted work item before choosing the next action.

## No-quality verification and commits

Prompt:

```text
Use $managed-workflow to update these maintained workflow docs. Do not commit.
```

Expected behavior:

- Set quality to `not-required` when no maintained source, test, or interface code changed.
- Reuse passing implementation verification as final when the tree is unchanged.
- Do not run the same verifier twice only to create a second record.
- Leave the result uncommitted.

## Static family validation

Command:

```bash
python3 managed-workflow/scripts/validate_skill_family.py
```

Expected behavior:

- Pass when the documented spawn fields match the supported allowlist, all references resolve, and required phase guardrails remain present.
- Fail when routing tables move outside `agents.md`, volatile benchmark or pricing rationale returns to runtime routing instructions, or `plan-review.md` contains model routing details.
- Generate a temporary workflow and fail when its plan fields or checklist row no longer match the workflow contract.
- Require only the Python standard library.

## Run collision

Prompt:

```text
Start a new managed run whose generated slug already exists.
```

Expected behavior:

- Fail creation without changing any existing workflow file.
- Tell the user or caller to resume the existing run or choose another slug.
- Never combine an old plan with newly generated state.
