# Slice Review

Use this output shape for each implementation slice review:

```text
Reviewer identity:
Reviewer agent/thread id:
Verdict: blocking | non-blocking
Critical findings:
Important non-blocking findings:
Missing context or unresolved questions:
Required slice fixes:
```

Review the slice prompt, slice report, diff, targeted check evidence, plan alignment, ownership boundary, and unrelated-change risk.

Flag an obviously simpler approach for this slice's scope so complexity does not accumulate for the final quality phase. Block when the simpler approach is local, clear, behavior-preserving, and materially reduces avoidable branching, wrong-layer logic, duplication, or indirection. Keep broader reframings and taste-level cleanup non-blocking for the final quality phase.

Block commit readiness when:

- the slice changes files outside its ownership without a recorded reason
- targeted checks were skipped without a credible reason
- `slices/<slice-id>.md` or `results/<slice-id>.md` is missing for an implementation slice
- the implementation does not satisfy the plan slice
- the slice has a clear local simplification that materially improves maintainability without expanding scope
- unrelated user/concurrent-agent changes are mixed into the slice
- review found material issues that were not fixed or explicitly rejected with reasons

After material fixes, ask the same reviewer/thread for re-review when available.
