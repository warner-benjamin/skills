#!/usr/bin/env python3
"""Create a manager-led AI-agent workflow artifact directory."""

from __future__ import annotations

import argparse
import json
import re
from datetime import datetime, timezone
from pathlib import Path


def slugify(value: str) -> str:
    slug = re.sub(r"[^a-z0-9]+", "-", value.lower()).strip("-")
    return slug[:64].strip("-") or "workflow"


def write_new(path: Path, content: str) -> None:
    if path.exists():
        return
    path.write_text(content, encoding="utf-8")


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

    now = datetime.now(timezone.utc).replace(microsecond=0).isoformat()
    state = {
        "title": args.title,
        "slug": slug,
        "created_at": now,
        "status": "planned",
        "approval": {"required": None, "granted": None, "notes": ""},
        "plan_review": {
            "model": "gpt-5.5-high",
            "reviewer": None,
            "status": "pending",
            "path": "reviews/plan-review.md",
        },
        "slices": [],
        "verification": {"status": "not_started", "checks": []},
        "commits": [],
    }

    write_new(
        run_dir / "plan.md",
        f"""# {args.title}

## Goal

## Success Criteria

## Current Context

## Constraints

## Risks

## Approval Required

## Plan Review

## Implementation Slices

## Integration Policy

## Verification

## Commit Policy

## Reusable Artifacts
""",
    )
    write_new(
        run_dir / "orchestration.md",
        f"""# Orchestration: {args.title}

## Execution Rules

- Keep the original objective intact.
- Ask for approval before risky, expensive, external, or destructive actions.
- Keep immediate blocking work local.
- Review and repair the plan before implementation.
- Delegate only bounded, disjoint, materially useful slices.
- Review, fix, sanity-check, and commit each slice before moving on.
- Integrate slice results before final verification.

## Branching Rules

## Slice Prompts

## Review Prompts

## Completion Audit
""",
    )
    write_new(
        run_dir / "reviews" / "plan-review.md",
        f"""# Plan Review: {args.title}

## Reviewer

Model: gpt-5.5-high plan reviewer

## Verdict

blocking | non-blocking

## Blocking Findings

## Non-blocking Findings

## Unsafe Assumptions

## Missing Context

## Slice Boundary Issues

## Verification Gaps

## Commit Boundary Issues

## Required Plan Changes

## Fixes Applied

## Rejected Findings

## Re-review Required

yes | no

## Re-review Notes
""",
    )
    write_new(run_dir / "state.json", json.dumps(state, indent=2) + "\n")
    write_new(
        run_dir / "final-report.md",
        f"""# Final Report: {args.title}

## Outcome

## Accepted Results

## Rejected Results

## Conflicts Resolved

## Slice Commits

## Verification Evidence

## Remaining Risks

## Reusable Follow-up
""",
    )

    print(run_dir)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
