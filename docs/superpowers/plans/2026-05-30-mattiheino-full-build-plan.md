# mattiheino.com full build implementation plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Take mattiheino-site from "Letterhead skeleton with 8 placeholders" to "fully populated bilingual site with 104 WordPress posts visible, 12 motivationselfmanagement.com posts in a private draft vetting queue, RSS subscriber continuity preserved, motivationselfmanagement.com redirects in place, deployed on Cloudflare Pages at mattiheino.com".

**Architecture:** Astro 6.3 content collections + Cloudflare Pages + self-hosted fonts + Pagefind search. Two Python ingest pipelines (`import_wp.py`, `import_msm.py`) produce Markdown files + colocated images in `src/content/`. Visibility gated by `draft` field; MSM posts always import as `draft: true`. RSS continuity via a new `wp_guid` frontmatter field. MSM redirect map auto-rebuilt from frontmatter so per-URL rules append themselves as posts go live.

**Tech Stack:** Astro 6.3.6 · @fontsource-variable · Pagefind · @astrojs/rss · Cloudflare Pages · Cloudflare Web Analytics · Python 3.14 (xml.etree + markdownify + requests) · pytest · GitHub.

**Spec:** `docs/superpowers/specs/2026-05-30-mattiheino-full-build-design.md`. Refer to it whenever this plan says "per the spec".

**Conventions:**
- Each phase ends with a natural pause-and-review checkpoint. Resume from any phase boundary in a later session.
- Commits use Conventional Commits prefix (`feat:`, `fix:`, `chore:`, `docs:`).
- All file paths are relative to `mattiheino-site/` unless noted.
- Run commands from `mattiheino-site/` unless noted.

---

## Phase 1b — Deploy skeleton to `new.mattiheino.com`

Ships the current Letterhead skeleton (with placeholder posts) to a real URL so the deploy pipeline is verified before content lands. Ends with Lighthouse 95+ on three pages.

### Task 1: Initial commit

**Files:**
- Create: `.gitignore`
- Touch: all current source files (will be added en bloc as initial commit)

- [ ] **Step 1: Create `.gitignore`**

```
# Node
node_modules/

# Astro build
dist/
.astro/

# Migration sources and intermediates (kept local, never pushed)
migration/source/
migration/source/media/
migration/cache/

# Editor / OS
.DS_Store
*.log
.vscode/
.idea/

# Env
.env
.env.*
!.env.example

# Pagefind output
public/pagefind/
```

- [ ] **Step 2: Initialise git, set default branch to `main`**

Run:
```bash
cd C:/Users/qn353/Documents/git-projects/mattiheino-site
git init -b main
git config user.email "matti.tj.heino@gmail.com"
git config user.name "Matti Heino"
```

Expected: `Initialized empty Git repository in ...`

- [ ] **Step 3: Stage and verify what would be committed**

Run:
```bash
git add -A
git status --short | wc -l
git ls-files --cached | head -30
```

Expected: a few dozen files staged; no `node_modules/`, no `dist/`, no `migration/source/`.

- [ ] **Step 4: Initial commit**

```bash
git commit -m "feat: initial scaffold — Astro 6.3 + Letterhead direction C + brand doc + build spec

Includes:
- src/ content collections, layouts, components, pages
- BRAND.md (Letterhead direction C, locked)
- docs/superpowers/specs/ design spec for full build
- placeholder posts (8) used to validate layouts
- @fontsource-variable Newsreader + Inter self-hosted
- Pagefind postbuild + RSS + sitemap

Brand source: Claude Design direction C (Letterhead).
See BRAND.md and the design spec for context."
```

- [ ] **Step 5: Verify the commit**

Run:
```bash
git log --oneline -1
git show --stat HEAD | head -30
```

Expected: one commit on `main`, ~50-60 files added.

### Task 2: Push to GitHub

**Files:** none locally; creates remote.

- [ ] **Step 1: Create the GitHub repo (manual, via `gh` CLI)**

Run:
```bash
gh repo create heinonmatti/mattiheino-site --public --source=. --remote=origin --description "mattiheino.com Astro rebuild"
```

Expected: `https://github.com/heinonmatti/mattiheino-site` created; `origin` remote added locally.

If `gh` is not authenticated, run `gh auth login` first.

- [ ] **Step 2: Push `main`**

Run:
```bash
git push -u origin main
```

Expected: push succeeds; `main` tracking `origin/main`.

- [ ] **Step 3: Verify on github.com**

Open `https://github.com/heinonmatti/mattiheino-site` in browser. Confirm:
- README appears (or note that there is no README — that is fine for now)
- BRAND.md visible and renders
- `docs/superpowers/specs/2026-05-30-mattiheino-full-build-design.md` visible

- [ ] **Step 4: Commit message tidy (no-op if first push was clean)**

Skip if Step 2 succeeded cleanly. Otherwise resolve.

### Task 3: Set up Cloudflare Pages project

**Files:** none in repo; Cloudflare-side configuration.

- [ ] **Step 1: Create Pages project (Cloudflare dashboard)**

Manual:
1. Cloudflare dashboard → Workers & Pages → Create application → Pages → Connect to Git.
2. Select GitHub → `heinonmatti/mattiheino-site` → Begin setup.
3. Project name: `mattiheino-site`
4. Production branch: `main`
5. Framework preset: Astro (autoselect)
6. Build command: `npm run build`
7. Build output: `dist`
8. Environment variables: none yet.
9. Save and Deploy.

Expected: first deploy starts immediately; succeeds in ~2 min; produces `https://mattiheino-site.pages.dev/`.

- [ ] **Step 2: Add custom domain `new.mattiheino.com`**

Manual:
1. Pages project → Custom domains → Set up a custom domain → `new.mattiheino.com` → Begin DNS auto-config.
2. Confirm CNAME record creation in Cloudflare DNS.

Expected: domain active in 1-3 min; `https://new.mattiheino.com/` reachable.

- [ ] **Step 3: Smoke-test deploy**

Run:
```bash
curl -sI https://new.mattiheino.com/ | head -8
curl -sI https://new.mattiheino.com/posts/tail-events/ | head -8
curl -sI https://new.mattiheino.com/applied-musings/antihauras/ | head -8
```

Expected: each returns `HTTP/2 200` and `cf-ray:` header.

### Task 4: Lighthouse audit on three pages

**Files:** none if all green; possible fixes in `src/styles/global.css`, `src/components/Letterhead.astro`, `src/layouts/Base.astro` if not.

- [ ] **Step 1: Run Lighthouse against three URLs**

Run (from any machine with Chrome installed):
```bash
npx lighthouse https://new.mattiheino.com/ --only-categories=performance,accessibility,best-practices,seo --output=json --output-path=/tmp/lh-home.json --quiet
npx lighthouse https://new.mattiheino.com/posts/tail-events/ --only-categories=performance,accessibility,best-practices,seo --output=json --output-path=/tmp/lh-post.json --quiet
npx lighthouse https://new.mattiheino.com/applied-musings/antihauras/ --only-categories=performance,accessibility,best-practices,seo --output=json --output-path=/tmp/lh-applied.json --quiet
```

Extract scores:
```bash
for f in /tmp/lh-home.json /tmp/lh-post.json /tmp/lh-applied.json; do
  echo "=== $f ==="
  jq '.categories | to_entries | map({(.key): (.value.score * 100)})' "$f"
done
```

Expected: all four categories ≥ 95 on all three pages.

- [ ] **Step 2: If any score < 95, list the failing audits**

Run:
```bash
jq '.audits | to_entries | map(select(.value.score != null and .value.score < 1)) | map({id: .key, score: .value.score, title: .value.title})' /tmp/lh-home.json
```

Note them; pick the cheapest 1-3 fixes that move the score over 95.

- [ ] **Step 3: Apply fixes (only if Step 2 surfaced any)**

Common Astro fixes:
- Add `<meta name="description">` if missing.
- Add `<html lang="en">` (or per-page lang).
- Ensure all `<img>` have `alt` (decorative images need `alt=""`, not missing alt).
- Defer non-critical JS via `is:inline defer`.

- [ ] **Step 4: Commit fixes (if Step 3 produced changes)**

```bash
git add -A
git commit -m "fix(seo/a11y): address Lighthouse audit findings before content import"
git push
```

- [ ] **Step 5: Re-run Lighthouse, confirm all green**

Repeat Step 1. All three pages must hit ≥ 95 on all four categories before proceeding.

**Phase 1b checkpoint.** Deploy pipeline verified. Pause here is safe. Resume at Task 5 when ready.

---

## Phase 2 — WordPress content import

Imports the 104 published posts + 17 drafts + 3 of the 9 pages from `migration/source/andoutcomethesystemskyttytymisarkkitehtuuri.WordPress.2026-05-20.xml`, using the local media tar as the authoritative image cache.

### Task 5: Add `wp_guid` and `msm_slug` to content schema

**Files:**
- Modify: `src/content.config.ts`

- [ ] **Step 1: Read the current schema**

Run:
```bash
cat src/content.config.ts
```

Note the `baseSchema` block.

- [ ] **Step 2: Add the two new optional string fields**

Open `src/content.config.ts`. In `baseSchema`, add the two fields (alphabetical or grouped with other migration fields):

```ts
wp_guid: z.string().optional(),
msm_slug: z.string().optional(),
```

- [ ] **Step 3: Verify the schema parses**

Run:
```bash
npm run build 2>&1 | tail -20
```

Expected: build completes without Zod errors. Existing placeholder content still validates.

- [ ] **Step 4: Commit**

```bash
git add src/content.config.ts
git commit -m "feat(schema): add wp_guid + msm_slug optional fields

wp_guid carries the original WordPress <guid> for RSS subscriber continuity
at Phase 3 DNS cutover. msm_slug carries the original
motivationselfmanagement.com slug so per-URL 301 rules can be appended
lazily as MSM posts are vetted and published."
git push
```

### Task 6: Wire RSS feeds to emit `wp_guid`

**Files:**
- Modify: `src/pages/posts.xml.ts`, `src/pages/applied-musings.xml.ts`, `src/pages/all.xml.ts`

The default Astro RSS helper sets `<guid>` to the canonical URL. Override it to use `data.wp_guid` when present.

- [ ] **Step 1: Read the current pattern**

Run:
```bash
cat src/pages/posts.xml.ts
```

- [ ] **Step 2: Add a `customData` per item that includes the wp_guid GUID override**

The `@astrojs/rss` helper takes `items[].customData` and `items[].link`. For the `<guid>` element specifically, use `items[].link` as fallback and use a custom item-level XML override when `wp_guid` is set.

Edit `src/pages/posts.xml.ts` to:

```ts
import rss from '@astrojs/rss';
import { getCollection } from 'astro:content';
import { cleanSlug } from '../lib/slug';
import type { APIContext } from 'astro';

export async function GET(context: APIContext) {
  const posts = (await getCollection('posts', ({ data }) => !data.draft)).sort(
    (a, b) => b.data.published.getTime() - a.data.published.getTime(),
  );
  return rss({
    title: '… And Out Come the Systems – Writing',
    description: 'Complex systems, health and well-being amidst uncertainty.',
    site: context.site!,
    items: posts.map((e) => {
      const link = `/posts/${cleanSlug(e.id)}/`;
      const guid = e.data.wp_guid ?? new URL(link, context.site!).toString();
      return {
        title: e.data.title,
        description: e.data.description,
        pubDate: e.data.published,
        link,
        // Override <guid> to preserve WP continuity. isPermaLink=false because
        // wp_guid is an opaque identifier from the WP <guid> field, not the
        // post's permalink.
        customData: `<guid isPermaLink="false">${guid}</guid>`,
      };
    }),
  });
}
```

Apply the same pattern (with the right link path) to `applied-musings.xml.ts` and `all.xml.ts`.

- [ ] **Step 3: Verify build still succeeds**

Run:
```bash
npm run build 2>&1 | tail -20
```

Expected: build succeeds; `dist/posts.xml`, `dist/applied-musings.xml`, `dist/all.xml` regenerated.

- [ ] **Step 4: Spot-check a generated feed**

Run:
```bash
grep -A1 '<guid' dist/posts.xml | head -10
```

Expected: every published post has a `<guid isPermaLink="false">...</guid>` element. For placeholder posts (no `wp_guid` yet), the GUID is the canonical URL. After Task 14 (real import), real `wp:guid` values appear.

- [ ] **Step 5: Commit**

