# Handoff: mattiheino.com home page

## Overview

A visual-design pass for the home page of **mattiheino.com**, replacing the
WordPress site at the same domain with a static, fast, archive-friendly
personal blog. This handoff covers the **home page only** — the brief's
Phase 1a gate. Post, applied-musing, and archive pages will follow once a
direction is locked.

## About the design files

The files in this bundle are **design references created in HTML** —
prototypes showing intended look and behaviour, not production code to copy
directly. Your task is to recreate these in the existing **Astro 5 +
TypeScript** codebase the user already has (the local folder you'll work
in), using its established patterns: content collections, `<Image>` from
`astro:assets`, the `src/styles/global.css` tokens-first stylesheet, and the
`src/components/` / `src/layouts/` structure that's already there.

The HTML files are React + Babel single-page artefacts so they can sit on a
design canvas with a live tweaks panel. Ignore that scaffolding — what
matters is the markup, type, colour, spacing, and interaction shown inside
each direction's component.

## Fidelity

**High-fidelity.** All colours, type, spacing and interactions are final
unless flagged below. Recreate pixel-faithfully; don't substitute fonts or
"close-enough" colours.

## Which direction?

Three directions were explored, all sharing the same identity (sky band,
warm cream, deep red, Newsreader + Inter). The user iterated on **Direction
C — Letterhead** through six rounds of comments and that is the build
target. A and B are kept in the bundle for reference; do not implement
them.

- **A · Quiet Reading Room** — single column, hairline rules, minimum
  ornament. _Reference only._
- **B · Marginalia** — running left gutter with date + ordinal, italic
  eyebrow. _Reference only._
- **C · Letterhead** — diptych intro (EN + FI side-by-side, language
  toggle dims the inactive pane), logo dissolving into the sky band beside
  a paired bilingual by-line. **Build this.**

## Final settings (from user)

After iteration the user settled on:

| Setting        | Value     | Where                                |
| -------------- | --------- | ------------------------------------ |
| Band height    | **149px** | Sky band top-of-page                 |
| Expand style   | **Inline** (summary slides in)  | Post-list rows |
| Cream pair     | `#faf5ec` / `#f1e8d7` |                          |
| Red pair       | `#9c2b21` / `#7d2018` |                          |
| Body size      | 17px (1rem)           |                          |
| Measure        | 64ch                  |                          |

The tweaks panel in the HTML is a design exploration tool — **do not port
it to production**. Bake the chosen values directly into tokens.

---

## The home page in detail

### Layout (Direction C — Letterhead)

```
┌────────────────────────────────────────────────────────────┐
│ [BAND, sky #a6d9ec, 149px tall]                            │
│  ┌─logo + brand cluster────────┐         ┌─nav──────────┐  │
│  │ [ajatuspää JPG, h≈132px]   │         │ Browse posts │  │
│  │  Matti T.J. Heino          │         └──────────────┘  │
│  │  ┊… And Out Come the Systems · Käyttäytymisarkkitehtuuri│
│  └─────────────────────────────┘                           │
├────────────────────────────────────────────────────────────┤
│                                                            │
│                Welcome / Tervetuloa  (centred h1)          │
│                                                            │
│  ┌──── EN pane ────┐  │  ┌──── FI pane ────┐               │
│  │ This is a blog… │  │  │ Näiden sivujen… │   (diptych)   │
│  │ For research…   │  │  │ Toivottavasti…  │               │
│  │ N.b. I instruct…│  │  │ Ystävällisesti, │               │
│  └─────────────────┘  │  └─────────────────┘               │
│                                                            │
│  ────────────────────────────────────────────              │
│  Read  [All][English][Suomeksi]                            │
│  Kind  [All][Research pieces][Applied musings]             │
│        › Browse by topic                                   │
│        ⚄ Random                                            │
│  ────────────────────────────────────────────              │
│                                                            │
│     writing · newest first                                 │
│  ┌─date─┬─title + meta────────────────────────┬─[+]─┐      │
│  │10 Nov│ Evidence is in the Past, Risk is …  │  +  │      │
│  │ 2025 │ Research piece                      │     │      │
│  │      │   (inline expanded summary, italic) │     │      │
│  └──────┴─────────────────────────────────────┴─────┘      │
│  …more rows, hairline rules between                        │
│                                                            │
│  © 2026 Matti T.J. Heino · · · RSS · all writing          │
└────────────────────────────────────────────────────────────┘
```

