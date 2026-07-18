# DNS cutover runbook – launching mattiheino.com on Cloudflare Pages

> **Do not run any DNS step without Matti's explicit go-ahead.** This document is the
> checklist; it does not authorise the launch. Reading it changes nothing.

**What this does:** moves the live `mattiheino.com` from WordPress.com to the new Astro
site on Cloudflare Pages. After it, visitors to `mattiheino.com` see the new site.

**Who does what:** the DNS steps happen in the **Cloudflare dashboard** (Matti clicks).
The verification steps are PowerShell commands the assistant can run for you.

**How long:** the swap itself is a few minutes. Because the domain is already proxied
through Cloudflare, the change takes effect in **seconds**, and so does a rollback.

---

## Why this is low-risk (verified 2026-06-07)

Before writing this, the assistant checked the live sites. All green:

| Check | Result | Why it matters |
|---|---|---|
| RSS GUID continuity | **10 of 10** live WordPress-feed GUIDs appear verbatim in the new feed, all `http://…/?p=N` | At cutover, feed readers see every current post as already-seen. **No mass re-broadcast to subscribers** – the single worst failure mode is already handled. |
| Staging health | `new.mattiheino.com/` → 200 | The new site is live and serving. |
| Cutover target | `mattiheino-site.pages.dev/` → 200 | The Pages project name is `mattiheino-site`. |
| Production today | `mattiheino.com/` → 200, `server=cloudflare` | The apex is already Cloudflare-proxied, so the swap and any rollback propagate in seconds. |
| www | `www.mattiheino.com/` → 301 → apex | www→apex redirect already exists; we preserve it. |
| Old-URL protection | `/feed/ → /all.xml`, `/posts/feed/ → /posts.xml` both 301 on Pages | The `_redirects` rules that catch old WordPress URLs are live and proven on the Pages deployment. |

Old WordPress permalinks (`/2014/11/slug/` etc.) already 301 to `/posts/slug/` via
`public/_redirects`, and zero `wp-content` references remain in the site. So the "old
links 404 after cutover" landmine is gone.

---

## Phase 0 – final sign-off (no DNS change yet)

Look at `https://new.mattiheino.com/` and confirm you are happy to make it public.

- [ ] Home page looks right (portrait, welcome, English-default toggle).
- [ ] Open 3–4 posts – text, images, and any animations render. Try one Finnish post.
- [ ] `/library` loads; the topic-chip filter works.
- [ ] Search works (type a word in the search box – Pagefind only works on the deployed
      site, which `new.mattiheino.com` is).
- [ ] Open one post on your phone – check it reads well on mobile.
- [ ] The "Applied musings" register shows only what you intend (recovered MSM drafts must
      stay hidden until you vet them).

If anything is wrong, **stop** and fix it on staging first. Do not cut over a broken site.

---

## Phase 1 – RSS pre-flight (re-run on launch day)

This is the check that protects your subscribers. Re-run it immediately before the swap,
because content may have changed since 2026-06-07.

Assistant runs:

```powershell
$ProgressPreference = 'SilentlyContinue'
function Get-Guids($url) {
  $r = Invoke-WebRequest -Uri $url -UseBasicParsing -TimeoutSec 30 -Headers @{ 'User-Agent'='Mozilla/5.0 cutover-preflight' }
  [regex]::Matches($r.Content, '<guid[^>]*>(.*?)</guid>') | ForEach-Object { $_.Groups[1].Value.Trim() }
}
$new = @(Get-Guids 'https://new.mattiheino.com/all.xml')
$wp  = @(Get-Guids 'https://mattiheino.com/feed/')
$missing = @($wp | Where-Object { $new -notcontains $_ })
"WP-feed GUIDs: $($wp.Count) | present in new feed: $($wp.Count - $missing.Count)"
if ($missing.Count) { "RE-BROADCAST RISK – these WP GUIDs are missing from the new feed:"; $missing }
else { "PASS: every live WP-feed GUID is present verbatim in the new feed." }
```

- [ ] Output says **PASS**. If it lists missing GUIDs, **stop** – the `wp_guid` wiring
      regressed (see `check-rss-guids.mjs` and the guid scheme note in the build plan).
      Subscribers would get every old post pushed at them again.

---

## Phase 2 – capture the current DNS (CRITICAL – this is your rollback)

You cannot roll back to values you did not write down. Do this **before** changing anything.

In Cloudflare dashboard → select `mattiheino.com` → **DNS → Records**:

- [ ] Screenshot the whole records list.
- [ ] Write down the **apex** record (Name = `mattiheino.com` or `@`): its **Type**
      (A or CNAME), its **Content/Target** (the WordPress.com IP or hostname), and whether
      it is **Proxied (orange cloud)**.
- [ ] Write down the **www** record (Name = `www`): Type, Target, Proxied state.
- [ ] **Do not touch** MX, TXT (SPF/DKIM/DMARC), or any other record. Those carry email and
      domain verification. Changing only the apex and www records keeps email working.

> Typical WordPress.com mapped-domain values are A records to `192.0.78.x` – but **trust
> what you captured, not this note.**

---

## Phase 3 – the swap

**Recommended method – Pages "Custom domains" (guided, also issues the TLS certificate):**

- [ ] Cloudflare dashboard → **Workers & Pages → `mattiheino-site` → Custom domains**.
- [ ] **Set up a custom domain → `mattiheino.com` → Activate domain.** Cloudflare detects
      the zone is on this account and updates the apex DNS record for you, then provisions
      an SSL certificate. Wait until it shows **Active** (usually under a minute).

