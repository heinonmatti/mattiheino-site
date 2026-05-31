# mattiheino.com – Design brief for Claude Design

## What this is

A rebuild of Matti T.J. Heino's personal blog at **mattiheino.com**, moving off WordPress.com to a static site (Astro + Cloudflare Pages). The structure and content scaffolding are done; this brief asks for a **visual direction** to apply to it. Produce **2–3 distinct directions** for the home page first. Matti picks one. The winner is then extended across the post / applied-musing / listing pages.

## The author and the blog

Matti T.J. Heino – complex-systems behavioural scientist (University of Tampere, University of Heidelberg, World Health Network). Writes on **complex systems, behaviour change, civil preparedness, health and well-being**.

- English blog name: **"… And Out Come the Systems"** (a deliberate Rancid play, kept).
- Finnish parallel brand: **Käyttäytymisarkkitehtuuri** ("behavioural architecture").
- Bilingual content, roughly 60/40 EN/FI.

**It is a blog, not a journal.** Not "research-grade", not "citable", not academic in framing. Two registers exist on the site:

- **Research pieces** – considered, longer essays on complex systems, behaviour change, preparedness.
- **Applied musings** – lighter, practical pieces for a general audience.

Both are writing. Neither claims to be a scientific article.

## Visual identity to inherit

A sibling site is already live at **https://news.mattiheino.com** (the newsletter signup). Inherit its identity – the new site is the same brand:

