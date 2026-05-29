---
name: Private Finance Analyzer
colors:
  surface: '#f7f9fb'
  surface-dim: '#d8dadc'
  surface-bright: '#f7f9fb'
  surface-container-lowest: '#ffffff'
  surface-container-low: '#f2f4f6'
  surface-container: '#eceef0'
  surface-container-high: '#e6e8ea'
  surface-container-highest: '#e0e3e5'
  on-surface: '#191c1e'
  on-surface-variant: '#45464d'
  inverse-surface: '#2d3133'
  inverse-on-surface: '#eff1f3'
  outline: '#76777d'
  outline-variant: '#c6c6cd'
  surface-tint: '#565e74'
  primary: '#000000'
  on-primary: '#ffffff'
  primary-container: '#131b2e'
  on-primary-container: '#7c839b'
  inverse-primary: '#bec6e0'
  secondary: '#505f76'
  on-secondary: '#ffffff'
  secondary-container: '#d0e1fb'
  on-secondary-container: '#54647a'
  tertiary: '#000000'
  on-tertiary: '#ffffff'
  tertiary-container: '#002113'
  on-tertiary-container: '#009668'
  error: '#ba1a1a'
  on-error: '#ffffff'
  error-container: '#ffdad6'
  on-error-container: '#93000a'
  primary-fixed: '#dae2fd'
  primary-fixed-dim: '#bec6e0'
  on-primary-fixed: '#131b2e'
  on-primary-fixed-variant: '#3f465c'
  secondary-fixed: '#d3e4fe'
  secondary-fixed-dim: '#b7c8e1'
  on-secondary-fixed: '#0b1c30'
  on-secondary-fixed-variant: '#38485d'
  tertiary-fixed: '#6ffbbe'
  tertiary-fixed-dim: '#4edea3'
  on-tertiary-fixed: '#002113'
  on-tertiary-fixed-variant: '#005236'
  background: '#f7f9fb'
  on-background: '#191c1e'
  surface-variant: '#e0e3e5'
typography:
  display-lg:
    fontFamily: Geist
    fontSize: 48px
    fontWeight: '700'
    lineHeight: 56px
    letterSpacing: -0.02em
  headline-lg:
    fontFamily: Geist
    fontSize: 32px
    fontWeight: '600'
    lineHeight: 40px
    letterSpacing: -0.01em
  headline-lg-mobile:
    fontFamily: Geist
    fontSize: 24px
    fontWeight: '600'
    lineHeight: 32px
  headline-md:
    fontFamily: Geist
    fontSize: 24px
    fontWeight: '600'
    lineHeight: 32px
  body-lg:
    fontFamily: Geist
    fontSize: 18px
    fontWeight: '400'
    lineHeight: 28px
  body-md:
    fontFamily: Geist
    fontSize: 16px
    fontWeight: '400'
    lineHeight: 24px
  label-md:
    fontFamily: Geist
    fontSize: 14px
    fontWeight: '500'
    lineHeight: 20px
    letterSpacing: 0.01em
  label-sm:
    fontFamily: Geist
    fontSize: 12px
    fontWeight: '600'
    lineHeight: 16px
    letterSpacing: 0.05em
rounded:
  sm: 0.25rem
  DEFAULT: 0.5rem
  md: 0.75rem
  lg: 1rem
  xl: 1.5rem
  full: 9999px
spacing:
  unit: 4px
  xs: 4px
  sm: 8px
  md: 16px
  lg: 24px
  xl: 40px
  container-margin: 32px
  gutter: 20px
---

## Brand & Style
The design system is anchored in the concepts of **Financial Intelligence** and **Edge Privacy**. The aesthetic is a fusion of **Corporate Modern** and **High-End Minimalism**, evoking the feeling of a private digital vault that is as powerful as it is secure.

The UI targets high-intent users who value data sovereignty. It prioritizes clarity over decoration, using generous whitespace to reduce cognitive load during complex financial analysis. The visual language is precise, intentional, and reassuringly stable.

## Colors
The palette is dominated by **Deep Navy** (Stability) and **Slate** (Professionalism), creating a grounded foundation. **Crisp White** and **Ghost Gray** backgrounds ensure the interface feels airy and legible.

**Safety Green** is used surgically to denote positive financial trends and "Local-Only" data states. We introduce **AI Blue** specifically for "Intelligence" indicators—this color should only appear when the local machine learning models are active, creating a distinct visual cue for the software's "thinking" state.

## Typography
This design system utilizes **Geist** for its technical precision and exceptional legibility in data-dense environments. 

Headlines use a tighter letter-spacing and heavier weights to feel authoritative. Body text maintains a comfortable line height to ensure financial statements and insights are easily scannable. Numeric data should always utilize the tabular figures feature of the font to ensure columns of currency align perfectly.

## Layout & Spacing
The system follows a strict **8px grid** (with a 4px sub-grid for fine details). The layout uses a **fixed-fluid hybrid model**:
- **Desktop:** 12-column grid, max-width 1440px, centered.
- **Tablet:** 8-column grid, fluid margins.
- **Mobile:** 4-column grid, 16px side margins.

Horizontal spacing between cards and modules is generous (`xl`) to emphasize the "Analyzer" aspect of the tool, preventing the UI from feeling cluttered or overwhelming.

## Elevation & Depth
Depth is expressed through **Tonal Layering** supplemented by **Ambient Shadows**. 

The background layer is always the lightest (`#F8FAFC`). Primary interaction cards sit on "Level 1" with a very soft, diffused shadow (Blur: 12px, Y: 4px, Opacity: 4% Black). 

Overlays and Modals sit on "Level 2" with a more pronounced shadow and a subtle 1px border (`#E2E8F0`). Avoid heavy shadows; the goal is to make elements appear as if they are resting lightly on a flat surface, not floating high above it.

## Shapes
The shape language is **Rounded**, using a base radius of `8px` (0.5rem). 

- **Small Components (Buttons, Inputs):** 8px.
- **Medium Components (Cards, Sections):** 16px.
- **Large Components (Modals):** 24px.

This balance avoids the clinical feel of sharp corners while maintaining a professional rigor that "Pill-shaped" buttons often lack.

## Components

### Buttons
- **Primary:** Deep Navy background, white text. No gradient. 
- **Secondary:** White background, 1px Slate-200 border, Deep Navy text.
- **Success:** Safety Green background, white text (used for "Finalize" or "Confirmed").

### Cards
Cards are the primary container. They feature a white background, the Level 1 shadow, and a subtle 1px border in `#F1F5F9`. Internal padding is typically `24px`.

### Local AI Status Indicators
A specialized component for this system. 
- **State: Idle:** A small 8px dot in Slate-300 with the label "Local AI Ready".
- **State: Processing:** The dot changes to **AI Blue** with a soft, 4px outer glow pulse (2-second duration).
- **State: Private/Secure:** A "Shield" icon in Safety Green appearing next to data points that have been analyzed locally.

### Input Fields
Fields use a 1px Slate-200 border. On focus, the border transitions to Deep Navy with a 2px outer "ring" of AI Blue at 20% opacity.

### Data Lists
Financial transactions use alternating row highlights in Ghost Gray (`#F8FAFC`) only on hover. Default state is clean white with thin horizontal dividers.