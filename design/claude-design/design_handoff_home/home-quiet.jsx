// home-quiet.jsx
// Direction A — "Quiet" Reading Room.
// The most considered, classic interpretation of the brief. Single column,
// hairline rules, minimum ornament. Logo + wordmark + nav inline on the sky
// band. Filter pills are quiet; topic fold collapsed on load.

const quietCss = `
  .qa { font-family: 'Inter', system-ui, sans-serif; color: var(--ink);
        background: var(--cream); font-size: var(--body-size); line-height: 1.6;
        font-feature-settings: 'ss01', 'cv02'; }
  .qa h1, .qa h2, .qa h3, .qa .serif { font-family: 'Newsreader', Georgia, serif;
        font-weight: 500; letter-spacing: -0.005em; }

  /* Band */
  .qa-band { background: var(--sky); height: var(--band-h);
        display: flex; align-items: center; padding: 0 56px;
        border-bottom: 1px solid var(--sky-deep); }
  .qa-band .inner { display: flex; align-items: center; width: 100%;
        justify-content: space-between; gap: 32px; }
  .qa-brand { display: flex; align-items: center; gap: 16px;
        text-decoration: none; color: var(--ink); }
  .qa-brand .wordmark { font-family: 'Newsreader', serif; font-weight: 500;
        font-size: 22px; letter-spacing: -0.01em; }
  .qa-nav { display: flex; gap: 28px; font-size: 14.5px; font-weight: 500; }
  .qa-nav a { color: var(--ink); text-decoration: none; padding-bottom: 2px;
        border-bottom: 1px solid transparent; }
  .qa-nav a:hover { border-bottom-color: var(--ink); }

  /* Main column */
  .qa-main { max-width: 760px; margin: 0 auto; padding: 64px 48px 96px; }

  /* Hero */
  .qa-kicker { font-family: 'Newsreader', serif; font-style: italic;
        font-size: 1em; color: var(--red); margin: 0 0 18px; letter-spacing: -0.005em; }
  .qa-h1 { font-family: 'Newsreader', serif; font-weight: 500;
        font-size: 64px; line-height: 1.02; letter-spacing: -0.022em;
        margin: 0 0 28px; color: var(--ink); text-wrap: balance; }
  .qa-h1 .slash { color: var(--ink-faint); font-weight: 400;
        margin: 0 0.1em; font-style: italic; }
  .qa-intro { font-family: 'Newsreader', serif; font-size: 1.14em;
        line-height: 1.55; max-width: min(56ch, var(--measure)); color: var(--ink); }
  .qa-intro p { margin: 0 0 0.9em; }
  .qa-intro p:last-child { margin: 0; }
  .qa-intro a { color: var(--ink); text-decoration: underline;
        text-decoration-color: var(--red); text-decoration-thickness: 1px;
        text-underline-offset: 3px; }
  .qa-intro a:hover { color: var(--red); }
  .qa-intro em { font-style: italic; color: var(--ink-soft); }

  /* Filters */
  .qa-filters { margin-top: 56px; padding-top: 28px;
        border-top: 1px solid var(--rule); display: flex;
        flex-direction: column; gap: 14px; }
  .qa-lang { display: flex; gap: 6px; align-items: center; }
  .qa-lang .lbl { font-size: 12px; text-transform: uppercase;
        letter-spacing: 0.12em; color: var(--ink-faint); margin-right: 14px; }
  .qa-pill { font: inherit; font-size: 13.5px; font-weight: 500;
        background: transparent; color: var(--ink-soft);
        border: 1px solid var(--rule); padding: 6px 14px; border-radius: 999px;
        cursor: default; }
  .qa-pill[data-on="1"] { background: var(--red); color: var(--cream);
        border-color: var(--red); }
  .qa-pill:hover:not([data-on="1"]) { color: var(--ink); border-color: var(--ink-faint); }
  .qa-fold { font: inherit; font-size: 13.5px; color: var(--ink-soft);
        background: transparent; border: 0; padding: 0; cursor: default;
        display: inline-flex; align-items: center; width: max-content; }
  .qa-fold[data-open="1"] { color: var(--ink); }
  .qa-chips { display: flex; flex-wrap: wrap; gap: 6px; margin-top: 12px; }
  .qa-chip { font: inherit; font-size: 12.5px; color: var(--ink-soft);
        background: var(--cream-deep); border: 1px solid var(--rule);
        padding: 4px 11px; border-radius: 999px; cursor: default; }

  /* List */
  .qa-list { list-style: none; padding: 0; margin: 40px 0 0;
        border-top: 1px solid var(--rule); }
  .qa-item { border-bottom: 1px solid var(--rule);
        padding: 22px 0; }
  .qa-row { display: grid; grid-template-columns: 1fr auto 36px;
        gap: 18px; align-items: baseline; }
  .qa-ttl { font-family: 'Newsreader', serif; font-size: 1.3em;
        font-weight: 500; letter-spacing: -0.012em; line-height: 1.25;
        text-decoration: none; color: var(--ink); text-wrap: balance; }
  .qa-ttl:hover { color: var(--red); }
  .qa-fi { display: inline-block; font-family: 'Inter', sans-serif;
        font-size: 10.5px; font-weight: 600; letter-spacing: 0.08em;
        color: var(--ink-soft); border: 1px solid var(--ink-faint);
        padding: 1px 5px 0; border-radius: 3px; vertical-align: 0.18em;
        margin-left: 8px; }
  .qa-date { font-size: 13px; color: var(--ink-soft); white-space: nowrap;
        font-variant-numeric: tabular-nums; }
  .qa-x { width: 30px; height: 30px; border-radius: 50%;
        border: 1px solid var(--rule); background: var(--cream);
        color: var(--ink-soft); font-size: 16px; line-height: 1; cursor: default;
        display: inline-flex; align-items: center; justify-content: center; }
  .qa-x[data-open="1"] { background: var(--ink); color: var(--cream);
        border-color: var(--ink); }

  /* Expand variants */
  .qa-sum-inline { margin: 10px 0 0; max-width: var(--measure);
        font-family: 'Newsreader', serif; font-size: 1em; line-height: 1.5;
        color: var(--ink-soft); }
  .qa-sum-quote { margin: 12px 0 0 0; padding: 4px 0 4px 18px;
        border-left: 2px solid var(--rule);
        font-family: 'Newsreader', serif; font-style: italic; font-size: 1em;
        line-height: 1.5; color: var(--ink-soft); max-width: var(--measure); }
  .qa-sum-panel { margin: 14px 0 0; padding: 18px 22px;
        background: var(--cream-deep); border: 1px solid var(--rule-soft);
        font-family: 'Newsreader', serif; font-size: 1em; line-height: 1.5;
        color: var(--ink); max-width: var(--measure); }

  /* Ornament levels — minimal removes the italic kicker entirely; richer adds
     a faint dot leader between hero and filters. */
  .qa[data-orn="minimal"] .qa-kicker { display: none; }
  .qa[data-orn="richer"] .qa-filters { position: relative; }
  .qa[data-orn="richer"] .qa-filters::before { content: '·   ·   ·';
        position: absolute; left: 50%; top: -14px; transform: translate(-50%, -50%);
        background: var(--cream); padding: 0 12px; color: var(--ink-faint);
        font-family: 'Newsreader', serif; font-style: italic; letter-spacing: 0.4em; }

  /* Footer */
  .qa-foot { padding: 32px 48px; border-top: 1px solid var(--rule);
        max-width: 760px; margin: 80px auto 0;
        font-size: 13px; color: var(--ink-faint); display: flex;
        justify-content: space-between; }
  .qa-foot a { color: var(--ink-soft); text-decoration: none;
        border-bottom: 1px solid var(--rule); }
`;