Alternative method (manual, the build plan's original): DNS → Records → edit the apex
record to point at `mattiheino-site.pages.dev` (proxied). Use this only if the Custom
Domains UI refuses the apex.

**www:** leave the www record as-is for now – it already 301s to the apex, and that still
works once the apex serves Pages. You will confirm and harden it in Phase 5.

---

## Phase 4 – verify immediately after the swap

Assistant runs (no redirect-following, so you see the real status codes):

```powershell
$ProgressPreference = 'SilentlyContinue'
function Probe($label,$url){
  try { $r = Invoke-WebRequest $url -UseBasicParsing -TimeoutSec 30 -MaximumRedirection 0 -Headers @{'User-Agent'='Mozilla/5.0 postcutover'}; "{0,-34} {1} server={2} {3}" -f $label,$r.StatusCode,$r.Headers['Server'],$r.Headers['Location'] }
  catch { $e=$_.Exception.Response; "{0,-34} {1} server={2} {3}" -f $label,[int]$e.StatusCode,$e.Headers['Server'],$e.Headers['Location'] }
}
Probe 'apex /'            'https://mattiheino.com/'
Probe 'apex /all.xml'     'https://mattiheino.com/all.xml'
Probe 'old WP feed /feed/' 'https://mattiheino.com/feed/'
Probe 'a known post'      'https://mattiheino.com/posts/yhteistyon-manifesti/'
Probe 'www /'             'https://www.mattiheino.com/'
```

Expect:
- [ ] `apex /` → **200**. Then open `https://mattiheino.com/` in a browser – it should be
      the **new** site, with a valid padlock (no certificate warning).
- [ ] `apex /all.xml` → **200** (the new RSS is now served from the live domain).
- [ ] `old WP feed /feed/` → **301 → /all.xml** (existing subscribers' readers follow this).
- [ ] `a known post` → **200**.
- [ ] `www /` → **301 → https://mattiheino.com/**.

If `apex /` still shows the old WordPress site, it is almost certainly **cache** – do Phase 5
cache purge, then re-check.

---

## Phase 5 – flush cache, harden www, check the edges

- [ ] **Purge cache:** Cloudflare → **Caching → Configuration → Purge Everything.** This
      drops any WordPress HTML Cloudflare had cached at the edge.
- [ ] **SSL/TLS mode:** Cloudflare → **SSL/TLS → Overview** should be **Full (strict)**.
      Pages serves a valid certificate, so strict is correct.
- [ ] **www durability (recommended):** the www→apex 301 currently works, but to stop it
      depending on WordPress.com, add a Cloudflare rule. **Rules → Redirect Rules → Create**:
      - When incoming **Hostname equals `www.mattiheino.com`**
      - Then **Static redirect** to `https://mattiheino.com${http.request.uri.path}`, status **301**.
      Re-run the www probe – still 301 → apex.
- [ ] **Social preview:** paste `https://mattiheino.com/posts/yhteistyon-manifesti/` into
      a social-card debugger (e.g. opengraph.xyz). The portrait OG image should resolve now
      that absolute URLs point at the live domain.
- [ ] **Search:** on `https://mattiheino.com/`, search a word – Pagefind should return hits.

---

## Rollback – if anything is wrong

The apex is proxied, so rollback takes effect in seconds.

1. If you used the recommended method: Cloudflare → **Workers & Pages → `mattiheino-site`
   → Custom domains → `mattiheino.com` → Remove**.
2. Cloudflare → **DNS → Records →** restore the **apex** record to exactly the Type and
   Content you captured in Phase 2 (the WordPress.com value), Proxied ON.
3. If you changed the www record, restore it too.
4. **Purge Everything** again.
5. Re-run the Phase 4 probe – `apex /` should be the old WordPress site again.

Nothing on the WordPress.com side was deleted; it keeps serving the moment DNS points back.
Your WordPress admin stays reachable at the wordpress.com dashboard throughout.

---

## Phase 6 – after a clean cutover (next day, not urgent)

- [ ] **Google Search Console:** add `https://mattiheino.com/sitemap-index.xml`. Leave the
      old WordPress sitemap submitted in parallel for ~6 weeks.
- [ ] **Retire staging:** once you are confident (give it a few days), remove the
      `new.mattiheino.com` custom domain from the Pages project and delete its `new` CNAME,
      so there is only one public copy of the site.
- [ ] **Record it:** append to `personal-assistant/decisions/log.md` –
      `[YYYY-MM-DD] DECISION: cut mattiheino.com over to Cloudflare Pages | REASONING: … | CONTEXT: …`
      and write a short handover note in `personal-assistant/docs/handovers/`.
- [ ] **MSM redirects (Phase 5 of the build plan):** only when the recovered
      motivationselfmanagement.com drafts go live. Separate task; not part of this cutover.

---

## Gotchas

- **It "didn't work" = usually cache.** If the old site lingers after the swap, Purge
  Everything and hard-refresh (Ctrl+F5). The DNS itself is instant.
- **Never touch MX / TXT records.** They carry email and domain verification. Only the apex
  and www records change.
- **Re-run the GUID pre-flight on the day**, not just trust the 2026-06-07 pass – content
  may have moved.
- **og:image / WhatsApp previews only resolve once live.** That is expected; verify
  post-cutover, not before.
- **git push from this repo** occasionally hits the MSYS2 credential-helper crash – just
  retry once or twice.

---

*Sources: build plan `docs/superpowers/plans/2026-05-30-mattiheino-full-build-plan.md`
Phase 3 (Tasks 25–27); live verification 2026-06-07; handover
`personal-assistant/docs/handovers/2026-06-07-mattiheino-wordpress-deps-removed.md`.*