### Components

#### 1. Header band

- Full-width, **149px tall**, background `#a6d9ec` (sky), bottom hairline
  `#8ec8e0` with an additional 1px `rgba(33,29,24,0.08)` shadow rule.
- **Logo**: `assets/ajatuspaa.jpg` (in this bundle, copied from the user's
  existing `src/assets/ajatuspaa.jpg`). Renders at **height = bandHeight − 16px**,
  i.e. ~132px tall at the default band, width auto. **No frame, no
  blend-mode** — the JPG's sky-blue ground exactly matches the band so the
  rectangle dissolves and the white heads read as floating on it.
- **Brand cluster** beside the logo (gap 20px):
  - Wordmark "Matti T.J. Heino" — Newsreader 500, 28px, letter-spacing
    -0.004em, colour `--ink`.
  - By-line beneath (gap 7px), Newsreader italic 13.5px:
    `… And Out Come the Systems` (colour `--red`) · `Käyttäytymisarkkitehtuuri` (colour `--ink-soft`).
    Centre dot separator `--ink-faint`, non-italic, 0.55em margin each side.
- **Right nav**: single link "Browse posts", Inter 500 14px, colour `--ink`,
  hover adds 1px bottom border `--ink`. No "Search" link in the band —
  Browse posts is the only entry point.

#### 2. Hero

- Centred, **70px Newsreader 500**, letter-spacing -0.025em, line-height 1.0:
  `Welcome / Tervetuloa`. The slash is `--ink-faint`, italic, weight 400,
  margins 0.1em.
- No kicker line above (was removed in iteration — the by-line in the band
  carries that role now).
- Margin-bottom 36px before the diptych.

#### 3. Diptych intro

- Two-column grid `1fr 1px 1fr`, gap 48px, with a 1px `--rule` vertical
  separator in the middle.
- **Each pane**: Newsreader serif, **1.08em** (~18.4px), line-height 1.55,
  max-width var(`--measure`) (64ch default).
- Pane label: Inter 600 11px uppercase, letter-spacing 0.18em,
  colour `--ink-faint`, margin-bottom 14px. Reads "English" / "Suomeksi".
- Three paragraphs each, gap 0.85em.
  - English: lead → contact-line (Scholar / email / LinkedIn) → "Nota bene"
    NECSI line. Links: colour `--ink`, underline `--red` 1px,
    underline-offset 3px. Hover: colour `--red`.
  - Finnish: lead → "Toivottavasti löydät jotain kiinnostavaa." →
    "Ystävällisesti, / Heinon Matti." (br between).
- When the language pills are set to EN or FI, the inactive pane gets
  `opacity: 0.38` with a `transition: opacity .2s`. The All state shows
  both at full opacity.

#### 4. Filter row

- Sits between two hairline rules (`--rule`, 1px, top + bottom). Max-width
  720px, padding 22px 0, centred items, gap 14px.
- **Row 1 — Read**: label "Read" (Inter 500 11px uppercase, letter-spacing
  0.14em, colour `--ink-faint`, min-width 48px, right-aligned), then chips
  All / English / Suomeksi.
- **Row 2 — Kind**: label "Kind", chips All / Research pieces / Applied musings.
- **Chip**: Inter 500 13.5px, 6px 16px padding, border-radius 999px, border
  `--rule`, transparent bg, colour `--ink-soft`. Active state: bg `--red`,
  colour `--cream`, border `--red`.
