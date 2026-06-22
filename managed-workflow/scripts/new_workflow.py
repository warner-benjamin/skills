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

Workflow artifacts: `{run_dir}`
Fill each section per `managed-workflow/references/workflow-contract.md` ("Required Plan Shape"). State one chosen path — no options, TODOs, or open questions.

## Goal

<Objective, non-goals, success criteria, hard stops, additional user approvals.>

## Design

<Standalone design a skeptical engineer could build without inventing a decision: facts, requirements, resolved assumptions, constraints, risks, contracts, invariants, edge cases, ownership boundaries, and the decisions behind the approach.>

## Implementation Steps

<Ordered technical steps — what must change. For code, name files, functions, tests, migrations, and contract deltas.>

## Verification / Acceptance

<Concrete commands, expected artifacts, acceptance criteria, primary verifier, completion proof, honest skip/fallback rules.>

## Execution Slices

Execution mode: <single-agent local | multi-agent delegated | hybrid>
Main agent role: <coding | manager | hybrid>

<One or more slices. Each references implementation step(s) and states ownership, dependencies, review gate, artifact expectations, targeted checks, and commit boundary. For single-agent local, use `Owner: main agent as coding agent` and no delegated artifacts.>

## Orchestration Notes

<Slice order, dependency readiness, artifact creation mode, retry/re-slice rules, reviewer-unavailable and failed-check behavior, integration policy, final-quality routing, reusable artifacts.>
""",
    )
    add_file(
        run_dir / "checklist.md",
        f"""# Workflow Checklist: {args.title}

Created: {now}

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
