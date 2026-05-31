# Mattiheino.com brand

**Scope (v1, 2026-05-28):** the website. Architected so each section below can
expand to cover newsletter, social infographics, slides and print without
re-doing the foundations. Reserved-for-later sections sit at the end with one
line of intent each, so the slot exists before it's filled.

Source: Claude Design direction C ("Letterhead"), locked tweaks:
- `creamPair`  `#faf5ec` / `#f1e8d7`
- `redPair`    `#9c2b21` / `#7d2018`
- `bandHeight` 149 px
- `bodySize`   17 px
- `measure`    64 ch
- `ornament`   as-designed (paper grain on)
- `expandStyle` inline

These values live in code at `src/styles/global.css` as CSS custom properties.
This document is the *why*; the stylesheet is the *what*.

---

## 1. Essence

A working scientist's blog. Two registers, one voice.

- **Research pieces** – the long-form, careful pieces. Footnoted. Linked to
  sources. Re-read on a cadence; a "relevance confirmed" stamp appears when
  Matti has re-vetted a legacy post.
- **Applied musings** – the light pieces (formerly
  motivationselfmanagement.com). Every applied musing opens with a standing
  disclaimer that it's for a general audience, not a citable scientific text.

The brand has to make the distinction visible without making the applied
register feel second-class. Both are writing. The difference is who they're
written for.

Positioning: behaviour change × complex systems × preparedness. The site
serves readers in that intersection in both English and Finnish.

---

## 2. Colour

Five families. Cream is the page; red is the accent; sky is the band; ink is
the type; rule is the hairline.

| Token            | Hex       | Job                                                         |
|------------------|-----------|-------------------------------------------------------------|
| `--cream`        | `#faf5ec` | Page background. Default surface.                           |
| `--cream-deep`   | `#f1e8d7` | Tonal panels: companion link, newsletter CTA, expand panel. |
| `--red`          | `#9c2b21` | Accent: links, active chip, CTA button, FI marker.          |
| `--red-deep`     | `#7d2018` | Link hover, CTA button hover.                               |
| `--ink`          | `#211d18` | Body type. Wordmark.                                        |
| `--ink-soft`     | `#5b5348` | Secondary type, intro panes, summaries.                     |
| `--ink-faint`    | `#8a7f6d` | Date stamps, section labels, ornaments.                     |
| `--sky`          | `#a6d9ec` | The Letterhead band. Disclaimer pill.                       |
| `--sky-deep`     | `#8ec8e0` | Band lower edge, chip active fallback.                      |
| `--sky-tint`     | `#dfeef5` | Reserved for tonal panels in future surfaces.               |
| `--rule`         | `#e0d6c4` | Hairlines, dividers, default chip border.                   |
| `--rule-soft`    | `#ece4d2` | Reserved (subtler panel border in future surfaces).         |

**Rules of use:**

- Cream is everywhere by default; never put red text on cream (use red only on
  links, active states, or against cream-deep / sky).
- Red is for action and emphasis. If everything is red, nothing is red.
- The sky band is the brand's strongest signature. Reserve it for the
  Letterhead. Don't paint other panels sky-blue.
- The logo (`ajatuspaa.jpg`) has a sky-blue ground that **exactly matches**
  `--sky`. The rectangle dissolves into the band by design. No border, no
  shadow, no `mix-blend-mode`.

---

## 3. Typography

Two faces. Self-hosted via `@fontsource-variable` (no Google Fonts CDN; perf
budget says zero third-party network on first paint).

| Use                                | Face                | Size       | Weight   | Notes                              |
|------------------------------------|---------------------|------------|----------|------------------------------------|
| Body, intro panes, list titles     | Newsreader (serif)  | 17 px      | 400      | Line-height 1.55, measure 64 ch.   |
| Italic for tone shifts             | Newsreader italic   | inherits   | 400      | "Originally published …", labels.  |
| H1                                 | Newsreader          | 70 px      | 500      | LH 1.0, letter-spacing −0.025 em.  |
| Wordmark ("Matti T.J. Heino")     | Newsreader          | 28 px      | 500      | LH 1.0, letter-spacing −0.004 em.  |
| Bylines under wordmark             | Newsreader italic   | 13.5 px    | 400      | EN in red; FI in ink-soft.         |
| Nav, filter labels, metadata       | Inter (sans)        | 11–14 px   | 500/600  | Uppercase for labels (0.18 em ls). |
| Pagination, footer, system UI      | Inter               | 13 px      | 400      | Used sparingly.                    |

**Voice rules** (these are typographic, not editorial – editorial voice lives
in § 11):

