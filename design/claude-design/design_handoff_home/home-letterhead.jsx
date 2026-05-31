// home-letterhead.jsx
// Direction C — "Letterhead".
// Same brand, more characterful. The EN + FI intro blocks sit side-by-side
// as a diptych under one shared title; the language toggle dims the inactive
// side rather than swapping it. A faint paper grain. Expand opens a cream
// panel beneath the row like a pasted-in note.

const lhCss = `
  .lh { font-family: 'Inter', system-ui, sans-serif; color: var(--ink);
        background: var(--cream); font-size: var(--body-size); line-height: 1.6;
        position: relative; }
  /* Whisper of paper grain — SVG noise mixed in at very low opacity */
  .lh::before { content: ''; position: absolute; inset: 0; pointer-events: none;
        background-image: url("data:image/svg+xml;utf8,<svg xmlns='http://www.w3.org/2000/svg' width='160' height='160'><filter id='n'><feTurbulence type='fractalNoise' baseFrequency='0.85' numOctaves='2' stitchTiles='stitch'/><feColorMatrix values='0 0 0 0 0.13  0 0 0 0 0.11  0 0 0 0 0.09  0 0 0 0.18 0'/></filter><rect width='100%25' height='100%25' filter='url(%23n)'/></svg>");
        opacity: 0.55; mix-blend-mode: multiply; }
  .lh > * { position: relative; }

  /* Band: brand left, nav right. Site-section nav (Research pieces /
     Applied musings) lives below in the filter row, not here — the band
     stays formal and uncluttered. */
  .lh-band { background: var(--sky); padding: 28px 56px;
        min-height: var(--band-h); display: flex; align-items: center;
        justify-content: space-between; gap: 32px;
        border-bottom: 1px solid var(--sky-deep); position: relative; }
  .lh-band::after { content: ''; position: absolute; left: 56px; right: 56px;
        bottom: -1px; height: 1px; background: var(--ink); opacity: 0.08; }
  .lh-nav { display: flex; gap: 26px; font-size: 14px; font-weight: 500; }
  .lh-nav a { color: var(--ink); text-decoration: none; padding-bottom: 2px;
        border-bottom: 1px solid transparent; }
  .lh-nav a:hover { border-bottom-color: var(--ink); }
  .lh-brand { display: flex; align-items: center; gap: 20px;
        text-decoration: none; color: var(--ink); }
  /* Logo sits directly on the band — its sky-blue JPG ground exactly
     matches var(--sky), so the rectangle dissolves and the two heads read
     as floating on the band, no frame, no blend tricks. */
  .lh-logo { display: block; }
  .lh-marks { display: flex; flex-direction: column; align-items: flex-start;
        line-height: 1.0; }
  .lh-marks .wm { font-family: 'Newsreader', serif; font-weight: 500;
        font-size: 28px; letter-spacing: -0.004em; }
  .lh-marks .bylines { font-family: 'Newsreader', serif; font-style: italic;
        font-size: 13.5px; color: var(--ink-soft); margin-top: 7px;
        letter-spacing: 0.005em; }
  .lh-marks .bylines .en { color: var(--red); }
  .lh-marks .bylines .sep { color: var(--ink-faint); margin: 0 0.55em;
        font-style: normal; }

  .lh-main { max-width: 1080px; margin: 0 auto; padding: 56px 56px 96px; }

  /* Hero (no kicker — the blog names live in the band now). */
  .lh-hero-head { text-align: center; margin-bottom: 36px; }
  .lh-h1 { font-family: 'Newsreader', serif; font-weight: 500;
        font-size: 70px; line-height: 1.0; letter-spacing: -0.025em;
        margin: 0; color: var(--ink); }
  .lh-h1 .slash { color: var(--ink-faint); font-style: italic; font-weight: 400;
        margin: 0 0.1em; }

  .lh-diptych { display: grid; grid-template-columns: 1fr 1px 1fr;
        gap: 48px; margin-top: 8px; }
  .lh-diptych .rule { background: var(--rule); width: 1px; }
  .lh-pane { font-family: 'Newsreader', serif; font-size: 1.08em;
        line-height: 1.55; color: var(--ink); transition: opacity .2s;
        max-width: var(--measure); }
  .lh-pane[data-dim="1"] { opacity: 0.38; }
  .lh-pane .lbl { display: block; font-family: 'Inter', sans-serif;
        font-size: 11px; letter-spacing: 0.18em; text-transform: uppercase;
        color: var(--ink-faint); margin-bottom: 14px; font-weight: 600; }
  .lh-pane p { margin: 0 0 0.85em; }
  .lh-pane p:last-child { margin: 0; }
  .lh-pane a { color: var(--ink); text-decoration: underline;
        text-decoration-color: var(--red); text-decoration-thickness: 1px;
        text-underline-offset: 3px; }
  .lh-pane em { font-style: italic; color: var(--ink-soft); }

  /* Filters: two chip rows (language; then content type) between hairlines. */
  .lh-filters { margin: 56px auto 0; padding: 22px 0;
        border-top: 1px solid var(--rule); border-bottom: 1px solid var(--rule);
        max-width: 720px; display: flex; flex-direction: column;
        align-items: center; gap: 14px; }
  .lh-filter-row { display: flex; align-items: center; gap: 10px; }
  .lh-filter-lbl { font-family: 'Inter', sans-serif; font-weight: 500;
        font-size: 11px; color: var(--ink-faint); letter-spacing: 0.14em;
        text-transform: uppercase; min-width: 48px; text-align: right; }
  .lh-lang { display: flex; gap: 6px; }
  .lh-pill { font: inherit; font-size: 13.5px; font-weight: 500;
        background: transparent; color: var(--ink-soft);
        border: 1px solid var(--rule); padding: 6px 16px; border-radius: 999px;
        cursor: default; }
  .lh-pill[data-on="1"] { background: var(--red); color: var(--cream);
        border-color: var(--red); }
  .lh-fold { font: inherit; font-size: 13px; color: var(--ink-soft);
        font-family: 'Newsreader', serif; font-style: italic;
        cursor: default; display: inline-flex; align-items: center;
        background: transparent; border: 0; }
  /* Random: same quiet voice as Browse by topic, sits just below it as a
     paired action. The little die glyph reads as a typographic ornament. */
  .lh-random { font-family: 'Newsreader', serif; font-style: italic;
        font-size: 13px; color: var(--ink-soft); text-decoration: none;
        display: inline-flex; align-items: center; gap: 0.4em;
        border-bottom: 1px solid transparent; padding-bottom: 1px; }
  .lh-random:hover { color: var(--red); border-bottom-color: var(--red); }
  .lh-random-dice { font-style: normal; font-size: 16px; line-height: 1;
        color: var(--ink-faint); }
  .lh-chips { display: flex; flex-wrap: wrap; gap: 6px; justify-content: center;
        padding-top: 4px; max-width: 600px; }
  .lh-chip { font: inherit; font-size: 12.5px; color: var(--ink-soft);
        background: transparent; border: 1px solid var(--rule);
        padding: 4px 11px; border-radius: 999px; cursor: default; }

  /* List */
  .lh-list { list-style: none; padding: 0;
        margin: 56px auto 0; max-width: 860px; }
  .lh-section-lbl { font-family: 'Newsreader', serif; font-style: italic;
        font-size: 0.88em; color: var(--ink-faint); text-align: center;
        margin: 0 0 18px; letter-spacing: 0.05em; }
  .lh-item { border-bottom: 1px solid var(--rule); padding: 22px 0; }
  .lh-row { display: grid; grid-template-columns: 110px 1fr 36px;
        gap: 24px; align-items: baseline; }
  .lh-dt { font-family: 'Newsreader', serif; font-style: italic;
        font-size: 14px; color: var(--ink-soft);
        font-variant-numeric: tabular-nums; line-height: 1.3; padding-top: 6px; }
  .lh-dt .yr { display: block; font-size: 18px; font-style: normal;
        color: var(--ink); margin-top: 2px; font-feature-settings: 'lnum'; }
  .lh-ttl-wrap { display: flex; flex-direction: column; gap: 4px; }
  .lh-ttl { font-family: 'Newsreader', serif; font-size: 1.32em;
        font-weight: 500; letter-spacing: -0.012em; line-height: 1.22;
        text-decoration: none; color: var(--ink); text-wrap: balance; }
  .lh-ttl:hover { color: var(--red); }
  .lh-meta { font-size: 12px; color: var(--ink-faint);
        letter-spacing: 0.06em; text-transform: uppercase;
        font-family: 'Inter', sans-serif; font-weight: 500; }
  .lh-meta .dot { color: var(--rule); margin: 0 6px; }
  .lh-meta .fi { color: var(--red); }
  .lh-x { width: 30px; height: 30px; border-radius: 50%;
        border: 1px solid var(--rule); background: var(--cream);
        color: var(--ink-soft); font-size: 16px; line-height: 1;
        display: inline-flex; align-items: center; justify-content: center;
        cursor: default; }
  .lh-x[data-open="1"] { background: var(--red); color: var(--cream);
        border-color: var(--red); }

  /* Expand variants — panel softened (no border, no drop-shadow) so the
     summary reads as a note on the page rather than a pasted-in card. */
  .lh-sum-inline { grid-column: 2 / 4; margin: 12px 0 0; max-width: var(--measure);
        font-family: 'Newsreader', serif; font-size: 1em; line-height: 1.5;
        color: var(--ink-soft); }
  .lh-sum-quote { grid-column: 2 / 4; margin: 12px 0 0;
        padding: 2px 0 2px 18px; border-left: 2px solid var(--rule);
        font-family: 'Newsreader', serif; font-style: italic; font-size: 1em;
        line-height: 1.5; color: var(--ink-soft); max-width: var(--measure); }
  .lh-sum-panel { grid-column: 2 / 4; margin: 12px 0 0;
        padding: 14px 20px; background: var(--cream-deep);
        font-family: 'Newsreader', serif; font-size: 1em; line-height: 1.5;
        color: var(--ink); max-width: var(--measure); }

  /* Ornament levels: minimal kills the paper grain + sub-wordmark + section label */
  .lh[data-orn="minimal"]::before { display: none; }
  .lh[data-orn="minimal"] .lh-marks .bylines .fi { display: none; }
  .lh[data-orn="minimal"] .lh-marks .bylines .sep { display: none; }
  .lh[data-orn="minimal"] .lh-section-lbl { display: none; }
  .lh[data-orn="richer"]::before { opacity: 0.85; }
  .lh[data-orn="richer"] .lh-marks::after { content: '· · ·';
        font-family: 'Newsreader', serif; font-style: italic;
        color: var(--ink-faint); letter-spacing: 0.4em; margin-top: 6px;
        font-size: 12px; }

  .lh-foot { max-width: 1080px; margin: 80px auto 0;
        padding: 28px 56px 40px; border-top: 1px solid var(--rule);
        font-size: 13px; color: var(--ink-faint); display: flex;
        justify-content: space-between; align-items: center; }
  .lh-foot a { color: var(--ink-soft); text-decoration: none;
        border-bottom: 1px solid var(--rule); }
  .lh-foot .orn { font-family: 'Newsreader', serif; font-style: italic;
        color: var(--ink-faint); }
`;

