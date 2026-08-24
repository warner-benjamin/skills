# Planning and durable delivery skills

This repository contains the skills that I use with Codex and other AI agents:

## Skills

- `ultraplan` researches an objective and challenges its assumptions. It compares viable directions and writes one new authoritative Markdown execution plan for the parent agent and subagents. It does not search for or read existing plans unless explicitly instructed. It reuses an established ignored `.plans/` storage convention; otherwise it asks whether the new plan should be checked in. It can also append an activation packet when durable-goal machinery is useful.
- `ultragoal` validates and activates an execution-ready objective. It maintains native goal and plan state and coordinates work in dependency order. The parent remains responsible for integration. The skill proves completion with the strongest feasible verifier.
- `quality-review` audits maintainability and product quality with evidence. It covers backend, general, test, and frontend code. It searches for structural simplifications before local cleanup. You can use it independently or as the final aggregate quality gate for Ultragoal.
- `delegate` fulfills an explicit request to use subagents without durable goal state. The core skills do not depend on it.
- External `simple-english` writes and rewrites technical text with ASD-STE100 Simplified Technical English. A pinned Git submodule references the original [`AminBlg/SimpleEnglish`](https://github.com/AminBlg/SimpleEnglish/tree/main/skills/simple-english) skill.

## External skill setup

The `simple-english` directory is a relative symlink to `.third-party-skills/simple-english`.

Clone this repository with the `--recurse-submodules` option.

If you already cloned the repository, run `git submodule update --init`.

## Planning and execution

`ultraplan` only researches and designs. It validates premises, challenges incorrect assumptions, selects a direction, and produces one authoritative plan. The plan has concise milestones and complete work-item contracts. Durable-goal activation is an optional final wrapper.

`ultragoal` validates an activation handoff against the current state. Then it uses the native active goal and plan for execution. It does not create a parallel workflow state machine.

Ultraplan adjusts each plan to the work. Small plans that the parent owns remain compact. Delegated work includes exact context, boundaries, model assignment, validations, and evidence. Thus, a less capable agent can start immediately.

Delegated work has clear limits, and the parent keeps ownership. Each worker receives one behavioral contract and sends only material events. Workers do not receive heartbeat polls. The parent uses long, event-driven waits. It integrates completed, non-interfering lanes while other work continues. The parent personally inspects the complete diff.

The parent reuses compatible task identities for corrections and confirmation. It runs final validation from the integration workspace. Multi-agent v2 releases idle execution capacity automatically. Reviews for specific risks remain separate from the final quality review.

Ultraplan proposes execution lanes and model/effort assignments. Ultragoal validates them again against the current state before dispatch. The inline Luna/Terra/Sol tables in both skills are intentionally identical. The parent can do independent work while agents operate. It must not duplicate or interfere with work that it delegated.

## Skill invocation

`ultraplan`, `ultragoal`, and `quality-review` disable implicit invocation.

- Use `$ultraplan` to research, challenge, and design ordinary or persistent work.
- Use `$ultragoal` to activate or resume a durable objective.
- Use `$quality-review` for the strict frozen-state quality gate.
- Use `$delegate` only for an explicit standalone delegation request.

## Migration from retired skills

- Use `$ultraplan` instead of `managed-plan`.
- Use `$ultragoal` instead of `managed-workflow` or `managed-implement`.
- Use `$quality-review` instead of `managed-quality`.
- Use `$ultraplan` directly for planning-only requests.
- Use `$ultragoal` only for activation or execution.

The repository does not retain wrappers for the retired skills.

## Sources

- **Ultraplan and Ultragoal:** [`dots/agents/skills/ultragoal/SKILL.md`](https://github.com/jxnl/dots/blob/e0174bdea2a55e8fe9d2912edafacb4abe9b3251/agents/skills/ultragoal/SKILL.md)

  This source inspired explicit goal activation, outcome grounding, real-surface validation, anti-cheating rules, restart discipline, completion proof, and parent-owned delegation.

- **Thermo-Nuclear Code Quality Review:** [`plugins/cursor-team-kit/skills/thermo-nuclear-code-quality-review/SKILL.md`](https://github.com/cursor/plugins/blob/cfd81b3961ef5fddc90e9f2994fa1c87cd454e61/cursor-team-kit/skills/thermo-nuclear-code-quality-review/SKILL.md)

  This source inspired structural simplification, code-judo reframing, spaghetti prevention, and a strong approval threshold.

- **AI Code Audit and AI Frontend Audit:** [`audit-ai-code/SKILL.md`](https://github.com/jxnl/dots/blob/74d80b1045c3a026704193ee69d09048276a79f1/agents/skills/audit-ai-code/SKILL.md) and [`audit-ai-frontend/SKILL.md`](https://github.com/jxnl/dots/blob/74d80b1045c3a026704193ee69d09048276a79f1/agents/skills/audit-ai-frontend/SKILL.md)

  These sources inspired local-idiom validation, canonical ownership, API reviews, generated-residue audits, test audits, and browser validation. They also inspired component reviews, data-shape reviews, accessibility, responsive resilience, and clear distinctions between facts and inferences.
