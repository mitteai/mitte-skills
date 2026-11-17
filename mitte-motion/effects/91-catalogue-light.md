# Light & glow: every parameter

Generated from `rexx-engine effects` by scripts/skills-effects-catalogue.py; do not edit by hand. Index: [90-catalogue.md](90-catalogue.md).

<!-- gen:catalogue-light-1:start -->
### `light.glow`

After Effects: Glow, at Deep Glow quality · Phase: P1 · Status: implemented · Tiling: whole · Reads: — · Reads time: no · Device: GPU when the whole stack lowers, else CPU

A multi-scale bloom: the thresholded source is downsampled into a mip pyramid (up to 10 levels), each level blurred, and the levels summed with weights that approximate the chosen falloff kernel up to `radius`.

| Parameter | Type | Default | Range | Anim | What it does |
|---|---|---|---|---|---|
| `threshold` | number | 0.8 | — | A | Working-space luminance above which pixels glow (> 1 allowed). |
| `knee` | number | 0.2 | ≥ 0 (clamped) | A | Soft threshold width around `threshold`. |
| `radius` | length px | 60 | ≥ 0 (clamped) | A | Visible extent of the glow in layer px. |
| `exposure` | number | 0 | — | A | Glow gain in stops (2^exposure). |
| `intensity` | number | 1 | ≥ 0 (clamped) | A | Glow gain; 0 is the neutral value. |
| `falloff` | enum `inverseSquare` / `gaussian` / `exponential` | `inverseSquare` | — | — | Shape of the glow tail. |
| `tint` | color | `#FFFFFF` | — | A | Glow tint. |
| `tintMode` | enum `multiply` / `colorize` / `gradient` | `multiply` | — | — | How `tint` (or `gradient`) colors the glow. |
| `gradient` | gradient | none | — | A | With `tintMode: gradient`: glow color from core (0) to edge (1). |
| `chromatic` | number | 0 | -1–1 (clamped) | A | Radius spread per channel: red wider, blue tighter (warm core, cool edge). |
| `source` | enum `layer` / `alpha` / `colorKey` | `layer` | — | — | What glows: the layer's color, its alpha, or pixels near `keyColor`. |
| `keyColor` | color | `#FFFFFF` | — | A | With `source: colorKey`: the color that glows. |
| `keyTolerance` | percent | 20 | 0–100 (soft) | A | With `source: colorKey`: tolerance around `keyColor` (display-encoded distance). |
| `composite` | enum `add` / `screen` / `over` / `glowOnly` | `add` | — | — | How the glow combines with the layer. |
| `tonemap` | boolean | false | — | — | Soft-clip the glow above 0.8 so bright glows roll off instead of clipping. |
| `dirt.amount` | percent | 0 | 0–100 (soft) | A | (P2) Lens-dirt texture amount. |
| `dirt.scale` | percent | 100 | 0–100 (soft) | A | (P2) Lens-dirt texture scale. |
| `preserveColor` | boolean | true | — | — | Saturated sources glow saturated instead of washing to white. |

Every instance also takes `expand` (number px or `"none"`); see 01-effects-basics.md.

### `light.bloom`

After Effects: — (highlight bloom) · Phase: P1 · Status: implemented · Tiling: whole · Reads: — · Reads time: no · Device: GPU when the whole stack lowers, else CPU

Preset-like specialization of `light.glow` for adjustment layers: only values above 1.0 bloom.

| Parameter | Type | Default | Range | Anim | What it does |
|---|---|---|---|---|---|
| `threshold` | number | 1 | — | A | Working-space luminance above which pixels bloom. |
| `knee` | number | 0.5 | ≥ 0 (clamped) | A | Soft threshold width. |
| `radius` | length px | 40 | ≥ 0 (clamped) | A | Visible extent of the bloom in layer px. |
| `intensity` | number | 0.3 | ≥ 0 (clamped) | A | Bloom gain; 0 is the neutral value. |

Every instance also takes `expand` (number px or `"none"`); see 01-effects-basics.md.

### `light.rays`

After Effects: CC Light Rays / Trapcode Shine · Phase: P1 · Status: implemented · Tiling: tiled · Reads: — · Reads time: no · Device: CPU

Radial line integral (god rays) from the thresholded source toward `center`, with exponential decay exp(−3*t*) along the ray; shimmer modulates by angular noise for animated streaks.

