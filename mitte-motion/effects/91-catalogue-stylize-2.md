# Stylize: every parameter (part 2 of 2)

Generated from `rexx-engine effects` by scripts/skills-effects-catalogue.py; do not edit by hand. Index: [90-catalogue.md](90-catalogue.md).

<!-- gen:catalogue-stylize-2:start -->
### `stylize.ccGlass`

After Effects: CC Glass · Phase: P2 · Status: implemented · Tiling: whole · Reads: other layers · Reads time: no · Device: CPU

Bump-mapped glass surface lit by the effect light; refracts by `displacement`.

| Parameter | Type | Default | Range | Anim | What it does |
|---|---|---|---|---|---|
| `bumpMap` | layer id | none | — | — | The layer whose property is the height (null = this layer). |
| `bumpMapSource` | enum `source` / `masks` / `effects` | `effects` | — | — | What of the other layer is read (spec 7 §7.6). |
| `property` | enum `red` / `green` / `blue` / `alpha` / `luminance` / `lightness` | `alpha` | — | — | Which property is the height. |
| `softness` | length px | 10 | ≥ 0 (clamped) | A | Blur of the height field (σ = half of it, px). |
| `height` | number | 50 | -100–100 (clamped) | A | Relief of the surface. |
| `displacement` | number | 100 | — | A | Refraction in quarter pixels. |
| `light.using` | enum `effectLight` / `compLights` | `effectLight` | — | — | The effect's own light (comp lights are not read). |
| `light.intensity` | percent | 100 | 0–400 (soft) | A | Light intensity. |
| `light.color` | color | `#FFFFFF` | — | A | Light color. |
| `light.type` | enum `distant` / `point` | `distant` | — | — | A distant or a point light. |
| `light.height` | number | 50 | -100–100 (clamped) | A | Elevation of the light (percent). |
| `light.position` | point `[x, y]` | `["25%", "25%"]` | — | A | Position of a point light. |
| `light.direction` | angle ° | -45 | — | A | Direction of a distant light. |
| `shading.ambient` | percent | 75 | 0–200 (soft) | A | Ambient light. |
| `shading.diffuse` | percent | 32 | 0–200 (soft) | A | Diffuse reflection. |
| `shading.specular` | percent | 26 | 0–200 (soft) | A | Specular highlight. |
| `shading.roughness` | number | 0.05 | 0.001–1 (clamped) | A | Highlight spread. |
| `shading.metal` | percent | 100 | 0–100 (soft) | A | How much the highlight takes the surface color. |

Every instance also takes `expand` (number px or `"none"`); see 01-effects-basics.md.

### `stylize.ccHexTile`

After Effects: CC HexTile · Phase: P2 · Status: implemented · Tiling: tiled · Reads: — · Reads time: no · Device: CPU

Hexagonal tiling of the layer.

| Parameter | Type | Default | Range | Anim | What it does |
|---|---|---|---|---|---|
| `render` | enum `normal` / `mirrored` / `rotated` | `normal` | — | — | How alternate cells are placed. |
| `radius` | number | 50 | 1–4000 (clamped) | A | Circumradius of a cell in px. |
| `center` | point `[x, y]` | `center` | — | A | The cell every tile repeats. |
| `rotate` | angle ° | 0 | — | A | Rotation of the tiling. |
| `smearing` | percent | 0 | 0–100 (soft) | A | Pull toward the pixel's own position. |

Every instance also takes `expand` (number px or `"none"`); see 01-effects-basics.md.

### `stylize.ccMrSmoothie`

After Effects: CC Mr. Smoothie · Phase: P2 · Status: implemented · Tiling: whole · Reads: other layers · Reads time: no · Device: CPU

Recolours by a colour map sampled from the image between `sampleA` and `sampleB`, indexed by the flow layer's `property`.

