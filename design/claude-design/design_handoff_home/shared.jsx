// shared.jsx
// Data + small atoms shared by all three direction artboards.
// Posts seeded from the real content in mattiheino-site/src/content + brief.

const POSTS = [
  {
    title: 'Evidence is in the Past, Risk is in the Future: On Tail Events and Foresight',
    date: '2025-11-10', lang: 'en', kind: 'research',
    summary: 'Why the worst event you have seen so far is a poor guide to the worst event that can happen \u2013 and what to do about it when planning for preparedness.',
    tags: ['complexity', 'risk', 'preparedness'],
  },
  {
    title: 'From Fruit Salad to Baked Bread: Understanding Complex Systems for Behaviour Change',
    date: '2025-05-22', lang: 'en', kind: 'research',
    summary: 'A working metaphor for the difference between complicated and complex \u2013 and what it changes about how behaviour-change practice should be set up.',
    tags: ['complex systems', 'behaviour change'],
  },
  {
    title: 'Opi torjumaan viruksia ja parantamaan sis\u00e4ilman laatua',
    date: '2024-08-05', lang: 'fi', kind: 'research',
    summary: 'Lyhyt johdatus siihen, miksi ilmanvaihto ja -puhdistus ovat arjen terveysteko, ja mit\u00e4 niiden eteen voi tehd\u00e4 kodin oloissa.',
    tags: ['ilmahygienia', 'varautuminen', 'terveys'],
  },
  {
    title: "Affordance Mapping to Manage Complex Systems: Planning a Children's Party",
    date: '2024-08-12', lang: 'en', kind: 'applied',
    summary: 'A small, domestic worked example to show how affordance mapping does what flat checklists cannot \u2013 plan for what the system will let you do.',
    tags: ['complex systems', 'planning'],
  },
  {
    title: 'A 14-day Fasting Experiment',
    date: '2021-09-13', lang: 'en', kind: 'applied',
    summary: 'One person, two weeks, a glucose monitor, and a lot of second-guessing. Less a result than a record of what self-experimentation actually feels like.',
    tags: ['self-experiment', 'metabolism', 'n-of-1'],
  },
  {
    title: 'When uncertainty makes decisions easier, not harder',
    date: '2020-09-15', lang: 'en', kind: 'research',
    summary: 'A counter-intuitive look at how acknowledging what we do not know can sharpen, rather than paralyse, the decisions in front of us.',
    tags: ['decision-making', 'uncertainty', 'behaviour change'],
    legacy: true, confirmed: '2026-05-24',
  },
  {
    title: '123 techniques for self-management',
    date: '2020-03-01', lang: 'en', kind: 'applied',
    summary: 'A long, practical menu of things you can actually try when you want to change a habit. Not a programme \u2013 a buffet.',
    tags: ['self-management', 'habits', 'behaviour change'],
  },
  {
    title: 'Antihauras el\u00e4m\u00e4',
    date: '2020-02-11', lang: 'fi', kind: 'applied',
    summary: 'Mit\u00e4 arjen valinnat voisivat oppia siit\u00e4, miten jotkin j\u00e4rjestelm\u00e4t vahvistuvat h\u00e4iri\u00f6ist\u00e4 sen sijaan, ett\u00e4 hajoaisivat niihin.',
    tags: ['antihauraus', 'kompleksisuus', 'el\u00e4m\u00e4ntapa'],
  },
];

const TOPICS = [
  'complex systems', 'behaviour change', 'preparedness', 'health & well-being',
  'risk', 'self-management', 'uncertainty', 'ilmahygienia', 'varautuminen',
];

const EN_INTRO_PARTS = {
  lead: 'This is a blog about behaviour change science and complex systems in preparedness, health and well-being.',
  contact_pre: 'For research articles, see my ',
  scholar: 'Google Scholar profile',
  contact_mid: '. To email me about anything, write to ',
  email: 'matti.tj.heino @ this domain',
  contact_post: ' (i.e. mattiheino.com). Find me ',
  linkedin: 'on LinkedIn',
  contact_end: '.',
  nb_pre: 'I instruct an ',
  necsi: 'online course for the New England Complex Systems Institute',
  nb_post: ', and am happy to answer questions. Do reach out.',
};