| Parameter | Type | Default | Range | Anim | What it does |
|---|---|---|---|---|---|
| `center` | point `[x, y]` | `center` | — | A | Light source the rays radiate from. |
| `length` | percent | 50 | 0–100 (soft) | A | Ray length as a percent of each pixel's distance to the center (capped at 95). |
| `intensity` | number | 1 | ≥ 0 (clamped) | A | Ray gain; 0 is the neutral value. |
| `threshold` | number | 0.5 | — | A | Working-space luminance above which the source emits rays. |
| `tint` | color | `#FFFFFF` | — | A | Ray tint (multiplied). |
| `colorize` | gradient | none | — | A | Colours each ray by its luminance through a gradient (0 → first stop, 1 → last) instead of tinting; a ray keeps its energy, so a pixel no ray reaches is untouched. |
| `boost` | number | 0 | — | A | Stops of exposure applied to the thresholded source before integration. |
| `shimmer.amount` | percent | 0 | 0–100 (soft) | A | Angular modulation of the rays (0 = even). |
| `shimmer.detail` | number | 10 | ≥ 1 (clamped) | A | Angular frequency of the shimmer. |
| `shimmer.phase` | angle ° | 0 | — | A | Shimmer phase; animate for moving streaks. |
| `composite` | enum `add` / `screen` / `over` / `glowOnly` | `add` | — | — | How the rays combine with the layer. |
| `sourceAlpha` | boolean | false | — | — | Rays from the alpha channel (white light) instead of the color. |
| `seed` | integer seed | 0 | — | — | Random seed (spec 7 §7.5). |

Every instance also takes `expand` (number px or `"none"`) and `seed`; see 01-effects-basics.md.

### `light.flare`

After Effects: Lens Flare / Optical Flares-lite · Phase: P2 · Status: implemented · Tiling: tiled · Reads: other layers · Reads time: no · Device: CPU

A procedural flare built from elements placed along the axis from `center` through the comp center.

| Parameter | Type | Default | Range | Anim | What it does |
|---|---|---|---|---|---|
| `center` | point `[x, y]` | `["25%", "25%"]` | — | A | Where the light source is. |
| `center3d` | point3d `[x, y, z]` | none | — | A | A 3D light position (its x, y are used; null = `center`). |
| `preset` | enum `prime50` / `zoom105` / `anamorphic` / `spotlight` / `sun` / `custom` | `prime50` | — | — | Element list preset. |
| `brightness` | percent | 100 | 0–100 (soft) | A | Overall brightness. |
| `scale` | percent | 100 | 0–100 (soft) | A | Size of every element. |
| `color` | color | `#FFFFFF` | — | A | Tint of the whole flare. |
| `elements` | list of `{ kind, position, size, color, intensity, shape, softness }` | `[]` | — | A | The elements of the `custom` preset. |
| `occlusion` | layer id | none | — | — | A layer whose alpha around the center dims the flare. |
| `occlusionSource` | enum `source` / `masks` / `effects` | `effects` | — | — | What of the other layer is read (spec 7 §7.6). |
| `blend` | blend mode (any of the 38; see 20-utility-controls.md) | `add` | — | — | How the light combines with the layer (add by default). |

Every instance also takes `expand` (number px or `"none"`); see 01-effects-basics.md.

### `light.leak`

After Effects: — (light leak overlays) · Phase: P2 · Status: implemented · Tiling: tiled · Reads: — · Reads time: yes · Device: CPU

A generator of drifting, overexposed blotches of light (procedural, seeded; animated by low-frequency curl noise).

