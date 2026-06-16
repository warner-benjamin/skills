# Slice Template

Each implementation slice must be self-contained.

```text
Slice ID:
Objective:
Context:
Files / sources:
Ownership:
Dependencies:
Do:
Do not:
Expected output:
Report path:
Verification:
Review:
Commit boundary:
```

Prefer disjoint slices:

- codebase discovery
- dependency/API research
- implementation
- tests/fixtures
- docs/examples
- UX/product review
- security/risk review
- final verification

Parallelize only when slices have no file, workflow-artifact, or semantic dependency overlap.

For code-edit slices, assign non-overlapping files or modules where possible. Tell workers they are not alone in the codebase, must not revert others' edits, and must adapt to concurrent changes.

Every delegated slice prompt must require the agent to return a report in the shape from `slice-report.md`, including changed paths, workspace or branch, verification evidence, blockers, and remaining risks.