| Parameter | Type | Default | Range | Anim | What it does |
|---|---|---|---|---|---|
| `flowLayer` | layer id | none | — | — | The layer whose property selects the color (null = this layer). |
| `flowLayerSource` | enum `source` / `masks` / `effects` | `effects` | — | — | What of the other layer is read (spec 7 §7.6). |
| `property` | enum `red` / `green` / `blue` / `alpha` / `luminance` / `lightness` / `hue` / `saturation` | `luminance` | — | — | Which property selects the color. |
| `smoothness` | length px | 20 | ≥ 0 (clamped) | A | Blur of the flow field (σ = half of it, px). |
| `sampleA` | point `[x, y]` | `["25%", "50%"]` | — | A | Start of the palette sample. |
| `sampleB` | point `[x, y]` | `["75%", "50%"]` | — | A | End of the palette sample. |
| `phase` | angle ° | 0 | — | A | Rotation of the palette. |
| `colorLoop` | enum `1x` / `2x` / `3x` / `4x` | `1x` | — | — | How many times the palette loops. |

Every instance also takes `expand` (number px or `"none"`); see 01-effects-basics.md.

### `stylize.ccPlastic`

After Effects: CC Plastic · Phase: P2 · Status: implemented · Tiling: whole · Reads: other layers · Reads time: no · Device: CPU

Bump-mapped plastic surface lit by the effect light.

| Parameter | Type | Default | Range | Anim | What it does |
|---|---|---|---|---|---|
| `bumpLayer` | layer id | none | — | — | The layer whose property is the height (null = this layer). |
| `bumpLayerSource` | enum `source` / `masks` / `effects` | `effects` | — | — | What of the other layer is read (spec 7 §7.6). |
| `property` | enum `red` / `green` / `blue` / `alpha` / `luminance` / `lightness` | `alpha` | — | — | Which property is the height. |
| `softness` | length px | 10 | ≥ 0 (clamped) | A | Blur of the height field (σ = half of it, px). |
| `height` | number | 25 | -100–100 (clamped) | A | Relief of the surface. |
| `cutMin` | percent | 0 | 0–100 (soft) | A | The height field's floor. |
| `cutMax` | percent | 100 | 0–100 (soft) | A | The height field's ceiling. |
| `light.using` | enum `effectLight` / `compLights` | `effectLight` | — | — | The effect's own light (comp lights are not read). |
| `light.intensity` | percent | 100 | 0–400 (soft) | A | Light intensity. |
| `light.color` | color | `#FFFFFF` | — | A | Light color. |
| `light.type` | enum `distant` / `point` | `distant` | — | — | A distant or a point light. |
| `light.height` | number | 50 | -100–100 (clamped) | A | Elevation of the light (percent). |
| `light.position` | point `[x, y]` | `["25%", "25%"]` | — | A | Position of a point light. |
| `light.direction` | angle ° | -45 | — | A | Direction of a distant light. |
| `shading.ambient` | percent | 100 | 0–200 (soft) | A | Ambient light. |
| `shading.diffuse` | percent | 70 | 0–200 (soft) | A | Diffuse reflection. |
| `shading.specular` | percent | 50 | 0–200 (soft) | A | Specular highlight. |
| `shading.roughness` | number | 0.05 | 0.001–1 (clamped) | A | Highlight spread. |
| `shading.metal` | percent | 50 | 0–100 (soft) | A | How much the highlight takes the surface color. |

Every instance also takes `expand` (number px or `"none"`); see 01-effects-basics.md.

### `stylize.ccRepeTile`

After Effects: CC RepeTile · Phase: P2 · Status: implemented · Tiling: tiled · Reads: — · Reads time: no · Device: CPU

Grows the layer by tiling it outward (`output_bounds` grows by the four expands).

