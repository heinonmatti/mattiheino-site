// home-marginalia.jsx
// Direction B — "Marginalia".
// Same identity as Quiet, with a running left gutter that carries date + a
// quiet ordinal. Italic eyebrow runs above the hero. A single typographic
// ornament between sections. Expand opens indented quote-style summary.

const margCss = `
  .mg { font-family: 'Inter', system-ui, sans-serif; color: var(--ink);
        background: var(--cream); font-size: var(--body-size); line-height: 1.6; }
  .mg h1, .mg .serif { font-family: 'Newsreader', Georgia, serif; }

  /* Band: same sky, slightly different layout — wordmark stacked over a thin red rule */
  .mg-band { background: var(--sky); height: var(--band-h);
        padding: 0 56px; display: flex; align-items: center;
        border-bottom: 1px solid var(--sky-deep); position: relative; }
  .mg-band::after { content: ''; position: absolute; left: 0; right: 0; bottom: -1px;
        height: 2px; background: var(--red); opacity: 0.85; }
  .mg-band .inner { display: flex; align-items: center; width: 100%;
        justify-content: space-between; gap: 32px; }
  .mg-brand { display: flex; align-items: center; gap: 18px;
        text-decoration: none; color: var(--ink); }
  .mg-brand .marks { display: flex; flex-direction: column; line-height: 1.05; }
  .mg-brand .wm { font-family: 'Newsreader', serif; font-weight: 500;
        font-size: 23px; letter-spacing: -0.01em; }
  .mg-brand .wm2 { font-family: 'Newsreader', serif; font-style: italic;
        font-size: 13px; color: var(--ink-soft); margin-top: 2px;
        letter-spacing: 0.005em; }
  .mg-nav { display: flex; gap: 26px; font-size: 14.5px; font-weight: 500; }
  .mg-nav a { color: var(--ink); text-decoration: none; }
  .mg-nav a:hover { color: var(--red-deep); }

  /* Main column with side gutter */
  .mg-main { max-width: 880px; margin: 0 auto; padding: 64px 48px 96px;
        display: grid; grid-template-columns: 80px 1fr; gap: 32px;
        align-items: start; }

  /* Hero spans both columns, with gutter empty */
  .mg-hero { grid-column: 1 / -1; display: grid;
        grid-template-columns: 80px 1fr; gap: 32px; align-items: start; }
  .mg-hero .gutter { display: flex; flex-direction: column;
        font-family: 'Newsreader', serif; }
  .mg-hero .gutter .yr { font-size: 11.5px; letter-spacing: 0.18em;
        text-transform: uppercase; color: var(--ink-faint);
        font-family: 'Inter', sans-serif; font-weight: 600; }
  .mg-hero .gutter .yr-num { font-size: 32px; color: var(--ink-faint);
        font-style: italic; margin-top: 6px; line-height: 1; }

  .mg-kicker { font-family: 'Newsreader', serif; font-style: italic;
        font-size: 1em; color: var(--red); margin: 0 0 14px; }
  .mg-h1 { font-family: 'Newsreader', serif; font-weight: 500;
        font-size: 60px; line-height: 1.04; letter-spacing: -0.022em;
        margin: 0 0 26px; color: var(--ink); text-wrap: balance; }
  .mg-h1 .slash { color: var(--ink-faint); font-weight: 400;
        font-style: italic; margin: 0 0.08em; }
  .mg-intro { font-family: 'Newsreader', serif; font-size: 1.12em;
        line-height: 1.55; max-width: min(54ch, var(--measure)); color: var(--ink); }
  .mg-intro p { margin: 0 0 0.85em; }
  .mg-intro p:last-child { margin: 0; }
  .mg-intro a { color: var(--ink); text-decoration: underline;
        text-decoration-color: var(--red); text-decoration-thickness: 1px;
        text-underline-offset: 3px; }
  .mg-intro a:hover { color: var(--red); }
  .mg-intro em { font-style: italic; }

  /* Ornament divider */
  .mg-orn { grid-column: 1 / -1; text-align: center;
        margin: 56px 0 28px; font-family: 'Newsreader', serif;
        font-style: italic; color: var(--ink-faint); font-size: 22px;
        letter-spacing: 0.6em; }

  /* Filters in main column; gutter holds a quiet label */
  .mg-filters { display: contents; }
  .mg-filters .gutter-lbl { font-family: 'Inter', sans-serif;
        font-size: 11px; text-transform: uppercase; letter-spacing: 0.16em;
        color: var(--ink-faint); padding-top: 8px; }
  .mg-filters .panel { display: flex; flex-direction: column; gap: 14px; }
  .mg-lang { display: flex; gap: 6px; align-items: center; }
  .mg-pill { font: inherit; font-size: 13.5px; font-weight: 500;
        background: transparent; color: var(--ink-soft);
        border: 1px solid var(--rule); padding: 6px 16px; border-radius: 999px;
        cursor: default; }
  .mg-pill[data-on="1"] { background: var(--red); color: var(--cream);
        border-color: var(--red); }
  .mg-fold { font: inherit; font-size: 13.5px; color: var(--ink-soft);
        font-family: 'Newsreader', serif; font-style: italic;
        background: transparent; border: 0; padding: 0; cursor: default;
        display: inline-flex; align-items: center; width: max-content; }
  .mg-chips { display: flex; flex-wrap: wrap; gap: 6px; margin-top: 6px; }
  .mg-chip { font: inherit; font-size: 12.5px; color: var(--ink-soft);
        background: transparent; border: 1px solid var(--rule);
        padding: 4px 11px; border-radius: 999px; cursor: default; }

  /* List rows */
  .mg-list { display: contents; }
  .mg-list .gutter { font-family: 'Inter', sans-serif;
        display: flex; flex-direction: column; padding-top: 4px; }
  .mg-list .gutter .num { font-family: 'Newsreader', serif; font-style: italic;
        font-size: 13px; color: var(--ink-faint); line-height: 1.2; }
  .mg-list .gutter .date { font-size: 11px; letter-spacing: 0.1em;
        text-transform: uppercase; color: var(--ink-soft); margin-top: 4px;
        font-variant-numeric: tabular-nums; line-height: 1.35; }
  .mg-item { display: contents; }
  .mg-cell { padding: 18px 0; border-bottom: 1px solid var(--rule); }
  .mg-gutter-cell { padding-top: 24px; border-bottom: 1px solid var(--rule-soft); }
  .mg-row { display: grid; grid-template-columns: 1fr 36px;
        gap: 18px; align-items: start; }
  .mg-ttl { font-family: 'Newsreader', serif; font-size: 1.3em;
        font-weight: 500; letter-spacing: -0.012em; line-height: 1.25;
        text-decoration: none; color: var(--ink); }
  .mg-ttl:hover { color: var(--red); }
  .mg-fi { display: inline-block; font-family: 'Inter', sans-serif;
        font-size: 10.5px; font-weight: 600; letter-spacing: 0.08em;
        color: var(--red); border-bottom: 1px solid var(--red);
        margin-left: 8px; padding: 0 1px 1px; }
  .mg-x { width: 28px; height: 28px; border-radius: 50%;
        border: 1px solid var(--rule); background: transparent;
        color: var(--ink-soft); font-size: 16px; line-height: 1;
        display: inline-flex; align-items: center; justify-content: center;
        cursor: default; }
  .mg-x[data-open="1"] { background: var(--ink); color: var(--cream);
        border-color: var(--ink); }

  /* Expand variants */
  .mg-sum-inline { margin: 8px 0 0; max-width: var(--measure);
        font-family: 'Newsreader', serif; font-size: 0.98em; line-height: 1.5;
        color: var(--ink-soft); }
  .mg-sum-quote { margin: 12px 0 0; padding: 2px 0 2px 18px;
        border-left: 2px solid var(--red); font-family: 'Newsreader', serif;
        font-style: italic; font-size: 1em; line-height: 1.5;
        color: var(--ink-soft); max-width: var(--measure); }
  .mg-sum-panel { margin: 12px 0 0; padding: 16px 20px;
        background: var(--cream-deep); border: 1px solid var(--rule-soft);
        font-family: 'Newsreader', serif; font-size: 0.98em; line-height: 1.5;
        color: var(--ink); max-width: var(--measure); }

  /* Ornament levels */
  .mg[data-orn="minimal"] .mg-orn { display: none; }
  .mg[data-orn="minimal"] .mg-brand .wm2 { display: none; }
  .mg[data-orn="minimal"] .mg-list .gutter .num { display: none; }
  .mg[data-orn="richer"] .mg-orn { letter-spacing: 1em; color: var(--red);
        opacity: 0.55; }
  .mg[data-orn="richer"] .mg-h1::first-letter { color: var(--red); }

  .mg-foot { max-width: 880px; margin: 64px auto 0;
        padding: 28px 48px 40px; border-top: 1px solid var(--rule);
        font-size: 13px; color: var(--ink-faint);
        display: flex; justify-content: space-between; }
  .mg-foot a { color: var(--ink-soft); text-decoration: none;
        border-bottom: 1px solid var(--rule); }
`;