```bash
git add src/pages/posts.xml.ts src/pages/applied-musings.xml.ts src/pages/all.xml.ts
git commit -m "feat(rss): emit wp_guid as <guid isPermaLink=\"false\"> for subscriber continuity

Falls back to canonical URL when wp_guid is unset (placeholder + native posts).
Load-bearing for Phase 3 DNS cutover: prevents existing WP RSS subscribers from
re-receiving the entire archive."
git push
```

### Task 7: Initialise the migration Python package

**Files:**
- Create: `migration/pyproject.toml`
- Create: `migration/lib/__init__.py`
- Create: `migration/tests/__init__.py`
- Create: `migration/tests/conftest.py`
- Create: `migration/.python-version` (`3.14`)

- [ ] **Step 1: Write `migration/pyproject.toml`**

```toml
[project]
name = "mattiheino-migration"
version = "0.0.1"
description = "One-off WordPress + Wayback ingest pipelines for mattiheino-site."
requires-python = ">=3.12"
dependencies = [
  "markdownify>=0.13",
  "requests>=2.31",
  "lxml>=5.1",
  "python-slugify>=8.0",
]

[project.optional-dependencies]
dev = [
  "pytest>=8.0",
  "pytest-mock>=3.12",
]

[build-system]
requires = ["setuptools>=68"]
build-backend = "setuptools.build_meta"

[tool.setuptools.packages.find]
where = ["."]
include = ["lib*", "tests*"]

[tool.pytest.ini_options]
testpaths = ["tests"]
python_files = ["test_*.py"]
```

- [ ] **Step 2: Empty package markers + conftest**

`migration/lib/__init__.py`:
```python
# Migration helpers package.
```

`migration/tests/__init__.py`: (empty)

`migration/tests/conftest.py`:
```python
"""Pytest fixtures shared across migration tests."""
from pathlib import Path
import pytest


@pytest.fixture(scope="session")
def fixtures_dir() -> Path:
    return Path(__file__).parent / "fixtures"
```

`migration/.python-version`:
```
3.14
```

- [ ] **Step 3: Install dependencies in a venv**

Run:
```bash
cd migration
python -m venv .venv
.venv\Scripts\activate
pip install -e ".[dev]"
```

Expected: editable install succeeds; pytest available.

- [ ] **Step 4: Confirm test runner discovers the empty test suite**

Run:
```bash
cd migration
.venv\Scripts\activate
pytest -q
```

Expected: `no tests ran in 0.NNs`. No errors.

- [ ] **Step 5: Add `.venv` and `__pycache__` to `.gitignore`**

Append to the repo-root `.gitignore`:
```
# Python
migration/.venv/
migration/**/__pycache__/
migration/**/*.pyc
migration/.pytest_cache/
```

- [ ] **Step 6: Commit**

```bash
cd C:/Users/qn353/Documents/git-projects/mattiheino-site
git add migration/pyproject.toml migration/lib/__init__.py migration/tests/__init__.py migration/tests/conftest.py migration/.python-version .gitignore
git commit -m "chore(migration): initialise Python package + pytest harness

markdownify + lxml + requests + python-slugify for the WP + Wayback ingest
pipelines. Editable install via 'pip install -e migration/[dev]'."
git push
```

### Task 8: Untar the media archive

**Files:**
- Create on disk (gitignored): `migration/source/media/` (~262 files)

- [ ] **Step 1: Untar in place**

Run:
```bash
cd migration/source
mkdir -p media
tar -xf media-export-95487425-from-0-to-4912.tar -C media/
```

- [ ] **Step 2: Verify entry count**

Run:
```bash
find migration/source/media -type f | wc -l
```

Expected: 262.

- [ ] **Step 3: Spot-check folder structure**

Run:
```bash
ls migration/source/media | head -5
ls migration/source/media/2014/11 | head -10
```

Expected: top level is `YYYY/`; below that `MM/`; below that files.

- [ ] **Step 4: Verify `migration/source/` is gitignored**

Run:
```bash
git check-ignore -v migration/source/media/2014/11/muutoskartta_fin_2-sivuinen_upd.doc
```

Expected: `.gitignore:N:migration/source/`. No commit needed for the untar.

### Task 9: `lib/lang.py` — Language inference (TDD)

**Files:**
- Create: `migration/lib/lang.py`
- Create: `migration/tests/test_lang.py`

The helper infers `'en' | 'fi'` from (a) a WP category list (Finnish category names → fi, English → en) and (b) Unicode heuristic on body text when category-based inference is ambiguous.

- [ ] **Step 1: Write the failing tests**

`migration/tests/test_lang.py`:
```python
import pytest
from lib.lang import infer_lang


def test_clear_finnish_categories_returns_fi():
    assert infer_lang(categories=["Ilmahygienia", "Varautuminen"], body="") == "fi"


def test_clear_english_categories_returns_en():
    assert infer_lang(categories=["Complex systems"], body="") == "en"


def test_no_categories_falls_back_to_body_heuristic_fi():
    body = "Tämä on suomenkielinen teksti, jossa on ääkkösiä ja muita merkkejä."
    assert infer_lang(categories=[], body=body) == "fi"


def test_no_categories_falls_back_to_body_heuristic_en():
    body = "This is an English-language post about behaviour change and uncertainty."
    assert infer_lang(categories=[], body=body) == "en"


def test_finnish_chars_dominate_short_body_returns_fi():
    body = "Pää ja ääni."
    assert infer_lang(categories=[], body=body) == "fi"


def test_mixed_categories_picks_more_frequent():
    # "Käyttäytymismuutos" is the FI side; should win
    assert infer_lang(categories=["Käyttäytymismuutos", "Käyttäytymismuutos", "Decision-making"], body="") == "fi"
```

Import path is `from lib.lang import infer_lang`. The `lib` package is exposed by the `packages.find` config in `pyproject.toml` (set up in Task 7); the editable install from Task 7 Step 3 makes it importable from anywhere in the venv.

- [ ] **Step 2: Run tests, confirm they fail**

```bash
pytest tests/test_lang.py -v
```

Expected: ImportError or ModuleNotFoundError — `lib.lang` doesn't exist yet.

- [ ] **Step 3: Implement `lib/lang.py`**

```python
"""Language inference from WordPress category + body text."""
from __future__ import annotations

import re

_FI_CHARS = set("äöåÄÖÅ")
# Finnish-named WP categories from the export inventory.
# Conservative: if the category name contains any of these tokens, it's FI.
_FI_CATEGORY_TOKENS = {
    "käyttäytym", "varautu", "terveys", "hyvinvoint", "ilmahygien",
    "kompleks", "muutos", "psykolog", "ajattel", "kriisi",
    "yhteistyö", "suomeksi",
}
_EN_CATEGORY_TOKENS = {
    "complex systems", "behaviour", "uncertainty", "self-management",
    "decision-making", "preparedness", "health", "wellbeing", "well-being",
    "risk", "english",
}


def _category_votes(categories: list[str]) -> tuple[int, int]:
    fi = en = 0
    for c in categories:
        lc = c.lower()
        if any(tok in lc for tok in _FI_CATEGORY_TOKENS):
            fi += 1
        if any(tok in lc for tok in _EN_CATEGORY_TOKENS):
            en += 1
    return fi, en


def _body_heuristic(body: str) -> str:
    """Finnish-character ratio over a sample. If >0.5% of alphabetic chars
    are Finnish-specific, classify as fi. Empty body → en (default)."""
    alpha = [c for c in body if c.isalpha()]
    if not alpha:
        return "en"
    fi_chars = sum(1 for c in alpha if c in _FI_CHARS)
    ratio = fi_chars / len(alpha)
    return "fi" if ratio > 0.005 else "en"


def infer_lang(categories: list[str], body: str) -> str:
    """Return 'fi' or 'en' for a post.

    Strategy:
      1. Category vote: count tokens matched in FI vs EN sets. Majority wins.
      2. On tie or zero votes: Unicode heuristic on body text.
    """
    fi, en = _category_votes(categories)
    if fi > en:
        return "fi"
    if en > fi:
        return "en"
    return _body_heuristic(body)
```

- [ ] **Step 4: Re-run tests, confirm pass**

```bash
pytest tests/test_lang.py -v
```

Expected: 6 passing.

- [ ] **Step 5: Commit**

```bash
cd C:/Users/qn353/Documents/git-projects/mattiheino-site
git add migration/lib/lang.py migration/tests/test_lang.py
git commit -m "feat(migration): lang.py — infer en/fi from category + Unicode heuristic"
git push
```

### Task 10: `lib/categories.py` — Category → tag mapping

**Files:**
- Create: `migration/lib/categories.py`
- Create: `migration/category-to-tag.txt` (manual config, hand-edited later)
- Create: `migration/tests/test_categories.py`

The helper maps WP category names to a normalised tag slug. The mapping file lets Matti tune the slugs by hand.

- [ ] **Step 1: Write the failing tests**

`migration/tests/test_categories.py`:
```python
import pytest
from pathlib import Path
from lib.categories import load_mapping, categories_to_tags


def test_load_mapping_parses_simple_pairs(tmp_path):
    f = tmp_path / "map.txt"
    f.write_text("Complex systems = complex-systems\nKäyttäytymismuutos = behaviour-change\n")
    m = load_mapping(f)
    assert m["complex systems"] == "complex-systems"
    assert m["käyttäytymismuutos"] == "behaviour-change"


def test_load_mapping_ignores_blank_and_comment_lines(tmp_path):
    f = tmp_path / "map.txt"
    f.write_text("# comment\n\nA = a\n# another\nB = b\n")
    m = load_mapping(f)
    assert m == {"a": "a", "b": "b"}


def test_categories_to_tags_resolves_known():
    m = {"complex systems": "complex-systems", "uncategorized": "uncategorised"}
    assert categories_to_tags(["Complex systems", "Uncategorized"], m) == ["complex-systems", "uncategorised"]


def test_categories_to_tags_unknown_falls_back_to_slug():
    m = {"complex systems": "complex-systems"}
    assert categories_to_tags(["Behaviour Change"], m) == ["behaviour-change"]


def test_categories_to_tags_empty_returns_uncategorised():
    m = {}
    assert categories_to_tags([], m) == ["uncategorised"]


def test_categories_to_tags_dedupes():
    m = {}
    assert categories_to_tags(["Foo", "foo", "FOO"], m) == ["foo"]
```

- [ ] **Step 2: Run, confirm fail**

```bash
pytest tests/test_categories.py -v
```

Expected: ImportError on `lib.categories`.

- [ ] **Step 3: Implement**

`migration/lib/categories.py`:
```python
"""Map WordPress categories → frontmatter tag slugs."""
from __future__ import annotations

from pathlib import Path
from slugify import slugify


def load_mapping(path: Path) -> dict[str, str]:
    """Parse a 'Category Name = tag-slug' file. Keys are lowercased."""
    m: dict[str, str] = {}
    for line in path.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if not line or line.startswith("#"):
            continue
        if "=" not in line:
            continue
        key, value = (s.strip() for s in line.split("=", 1))
        m[key.lower()] = value
    return m


def categories_to_tags(categories: list[str], mapping: dict[str, str]) -> list[str]:
    """Translate a WP post's category list to a unique, ordered tag list."""
    if not categories:
        return ["uncategorised"]
    seen: set[str] = set()
    out: list[str] = []
    for c in categories:
        key = c.lower()
        tag = mapping.get(key, slugify(key))
        if tag not in seen:
            seen.add(tag)
            out.append(tag)
    return out
```

- [ ] **Step 4: Run, confirm pass**

```bash
pytest tests/test_categories.py -v
```

Expected: 6 passing.

- [ ] **Step 5: Seed `migration/category-to-tag.txt`**

```
# WordPress category → frontmatter tag slug.
# Edit by hand. Re-run import_wp.py to apply.
# Format: "WP category name" = "tag-slug"
# Lookup is case-insensitive on the LHS.

Complex systems        = complex-systems
Behaviour change       = behaviour-change
Preparedness           = preparedness
Health                 = health
Risk                   = risk
Self-management        = self-management
Uncertainty            = uncertainty
Käyttäytymismuutos     = käyttäytymismuutos
Varautuminen           = varautuminen
Ilmahygienia           = ilmahygienia
Terveys                = terveys
Kompleksisuus          = kompleksisuus
Uncategorized          = uncategorised
```

Tune after seeing the actual category distribution in the export.

