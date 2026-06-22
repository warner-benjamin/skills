#!/usr/bin/env python3
"""Create a managed workflow artifact directory."""

from __future__ import annotations

import argparse
import re
import sys
from datetime import datetime, timezone
from pathlib import Path


def slugify(value: str) -> str:
    slug = re.sub(r"[^a-z0-9]+", "-", value.lower()).strip("-")
    return slug[:64].strip("-") or "workflow"


def write_new(path: Path, content: str) -> bool:
    if path.exists():
        return False
    path.write_text(content, encoding="utf-8")
    return True


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("title", help="Workflow title or task summary")
    parser.add_argument(
        "--root",
        default="workflows",
        help="Directory where workflow runs are stored (default: workflows)",
    )
    parser.add_argument("--slug", help="Optional explicit workflow slug")
    args = parser.parse_args()

    slug = slugify(args.slug or args.title)
    run_dir = Path(args.root) / slug
    run_dir.mkdir(parents=True, exist_ok=True)
    skipped: list[Path] = []

    def add_file(path: Path, content: str) -> None:
        if not write_new(path, content):
            skipped.append(path)

    now = datetime.now(timezone.utc).replace(microsecond=0).isoformat()
    add_file(
        run_dir / "plan.md",
        f"""# {args.title}

## Goal

Include the objective, non-goals, success criteria, hard stops, additional user approvals, and workflow artifact path when they matter.

`{run_dir}`

## Design

Write this as a standalone, domain-specific design a skeptical engineer could implement without asking a planning question. Include observed facts, user requirements, resolved assumptions, constraints, risks, behavior/API/config/data contracts, invariants, edge cases, ownership boundaries, and decisions behind the approach. Spend depth where the problem is hard; keep obvious grounding concise.

## Implementation Steps

List ordered technical steps. For code work, name concrete files, functions, tests, migrations, and contract deltas when known. Steps answer what must change; they are not review or commit units.

## Verification / Acceptance

Define concrete commands, expected artifacts, acceptance criteria, primary verifier, completion proof, and honest skip/fallback rules.

## Execution Slices

Define the execution mode, main agent role, and structured implementation/review/verification/commit units.

Use one of:

- `Execution mode: single-agent local`
- `Execution mode: multi-agent delegated`
- `Execution mode: hybrid`

Use one of:

- `Main agent role: coding`
- `Main agent role: manager`
- `Main agent role: hybrid`

For single-agent local work, each slice should say `Owner: main agent as coding agent` and should not pre-create delegated slice artifacts. For multi-agent delegated work, each slice should state worker ownership and the main agent's manager/integrator responsibility. For hybrid work, each slice should state whether the main agent is acting as coding agent or manager/integrator. Each slice should reference one or more implementation steps and include ownership, dependencies, review gate, artifact expectations, targeted checks, and commit boundary.

## Orchestration Notes

Record slice order, dependency readiness, artifact creation mode, retry/re-slice rules, reviewer-unavailable behavior, failed-check behavior, integration policy, final-quality routing, and reusable artifacts.
""",
    )
    add_file(
        run_dir / "checklist.md",
        f"""# Workflow Checklist: {args.title}

Created: {now}
Status: scaffolded

Keep this as a status ledger only. Do not duplicate `plan.md`; update the plan for goal, constraints, risks, slice details, and verification strategy.

## Phase Gates

Plan review: pending
Implementation approval: waiting
Implementation status: pending
Initial verification: pending
Final quality review: pending
Final verification: pending

## Plan Review

Review level:
Reviewer(s):
Verdicts / caveats:
Accepted fixes:
Rejected or unresolved findings:
Implementation approval request:
Implementation approval evidence:

## Decision Log

| Date | Type | Decision or event | Rationale / evidence |
| --- | --- | --- | --- |

## Slices

| ID | Status | Depends on | Artifacts / evidence | Review | Commit |
| --- | --- | --- | --- | --- | --- |

## Verification

| Check | Required | Status | Evidence |
| --- | --- | --- | --- |

## Final Quality Review

Review path: create reviews/final-quality-review.md only when a final quality reviewer runs
Reviewer:
Decision:
Cleanup slice:

## Commits

| Slice | Commit | Notes |
| --- | --- | --- |
""",
    )
    add_file(
        run_dir / "final-report.md",
        f"""# Final Report: {args.title}

## Outcome

## Changes

## Completion Proof

## Remaining Risks

## Follow-up
""",
    )

    print(run_dir)
    if skipped:
        print(
            "Warning: existing workflow files were left unchanged: "
            + ", ".join(str(path) for path in skipped),
            file=sys.stderr,
        )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
