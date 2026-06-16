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
    for dirname in ("slices", "results", "reviews"):
        (run_dir / dirname).mkdir(parents=True, exist_ok=True)
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

## Observed Facts

## User Requirements

## Resolved Assumptions

## Constraints

## Anti-cheating Constraints

## Risks

## Hard Stops

## Approval Gates

## Workflow Artifact Path

`{run_dir}`

## Implementation Slices

## Orchestration Sequence

## Integration Policy

## Verification

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
- [ ] User interview complete or not needed
- [ ] Plan drafted
- [ ] Selected plan review complete or marked unavailable
- [ ] User cleared implementation
- [ ] Approval gates resolved or not needed
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

Review level:
Codex reviewer:
Claude review:
Verdicts:
Accepted fixes:
Critical findings:
Important non-blocking findings:
Missing context or unresolved questions:
Required plan changes:
Rejected or unresolved findings:
Skipped or unavailable review caveats:

## Decision Log

| Date | Type | Decision or event | Rationale / evidence |
| --- | --- | --- | --- |

## Slices

| ID | Status | Depends on | Prompt | Report | Review | Commit |
| --- | --- | --- | --- | --- | --- | --- |

## Verification

| Check | Required | Status | Evidence |
| --- | --- | --- | --- |

## Final Quality Review

Review path: reviews/final-quality-review.md
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