- [ ] **Step 6: Commit**

```bash
git add migration/lib/categories.py migration/tests/test_categories.py migration/category-to-tag.txt
git commit -m "feat(migration): categories.py + initial category→tag mapping"
git push
```

### Task 11: `lib/slug.py` — Slug normalisation + redirect emission

**Files:**
- Create: `migration/lib/slug.py`
- Create: `migration/tests/test_slug.py`

- [ ] **Step 1: Write failing tests**

`migration/tests/test_slug.py`:
```python
import pytest
from lib.slug import normalise_slug, redirect_lines_for


def test_normalise_slug_lowercases():
    assert normalise_slug("Hello World") == "hello-world"


def test_normalise_slug_preserves_finnish_chars():
    # Astro content collection IDs allow Unicode; keep ä/ö/å
    assert normalise_slug("Käyttäytymisarkkitehtuuri") == "käyttäytymisarkkitehtuuri"


def test_redirect_lines_for_same_slug_returns_empty():
    assert redirect_lines_for(wp_slug="foo", new_slug="foo", new_path="/posts/foo/") == []


def test_redirect_lines_for_changed_slug_emits_two_variants():
    lines = redirect_lines_for(wp_slug="old-name", new_slug="new-name", new_path="/posts/new-name/")
    assert "/old-name/  /posts/new-name/  301" in lines
    assert any("/2014/" not in l for l in lines)


def test_redirect_lines_for_dated_wp_url_when_year_month_given():
    lines = redirect_lines_for(
        wp_slug="old-name", new_slug="new-name", new_path="/posts/new-name/",
        year="2014", month="11",
    )
    assert "/2014/11/old-name/  /posts/new-name/  301" in lines
    assert "/old-name/  /posts/new-name/  301" in lines
```

- [ ] **Step 2: Run, confirm fail**

```bash
pytest tests/test_slug.py -v
```

- [ ] **Step 3: Implement**

`migration/lib/slug.py`:
```python
"""Slug normalisation + per-URL redirect emission."""
from __future__ import annotations


def normalise_slug(slug: str) -> str:
    """Lowercase + dash-separate, but preserve Finnish ä/ö/å."""
    out: list[str] = []
    for ch in slug.lower():
        if ch.isalnum() or ch in "äöå":
            out.append(ch)
        elif ch in " -_":
            if out and out[-1] != "-":
                out.append("-")
    return "".join(out).strip("-")


def redirect_lines_for(
    wp_slug: str,
    new_slug: str,
    new_path: str,
    year: str | None = None,
    month: str | None = None,
) -> list[str]:
    """Emit _redirects lines for a post.

    No-op when wp_slug == new_slug. Otherwise emit one or two 301s:
      - bare /<wp_slug>/ → new_path
      - /<year>/<month>/<wp_slug>/ → new_path (if year+month given)
    """
    if wp_slug == new_slug:
        return []
    lines = [f"/{wp_slug}/  {new_path}  301"]
    if year and month:
        lines.append(f"/{year}/{month}/{wp_slug}/  {new_path}  301")
    return lines
```

- [ ] **Step 4: Run, confirm pass**

```bash
pytest tests/test_slug.py -v
```

- [ ] **Step 5: Commit**

```bash
git add migration/lib/slug.py migration/tests/test_slug.py
git commit -m "feat(migration): slug.py — slug normalisation + redirect line emission"
git push
```

### Task 12: `lib/html_to_md.py` — HTML → Markdown + shortcode sweep

**Files:**
- Create: `migration/lib/html_to_md.py`
- Create: `migration/tests/test_html_to_md.py`

- [ ] **Step 1: Write failing tests**

`migration/tests/test_html_to_md.py`:
```python
import pytest
from lib.html_to_md import sweep_shortcodes, to_markdown


def test_strip_caption_shortcode_preserves_img_and_caption():
    src = (
        '[caption id="" align="alignnone" width="500"]'
        '<img class="x" src="http://e.com/i.jpg" alt="" width="500" />'
        ' My caption[/caption]'
    )
    out = sweep_shortcodes(src)
    assert "[caption" not in out
    assert "[/caption]" not in out
    assert "<img" in out
    assert "My caption" in out


def test_strip_gutenberg_block_comments():
    src = "<!-- wp:paragraph --><p>Hello</p><!-- /wp:paragraph -->"
    out = sweep_shortcodes(src)
    assert "wp:paragraph" not in out
    assert "<p>Hello</p>" in out


def test_strip_more_marker():
    src = "Intro<!--more-->Body"
    out = sweep_shortcodes(src)
    assert "more" not in out


def test_gallery_left_as_marker():
    src = '[gallery ids="1,2,3"]'
    out = sweep_shortcodes(src)
    assert "TODO: gallery" in out


def test_to_markdown_basic_paragraph():
    html = "<p>This is a <strong>test</strong>.</p>"
    md = to_markdown(html)
    assert md.strip() == "This is a **test**."


def test_to_markdown_preserves_links():
    html = '<p>See <a href="https://example.com">example</a>.</p>'
    md = to_markdown(html)
    assert "[example](https://example.com)" in md
```

- [ ] **Step 2: Run, confirm fail**

```bash
pytest tests/test_html_to_md.py -v
```

- [ ] **Step 3: Implement**

`migration/lib/html_to_md.py`:
```python
"""HTML → Markdown conversion with WordPress shortcode + Gutenberg sweep."""
from __future__ import annotations

import re
from markdownify import markdownify as _md


_CAPTION_RE = re.compile(
    r"\[caption[^\]]*\](.*?)\[/caption\]",
    re.IGNORECASE | re.DOTALL,
)
_GUTENBERG_RE = re.compile(r"<!--\s*/?wp:[^>]*-->")
_MORE_RE = re.compile(r"<!--\s*more\s*-->", re.IGNORECASE)
_GALLERY_RE = re.compile(r"\[gallery[^\]]*\]", re.IGNORECASE)


def sweep_shortcodes(html: str) -> str:
    """Strip / replace WP shortcodes + Gutenberg block comments.

    - [caption ...]<img> caption[/caption]  → inner content kept verbatim
    - <!-- wp:* --> / <!-- /wp:* -->        → stripped
    - <!--more-->                            → stripped
    - [gallery ids="..."]                    → '<!-- TODO: gallery -->'
    """
    html = _CAPTION_RE.sub(lambda m: m.group(1), html)
    html = _GUTENBERG_RE.sub("", html)
    html = _MORE_RE.sub("", html)
    html = _GALLERY_RE.sub("<!-- TODO: gallery -->", html)
    return html


def to_markdown(html: str) -> str:
    """Convert sanitised HTML to Markdown via markdownify.

    Run sweep_shortcodes() first to clear WP-specific cruft, then convert.
    """
    return _md(html, heading_style="ATX", bullets="-")
```

- [ ] **Step 4: Run, confirm pass**

```bash
pytest tests/test_html_to_md.py -v
```

- [ ] **Step 5: Commit**

```bash
git add migration/lib/html_to_md.py migration/tests/test_html_to_md.py
git commit -m "feat(migration): html_to_md.py — shortcode sweep + markdownify conversion"
git push
```

### Task 13: `lib/images.py` — Image rehost pipeline

**Files:**
- Create: `migration/lib/images.py`
- Create: `migration/tests/test_images.py`
- Create: `migration/tests/fixtures/media/2014/11/foo.jpg` (small fixture, ~1 KB)
- Create: `migration/tests/fixtures/gdrive/lottalosada.jpg` (small fixture, ~1 KB)

- [ ] **Step 1: Create test fixtures**

Run (Bash):
```bash
mkdir -p migration/tests/fixtures/media/2014/11
mkdir -p migration/tests/fixtures/gdrive
# Generate 1-KB placeholder JPEGs
python -c "open('migration/tests/fixtures/media/2014/11/foo.jpg','wb').write(b'\\xff\\xd8\\xff\\xd9' + b'\\x00'*1020)"
python -c "open('migration/tests/fixtures/gdrive/lottalosada.jpg','wb').write(b'\\xff\\xd8\\xff\\xd9' + b'\\x00'*1020)"
```

- [ ] **Step 2: Write failing tests**

`migration/tests/test_images.py`:
```python
from pathlib import Path

import pytest

from lib.images import (
    GDRIVE_FOLDER, MEDIA_ROOT, classify_src, rehost,
    build_gdrive_index, build_media_index,
)


def test_classify_wp_cdn_with_uploads_prefix():
    assert classify_src("https://mattiheino.files.wordpress.com/wp-content/uploads/2014/11/foo.jpg") == "wp-cdn"


def test_classify_external():
    assert classify_src("https://daringtodo.com/wp-content/uploads/2010/07/x.jpg") == "external"


def test_classify_relative_assumed_wp_cdn():
    # WP exports sometimes have relative paths.
    assert classify_src("/wp-content/uploads/2014/11/foo.jpg") == "wp-cdn"


def test_build_media_index_maps_relative_paths(fixtures_dir, tmp_path):
    media = fixtures_dir / "media"
    idx = build_media_index(media)
    assert "2014/11/foo.jpg" in idx
    assert idx["2014/11/foo.jpg"].name == "foo.jpg"


def test_build_gdrive_index_strips_resize_suffix(fixtures_dir):
    idx = build_gdrive_index(fixtures_dir / "gdrive")
    assert "lottalosada.jpg" in idx


def test_rehost_wp_cdn_copies_from_media(fixtures_dir, tmp_path):
    media_idx = build_media_index(fixtures_dir / "media")
    gdrive_idx = build_gdrive_index(fixtures_dir / "gdrive")
    out = tmp_path / "posts/images/sample"
    result = rehost(
        "https://mattiheino.files.wordpress.com/wp-content/uploads/2014/11/foo.jpg",
        slug="sample", dest=out, media_index=media_idx, gdrive_index=gdrive_idx,
    )
    assert result.status == "ok"
    assert result.local_path == out / "foo.jpg"
    assert (out / "foo.jpg").exists()


def test_rehost_external_matches_gdrive_by_basename(fixtures_dir, tmp_path):
    media_idx = build_media_index(fixtures_dir / "media")
    gdrive_idx = build_gdrive_index(fixtures_dir / "gdrive")
    out = tmp_path / "posts/images/sample"
    result = rehost(
        "https://daringtodo.com/wp-content/uploads/2010/07/lottalosada-300x200.jpg",
        slug="sample", dest=out, media_index=media_idx, gdrive_index=gdrive_idx,
    )
    assert result.status == "ok"
    assert result.source == "gdrive"
    assert result.local_path == out / "lottalosada.jpg"


def test_rehost_missing_returns_placeholder(fixtures_dir, tmp_path):
    media_idx = build_media_index(fixtures_dir / "media")
    gdrive_idx = build_gdrive_index(fixtures_dir / "gdrive")
    out = tmp_path / "posts/images/sample"
    result = rehost(
        "https://cdn.meme.am/instances/500x/57546405.jpg",
        slug="sample", dest=out, media_index=media_idx, gdrive_index=gdrive_idx,
    )
    assert result.status == "lost"
    assert result.local_path is None
```

- [ ] **Step 3: Run, confirm fail**

```bash
pytest tests/test_images.py -v
```

- [ ] **Step 4: Implement**