const FI_INTRO_PARTS = {
  lead: 'N\u00e4iden sivujen tarkoituksena on lis\u00e4t\u00e4 tietoa inhimilliseen toimintaan vaikuttamisesta yhteisen hyvinvoinnin lis\u00e4\u00e4miseksi. Tavoitteena on l\u00f6yt\u00e4\u00e4 n\u00e4k\u00f6kulmia niin omaan kuin muidenkin k\u00e4ytt\u00e4ytymiseen.',
  hope: 'Toivottavasti l\u00f6yd\u00e4t jotain kiinnostavaa.',
  sign1: 'Yst\u00e4v\u00e4llisesti,',
  sign2: 'Heinon Matti.',
};

// British English date formatter — matches the Astro fmt() helper.
function fmtDate(iso) {
  const d = new Date(iso);
  return d.toLocaleDateString('en-GB', { year: 'numeric', month: 'long', day: 'numeric' });
}

// Short variant for compact use (e.g. side-gutter)
function fmtShort(iso) {
  const d = new Date(iso);
  const mo = d.toLocaleDateString('en-GB', { month: 'short' });
  return `${String(d.getDate()).padStart(2, '0')} ${mo} ${d.getFullYear()}`;
}

// Small-caps year extractor
function yearOf(iso) { return new Date(iso).getFullYear(); }

// CSS variables — applied to each artboard's root so tweaks cascade only inside the home mock.
function tokenStyle(t) {
  // Cream pair: derive deeper from the base by mixing toward warm tan.
  // For curated palettes we pass [cream, creamDeep] together.
  const cream = Array.isArray(t.creamPair) ? t.creamPair[0] : t.cream;
  const creamDeep = Array.isArray(t.creamPair) ? t.creamPair[1] : t.creamDeep;
  const red = Array.isArray(t.redPair) ? t.redPair[0] : t.red;
  const redDeep = Array.isArray(t.redPair) ? t.redPair[1] : t.redDeep;
  return {
    '--cream': cream,
    '--cream-deep': creamDeep,
    '--ink': '#211d18',
    '--ink-soft': '#5b5348',
    '--ink-faint': '#8a7f6d',
    '--red': red,
    '--red-deep': redDeep,
    '--sky': '#a6d9ec',
    '--sky-deep': '#8ec8e0',
    '--sky-tint': '#dfeef5',
    '--rule': '#e0d6c4',
    '--rule-soft': '#ece4d2',
    '--band-h': t.bandHeight + 'px',
    '--body-size': t.bodySize + 'px',
    '--measure': t.measure + 'ch',
  };
}

// Resolve per-direction expand style, allowing the tweak to override.
function resolveExpand(globalChoice, defaultForDirection) {
  return globalChoice === 'as-designed' ? defaultForDirection : globalChoice;
}

// Same idea for ornament: 'as-designed' = use the direction's default.
function resolveOrnament(globalChoice, defaultForDirection) {
  if (globalChoice === 'as-designed') return defaultForDirection;
  return globalChoice;
}

// Tiny right-arrow chevron used in the topic-fold summary.
function FoldChevron({ open }) {
  return (
    <span aria-hidden="true" style={{
      display: 'inline-block',
      width: '0.7em',
      transform: open ? 'rotate(90deg)' : 'rotate(0)',
      transition: 'transform .15s',
      color: 'var(--ink-faint)',
      marginRight: '0.25em',
    }}>›</span>
  );
}

// Logo on sky band. Uses the actual ajatuspää JPG copied into /assets.
function Logo({ height = 56 }) {
  return (
    <img src="assets/ajatuspaa.jpg" alt="" style={{
      height, width: 'auto', display: 'block',
      // dissolve into the sky band — no border, no shadow
      mixBlendMode: 'multiply',
    }} />
  );
}

Object.assign(window, {
  POSTS, TOPICS, EN_INTRO_PARTS, FI_INTRO_PARTS,
  fmtDate, fmtShort, yearOf,
  tokenStyle, resolveExpand, resolveOrnament,
  FoldChevron, Logo,
});
