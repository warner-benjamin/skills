## Durable delivery skills

This repository provides four delivery skills:

- `ultraplan` grounds and critiques a proposed durable objective, decomposes it into bounded dependency-ordered parent and subagent lanes with proposed models and efforts, and returns an execution-ready activation packet without mutating goal state or implementing.
- `ultragoal` validates and activates an execution-ready objective, maintains native goal and plan state, coordinates dependency-ordered implementation, keeps the parent responsible for integration, and proves completion with the strongest feasible verifier.
- `quality-review` performs an ambitious, evidence-backed maintainability and product-quality audit across backend, general, test, and frontend code. It searches for structural simplifications before local cleanup and can be used independently or as Ultragoal's final aggregate quality gate.
- `delegate` carries out an explicit request to use subagents, gives each worker sole ownership of its assigned scope while running, waits without polling, and limits parent verification to targeted post-return spot-checks instead of duplicate work.

`ultraplan` is design-only and returns a conversational activation packet unless the user requests one canonical durable artifact. `ultragoal` deliberately avoids a parallel workflow state machine: it validates that packet or an existing runbook against live state, then uses the native active goal and plan for execution.

Ultraplan scales its packet to the goal: small parent-owned plans may compress concerns and omit lane or wave machinery, while delegated or risk-bearing plans retain the full execution map.

Delegated work remains bounded and manager-owned: workers receive one behavioral contract, the parent waits without polling, personally inspects the complete diff, reuses compatible open implementers and reviewers through correction and confirmation, verifies from the integration workspace, and closes agents only after their slices and reviews are accepted. Risk-specific reviews remain separate from the final quality review.

Ultraplan proposes execution lanes and model/effort assignments; Ultragoal revalidates them against live state before dispatch. Their duplicated Luna/Terra/Sol assignment tables are intentionally identical and must remain synchronized. The parent may continue genuinely independent work while agents run, but must never duplicate or interfere with delegated ownership.

`ultraplan`, `ultragoal`, and `quality-review` disable implicit invocation. Use `$ultraplan` to design or critique a persistent objective, `$ultragoal` to activate or resume it, and `$quality-review` for the strict quality gate. `delegate` activates for an explicit request to use subagents and can also be invoked as `$delegate`.

Migration from the retired family is direct: use `$ultraplan` instead of `managed-plan`, `$ultragoal` instead of `managed-workflow` and `managed-implement`, and `$quality-review` instead of `managed-quality`. Invoke `$ultraplan` directly for planning-only requests and `$ultragoal` only for activation or execution; no retired wrappers are retained.

### Sources

- Ultraplan and Ultragoal:
  [`dots/agents/skills/ultragoal/SKILL.md`](https://github.com/jxnl/dots/blob/e0174bdea2a55e8fe9d2912edafacb4abe9b3251/agents/skills/ultragoal/SKILL.md)

  Inspired explicit goal activation, outcome grounding, real-surface verification, anti-cheating rules, restart discipline, completion proof, and parent-owned delegation.

- Thermo-Nuclear Code Quality Review:
  [`plugins/cursor-team-kit/skills/thermo-nuclear-code-quality-review/SKILL.md`](https://github.com/cursor/plugins/blob/cfd81b3961ef5fddc90e9f2994fa1c87cd454e61/cursor-team-kit/skills/thermo-nuclear-code-quality-review/SKILL.md)

  Inspired ambitious structural simplification, code-judo reframing, spaghetti prevention, and the strong approval bar.

- AI Code Audit and AI Frontend Audit:
  [`audit-ai-code/SKILL.md`](https://github.com/jxnl/dots/blob/74d80b1045c3a026704193ee69d09048276a79f1/agents/skills/audit-ai-code/SKILL.md) and [`audit-ai-frontend/SKILL.md`](https://github.com/jxnl/dots/blob/74d80b1045c3a026704193ee69d09048276a79f1/agents/skills/audit-ai-frontend/SKILL.md)

  Inspired local-idiom checks, canonical ownership and API review, generated-residue and test audits, browser verification, component and data-shape review, accessibility, responsive resilience, and fact-versus-inference discipline.