`migration/lib/images.py`:
```python
"""Image rehost pipeline.

For each <img src> in an imported post body:
  - wp-cdn ref → look up in untar'd media index; copy to post images dir
  - external ref → try filename match against GDrive folder; on hit, copy
  - no match → record as 'lost'; caller writes a placeholder + worksheet row
"""
from __future__ import annotations

import re
import shutil
from dataclasses import dataclass
from pathlib import Path
from urllib.parse import urlparse


MEDIA_ROOT = Path("migration/source/media")
GDRIVE_FOLDER = Path("/c/LocalData/hema/Google Drive/Wordpress")

# WP resize suffix pattern e.g. foo-300x200.jpg, bar-1024x768.png
_RESIZE_RE = re.compile(r"-\d+x\d+(?=\.[a-z]+$)", re.IGNORECASE)
_LEADING_HASH_RE = re.compile(r"^#")


@dataclass
class RehostResult:
    status: str       # "ok" | "lost"
    source: str | None  # "media" | "gdrive" | None
    local_path: Path | None  # destination on disk if ok


def classify_src(src: str) -> str:
    """Return 'wp-cdn' or 'external'."""
    u = urlparse(src)
    host = (u.netloc or "").lower()
    path = u.path
    if host.endswith("mattiheino.files.wordpress.com"):
        return "wp-cdn"
    if not host and "/wp-content/uploads/" in path:
        return "wp-cdn"
    return "external"


def _normalise_basename(name: str) -> str:
    """For gdrive matching: lowercase, strip leading '#', strip WP resize suffix."""
    name = _LEADING_HASH_RE.sub("", name)
    name = _RESIZE_RE.sub("", name)
    return name.lower()


def build_media_index(root: Path) -> dict[str, Path]:
    """Walk the untar'd media tree. Map 'YYYY/MM/file.ext' → Path."""
    idx: dict[str, Path] = {}
    for p in root.rglob("*"):
        if p.is_file():
            rel = p.relative_to(root).as_posix()
            idx[rel] = p
    return idx


def build_gdrive_index(root: Path) -> dict[str, Path]:
    """Index the GDrive folder by normalised basename."""
    idx: dict[str, Path] = {}
    for p in root.iterdir():
        if p.is_file() and p.suffix.lower() in {".jpg", ".jpeg", ".png", ".gif", ".webp"}:
            idx[_normalise_basename(p.name)] = p
    return idx


def _extract_relpath_from_wp_cdn(src: str) -> str:
    """Strip the WP-CDN prefix to a 'YYYY/MM/file.ext' relpath."""
    u = urlparse(src)
    path = u.path
    marker = "/wp-content/uploads/"
    if marker in path:
        return path.split(marker, 1)[1]
    return path.lstrip("/")


def rehost(
    src: str,
    *,
    slug: str,
    dest: Path,
    media_index: dict[str, Path],
    gdrive_index: dict[str, Path],
) -> RehostResult:
    """Resolve src → copy a file into dest/. Return RehostResult.

    dest is the post's images/<slug>/ directory; it's created if needed.
    """
    kind = classify_src(src)
    dest.mkdir(parents=True, exist_ok=True)

    if kind == "wp-cdn":
        rel = _extract_relpath_from_wp_cdn(src)
        if rel in media_index:
            srcpath = media_index[rel]
            outpath = dest / srcpath.name
            shutil.copy2(srcpath, outpath)
            return RehostResult(status="ok", source="media", local_path=outpath)
        return RehostResult(status="lost", source=None, local_path=None)

    # external
    basename = Path(urlparse(src).path).name
    key = _normalise_basename(basename)
    if key in gdrive_index:
        srcpath = gdrive_index[key]
        outpath = dest / srcpath.name
        shutil.copy2(srcpath, outpath)
        return RehostResult(status="ok", source="gdrive", local_path=outpath)
    return RehostResult(status="lost", source=None, local_path=None)
```

- [ ] **Step 5: Run, confirm pass**

```bash
pytest tests/test_images.py -v
```

- [ ] **Step 6: Commit**

```bash
git add migration/lib/images.py migration/tests/test_images.py migration/tests/fixtures/
git commit -m "feat(migration): images.py — 3-source rehost pipeline with media + gdrive indices"
git push
```

### Task 14: `lib/dead_images.py` — Worksheet writer

**Files:**
- Create: `migration/lib/dead_images.py`
- Create: `migration/tests/test_dead_images.py`

- [ ] **Step 1: Write failing tests**

`migration/tests/test_dead_images.py`:
```python
from pathlib import Path
from lib.dead_images import DeadImageRow, write_worksheet


def test_write_worksheet_groups_by_collection(tmp_path):
    rows = [
        DeadImageRow(collection="posts", slug="muutoskartta", paragraph=3,
                     original="http://daringtodo.com/x.jpg", alt="Sitku"),
        DeadImageRow(collection="applied-musings", slug="antihauras", paragraph=1,
                     original="http://e.com/y.png", alt="X"),
    ]
    out = tmp_path / "dead.md"
    write_worksheet(out, rows)
    text = out.read_text(encoding="utf-8")
    assert "## posts" in text
    assert "## applied-musings" in text
    assert "muutoskartta" in text
    assert "antihauras" in text


def test_write_worksheet_emits_checkbox_per_row(tmp_path):
    rows = [DeadImageRow(collection="posts", slug="x", paragraph=1, original="u", alt="a")]
    out = tmp_path / "dead.md"
    write_worksheet(out, rows)
    text = out.read_text(encoding="utf-8")
    assert "- [ ]" in text
```

- [ ] **Step 2: Run, confirm fail**

```bash
pytest tests/test_dead_images.py -v
```

- [ ] **Step 3: Implement**

`migration/lib/dead_images.py`:
```python
"""Dead-image worksheet writer."""
from __future__ import annotations

from dataclasses import dataclass
from itertools import groupby
from pathlib import Path


@dataclass(frozen=True)
class DeadImageRow:
    collection: str  # "posts" | "applied-musings"
    slug: str
    paragraph: int
    original: str
    alt: str


def write_worksheet(path: Path, rows: list[DeadImageRow]) -> None:
    """Emit a Markdown worksheet with one checkbox per row, grouped by collection."""
    lines = ["# Dead-image worksheet", "",
             "Each row: pick an image (from GDrive or anywhere), drop it into",
             "`src/content/<collection>/images/<slug>/`, replace the `[Image lost",
             "in migration]` placeholder in the post body with a proper `<Image>`",
             "reference, and tick the row.",
             ""]
    rows_sorted = sorted(rows, key=lambda r: (r.collection, r.slug, r.paragraph))
    for collection, group in groupby(rows_sorted, key=lambda r: r.collection):
        lines.append(f"## {collection}")
        lines.append("")
        for row in group:
            lines.append(f"- [ ] **{row.slug}** · ¶{row.paragraph}")
            lines.append(f"  - Original: `{row.original}`")
            lines.append(f"  - Alt: \"{row.alt}\"")
        lines.append("")
    path.write_text("\n".join(lines), encoding="utf-8")
```

- [ ] **Step 4: Run, confirm pass**

```bash
pytest tests/test_dead_images.py -v
```

- [ ] **Step 5: Commit**

```bash
git add migration/lib/dead_images.py migration/tests/test_dead_images.py
git commit -m "feat(migration): dead_images.py — worksheet writer for vetting-time rehost"
git push
```

### Task 15: `lib/wp_xml.py` — XML parser

**Files:**
- Create: `migration/lib/wp_xml.py`
- Create: `migration/tests/test_wp_xml.py`
- Create: `migration/tests/fixtures/sample_export.xml` (tiny fixture: 2 posts + 1 page)

- [ ] **Step 1: Create the XML fixture**

`migration/tests/fixtures/sample_export.xml`:
```xml
<?xml version="1.0" encoding="UTF-8"?>
<rss version="2.0"
     xmlns:wp="http://wordpress.org/export/1.2/"
     xmlns:dc="http://purl.org/dc/elements/1.1/"
     xmlns:content="http://purl.org/rss/1.0/modules/content/"
     xmlns:excerpt="http://wordpress.org/export/1.2/excerpt/">
  <channel>
    <title>Sample blog</title>
    <link>https://example.test/</link>
    <wp:base_blog_url>https://example.test</wp:base_blog_url>
    <item>
      <title>First post</title>
      <link>https://example.test/2014/11/first-post/</link>
      <pubDate>Sat, 15 Nov 2014 10:00:00 +0000</pubDate>
      <dc:creator>matti</dc:creator>
      <guid isPermaLink="false">https://example.test/?p=1</guid>
      <wp:post_id>1</wp:post_id>
      <wp:post_date>2014-11-15 10:00:00</wp:post_date>
      <wp:post_name>first-post</wp:post_name>
      <wp:status>publish</wp:status>
      <wp:post_type>post</wp:post_type>
      <category domain="category" nicename="complex-systems"><![CDATA[Complex systems]]></category>
      <content:encoded><![CDATA[<p>Hello, <strong>world</strong>.</p><p>An image: <img src="https://mattiheino.files.wordpress.com/wp-content/uploads/2014/11/foo.jpg" alt="" /></p>]]></content:encoded>
      <excerpt:encoded><![CDATA[Intro paragraph.]]></excerpt:encoded>
    </item>
    <item>
      <title>Draft post</title>
      <link>https://example.test/?p=2</link>
      <pubDate>Sun, 16 Nov 2014 10:00:00 +0000</pubDate>
      <dc:creator>matti</dc:creator>
      <guid isPermaLink="false">https://example.test/?p=2</guid>
      <wp:post_id>2</wp:post_id>
      <wp:post_date>2014-11-16 10:00:00</wp:post_date>
      <wp:post_name>draft-post</wp:post_name>
      <wp:status>draft</wp:status>
      <wp:post_type>post</wp:post_type>
      <category domain="category" nicename="kayttaytymismuutos"><![CDATA[Käyttäytymismuutos]]></category>
      <content:encoded><![CDATA[<p>Tämä on luonnos.</p>]]></content:encoded>
      <excerpt:encoded><![CDATA[]]></excerpt:encoded>
    </item>
    <item>
      <title>Welcome page</title>
      <link>https://example.test/tervetuloa/</link>
      <pubDate>Mon, 17 Sep 2012 10:00:00 +0000</pubDate>
      <dc:creator>matti</dc:creator>
      <guid isPermaLink="false">https://example.test/?p=3</guid>
      <wp:post_id>3</wp:post_id>
      <wp:post_date>2012-09-17 10:00:00</wp:post_date>
      <wp:post_name>tervetuloa</wp:post_name>
      <wp:status>private</wp:status>
      <wp:post_type>page</wp:post_type>
      <content:encoded><![CDATA[<p>Tervetuloa.</p>]]></content:encoded>
      <excerpt:encoded><![CDATA[]]></excerpt:encoded>
    </item>
  </channel>
</rss>
```

- [ ] **Step 2: Write failing tests**

`migration/tests/test_wp_xml.py`:
```python
from datetime import datetime
from lib.wp_xml import iter_items


def test_iter_items_yields_all_items(fixtures_dir):
    items = list(iter_items(fixtures_dir / "sample_export.xml"))
    assert len(items) == 3


def test_iter_items_parses_first_post_fields(fixtures_dir):
    items = list(iter_items(fixtures_dir / "sample_export.xml"))
    p = items[0]
    assert p.title == "First post"
    assert p.slug == "first-post"
    assert p.status == "publish"
    assert p.post_type == "post"
    assert p.guid == "https://example.test/?p=1"
    assert p.published == datetime(2014, 11, 15, 10, 0, 0)
    assert p.categories == ["Complex systems"]
    assert "Hello" in p.content_html


def test_iter_items_distinguishes_drafts(fixtures_dir):
    items = list(iter_items(fixtures_dir / "sample_export.xml"))
    drafts = [i for i in items if i.status == "draft"]
    assert len(drafts) == 1
    assert drafts[0].slug == "draft-post"


def test_iter_items_picks_up_pages(fixtures_dir):
    items = list(iter_items(fixtures_dir / "sample_export.xml"))
    pages = [i for i in items if i.post_type == "page"]
    assert len(pages) == 1
    assert pages[0].slug == "tervetuloa"
```

- [ ] **Step 3: Run, confirm fail**

```bash
pytest tests/test_wp_xml.py -v
```

- [ ] **Step 4: Implement**

`migration/lib/wp_xml.py`:
```python
"""Parse a WordPress eXtended RSS (WXR) export."""
from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime
from pathlib import Path
from typing import Iterator
from lxml import etree


NS = {
    "wp": "http://wordpress.org/export/1.2/",
    "dc": "http://purl.org/dc/elements/1.1/",
    "content": "http://purl.org/rss/1.0/modules/content/",
    "excerpt": "http://wordpress.org/export/1.2/excerpt/",
}


@dataclass(frozen=True)
class WPItem:
    title: str
    slug: str
    status: str          # publish | draft | private | pending | ...
    post_type: str       # post | page | attachment | ...
    guid: str
    published: datetime
    categories: list[str]
    content_html: str
    excerpt: str


def _text(elem, xpath: str, ns: dict | None = None) -> str:
    nodes = elem.xpath(xpath, namespaces=ns or NS)
    if not nodes:
        return ""
    n = nodes[0]
    return (n.text or "") if hasattr(n, "text") else str(n)