| Parameter | Type | Default | Range | Anim | What it does |
|---|---|---|---|---|---|
| `expandRight` | length px | 0 | ≥ 0 (clamped) | A | Growth to the right in px. |
| `expandLeft` | length px | 0 | ≥ 0 (clamped) | A | Growth to the left in px. |
| `expandDown` | length px | 0 | ≥ 0 (clamped) | A | Growth downward in px. |
| `expandUp` | length px | 0 | ≥ 0 (clamped) | A | Growth upward in px. |
| `tiling` | enum `repeat` / `unfold` / `checkerFlipH` / `checkerFlipV` / `checkerFlip` | `repeat` | — | — | How the copies are placed. |

Every instance also takes `expand` (number px or `"none"`); see 01-effects-basics.md.

### `stylize.ccThresholdRgb`

After Effects: CC Threshold RGB · Phase: P2 · Status: implemented · Tiling: tiled · Reads: — · Reads time: no · Device: CPU

Per-channel threshold (`color.threshold` is the luma one).

| Parameter | Type | Default | Range | Anim | What it does |
|---|---|---|---|---|---|
| `redThreshold` | number | 127 | 0–255 (clamped) | A | Red threshold (0–255). |
| `greenThreshold` | number | 127 | 0–255 (clamped) | A | Green threshold (0–255). |
| `blueThreshold` | number | 127 | 0–255 (clamped) | A | Blue threshold (0–255). |
| `invertRed` | boolean | false | — | — | Invert the red result. |
| `invertGreen` | boolean | false | — | — | Invert the green result. |
| `invertBlue` | boolean | false | — | — | Invert the blue result. |
| `blendWithOriginal` | percent | 0 | 0–100 (soft) | A | Mix back toward the layer. |

Every instance also takes `expand` (number px or `"none"`); see 01-effects-basics.md.

### `stylize.ccVignette`

After Effects: CC Vignette · Phase: P2 · Status: implemented · Tiling: tiled · Reads: — · Reads time: no · Device: CPU

Lens-model vignette (`stylize.vignette` is the Lumetri one).

| Parameter | Type | Default | Range | Anim | What it does |
|---|---|---|---|---|---|
| `amount` | number | 50 | -100–100 (clamped) | A | Strength of the falloff. |
| `angleOfView` | number | 60 | 0–179 (clamped) | A | The lens's angle of view in degrees. |
| `center` | point `[x, y]` | `center` | — | A | The lens axis. |
| `pinHighlights` | percent | 0 | 0–100 (soft) | A | Keep bright pixels bright. |

Every instance also takes `expand` (number px or `"none"`); see 01-effects-basics.md.

### `stylize.ascii`

After Effects: — · Phase: P2 · Status: implemented · Tiling: tiled · Reads: — · Reads time: no · Device: CPU

Text-art look; glyphs rasterized via the text engine.

| Parameter | Type | Default | Range | Anim | What it does |
|---|---|---|---|---|---|
| `cellSize` | length px | 8 | ≥ 0 (clamped) | A | Cell size in px. |
| `charset` | list of `char` | required | — | — | Glyphs from dark to bright (a string; default ` .:-=+*#%@`). |
| `font` | enum `mono` | `mono` | — | — | Glyph font (the built-in monospace bitmap). |
| `color` | enum `source` / `mono` | `source` | — | — | Glyphs in the cell's color, or `foreground` on `background`. |
| `foreground` | color | `#FFFFFF` | — | A | Glyph color for `mono`. |
| `background` | color | `#000000` | — | A | Cell color for `mono`. |

Every instance also takes `expand` (number px or `"none"`); see 01-effects-basics.md.

### `stylize.datamosh`

After Effects: — (datamosh) · Phase: P4 · Status: not implemented (P4: `effect.unavailable`)

Needs codec motion vectors; uses an optical-flow field from the decoder path.

No parameters are registered: the engine answers `effect.unavailable` (the message names the phase).

### `stylize.motionTrails`

After Effects: — (echo-based trails) · Phase: — · Status: not implemented (not provided: `effect.unavailable`)

Use `time.echo`.

No parameters are registered: the engine answers `effect.unavailable` (the message names the phase).

<!-- gen:catalogue-stylize-2:end -->
