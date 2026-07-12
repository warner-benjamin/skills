# Human code quality bar

Use this shared bar before the backend or frontend checks. The goal is deliberate code that carries the least necessary complexity.

## Start with intent and evidence

Start with the requested behavior, plan, real callers, data, supported states, failure rules, and non goals. Each important design choice should be explainable from that evidence.

Use nearby code and repository conventions when they solve the same kind of problem or impose a real contract. Do not copy a local pattern merely because it exists elsewhere.

When the code is new and has no useful precedent, define one small design contract. Choose the owner, data shape, state model, error behavior, required variation points, and non goals. Judge the implementation against those choices.

Human quality comes from traceable intent and coherent tradeoffs. It does not require imitating older code or adding irregularity for appearance.

## Search for the simpler framing

Look beyond line cleanup. Ask whether a different ownership boundary, state model, data shape, or control flow would let the implementation delete whole concepts.

Prefer changes that remove branches, flags, wrappers, modes, special cases, or duplicate helpers. Reject a refactor that only moves the same complexity into more files.

## Common AI shaped residue

Flag these when the diff provides concrete evidence:

- speculative abstractions, factories, hooks, extension points, or fallback paths with no real caller
- pass through wrappers and identity helpers that add names without adding a useful boundary
- broad option objects, boolean mode arguments, optional fields, casts, or generic types used to avoid a clear contract
- repeated checks and one off branches inserted into unrelated flows
- comments and docstrings that restate each line instead of recording intent or an invariant
- generic names and patterns that ignore the domain, requirements, or chosen design contract
- defensive checks for impossible states, followed by silent defaults that hide the real invariant
- duplicate helpers or local utilities that shadow a canonical repository API
- hard coded fixture values, canned branches, or production behavior shaped around tests
- large volumes of scaffolding for a small behavior change

## Structural smells

Treat a file crossing from below 1000 lines to above 1000 lines as a strong prompt to review ownership and decomposition. It is not an automatic failure, but require a clear reason to keep the file whole.

Flag new special case branches in an already busy flow. Prefer moving the rule to the module, type, policy, or state model that owns it.

Flag non atomic updates and needless sequential orchestration when a clearer structure can keep related changes together or independent work independent.

## Preferred repairs

- Reuse the canonical helper or local primitive.
- Move behavior to the existing owner.
- Replace a flag or option bag with an explicit operation or a derived decision.
- Flatten control flow with direct checks and early returns.
- Delete unused flexibility and speculative branches.
- Replace loose data with the smallest explicit local type.
- Split a file when the new boundary has a clear owner and job.
- Keep one direct flow when an abstraction would only hide it.

## Evidence and restraint

State the issue, evidence, why it harms the design or repository, the smallest repair, and the check that proves behavior stayed intact.

Treat AI appearance as a smell, not proof. Consider a normal explanation such as an existing local convention, generated output, compatibility support, or a deliberate public API before changing code.

Do not create novelty to make code seem human. Do not add a new layer, rename broad areas, or reformat unrelated files without a concrete benefit to the changed behavior.

## Pass bar

Pass only when the diff has a clear owner, its important choices follow from real requirements or an explicit greenfield contract, it has no clear simpler behavior preserving design, and it leaves no high confidence AI residue that affects maintenance, correctness, safety, or product quality.
