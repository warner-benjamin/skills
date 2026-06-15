#!/usr/bin/env python3
"""Run a shallow artifact audit for manager-led workflow runs."""

from __future__ import annotations

import argparse
import json
from pathlib import Path


REQUIRED_FILES = ("plan.md", "state.json", "final-report.md")
REQUIRED_DIRS = ("slices", "results", "reviews")
PHASES = ("scaffold", "planned", "complete")


def require_non_empty(paths: list[Path], label: str, failures: list[str]) -> None:
    for path in paths:
        if not path.read_text(encoding="utf-8").strip():
            failures.append(f"Empty {label} file: {path}")


def relative_path(workflow_dir: Path, value: object) -> Path:
    if isinstance(value, str) and value:
        path = Path(value)
    else:
        path = Path("reviews/final-quality-review.md")
    if path.is_absolute():
        return path
    return workflow_dir / path


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("workflow_dir", help="Path to workflows/<slug>")
    parser.add_argument(
        "--phase",
        choices=PHASES,
        default="complete",
        help="Lifecycle phase to verify (default: complete)",
    )
    args = parser.parse_args()

    workflow_dir = Path(args.workflow_dir)
    failures: list[str] = []

    if not workflow_dir.is_dir():
        failures.append(f"Missing workflow directory: {workflow_dir}")
    for name in REQUIRED_FILES:
        path = workflow_dir / name
        if not path.is_file():
            failures.append(f"Missing file: {path}")
        elif not path.read_text(encoding="utf-8").strip():
            failures.append(f"Empty file: {path}")
    for name in REQUIRED_DIRS:
        path = workflow_dir / name
        if not path.is_dir():
            failures.append(f"Missing directory: {path}")

    state: dict[str, object] | None = None
    state_path = workflow_dir / "state.json"
    if state_path.is_file():
        try:
            state = json.loads(state_path.read_text(encoding="utf-8"))
        except json.JSONDecodeError as exc:
            failures.append(f"Invalid JSON in {state_path}: {exc}")
        else:
            if not isinstance(state, dict):
                failures.append(f"State JSON must be an object: {state_path}")
                state = {}
            for key in (
                "title",
                "slug",
                "status",
                "hard_stops",
                "plan_review",
                "agent_limits",
                "slices",
                "verification",
                "final_quality_review",
                "commits",
            ):
                if key not in state:
                    failures.append(f"Missing state key: {key}")

    slices_dir = workflow_dir / "slices"
    results_dir = workflow_dir / "results"
    reviews_dir = workflow_dir / "reviews"
    slice_files = sorted(slices_dir.glob("*.md")) if slices_dir.is_dir() else []
    result_files = sorted(results_dir.glob("*.md")) if results_dir.is_dir() else []
    review_files = sorted(reviews_dir.glob("*.md")) if reviews_dir.is_dir() else []
    plan_review = reviews_dir / "plan-review.md"
    slice_review_files = [path for path in review_files if path.name != "plan-review.md"]

    if not plan_review.is_file():
        failures.append(f"Missing plan review file: {plan_review}")
    else:
        require_non_empty([plan_review], "plan review", failures)
    if args.phase in ("planned", "complete"):
        if not slice_files:
            failures.append("No slice files found under slices/")
        else:
            require_non_empty(slice_files, "slice", failures)
    if args.phase == "complete":
        if not result_files:
            failures.append("No result files found under results/")
        else:
            require_non_empty(result_files, "result", failures)
        if not slice_review_files:
            failures.append("No slice review files found under reviews/")
        else:
            require_non_empty(slice_review_files, "slice review", failures)
        quality_review = state.get("final_quality_review") if isinstance(state, dict) else None
        if isinstance(quality_review, dict):
            required = quality_review.get("required")
            status = quality_review.get("status")
            if required not in (True, False) or status == "undecided":
                failures.append(
                    "Final quality review is undecided; record an explicit decision "
                    "(required true with a completed review, or required false with a reason)"
                )
            elif required is True:
                if status != "complete":
                    failures.append("Final quality review is required but not marked complete")
                quality_path = relative_path(workflow_dir, quality_review.get("path"))
                if not quality_path.is_file():
                    failures.append(f"Missing final quality review file: {quality_path}")
                else:
                    require_non_empty([quality_path], "final quality review", failures)
            elif not str(quality_review.get("reason") or "").strip():
                failures.append("Final quality review skipped without a reason")

    if failures:
        print("Workflow verification failed:")
        for failure in failures:
            print(f"- {failure}")
        return 1

    print(f"Workflow verification passed for {args.phase}: {workflow_dir}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