- **Palette**
  - Warm cream page: `#faf5ec` (deeper: `#f1e8d7`)
  - Deep red accent: `#9c2b21` (deeper hover: `#7d2018`)
  - Sky-blue header band: `#a6d9ec` (matches the logo's ground colour so the logo dissolves into the band)
  - Ink: `#211d18`; soft ink: `#5b5348`; rules/dividers: `#e0d6c4`
- **Type pairing**: **Newsreader** (serif – headings + long-form body, italic-capable) + **Inter** (sans – UI and meta). Self-host both (no Google Fonts CDN at runtime).
- **Logo**: **ajatuspää** ("thought-head") – two line-drawn heads with cityscapes inside, on a sky-blue ground. JPG at `C:\Users\qn353\Documents\git-projects\mattiheino-newsletter\assets\ajatuspaa.jpg` and `C:\Users\qn353\Documents\git-projects\mattiheino-site\src\assets\ajatuspaa.jpg`. 668 × 288.

Feel: thoughtful, considered, faintly old-paper, not corporate, not generic-Medium-blog.

## What to design (in priority order)

### 1. Home / welcome page

- **Header**: ajatuspää logo + "Matti T.J. Heino" wordmark on the sky-blue band. Nav (right-aligned on desktop): **Research pieces · Applied musings · Archive · Search**.
- **Hero**: small italic serif kicker "… And Out Come the Systems"; large serif H1 "**Welcome / Tervetuloa**"; then a bilingual intro paragraph **that swaps with the language toggle**.
  - English intro (verbatim Matti voice):
    > This is a blog about behaviour change science and complex systems in preparedness, health and well-being. For research articles, see my Google Scholar profile. To email me about anything, write to matti.tj.heino @ this domain (i.e. mattiheino.com). Find me on LinkedIn. *Nota bene:* I instruct an online course for the New England Complex Systems Institute, and am happy to answer questions. Do reach out.
  - Finnish intro (verbatim):
    > Näiden sivujen tarkoituksena on lisätä tietoa inhimilliseen toimintaan vaikuttamisesta yhteisen hyvinvoinnin lisäämiseksi. Tavoitteena on löytää näkökulmia niin omaan kuin muidenkin käyttäytymiseen. Toivottavasti löydät jotain kiinnostavaa. Ystävällisesti, Heinon Matti.
- **Filter row**: three pill buttons **All / English / Suomeksi** (active = deep red); below them a collapsed `<details>` summary **"Browse by topic"** that, when expanded, reveals topic chips (default state: collapsed – the topic chips must not visibly clutter the page on load).
- **Writing list** (both registers mixed, newest first). Each row:
  - title (serif, link),
  - FI badge if Finnish,
  - date (small, soft ink),
  - a `+` control on the right that expands a one-paragraph **summary** below the row. Default collapsed.

### 2. Research piece (long-form blog post)

- Header: title (serif H1, balanced), then a **date stamp** in one of two voices:
  - "Published 10 November 2025" – for natively dated posts.
  - "Originally published 15 September 2020 · Relevance confirmed 24 May 2026" – for legacy posts the author has re-read.
- Body: serif, comfortable measure (~68ch), generous line-height, balanced headings.
- Optional **cross-link** to a companion in the other register: "There's an applied musing on this – here."
- Footer **CTA**: subscribe at news.mattiheino.com (link-through, no embedded form on this site).

### 3. Applied musing

- A standing top-of-post note (compact, sky-tinted): **"An applied musing – written for a general audience."** Optionally followed by a longer-companion link.
- Same body and footer pattern as Research piece.

### 4. Section index pages (`/posts/`, `/applied-musings/`) and the **Archive** (all posts grouped by year).

### 5. **Search**, **404**, and a **noindex internal vetting-queue** (utility pages – clean and minimal, no special design effort needed).

## Hard constraints

- **British English** (no Americanisms). En-dashes (` – `) with spaces. Never em-dashes (`—`).
- **No academic framing**. Avoid "research-grade", "citable", "scientific text", "rigorous treatment", "the full treatment", "the rigorous version".
- **Bilingual on one canonical site** (no `/en/` or `/fi/` URL trees). Language is a per-item tag and a UI filter.
- **Performance**: Lighthouse 95+ on Performance, Accessibility, Best Practices, SEO. Near-zero JS by default; small interaction islands acceptable for the language toggle, topic filter, and per-row expand.
- **No analytics that needs a cookie banner**. Cloudflare Web Analytics (cookieless).
- **No dark-mode-first**. Warm cream is the brand. Optional dark mode is low priority.
- **Comfortable reading**, not bento-card-grid. Posts are typographic, left-aligned, balanced headings, no rounded card chrome around post bodies.

## Deliverable formats

Preferred, in order:

1. **HTML + CSS** for each screen – I'll transcribe to Astro components/layouts directly.
2. **Figma / Penpot / PDF / PPTX** visual direction with explicit type, colour, and spacing specs.

If Claude Design can ingest a codebase, point it at:

- `C:\Users\qn353\Documents\git-projects\mattiheino-newsletter\` – the production-deployed signup site (canonical source for palette, font pairing, logo usage).
- `C:\Users\qn353\Documents\git-projects\mattiheino-site\` – the in-progress new site (the placeholder skin to redesign). Key files:
  - `src/styles/global.css` – current design tokens.
  - `src/layouts/Base.astro` – header / nav / footer shell.
  - `src/pages/index.astro` – home with the filter island.
  - `src/layouts/Post.astro` – post layout (with date-stamp logic + companion link + applied disclaimer).
  - `src/components/AppliedDisclaimer.astro`, `DateStamp.astro`, `NewsletterCTA.astro`, `PostList.astro`.

The current placeholder built output is in `mattiheino-site/dist/` (after `npm run build`) – static HTML for each route, viewable directly. Useful as a reference for what's there now and what needs replacing.

## Things to push back on if asked

- Don't propose a generic personal-blog-on-Medium look. The identity has more flavour than that.
- Don't centre-align long body text. Left-align with a comfortable measure (~60–70ch).
- Don't wrap post bodies in rounded card containers. Posts are typographic.
- Don't optimise the home page around social-share thumbnails or a "subscribe" modal.
- Don't introduce icons-everywhere. Restraint over decoration.

## Reference reading (Matti's voice as a writer)

Three recent English pieces to skim for tone:

- *Evidence is in the Past, Risk is in the Future: On Tail Events and Foresight* (Nov 2025)
- *From Fruit Salad to Baked Bread: Understanding Complex Systems for Behaviour Change* (May 2025)
- *Affordance Mapping to Manage Complex Systems: Planning a Children's Party* (Aug 2024)

All live at https://mattiheino.com until DNS cutover.
