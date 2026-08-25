# Frontend quality reference

Use this reference for components, routes, pages, styles, browser behavior, and other user-interface code.

## Establish the product contract

- Read nearby pages, components, routes, layout shells, hooks, state patterns, design tokens, shared primitives, and product copy.
- Identify the user, primary job, information hierarchy, data model, supported states, product tone, responsive behavior, and interaction constraints.
- Preserve established product structure unless the user authorizes a redesign.
- When no useful precedent exists, define one explicit interface contract instead of falling back to a generic dashboard or landing page.

If runnable, inspect the real UI. Use screenshots only as evidence for visible claims. Treat code, interaction, responsive, and accessibility claims as inferred until source, the DOM or accessibility tree, or browser behavior proves them.

## Data, state, and component shape

Review data flow before styling. Flag:

- fixture screens built from hard-coded sample arrays, perfect strings, or fake metrics;
- duplicated JSX or CSS that differs only by literals;
- boolean-mode prop soup and component APIs that expose implementation details instead of domain state;
- one component owning unrelated data fetching, state, layout, and interaction responsibilities;
- lifted or global state without a real shared owner;
- missing loading, empty, error, disabled, success, recovery, permission, long-content, or many-row behavior;
- manually owned server state that the repository's canonical data layer should own.

Prefer narrow typed props, real domain data, established variants, slots or children, and small components with genuine responsibilities. Componentize only when it removes current duplication, supports real states, or matches a local primitive.

## Design-system and visual quality

Reuse established buttons, fields, dialogs, menus, cards, tables, tokens, spacing, type, color, radius, shadow, and motion. Extend a local primitive through its normal API instead of styling around it repeatedly.

Treat these as smells only when the diff introduces them without product or design-system support:

- generic purple, indigo, or cyan gradients and glows;
- glass panels, blurred blobs, gradient headlines, and decorative charting;
- every concept in the same rounded card;
- repeated icon pills, equal-weight metric tiles, or centered generic landing-page composition;
- arbitrary fonts, radii, shadows, spacing, utility strings, or inline styles;
- vague headings, transformation claims, and unclear action labels;
- hover scale and animation without interaction meaning.

Remove containers and decoration that add no grouping, state, or meaning. Do not overcorrect with novelty fonts, random ornaments, or visual inconsistency.

## Accessibility and resilience

Use native semantics first. Inspect accessible names, labels, headings, landmarks, visible focus, keyboard order, dialog and menu behavior, contrast, touch targets, reduced motion, and non-color state cues.

Exercise narrow screens, larger text, long labels, missing values, overflow, many rows, asynchronous state changes, and failure recovery. A desktop layout that merely shrinks without deciding mobile priority is incomplete.

Use concrete product copy that names the object, state, and next action. Preserve known information architecture and tone unless the review finds a concrete usability defect.

## Browser verification

After a frontend repair:

- reopen the changed surface at representative desktop and mobile sizes;
- exercise the primary flow and supported negative states;
- tab through interactive controls and inspect the accessibility tree when available;
- compare against supplied references or the existing product, not an invented aesthetic;
- rerun the repository's existing component, browser, visual, type, lint, and build checks as relevant.

Do not introduce a new UI framework, component system, state library, or test framework solely for cleanup.

## Pass bar

Pass only when the interface uses real data shapes, justified components and tokens, clear product-specific hierarchy, resilient states, responsive and keyboard behavior, concrete copy, and no high-confidence generic AI default that conflicts with the product contract.
