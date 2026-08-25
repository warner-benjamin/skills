# Code quality reference

Use this reference for backend, CLI, library, service, data, script, test, and general implementation code.

## Local contract and ownership

- Read adjacent maintained code before judging style or structure.
- Identify established patterns for module boundaries, dependency injection, configuration, validation, errors, logging, data models, naming, helper placement, and tests.
- Prefer canonical repository utilities and domain models over bespoke local variants.
- Verify that new imports, methods, packages, permissions, and defaults are real and used as their source defines.
- Move behavior to the module or type that already owns the concept. Avoid broad context objects and utility dumping grounds.

Keep each API narrow and give it a clear purpose. Report:

- duplicate helpers or shadow APIs with slightly different names or behavior;
- boolean arguments that select unrelated modes;
- sprawling optional configuration or parameter bags;
- generic dictionaries where the domain shape is known;
- pass-through wrappers that only rename another call;
- abstractions with one implementation and no present boundary need;
- adapters, factories, registries, hooks, or plugin points created for hypothetical callers.

Parameterize repeated values only when they represent a real variation point. Do not trade repetition for a mega-helper, dynamic contract, or configuration soup.

## Control flow and failure boundaries

- Flatten nested conditions with guards or a clearer state model.
- Merge checks and branches that produce the same result.
- Delete flags used only to steer incidental control flow.
- Keep exception handling at real boundaries; reject broad catches, swallowed errors, silent defaults, and best-effort behavior at correctness boundaries.
- Replace defensive handling of impossible states with an explicit invariant.
- Preserve useful error context without leaking secrets, prompts, model output, credentials, tokens, headers, claims, tool payloads, PII, or raw provider responses.

Look for check-then-act races, partial updates, unnecessarily long transactions, network work inside transactions, and needless sequential I/O. Prefer atomic related updates and concurrent independent work when that also simplifies reasoning.

## Generated residue and tests

Delete:

- dead branches, placeholders, speculative fallbacks, compatibility layers, and unused flexibility;
- comments or docstrings that narrate obvious code;
- generic names that discard domain meaning;
- fixture-shaped production branches, fake IDs, canned timestamps, and magic test values;
- copied parsing, path, date, time, and string logic when a canonical helper exists.

Prefer behavior tests over tests that mirror private helpers or only assert mock calls. Keep fixtures and setup explicit enough that failures explain the violated behavior. Do not weaken assertions or delete coverage to make cleanup easier.

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

## Pass bar

Pass only when every extra mechanism has a current reason, behavior has a clear owner, control flow reflects explicit invariants, tests prove observable behavior, and no simpler framing would remove meaningful complexity.
