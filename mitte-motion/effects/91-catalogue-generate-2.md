# Generate: every parameter (part 2 of 2)

Generated from `rexx-engine effects` by scripts/skills-effects-catalogue.py; do not edit by hand. Index: [90-catalogue.md](90-catalogue.md).

<!-- gen:catalogue-generate-2:start -->
### `generate.advancedLightning`

After Effects: Advanced Lightning / Lightning (obsolete) · Phase: P2 · Status: implemented · Tiling: whole · Reads: — · Reads time: no · Device: CPU

Seeded, `conductivityState` animates the bolt.

| Parameter | Type | Default | Range | Anim | What it does |
|---|---|---|---|---|---|
| `lightningType` | enum `direction` / `strike` / `breaking` / `bouncy` / `omni` / `anywhere` / `vertical` / `twoWayStrike` | `strike` | — | — | Where the bolt goes. |
| `origin` | point `[x, y]` | `["25%", "20%"]` | — | A | Where the bolt starts. |
| `direction` | point `[x, y]` | `["75%", "80%"]` | — | A | Where the bolt goes (or points). |
| `conductivityState` | number | 10 | — | A | Picks the random tree; animate it to flicker. |
| `core.radius` | length px | 3 | ≥ 0 (clamped) | A | Half-width of the core (px). |
| `core.opacity` | percent | 75 | 0–100 (soft) | A | Opacity of the core. |
| `core.color` | color | `#FFFFFF` | — | A | Colour of the core. |
| `glow.radius` | length px | 50 | ≥ 0 (clamped) | A | Radius of the glow (px). |
| `glow.opacity` | percent | 50 | 0–100 (soft) | A | Opacity of the glow. |
| `glow.color` | color | `#4059FF` | — | A | Colour of the glow. |
| `turbulence` | number | 1 | 0–10 (clamped) | A | Zig-zag of the bolt. |
| `forking` | percent | 25 | 0–100 (soft) | A | Chance of a fork at each subdivision. |
| `decay` | number | 0.3 | 0–1 (clamped) | A | How much fainter each fork is. |
| `decayMainCore` | boolean | false | — | — | Fade the whole bolt with the distance from the origin. |
| `alphaObstacle` | number | 0 | -10–10 (clamped) | A | Avoid (positive) or seek (negative) opaque areas. |
| `compositeOnOriginal` | boolean | true | — | — | Add the light to the layer (else the bolt alone). |
| `expert.complexity` | integer | 6 | 1–12 (clamped) | — | Subdivision depth. |
| `expert.minForkDistance` | length px | 0 | ≥ 0 (clamped) | A | Shorter stretches do not fork (px). |
| `expert.terminationThreshold` | percent | 5 | 0–100 (soft) | A | Branches fainter than this stop. |
| `expert.mainCoreCollisionOnly` | boolean | false | — | — | Only the main core avoids obstacles. |
| `expert.fractalType` | enum `linear` / `semiLinear` / `spline` | `linear` | — | — | Shape of the zig-zag. |
| `expert.coreDrain` | percent | 0 | 0–100 (soft) | A | The main core fades along its length. |
| `expert.forkStrength` | percent | 50 | 0–100 (soft) | A | Intensity of the forks (50 keeps the decayed one). |
| `expert.forkVariation` | percent | 0 | 0–100 (soft) | A | Random variation of the fork intensity. |

Every instance also takes `expand` (number px or `"none"`); see 01-effects-basics.md.

### `generate.paintBucket`

After Effects: Paint Bucket · Phase: P3 · Status: implemented · Tiling: whole · Reads: — · Reads time: no · Device: CPU

Implemented: a 4-connected flood fill over the layer rect from `fillPoint`; `tolerance` is in display-encoded 0–255 codes; `featherSoftness` and `spreadRadius` (not in After Effects' panel by these names) are the radii of `feather` and `spread`/`choke`; the fill composites normally over the layer (After Effects' blending modes and View Threshold are not provided).

| Parameter | Type | Default | Range | Anim | What it does |
|---|---|---|---|---|---|
| `fillPoint` | point `[x, y]` | `center` | — | A | Where the fill starts, in layer px. |
| `selector` | enum `colorAndAlpha` / `straightColor` / `transparency` / `opacity` / `alphaChannel` | `colorAndAlpha` | — | — | What the fill compares. |
| `tolerance` | number | 10 | 0–255 (clamped) | A | How far a pixel may differ (0–255). |
| `strokeType` | enum `antialias` / `feather` / `spread` / `choke` | `antialias` | — | — | How the fill's edge is drawn. |
| `featherSoftness` | length px | 10 | ≥ 0 (clamped) | A | Feather width for `strokeType: feather` (px). |
| `spreadRadius` | length px | 3 | ≥ 0 (clamped) | A | Growth for `spread`, shrink for `choke` (px). |
| `color` | color | `#FF0000` | — | A | Fill color. |
| `opacity` | percent | 100 | 0–100 (soft) | A | Fill opacity. |

Every instance also takes `expand` (number px or `"none"`); see 01-effects-basics.md.

### `generate.writeOn`

After Effects: Write-on · Phase: P3 · Status: implemented · Tiling: whole · Reads: parameter history · Reads time: no · Device: CPU

Paint a stroke by keyframing the brush; signatures, hand-drawn reveals.

| Parameter | Type | Default | Range | Anim | What it does |
|---|---|---|---|---|---|
| `brushPosition` | point `[x, y]` | `center` | — | A | Where the brush is (animate it to write). |
| `color` | color | `#FFFFFF` | — | A | Paint color. |
| `size` | length px | 6 | ≥ 0 (clamped) | A | Brush size in px. |
| `hardness` | percent | 75 | 0–100 (soft) | A | Fraction of the brush that is fully opaque. |
| `opacity` | percent | 100 | 0–100 (soft) | A | Paint opacity. |
| `length` | number | 0 | ≥ 0 (clamped) | A | Seconds of stroke kept behind the brush (0 = all). |
| `spacing` | number | 0.001 | ≥ 0 (clamped) | A | Seconds between dabs. |
| `paintTime` | enum `none` / `opacity` / `color` | `none` | — | — | Which paint properties each dab keeps from its time. |
| `paintStyle` | enum `onOriginal` / `onTransparent` / `revealOriginal` | `onOriginal` | — | — | How the paint meets the layer. |

Every instance also takes `expand` (number px or `"none"`); see 01-effects-basics.md.

### `generate.ccGlueGun`

After Effects: CC Glue Gun · Phase: P2 · Status: implemented · Tiling: tiled · Reads: parameter history · Reads time: no · Device: CPU

Blobs of "glue" laid along the animated `brushPosition` over the last `timeSpan` seconds (reads the parameter's history, `Deps::param_samples`).

| Parameter | Type | Default | Range | Anim | What it does |
|---|---|---|---|---|---|
| `brushPosition` | point `[x, y]` | `center` | — | A | Where the glue is laid (animate it to draw). |
| `strokeWidth` | length px | 25 | ≥ 0 (clamped) | A | Blob width in px. |
| `density` | number | 5 | 0–32 (clamped) | A | Beads per blob. |
| `timeSpan` | number | 1 | ≥ 0 (clamped) | A | Seconds of brush history drawn. |
| `reflection` | angle ° | 45 | — | A | Direction of the highlight. |
| `strength` | percent | 100 | 0–100 (soft) | A | How much the glue shows. |
| `style` | enum `overLayer` / `glueOnly` | `overLayer` | — | — | Over the layer, or the glue alone. |

Every instance also takes `expand` (number px or `"none"`); see 01-effects-basics.md.

<!-- gen:catalogue-generate-2:end -->