- **Browse by topic** (below): chevron + text, Newsreader italic 13px,
  `--ink-soft`. Click expands a wrapping row of topic chips (transparent,
  border `--rule`, same scale as a small pill).
- **Random** (below Browse by topic): Newsreader italic 13px, `--ink-soft`,
  preceded by a small ⚄ die glyph (16px, `--ink-faint`, non-italic). Hover
  recolours both text and the 1px underline to `--red`.
  **Production behaviour**: hit a server route that picks a random live
  entry from the content collections and 302s to its `cleanSlug` URL. In
  the mockup it just expands a random row.

#### 5. Writing list

- Max-width 860px, centred. Section label above: "writing · newest first",
  Newsreader italic 0.88em, `--ink-faint`, letter-spacing 0.05em,
  margin-bottom 18px.
- **Row** grid: `110px 1fr 36px`, gap 24px, padding 22px 0, bottom hairline
  `--rule`.
  - **Date column**: day + month abbrev (e.g. "10 Nov") Newsreader italic
    14px, `--ink-soft`, tabular-nums. Year below as a span with
    `display: block`, normal weight, 18px, colour `--ink`, lining figures,
    margin-top 2px.
  - **Title column**: title is Newsreader 500 1.32em, letter-spacing
    -0.012em, line-height 1.22, colour `--ink`, hover `--red`, text-wrap
    balance. Beneath: meta line, Inter 500 12px uppercase, letter-spacing
    0.06em, `--ink-faint`. Format: `Research piece` or `Applied musing`,
    optionally followed by `·` + `Suomeksi` in `--red`.
  - **Toggle**: 30×30 circle, 1px border `--rule`, bg `--cream`,
    `+` / `–` glyph 16px `--ink-soft`. Open state: bg `--red`, colour
    `--cream`, border `--red`. **aria-expanded** + label "Show summary" /
    "Hide summary".
- **Inline expand** (the chosen default): when open, a `<p>` slides in
  below in grid column `2 / 4`, margin-top 12px, max-width var(--measure),
  Newsreader 1em, line-height 1.5, colour `--ink-soft`. The summary text
  is the post's `description` field from the content collection.

#### 6. Footer

- Max-width 1080px, padding 28px 56px 40px, top hairline `--rule`,
  flex space-between, font 13px `--ink-faint`.
- Left: "© 2026 Matti T.J. Heino"
- Middle: italic ornament `· · ·` `--ink-faint`
- Right: "RSS · all writing" — colour `--ink-soft`, 1px bottom border
  `--rule`.

### Interactions & behaviour

- **Language toggle** (Read pills) — updates state, dims inactive diptych
  pane, filters the writing list. Default: "All".
- **Kind toggle** (Kind pills) — filters the writing list to research /
  applied / both. Default: "All". Composes AND with Language.
- **Topic chips** — clicking a topic should filter the list to posts whose
  `tags` include that slug (out of scope for the mockup; collapsed by
  default).
- **Row toggle** — opens/closes the inline summary; multiple rows can be
  open simultaneously. One row open by default on first paint for demo
  purposes — **in production, all rows start collapsed**.
- **Random** — see §4. Server-route + 302 redirect.
- **Browse posts** (band nav) — single entry point to the search / browse
  view (Phase 1b scope).

### Animations

- Diptych pane opacity fade: 200ms ease (CSS transition on `opacity`).
- Row toggle: no animation in the mockup; if you want one, use a 150ms
  ease height/opacity for the summary `<p>`. Keep it subtle.
- No scroll-driven effects, no parallax.

### State management

For a single Astro page, state is minimal:
- `lang: 'all' | 'en' | 'fi'`
- `kind: 'all' | 'research' | 'applied'`
- `topicOpen: boolean`
- `open: Record<index, boolean>`

