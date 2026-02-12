# Design Token Specification

Generate all tokens as CSS custom properties under `:root`.
Use this structure as the baseline — expand or contract based on the project's needs.

## Colors

### Primary palette

Generate a primary color with 10 shades (50–950) using perceptually uniform lightness steps. When the user provides a hex, use it as the 500 (mid) value and derive the rest.

```css
--color-primary-50: ...; /* lightest tint */
--color-primary-100: ...;
--color-primary-200: ...;
--color-primary-300: ...;
--color-primary-400: ...;
--color-primary-500: ...; /* base */
--color-primary-600: ...;
--color-primary-700: ...;
--color-primary-800: ...;
--color-primary-900: ...;
--color-primary-950: ...; /* darkest shade */
```

### Secondary palette

Same 50–950 scale. Choose a complementary, analogous, or split-complementary hue depending on the style direction.

### Neutral palette

A gray scale (50–950) with a subtle warm or cool tint that matches the primary hue. Pure gray is rarely ideal.

### Semantic colors

```css
--color-success: ...; /* green family */
--color-warning: ...; /* amber/yellow family */
--color-error: ...; /* red family */
--color-info: ...; /* blue family */
```

Each semantic color also gets a `-light` (background) and `-dark` (text-on-background) variant.

### Surface colors

```css
--color-background: ...;
--color-surface: ...;
--color-surface-raised: ...;
--color-border: ...;
--color-border-subtle: ...;
```

### Text colors

```css
--color-text: ...;
--color-text-secondary: ...;
--color-text-tertiary: ...;
--color-text-inverse: ...;
--color-text-on-primary: ...;
```

## Typography

### Font families

Choose fonts that are beautiful, unique, and interesting. Avoid generic fonts like Arial and Inter; opt instead for distinctive choices that elevate the frontend's aesthetics; unexpected, characterful font choices. Pair a distinctive display font with a refined body font.

Replace with user-specified fonts when provided. Always include system fallbacks.

### Font sizes (modular scale)

Use a ratio between 1.2 (minor third) and 1.333 (perfect fourth). Base size: 1rem (16px).

```css
--text-xs: 0.75rem; /* 12px */
--text-sm: 0.875rem; /* 14px */
--text-base: 1rem; /* 16px */
--text-lg: 1.125rem; /* 18px */
--text-xl: 1.25rem; /* 20px */
--text-2xl: 1.5rem; /* 24px */
--text-3xl: 1.875rem; /* 30px */
--text-4xl: 2.25rem; /* 36px */
```

### Font weights

```css
--font-normal: 400;
--font-medium: 500;
--font-semibold: 600;
--font-bold: 700;
```

### Line heights

```css
--leading-tight: 1.25;
--leading-normal: 1.5;
--leading-relaxed: 1.75;
```

### Letter spacing

```css
--tracking-tight: -0.025em;
--tracking-normal: 0;
--tracking-wide: 0.025em;
```

## Spacing

Use a base-4 or base-8 system. Generate a scale:

```css
--space-0: 0;
--space-1: 0.25rem; /* 4px */
--space-2: 0.5rem; /* 8px */
--space-3: 0.75rem; /* 12px */
--space-4: 1rem; /* 16px */
--space-5: 1.25rem; /* 20px */
--space-6: 1.5rem; /* 24px */
--space-8: 2rem; /* 32px */
--space-10: 2.5rem; /* 40px */
--space-12: 3rem; /* 48px */
--space-16: 4rem; /* 64px */
--space-20: 5rem; /* 80px */
```

## Border radius

```css
--radius-none: 0;
--radius-sm: 0.25rem; /* 4px */
--radius-md: 0.5rem; /* 8px */
--radius-lg: 0.75rem; /* 12px */
--radius-xl: 1rem; /* 16px */
--radius-2xl: 1.5rem; /* 24px */
--radius-full: 9999px;
```

Adjust the scale to match the style — playful designs use larger radii, corporate designs use smaller.

## Shadows

```css
--shadow-xs: 0 1px 2px rgba(0, 0, 0, 0.05);
--shadow-sm: 0 1px 3px rgba(0, 0, 0, 0.1), 0 1px 2px rgba(0, 0, 0, 0.06);
--shadow-md: 0 4px 6px rgba(0, 0, 0, 0.1), 0 2px 4px rgba(0, 0, 0, 0.06);
--shadow-lg: 0 10px 15px rgba(0, 0, 0, 0.1), 0 4px 6px rgba(0, 0, 0, 0.05);
--shadow-xl: 0 20px 25px rgba(0, 0, 0, 0.1), 0 8px 10px rgba(0, 0, 0, 0.04);
```

Tint shadows with the primary or neutral hue for more cohesion.

## Transitions

```css
--duration-fast: 100ms;
--duration-normal: 200ms;
--duration-slow: 300ms;
--ease-default: cubic-bezier(0.4, 0, 0.2, 1);
--ease-in: cubic-bezier(0.4, 0, 1, 1);
--ease-out: cubic-bezier(0, 0, 0.2, 1);
```

## Breakpoints (for reference, not as custom properties)

```
sm:  640px
md:  768px
lg:  1024px
xl:  1280px
2xl: 1536px
```

## Z-index scale

```css
--z-dropdown: 1000;
--z-sticky: 1100;
--z-overlay: 1300;
--z-modal: 1400;
--z-toast: 1500;
```

## Dark Mode

When dark mode is requested (or when the style calls for it), generate a second set of surface, text, and border tokens under a `[data-theme="dark"]` or `@media (prefers-color-scheme: dark)` selector. Primary/secondary color shades typically stay the same; adjust surface/text/shadow tokens.