def iter_items(xml_path: Path) -> Iterator[WPItem]:
    tree = etree.parse(str(xml_path))
    for item in tree.xpath("//item"):
        title = _text(item, "title")
        slug = _text(item, "wp:post_name")
        status = _text(item, "wp:status")
        post_type = _text(item, "wp:post_type")
        guid = _text(item, "guid")
        pub_str = _text(item, "wp:post_date")
        try:
            published = datetime.strptime(pub_str, "%Y-%m-%d %H:%M:%S")
        except ValueError:
            published = datetime(1970, 1, 1)
        categories = [
            (c.text or "")
            for c in item.xpath("category[@domain='category']")
        ]
        content_html = _text(item, "content:encoded")
        excerpt = _text(item, "excerpt:encoded")
        yield WPItem(
            title=title,
            slug=slug,
            status=status,
            post_type=post_type,
            guid=guid,
            published=published,
            categories=categories,
            content_html=content_html,
            excerpt=excerpt,
        )
```

- [ ] **Step 5: Run, confirm pass**

```bash
pytest tests/test_wp_xml.py -v
```

- [ ] **Step 6: Commit**

```bash
git add migration/lib/wp_xml.py migration/tests/test_wp_xml.py migration/tests/fixtures/sample_export.xml
git commit -m "feat(migration): wp_xml.py — iterate <item>s from WXR with frozen dataclass"
git push
```

### Task 16: `lib/pages.py` — Page disposition map

**Files:**
- Create: `migration/lib/pages.py`
- Create: `migration/tests/test_pages.py`

- [ ] **Step 1: Write failing tests**

`migration/tests/test_pages.py`:
```python
from lib.pages import disposition_for, PageDisposition


def test_disposition_for_known_slug_returns_import_as_draft():
    d = disposition_for("johdatus-kayttaytymisarkkitehtuuriin")
    assert d.action == "import"
    assert d.draft is True
    assert d.collection == "posts"


def test_disposition_for_10_taitoa_same():
    d = disposition_for("10-taitoa")
    assert d.action == "import"
    assert d.draft is True
    assert d.collection == "posts"


def test_disposition_for_yhteistyon_manifesti_same():
    d = disposition_for("yhteistyon-manifesti")
    assert d.action == "import"
    assert d.draft is True


def test_disposition_for_tervetuloa_returns_skip():
    d = disposition_for("tervetuloa")
    assert d.action == "skip"


def test_disposition_for_unknown_returns_skip_with_reason():
    d = disposition_for("research-the-academic-stuff")
    assert d.action == "skip"
    assert d.reason
```

- [ ] **Step 2: Run, confirm fail**

```bash
pytest tests/test_pages.py -v
```

- [ ] **Step 3: Implement**

`migration/lib/pages.py`:
```python
"""Disposition map for the 9 WP pages."""
from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class PageDisposition:
    action: str      # "import" | "skip"
    collection: str  # "posts" | "applied-musings" | ""
    draft: bool
    reason: str


_MAP: dict[str, PageDisposition] = {
    # Import as drafts in posts/ — need revising before publishing
    "johdatus-kayttaytymisarkkitehtuuriin": PageDisposition(
        action="import", collection="posts", draft=True,
        reason="published in WP; needs revising before re-publishing",
    ),
    "10-taitoa": PageDisposition(
        action="import", collection="posts", draft=True,
        reason="published in WP; needs revising before re-publishing",
    ),
    "yhteistyon-manifesti": PageDisposition(
        action="import", collection="posts", draft=True,
        reason="private in WP; never went live",
    ),
    # Skip
    "tervetuloa": PageDisposition(
        action="skip", collection="", draft=False,
        reason="home page already serves FI welcome",
    ),
    "reflektiota-oppimisesta-pohdintaa-lahtotilanteesta": PageDisposition(
        action="skip", collection="", draft=False,
        reason="uni-course reflection, not blog content",
    ),
    "sisallysluettelo": PageDisposition(
        action="skip", collection="", draft=False, reason="placeholder stub",
    ),
    "parempaa-ajattelua-rakentamassa": PageDisposition(
        action="skip", collection="", draft=False, reason="placeholder stub",
    ),
    "research-the-academic-stuff": PageDisposition(
        action="skip", collection="", draft=False,
        reason="2015 CV-style EN page; Google Scholar link covers it",
    ),
    "": PageDisposition(  # the empty-slug Welcome / Tervetuloa
        action="skip", collection="", draft=False,
        reason="lang-router stub; replaced by new home",
    ),
}


def disposition_for(slug: str) -> PageDisposition:
    """Return the import disposition for a WP page slug.

    Default is skip with a generic reason. Known slugs override.
    """
    return _MAP.get(
        slug,
        PageDisposition(
            action="skip", collection="", draft=False,
            reason="unknown page slug — review manually",
        ),
    )
```

- [ ] **Step 4: Run, confirm pass**

```bash
pytest tests/test_pages.py -v
```

- [ ] **Step 5: Commit**

```bash
git add migration/lib/pages.py migration/tests/test_pages.py
git commit -m "feat(migration): pages.py — disposition map for the 9 WP pages

