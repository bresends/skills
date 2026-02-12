---
name: design-system
description: Generate complete design systems with design tokens and UI components. Use when the user wants to create a design system, UI kit or component or theme for a project. Handles vague creative briefs ("make something for a fintech app"), reference images (screenshots, mockups, mood boards), and precise specifications ("use #2563EB as primary, Inter font, 8px grid"). Outputs token files and framework-specific components.
---

# Design System Generator

Generate design tokens and UI components from a creative brief or detailed specification.

## Workflow

1. **Interpret the brief** — Determine what the user specified vs. what needs creative decisions
2. **Establish tokens** — Generate the full token set (see [references/tokens.md](references/tokens.md))
3. **Generate components** — Build components using the tokens (see [references/components.md](references/components.md))
4. **Output files** — Write everything to disk in a clean structure

## Step 1: Interpret the Brief

Users provide anything from a single sentence to a full spec. Extract what's explicit and fill in the rest creatively.

**Explicit inputs to look for:**

- Style direction (minimal, playful, corporate, brutalist, etc.)
- Reference image (screenshot, mockup, mood board, or existing UI)
- Brand colors (hex, RGB, HSL, or named colors)
- Typography (font families, scale preferences, weight)
- Spacing and radius
- Framework target (React, Vue, Svelte, plain HTML/CSS, etc.)
- Dark mode preference

**When the user provides a reference image**, read it with the Read tool and extract design tokens:

- Dominant colors and color relationships (primary, secondary, accent, neutrals)
- Typography style (serif/sans-serif/mono, weight usage, size hierarchy)
- Spacing density (tight/comfortable/spacious)
- Border radius tendencies (sharp/slightly rounded/very rounded/pill)
- Shadow usage (flat/subtle/elevated)
- Overall aesthetic (the mood, era, and personality of the design)

Use these observations as the foundation for all token decisions. The generated system should feel like it belongs to the same visual family as the reference.

**When the user is vague**, make bold creative choices. Don't default to safe/generic — create something with personality. Use the project context to drive decisions.

**When the user is specific**, follow their constraints and fill only the remaining gaps.

If no framework is specified, ask which framework to target.

## Step 2: Establish Tokens

Read [references/tokens.md](references/tokens.md) for the complete token specification.

Generate tokens as CSS custom properties in a `tokens.css` file and optionally as a JSON file (`tokens.json`) for programmatic use.

## Step 3: Generate Components

Read [references/components.md](references/components.md) for component patterns per framework.

Generate a core set of components that consume the tokens:

- **Button** (primary, secondary, ghost, destructive; sizes sm/md/lg)
- **Input** (text, with label, with error state)
- **Card** (with header, body, footer slots)
- **Badge** (status variants: info, success, warning, error)
- **Typography** (heading levels h1-h4, body, caption, code)

Add more components if the user's context calls for them (e.g., data tables for dashboards, navigation for apps).

## Step 4: Output Structure

```text
design-system/
├── tokens.css              # CSS custom properties
├── tokens.json             # Machine-readable tokens (optional)
├── components/
│   ├── Button.{ext}
│   ├── Input.{ext}
│   ├── Card.{ext}
│   ├── Badge.{ext}
│   └── Typography.{ext}
└── preview.{ext}            # Single-page preview of all components
```

`{ext}` matches the target framework (`.jsx`, `.vue`, `.svelte`, `.html`, etc.).

The `preview.html` file should be a standalone page that imports `tokens.css` and renders every component variant so the user can visually review the system. Inline the component styles if needed so the preview works by just opening the file in a browser.
