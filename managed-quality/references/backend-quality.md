# Backend and general code quality

Read this for backend, CLI, library, data, service, script, test, and other non UI code.

## Establish the implementation contract

Start with the feature requirements, real callers, data shapes, failure behavior, and non goals. Identify which module or type should own the behavior.

Read adjacent modules when they provide relevant contracts for dependency injection, configuration, validation, errors, logging, data shapes, helper placement, or tests.

For a new subsystem, choose one direct contract before auditing it. State the public entry point, owned state, dependencies, failure boundary, supported variation, and intentionally unsupported flexibility.

Prefer domain vocabulary and existing repository utilities when they fit the requirement. Verify that new imports, packages, methods, configuration keys, and APIs exist and are used in the expected way.

## Audit ownership and APIs

Look for duplicate helpers and shadow APIs with slightly different names or one off behavior. Consolidate into the canonical owner when one exists.

Move behavior to the module or type that already owns the concept. Avoid shared utility bins and broad context objects that couple unrelated work.

Keep interfaces narrow and explicit. Flag these patterns:

- boolean arguments that make callers choose unrelated modes
- configuration bags with many optional values
- parameter objects that group data with no shared meaning
- generic dictionaries or loose objects where the repository uses typed models
- pass through wrappers that only rename another call

Use a parameter or object only when it represents a real variation or cohesive domain value.

## Remove generated residue

Delete speculative factories, hooks, registries, adapters, fallback branches, and placeholder implementations with no concrete caller or product need.

Remove comments and docstrings that narrate obvious code. Keep comments for non obvious intent, invariants, compatibility constraints, and tradeoffs.

Replace fixture shaped values, copied constants, fake IDs, canned timestamps, and test specific branches with the real rule. Keep fixtures in tests, stories, or named fixture modules.

Do not generalize a one case behavior unless the variation is present in current requirements or callers.

## Simplify control flow and failures

Flatten nested condition ladders with direct guards and early returns when that matches local style. Merge checks that produce the same result and delete state flags used only to steer control flow.

Keep exception handling at real boundaries. Flag broad catches that swallow uncertainty, log and continue without a contract, or return silent defaults for impossible states.

Use explicit precondition checks for expected cases. Preserve useful error context and follow the repository's error type and logging conventions.

## Check tests

Prefer tests that prove behavior over tests that mirror private methods or only assert mock calls.

Look for production branches that recognize fixture names, sample values, or test timing. Remove those branches and fix the test setup.

Keep test helpers small and parameterized around meaningful scenarios. Avoid hidden setup, giant fixtures, and snapshots that obscure the behavior under test.

Confirm that cleanup does not weaken assertions or delete coverage merely to make the implementation easier.

## Check runtime basics

Inspect touched code for high confidence issues with authorization, secret handling, logs, queries, shell commands, paths, deserialization, outbound requests, timeouts, unchecked results, and check then act races.

Check for avoidable repeated work, unbounded loops or collections, needless sequential I/O, and partial updates. Fix only what is local and clear. Report broader security or architecture work instead of expanding the cleanup silently.

## Backend pass bar

Pass when the code has an intentional owner and API, has direct control flow, exposes a clear contract, keeps tests focused on behavior, and contains no speculative or fixture shaped residue. New code does not need an older local twin, but every extra mechanism needs a current reason.
