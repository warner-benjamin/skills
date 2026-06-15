#!/usr/bin/env python3
"""Create a manager-led AI-agent workflow artifact directory."""

from __future__ import annotations

import argparse
import json
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
    state = {
        "title": args.title,
        "slug": slug,
        "created_at": now,
        "status": "scaffolded",
        "hard_stops": {
            "encountered": [],
            "goal_exceptions_mirror": [],
            "notes": "",
        },
        "plan_review": {
            "agent_type": "default",
            "model": None,
            "reasoning_effort": "high",
            "reviewer": None,
            "status": "pending",
            "path": "reviews/plan-review.md",
        },
        "agent_limits": {
            "max_concurrent_agents": 4,
            "max_total_agents": 12,
            "hard_stop_above_limits": True,
        },
        "slices": [],
        "verification": {"status": "not_started", "checks": []},
        "final_quality_review": {
            "required": None,
            "status": "undecided",
            "path": "reviews/final-quality-review.md",
            "reason": "",
            "reviewer": None,
            "cleanup_slice": None,
        },
        "commits": [],
    }

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

## Plan Review

## Implementation Slices

## Integration Policy

## Verification

## Final Quality Review

## Commit Policy

## Reusable Artifacts
""",
    )
    add_file(
        run_dir / "reviews" / "plan-review.md",
        f"""# Plan Review: {args.title}

## Reviewer

Agent type: default
Model: inherited unless an explicit override is needed
Reasoning effort: high

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
    add_file(run_dir / "state.json", json.dumps(state, indent=2) + "\n")
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
