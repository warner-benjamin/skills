---
name: managed-workflow
description: Orchestrate human-reviewed planning, delegated implementation, final human code cleanup, verification, and review based on risk with a durable plan and checklist. Use when the user explicitly invokes $managed-workflow, asks for a managed plan-and-execute process, requests subagent implementation, or needs controlled work across several subsystems. Present the plan and checklist and wait for approval before implementation.
---

# Managed workflow

Route work through `managed-plan`, `managed-implement`, and `managed-quality` while keeping one concise contract.

`SKILL_DIR` is the absolute directory containing this file. Resolve the three phase skills as sibling directories.

## Start

Read `references/workflow-contract.md` and choose `managed` or `strict`.

- For `managed`, create the core artifacts, obtain human approval, use one `multi_agent_v1` implementation worker by default when delegation is worthwhile, set its model and reasoning effort explicitly, keep the main agent on integration, run final human code cleanup, and verify.
- For `strict`, also run the independent review required by the shared contract and phase skills. Record its outcome in the checklist.

Every explicit managed-workflow invocation creates `plan.md` and `checklist.md`, even when the implementation is small. Small immediate tasks that do not need this process should not invoke the skill. If the user requests planning only, run `managed-plan` and stop before implementation.

You may find risk during planning that was not visible at the start. Promote the run to `strict` when the contract requires it. Do not preserve the original path merely because files already exist.

Immediately before every new worker or reviewer spawn, name the selected model and reasoning level in commentary. Announce any replacement combination before retrying a rejected spawn.

## Create or resume

For a new managed run, execute:

```bash
python3 "$SKILL_DIR/scripts/new_workflow.py" "Task title"
```

Add `--strict` for a known strict path. The command fails if the run directory already exists. Resume an existing run by reusing its directory and reconciling its state under the shared contract.

## Run the phases

Before each phase, read that phase's `SKILL.md`.

During delegated work, do not babysit a running worker. Pause parent work and use the increasing 2-, 5-, then 8-minute wait sequence without progress commentary, status polling, repository probes, context rereading, or side work. Resume a tool-yielded wait silently; act only on completion, an explicit worker message, user steering, a hard stop, or a material external event.

1. Run `managed-plan` to research, choose an approach, and define work items with acceptance checks.
2. Present `plan.md` and `checklist.md`, ask for implementation approval, and stop.
3. On a later user turn, record explicit approval in the checklist. Run `managed-implement` only when the plan is still ready and authorization is approved.
4. Run `managed-quality` for every managed source, test, or user interface code change. Skip it only under that phase's `not-required` rules or when the user explicitly skips it.
5. When quality is not required and the tree has not changed since implementation verification, use that verification as the final result. Do not rerun it only to relabel the same evidence.
6. Apply the shared commit policy throughout implementation and finish any remaining required commit after final verification.
7. If goal mode is active, keep it active through quality, final verification, and any required final commit or explicitly requested artifact. Mark it complete only when the shared completion condition is true.
8. Report the result to the user. Create an extra report file only under the shared contract's exception.

Operate autonomously inside the approved plan. Return to planning when code or new evidence invalidates a material design choice, changes the requested outcome, or promotes the path to `strict`.

## Load references only when needed

- Read `references/hard-stops.md` before consequential or ambiguous actions.
- Read `references/validation-examples.md` only when testing or revising this skill family.