function MargIntroEN() {
  const i = EN_INTRO_PARTS;
  return (
    <div className="mg-intro">
      <p>{i.lead}</p>
      <p>{i.contact_pre}<a href="#s">{i.scholar}</a>{i.contact_mid}<a href="#e">{i.email}</a>{i.contact_post}<a href="#l">{i.linkedin}</a>{i.contact_end}</p>
      <p><em>Nota bene:</em> {i.nb_pre}<a href="#n">{i.necsi}</a>{i.nb_post}</p>
    </div>
  );
}
function MargIntroFI() {
  const i = FI_INTRO_PARTS;
  return (
    <div className="mg-intro">
      <p>{i.lead}</p>
      <p>{i.hope}</p>
      <p>{i.sign1}<br />{i.sign2}</p>
    </div>
  );
}

function MargRow({ post, idx, expanded, onToggle, expandStyle }) {
  const sumClass = expandStyle === 'quote' ? 'mg-sum-quote'
                  : expandStyle === 'panel' ? 'mg-sum-panel'
                  : 'mg-sum-inline';
  // Date in gutter: "10 NOV / 2025" small caps
  const d = new Date(post.date);
  const day = String(d.getDate()).padStart(2, '0');
  const mo = d.toLocaleDateString('en-GB', { month: 'short' }).toUpperCase();
  const yr = d.getFullYear();
  return (
    <li className="mg-item">
      <div className="mg-gutter-cell">
        <span className="num">№ {String(idx + 1).padStart(2, '0')}</span>
        <span className="date">{day} {mo}<br />{yr}</span>
      </div>
      <div className="mg-cell">
        <div className="mg-row">
          <div>
            <a className="mg-ttl" href="#">{post.title}</a>
            {post.lang === 'fi' && <span className="mg-fi">FI</span>}
          </div>
          <button className="mg-x" data-open={expanded ? '1' : '0'} onClick={onToggle}
                  aria-expanded={expanded} aria-label={expanded ? 'Hide summary' : 'Show summary'}>
            {expanded ? '\u2013' : '+'}
          </button>
        </div>
        {expanded && <p className={sumClass}>{post.summary}</p>}
      </div>
    </li>
  );
}