function LhPaneEN({ dim }) {
  const i = EN_INTRO_PARTS;
  return (
    <div className="lh-pane" data-dim={dim ? '1' : '0'}>
      <span className="lbl">English</span>
      <p>{i.lead}</p>
      <p>{i.contact_pre}<a href="#s">{i.scholar}</a>{i.contact_mid}<a href="#e">{i.email}</a>{i.contact_post}<a href="#l">{i.linkedin}</a>{i.contact_end}</p>
      <p><em>Nota bene:</em> {i.nb_pre}<a href="#n">{i.necsi}</a>{i.nb_post}</p>
    </div>);

}
function LhPaneFI({ dim }) {
  const i = FI_INTRO_PARTS;
  return (
    <div className="lh-pane" data-dim={dim ? '1' : '0'}>
      <span className="lbl">Suomeksi</span>
      <p>{i.lead}</p>
      <p>{i.hope}</p>
      <p>{i.sign1}<br />{i.sign2}</p>
    </div>);

}

function LhRow({ post, expanded, onToggle, expandStyle }) {
  const sumClass = expandStyle === 'quote' ? 'lh-sum-quote' :
  expandStyle === 'inline' ? 'lh-sum-inline' :
  'lh-sum-panel';
  const d = new Date(post.date);
  const day = String(d.getDate()).padStart(2, '0');
  const mo = d.toLocaleDateString('en-GB', { month: 'short' });
  const yr = d.getFullYear();
  return (
    <li className="lh-item">
      <div className="lh-row">
        <span className="lh-dt">{day} {mo}<span className="yr">{yr}</span></span>
        <div className="lh-ttl-wrap">
          <a className="lh-ttl" href="#">{post.title}</a>
          <span className="lh-meta">
            {post.kind === 'research' ? 'Research piece' : 'Applied musing'}
            {post.lang === 'fi' && <><span className="dot">·</span><span className="fi">Suomeksi</span></>}
          </span>
        </div>
        <button className="lh-x" data-open={expanded ? '1' : '0'} onClick={onToggle}
        aria-expanded={expanded} aria-label={expanded ? 'Hide summary' : 'Show summary'}>
          {expanded ? '\u2013' : '+'}
        </button>
        {expanded && <p className={sumClass}>{post.summary}</p>}
      </div>
    </li>);

}

