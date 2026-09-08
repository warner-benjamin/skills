# Planning and durable delivery skills

This repository contains the skills that I use with Codex and other AI agents:

## Skills

- `ultraplan` researches an objective, checks out or downloads relevant reference materials, challenges assumptions, and chooses the simplest sufficient approach. It writes one Markdown execution plan with concrete completion checks, then obtains independent subagent review. It uses a designated artifact or creates an untracked plan under `.plans/`.
- `ultragoal` validates and activates an execution-ready objective. It maintains native goal and plan state. The parent remains responsible for integration. A fresh read-only subagent must review the final frozen change before completion. The skill proves completion with the strongest feasible verifier.
- `quality-review` audits maintainability and product quality with evidence. It covers backend, general, test, and frontend code. It searches for structural simplifications before local cleanup. You can use it independently or as the final aggregate quality gate for Ultragoal.
- `delegate` fulfills an explicit request to use subagents without durable goal state. The core skills do not depend on it.
- `myskills` pulls this repository and its submodules. It updates each installed custom skill in place without backups or temporary copies of old versions.
- `quiet-polling` waits for long-running jobs with brief scheduled updates and polling intervals of 5, 10, 15, 20, then 25 minutes. It starts later on the ladder when the expected runtime supports it.
- External `simple-english` writes and rewrites technical text with ASD-STE100 Simplified Technical English. A pinned Git submodule references the original [`AminBlg/SimpleEnglish`](https://github.com/AminBlg/SimpleEnglish/tree/main/skills/simple-english) skill.

## External skill setup

The `simple-english` directory is a relative symlink to `.third-party-skills/simple-english`.

Clone this repository with the `--recurse-submodules` option.

If you already cloned the repository, run `git submodule update --init`.

## Planning and execution

`ultraplan` researches and designs before implementation. Its authoritative plan includes the chosen direction, supporting evidence, ordered work, boundaries, and verification. Execution requires separate activation, which may already be authorized by the user.

`ultragoal` validates an activation handoff against the current state. Then it uses the native active goal and plan for execution. It does not create a parallel workflow state machine.

Ultraplan adjusts each plan to the work. Small plans remain compact. When delegation is useful, the plan gives workers enough context, boundaries, and completion checks to start without rediscovering the design.

Delegated work has clear limits, and the parent keeps ownership. Each worker receives one behavioral contract and sends only material events. Workers do not receive heartbeat polls. The parent uses long, event-driven waits. It integrates completed, non-interfering lanes while other work continues. The parent personally inspects the complete diff.

The parent reuses compatible task identities for corrections. It runs final validation from the integration workspace. A fresh subagent does the final aggregate review. After corrections, the same reviewer examines the complete frozen change again. Reviews for specific risks remain separate from the quality review.

Ultraplan proposes ownership, useful concurrency, and model/effort assignments, with handoff detail matched to each worker. Execution revalidates those assignments and adjusts the brief if the worker changes before dispatch. The parent can do independent work while agents operate. It must not duplicate or interfere with work that it delegated.

## Skill invocation

`ultraplan`, `ultragoal`, and `quality-review` disable implicit invocation.

- Use `$ultraplan` to research, challenge, and design ordinary or persistent work.
- Use `$ultragoal` to activate or resume a durable objective.
- Use `$quality-review` for the strict frozen-state quality gate.
- Use `$delegate` only for an explicit standalone delegation request.
- Use `$myskills` to pull this repository and update every installed custom skill.

## Sources

- **Ultraplan and Ultragoal:** [`dots/agents/skills/ultragoal/SKILL.md`](https://github.com/jxnl/dots/blob/e0174bdea2a55e8fe9d2912edafacb4abe9b3251/agents/skills/ultragoal/SKILL.md)

  This source inspired explicit goal activation, outcome grounding, real-surface validation, anti-cheating rules, restart discipline, completion proof, and parent-owned delegation.

- **Thermo-Nuclear Code Quality Review:** [`plugins/cursor-team-kit/skills/thermo-nuclear-code-quality-review/SKILL.md`](https://github.com/cursor/plugins/blob/cfd81b3961ef5fddc90e9f2994fa1c87cd454e61/cursor-team-kit/skills/thermo-nuclear-code-quality-review/SKILL.md)

  This source inspired structural simplification, code-judo reframing, spaghetti prevention, and a strong approval threshold.

- **AI Code Audit and AI Frontend Audit:** [`audit-ai-code/SKILL.md`](https://github.com/jxnl/dots/blob/74d80b1045c3a026704193ee69d09048276a79f1/agents/skills/audit-ai-code/SKILL.md) and [`audit-ai-frontend/SKILL.md`](https://github.com/jxnl/dots/blob/74d80b1045c3a026704193ee69d09048276a79f1/agents/skills/audit-ai-frontend/SKILL.md)

  These sources inspired local-idiom validation, canonical ownership, API reviews, generated-residue audits, test audits, and browser validation. They also inspired component reviews, data-shape reviews, accessibility, responsive resilience, and clear distinctions between facts and inferences.