| Parameter | Type | Default | Range | Anim | What it does |
|---|---|---|---|---|---|
| `seed` | integer seed | 0 | — | — | Random seed (spec 7 §7.5). |
| `speed` | number | 1 | — | A | How fast the leaks drift (1 = one cycle per second). |
| `colors` | gradient | gradient `#FFB350` → `#FF7661` → `#ED59CB` (oklab) | — | A | The colors the leaks take. |
| `intensity` | number | 1 | 0–10 (clamped) | A | Brightness of the light. |
| `scale` | percent | 100 | 0–100 (soft) | A | Size of the leaks (percent of the layer's shorter side). |
| `position` | point `[x, y]` | `center` | — | A | Center of the drift. |
| `softness` | percent | 80 | 0–100 (soft) | A | Softness of the blotches' falloff. |
| `opacity` | percent | 100 | 0–100 (soft) | A | Opacity of the generated light. |
| `mode` | blend mode (any of the 38; see 20-utility-controls.md) | `screen` | — | — | Blend mode of the light over the layer. |
| `composite` | enum `replace` / `over` / `under` / `inside` | `over` | — | — | How generated pixels combine with the layer: replace, over, under, or inside (only where the layer is opaque). |

Every instance also takes `expand` (number px or `"none"`) and `seed`; see 01-effects-basics.md.

### `light.energy`

After Effects: Saber (Video Copilot) · Phase: P2 · Status: implemented · Tiling: whole · Reads: mask paths · Reads time: no · Device: CPU

Strokes a path (mask, the layer's alpha edge, or a text layer's glyph outlines) with a hot core and a large physically-based glow (the `light.glow` pyramid), displaced along the normal by animated curl noise.

| Parameter | Type | Default | Range | Anim | What it does |
|---|---|---|---|---|---|
| `path` | mask id | `layerAlpha` | — | — | Mask id, `layerAlpha` or `textOutlines`. |
| `coreColor` | color | `#FFFFFF` | — | A | Color of the hot core. |
| `glowColor` | color | `#2A8CFF` | — | A | Color of the glow. |
| `coreSize` | length px | 2 | ≥ 0 (clamped) | A | Core width in px. |
| `glowSize` | length px | 24 | ≥ 0 (clamped) | A | Glow extent in px. |
| `glowIntensity` | number | 1.5 | ≥ 0 (clamped) | A | Glow gain. |
| `start` | percent | 0 | 0–100 (soft) | A | Where the stroke starts, percent of the path. |
| `end` | percent | 100 | 0–100 (soft) | A | Where the stroke ends, percent of the path. |
| `offset` | percent | 0 | 0–100 (soft) | A | Shift of start and end along the path. |
| `distortion.amount` | number | 0 | ≥ 0 (clamped) | A | Displacement along the normal, px. |
| `distortion.size` | length px | 20 | ≥ 0 (clamped) | A | Feature size of the displacement noise, px. |
| `distortion.speed` | number | 1 | — | A | Animation speed of the displacement noise. |
| `distortion.octaves` | integer | 3 | 1–8 (clamped) | — | Octaves of the displacement noise. |
| `flicker` | percent | 0 | 0–100 (soft) | A | Random dimming per frame. |
| `taper.start` | percent | 0 | 0–100 (soft) | A | Percent of the stroke over which the core grows from nothing. |
| `taper.end` | percent | 0 | 0–100 (soft) | A | Percent of the stroke over which the core shrinks to nothing. |
| `composite` | enum `add` / `over` / `energyOnly` | `add` | — | — | How the energy meets the layer. |

Every instance also takes `expand` (number px or `"none"`); see 01-effects-basics.md.

### `light.neon`

After Effects: — (neon tube look) · Phase: P2 · Status: implemented · Tiling: whole · Reads: — · Reads time: no · Device: CPU

Convenience over `light.energy` on the layer's outline with no distortion and a white-hot core.

| Parameter | Type | Default | Range | Anim | What it does |
|---|---|---|---|---|---|
| `color` | color | `#FF2BD6` | — | A | Tube color. |
| `tubeWidth` | length px | 4 | ≥ 0 (clamped) | A | Tube width in px. |
| `glow` | number | 1 | ≥ 0 (clamped) | A | Glow gain. |
| `flicker.amount` | percent | 0 | 0–100 (soft) | A | Random dimming. |
| `flicker.rate` | number | 8 | ≥ 0 (clamped) | A | Flicker changes per second (Hz). |
| `off` | boolean | false | — | A | The tube unlit (hold-animatable). |

Every instance also takes `expand` (number px or `"none"`); see 01-effects-basics.md.

### `light.ccLightBurst`

After Effects: CC Light Burst 2.5 · Phase: P2 · Status: implemented · Tiling: tiled · Reads: — · Reads time: no · Device: CPU

Radial burst of the layer's pixels from `center` (`light.rays` is the Trapcode-class version).

| Parameter | Type | Default | Range | Anim | What it does |
|---|---|---|---|---|---|
| `center` | point `[x, y]` | `center` | — | A | The point the rays burst from. |
| `intensity` | number | 100 | ≥ 0 (clamped) | A | Gain of the burst (100 = 1). |
| `rayLength` | percent | 50 | 0–100 (soft) | A | Ray length as a percent of each pixel's distance to the centre (capped at 95). |
| `burst` | enum `straight` / `fade` / `center` | `straight` | — | — | Brightest sample, fade towards the pixel, or an even average. |
| `setColor` | boolean | false | — | — | Recolour the burst by its luminance in `color`. |
| `color` | color | `#FFFFFF` | — | A | The burst colour with `setColor`. |

Every instance also takes `expand` (number px or `"none"`); see 01-effects-basics.md.

### `light.ccLightSweep`

After Effects: CC Light Sweep · Phase: P2 · Status: implemented · Tiling: whole · Reads: — · Reads time: no · Device: CPU

A band of light swept across the layer with a highlight on the alpha edge (logo sheens).

| Parameter | Type | Default | Range | Anim | What it does |
|---|---|---|---|---|---|
| `center` | point `[x, y]` | `center` | — | A | A point on the band. |
| `direction` | angle ° | -30 | — | A | Direction the band runs along (0 = vertical). |
| `shape` | enum `linear` / `smooth` / `sharp` | `smooth` | — | — | Falloff to the band's sides. |
| `width` | length px | 50 | ≥ 0 (clamped) | A | Width of the band in px. |
| `sweepIntensity` | number | 50 | ≥ 0 (clamped) | A | Gain of the band (100 = 1). |
| `edgeIntensity` | number | 100 | ≥ 0 (clamped) | A | Gain of the alpha-edge highlight (100 = 1). |
| `edgeThickness` | length px | 1 | ≥ 0 (clamped) | A | Softening of the alpha before its edge is taken, px. |
| `lightColor` | color | `#FFFFFF` | — | A | Colour of the light. |
| `lightReception` | enum `add` / `composite` / `cutout` | `add` | — | — | How the layer receives the light. |

Every instance also takes `expand` (number px or `"none"`); see 01-effects-basics.md.

### `light.ccSpotlight`

After Effects: CC Spotlight · Phase: P2 · Status: implemented · Tiling: tiled · Reads: — · Reads time: no · Device: CPU

2D spotlight shading cast from `from` toward `to` (no comp lights).

| Parameter | Type | Default | Range | Anim | What it does |
|---|---|---|---|---|---|
| `light.using` | enum `effectLight` / `compLights` | `effectLight` | — | — | The effect's own light (comp lights are not read). |
| `from` | point `[x, y]` | `["30%", "20%"]` | — | A | Where the light hangs (its foot on the layer). |
| `to` | point `[x, y]` | `center` | — | A | Where the light points. |
| `height` | number | 50 | ≥ 0 (clamped) | A | Height of the light, percent of the layer's larger side. |
| `coneAngle` | number | 20 | 0.1–89.9 (clamped) | A | Half-angle of the cone in degrees. |
| `edgeSoftness` | percent | 25 | 0–100 (soft) | A | How much of the cone angle the rim softens over. |
| `color` | color | `#FFFFFF` | — | A | Colour of the light. |
| `intensity` | number | 100 | ≥ 0 (clamped) | A | Gain of the light (100 = 1). |
| `render` | enum `light` / `lightOnly` | `light` | — | — | The lit layer, or the light alone. |

Every instance also takes `expand` (number px or `"none"`); see 01-effects-basics.md.

### `light.godrays3d`

After Effects: — · Phase: P3 · Status: implemented · Tiling: tiled · Reads: — · Reads time: no · Device: CPU

Rays from a 3D point projected through the comp camera.

| Parameter | Type | Default | Range | Anim | What it does |
|---|---|---|---|---|---|
| `center` | point `[x, y]` | `center` | — | A | Light source the rays radiate from. |
| `center3d` | point3d `[x, y, z]` | none | — | A | The 3D light position the rays radiate from (on a 3D layer seen through the camera; on a 2D layer its x, y; null = `center`). |
| `length` | percent | 50 | 0–100 (soft) | A | Ray length as a percent of each pixel's distance to the center (capped at 95). |
| `intensity` | number | 1 | ≥ 0 (clamped) | A | Ray gain; 0 is the neutral value. |
| `threshold` | number | 0.5 | — | A | Working-space luminance above which the source emits rays. |
| `tint` | color | `#FFFFFF` | — | A | Ray tint (multiplied). |
| `colorize` | gradient | none | — | A | Colours each ray by its luminance through a gradient (0 → first stop, 1 → last) instead of tinting; a ray keeps its energy, so a pixel no ray reaches is untouched. |
| `boost` | number | 0 | — | A | Stops of exposure applied to the thresholded source before integration. |
| `shimmer.amount` | percent | 0 | 0–100 (soft) | A | Angular modulation of the rays (0 = even). |
| `shimmer.detail` | number | 10 | ≥ 1 (clamped) | A | Angular frequency of the shimmer. |
| `shimmer.phase` | angle ° | 0 | — | A | Shimmer phase; animate for moving streaks. |
| `composite` | enum `add` / `screen` / `over` / `glowOnly` | `add` | — | — | How the rays combine with the layer. |
| `sourceAlpha` | boolean | false | — | — | Rays from the alpha channel (white light) instead of the color. |
| `seed` | integer seed | 0 | — | — | Random seed (spec 7 §7.5). |

Every instance also takes `expand` (number px or `"none"`) and `seed`; see 01-effects-basics.md.

<!-- gen:catalogue-light-1:end -->
