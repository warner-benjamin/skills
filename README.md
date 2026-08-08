## Planning and durable delivery skills

This repository provides three core delivery skills and one experimental standalone skill:

- `ultraplan` researches and challenges an objective, compares viable directions, and produces a proportional execution plan with execution-ready parent and subagent work. It can return a conversational handoff, update one canonical plan document, or append an activation packet when durable-goal machinery is useful.
- `ultragoal` validates and activates an execution-ready objective, maintains native goal and plan state, coordinates dependency-ordered implementation, keeps the parent responsible for integration, and proves completion with the strongest feasible verifier.
- `quality-review` performs an ambitious, evidence-backed maintainability and product-quality audit across backend, general, test, and frontend code. It searches for structural simplifications before local cleanup and can be used independently or as Ultragoal's final aggregate quality gate.
- Experimental `delegate` carries out an explicit request to use subagents without durable goal state. The core skills never depend on it being installed.

`ultraplan` is research-and-design only: it verifies premises, pushes back when evidence disagrees, chooses a direction, and returns one authoritative plan with concise milestones plus execution-complete work-item contracts. Durable-goal activation is an optional final wrapper. `ultragoal` validates an activation handoff against live state, then uses the native active goal and plan for execution without creating a parallel workflow state machine.

Ultraplan scales its plan to the work: small parent-owned plans stay compact, while delegated work receives the exact context, boundaries, model assignment, checks, and evidence needed for a less capable agent to start immediately.

Delegated work remains bounded and manager-owned: workers receive one behavioral contract, send only material events, and never receive heartbeat polls. The parent uses long event-driven waits, integrates completed non-interfering lanes while other work continues, personally inspects the complete diff, reuses compatible task identities through correction and confirmation, and verifies from the integration workspace. Multi-agent v2 releases idle execution capacity automatically. Risk-specific reviews remain separate from the final quality review.

Ultraplan proposes execution lanes and model/effort assignments; Ultragoal revalidates them against live state before dispatch. Their inline Luna/Terra/Sol tables remain intentionally identical. The parent may continue genuinely independent work while agents run, but must never duplicate or interfere with delegated ownership.

`ultraplan`, `ultragoal`, and `quality-review` disable implicit invocation. Use `$ultraplan` to research, challenge, and design ordinary or persistent work; use `$ultragoal` to activate or resume a durable objective; and use `$quality-review` for the strict frozen-state quality gate. Use experimental `$delegate` only for an explicit standalone delegation request.

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