function HomeLetterhead({ tweaks }) {
  const [lang, setLang] = React.useState('all');
  const [type, setType] = React.useState('all');
  const [open, setOpen] = React.useState({ 0: true });
  const [topicOpen, setTopicOpen] = React.useState(false);
  // Default expand style softened from 'panel' to 'quote' — the bordered
  // drop-shadowed cream-deep card stood out too much in user review.
  const expandStyle = resolveExpand(tweaks.expandStyle, 'quote');
  const visible = POSTS.filter((p) =>
    (lang === 'all' || p.lang === lang) &&
    (type === 'all' || p.kind === type));
  const year = new Date().getFullYear();

  return (
    <div className="lh" data-orn={tweaks.ornament} style={tokenStyle(tweaks)}>
      <style>{lhCss}</style>

      <header className="lh-band">
        <a className="lh-brand" href="#">
          <img className="lh-logo" src="assets/ajatuspaa.jpg" alt=""
               style={{ height: Math.min(tweaks.bandHeight - 16, 132), width: 'auto' }} />
          <span className="lh-marks">
            <span className="wm">Matti T.J. Heino</span>
            <span className="bylines">
              <span className="en">… And Out Come the Systems</span>
              <span className="sep">·</span>
              <span className="fi">Käyttäytymisarkkitehtuuri</span>
            </span>
          </span>
        </a>
        <nav className="lh-nav">
          <a href="#">Browse posts</a>
        </nav>
      </header>

      <main className="lh-main">
        <div className="lh-hero-head">
          <h1 className="lh-h1">Welcome <span className="slash">/</span> Tervetuloa</h1>
        </div>

        <div className="lh-diptych">
          <LhPaneEN dim={lang === 'fi'} />
          <div className="rule" />
          <LhPaneFI dim={lang === 'en'} />
        </div>

        <div className="lh-filters">
          <div className="lh-filter-row">
            <span className="lh-filter-lbl">Read</span>
            <div className="lh-lang">
              {['all', 'en', 'fi'].map((k) =>
                <button key={k} className="lh-pill" data-on={lang === k ? '1' : '0'}
                        onClick={() => setLang(k)}>
                  {k === 'all' ? 'All' : k === 'en' ? 'English' : 'Suomeksi'}
                </button>
              )}
            </div>
          </div>
          <div className="lh-filter-row">
            <span className="lh-filter-lbl">Kind</span>
            <div className="lh-lang">
              {[
                { v: 'all', label: 'All' },
                { v: 'research', label: 'Research pieces' },
                { v: 'applied', label: 'Applied musings' },
              ].map((k) =>
                <button key={k.v} className="lh-pill" data-on={type === k.v ? '1' : '0'}
                        onClick={() => setType(k.v)}>
                  {k.label}
                </button>
              )}
            </div>
          </div>
          <button className="lh-fold" onClick={() => setTopicOpen((v) => !v)}>
            <FoldChevron open={topicOpen} />
            Browse by topic
          </button>
          <a className="lh-random" href="#random" onClick={(e) => {
            e.preventDefault();
            // Demo behaviour for the mockup — production should hit a route
            // that picks a random live entry and 302s to it.
            const pool = POSTS;
            const pick = pool[Math.floor(Math.random() * pool.length)];
            setOpen({ [POSTS.indexOf(pick)]: true });
          }}>
            <span className="lh-random-dice" aria-hidden="true">⚄</span>
            Random
          </a>
          {topicOpen &&
            <div className="lh-chips">
              {TOPICS.map((t) => <button key={t} className="lh-chip">{t}</button>)}
            </div>
          }
        </div>

        <ul className="lh-list">
          <p className="lh-section-lbl">writing · newest first</p>
          {visible.map((p, i) =>
          <LhRow key={p.title} post={p} expanded={!!open[i]}
          onToggle={() => setOpen((o) => ({ ...o, [i]: !o[i] }))}
          expandStyle={expandStyle} />
          )}
        </ul>
      </main>

      <footer className="lh-foot">
        <span>© {year} Matti T.J. Heino</span>
        <span className="orn">·   ·   ·</span>
        <a href="#rss">RSS · all writing</a>
      </footer>
    </div>);

}

window.HomeLetterhead = HomeLetterhead;