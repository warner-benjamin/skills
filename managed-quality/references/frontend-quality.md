# Frontend code and interface quality

Read this for components, pages, routes, styles, browser behavior, and other user interface code.

## Establish the interface contract

Start with the user, primary job, content and data, required states, product tone, and interaction constraints. Preserve the existing product structure unless the plan authorizes a redesign.

Read nearby pages, components, layout shells, hooks, state patterns, design tokens, shared primitives, and product copy when they provide relevant constraints.

For a new interface with no useful precedent, choose one explicit design contract before auditing it. State the primary action, information hierarchy, data model, state set, layout behavior, token rules, type direction, and motion rule. Do not fall back to a generic dashboard or landing page because no local screen exists.

When the interface can run, inspect it in a browser. Check at least one desktop size and one mobile size. Exercise loading, empty, error, long content, disabled, and permission states that the changed surface supports.

Use screenshots alone only for visible findings. Mark code, accessibility, or interaction claims as inferred until source, browser behavior, or the accessibility tree proves them.

## Audit data and component shape

Look for screens built around hard coded sample arrays, copied cards, perfect strings, fake metrics, or one fixed data shape. Move demo data to tests, stories, or fixtures and render the real domain shape through props or state.

Prefer narrow component APIs. Flag these patterns:

- many booleans that select unrelated layouts or visual modes
- props that expose implementation details instead of domain state
- duplicated JSX that differs only by literals
- one component that owns unrelated data, state, layout, and interaction jobs
- lifted state or global state with no shared owner that needs it

Use local primitives, stable variants, slots, children, and typed data only when they remove current duplication or support real states.

## Audit the design system

Reuse existing buttons, forms, dialogs, menus, cards, tokens, spacing, type, color, radius, shadow, and motion rules. Extend a local primitive through its established API instead of styling around it at every use site.

Flag arbitrary values, copied utility strings, inline styles, and one off CSS when they repeat a token or component role that already exists.

Do not replace native semantics or proven local components with clickable containers or custom accessibility code.

## Remove generic AI visual defaults

Treat these as smells only when the diff introduces them without support from the local design system or product brief:

- purple, indigo, or cyan gradients and glows
- glass surfaces, blurred blobs, and gradient headline text
- every concept placed inside the same rounded card
- repeated icon pills above headings
- one font, weight, spacing, and radius used everywhere
- equal weight dashboard tiles with no clear primary job
- generic landing page order and centered composition
- decorative charts, metrics, animation, or hover scale with no product meaning
- vague copy such as generic transformation claims or unclear action labels

Remove containers and decoration that add no grouping, state, or meaning. Preserve a common visual choice when it is already part of the documented product system.

Do not overcorrect with novelty fonts, random ornaments, or visual inconsistency. Human quality comes from product intent and local consistency, not from being unusual.

## Check accessibility and resilience

Use native elements first. Check names and labels, visible focus, keyboard order, dialog and menu behavior, headings, landmarks, contrast, touch targets, reduced motion, and non color state cues.

Test narrow screens, larger text, long labels, missing values, many rows, and overflow. Do not accept a desktop layout that only shrinks without deciding what mobile users need first.

Make loading, empty, error, disabled, success, and recovery states useful. Use concrete copy that names the object and next action.

## Browser verification

After cleanup, reopen the changed surface. Compare desktop and mobile behavior, tab through the main flow, inspect the accessibility tree when tools allow, and rerun existing visual or browser tests.

Add tests only through the repository's current browser or component test setup. Do not introduce a new framework only for this quality pass.

## Frontend pass bar

Pass when the interface uses real data shapes, justified components and tokens, clear product specific hierarchy, concrete copy, resilient states, and working keyboard and responsive behavior. Leave no high confidence generic AI default that conflicts with the product intent or chosen design contract.
