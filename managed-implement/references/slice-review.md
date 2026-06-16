# Slice Review

Use this output shape for each implementation slice review:

```text
Verdict: blocking | non-blocking
Plan alignment:
Prompt reviewed:
Report reviewed:
Files reviewed:
Blocking findings:
Non-blocking findings:
Test or verification gaps:
Unrelated-change risk:
Required fixes:
Re-review required: yes | no
Commit-ready: yes | no
```

Review the slice prompt, slice report, diff, targeted check evidence, plan alignment, ownership boundary, and unrelated-change risk.

Block commit readiness when:

- the slice changes files outside its ownership without a recorded reason
- targeted checks were skipped without a credible reason
- `slices/<slice-id>.md` or `results/<slice-id>.md` is missing for an implementation slice
- the implementation does not satisfy the plan slice
- unrelated user/concurrent-agent changes are mixed into the slice
- review found material issues that were not fixed or explicitly rejected with reasons

After material fixes, ask the same reviewer/thread for re-review when available.
