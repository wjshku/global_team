# Style Guide - Global Team Manager

## Overview
This document outlines the design system and style guidelines for the Global Team Manager application. The application uses a **light black primary theme** with a comprehensive design system built on CSS custom properties.

## Color Palette

### Primary Colors (Light Black Theme)
- **Primary**: `#2d3748` - Main brand color
- **Primary Hover**: `#1a202c` - Darker shade for hover states
- **Primary Light**: `#4a5568` - Lighter shade for accents
- **Primary Dark**: `#1a202c` - Darkest shade for emphasis

### Secondary Colors
- **Secondary**: `#6b7280` - Supporting color
- **Secondary Hover**: `#4b5563` - Hover state
- **Secondary Light**: `#9ca3af` - Light accent
- **Secondary Dark**: `#374151` - Dark accent

### Status Colors
- **Success**: `#10b981` - Success states
- **Warning**: `#f59e0b` - Warning states
- **Danger**: `#ef4444` - Error states
- **Info**: `#3b82f6` - Information states

### Gray Scale
- **Gray 50**: `#f7fafc` - Lightest background
- **Gray 100**: `#edf2f7` - Light background
- **Gray 200**: `#e2e8f0` - Border color
- **Gray 300**: `#cbd5e0` - Light border
- **Gray 400**: `#a0aec0` - Muted text
- **Gray 500**: `#718096` - Secondary text
- **Gray 600**: `#4a5568` - Primary text
- **Gray 700**: `#2d3748` - Dark text
- **Gray 800**: `#1a202c` - Darkest text
- **Gray 900**: `#171923` - Black text

## Typography

### Font Sizes
- **xs**: `0.75rem` (12px)
- **sm**: `0.875rem` (14px)
- **base**: `1rem` (16px)
- **lg**: `1.125rem` (18px)
- **xl**: `1.25rem` (20px)
- **2xl**: `1.5rem` (24px)
- **3xl**: `1.875rem` (30px)
- **4xl**: `2.25rem` (36px)
- **5xl**: `3rem` (48px)
- **6xl**: `3.75rem` (60px)

### Font Weights
- **Thin**: 100
- **Light**: 300
- **Normal**: 400
- **Medium**: 500
- **Semibold**: 600
- **Bold**: 700
- **Extrabold**: 800
- **Black**: 900

## Spacing System

### Spacing Scale
- **0**: `0`
- **px**: `1px`
- **0.5**: `0.125rem` (2px)
- **1**: `0.25rem` (4px)
- **1.5**: `0.375rem` (6px)
- **2**: `0.5rem` (8px)
- **2.5**: `0.625rem` (10px)
- **3**: `0.75rem` (12px)
- **3.5**: `0.875rem` (14px)
- **4**: `1rem` (16px)
- **5**: `1.25rem` (20px)
- **6**: `1.5rem` (24px)
- **7**: `1.75rem` (28px)
- **8**: `2rem` (32px)
- **9**: `2.25rem` (36px)
- **10**: `2.5rem` (40px)
- **11**: `2.75rem` (44px)
- **12**: `3rem` (48px)
- **14**: `3.5rem` (56px)
- **16**: `4rem` (64px)
- **20**: `5rem` (80px)
- **24**: `6rem` (96px)
- **28**: `7rem` (112px)
- **32**: `8rem` (128px)

## Gradients

### Primary Gradients
- **Primary**: `linear-gradient(135deg, #2d3748 0%, #1a202c 100%)`
- **Secondary**: `linear-gradient(135deg, #4a5568 0%, #2d3748 100%)`
- **Card**: `linear-gradient(135deg, #f7fafc 0%, #edf2f7 100%)`
- **Header**: `linear-gradient(135deg, #2d3748 0%, #1a202c 100%)`

## Component Guidelines

### Buttons
- Use `BaseButton` component instead of global `.btn` classes
- Variants: `primary`, `secondary`, `danger`
- Sizes: `small`, `medium`, `large`
- States: `disabled`, `loading`

### Cards
- Use `BaseCard` component for consistent card styling
- Props: `shadow`, `border`, `hover`, `padding`, `clickable`

### Forms
- Use `BaseForm` component for form consistency
- Use utility classes for spacing and layout
- Follow accessibility guidelines for form elements

## Utility Classes

### Spacing
- Margin: `.m-{size}`, `.mt-{size}`, `.mb-{size}`, `.ml-{size}`, `.mr-{size}`
- Padding: `.p-{size}`, `.pt-{size}`, `.pb-{size}`, `.pl-{size}`, `.pr-{size}`

### Colors
- Text: `.text-{color}`, `.text-primary`, `.text-secondary`
- Background: `.bg-{color}`, `.bg-primary`, `.bg-secondary`

### Typography
- Size: `.text-{size}`
- Weight: `.font-{weight}`
- Alignment: `.text-{alignment}`

## Dark Mode

The application supports dark mode with automatic theme switching. Dark mode uses:
- Darker backgrounds with lighter text
- Adjusted color scales for better contrast
- Consistent gradient system

## Accessibility

### Focus States
- All interactive elements have visible focus indicators
- Focus rings use `rgba(102, 126, 234, 0.1)` for consistency

### Color Contrast
- All text meets WCAG AA contrast requirements
- Status colors are distinguishable for colorblind users

### Reduced Motion
- Respects `prefers-reduced-motion` media query
- Animations are disabled for users who prefer reduced motion

## File Organization

```
src/styles/
├── variables.css          # Design tokens
├── main.css              # Global styles & utilities
├── components.css        # Shared component styles
├── themes/
│   ├── light.css         # Light theme overrides
│   └── dark.css          # Dark theme overrides
└── utilities/
    ├── spacing.css       # Spacing utilities
    ├── colors.css        # Color utilities
    └── typography.css    # Typography utilities
```

## Best Practices

1. **Use CSS Variables**: Always use CSS custom properties for colors, spacing, and other design tokens
2. **Component Scoping**: Use `<style scoped>` for component-specific styles
3. **Utility First**: Prefer utility classes over custom CSS when possible
4. **Consistent Naming**: Follow BEM-like naming conventions for component classes
5. **Accessibility**: Always consider accessibility when adding new styles
6. **Performance**: Use CSS purging in production builds
7. **Documentation**: Document any new design patterns or utilities

## Migration Notes

- **Deprecated**: Global `.btn` classes (use `BaseButton` component instead)
- **New**: Gradient variables for consistent gradient usage
- **Updated**: Light black primary theme throughout the application
- **Improved**: Better dark mode support with consistent color scales