The user's brief is firm that the home is **largely static + minimal
client JS**. Use Astro islands (`client:load` only where needed) on the
filter cluster and the row-toggle island. Posts come from the Astro
content collection helper at `src/lib/collections.ts`
(`allLive()`) — sort by `published` desc.

### Filters and the URL

Mirror filter state in the URL query string so language + kind selections
are shareable and survive reload: `?lang=fi&kind=research`. Default
omits the params. This wasn't shown in the mockup but matches the brief's
"archive-friendly" disposition.

---

## Design tokens

CSS custom properties — drop these into `src/styles/global.css` under the
existing tokens block.

```css
:root {
  /* Paper */
  --cream:       #faf5ec;   /* page background */
  --cream-deep:  #f1e8d7;   /* hairlines, expand-panel surface */

  /* Ink */
  --ink:         #211d18;   /* primary text */
  --ink-soft:    #5b5348;   /* secondary text */
  --ink-faint:   #8a7f6d;   /* tertiary text, ornaments */

  /* Accent */
  --red:         #9c2b21;   /* links, active pills */
  --red-deep:    #7d2018;   /* hover, deeper red */

  /* Sky (header band) */
  --sky:         #a6d9ec;   /* exact match to ajatuspää JPG ground */
  --sky-deep:    #8ec8e0;   /* band bottom hairline */
  --sky-tint:    #dfeef5;   /* unused on home, reserved for post pages */

  /* Rules */
  --rule:        #e0d6c4;
  --rule-soft:   #ece4d2;

  /* Type */
  --measure:     64ch;
  --body-size:   17px;
}
```

### Typography

- **Newsreader** (Google Fonts, self-host per brief): weights 400 + 500,
  italic 400 + 500. Variable axes 6..72 opsz. Used for: headings, hero,
  intro panes, post titles, post summaries, byline, all serif text.
- **Inter** (Google Fonts, self-host): weights 400 / 500 / 600. Used for:
  nav, pill chips, meta labels, "Read" / "Kind" labels, footer.

Type scale (use these exact values; only the slider in the mockup was
parametric):

| Element              | Family     | Size         | Weight | Misc                              |
| -------------------- | ---------- | ------------ | ------ | --------------------------------- |
| Hero h1              | Newsreader | 70px / 1.0   | 500    | letter-spacing -0.025em           |
| Diptych body         | Newsreader | 18.4px / 1.55| 400    | max-width 64ch                    |
| Diptych label        | Inter      | 11px         | 600    | uppercase, letter-spacing 0.18em  |
| Wordmark             | Newsreader | 28px         | 500    | letter-spacing -0.004em           |
| Byline               | Newsreader italic | 13.5px | 400 | letter-spacing 0.005em            |
| Nav                  | Inter      | 14px         | 500    |                                   |
| Section label        | Newsreader italic | 14.96px (0.88em) | 400 | letter-spacing 0.05em      |
| Post title           | Newsreader | 22.44px (1.32em) | 500 | letter-spacing -0.012em, balance  |
| Post date day/month  | Newsreader italic | 14px  | 400 | tabular-nums                      |
| Post date year       | Newsreader | 18px         | 400    | lining figures                    |
| Post meta            | Inter      | 12px         | 500    | uppercase, letter-spacing 0.06em  |
| Summary (inline)     | Newsreader | 17px / 1.5   | 400    | colour `--ink-soft`               |
| Chip                 | Inter      | 13.5px       | 500    |                                   |
| Filter label         | Inter      | 11px         | 500    | uppercase, letter-spacing 0.14em  |
| Footer               | Inter      | 13px         | 400    | colour `--ink-faint`              |
| Random / Browse-by-topic | Newsreader italic | 13px | 400 |                                |

### Spacing & layout