- Use the en-dash with spaces ` – ` for parenthetical breaks. Never the em-dash.
- Numbers in body copy: European format. `8 693,19` not `8,693.19`.
- Headings always `text-wrap: balance`.
- Date stamps: `font-variant-numeric: tabular-nums; font-feature-settings: 'lnum'`.
- Reserve uppercase + letter-spacing for system labels (Read · Kind · English ·
  Suomeksi). Never SHOUT in body copy.

---

## 4. The Letterhead

The signature element. A sky band 149 px tall holds the logo, wordmark and
bylines on the left and a single restrained nav link on the right. The band
repeats on every page of the site, including post pages and 404. Without it,
this is just another Astro site; with it, this is the only mattiheino.com.

Structure (left-to-right):

1. `ajatuspaa.jpg` – the head silhouette, 132 px tall, sky ground dissolves
   into `--sky`.
2. Wordmark stack:
   - `Matti T.J. Heino` (Newsreader 28 px / 500)
   - Bylines: `… And Out Come the Systems · Käyttäytymisarkkitehtuuri`
     (italic 13.5 px; EN in red, separator in ink-faint, FI in ink-soft)
3. Padding 28 px vertical / 56 px horizontal.
4. Right side: a single nav link, currently `Browse posts`. Site-section
   navigation (Research pieces / Applied musings) lives below in the filter
   row on the home page, not in the band.

**Why the band stays simple:** the band is the formal handshake at the top of
every page. If we crowd it with nav, we lose the letterhead feel. Filtering
and sub-navigation live one row down.

---

## 5. The diptych (home only)

Home page only. EN + FI intro panes side-by-side, separated by a 1 px rule.
The language toggle in the filter strip *dims* the inactive pane (opacity
0.38) rather than hiding it – both languages stay present on the page, so the
bilingual identity is structurally visible, not a flag-toggle.

Pane content is set in Newsreader 18.4 px (1.08 em) / 1.55. Each pane caps at
the 64 ch measure even when the column is wider.

Intro text is locked – it's the recovered welcome page from the WordPress
export, edited only to fit two columns. EN ends with the NECSI course
mention; FI ends with `Ystävällisesti, / Heinon Matti.`

---

## 6. Filter row

Between the diptych and the writing list. Two hairline-bounded rows:

1. **Read** – language pills (All / English / Suomeksi). Active pill is red
   fill, cream text. Inactive pills are transparent with a rule border.
2. **Kind** – content-type pills (All / Research pieces / Applied musings).
   Same active/inactive treatment.

Below the rows, two paired actions in italic Newsreader 13 px:

- **Browse by topic** (chevron) – opens a fold of topic chips below.
- **Random** (die glyph `⚄`) – picks one entry at random.

These are deliberately quiet. The reader's primary action is to scroll the
list; topic browse and random are secondary. They sit as italic affordances,
not as buttons.

---

## 7. Writing list

The list is the centre of gravity. Each row is a 3-column grid:

| Col 1 (110 px) | Col 2 (flex)                                     | Col 3 (36 px)    |
|----------------|--------------------------------------------------|------------------|
| Date stack:    | Title (Newsreader 22 px / 500) + metadata        | `+` button       |
| `04 Nov`       | `Research piece` or `Applied musing` + FI marker | toggles summary  |
| `2025`         |                                                  |                  |

- Hairline divider between rows (`--rule`).
- Title turns red on hover.
- `+` is a 30 × 30 circle; when open, fills red.
- The summary appears inline beneath the title, Newsreader 17 px / 1.5 in
  `--ink-soft`, capped at the 64 ch measure. (`expandStyle: inline` locked
  after review – the panel variant stood out too much.)

Section label above the list: `writing · newest first` in italic Newsreader
14 px, centred. Quiet, ornamental, removable.

---

## 8. Date treatment

Three states, set by the post's frontmatter:

- **Native post, fresh:** `Published [date]` – `published` and `vetted_on` are
  equal.
- **Legacy post, re-vetted:** `Originally published [pub] · Relevance
  confirmed [vetted_on]` – the two dates differ; `vetting_status: done`.
- **Internal queue only:** no stamp rendered to readers; only the
  `/vetting-queue` internal page shows the published date for triage.

Format: British English, `1 November 2025`. Numerals are tabular.

---

## 9. Applied disclaimer

Top of every applied-musings post, in a sky pill:

> This is an applied musing, written for a general audience – not a scientific
> text. For the rigorous version, see [companion post].