function HomeMarginalia({ tweaks }) {
  const [lang, setLang] = React.useState('all');
  const [open, setOpen] = React.useState({ 0: true });
  const [topicOpen, setTopicOpen] = React.useState(false);
  const expandStyle = resolveExpand(tweaks.expandStyle, 'quote');
  const visible = POSTS.filter((p) => lang === 'all' || p.lang === lang);
  const year = new Date().getFullYear();

  return (
    <div className="mg" data-orn={tweaks.ornament} style={tokenStyle(tweaks)}>
      <style>{margCss}</style>

      <header className="mg-band">
        <div className="inner">
          <a className="mg-brand" href="#">
            <Logo height={Math.min(tweaks.bandHeight - 26, 78)} />
            <div className="marks">
              <span className="wm">Matti T.J. Heino</span>
              <span className="wm2">behavioural science · complex systems</span>
            </div>
          </a>
          <nav className="mg-nav">
            <a href="#">Research pieces</a>
            <a href="#">Applied musings</a>
            <a href="#">Archive</a>
            <a href="#">Search</a>
          </nav>
        </div>
      </header>

      <main className="mg-main">
        <section className="mg-hero">
          <div className="gutter">
            <span className="yr">A blog</span>
            <span className="yr-num">{year}</span>
          </div>
          <div>
            <p className="mg-kicker">… And Out Come the Systems</p>
            <h1 className="mg-h1">Welcome<span className="slash">/</span>Tervetuloa</h1>
            {lang === 'fi' ? <MargIntroFI /> : <MargIntroEN />}
          </div>
        </section>

        <div className="mg-orn" aria-hidden="true">·   ·   ·</div>

        <div className="mg-filters">
          <div className="gutter-lbl">Filter</div>
          <div className="panel">
            <div className="mg-lang">
              {['all', 'en', 'fi'].map((k) => (
                <button key={k} className="mg-pill" data-on={lang === k ? '1' : '0'}
                        onClick={() => setLang(k)}>
                  {k === 'all' ? 'All' : k === 'en' ? 'English' : 'Suomeksi'}
                </button>
              ))}
            </div>
            <button className="mg-fold" onClick={() => setTopicOpen((v) => !v)}>
              <FoldChevron open={topicOpen} />
              Browse by topic
            </button>
            {topicOpen && (
              <div className="mg-chips">
                {TOPICS.map((t) => <button key={t} className="mg-chip">{t}</button>)}
              </div>
            )}
          </div>
        </div>

        <div className="mg-orn" aria-hidden="true">·   ·   ·</div>

        <ul className="mg-list" style={{ listStyle: 'none', padding: 0, margin: 0, display: 'contents' }}>
          {visible.map((p, i) => (
            <MargRow key={p.title} post={p} idx={i} expanded={!!open[i]}
                     onToggle={() => setOpen((o) => ({ ...o, [i]: !o[i] }))}
                     expandStyle={expandStyle} />
          ))}
        </ul>
      </main>

      <footer className="mg-foot">
        <span>© {year} Matti T.J. Heino · Tampere</span>
        <a href="#rss">RSS</a>
      </footer>
    </div>
  );
}

window.HomeMarginalia = HomeMarginalia;
