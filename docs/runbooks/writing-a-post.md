# Writing a post (with images) on mattiheino.com

**What this does:** takes you from "I want to write something" to "it is live on
mattiheino.com". Everything here was tested against this repo on 2026-07-16 – the image
steps are not guesswork, they were built and the output inspected.

**The short version:** a post is one Markdown file. Its images sit in a folder next to it.
You push to `main` and Cloudflare builds the site for you. There is no admin login, no
"upload media" button. The files *are* the blog.

---

## Where things go

| Thing | Where |
|---|---|
| A rigorous post | `src/content/posts/YYYY-MM-DD-slug.md` |
| An applied musing | `src/content/applied-musings/YYYY-MM-DD-slug.md` |
| That post's images | `src/content/posts/images/slug/` (note: **no date** in the image folder) |
| Downloadable files (PDF, pptx, xlsx) | `public/files/` |

The date in the filename is stripped to make the URL. So
`src/content/posts/2026-07-16-ladders.md` becomes `https://mattiheino.com/posts/ladders/`.
The date is only there so the folder lists in order.

---

## Step 1 – make the two things

1. Create the Markdown file, e.g. `src/content/posts/2026-07-16-ladders.md`.
2. Create its image folder, e.g. `src/content/posts/images/ladders/`, and drop your
   pictures in. Name them something you will recognise (`ladder-cascade.png`), not
   `image-4.png`.

Keep the image-folder name identical to the slug – the part of the filename after the date.
Nothing enforces this; it is just how every existing post is arranged, and you will lose
track otherwise.

---

## Step 2 – the frontmatter

The block at the top between `---` lines. Copy this and edit it:

```yaml
---
title: "Your title here"
description: "One sentence. This shows in the library list and in search results."
published: 2026-07-16
lang: en
vetting_status: done
vetted_on: 2026-07-16
migration_source: native
draft: false
tags: ['preparedness', 'complexity']
---
```

Only `title`, `description` and `published` are genuinely required. The rest have defaults,
but two of those defaults are wrong for a post you write today:

- **`vetting_status`** defaults to `pending`, which is a backlog flag for old imported
  posts you have not re-read yet. Leave it at `pending` and your brand-new post shows up in
  your internal vetting queue at `/vetting-queue`, asking you to check work you just wrote.
  Set it to `done`.
- **`migration_source`** defaults to `native`, which is correct for you. Only the old
  WordPress and motivationselfmanagement imports set it to something else. Leave it alone.

`lang` is `en` or `fi`. It drives which newsletter call-to-action appears at the foot.

**`draft: true` hides the post from the public site completely** – no page, no library
entry, no RSS. This is your safety net: you can push a half-finished post to `main` and
nobody sees it. Flip it to `false` when you want it out.

On your own machine the preview server (Step 4) **does** show drafts, so you can watch the
post take shape while it stays hidden from the world. (Added 2026-07-17 in the two
`[...slug].astro` page files; verified that a draft renders locally and is absent from the
built site, the sitemap, and RSS.)

---

## Step 3 – images

There are two routes, and they behave differently. Both were verified on 2026-07-16.

### Route A – a picture inside the text (the normal one)

Plain Markdown, with a relative path starting `./`:

```markdown
![Ladders tied together with rope, all leaning on one wall](./images/ladders/ladder-cascade.png)
```

The text in the square brackets is the **alt text** – what a blind reader hears and what
shows if the image fails to load. Write a real sentence there. Almost every imported
WordPress post has empty alt text (`![]`), which is an accessibility hole you inherited;
do not copy that habit into new work.

Astro converts the file to WebP and gives it a hashed name automatically. You do not
optimise anything by hand, and you never write an `<img>` tag.

### Route B – a hero image under the title

Add this to the frontmatter instead:

```yaml
hero:
  src: ./images/ladders/ladder-cascade.png
  alt: "Ladders tied together with rope, all leaning on one wall"
  prompt: "optional – the AI prompt you used to make it, for your own records"
```

It renders below the title and above the body text, and it becomes the post's share card –
the picture WhatsApp and LinkedIn show when someone pastes the link. **No post uses this
yet** – you are first. It works; it was built and checked. (The field was called
`infographic` until 2026-07-19; renamed before any post used it.)

### Which to use

