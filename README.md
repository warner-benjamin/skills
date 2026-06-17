## Managed Skills

The `managed-*` skill family:

- `managed-workflow`: orchestrates the end-to-end workflow across organic design planning, implementation, final quality review, and final reporting.
- `managed-plan`: researches the codebase and relevant sources, resolves user decisions, drafts a reviewed organic design plan plus checklist artifacts, and runs plan review.
- `managed-implement`: executes a reviewed design plan after implementation approval, using self-contained execution slices, delegated or substantial-slice prompts/reports, reviews, checks, commits, and fit-based goal-mode discipline.
- `managed-quality`: runs the final maintainability and simplification gate after implementation passes initial verification.

They are designed to either be used independently for individual phases of the plan, code, and review workflow or to be orchestrated together by `managed-workflow` for a full end-to-end Codex-managed workflow.

These skills are inspired by my personal Agentic workflow and informed by the following third-party skills.

### Sources

- Ultragoal:
  [`dots/agents/skills/ultragoal/SKILL.md`](https://github.com/jxnl/dots/blob/e0174bdea2a55e8fe9d2912edafacb4abe9b3251/agents/skills/ultragoal/SKILL.md)

  Inspired durable goal activation packets, restart-safe objective text, `create_goal` sequencing, active-goal discipline, blocker standards, and bounded child-goal guidance.

- Codex Dynamic Workflows:
  [`codex-dynamic-workflows/SKILL.md`](https://github.com/DannyMac180/skills/blob/5695fa19b9d39b8270025e79633b49a8b863f9a2/codex-dynamic-workflows/SKILL.md)

  Inspired explicit orchestration, additional approval checks, work packets, integration policy, verification flow, and reusable workflow artifact conventions.

- Thermo-Nuclear Code Quality Review:
  [`plugins/cursor-team-kit/skills/thermo-nuclear-code-quality-review/SKILL.md`](https://github.com/cursor/plugins/blob/cfd81b3961ef5fddc90e9f2994fa1c87cd454e61/cursor-team-kit/skills/thermo-nuclear-code-quality-review/SKILL.md)

  Inspired the final maintainability and simplification review bar, especially the emphasis on structural simplification over cosmetic review comments.
