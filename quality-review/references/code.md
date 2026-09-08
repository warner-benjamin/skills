# Code quality reference

Use this reference for backend, CLI, library, service, data, script, test, and general implementation code.

## Local contract and ownership

Place behavior with the module or type that owns the concept and use canonical repository utilities and domain models. Judge file cohesion by responsibilities and dependencies, not a line-count threshold. Splitting a file without improving those boundaries does not resolve a cohesion problem.

Keep each API narrow and give it a clear purpose. Investigate:

- duplicate helpers or shadow APIs with slightly different names or behavior;
- boolean arguments that select unrelated modes;
- sprawling optional configuration or parameter bags;
- optionality, casts, generic dictionaries, or stringly typed state that obscure a known domain invariant;
- pass-through wrappers that only rename another call;
- abstractions with one implementation and no present boundary need;
- adapters, factories, registries, hooks, or plugin points created for hypothetical callers.

Parameterize repeated values only when they represent a real variation point. Do not trade repetition for a mega-helper, dynamic contract, or configuration soup.

## Control flow and failure boundaries

- Flatten nested conditions with guards or a clearer state model.
- Merge checks and branches that produce the same result.
- Delete flags used only to steer incidental control flow; look for special-case branches or scattered feature checks that a clearer owner or state model would eliminate.
- Keep exception handling at real boundaries; reject broad catches, swallowed errors, silent defaults, and best-effort behavior at correctness boundaries.
- Replace defensive handling of impossible states with an explicit invariant.
- Preserve useful error context without leaking secrets, prompts, model output, credentials, tokens, headers, claims, tool payloads, PII, or raw provider responses.

Look for check-then-act races, partial updates, unnecessarily long transactions, network work inside transactions, and needless sequential I/O. Prefer atomic related updates and concurrent independent work when that also simplifies reasoning.

## Generated residue and tests

Remove residue when it has no supported behavior or current requirement:

- dead branches, placeholders, speculative fallbacks, obsolete compatibility layers, and unused flexibility;
- generic names that discard domain meaning;
- fixture-shaped production branches, fake IDs, canned timestamps, and magic test values;
- copied parsing, path, date, time, and string logic when a canonical helper exists.

Keep comments and docstrings concise and focused on non-obvious current contracts, invariants, or behavior that clearer code cannot express. Remove obvious narration and patch history; preserve required public-API documentation and keep it accurate.

Prefer behavior tests over tests that mirror private helpers or only assert mock calls. Keep fixtures and setup explicit enough that failures explain the violated behavior.

## Safety and runtime basics

Inspect touched boundaries for:

- missing server-side authorization or authorization checked outside the observing transaction;
- unsafe query, shell, path, deserialization, or outbound-request construction;
- SSRF-shaped fetches, missing timeouts, unchecked return values, and unbounded loops or collections;
- sensitive content in logs and errors;
- dependency duplication or hallucinated APIs;
- stale caches, duplicate projections, and multiple sources of truth;
- cancellation windows that can strand committed state or runtime ownership.

Patch only in-scope high-confidence defects. Report broader security or architecture work separately rather than silently expanding authority.
