#!/usr/bin/env python3
"""Create concise managed workflow files."""

from __future__ import annotations

import argparse
import re
import sys
from datetime import datetime, timezone
from pathlib import Path


def slugify(value: str) -> str:
    slug = re.sub(r"[^a-z0-9]+", "-", value.lower()).strip("-")
    return slug[:64].strip("-") or "workflow"


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("title", help="Workflow title or task summary")
    parser.add_argument(
        "--root",
        default="workflows",
        help="Directory where workflow runs are stored (default: workflows)",
    )
    parser.add_argument("--slug", help="Optional explicit workflow slug")
    parser.add_argument(
        "--strict",
        action="store_true",
        help="Create strict path and plan review state",
    )
    args = parser.parse_args()

    slug = slugify(args.slug or args.title)
    run_dir = (Path(args.root) / slug).resolve()
    try:
        run_dir.mkdir(parents=True)
    except FileExistsError:
        print(
            f"Error: workflow directory already exists: {run_dir}. "
            "Resume it directly or choose a different --slug.",
            file=sys.stderr,
        )
        return 2

    path_name = "strict" if args.strict else "managed"
    plan_review = "pending" if args.strict else "not-required"
    risks = (
        """
## Risks and approvals

<Record only material risks, hard stops, and authority still needed.>
"""
        if args.strict
        else ""
    )
    now = datetime.now(timezone.utc).replace(microsecond=0).isoformat()

    (run_dir / "plan.md").write_text(
        f"""# {args.title}

Workflow: `{run_dir}`

## Goal

<Requested outcome, success conditions, and meaningful exclusions.>

## Approach

<One chosen design with the observed facts, contracts, and edge cases that affect implementation.>

## Work

| ID | Objective | Paths | Depends on | Done when | Checks |
| --- | --- | --- | --- | --- | --- |
| work-1 | <objective> | <ownership boundary> | <none or ID> | <observable result> | <targeted checks> |

## Verification

<Implementation checks, final verifier, and backend, frontend, mixed, or not-required quality lane.>
{risks}""",
        encoding="utf-8",
    )

    (run_dir / "checklist.md").write_text(
        f"""# Workflow checklist: {args.title}

Created: {now}

## State

Path: {path_name}
Plan: drafting
Plan review: {plan_review}
Implementation authorization: waiting
Implementation: pending
Implementation verification: pending
Verification: pending
Quality: pending

## Work

| ID | Status | Worker | Evidence |
| --- | --- | --- | --- |

## Checks

| Check | Status | Evidence |
| --- | --- | --- |

## Decisions and evidence

<Record only approval, review outcomes, blockers, or decisions needed to resume safely.>
""",
        encoding="utf-8",
    )

    print(run_dir)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