Route B is technically better: it emits three sizes (480, 800 and 1200 pixels wide) and the
browser picks the one it needs. Route A emits a single WebP at the image's full size, so a
2400-pixel-wide screenshot ships at 2400 pixels to a phone. It still works and it still gets
compressed – it is just heavier than it needs to be.

Practical rule: **shrink big pictures to about 1600 pixels wide before you put them in the
folder.** Some existing images are near 5 MB; the build now warns about any file over 1 MB
in a native post.

**The share card picks itself, WordPress-style.** Every post's share picture is chosen in
this order: the `hero` if you set one, else the first picture in the post body, else the
site portrait. So a post with any decent image advertises itself with no extra work.
Pictures under 400 px wide are skipped (icons make bad cards), GIFs are skipped, and the
card is served as JPG because LinkedIn's link reader handles WebP unreliably. Old imported
posts with images get their cards too – verified on built pages 2026-07-19.

---

## Step 4 – write with a live preview

This is the closest thing this site has to WYSIWYG, and it is faithful in a way no
Markdown editor can be: the preview **is** the real site – same fonts, same layout, same
image handling.

Set up two windows side by side:

1. **Left half:** your editor (Positron), with the post's `.md` file open.
2. **Right half:** a browser. In a terminal, run:

```powershell
cd C:\Users\qn353\Documents\git-projects\mattiheino-site
npm run dev
```

then open `http://localhost:4321/posts/ladders/` (your slug, no date). If the terminal
says a different port (it picks the next free one when 4321 is busy), use that.

Now just write. Every save shows up in the browser in about two seconds, without you
touching anything – verified 2026-07-17 by editing a post mid-session and watching the
served page change. Drafts (`draft: true`) are visible here too, but you must type the
URL yourself; the library list still hides them.

Things that do **not** work in the local preview:

- **The search box.** Search is built after the site is compiled, so it only works on the
  deployed site.
- **Finding drafts by browsing.** Type the post URL directly.

Stop the server with Ctrl+C in the terminal when you are done.

**Quick alternative while drafting:** Positron/VS Code's built-in Markdown preview
(Ctrl+Shift+V) renders the text and the relative image paths instantly, but with generic
styling and no frontmatter handling – fine for structure, not for judging the final look.
**Avoid MarkText for these files:** it rewrites Markdown on save (reformats lists, has
dropped lines), which silently corrupts posts.

---

## Step 5 – publish

Cloudflare Pages watches the `main` branch of `github.com/heinonmatti/mattiheino-site`.
Pushing to `main` **is** publishing. There is no separate deploy button.

```powershell
cd C:\Users\qn353\Documents\git-projects\mattiheino-site
npm run build      # optional, but catches errors before the world sees them
git add src/content/posts/2026-07-16-ladders.md src/content/posts/images/ladders
git commit -m "post: ladders and cascade risk"
git push
```

The build takes roughly two minutes, then the post is live. If the build fails, Cloudflare
keeps serving the previous version – a broken push cannot take the site down.

> This repo has a real remote, unlike your other projects. A push here is public.

---

## Known limits – things that will not do what you expect

- **The cross-poster does not exist.** `social_status: queued` does nothing – there is no
  automation behind it, and sharing is manual. Feasibility was scoped 2026-07-18 (short
  verdict: full LinkedIn automation is not worth it, a paste-ready blurb would be; Bluesky
  is trivial if ever wanted). The scoping doc lives in the personal-assistant wiki under
  `projects/Personal/mattiheino-site/threads/`. Parked until Matti reopens it.
- **The image checker guards native posts only.** Every build errors on empty alt text and
  on image references that point at nothing, and warns on files over 1 MB or an image
  folder that does not match the slug – but only for posts with `migration_source: native`.
  The old imports' empty alts stay as invisible backlog, on purpose, so warnings about the
  past do not drown problems in what you write today.

---

*Verified 2026-07-16 by building a throwaway post that used both image routes and reading
the generated HTML; preview workflow verified 2026-07-17 by running the dev server against
a throwaway draft (renders locally with image, updates on save in ~2 s, absent from the
production build, sitemap and RSS). Hero rename, share-card chain and the image checker
verified 2026-07-19 the same way: throwaway posts built, generated pages read, the checker
made to stop a build over an empty alt text, then all test artefacts deleted. Related:
`dns-cutover.md` (how the domain got here),
`docs/superpowers/plans/2026-05-30-mattiheino-full-build-plan.md` (why the site is shaped
this way).*