- Page background `--cream`.
- Header band: padding `28px 56px`, min-height 149px, bottom border 1px.
- Main container: max-width 1080px, padding `56px 56px 96px`, centred.
- Diptych: grid `1fr 1px 1fr`, gap 48px, margin-top 8px.
- Filter row: max-width 720px, padding `22px 0`, top + bottom hairline.
- Writing list: max-width 860px, margin-top 56px, row padding `22px 0`,
  row grid `110px 1fr 36px` gap 24px.
- Footer: max-width 1080px, padding `28px 56px 40px`, top hairline.

### Border radii / shadows

- Chips and toggle circle: `border-radius: 999px` (pill / full circle).
- Toggle button: 30×30, 1px border.
- No drop shadows anywhere on the home. The earlier "panel" expand variant
  used a soft `2px 2px 0 var(--rule-soft)` box-shadow but was deprecated in
  favour of inline expand.

---

## Assets

- **`assets/ajatuspaa.jpg`** — the existing logo, copied verbatim from the
  user's `mattiheino-site/src/assets/ajatuspaa.jpg`. Two stylised heads on
  a sky-blue ground. Move into the Astro `src/assets/` folder and load via
  `import logo from '../assets/ajatuspaa.jpg'` + `<Image>` so it's
  fingerprinted and width-served. The natural sky-blue ground in the JPG
  **exactly matches** `--sky` so it visually dissolves into the band — do
  not apply CSS blend modes, do not crop, do not regenerate as SVG.
- No other images on the home page.
- No icon set used; the chevron and die glyphs are Unicode (`›` `⚄`) and
  the diptych separator is a CSS 1px column.

---

## Files in this bundle

| File                       | What it is                                       |
| -------------------------- | ------------------------------------------------ |
| `Home.html`                | Entry point — loads React + Babel and the JSX    |
| `app.jsx`                  | Design-canvas host + tweaks-panel wiring         |
| `shared.jsx`               | Post data, copy, helpers, tokenStyle()           |
| **`home-letterhead.jsx`**  | **Direction C — the build target**               |
| `home-quiet.jsx`           | Direction A — reference only                     |
| `home-marginalia.jsx`      | Direction B — reference only                     |
| `design-canvas.jsx`        | Pan/zoom canvas (design tool — do not port)      |
| `tweaks-panel.jsx`         | Tweaks panel (design tool — do not port)         |
| `assets/ajatuspaa.jpg`     | Logo                                             |

Open `Home.html` locally to see the live prototype. The Letterhead
artboard is the third / rightmost.

## What's not in this handoff (and is therefore next)

- **Post page** layout (Newsreader body, footnotes, figure handling).
- **Applied-musing** top-of-page block (per brief, "Disclaimers and
  caveats" warning panel).
- **Archive** view.
- **Search / Browse posts** view that "Browse posts" points to.
- **Topic / tag** filter result view.
- **Random** server route.
- **Light/dark mode** if any (not specified in the brief; assume light only
  for now).

Phase order in the brief suggests: home → post → applied musing → archive →
search. Confirm with the user before starting the next page.

## Implementation notes

- The brief is firm about **British English** + **en-dashes only**. Audit
  copy strings; the mockup occasionally used em-dashes in code comments
  which don't ship.
- All `<a>` in the writing list should point to `cleanSlug(item)` URLs from
  the existing `src/lib/slug.ts` helper.
- The `Browse posts` link should route to `/browse` (or wherever search
  lives — confirm with user).
- Use Astro's `<Image>` for the logo so it's served as both AVIF and WebP
  at the correct intrinsic size.
- Self-host Newsreader + Inter (Fontsource or equivalent) — do **not**
  hot-link Google Fonts in production. The HTML mockup hot-links for
  convenience; the brief explicitly calls this out.
- Posts come from existing content collections; reuse `allLive()` from
  `src/lib/collections.ts`. Sort by `published` descending.
- `description` field on each entry is what shows in the inline expand;
  ensure all entries have one (the brief notes this as part of Phase 1a).
