---
name: ultraplan
description: Research and challenge an objective, choose an approach, and write an independently reviewed execution plan. Use when explicitly asked to use ultraplan for planning before implementation.
---

# Ultraplan

Turn an uncertain request into the smallest justified plan that another executor can carry out and prove complete. This workflow produces a Markdown handoff. Implementation follows planning only when the user has authorized execution, including in the original request. Do not create a goal or parallel native plan state.

## Establish the problem and gather references

Identify the intended outcome, existing behavior, constraints, and acceptance criteria. Read the repository instructions and only the documents, code, callers, tests, history, and live state that can affect the plan.

Check out reference repositories and download relevant source, documentation, or packages when needed to resolve consequential claims. Prefer primary sources. Use the project's exact dependency version; for a new dependency, identify a compatible stable release before relying on its behavior.

Keep research copies and their generated files under `<project-root>/.external_resources/`, excluded through Git's local exclude file. Keep them separate from project dependencies and the active environment; avoid running installation scripts just to inspect source. Record the source URL and exact version or revision, and cite the files or documentation that support decisions.

Distinguish observations from inferences and unresolved assumptions. Stop researching when further evidence would not change the direction, work, verification, or risk.

When delegation is useful, use `gpt-5.6-terra` at `medium` effort for less consequential code exploration during planning, such as tracing callers, mapping dependencies, or locating relevant tests. Give it bounded questions and ask for source anchors; keep consequential synthesis and direction decisions with the parent. Honor user-specified models and efforts.

## Challenge the solution and resolve choices

Check that the problem exists, the proposed mechanism addresses its cause, and the constraints permit it. Look for existing features and simpler local changes before adding machinery. Surface conflicts with governing decisions and propose a compatible alternative; do not silently change constraints to make a solution fit.

Resolve technical questions through research. Ask the user early about consequential preferences, tradeoffs, or authority decisions that existing instructions do not settle. Give the relevant evidence, viable options, and recommendation. Continue independent work while awaiting an answer, but do not commit the dependent part of the plan. Use and label reasonable reversible assumptions for routine details.

## Choose the smallest sufficient approach

Compare materially different approaches when the choice is consequential or unclear. Choose one based on outcome fit, simplicity, compatibility, verification cost, and risk. Explain why it wins and record rejected alternatives only when their rationale matters to execution.

Remove scope, abstractions, coordination, and tests that have no requirement or evidenced risk. Match the plan's detail to the work; a small change may need one implementation item and one targeted check.

## Write an executable plan

Write one authoritative Markdown artifact. Use the user-designated path or existing plan when directed; otherwise create a descriptively named file under `<project-root>/.plans/`, excluded through Git's local exclude file. Do not overwrite unrelated artifacts or stage or commit the plan without authorization.

Include the outcome, chosen direction, supporting evidence, constraints, non-goals, and material assumptions. Order work by dependencies. Give each item enough context for an executor to start without rediscovering the design:

- The behavior to change, relevant paths or symbols, and required boundaries or invariants.
- Dependencies and ownership, including write limits when work is delegated.
- Observable completion criteria and concrete checks or commands, with the evidence to return.

Specify verification on the actual user surface, including necessary environment and setup. Cover failure or recovery paths when the risk warrants them. An unavailable required verifier is a readiness gap; do not quietly substitute a weaker proxy or weaken acceptance criteria.

## Plan delegation and worker handoffs

Propose delegation only when its value exceeds coordination costs. The planner assigns provisional scopes, dependencies, write limits, models, and efforts; the parent keeps integration and acceptance. Honor requested models and efforts; otherwise use these starting points among configurations the runtime exposes.

| Work | Model and effort | Typical use |
| --- | --- | --- |
| Mechanical execution | `gpt-5.6-luna`, `low` | Exact lookup, specified command, obvious edits, or checking an explicit condition |
| Cheap bounded scout | `gpt-5.6-luna`, `medium` | Scouting, evidence extraction, or mapping with explicit questions and cheap verification |
| Clear bounded implementation | `gpt-5.6-luna`, `high` | Small feature scopes, tests, and clear fixes with explicit acceptance criteria |
| Code exploration | `gpt-5.6-terra`, `medium` | Retrieve and connect evidence across unfamiliar code, trace dependencies, and ask the parent for guidance or decisions |
| Moderately difficult work | `gpt-5.6-terra`, `high` | Bounded reasoning or implementation benefiting parent guidance on major decisions |
| Substantial coder | `gpt-5.6-sol`, `medium` | Substantial but bounded implementation, tests, repository fixes, or moderately difficult reasoning |
| Frontier knowledge | `gpt-6-astra`, `low` | Obscure cross-domain knowledge or a hard task with a clear approach and checks |
| Ambiguous or consequential judgment | `gpt-6-astra`, `medium` | Synthesis, diagnosis, design, independent review, or permissions, data, and concurrency decisions |
| Critical reasoning | `gpt-6-astra`, `high` | Interacting high-risk constraints or a consequential reasoning or security decisions |

Match each handoff to the intended worker. Luna needs an explicit approach, precise entry points, concrete checks, and a final-report exit for blockers because it cannot use `send_message`. Terra, Sol, and Astra can return consequential design or scope decisions to the parent while continuing independent work. Stronger workers can own broader reasoning, but every handoff still needs the relevant evidence, constraints, and acceptance criteria.

Execution revalidates assignments against available models and current conditions before dispatch. If the worker changes, adjust the brief to its capabilities; substituting Luna for Astra may require resolving design choices and supplying more explicit steps. Runtime dispatch and coordination belong to execution.

## Independently review and correct

Every plan requires a fresh read-only subagent reviewer before it is ready. Explicit ultraplan invocation authorizes this review. Once the draft is stable, use [references/plan-review-prompt.md](references/plan-review-prompt.md) with the plan path, relevant sources, and settled user decisions. Give the reviewer a self-contained brief without the intended verdict, using `fork_turns: "none"`.

The parent owns corrections. Resolve blocking correctness findings and required simplifications, then use `followup_task` with the same reviewer to review the complete revised plan. Substantive changes require rereview; formatting, wording without changed meaning, and recording approval do not.

Mark the plan `ready` only after approval and resolution of consequential decisions and evidence gaps. If independent review is unavailable or prohibited, retain `not ready` and report the gap.

## Hand off

Link the plan and briefly explain the direction, important tradeoffs, readiness or exact gaps, and next action. Keep execution details in the artifact so it remains sufficient without the conversation. End at the planning handoff unless the user has already authorized subsequent execution.
