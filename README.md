# Codex skills

These skills provide instructions for Codex. This ReadMe was written with the `simple-english` skill.

## Skills

### `ultraplan`

The agent researches an objective, questions assumptions, and writes the simplest sufficient execution plan with completion checks. It uses a designated artifact or an untracked plan under `.plans/`. Readiness requires approval from an independent review agent.

### `ultragoal`

The agent activates or resumes a durable objective and maintains native goal and plan state through implementation. The parent agent owns integration and acceptance. Completion requires successful verification and approval from an independent review agent.

### `quality-review`

The agent reviews code structure, maintainability, and product quality with repository evidence. Reviews stay read-only and return prioritized findings with a verdict. For authorized fixes, the agent repairs problems and checks behavior.

### `delegate`

The agent selects and coordinates explicitly requested subagents without durable goal state. Subagent roles are recommended based on agent capabilities.

### `myskills`

The agent updates this repository and its submodules, then installs top-level skills, including symlink targets. It replaces installed versions without backups. Use: "update $myskills".

### `quiet-polling`

The agent monitors long-running jobs with brief updates and adaptive polling intervals from 5 to 25 minutes. Builds and long tests that block the next step use 5-minute intervals.

### External skill: `simple-english`

The agent writes technical text with ASD-STE100 Simplified Technical English. A pinned Git submodule references the original [`AminBlg/SimpleEnglish`](https://github.com/AminBlg/SimpleEnglish/tree/main/skills/simple-english) skill.

## External skill setup

The `simple-english` directory is a relative symlink to `.third-party-skills/simple-english/skills/simple-english`.

Clone this repository with the `--recurse-submodules` option.

If you already cloned the repository, run `git submodule update --init`.

## Skill invocation

`ultraplan`, `ultragoal`, and `quality-review` disable implicit invocation.

Use these commands to invoke the skills:

- Use `$ultraplan` to research and plan ordinary or persistent work. Question assumptions with this skill.
- Use `$ultragoal` to activate or resume a durable objective.
- Use `$quality-review` to review code quality or make authorized repairs.
- Only for an explicit standalone delegation request, use `$delegate`.
- Use `$myskills` to install or update the top-level skills from this repository.

## Sources

### Ultraplan and Ultragoal

Source: [`dots/agents/skills/ultragoal/SKILL.md`](https://github.com/jxnl/dots/blob/e0174bdea2a55e8fe9d2912edafacb4abe9b3251/agents/skills/ultragoal/SKILL.md)

This source inspired explicit goal activation and plans based on the intended outcome. It also inspired observable verification, rules against false completion claims, recovery after interruptions, and proof of completion. Its delegation rules keep scope, integration, conflict resolution, and final completion with the parent agent.

### Thermo-Nuclear Code Quality Review

Source: [`plugins/cursor-team-kit/skills/thermo-nuclear-code-quality-review/SKILL.md`](https://github.com/cursor/plugins/blob/cfd81b3961ef5fddc90e9f2994fa1c87cd454e61/cursor-team-kit/skills/thermo-nuclear-code-quality-review/SKILL.md)

This source inspired changes that simplify code structure without a change in behavior. It also inspired rules to prevent tangled code and strict criteria for approval.

### AI Code Audit and AI Frontend Audit

Sources: [`audit-ai-code/SKILL.md`](https://github.com/jxnl/dots/blob/74d80b1045c3a026704193ee69d09048276a79f1/agents/skills/audit-ai-code/SKILL.md) and [`audit-ai-frontend/SKILL.md`](https://github.com/jxnl/dots/blob/74d80b1045c3a026704193ee69d09048276a79f1/agents/skills/audit-ai-frontend/SKILL.md)

These sources inspired checks against local code conventions and clear ownership of the authoritative implementation. They also inspired API reviews, audits of unnecessary generated code, test audits, and browser validation.

Other contributions include component reviews, reviews of data structures, and accessibility checks. They also include reliable layouts across screen sizes and clear distinctions between facts and inferences.
