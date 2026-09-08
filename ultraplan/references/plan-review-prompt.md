# Independent plan review

Adapt this brief with the plan path, relevant evidence sources, and settled user decisions.

> Review the complete plan at [plan path] for achieving [user outcome]. Use [governing sources] and respect [settled user decisions]. Inspect the evidence needed to validate consequential claims, including the exact dependency version where relevant.
>
> Determine whether the approach is correct, executable, and the simplest sufficient solution. Check dependencies, ownership, boundaries, and whether the proposed verification proves the requested outcome. Challenge unsupported assumptions and unnecessary scope, abstractions, coordination, or tests. Preserve required behavior and checks justified by actual risks.
>
> Check whether existing project dependencies or established, maintained libraries can replace proposed custom implementations. Require justification for consequential custom implementations when a suitable library exists, accounting for fit and integration cost.
>
> Remain read-only and do not spawn agents. The parent owns revisions. Return evidence-backed findings with source anchors and the smallest useful corrections. Separate blocking correctness problems, required simplifications, and optional refinements. Treat required simplifications as blocking and optional refinements as advisory.
>
> Return `approved` only if the complete plan has no blocking findings; otherwise return `not ready`. Report any evidence you could not verify. On rereview, assess the complete revised plan, not only the corrections.
