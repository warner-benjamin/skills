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
    slices_dir = run_dir / "slices"
    results_dir = run_dir / "results"
    reviews_dir = run_dir / "reviews"
    slices_dir.mkdir(parents=True, exist_ok=True)
    results_dir.mkdir(parents=True, exist_ok=True)
    reviews_dir.mkdir(parents=True, exist_ok=True)
    skipped: list[Path] = []

    def add_file(path: Path, content: str) -> None:
        if not write_new(path, content):
            skipped.append(path)

    now = datetime.now(timezone.utc).replace(microsecond=0).isoformat()
    add_file(
        run_dir / "plan.md",
        f"""# {args.title}

## Goal

## Baseline

## Success Criteria

## Primary Verifier

## Completion Proof

## Current Context

## Constraints

## Anti-cheating Constraints

## Risks

## Hard Stops

## Workflow Artifact Path

`{run_dir}`

## Implementation Slices

For each implementation slice, include slice ID, objective, ownership, dependencies, prompt path (`slices/<id>.md`), report path (`results/<id>.md`), review path, verification, and commit boundary.

## Integration Policy

Describe how worker or forked-workspace changes will be imported into the manager's current branch, how conflicts will be resolved, and which checks must pass before each slice commit.

## Verification

## Final Quality Review

## Commit Policy

## Reusable Artifacts
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
User implementation gate: pending
Implementation status: pending
Initial verification: pending
Final quality review: pending
Final verification: pending

## Lifecycle

- [ ] Local/code research complete
- [ ] External research complete or not needed
- [ ] Plan drafted
- [ ] Fresh plan review complete or marked unavailable
- [ ] User cleared implementation
- [ ] Slice prompts written before implementation
- [ ] Slice reports collected and integrated
- [ ] Slices complete
- [ ] Slice reviews complete
- [ ] Integration complete
- [ ] Initial verification passed
- [ ] Final quality review complete or explicitly skipped
- [ ] Final verification passed or explicitly skipped
- [ ] Final report complete

## Plan Review

Reviewer:
Reviewer agent/thread id:
Model/effort: strongest available reasoning model / high
Gate: see `Plan review` and `User implementation gate` in Phase Gates
Initial verdict:
Re-review verdict:
Accepted fixes:
Blocking findings:
Non-blocking findings:
Missing context / verification gaps:
Rejected findings:
Unresolved findings:
Unavailable caveat shown to user:
User override after unavailable review:

## Agent Limits

Max concurrent agents: 4
Max total agents: 12
Hard stop above limits: yes

## Agent Lanes

| Agent id | Role | Slice | Status | Notes |
| --- | --- | --- | --- | --- |

## Hard Stops

| Status | Action | Reason | Resolution |
| --- | --- | --- | --- |

Goal exceptions mirror: none

## Slices

| ID | Status | Prompt | Report | Review | Commit |
| --- | --- | --- | --- | --- | --- |

## Worker Integration

| Slice | Source workspace/branch | Imported paths | Local checks | Notes |
| --- | --- | --- | --- | --- |

## Verification

| Check | Required | Status | Evidence |
| --- | --- | --- | --- |

## Final Quality Review

Gate: see `Final quality review` in Phase Gates
Review path: reviews/final-quality-review.md
Decision reason if not-required:
Reviewer:
Reviewer agent/thread id:
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

## Accepted Results

## Rejected Results

## Conflicts Resolved

## Slice Commits

## Verification Evidence

## Final Quality Review

## Completion Proof

## Remaining Risks

## Reusable Follow-up
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