function QuietIntroEN() {
  const i = EN_INTRO_PARTS;
  return (
    <div className="qa-intro">
      <p>{i.lead}</p>
      <p>{i.contact_pre}<a href="#scholar">{i.scholar}</a>{i.contact_mid}<a href="#email">{i.email}</a>{i.contact_post}<a href="#linkedin">{i.linkedin}</a>{i.contact_end}</p>
      <p><em>Nota bene:</em> {i.nb_pre}<a href="#necsi">{i.necsi}</a>{i.nb_post}</p>
    </div>
  );
}
function QuietIntroFI() {
  const i = FI_INTRO_PARTS;
  return (
    <div className="qa-intro">
      <p>{i.lead}</p>
      <p>{i.hope}</p>
      <p>{i.sign1}<br />{i.sign2}</p>
    </div>
  );
}

function QuietRow({ post, expanded, onToggle, expandStyle }) {
  const sumClass = expandStyle === 'quote' ? 'qa-sum-quote'
                  : expandStyle === 'panel' ? 'qa-sum-panel'
                  : 'qa-sum-inline';
  return (
    <li className="qa-item">
      <div className="qa-row">
        <div>
          <a className="qa-ttl" href="#">{post.title}</a>
          {post.lang === 'fi' && <span className="qa-fi">FI</span>}
        </div>
        <span className="qa-date">{fmtDate(post.date)}</span>
        <button className="qa-x" data-open={expanded ? '1' : '0'} onClick={onToggle}
                aria-expanded={expanded} aria-label={expanded ? 'Hide summary' : 'Show summary'}>
          {expanded ? '\u2013' : '+'}
        </button>
      </div>
      {expanded && <p className={sumClass}>{post.summary}</p>}
    </li>
  );
}

