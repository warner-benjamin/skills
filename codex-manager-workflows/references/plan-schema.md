# Plan Schema

Use this schema when a machine-readable workflow plan helps coordination. Keep `workflows/<slug>/plan.md` as the human source of truth. Treat this as a state contract for agents and scripts, not a promise that `verify_workflow.py` performs deep schema validation.

```json
{
  "goal": "string",
  "baseline": "string",
  "success_criteria": ["string"],
  "primary_verifier": {
    "command": "string or null",
    "success_evidence": "string"
  },
  "completion_proof": ["string"],
  "constraints": ["string"],
  "anti_cheating_constraints": ["string"],
  "risks": [
    {
      "risk": "string",
      "hard_stop": true,
      "mitigation": "string"
    }
  ],
  "hard_stops": {
    "encountered": [],
    "goal_exceptions_mirror": [],
    "notes": "string"
  },
  "plan_review": {
    "agent_type": "default",
    "model": null,
    "reasoning_effort": "high",
    "reviewer": "same reviewer/thread for re-review",
    "status": "pending",
    "path": "reviews/plan-review.md"
  },
  "agent_limits": {
    "max_concurrent_agents": 4,
    "max_total_agents": 12,
    "hard_stop_above_limits": true
  },
  "slices": [
    {
      "id": "01-discovery",
      "objective": "string",
      "context": "string",
      "files_or_sources": ["string"],
      "ownership": "string",
      "dependencies": [],
      "do": ["string"],
      "do_not": ["string"],
      "expected_output": "string",
      "verification": ["string"],
      "review": {
        "agent_type": "default",
        "model": null,
        "reasoning_effort": "medium",
        "path": "reviews/01-discovery-review.md",
        "status": "pending"
      },
      "commit": {
        "message": "slice 01-discovery: string",
        "sha": null,
        "status": "pending"
      },
      "status": "pending"
    }
  ],
  "integration_policy": {
    "owner": "parent",
    "conflict_resolution": "Inspect authoritative sources before choosing.",
    "final_output": "string"
  },
  "verification": [
    {
      "check": "string",
      "command": "string or null",
      "required": true,
      "status": "pending"
    }
  ],
  "final_quality_review": {
    "required": null,
    "status": "undecided",
    "path": "reviews/final-quality-review.md",
    "reason": "required for multi-slice code workflows; skipped for docs/research/small work",
    "reviewer": null,
    "cleanup_slice": null
  },
  "reusable_artifacts": ["string"]
}
```

Suggested defaults:

- `agent_limits.max_concurrent_agents`: 2-4 for normal work.
- `agent_limits.max_total_agents`: 6-12 unless the plan sets a bounded larger run.
- `model`: `null` means inherit the parent model; set only when an explicit override is needed.
- `hard_stops.goal_exceptions_mirror`: audit mirror only; only user-authorized active goal text can authorize a hard-stop exception.
- `final_quality_review.required`: record an explicit decision before the complete phase. `true` enforces a completed `reviews/final-quality-review.md`; `false` skips the gate but needs a `reason`. Leaving it `null`/`undecided` fails complete-phase verification.
- Slice IDs: prefix with two digits so files sort naturally.
- Status values: `pending`, `in_progress`, `complete`, `blocked`, `skipped`.
