## Managed skills

The `managed-*` skill family provides four separate phases:

- `managed-workflow` selects a managed or strict assurance level and coordinates the other phases.
- `managed-plan` researches the repository and writes a concise implementation plan.
- `managed-implement` delegates through `multi_agent_v1`, using a chart-grounded Luna-first core ladder plus Terra and Sol knowledge-breadth overrides while the main agent owns integration and verification.
- `managed-quality` removes AI shaped residue from integrated backend and frontend code, then reverifies behavior.

Every managed workflow creates `plan.md` and `checklist.md`, presents them for human review, and waits for explicit approval before implementation. After approval, normal managed work activates goal mode when persistence helps, starts one explicitly configured implementation worker when delegation is worthwhile, uses the main agent for integration review, runs a final human code cleanup, and verifies the cleaned result. Model routing uses Luna `xhigh` by default, Luna `high` or `medium` only for bounded economy lanes, and `max` as the within-model quality-first setting. Terra and Sol below `max` are selected for knowledge breadth rather than as automatic cost-quality steps. Strict work adds an explicitly configured independent reviewer for changes with high risk and records its evidence in the checklist.

Worker prompts and final responses are the normal delegated-work record. Separate slice, result, review, or final-report files are created only when the user explicitly requests them or an external workspace or handoff cannot preserve the normal record. Small immediate work that does not need these artifacts should not invoke the managed workflow.

The skills can be invoked separately or coordinated through `managed-workflow`.

These skills are inspired by a personal agent workflow and informed by the following third-party skills.

### Sources

- Ultragoal:
  [`dots/agents/skills/ultragoal/SKILL.md`](https://github.com/jxnl/dots/blob/e0174bdea2a55e8fe9d2912edafacb4abe9b3251/agents/skills/ultragoal/SKILL.md)

  Inspired conditional goal mode, restart-safe objectives, completion standards, and bounded child work.

- Codex Dynamic Workflows:
  [`codex-dynamic-workflows/SKILL.md`](https://github.com/DannyMac180/skills/blob/5695fa19b9d39b8270025e79633b49a8b863f9a2/codex-dynamic-workflows/SKILL.md)

  Inspired explicit orchestration, work ownership, integration policy, verification, and durable workflow files.

- Thermo-Nuclear Code Quality Review:
  [`plugins/cursor-team-kit/skills/thermo-nuclear-code-quality-review/SKILL.md`](https://github.com/cursor/plugins/blob/cfd81b3961ef5fddc90e9f2994fa1c87cd454e61/cursor-team-kit/skills/thermo-nuclear-code-quality-review/SKILL.md)

  Inspired the final structural simplification review.

- AI Code Audit and AI Frontend Audit:
  [`audit-ai-code/SKILL.md`](https://github.com/jxnl/dots/blob/74d80b1045c3a026704193ee69d09048276a79f1/agents/skills/audit-ai-code/SKILL.md) and [`audit-ai-frontend/SKILL.md`](https://github.com/jxnl/dots/blob/74d80b1045c3a026704193ee69d09048276a79f1/agents/skills/audit-ai-frontend/SKILL.md)

  Inspired the backend and frontend checks for generated residue, intentional APIs, component and data shape, accessibility, responsive behavior, and generic visual defaults.
