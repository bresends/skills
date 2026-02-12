# Component Patterns

Every component must consume design tokens from `tokens.css` — never hardcode color, spacing, or typography values.

## General Rules

- Use `var(--token-name)` for all visual properties
- Components are self-contained — each file includes its own styles (CSS modules, scoped styles, styled-components, or `<style>` blocks depending on framework)
- Every component exposes a `className` / `class` prop for overrides
- Use semantic HTML elements (`<button>`, `<input>`, `<article>`, etc.)
- Include basic accessibility: labels, focus states, aria attributes where needed

## Component Specifications

### Button

**Variants:** primary, secondary, ghost, destructive
**Sizes:** sm, md, lg
**States:** default, hover, active, focus-visible, disabled

```
primary   → bg: primary-500, text: text-on-primary, hover: primary-600
secondary → bg: transparent, border: border, text: text, hover: surface-raised
ghost     → bg: transparent, text: text-secondary, hover: surface
destructive → bg: error, text: white, hover: error-dark
```

Size mapping:

```text
sm → text-sm,  py: space-1, px: space-3, radius-sm
md → text-base, py: space-2, px: space-4, radius-md
lg → text-lg,  py: space-3, px: space-6, radius-md
```

Include focus-visible ring: `outline: 2px solid var(--color-primary-500); outline-offset: 2px`.

### Input

**Parts:** wrapper, label, input field, helper/error text
**States:** default, focus, error, disabled

```text
border: border → focus: primary-500
error state: border → error, helper text in error color
label: text-sm, font-medium, text-secondary
```

### Card

**Slots:** header (optional), body, footer (optional)

```text
bg: surface, border: border-subtle, radius: radius-lg, shadow: shadow-sm
header: border-bottom, padding space-4
body: padding space-4
footer: border-top, padding space-4, bg: surface-raised (subtle)
```

### Badge

**Variants:** default, info, success, warning, error

```text
default → bg: neutral-100, text: neutral-700
info    → bg: info-light, text: info-dark
success → bg: success-light, text: success-dark
warning → bg: warning-light, text: warning-dark
error   → bg: error-light, text: error-dark
```

Small, inline element: `text-xs, font-medium, px: space-2, py: space-0.5, radius-full`.

### Typography

Expose heading and text components that map to the type scale.

```text
h1 → text-4xl, font-bold, leading-tight, tracking-tight
h2 → text-3xl, font-bold, leading-tight
h3 → text-2xl, font-semibold, leading-tight
h4 → text-xl, font-semibold, leading-normal
body → text-base, font-normal, leading-normal
caption → text-sm, text-secondary, leading-normal
code → font-mono, text-sm, bg: surface-raised, px: space-1, radius-sm
```

## Framework-Specific Patterns

### React (JSX/TSX)

- One component per file, named export
- Props interface with `variant`, `size`, `className`, `children`
- Use CSS modules (`.module.css`) or inline `<style>` in preview
- Example structure:

```tsx
interface ButtonProps {
  variant?: "primary" | "secondary" | "ghost" | "destructive";
  size?: "sm" | "md" | "lg";
  className?: string;
  children: React.ReactNode;
}

export function Button({
  variant = "primary",
  size = "md",
  className,
  children,
  ...props
}: ButtonProps) {
  return (
    <button
      className={`btn btn-${variant} btn-${size} ${className ?? ""}`}
      {...props}
    >
      {children}
    </button>
  );
}
```

### Plain HTML/CSS

- Components as CSS class patterns (`.btn`, `.btn--primary`, `.card`, etc.)
- BEM naming convention
- All variants shown in `preview.html`

## preview.html

The preview page must:

1. Import `tokens.css`
2. Include all component styles (inline or via `<link>`)
3. Show every component in every variant and size
4. Group components in sections with headings
5. Use a clean layout with spacing between sections
6. Work by opening the file directly in a browser (no build step)
7. Include a color palette swatch grid showing primary, secondary, and neutral scales
8. Include a semantic colors section showing success, warning, error, and info with their light/dark variants
9. Include a shadow showcase displaying each shadow level (xs–xl) on sample cards
10. Include a typography specimen showing all type scale levels