function HomeQuiet({ tweaks }) {
  const [lang, setLang] = React.useState('all');
  const [open, setOpen] = React.useState({ 0: true }); // first row expanded by default for demo
  const [topicOpen, setTopicOpen] = React.useState(false);
  const expandStyle = resolveExpand(tweaks.expandStyle, 'inline');
  const visible = POSTS.filter((p) => lang === 'all' || p.lang === lang);

  return (
    <div className="qa" data-orn={tweaks.ornament} style={tokenStyle(tweaks)}>
      <style>{quietCss}</style>

      <header className="qa-band">
        <div className="inner">
          <a className="qa-brand" href="#">
            <Logo height={Math.min(tweaks.bandHeight - 30, 72)} />
            <span className="wordmark">Matti T.J. Heino</span>
          </a>
          <nav className="qa-nav">
            <a href="#">Research pieces</a>
            <a href="#">Applied musings</a>
            <a href="#">Archive</a>
            <a href="#">Search</a>
          </nav>
        </div>
      </header>

      <main className="qa-main">
        <p className="qa-kicker">… And Out Come the Systems</p>
        <h1 className="qa-h1">Welcome <span className="slash">/</span> Tervetuloa</h1>
        {lang === 'fi' ? <QuietIntroFI /> : <QuietIntroEN />}

        <div className="qa-filters">
          <div className="qa-lang">
            <span className="lbl">Read</span>
            {['all', 'en', 'fi'].map((k) => (
              <button key={k} className="qa-pill" data-on={lang === k ? '1' : '0'}
                      onClick={() => setLang(k)}>
                {k === 'all' ? 'All' : k === 'en' ? 'English' : 'Suomeksi'}
              </button>
            ))}
          </div>
          <button className="qa-fold" data-open={topicOpen ? '1' : '0'}
                  onClick={() => setTopicOpen((v) => !v)}>
            <FoldChevron open={topicOpen} />
            Browse by topic
          </button>
          {topicOpen && (
            <div className="qa-chips">
              {TOPICS.map((t) => <button key={t} className="qa-chip">{t}</button>)}
            </div>
          )}
        </div>

        <ul className="qa-list">
          {visible.map((p, i) => (
            <QuietRow key={p.title} post={p} expanded={!!open[i]}
                      onToggle={() => setOpen((o) => ({ ...o, [i]: !o[i] }))}
                      expandStyle={expandStyle} />
          ))}
        </ul>
      </main>

      <footer className="qa-foot">
        <span>© 2026 Matti T.J. Heino</span>
        <a href="#rss">RSS</a>
      </footer>
    </div>
  );
}

window.HomeQuiet = HomeQuiet;
