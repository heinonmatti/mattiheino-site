// app.jsx — design canvas + tweaks panel hosting three home directions.

const TWEAK_DEFAULTS = /*EDITMODE-BEGIN*/{
  "creamPair": ["#faf5ec", "#f1e8d7"],
  "redPair": ["#9c2b21", "#7d2018"],
  "bandHeight": 149,
  "bodySize": 17,
  "measure": 64,
  "ornament": "as-designed",
  "expandStyle": "inline"
}/*EDITMODE-END*/;

function App() {
  const [t, setTweak] = useTweaks(TWEAK_DEFAULTS);

  return (
    <>
      <DesignCanvas>
        <DCSection
          id="home"
          title="Home page – three faithful directions"
          subtitle="Same inherited identity (sky band, warm cream, deep red, Newsreader + Inter). Variations sit in rhythm and ornament. Open Tweaks (toolbar) to dial cream, accent red, band height, body size, and ornament/expand styles across all three at once."
        >
          <DCArtboard id="a-quiet" label="A · Quiet Reading Room" width={1280} height={1640}>
            <HomeQuiet tweaks={t} />
          </DCArtboard>
          <DCArtboard id="b-marginalia" label="B · Marginalia" width={1280} height={1640}>
            <HomeMarginalia tweaks={t} />
          </DCArtboard>
          <DCArtboard id="c-letterhead" label="C · Letterhead" width={1280} height={1640}>
            <HomeLetterhead tweaks={t} />
          </DCArtboard>
        </DCSection>
      </DesignCanvas>

      <TweaksPanel title="Tweaks">
        <TweakSection label="Palette" />
        <TweakColor
          label="Cream tone"
          value={t.creamPair}
          options={[
            ['#faf5ec', '#f1e8d7'],
            ['#fbf8f0', '#f3eddd'],
            ['#f4ecdb', '#e6d9bf'],
            ['#fbf9f4', '#efe8d7'],
          ]}
          onChange={(v) => setTweak('creamPair', v)}
        />
        <TweakColor
          label="Accent red"
          value={t.redPair}
          options={[
            ['#9c2b21', '#7d2018'],
            ['#b13627', '#8e2620'],
            ['#7d1f17', '#5e160f'],
            ['#a84a1c', '#83361b'],
          ]}
          onChange={(v) => setTweak('redPair', v)}
        />

        <TweakSection label="Header band" />
        <TweakSlider
          label="Band height"
          value={t.bandHeight}
          min={80}
          max={180}
          unit="px"
          onChange={(v) => setTweak('bandHeight', v)}
        />

        <TweakSection label="Body type" />
        <TweakSlider
          label="Body size"
          value={t.bodySize}
          min={15}
          max={21}
          unit="px"
          onChange={(v) => setTweak('bodySize', v)}
        />
        <TweakSlider
          label="Measure"
          value={t.measure}
          min={52}
          max={78}
          unit="ch"
          onChange={(v) => setTweak('measure', v)}
        />

        <TweakSection label="Personality" />
        <TweakRadio
          label="Ornament"
          value={t.ornament}
          options={[
            { value: 'minimal', label: 'Quiet' },
            { value: 'as-designed', label: 'Default' },
            { value: 'richer', label: 'Richer' },
          ]}
          onChange={(v) => setTweak('ornament', v)}
        />
        <TweakSelect
          label="Row + expand"
          value={t.expandStyle}
          options={[
            { value: 'as-designed', label: 'As designed (per direction)' },
            { value: 'inline', label: 'Inline · summary slides in' },
            { value: 'quote', label: 'Quote · indented hairline' },
            { value: 'panel', label: 'Panel · cream-deep card' },
          ]}
          onChange={(v) => setTweak('expandStyle', v)}
        />
      </TweaksPanel>
    </>
  );
}

ReactDOM.createRoot(document.getElementById('root')).render(<App />);
