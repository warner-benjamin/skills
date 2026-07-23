## Durable delivery skills

This repository provides two explicitly invoked skills:

- `ultragoal` grounds and activates a durable objective, maintains native goal and plan state, coordinates dependency-ordered implementation, keeps the parent responsible for integration, and proves completion with the strongest feasible verifier.
- `quality-review` performs an ambitious, evidence-backed maintainability and product-quality audit across backend, general, test, and frontend code. It searches for structural simplifications before local cleanup and can be used independently or as Ultragoal's final aggregate quality gate.

`ultragoal` deliberately avoids a parallel workflow state machine. It prefers existing design documents and delivery runbooks, the native active goal, and the native plan. Additional generated workflow files are created only when the user requests durable artifacts or an external handoff cannot use the existing state.

Delegated work remains bounded and manager-owned: workers receive one behavioral contract, the parent waits without polling, personally inspects the complete diff, permits at most one focused correction pass, verifies from the integration workspace, and accepts or commits only at requested boundaries. Risk-specific reviews remain separate from the final quality review.

Both skills disable implicit invocation. Use `$ultragoal` for a persistent managed objective and `$quality-review` for the strict quality gate.

Migration from the retired family is direct: use `$ultragoal` Design instead of `managed-plan`, `$ultragoal` Activate or Resume instead of `managed-workflow` and `managed-implement`, and `$quality-review` instead of `managed-quality`. No compatibility wrappers are retained.

### Sources

- Ultragoal:
  [`dots/agents/skills/ultragoal/SKILL.md`](https://github.com/jxnl/dots/blob/e0174bdea2a55e8fe9d2912edafacb4abe9b3251/agents/skills/ultragoal/SKILL.md)

  Inspired explicit goal activation, outcome grounding, real-surface verification, anti-cheating rules, restart discipline, completion proof, and parent-owned delegation.

- Thermo-Nuclear Code Quality Review:
  [`plugins/cursor-team-kit/skills/thermo-nuclear-code-quality-review/SKILL.md`](https://github.com/cursor/plugins/blob/cfd81b3961ef5fddc90e9f2994fa1c87cd454e61/cursor-team-kit/skills/thermo-nuclear-code-quality-review/SKILL.md)

  Inspired ambitious structural simplification, code-judo reframing, spaghetti prevention, and the strong approval bar.

- AI Code Audit and AI Frontend Audit:
  [`audit-ai-code/SKILL.md`](https://github.com/jxnl/dots/blob/74d80b1045c3a026704193ee69d09048276a79f1/agents/skills/audit-ai-code/SKILL.md) and [`audit-ai-frontend/SKILL.md`](https://github.com/jxnl/dots/blob/74d80b1045c3a026704193ee69d09048276a79f1/agents/skills/audit-ai-frontend/SKILL.md)

  Inspired local-idiom checks, canonical ownership and API review, generated-residue and test audits, browser verification, component and data-shape review, accessibility, responsive resilience, and fact-versus-inference discipline.
