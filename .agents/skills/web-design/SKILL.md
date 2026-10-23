---
name: web-design
description: Guidelines, design tokens, component archetypes, and layout heuristics for crafting stunning, accessible, human-centered web applications. Incorporates Claude-inspired warm editorial palettes (cream, coral, dark navy), serif display typography, responsive spatial grids, and micro-interactions.
---

# Web Design & UI/UX Craftsmanship Skill

This skill provides comprehensive instructions, tokens, and component archetypes for building world-class web user interfaces with exceptional visual hierarchy, typography, and layout balance.

---

## 1. The Warm Editorial Design Language (Claude-Inspired)

Modern tech products often feel sterile when using cold grays and harsh saturated blues. The **Warm Editorial** design system counters this with warmth, literary refinement, and deliberate contrast.

### Color Tokens
- **Canvas (`#faf9f5`)**: Default page floor. Tinted cream, warm, calm, non-glaring.
- **Surface Soft (`#f5f0e8`)**: Section dividers, subtle background bands.
- **Surface Card (`#efe9de`)**: Content card backgrounds, feature cards.
- **Surface Dark (`#181715`)**: High-contrast product surfaces, terminal mockups, code windows.
- **Primary Coral (`#cc785c`)**: Signature action voltage. Used for primary CTAs, active highlights.
- **Primary Active (`#a9583e`)**: Pressed/hover-darkened coral.
- **Ink / Headlines (`#141413`)**: Deep charcoal/ink for high contrast headlines.
- **Body Text (`#3d3d3a`)**: Warm readable dark neutral for paragraphs.
- **Muted / Captions (`#6c6a64`)**: Secondary information and helper labels.
- **Hairline (`#e6dfd8`)**: 1px subtle card/input borders.
- **Accents**:
  - Emerald Success: `#5db872` (or `#10b981`)
  - Warm Amber: `#e8a55a`
  - Soft Teal: `#5db8a6`
  - Crimson Error: `#c64545`

---

## 2. Typography Hierarchy

### Display (Headlines)
- Font: Serif display (`Cormorant Garamond`, `Tiempos Headline`, or `Merriweather`, serif).
- Weight: `400` (Regular) or `500` (Medium). Never bombastic bold (`700+`).
- Tracking: Negative letter spacing (`-0.02em` to `-0.03em`).
- Visual Voice: Thoughtful, literary, editorial, intelligent.

### Interface & Body
- Font: Humanist Sans (`Inter`, `system-ui`, `-apple-system`, `sans-serif`).
- Weight: `400` for body text, `500` or `600` for labels, buttons, and badges.
- Line Height: `1.55` to `1.6` for paragraphs; `1.2` to `1.3` for card titles.

### Code & Technical
- Font: `JetBrains Mono`, `ui-monospace`, `Consolas`.
- Size: `13px` - `14px`.

---

## 3. Layout, Spacing & Positioning Rules

1. **Container Alignment**:
   - Main container: `max-w-6xl` (`1152px` - `1200px`) centered with `mx-auto` and horizontal padding (`px-4 sm:px-6 lg:px-8`).
   - Sticky top navigation at `64px` height with backdrop blur (`bg-[#faf9f5]/90 backdrop-blur-md`).
2. **Spacing Cadence**:
   - Section rhythm: `64px` - `96px` (`py-16` - `py-24`).
   - Card internal padding: `24px` - `32px` (`p-6` - `p-8`).
   - Element gap: `12px` - `16px` (`gap-3` - `gap-4`).
3. **Card & Component Radii**:
   - Buttons & Inputs: `rounded-lg` (`8px`).
   - Cards & Containers: `rounded-xl` (`12px` - `16px`).
   - Hero container: `rounded-2xl` (`16px` - `24px`).
   - Badges & Pills: `rounded-full` (`9999px`).
4. **Elevation & Depth**:
   - Color-block first, hairline borders second, shadows minimal.
   - 1px hairline border (`#e6dfd8`) on cream surfaces.
   - Alternating surfaces (Cream canvas $\rightarrow$ light cream card $\rightarrow$ dark product card) provide depth without cluttered drop shadows.

---

## 4. UI/UX Checklist for Form & Dashboard Applications

- **Form Labels**: Always positioned directly above the input with a subtle icon and clear `*` required marker.
- **Input Focus**: Smooth 2px focus ring in Coral (`#cc785c`) with subtle tint.
- **Badges / Multi-select**: Pill badges that clearly toggle between unselected (neutral cream with hairline border) and selected (solid coral or deep ink with check icon).
- **Progress Bars**: Clear numeric percentage label alongside a smooth colored bar.
- **Card Hierarchy**: Distinct top badges (#1 Best Match with gold/coral accent, #2, #3).
- **Empty States**: Clear messaging, helpful guidance, and one-click action buttons.