Lives in the layout (`AppliedDisclaimer.astro`), never copy-pasted into post
files. The companion link only renders when the post's frontmatter names a
`rigorous_companion`.

---

## 10. Newsletter CTA

End of every post. Cream-deep panel with a 1 px rule border:

- Kicker (red uppercase 11 px / 0.08 em letter-spacing): `Newsletter`.
- Body (Newsreader 17 px): a single sentence inviting subscription.
- Button (red fill, cream text, 4 px radius): links to
  `https://news.mattiheino.com/`.

Reserved for later: an inline form that posts directly to Listmonk, replacing
the link-through.

---

## 11. Editorial voice

The brand's words, not just its visuals.

- **British English.** Spelling, punctuation, idiom. Never American English
  unless the destination is explicitly American.
- **Direct.** Get to the point. No throat-clearing ("In this post we will
  argue that …").
- **Iconoclastic when warranted.** Steve Rawlings (BBC) and Nassim Nicholas
  Taleb as touchstones. Vivid, persuasive, willing to challenge norms.
- **Rigorous but not jargon-heavy.** Where a technical term earns its place,
  use it; where it doesn't, drop it.
- **Bilingual identity in metadata, not in prose.** Posts are either EN or
  FI – no inline switching. The site shell is bilingual; each post is
  monolingual.
- **No fluff parallelisms.** Avoid "Not only X but also Y", "It's not just …
  it's …", and similar AI-writing tropes (see the Wikipedia *Signs of AI
  writing* list).
- **Numbers in European format** in any FI or EU-bound output. Comma as
  decimal separator, space (or nothing) as thousands separator.

---

## 12. Ornament

A control knob, not a default. The Letterhead component takes an `ornament`
prop with three values:

- `minimal` – no paper grain, no FI byline, no section label. Clean.
- `as-designed` (default) – paper grain at 0.55 opacity, full bylines, italic
  section label above the list.
- `richer` – grain at 0.85, plus a `· · ·` italic glyph under the wordmark.

Production runs `as-designed`. Reserve `minimal` for embedded contexts (e.g.
a slide deck slide that re-uses the band but should feel lighter) and
`richer` for the about page or a one-off seasonal moment.

---

## 13. Footer

Page-foot row, 28 px / 56 px padding, hairline top.

- Left: `© [year] Matti T.J. Heino`
- Middle: `·   ·   ·` ornament (italic Newsreader, ink-faint)
- Right: `RSS · all writing` linking to `/all.xml`

---

## 14. Imagery

Pending broader direction. The site currently uses two image classes:

- **The logo** – `ajatuspaa.jpg`, treated as the wordmark visual, not as a
  photograph. Sits on the band; never embedded in body copy.
- **Per-post infographics** – AI-generated summary infographics colocated
  under `src/content/<collection>/images/<slug>/`. Rendered through Astro's
  `<Image>` with responsive widths.

No photography on the site for now. If photography is added later, treatment
direction lives in § 24 below.

---

# Reserved for later expansion

The site is v1. The sections below are slots; each carries one line of intent
so future-Matti (or future-Claude) knows what the slot is for before filling
it.

## 21. Social-media infographics
- Square 1080 × 1080 + portrait 1080 × 1350.
- Cream page, red accent, Newsreader display, AI-generated infographic body.
- One per published post; orchestrated by the cross-post Worker (Phase 6).

## 22. Newsletter (news.mattiheino.com)
- Listmonk HTML template adapted from the site Letterhead.
- Smaller band (proportional), cream body, red CTA, footer with unsubscribe.

## 23. Slide decks (talks)
- Title slides reuse the Letterhead band on cream.
- Body slides: cream + ink + sparing red. Inter for slide labels, Newsreader
  for slide titles + pull quotes.

## 24. Print (handouts, A4 letterhead, posters)
- Cream paper. Sky band optional (printable on standard CMYK).
- Newsreader for body, Inter for sidebar metadata. Red accent for headings.

## 25. Photography direction
- Not in scope. Site is text + AI-generated diagrams only as of v1.

## 26. Iconography
- Current ornaments (`·`, dice `⚄`, chevron `›`) are the only glyph set.
- A custom mark set is a Phase-6+ decision; don't add icons piecemeal.

## 27. Motion
- Site is near-zero JS by design. The only animation is the chevron rotation
  on the topic-fold open/close.
- Reserve any future motion for state changes (filter active, expand toggle).
  No decorative motion.

---

## Change log

- **2026-05-28** – v1 created. Brand extracted from Letterhead direction C;
  reserved-for-later sections added so the doc can grow without restructure.