3 imports as draft (#4 #5 #6 from spec §6.5); 6 skips with stated reason."
git push
```

### Task 17: `import_wp.py` — Main entry point

**Files:**
- Create: `migration/import_wp.py`
- Create: `migration/post_collection_overrides.txt` (empty initially; format documented in header comment)

- [ ] **Step 1: Seed the override file**

`migration/post_collection_overrides.txt`:
```
# WP post slugs that should land in applied-musings/ instead of posts/.
# One slug per line. Lines starting with # are comments.
# Edit by hand before/after the first import_wp.py run.
```

- [ ] **Step 2: Write `migration/import_wp.py`**

```python
"""WordPress eXtended RSS → Astro content collection import.

One-shot pipeline. Reads:
  - migration/source/andoutcomethesystemskyttytymisarkkitehtuuri.WordPress.2026-05-20.xml
  - migration/source/media/ (untar'd)
  - migration/category-to-tag.txt
  - migration/post_collection_overrides.txt

Writes:
  - src/content/posts/YYYY-MM-DD-<slug>.md (+ images/<slug>/ folder)
  - src/content/applied-musings/YYYY-MM-DD-<slug>.md (+ images/<slug>/)
  - public/_redirects (append)
  - migration/dead-images-todo.md

Usage:
  cd migration && .venv/Scripts/activate
  python import_wp.py --dry-run    # no writes; report only
  python import_wp.py              # actual import
"""
from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

from lib.categories import categories_to_tags, load_mapping
from lib.dead_images import DeadImageRow, write_worksheet
from lib.html_to_md import sweep_shortcodes, to_markdown
from lib.images import (
    GDRIVE_FOLDER, MEDIA_ROOT, build_gdrive_index, build_media_index,
    classify_src, rehost,
)
from lib.lang import infer_lang
from lib.pages import disposition_for
from lib.slug import normalise_slug, redirect_lines_for
from lib.wp_xml import WPItem, iter_items


REPO_ROOT = Path(__file__).parent.parent
XML_PATH = REPO_ROOT / "migration" / "source" / "andoutcomethesystemskyttytymisarkkitehtuuri.WordPress.2026-05-20.xml"
CONTENT_ROOT = REPO_ROOT / "src" / "content"
REDIRECTS_PATH = REPO_ROOT / "public" / "_redirects"
WORKSHEET_PATH = REPO_ROOT / "migration" / "dead-images-todo.md"
CATEGORY_MAP_PATH = REPO_ROOT / "migration" / "category-to-tag.txt"
OVERRIDES_PATH = REPO_ROOT / "migration" / "post_collection_overrides.txt"


_IMG_RE = re.compile(r'<img[^>]+src=["\']([^"\']+)["\'][^>]*>', re.IGNORECASE)


def _load_overrides(path: Path) -> set[str]:
    if not path.exists():
        return set()
    return {
        line.strip()
        for line in path.read_text(encoding="utf-8").splitlines()
        if line.strip() and not line.strip().startswith("#")
    }


def _pick_collection(item: WPItem, overrides: set[str]) -> str:
    return "applied-musings" if item.slug in overrides else "posts"


def _frontmatter(item: WPItem, lang: str, tags: list[str], collection: str, draft: bool) -> str:
    description = (item.excerpt.strip()
                   or _first_paragraph(item.content_html)[:160].strip())
    description = description.replace('"', "'")
    parts = [
        "---",
        f'title: "{item.title.replace(chr(34), chr(39))}"',
        f'description: "{description}"',
        f"published: {item.published.date().isoformat()}",
        f"lang: {lang}",
        "vetting_status: pending",
        "migration_source: mattiheino-wp",
        f"draft: {'true' if draft else 'false'}",
        f"tags: [{', '.join(repr(t) for t in tags)}]",
        f'wp_guid: "{item.guid}"',
        "---",
        "",
    ]
    return "\n".join(parts)


def _first_paragraph(html: str) -> str:
    m = re.search(r"<p[^>]*>(.*?)</p>", html, re.IGNORECASE | re.DOTALL)
    if not m:
        return ""
    text = re.sub(r"<[^>]+>", "", m.group(1))
    return text


def _process_item(item: WPItem, collection: str, draft: bool,
                  media_index, gdrive_index, dead_rows: list[DeadImageRow],
                  category_map: dict[str, str], dry_run: bool) -> list[str]:
    """Return the list of _redirects lines emitted for this item."""
    new_slug = normalise_slug(item.slug)
    out_path = CONTENT_ROOT / collection / f"{item.published.date().isoformat()}-{new_slug}.md"
    images_dir = CONTENT_ROOT / collection / "images" / new_slug

    lang = infer_lang(item.categories, item.content_html)
    tags = categories_to_tags(item.categories, category_map)
    body_html = sweep_shortcodes(item.content_html)

    # Rehost + rewrite images
    for i, m in enumerate(_IMG_RE.finditer(body_html), start=1):
        src = m.group(1)
        result = rehost(src, slug=new_slug, dest=images_dir,
                        media_index=media_index, gdrive_index=gdrive_index)
        if result.status == "ok":
            new_src = f"./images/{new_slug}/{result.local_path.name}"
            body_html = body_html.replace(src, new_src, 1)
        else:
            placeholder = "<!-- IMAGE LOST: src=" + src + " -->"
            body_html = body_html.replace(m.group(0), placeholder, 1)
            dead_rows.append(DeadImageRow(
                collection=collection, slug=new_slug, paragraph=i,
                original=src, alt="",
            ))

    body_md = to_markdown(body_html)
    fm = _frontmatter(item, lang, tags, collection, draft)
    full = fm + body_md.strip() + "\n"

    if not dry_run:
        out_path.parent.mkdir(parents=True, exist_ok=True)
        out_path.write_text(full, encoding="utf-8")

    # Redirects (year + month from publish date)
    year = f"{item.published.year:04d}"
    month = f"{item.published.month:02d}"
    new_path = f"/{collection}/{new_slug}/"
    return redirect_lines_for(
        wp_slug=item.slug, new_slug=new_slug, new_path=new_path,
        year=year, month=month,
    )


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()

    media_index = build_media_index(REPO_ROOT / MEDIA_ROOT)
    gdrive_index = build_gdrive_index(GDRIVE_FOLDER)
    overrides = _load_overrides(OVERRIDES_PATH)
    category_map = load_mapping(CATEGORY_MAP_PATH)

    dead_rows: list[DeadImageRow] = []
    redirect_lines: list[str] = []
    counts = {"published": 0, "drafts": 0, "pages_imported": 0,
              "pages_skipped": 0, "images_ok": 0, "images_lost": 0}

    for item in iter_items(XML_PATH):
        if item.post_type == "page":
            d = disposition_for(item.slug)
            if d.action == "skip":
                counts["pages_skipped"] += 1
                print(f"  skip page  {item.slug}  ({d.reason})")
                continue
            counts["pages_imported"] += 1
            redirect_lines.extend(_process_item(
                item, collection=d.collection, draft=d.draft,
                media_index=media_index, gdrive_index=gdrive_index,
                dead_rows=dead_rows, category_map=category_map,
                dry_run=args.dry_run,
            ))
            continue

        if item.post_type != "post":
            continue

        if item.status == "publish":
            counts["published"] += 1
            draft = False
        elif item.status == "draft":
            counts["drafts"] += 1
            draft = True
        else:
            continue  # private / pending / trash → skip

        collection = _pick_collection(item, overrides)
        redirect_lines.extend(_process_item(
            item, collection=collection, draft=draft,
            media_index=media_index, gdrive_index=gdrive_index,
            dead_rows=dead_rows, category_map=category_map,
            dry_run=args.dry_run,
        ))

    counts["images_lost"] = len(dead_rows)

    if not args.dry_run:
        WORKSHEET_PATH.parent.mkdir(parents=True, exist_ok=True)
        write_worksheet(WORKSHEET_PATH, dead_rows)

        if redirect_lines:
            REDIRECTS_PATH.parent.mkdir(parents=True, exist_ok=True)
            existing = REDIRECTS_PATH.read_text(encoding="utf-8") if REDIRECTS_PATH.exists() else ""
            block = "# === BEGIN WP slug redirects (import_wp.py) ===\n"
            block += "\n".join(redirect_lines) + "\n"
            block += "# === END WP slug redirects ===\n"
            # Strip any prior version of this block before re-emitting
            cleaned = re.sub(
                r"# === BEGIN WP slug redirects[\s\S]*?# === END WP slug redirects ===\n?",
                "", existing,
            )
            REDIRECTS_PATH.write_text(cleaned + block, encoding="utf-8")

    print("\n=== import_wp.py summary ===")
    for k, v in counts.items():
        print(f"  {k:18s} {v}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
```

- [ ] **Step 3: Dry-run on the real export**

Run:
```bash
cd migration
.venv\Scripts\activate
python import_wp.py --dry-run
```

Expected output: a summary line like
```
published          104
drafts             17
pages_imported     3
pages_skipped      6
images_ok          ???
images_lost        ???
```

- [ ] **Step 4: Read the dry-run report; sanity-check counts**

- 104 published posts expected. If the count is off, debug `wp_xml.iter_items` against the real XML.
- 17 drafts expected.
- 3 pages imported, 6 skipped.

If any count is wrong, fix before proceeding.

- [ ] **Step 5: Commit (without running the real import yet)**

```bash
cd C:/Users/qn353/Documents/git-projects/mattiheino-site
git add migration/import_wp.py migration/post_collection_overrides.txt
git commit -m "feat(migration): import_wp.py — main entry point + dry-run summary"
git push
```

### Task 18: First real import + manual review

**Files generated (committed in Task 19):**
- `src/content/posts/*.md` (~104 + drafts)
- `src/content/applied-musings/*.md` (any overridden)
- `src/content/posts/images/<slug>/*`, `src/content/applied-musings/images/<slug>/*`
- `migration/dead-images-todo.md`
- `public/_redirects` (block appended)

- [ ] **Step 1: Run the real import**

```bash
cd migration
.venv\Scripts\activate
python import_wp.py
```

Expected: same summary as Task 17 Step 3, but with files now on disk. Run time: < 60 sec for 104 posts.

- [ ] **Step 2: Spot-check three imported posts**

```bash
ls src/content/posts | head -10
cat src/content/posts/2025-11-10-tail-events.md | head -30
```

Each Markdown file should have:
- Valid YAML frontmatter (title, description, published, lang, vetting_status, migration_source, draft, tags, wp_guid)
- Markdown body (no raw `[caption]` shortcodes; no `<!-- wp: -->` Gutenberg comments)
- `./images/<slug>/foo.jpg` paths instead of `https://mattiheino.files.wordpress.com/...` paths

- [ ] **Step 3: Inspect `dead-images-todo.md`**

```bash
cat migration/dead-images-todo.md | head -30
wc -l migration/dead-images-todo.md
```

- Skim the list. Are there obvious GDrive matches that the auto-matcher missed? If so, add the missing filename normalisation to `lib/images.py` (e.g., spaces vs underscores) and re-run.

- [ ] **Step 4: Try `npm run build`; expect Zod errors on first run**

```bash
cd C:/Users/qn353/Documents/git-projects/mattiheino-site
npm run build 2>&1 | tail -40
```

Typical first-run errors:
- A post missing `description` (frontmatter generation fell through). Fix the generator in `import_wp.py`, re-run.
- A post with a `tags` array of non-strings (slugify edge case). Fix.
- A post with an invalid `published` date format. Fix.

Iterate until `npm run build` succeeds.

- [ ] **Step 5: Smoke-test rendered pages locally**

```bash
npm run preview
```

Open in Brave: `http://localhost:4321/posts/`, then click into 2-3 posts at random. Confirm:
- Images render
- No raw HTML / leftover shortcode artefacts in the body
- Date stamp renders correctly

- [ ] **Step 6: Commit (this is a big commit)**

```bash
git add src/content public/_redirects migration/dead-images-todo.md migration/post_collection_overrides.txt
git status --short | head -10
git commit -m "feat(content): import 104 WP posts + 17 drafts + 3 pages from 2026-05-20 export

Posts and pages render with rehosted images from the local media tar.
Dead-image references logged in migration/dead-images-todo.md for
vetting-time rehost. WP slug → new slug 301 rules in public/_redirects."
git push
```

- [ ] **Step 7: Deploy + smoke on `new.mattiheino.com`**

Cloudflare Pages auto-deploys on push. Wait ~2 min, then:

```bash
curl -sI https://new.mattiheino.com/posts/tail-events/ | head -8
curl -sI https://new.mattiheino.com/posts/uncertainty/ | head -8
```

Expected: 200s.

### Task 19: Lighthouse audit on imported posts

**Files:** none unless any score < 95.

- [ ] **Step 1: Run Lighthouse on three real-content URLs**

```bash
npx lighthouse https://new.mattiheino.com/ --only-categories=performance,accessibility,best-practices,seo --output=json --output-path=/tmp/lh-home2.json --quiet
npx lighthouse https://new.mattiheino.com/posts/<any-real-slug>/ --output=json --output-path=/tmp/lh-realpost.json --quiet
npx lighthouse https://new.mattiheino.com/archive/ --output=json --output-path=/tmp/lh-archive.json --quiet
```

- [ ] **Step 2: Extract scores**

```bash
for f in /tmp/lh-home2.json /tmp/lh-realpost.json /tmp/lh-archive.json; do
  echo "=== $f ==="
  jq '.categories | to_entries | map({(.key): (.value.score * 100)})' "$f"
done
```

Expected: all ≥ 95. Common Lighthouse regressions after content import:
- Image LCP from a large hero image → add explicit `width`/`height` to the `<Image>` so Astro generates the right `srcset`.
- Layout shift from images loading after text → ensure intrinsic aspect ratio is set.

- [ ] **Step 3: Fix any regressions; commit**

```bash
git add -A
git commit -m "fix(perf): address Lighthouse regressions after content import"
git push
```

**Phase 2 checkpoint.** Pause-and-review point. `new.mattiheino.com` now serves all real content. Resume at Task 20 for the MSM recovery.

---

## Phase 4 — MSM Wayback recovery (DRAFTS only)

Recovers 12 MSM posts from Wayback into `src/content/applied-musings/` as `draft: true`. Two source-specific challenges: Wayback's `im_` infix for image fetches, and a pre-cutover rescue of MSM-embedded `mattiheino.files.wordpress.com` images (must happen before Phase 3 fires).

### Task 20: `migration/msm_inventory.py` — Inventory dataclass

**Files:**
- Create: `migration/msm_inventory.py`

- [ ] **Step 1: Write the inventory**

`migration/msm_inventory.py`:
```python
"""Hard-coded MSM post inventory from the design spec §8.

13 entries in total: 12 recoverable + 1 (aloittaminen) skip.
"""
from __future__ import annotations

from dataclasses import dataclass
from datetime import date


@dataclass(frozen=True)
class MSMPost:
    slug: str
    title: str
    lang: str          # "en" | "fi"
    published: date
    notes: str = ""


INVENTORY: list[MSMPost] = [
    MSMPost("aloittaminen", "Muutostekniikat: Mitä haluan muuttaa?", "fi", date(2020, 1, 1),
            notes="No individual Wayback snapshot — handled out-of-band"),
    MSMPost("safe-changes",
            "Changing something while not making it worse: 7 rules of thumb",
            "en", date(2020, 1, 1)),
    MSMPost("motivaatio-on-tietolahde",
            "Muutostekniikat: Motivaatio on tietolähde", "fi", date(2020, 1, 7)),
    MSMPost("tekniikkalistaus", "123 tekniikkaa itsensä johtamiseen",
            "fi", date(2020, 1, 7)),
    MSMPost("antihauras", "Antihauras elämä", "fi", date(2020, 2, 11)),
    MSMPost("123-techniques", "123 techniques for self-management",
            "en", date(2020, 3, 1)),
    MSMPost("mindfulness-face",
            "Mindfulness for burning cities and viral pandemics",
            "en", date(2020, 3, 1)),
    MSMPost("decline-handshake", "How to decline a handshake",
            "en", date(2020, 3, 12)),
    MSMPost("itseohjautuvuus",
            "Itseohjautuvat kansalaiset, kriisinkestävä yhteiskunta",
            "fi", date(2020, 8, 18)),
    MSMPost("uncertainty",
            "When uncertainty makes decisions easier, not harder",
            "en", date(2020, 9, 15)),
    MSMPost("valmius",
            "Pandemia haastaa ajattelumme: Neljä kompastuskiveä torjuntapolulla",
            "fi", date(2021, 3, 7)),
    MSMPost("fasting-experiment", "A 14-day Fasting Experiment",
            "en", date(2021, 9, 13)),
    MSMPost("personal-change",
            "Lifestyle change is not a willpower issue",
            "en", date(2023, 2, 14),
            notes="Reposted Helsinki University interview — try helsinki.fi first"),
]
```

- [ ] **Step 2: Commit**

```bash
git add migration/msm_inventory.py
git commit -m "feat(migration): msm_inventory.py — 13-entry hard-coded MSM post catalogue"
git push
```

### Task 21: `lib/wayback.py` — Wayback fetcher

**Files:**
- Create: `migration/lib/wayback.py`
- Create: `migration/tests/test_wayback.py` (mocked HTTP only)

- [ ] **Step 1: Write failing tests**

`migration/tests/test_wayback.py`:
```python
from unittest.mock import MagicMock, patch
import pytest

from lib.wayback import fetch_snapshot_html, fetch_image_bytes, WaybackError


@patch("lib.wayback.requests.get")
def test_fetch_snapshot_html_returns_body_on_200(mock_get):
    mock_get.return_value = MagicMock(status_code=200, text="<article>x</article>")
    html = fetch_snapshot_html("https://www.motivationselfmanagement.com/safe-changes/", "20200201123456")
    assert "<article>" in html


@patch("lib.wayback.requests.get")
def test_fetch_snapshot_html_raises_on_503(mock_get):
    mock_get.return_value = MagicMock(status_code=503, text="busy")
    with pytest.raises(WaybackError):
        fetch_snapshot_html("https://x.test/", "20200201123456")


@patch("lib.wayback.requests.get")
def test_fetch_image_bytes_uses_im_infix(mock_get):
    mock_get.return_value = MagicMock(status_code=200, content=b"\xff\xd8\xff\xd9", headers={})
    data = fetch_image_bytes("https://www.motivationselfmanagement.com/wp-content/uploads/2020/02/x.png", "20200201123456")
    assert mock_get.call_args[0][0].startswith("https://web.archive.org/web/20200201123456im_/")
    assert data.startswith(b"\xff\xd8")
```

- [ ] **Step 2: Run, confirm fail**

```bash
pytest tests/test_wayback.py -v
```

- [ ] **Step 3: Implement**

`migration/lib/wayback.py`:
```python
"""Wayback Machine fetch helpers."""
from __future__ import annotations

import time

import requests


class WaybackError(RuntimeError):
    pass


_HTML_TPL = "https://web.archive.org/web/{ts}/{url}"
_IMG_TPL = "https://web.archive.org/web/{ts}im_/{url}"
_UA = {"User-Agent": "mattiheino-site migration/0.0.1"}


def fetch_snapshot_html(url: str, timestamp: str, *, retries: int = 3, backoff: float = 1.5) -> str:
    """GET a Wayback HTML snapshot; retry on transient errors."""
    last = None
    for attempt in range(retries):
        r = requests.get(_HTML_TPL.format(ts=timestamp, url=url), headers=_UA, timeout=30)
        if r.status_code == 200:
            return r.text
        last = r
        time.sleep(backoff ** attempt)
    raise WaybackError(f"Wayback returned {last.status_code} for {url} @ {timestamp}")


def fetch_image_bytes(url: str, timestamp: str, *, retries: int = 3, backoff: float = 1.5) -> bytes:
    """GET an image via the Wayback 'im_' infix (returns the raw bytes, not a wrapped HTML page)."""
    last = None
    for attempt in range(retries):
        r = requests.get(_IMG_TPL.format(ts=timestamp, url=url), headers=_UA, timeout=30)
        if r.status_code == 200:
            return r.content
        last = r
        time.sleep(backoff ** attempt)
    raise WaybackError(f"Wayback returned {last.status_code} for image {url} @ {timestamp}")
```

- [ ] **Step 4: Run, confirm pass**

```bash
pytest tests/test_wayback.py -v
```

- [ ] **Step 5: Commit**

```bash
git add migration/lib/wayback.py migration/tests/test_wayback.py
git commit -m "feat(migration): wayback.py — HTML + im_-infix image fetchers with retry/backoff"
git push
```

### Task 22: `import_msm.py` — MSM import pipeline

**Files:**
- Create: `migration/import_msm.py`
- Create: `migration/msm_cdx_cache.txt` (manually exported from the Wayback CDX query)

- [ ] **Step 1: Refresh the CDX list**

Run (manual, anywhere with curl):
```bash
curl -s "http://web.archive.org/cdx/search/cdx?url=motivationselfmanagement.com/*&output=text&fl=original,timestamp,statuscode&collapse=urlkey" > migration/msm_cdx_cache.txt
wc -l migration/msm_cdx_cache.txt
```

Expected: ~150-300 lines. If 0, debug the URL.

- [ ] **Step 1.5: Manual pre-step — `personal-change` Helsinki cross-check (per spec §8.4)**

Before running `import_msm.py`, search `helsinki.fi` (and the Helsinki University News site) for the original interview that became the MSM `personal-change` post. Plausible search queries:
- `site:helsinki.fi "Matti Heino" lifestyle change`
- `site:helsinki.fi käyttäytymismuutos haastattelu`

If found and the page is live:
1. Save the canonical URL to `migration/personal-change-source.txt` (one line).
2. After `import_msm.py` runs, manually edit the resulting `applied-musings/2023-02-14-personal-change.md` to replace the recovered Wayback body with the cleaner Helsinki version, citing the URL in the frontmatter `migration_notes` field.

If not found, the script's Wayback recovery is the authoritative source — no further action.

- [ ] **Step 2: Write `migration/import_msm.py`**

```python
"""Wayback recovery of motivationselfmanagement.com posts.

Reads:
  - migration/msm_inventory.py  (the 13-entry inventory)
  - migration/msm_cdx_cache.txt (latest CDX dump)

Writes (per recoverable post):
  - src/content/applied-musings/YYYY-MM-DD-<slug>.md (draft: true)
  - src/content/applied-musings/images/<slug>/*

Skips 'aloittaminen' with a note in migration/aloittaminen-decision.md.
"""
from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path
from urllib.parse import urlparse

from lxml import html as lhtml

from lib.html_to_md import sweep_shortcodes, to_markdown
from lib.images import (
    GDRIVE_FOLDER, MEDIA_ROOT, build_gdrive_index, build_media_index, rehost,
)
from lib.slug import normalise_slug
from lib.wayback import WaybackError, fetch_image_bytes, fetch_snapshot_html
from msm_inventory import INVENTORY, MSMPost


REPO_ROOT = Path(__file__).parent.parent
CDX_PATH = REPO_ROOT / "migration" / "msm_cdx_cache.txt"
CONTENT_ROOT = REPO_ROOT / "src" / "content" / "applied-musings"
ALOITTAMINEN_NOTE = REPO_ROOT / "migration" / "aloittaminen-decision.md"


def _best_snapshot_ts(cdx_lines: list[str], post_url: str) -> str | None:
    """Pick the latest status=200 snapshot for a given URL."""
    candidates = []
    for line in cdx_lines:
        parts = line.strip().split()
        if len(parts) < 3:
            continue
        original, timestamp, status = parts[0], parts[1], parts[2]
        if status != "200":
            continue
        if post_url not in original:
            continue
        candidates.append(timestamp)
    return max(candidates) if candidates else None


def _extract_article(html: str) -> str:
    """Pull the <article> body from a Wayback snapshot."""
    tree = lhtml.fromstring(html)
    art = tree.xpath("//article")
    if not art:
        # Some themes wrap in <div class="entry-content">
        art = tree.xpath("//*[contains(@class, 'entry-content')]")
    if not art:
        raise RuntimeError("No <article> in snapshot")
    # Render the first match back to HTML
    return lhtml.tostring(art[0], encoding="unicode")


def _frontmatter(post: MSMPost) -> str:
    parts = [
        "---",
        f'title: "{post.title.replace(chr(34), chr(39))}"',
        f'description: "{post.title}"',
        f"published: {post.published.isoformat()}",
        f"lang: {post.lang}",
        "vetting_status: pending",
        "migration_source: motivationselfmanagement",
        "draft: true",
        f"msm_slug: \"{post.slug}\"",
        "tags: []",
        "---",
        "",
    ]
    return "\n".join(parts)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()

    cdx = CDX_PATH.read_text(encoding="utf-8").splitlines()
    media_index = build_media_index(REPO_ROOT / MEDIA_ROOT)
    gdrive_index = build_gdrive_index(GDRIVE_FOLDER)

    counts = {"ok": 0, "skipped": 0, "failed": 0, "images_ok": 0, "images_lost": 0}

    for post in INVENTORY:
        if post.slug == "aloittaminen":
            counts["skipped"] += 1
            if not args.dry_run:
                ALOITTAMINEN_NOTE.write_text(
                    "# `aloittaminen` decision pending\n\n"
                    "No individual Wayback snapshot. Options:\n"
                    "- Reconstruct from /blog/ index excerpt.\n"
                    "- Skip entirely (redirect to /applied-musings/).\n",
                    encoding="utf-8",
                )
            print(f"  skip  {post.slug}  (no individual Wayback snapshot)")
            continue

        url = f"https://www.motivationselfmanagement.com/{post.slug}/"
        ts = _best_snapshot_ts(cdx, url)
        if ts is None:
            counts["failed"] += 1
            print(f"  fail  {post.slug}  (no Wayback 200 snapshot)")
            continue

        try:
            html_doc = fetch_snapshot_html(url, ts)
            article_html = _extract_article(html_doc)
        except (WaybackError, RuntimeError) as e:
            counts["failed"] += 1
            print(f"  fail  {post.slug}  ({e})")
            continue

        new_slug = normalise_slug(post.slug)
        out_path = CONTENT_ROOT / f"{post.published.isoformat()}-{new_slug}.md"
        images_dir = CONTENT_ROOT / "images" / new_slug

        body_html = sweep_shortcodes(article_html)

        # Rehost images: WP-CDN refs via local tar; Wayback im_ for MSM uploads;
        # external dead → placeholder.
        IMG_RE = re.compile(r'<img[^>]+src=["\']([^"\']+)["\']', re.IGNORECASE)
        for i, m in enumerate(IMG_RE.finditer(body_html), start=1):
            src = m.group(1)
            # Strip Wayback URL prefix if present in the snapshot's HTML
            src_clean = re.sub(r"^https?://web\.archive\.org/web/\d+/", "", src)

            if "motivationselfmanagement.com/wp-content/uploads/" in src_clean:
                # Wayback im_ infix for MSM uploads
                try:
                    data = fetch_image_bytes(src_clean, ts)
                    name = Path(urlparse(src_clean).path).name
                    images_dir.mkdir(parents=True, exist_ok=True)
                    outpath = images_dir / name
                    if not args.dry_run:
                        outpath.write_bytes(data)
                    body_html = body_html.replace(src, f"./images/{new_slug}/{name}", 1)
                    counts["images_ok"] += 1
                except WaybackError:
                    body_html = body_html.replace(m.group(0), f"<!-- IMAGE LOST: {src_clean} -->", 1)
                    counts["images_lost"] += 1
                continue

            # mattiheino.files.wordpress.com refs → local tar
            result = rehost(
                src_clean, slug=new_slug, dest=images_dir,
                media_index=media_index, gdrive_index=gdrive_index,
            )
            if result.status == "ok":
                body_html = body_html.replace(src, f"./images/{new_slug}/{result.local_path.name}", 1)
                counts["images_ok"] += 1
            else:
                body_html = body_html.replace(m.group(0), f"<!-- IMAGE LOST: {src_clean} -->", 1)
                counts["images_lost"] += 1

        body_md = to_markdown(body_html)
        full = _frontmatter(post) + body_md.strip() + "\n"

        if not args.dry_run:
            out_path.parent.mkdir(parents=True, exist_ok=True)
            out_path.write_text(full, encoding="utf-8")
        counts["ok"] += 1
        print(f"  ok    {post.slug}")

    print("\n=== import_msm.py summary ===")
    for k, v in counts.items():
        print(f"  {k:14s} {v}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
```

- [ ] **Step 3: Dry-run**

```bash
cd migration
.venv\Scripts\activate
python import_msm.py --dry-run
```

Expected: 12 ok + 1 skipped + 0 failed. If any "fail", check the CDX cache contains 200-status entries for that slug.

- [ ] **Step 4: Real run**

```bash
python import_msm.py
```

Expected: same counts; files appear under `src/content/applied-musings/`.

- [ ] **Step 5: Build + smoke**

```bash
cd C:/Users/qn353/Documents/git-projects/mattiheino-site
npm run build 2>&1 | tail -20
```

Expected: build succeeds. Spot-check `dist/applied-musings/` — should NOT contain any of the new MSM slugs (they're drafts). Should contain only the placeholder applied-musings from before.

- [ ] **Step 6: Commit**

```bash
git add migration/import_msm.py migration/msm_cdx_cache.txt migration/aloittaminen-decision.md src/content/applied-musings
git commit -m "feat(content): recover 12 MSM posts via Wayback as draft applied-musings

aloittaminen skipped (no individual snapshot; decision pending — see
migration/aloittaminen-decision.md).

All posts land draft: true; not visible to readers. Vetting flow B (per
spec §10.2) flips them live one at a time."
git push
```

### Task 23: Update `vetting-queue.astro` to split by source

**Files:**
- Modify: `src/pages/vetting-queue.astro`

- [ ] **Step 1: Replace the body**

Replace the current `src/pages/vetting-queue.astro` with:

```astro
---
import Base from '../layouts/Base.astro';
import { pendingAll } from '../lib/collections';

const all = await pendingAll();

const wpPending = all.filter(
  (e) => e.data.migration_source === 'mattiheino-wp' && !e.data.draft
);
const wpDrafts = all.filter(
  (e) => e.data.migration_source === 'mattiheino-wp' && e.data.draft
);
const msmDrafts = all.filter(
  (e) => e.data.migration_source === 'motivationselfmanagement' && e.data.draft
);

const fmt = (d: Date) =>
  d.toLocaleDateString('en-GB', { year: 'numeric', month: 'long', day: 'numeric' });
---
<Base title="Vetting queue (internal) – Matti T.J. Heino" noindex={true}>
  <h1>Vetting queue</h1>
  <p>
    Internal backlog &ndash; not linked publicly, excluded from sitemap and
    search engines.
  </p>

  <h2>mattiheino-wp — pending re-vet ({wpPending.length})</h2>
  <p>Already visible to readers. Vetting drives the social repost trigger.</p>
  <ul class="post-list">
    {wpPending.map((e) => (
      <li>
        <strong>{e.data.title}</strong>
        {e.data.lang === 'fi' && <span class="lang-tag">FI</span>}
        <p class="meta">{e.collection} &middot; published {fmt(e.data.published)}</p>
      </li>
    ))}
  </ul>

  <h2>mattiheino-wp drafts ({wpDrafts.length})</h2>
  <p>WordPress drafts + the three imported pages from §6.5 of the spec.</p>
  <ul class="post-list">
    {wpDrafts.map((e) => (
      <li>
        <strong>{e.data.title}</strong>
        {e.data.lang === 'fi' && <span class="lang-tag">FI</span>}
        <p class="meta">{e.collection} &middot; published {fmt(e.data.published)}</p>
      </li>
    ))}
  </ul>

  <h2>MSM drafts ({msmDrafts.length})</h2>
  <p>
    Hidden from readers until you flip <code>draft: false</code> + run
    <code>npm run sync:msm-redirects</code>.
  </p>
  <ul class="post-list">
    {msmDrafts.map((e) => (
      <li>
        <strong>{e.data.title}</strong>
        {e.data.lang === 'fi' && <span class="lang-tag">FI</span>}
        <p class="meta">applied-musings &middot; published {fmt(e.data.published)}</p>
      </li>
    ))}
  </ul>
</Base>
```

- [ ] **Step 2: Build + open in browser**

```bash
npm run build && npm run preview
```

Open `http://localhost:4321/vetting-queue/`. Confirm three sections each with realistic counts.

- [ ] **Step 3: Commit**

```bash
git add src/pages/vetting-queue.astro
git commit -m "feat(vetting): split vetting-queue into three sections by source/draft state"
git push
```

### Task 24: `scripts/check-msm-drafts.mjs` + prebuild wiring

**Files:**
- Create: `scripts/check-msm-drafts.mjs`
- Modify: `package.json` (add `prebuild` script)

- [ ] **Step 1: Write `scripts/check-msm-drafts.mjs`**

```js
// Print one-line MSM publish-state summary at every build.
// Does not fail the build.
import { readdirSync, readFileSync } from "node:fs";
import { join } from "node:path";

const dir = "src/content/applied-musings";
const files = readdirSync(dir).filter((f) => f.endsWith(".md"));

let total = 0;
let live = 0;
const liveSlugs = [];

for (const f of files) {
  const body = readFileSync(join(dir, f), "utf8");
  const fm = body.split("---")[1] ?? "";
  if (!fm.includes("migration_source: motivationselfmanagement")) continue;
  total++;
  const draft = /^draft:\s*(true|false)/m.exec(fm)?.[1] ?? "true";
  if (draft === "false") {
    live++;
    liveSlugs.push(f.replace(/\.md$/, ""));
  }
}

console.log(`MSM recovered: ${total}. Currently drafts: ${total - live}. Live: ${live}.`);
if (liveSlugs.length) {
  console.log("  Live MSM slugs:");
  for (const s of liveSlugs) console.log(`    - ${s}`);
}
```

- [ ] **Step 2: Wire as `prebuild` in `package.json`**

In `package.json`, add to `scripts`:
```json
"prebuild": "node scripts/check-msm-drafts.mjs",
```

- [ ] **Step 3: Verify the prebuild fires**

```bash
npm run build 2>&1 | head -3
```

Expected: first line of output is the MSM summary.

- [ ] **Step 4: Commit**

```bash
git add scripts/check-msm-drafts.mjs package.json
git commit -m "chore(build): prebuild script — MSM draft/live count visible at every build"
git push
```

**Phase 4 checkpoint.** MSM content recovered + queued + invisible to readers. Pause-and-review point.

---

## Phase 3 — DNS cutover (`mattiheino.com`)

Small but high-stakes. Pre-flight tests RSS GUID continuity; DNS swap proper; verification.

### Task 25: Pre-flight — subscribe to new.mattiheino.com RSS in Feedly + Inoreader

**Files:** none.

- [ ] **Step 1: Subscribe in Feedly**

Open Feedly. Add subscription: `https://new.mattiheino.com/all.xml`. Confirm the feed loads with the latest posts.

- [ ] **Step 2: Subscribe in Inoreader**

Same in Inoreader: `https://new.mattiheino.com/all.xml`.

- [ ] **Step 3: Quietly verify GUID values**

```bash
curl -s https://new.mattiheino.com/all.xml | grep -A0 '<guid' | head -10
```

Each `<guid isPermaLink="false">...</guid>` should be a WP-style `<guid>` from the original export (e.g. `https://mattiheino.com/?p=1234`), not a new canonical URL.

If they are canonical URLs, the wp_guid wiring didn't take. Debug Task 6 before proceeding.

- [ ] **Step 4: Wait 24 hours, confirm no new items appear in either reader**

Feedly and Inoreader treat matching GUIDs as already-seen. If new items appear, the GUIDs don't match the WP feed — diagnose before doing the DNS swap.

### Task 26: DNS swap

**Files:** none (Cloudflare-side).

- [ ] **Step 1: Update Cloudflare DNS**

Cloudflare dashboard → DNS for `mattiheino.com`:
1. Locate the existing CNAME / A record for `mattiheino.com` apex pointing at WordPress.com.
2. Edit to point at CF Pages (the dashboard offers the Pages target as a suggestion when you start typing).
3. Same for `www.mattiheino.com` (or, alternatively, set up a Page Rule redirecting `www → apex`).
4. Save.

Expected: propagation within seconds (Cloudflare proxied).

- [ ] **Step 2: Smoke-test**

```bash
curl -sI https://mattiheino.com/ | head -10
curl -sI https://www.mattiheino.com/ | head -10
curl -sI https://mattiheino.com/posts/<known-slug>/ | head -10
```

Expected: `mattiheino.com/` returns 200 from Cloudflare; `www.mattiheino.com/` returns 301 → apex.

- [ ] **Step 3: Verify RSS via the production URL**

Subscribe to `https://mattiheino.com/all.xml` in a third feed reader (or use feedvalidator.org). Confirm no new items appear in the next 24 hours.

### Task 27: Submit new sitemap to Google Search Console + clean up `new.mattiheino.com`

**Files:** none.

- [ ] **Step 1: Submit sitemap**

Search Console → Sitemaps → Add a new sitemap → `https://mattiheino.com/sitemap-index.xml`. Submit.

Leave the existing WordPress sitemap (`/sitemap.xml`) submitted in parallel for 6 weeks.

- [ ] **Step 2: Remove `new.mattiheino.com` domain from CF Pages project**

Pages project → Custom domains → `new.mattiheino.com` → Remove.

Cloudflare DNS: remove the `new` CNAME.

- [ ] **Step 3: Commit a note**

```bash
cat <<EOF > docs/handovers/2026-MM-DD-mattiheino-cutover.md
# mattiheino.com cutover

Date: <today>
new.mattiheino.com removed. mattiheino.com is now served by Cloudflare Pages.
WordPress.com left at its previous state (DNS no longer points at it). Old WP
admin still accessible via wordpress.com dashboard if needed.
EOF
git add docs/handovers/
git commit -m "docs: mattiheino.com cutover handover note"
git push
```

**Phase 3 checkpoint.** Live site is now on the new infrastructure. Pause-and-review.

---

## Phase 5 — `motivationselfmanagement.com` redirects

Adds the second custom domain to the CF Pages project, emits a fallback-only `_redirects` rule, sets up the per-URL append helper for future use.

### Task 28: Add `motivationselfmanagement.com` as custom domain on CF Pages

**Files:** none (Cloudflare-side).

- [ ] **Step 1: Add to Pages project**

Pages project → Custom domains → Set up → `motivationselfmanagement.com`. Cloudflare prompts to add the DNS records; confirm.

Expected: domain active in 1-3 min. `https://motivationselfmanagement.com/` resolves and serves the mattiheino.com site (no redirects in place yet).

### Task 29: Initial fallback rule in `_redirects`

**Files:**
- Modify: `public/_redirects`

- [ ] **Step 1: Add MSM fallback rules above any existing WP redirect block**

Edit `public/_redirects`. Add at the top:
```
# === BEGIN MSM PER-URL (auto-generated by sync-msm-redirects.mjs) ===
# (none yet)
# === END MSM PER-URL ===

# MSM fallback — catch-all (always last for MSM)
https://motivationselfmanagement.com/*       https://mattiheino.com/applied-musings/  301
https://www.motivationselfmanagement.com/*   https://mattiheino.com/applied-musings/  301

```

- [ ] **Step 2: Build + verify**

```bash
npm run build
cat dist/_redirects | head -10
```

The block should appear in the build output.

- [ ] **Step 3: Push, wait for CF Pages deploy, verify**

```bash
git add public/_redirects
git commit -m "feat(redirects): MSM fallback catch-all to /applied-musings/ index

Per-URL rules will append themselves above this block via
sync-msm-redirects.mjs as MSM posts are vetted and published."
git push
```

After deploy:
```bash
curl -sI https://motivationselfmanagement.com/random-test-path/ | head -8
curl -sI https://motivationselfmanagement.com/safe-changes/ | head -8
```

Expected: both 301 to `https://mattiheino.com/applied-musings/`.

### Task 30: `scripts/sync-msm-redirects.mjs` — per-URL rule generator

**Files:**
- Create: `scripts/sync-msm-redirects.mjs`
- Modify: `package.json` (add `sync:msm-redirects` script)

- [ ] **Step 1: Write `scripts/sync-msm-redirects.mjs`**

```js
// Walk applied-musings/. For every entry with
//   migration_source: motivationselfmanagement
//   draft: false
// emit a per-URL 301 from /<msm_slug>/ → /applied-musings/<new-slug>/.
//
// Rebuilds the per-URL block (between sentinel comments) in public/_redirects
// without touching anything outside that block.

import { readdirSync, readFileSync, writeFileSync } from "node:fs";
import { join } from "node:path";

const dir = "src/content/applied-musings";
const redirectsPath = "public/_redirects";

const rules = [];
for (const f of readdirSync(dir)) {
  if (!f.endsWith(".md")) continue;
  const body = readFileSync(join(dir, f), "utf8");
  const fm = body.split("---")[1] ?? "";
  if (!fm.includes("migration_source: motivationselfmanagement")) continue;
  if (!/^draft:\s*false\b/m.test(fm)) continue;
  const msmSlug = /^msm_slug:\s*"?([^"\n]+)"?/m.exec(fm)?.[1];
  if (!msmSlug) {
    console.warn(`  WARN: ${f} is live but has no msm_slug; skipping`);
    continue;
  }
  // New slug = filename minus YYYY-MM-DD- prefix
  const newSlug = f.replace(/^\d{4}-\d{2}-\d{2}-/, "").replace(/\.md$/, "");
  rules.push(`https://motivationselfmanagement.com/${msmSlug}/       https://mattiheino.com/applied-musings/${newSlug}/  301`);
  rules.push(`https://www.motivationselfmanagement.com/${msmSlug}/   https://mattiheino.com/applied-musings/${newSlug}/  301`);
}

const block = [
  "# === BEGIN MSM PER-URL (auto-generated by sync-msm-redirects.mjs) ===",
  rules.length ? rules.join("\n") : "# (none yet)",
  "# === END MSM PER-URL ===",
].join("\n");

const current = readFileSync(redirectsPath, "utf8");
const next = current.replace(
  /# === BEGIN MSM PER-URL[\s\S]*?# === END MSM PER-URL ===/m,
  block,
);
writeFileSync(redirectsPath, next, "utf8");
console.log(`MSM redirects: ${rules.length / 2} live (${rules.length} lines emitted).`);
```

- [ ] **Step 2: Wire as `sync:msm-redirects` in package.json**

In `package.json`:
```json
"sync:msm-redirects": "node scripts/sync-msm-redirects.mjs"
```

- [ ] **Step 3: Smoke-test (no MSM posts live yet → should emit "(none yet)")**

```bash
npm run sync:msm-redirects
cat public/_redirects | head -10
```

Expected: "0 live (0 lines emitted)" + the sentinel block shows `# (none yet)`.

- [ ] **Step 4: Commit**

```bash
git add scripts/sync-msm-redirects.mjs package.json public/_redirects
git commit -m "feat(redirects): sync-msm-redirects.mjs — auto-generated per-URL block

Walks applied-musings/, picks live MSM posts, rewrites the per-URL block
between sentinel comments. Run manually after vetting + flipping draft:false."
git push
```

**Phase 5 checkpoint.** Build complete. Pause-and-review.

---

## Self-review checklist (run after all tasks executed)

- [ ] All 5 phases have working `curl -sI` smoke tests passing.
- [ ] Lighthouse 95+ on three pages.
- [ ] `https://mattiheino.com/all.xml` validates at validator.w3.org.
- [ ] No Feedly / Inoreader subscriber sees re-broadcast posts.
- [ ] `/vetting-queue/` shows realistic counts in all three sections.
- [ ] `npm run build` prints the MSM count line.
- [ ] `npm run sync:msm-redirects` is idempotent on a clean tree.
- [ ] Every commit message uses `feat:` / `fix:` / `chore:` / `docs:` prefix.
- [ ] No file in `dist/` is in git (`.gitignore` working).
- [ ] No file in `migration/source/` is in git.

---

## After this plan

- **Phase 6 (cross-poster Worker)** — own design + plan, when ready.
- **Vetting backlog work** — Flow A and Flow B (per spec §10), Matti runs over time.
- **WP.com subscriber migration to Listmonk** — one-off task, separate doc.
- **About page v2** — separate task.
