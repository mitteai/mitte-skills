# Generate: every parameter (part 1 of 2)

Generated from `rexx-engine effects` by scripts/skills-effects-catalogue.py; do not edit by hand. Index: [90-catalogue.md](90-catalogue.md).

<!-- gen:catalogue-generate-1:start -->
### `generate.fill`

After Effects: Fill · Phase: P1 · Status: implemented · Tiling: tiled · Reads: mask paths · Reads time: no · Device: GPU when the whole stack lowers, else CPU

Recolors the layer's alpha; the standard way to color a footage matte or a logo.

| Parameter | Type | Default | Range | Anim | What it does |
|---|---|---|---|---|---|
| `color` | color | `#FF0000` | — | A | Fill color. |
| `opacity` | percent | 100 | 0–100 (soft) | A | Fill opacity over the layer. |
| `masks` | list of mask ids | `[]` | — | — | Mask ids the fill is restricted to (empty = all; applied by the renderer). |

Every instance also takes `expand` (number px or `"none"`); see 01-effects-basics.md.

### `generate.gradient`

After Effects: Gradient Ramp · Phase: P1 · Status: implemented · Tiling: tiled · Reads: — · Reads time: no · Device: GPU when the whole stack lowers, else CPU

Dithered by default so 8-bit renders of soft gradients do not band: blue noise of ±½ LSB at 8 bits, applied **in linear light** scaled by the encoded LSB step at the pixel's value (a lookup table of step sizes over the linear range), so the effect never encodes and decodes a pixel; it differs from a dither applied in encoded space by at most 1 LSB.

| Parameter | Type | Default | Range | Anim | What it does |
|---|---|---|---|---|---|
| `type` | enum `linear` / `radial` / `angular` / `diamond` / `reflected` | `linear` | — | — | Ramp shape. |
| `start` | point `[x, y]` | `["50%", "0%"]` | — | A | Where the gradient starts (top center). |
| `end` | point `[x, y]` | `["50%", "100%"]` | — | A | Where the gradient ends (bottom center). |
| `gradient` | gradient | gradient `#000000` → `#FFFFFF` (oklab) | — | A | The colors. |
| `interpolation` | enum `oklab` / `linear` / `srgb` | `oklab` | — | — | Space the stops interpolate in. |
| `dither` | boolean | true | — | — | Blue-noise dither (±½ LSB at 8 bits) so soft ramps do not band. |
| `scatter` | length px | 0 | ≥ 0 (clamped) | A | Random jitter of the ramp position in layer px. |
| `opacity` | percent | 100 | 0–100 (soft) | A | Opacity of the generated pixels. |
| `mode` | blend mode (any of the 38; see 20-utility-controls.md) | `normal` | — | — | Blend mode of the generated pixels over the layer. |
| `composite` | enum `replace` / `over` / `under` / `inside` | `replace` | — | — | How generated pixels combine with the layer: replace, over, under, or inside (only where the layer is opaque). |
| `seed` | integer seed | 0 | — | — | Random seed (spec 7 §7.5). |

Every instance also takes `expand` (number px or `"none"`) and `seed`; see 01-effects-basics.md.

### `generate.gradient4`

After Effects: 4-Color Gradient · Phase: P1 · Status: implemented · Tiling: tiled · Reads: — · Reads time: no · Device: GPU when the whole stack lowers, else CPU

Inverse-distance blend with exponent *q* = 200 / `blend` (100 = inverse square); the classic "mesh gradient" background.

| Parameter | Type | Default | Range | Anim | What it does |
|---|---|---|---|---|---|
| `points` | list of `{ position: point, color: color }` | `[{"position": ["10%", "10%"], "color": "#FF6633"}, {"position": ["90%", "10%"], "color": "#FFCC33"}, {"position": ["10%", "90%"], "color": "#3366FF"}, {"position": ["90%", "90%"], "color": "#9933FF"}]` | — | A | The four colored points. |
| `blend` | number | 100 | ≥ 1 (clamped) | A | Softness of the blend (100 = inverse-square distance). |
| `jitter` | percent | 0 | 0–100 (soft) | A | Random perturbation of the weights to break banding. |
| `opacity` | percent | 100 | 0–100 (soft) | A | Opacity of the generated pixels. |
| `mode` | blend mode (any of the 38; see 20-utility-controls.md) | `normal` | — | — | Blend mode of the generated pixels over the layer. |
| `composite` | enum `replace` / `over` / `under` / `inside` | `replace` | — | — | How generated pixels combine with the layer: replace, over, under, or inside (only where the layer is opaque). |
| `seed` | integer seed | 0 | — | — | Random seed (spec 7 §7.5). |

Every instance also takes `expand` (number px or `"none"`) and `seed`; see 01-effects-basics.md.

### `generate.fractalNoise`

After Effects: Fractal Noise · Phase: P1 · Status: implemented · Tiling: tiled · Reads: — · Reads time: no · Device: GPU when the whole stack lowers, else CPU

P1 ships a plain fractional-Brownian-motion noise with the full parameter set, enough for backgrounds, displacement sources, and transitions.

| Parameter | Type | Default | Range | Anim | What it does |
|---|---|---|---|---|---|
| `type` | enum `block` / `linear` / `softLinear` / `spline` | `softLinear` | — | — | Interpolation between lattice values. |
| `fractal` | enum `basic` / `turbulentBasic` / `turbulentSmooth` / `turbulentSharp` / `dynamic` / `dynamicProgressive` / `dynamicTwist` / `max` / `rocky` / `smeary` / `swirly` / `threads` / `turbulentSmear` / `cloudy` / `strands` / `smoky` | `basic` | — | — | Octave combination (P1: basic, turbulentBasic, turbulentSmooth). |
| `invert` | boolean | false | — | — | Invert the noise. |
| `contrast` | number | 100 | — | A | Contrast around 0.5. |
| `brightness` | number | 0 | — | A | Added brightness (percent of 1). |
| `overflow` | enum `clip` / `softClamp` / `wrapBack` / `allowHdr` | `allowHdr` | — | — | What happens to values outside 0–1. |
| `rotation` | angle ° | 0 | — | A | Rotation of the noise. |
| `uniformScaling` | boolean | true | — | — | Use `scale` for both axes. |
| `scale` | percent | 100 | 0–100 (soft) | A | Feature size (one lattice cell is 2 · scale px). |
| `scaleWidth` | percent | 100 | 0–100 (soft) | A | Horizontal feature size when not uniform. |
| `scaleHeight` | percent | 100 | 0–100 (soft) | A | Vertical feature size when not uniform. |
| `offset` | point `[x, y]` | `center` | — | A | Lattice origin (After Effects' Offset Turbulence). |
| `perspectiveOffset` | boolean | false | — | — | (ignored in P1) Offset sub-octaves by perspective. |
| `complexity` | number | 6 | 1–20 (clamped) | A | Number of octaves (fractional). |
| `subInfluence` | percent | 70 | 0–100 (soft) | A | Amplitude ratio between octaves. |
| `subScale` | percent | 56 | 0–100 (soft) | A | Size ratio between octaves. |
| `subRotation` | angle ° | 0 | — | A | Rotation added per octave. |
| `subOffset` | point `[x, y]` | `[0, 0]` | — | A | Offset added per octave (px). |
| `centerSubscale` | boolean | false | — | — | (ignored in P1) Scale sub-octaves about the center. |
| `evolution` | angle ° | 0 | — | A | Evolution; one revolution moves one lattice unit. |
| `cycleEvolution` | boolean | false | — | — | Loop the evolution after `cycle` revolutions. |
| `cycle` | integer | 1 | 1–100 (clamped) | — | Revolutions per loop. |
| `randomSeed` | integer | 0 | 0–100000 (clamped) | — | After Effects' random seed. |
| `opacity` | percent | 100 | 0–100 (soft) | A | Opacity of the generated pixels. |
| `mode` | blend mode (any of the 38; see 20-utility-controls.md) | `normal` | — | — | Blend mode of the generated pixels over the layer. |
| `composite` | enum `replace` / `over` / `under` / `inside` | `replace` | — | — | How generated pixels combine with the layer: replace, over, under, or inside (only where the layer is opaque). |

Every instance also takes `expand` (number px or `"none"`); see 01-effects-basics.md.

### `generate.grid`

After Effects: Grid · Phase: P1 · Status: implemented · Tiling: tiled · Reads: — · Reads time: no · Device: GPU when the whole stack lowers, else CPU

Background grids for tech/UI looks; anti-aliased lines at any border width.

| Parameter | Type | Default | Range | Anim | What it does |
|---|---|---|---|---|---|
| `anchor` | point `[x, y]` | `center` | — | A | A grid intersection. |
| `size` | point `[x, y]` | `[100, 100]` | — | A | Cell width and height in px. |
| `border` | length px | 2 | ≥ 0 (clamped) | A | Line width in px. |
| `feather` | length px | 0 | ≥ 0 (clamped) | A | Softness of the line edges in px. |
| `invert` | boolean | false | — | — | Draw the cells instead of the lines. |
| `color` | color | `#FFFFFF` | — | A | Line color. |
| `opacity` | percent | 100 | 0–100 (soft) | A | Opacity of the generated pixels. |
| `mode` | blend mode (any of the 38; see 20-utility-controls.md) | `normal` | — | — | Blend mode of the generated pixels over the layer. |
| `composite` | enum `replace` / `over` / `under` / `inside` | `replace` | — | — | How generated pixels combine with the layer: replace, over, under, or inside (only where the layer is opaque). |

Every instance also takes `expand` (number px or `"none"`); see 01-effects-basics.md.

### `generate.checkerboard`

After Effects: Checkerboard · Phase: P2 · Status: implemented · Tiling: tiled · Reads: — · Reads time: no · Device: CPU

Cells of `size` px from `anchor`, alternately `color` and transparent, with `feather` px soft edges (half a pixel of anti-aliasing otherwise).

| Parameter | Type | Default | Range | Anim | What it does |
|---|---|---|---|---|---|
| `anchor` | point `[x, y]` | `[0, 0]` | — | A | A cell corner. |
| `size` | point `[x, y]` | `[64, 64]` | — | A | Cell width and height in px. |
| `feather` | length px | 0 | ≥ 0 (clamped) | A | Softness of the cell edges in px. |
| `color` | color | `#FFFFFF` | — | A | Color of the filled cells. |
| `opacity` | percent | 100 | 0–100 (soft) | A | Opacity of the generated pixels. |
| `mode` | blend mode (any of the 38; see 20-utility-controls.md) | `normal` | — | — | Blend mode of the generated pixels over the layer. |
| `composite` | enum `replace` / `over` / `under` / `inside` | `replace` | — | — | How generated pixels combine with the layer: replace, over, under, or inside (only where the layer is opaque). |

Every instance also takes `expand` (number px or `"none"`); see 01-effects-basics.md.

### `generate.circle`

After Effects: Circle · Phase: P2 · Status: implemented · Tiling: tiled · Reads: — · Reads time: no · Device: CPU

A disc of `radius` px about `center`, or a ring whose inner edge is `edgeRadius`, a `thickness` in px, or a thickness in percent of the radius (the last also scaling the feathers by the radius), with outer and inner feathers, optionally inverted.

| Parameter | Type | Default | Range | Anim | What it does |
|---|---|---|---|---|---|
| `center` | point `[x, y]` | `center` | — | A | Center of the circle. |
| `radius` | length px | 100 | ≥ 0 (clamped) | A | Outer radius in px. |
| `edge` | enum `none` / `edgeRadius` / `thickness` / `thicknessRadius` / `thicknessFeatherRadius` | `none` | — | — | Solid disc, or how the ring's inner edge is given. |
| `edgeRadius` | length px | 50 | ≥ 0 (clamped) | A | Inner radius in px (`edgeRadius`). |
| `thickness` | number | 10 | ≥ 0 (clamped) | A | Ring thickness in px, or percent of the radius. |
| `feather.outer` | length px | 0 | ≥ 0 (clamped) | A | Outer feather in px (percent of the radius for `thicknessFeatherRadius`). |
| `feather.inner` | length px | 0 | ≥ 0 (clamped) | A | Inner feather in px (percent of the radius for `thicknessFeatherRadius`). |
| `invert` | boolean | false | — | — | Draw outside the shape instead. |
| `color` | color | `#FFFFFF` | — | A | Fill color. |
| `opacity` | percent | 100 | 0–100 (soft) | A | Opacity of the generated pixels. |
| `mode` | blend mode (any of the 38; see 20-utility-controls.md) | `normal` | — | — | Blend mode of the generated pixels over the layer. |
| `composite` | enum `replace` / `over` / `under` / `inside` | `replace` | — | — | How generated pixels combine with the layer: replace, over, under, or inside (only where the layer is opaque). |

Every instance also takes `expand` (number px or `"none"`); see 01-effects-basics.md.

### `generate.ellipse`

After Effects: Ellipse · Phase: P2 · Status: implemented · Tiling: tiled · Reads: — · Reads time: no · Device: CPU

A ring of `thickness` px on the ellipse `width` × `height` about `center`, `inside` at its middle fading to `outside` at its edges, with a `softness` percent edge.

| Parameter | Type | Default | Range | Anim | What it does |
|---|---|---|---|---|---|
| `center` | point `[x, y]` | `center` | — | A | Center of the ellipse. |
| `width` | length px | 100 | ≥ 0 (clamped) | A | Width in px. |
| `height` | length px | 60 | ≥ 0 (clamped) | A | Height in px. |
| `thickness` | length px | 10 | ≥ 0 (clamped) | A | Ring thickness in px. |
| `softness` | percent | 0 | 0–100 (soft) | A | Soft edge, percent of the thickness. |
| `inside` | color | `#FFFFFF` | — | A | Color at the middle of the ring. |
| `outside` | color | `#FF0000` | — | A | Color at the edges of the ring. |
| `opacity` | percent | 100 | 0–100 (soft) | A | Opacity of the generated pixels. |
| `mode` | blend mode (any of the 38; see 20-utility-controls.md) | `normal` | — | — | Blend mode of the generated pixels over the layer. |
| `composite` | enum `replace` / `over` / `under` / `inside` | `replace` | — | — | How generated pixels combine with the layer: replace, over, under, or inside (only where the layer is opaque). |

Every instance also takes `expand` (number px or `"none"`); see 01-effects-basics.md.

### `generate.beam`

After Effects: Beam · Phase: P2 · Status: implemented · Tiling: tiled · Reads: — · Reads time: no · Device: CPU

A segment of `length` percent of the path from `start` to `end`, positioned by `time` percent along it, `startThickness` to `endThickness` px wide (the thickness follows the beam's position between the points with `3dPerspective`, its own tail and head otherwise), `inside` at the middle fading to `outside` at the edges.

| Parameter | Type | Default | Range | Anim | What it does |
|---|---|---|---|---|---|
| `start` | point `[x, y]` | `["10%", "50%"]` | — | A | Start of the beam's path. |
| `end` | point `[x, y]` | `["90%", "50%"]` | — | A | End of the beam's path. |
| `length` | percent | 40 | 0–100 (soft) | A | Length of the beam, percent of the path. |
| `time` | percent | 0 | 0–100 (soft) | A | Position of the beam along the path. |
| `startThickness` | length px | 8 | ≥ 0 (clamped) | A | Thickness at the start in px. |
| `endThickness` | length px | 4 | ≥ 0 (clamped) | A | Thickness at the end in px. |
| `softness` | percent | 0 | 0–100 (soft) | A | Soft edge, percent of the thickness. |
| `inside` | color | `#FFFFFF` | — | A | Color at the middle of the beam. |
| `outside` | color | `#FF0000` | — | A | Color at the edges of the beam. |
| `3dPerspective` | boolean | true | — | — | Thickness follows the position between the points. |
| `opacity` | percent | 100 | 0–100 (soft) | A | Opacity of the generated pixels. |
| `mode` | blend mode (any of the 38; see 20-utility-controls.md) | `normal` | — | — | Blend mode of the generated pixels over the layer. |
| `composite` | enum `replace` / `over` / `under` / `inside` | `replace` | — | — | How generated pixels combine with the layer: replace, over, under, or inside (only where the layer is opaque). |

Every instance also takes `expand` (number px or `"none"`); see 01-effects-basics.md.

### `generate.cells`

After Effects: Cell Pattern · Phase: P2 · Status: implemented · Tiling: tiled · Reads: — · Reads time: no · Device: CPU

Worley/Voronoi cells of `size` px: one hashed point per cell, scattered by `disperse` (0 = a grid) and circling with `evolution` (one revolution per circle), shaped by `pattern` (the `…Hq` kinds take 4 × 4 samples per pixel over a wider neighbourhood), pushed through `contrast` and `overflow`, optionally inverted and tiled every `tiling.cellsHorizontal` × `tiling.cellsVertical` cells.

| Parameter | Type | Default | Range | Anim | What it does |
|---|---|---|---|---|---|
| `pattern` | enum `bubbles` / `crystals` / `plates` / `staticPlates` / `crystallize` / `pillow` / `mixedCrystals` / `tubular` / `crystalsHq` / `platesHq` / `staticPlatesHq` / `crystallizeHq` / `mixedCrystalsHq` / `tubularHq` | `bubbles` | — | — | Cell shaping. |
| `invert` | boolean | false | — | — | Invert the pattern. |
| `contrast` | percent | 100 | 0–400 (soft) | A | Contrast about mid grey. |
| `overflow` | enum `clip` / `softClamp` / `wrapBack` | `clip` | — | — | How values past the range are handled. |
| `disperse` | number | 1 | 0–1.5 (clamped) | A | Scatter of the cell points (0 = a grid). |
| `size` | length px | 60 | ≥ 0 (clamped) | A | Cell size in px. |
| `offset` | point `[x, y]` | `[0, 0]` | — | A | Pattern offset in px. |
| `tiling.enable` | boolean | false | — | — | Repeat the pattern every so many cells. |
| `tiling.cellsHorizontal` | integer | 8 | 1–1000 (clamped) | — | Cells across one tile. |
| `tiling.cellsVertical` | integer | 8 | 1–1000 (clamped) | — | Cells down one tile. |
| `evolution` | angle ° | 0 | — | A | Cell point motion; one revolution per circle. |
| `cycleEvolution` | boolean | false | — | — | Loop the evolution after `cycle` revolutions. |
| `cycle` | integer | 1 | 1–100 (clamped) | — | Revolutions per loop. |
| `randomSeed` | integer | 0 | 0–100000 (clamped) | — | After Effects' random seed. |
| `opacity` | percent | 100 | 0–100 (soft) | A | Opacity of the generated pixels. |
| `mode` | blend mode (any of the 38; see 20-utility-controls.md) | `normal` | — | — | Blend mode of the generated pixels over the layer. |
| `composite` | enum `replace` / `over` / `under` / `inside` | `replace` | — | — | How generated pixels combine with the layer: replace, over, under, or inside (only where the layer is opaque). |

Every instance also takes `expand` (number px or `"none"`); see 01-effects-basics.md.

### `generate.lensFlareSimple`

After Effects: Lens Flare · Phase: P2 · Status: implemented · Tiling: tiled · Reads: — · Reads time: no · Device: CPU

After Effects' built-in flare, for imported projects; `light.flare` is the better one.

| Parameter | Type | Default | Range | Anim | What it does |
|---|---|---|---|---|---|
| `center` | point `[x, y]` | `["25%", "25%"]` | — | A | Where the light source is. |
| `brightness` | percent | 100 | 0–300 (soft) | A | Brightness of the flare. |
| `lens` | enum `50-300zoom` / `35prime` / `105prime` | `50-300zoom` | — | — | Lens type (ghost layout). |
| `blend` | percent | 0 | 0–100 (soft) | A | Blend with the original. |

Every instance also takes `expand` (number px or `"none"`); see 01-effects-basics.md.

### `generate.meshGradient`

After Effects: — (mesh/freeform gradients) · Phase: P2 · Status: implemented · Tiling: tiled · Reads: — · Reads time: no · Device: CPU

Freeform gradient with radial basis interpolation in OKLab, optionally warped by animated noise: the animated "aurora blob" background.

| Parameter | Type | Default | Range | Anim | What it does |
|---|---|---|---|---|---|
| `points` | list of `{ position: point, color: color, radius: length }` | `[{"position": ["20%", "30%"], "color": "#7C5CFF"}, {"position": ["75%", "25%"], "color": "#22D3EE"}, {"position": ["60%", "80%"], "color": "#F472B6"}, {"position": ["25%", "85%"], "color": "#FACC15"}]` | — | A | 3–16 color points; `radius` defaults to 60 % of the layer's longer side. |
| `smoothness` | number | 1 | 0.05–10 (clamped) | A | Softness of the blend between points. |
| `warp` | object (group of the dotted parameters below) | none | — | — | The noise warp: `amount`, `scale`, `speed`. |
| `warp.amount` | length px | 0 | ≥ 0 (clamped) | A | Noise displacement of the gradient in px. |
| `warp.scale` | length px | 600 | ≥ 0 (clamped) | A | Feature size of the warp noise in px. |
| `warp.speed` | number | 0 | — | A | Warp animation speed (revolutions per second). |
| `opacity` | percent | 100 | 0–100 (soft) | A | Opacity of the generated pixels. |
| `mode` | blend mode (any of the 38; see 20-utility-controls.md) | `normal` | — | — | Blend mode of the generated pixels over the layer. |
| `composite` | enum `replace` / `over` / `under` / `inside` | `replace` | — | — | How generated pixels combine with the layer: replace, over, under, or inside (only where the layer is opaque). |

Every instance also takes `expand` (number px or `"none"`); see 01-effects-basics.md.

### `generate.curlNoise`

After Effects: Curl Noise (AE 26.3) · Phase: P2 · Status: implemented · Tiling: tiled · Reads: — · Reads time: no · Device: CPU

Divergence-free noise; `vectorField` outputs a displacement map (red/green), `flowLines` draws advected streaks (silky "flow field" generative look).

| Parameter | Type | Default | Range | Anim | What it does |
|---|---|---|---|---|---|
| `scale` | length px | 200 | ≥ 0 (clamped) | A | Feature size in px. |
| `complexity` | integer | 3 | 1–10 (clamped) | A | Number of octaves. |
| `evolution` | angle ° | 0 | — | A | Evolution; one revolution moves one lattice unit. |
| `speed` | number | 0 | — | A | Evolution added per second, in revolutions. |
| `output` | enum `vectorField` / `flowLines` / `magnitude` | `flowLines` | — | — | The vector field, flow lines, or the magnitude. |
| `lineLength` | length px | 40 | ≥ 0 (clamped) | A | Length of the flow lines in px. |
| `color` | gradient | gradient `#000000` → `#FFFFFF` (oklab) | — | A | Colors of the flow lines / magnitude. |
| `seed` | integer seed | 0 | — | — | Random seed (spec 7 §7.5). |
| `opacity` | percent | 100 | 0–100 (soft) | A | Opacity of the generated pixels. |
| `mode` | blend mode (any of the 38; see 20-utility-controls.md) | `normal` | — | — | Blend mode of the generated pixels over the layer. |
| `composite` | enum `replace` / `over` / `under` / `inside` | `replace` | — | — | How generated pixels combine with the layer: replace, over, under, or inside (only where the layer is opaque). |

Every instance also takes `expand` (number px or `"none"`) and `seed`; see 01-effects-basics.md.

### `generate.stroke`

After Effects: Stroke · Phase: P2 · Status: implemented · Tiling: whole · Reads: mask paths · Reads time: no · Device: CPU

Strokes masks of the layer; for shape layers prefer the shape stroke ([spec 4](04-shapes.md)).

| Parameter | Type | Default | Range | Anim | What it does |
|---|---|---|---|---|---|
| `path` | mask id | none | — | — | Mask id to stroke (`all` for every mask; none = the first mask). |
| `sequential` | boolean | true | — | — | With `all`, stroke the masks one after the other (start/end run over the sum). |
| `color` | color | `#FFFFFF` | — | A | Brush color. |
| `size` | length px | 2 | ≥ 0 (clamped) | A | Brush size in px. |
| `hardness` | percent | 100 | 0–100 (soft) | A | Fraction of the brush that is fully opaque. |
| `opacity` | percent | 100 | 0–100 (soft) | A | Paint opacity. |
| `start` | percent | 0 | 0–100 (soft) | A | Where the stroke starts, percent of the path length. |
| `end` | percent | 100 | 0–100 (soft) | A | Where the stroke ends, percent of the path length. |
| `spacing` | percent | 15 | 0–100 (soft) | A | Dab spacing, percent of the brush size (up to 50 % paints a continuous line). |
| `paintStyle` | enum `onOriginal` / `onTransparent` / `revealOriginal` | `onOriginal` | — | — | How the paint meets the layer. |

Every instance also takes `expand` (number px or `"none"`); see 01-effects-basics.md.

### `generate.vegas`

After Effects: Vegas · Phase: P2 · Status: implemented · Tiling: whole · Reads: mask paths · Reads time: no · Device: CPU

Marching-ants / chasing lights along contours.

| Parameter | Type | Default | Range | Anim | What it does |
|---|---|---|---|---|---|
| `path` | mask id | `imageContours` | — | — | Mask id to trace, or `imageContours` for the layer's own contours. |
| `channel` | enum `intensity` / `red` / `green` / `blue` / `alpha` | `intensity` | — | — | Image contours: the channel traced. |
| `invert` | boolean | false | — | — | Image contours: trace the channel inverted. |
| `threshold` | percent | 50 | 0–100 (soft) | A | Image contours: the iso-level traced. |
| `preBlur` | length px | 1 | ≥ 0 (clamped) | A | Image contours: blur before tracing (px). |
| `tolerance` | number | 0.01 | 0–1 (clamped) | A | Image contours: simplification, a fraction of the layer size. |
| `segments` | integer | 32 | 1–1000 (clamped) | A | Dashes per contour. |
| `length` | number | 0.5 | 0–1 (clamped) | A | Each dash's share of its slot. |
| `segmentDistribution` | enum `bunched` / `even` | `bunched` | — | — | Even slots, or slots jittered along the path. |
| `rotation` | angle ° | 0 | — | A | Where the dashes sit along the path (one turn = once around). |
| `randomPhase` | boolean | false | — | — | Each contour starts its dashes at a random phase. |
| `seed` | integer seed | 0 | — | — | Random seed (spec 7 §7.5). |
| `blend` | enum `transparent` / `over` / `under` / `stencil` | `over` | — | — | How the lights meet the layer. |
| `color` | color | `#FFFFFF` | — | A | Light color. |
| `width` | length px | 2 | ≥ 0 (clamped) | A | Light width in px. |
| `hardness` | number | 0.5 | 0–1 (clamped) | A | Fraction of the width that is fully opaque. |
| `startOpacity` | number | 1 | 0–1 (clamped) | A | Opacity at a dash's start. |
| `midOpacity` | number | 0.5 | 0–1 (clamped) | A | Opacity at `midPosition`. |
| `midPosition` | number | 0.5 | 0–1 (clamped) | A | Where along the dash the mid opacity sits. |
| `endOpacity` | number | 0 | 0–1 (clamped) | A | Opacity at a dash's end. |

Every instance also takes `expand` (number px or `"none"`) and `seed`; see 01-effects-basics.md.

### `generate.scribble`

After Effects: Scribble · Phase: P2 · Status: implemented · Tiling: whole · Reads: mask paths · Reads time: yes · Device: CPU

Hand-drawn scribble fills: a strong 2026 "human-made" look.

| Parameter | Type | Default | Range | Anim | What it does |
|---|---|---|---|---|---|
| `path` | mask id | `all` | — | — | Mask id to fill, or `all` for every mask. |
| `fillType` | enum `inside` / `centeredEdge` / `insideEdge` / `outsideEdge` / `leftEdge` / `rightEdge` | `inside` | — | — | What is filled: the inside, or a band at the edge. |
| `edgeWidth` | length px | 10 | ≥ 0 (clamped) | A | Width of the edge band (px). |
| `color` | color | `#FF0000` | — | A | Stroke color. |
| `opacity` | percent | 100 | 0–100 (soft) | A | Stroke opacity. |
| `angle` | angle ° | 45 | — | A | Direction of the zig-zag lines. |
| `strokeWidth` | length px | 2 | ≥ 0 (clamped) | A | Stroke width (px). |
| `curviness` | percent | 50 | 0–100 (soft) | A | How round the turns are. |
| `curvinessVariation` | percent | 50 | 0–100 (soft) | A | Random variation of the curviness. |
| `spacing` | length px | 5 | ≥ 0 (clamped) | A | Distance between lines (px). |
| `spacingVariation` | percent | 50 | 0–100 (soft) | A | Random variation of the spacing. |
| `pathOverlap` | percent | 0 | -100–100 (soft) | A | How far lines overshoot the edge, percent of the spacing. |
| `pathOverlapVariation` | percent | 50 | 0–100 (soft) | A | Random variation of the overlap. |
| `start` | percent | 0 | 0–100 (soft) | A | Where the stroke starts, percent of its length. |
| `end` | percent | 100 | 0–100 (soft) | A | Where the stroke ends, percent of its length. |
| `startEndApplyTo` | enum `allStrokes` / `eachStroke` | `allStrokes` | — | — | Start/end over all strokes together, or each on its own. |
| `fillPathsSequentially` | boolean | true | — | — | With `all`, fill the masks one after the other. |
| `wiggleType` | enum `static` / `jumpy` / `smooth` | `jumpy` | — | — | How the lines redraw over time. |
| `wigglesPerSecond` | number | 5 | ≥ 0 (clamped) | A | Redraws per second. |
| `seed` | integer seed | 0 | — | — | Random seed (spec 7 §7.5). |
| `composite` | enum `onOriginal` / `onTransparent` / `revealOriginal` | `onOriginal` | — | — | How the paint meets the layer. |

Every instance also takes `expand` (number px or `"none"`) and `seed`; see 01-effects-basics.md.

### `generate.radioWaves`

After Effects: Radio Waves · Phase: P2 · Status: implemented · Tiling: whole · Reads: mask paths, parameter history · Reads time: yes · Device: CPU

Concentric ripples; ping/notification effects.

| Parameter | Type | Default | Range | Anim | What it does |
|---|---|---|---|---|---|
| `producer` | point `[x, y]` | `center` | — | A | Where waves are born. |
| `parametersAt` | enum `birth` / `eachFrame` | `birth` | — | — | Whether a wave keeps its birth values or follows the current ones. |
| `quality` | number | 4 | 1–10 (clamped) | A | Edge anti-aliasing (higher is crisper). |
| `shape` | enum `polygon` / `imageContours` / `mask` | `polygon` | — | — | The wave's shape. |
| `sides` | integer | 64 | 3–64 (clamped) | A | Polygon sides (64 = circle). |
| `star` | boolean | false | — | — | A star instead of a polygon. |
| `starDepth` | number | -0.3 | -1–1 (clamped) | A | How deep the star's inner points sit. |
| `curvature` | number | 0 | 0–1 (clamped) | A | Rounds the polygon toward a circle. |
| `threshold` | percent | 50 | 0–100 (soft) | A | Image contours: the alpha level traced. |
| `path` | mask id | none | — | — | Mask id for `shape: mask` (none = the first mask). |
| `frequency` | number | 1 | ≥ 0.01 (clamped) | A | Waves born per second. |
| `expansion` | number | 100 | ≥ 0 (clamped) | A | Growth in px per second. |
| `orientation` | angle ° | 0 | — | A | Rotation of every wave's shape. |
| `direction` | angle ° | 90 | — | A | Drift direction. |
| `velocity` | number | 0 | ≥ 0 (clamped) | A | Drift speed in px per second. |
| `spin` | angle ° | 0 | — | A | Rotation per second. |
| `lifespan` | number | 2 | ≥ 0.01 (clamped) | A | Seconds a wave lives. |
| `reflection` | boolean | false | — | — | Drifting waves bounce off the layer's edges. |
| `profile` | enum `square` / `taperFront` / `taperBack` / `taperBoth` / `sine` / `sawtoothOut` / `sawtoothIn` | `square` | — | — | Opacity across the stroke's width. |
| `color` | color | `#FFFFFF` | — | A | Wave color. |
| `opacity` | percent | 100 | 0–100 (soft) | A | Wave opacity. |
| `fadeIn` | number | 0 | ≥ 0 (clamped) | A | Seconds a wave takes to appear. |
| `fadeOut` | number | 0 | ≥ 0 (clamped) | A | Seconds a wave takes to vanish. |
| `startWidth` | length px | 5 | ≥ 0 (clamped) | A | Stroke width at birth (px). |
| `endWidth` | length px | 5 | ≥ 0 (clamped) | A | Stroke width at the end of its life (px). |

Every instance also takes `expand` (number px or `"none"`); see 01-effects-basics.md.

### `generate.audioSpectrum`

After Effects: Audio Spectrum · Phase: P2 · Status: implemented · Tiling: whole · Reads: other layers, mask paths · Reads time: no · Device: CPU

Spectrum from the audio analysis of [spec 10](10-media-and-audio.md#audio-analysis) (FFT computed once per render, deterministic).

| Parameter | Type | Default | Range | Anim | What it does |
|---|---|---|---|---|---|
| `audio` | layer id | none | — | — | The audio or video layer analysed. |
| `path` | mask id | none | — | — | Mask id to draw along (none = the start → end line). |
| `start` | point `[x, y]` | `["10%", "50%"]` | — | A | Start of the baseline. |
| `end` | point `[x, y]` | `["90%", "50%"]` | — | A | End of the baseline. |
| `startFrequency` | number | 20 | ≥ 1 (clamped) | A | Lowest band, Hz. |
| `endFrequency` | number | 12000 | ≥ 1 (clamped) | A | Highest band, Hz. |
| `bands` | integer | 64 | 1–4096 (clamped) | A | Number of bands. |
| `maxHeight` | length px | 300 | ≥ 0 (clamped) | A | Height of a full-scale band (px). |
| `duration` | number | 90 | ≥ 1 (clamped) | A | Analysis window, ms. |
| `offset` | number | 0 | — | A | Window shift, ms. |
| `thickness` | length px | 4 | ≥ 0 (clamped) | A | Mark thickness (px). |
| `softness` | percent | 0 | 0–100 (soft) | A | Halo width, percent of the thickness. |
| `insideColor` | color | `#FFFFFF` | — | A | Core color. |
| `outsideColor` | color | `#3366FF` | — | A | Halo color. |
| `side` | enum `a` / `b` / `ab` | `a` | — | — | Which side of the baseline the bands rise on. |
| `display` | enum `digital` / `analogLines` / `analogDots` | `digital` | — | — | Bars, a line through the peaks, or dots. |
| `compositeOnOriginal` | boolean | false | — | — | Draw over the layer instead of alone. |

Every instance also takes `expand` (number px or `"none"`); see 01-effects-basics.md.

### `generate.audioWaveform`

After Effects: Audio Waveform · Phase: P2 · Status: implemented · Tiling: whole · Reads: other layers, mask paths · Reads time: no · Device: CPU

| Parameter | Type | Default | Range | Anim | What it does |
|---|---|---|---|---|---|
| `audio` | layer id | none | — | — | The audio or video layer read. |
| `path` | mask id | none | — | — | Mask id to draw along (none = the start → end line). |
| `start` | point `[x, y]` | `["10%", "50%"]` | — | A | Start of the baseline. |
| `end` | point `[x, y]` | `["90%", "50%"]` | — | A | End of the baseline. |
| `displayedSamples` | integer | 64 | 2–4096 (clamped) | — | Marks along the baseline. |
| `maxHeight` | length px | 100 | ≥ 0 (clamped) | A | Height of a full-scale sample (px). |
| `duration` | number | 200 | ≥ 1 (clamped) | A | Window, ms. |
| `offset` | number | 0 | — | A | Window shift, ms. |
| `thickness` | length px | 2 | ≥ 0 (clamped) | A | Mark thickness (px). |
| `softness` | percent | 10 | 0–100 (soft) | A | Halo width, percent of the thickness. |
| `insideColor` | color | `#FFFFFF` | — | A | Core color. |
| `outsideColor` | color | `#3366FF` | — | A | Halo color. |
| `display` | enum `digital` / `analogLines` / `analogDots` | `analogLines` | — | — | Bars, a line through the samples, or dots. |
| `compositeOnOriginal` | boolean | false | — | — | Draw over the layer instead of alone. |

Every instance also takes `expand` (number px or `"none"`); see 01-effects-basics.md.

### `generate.turbulentNoise`

After Effects: Turbulent Noise · Phase: P2 · Status: implemented · Tiling: tiled · Reads: — · Reads time: no · Device: GPU when the whole stack lowers, else CPU

The Turbulent Noise variant of the fractal-noise engine: `turbulenceFactor` folds the noise per octave.

| Parameter | Type | Default | Range | Anim | What it does |
|---|---|---|---|---|---|
| `type` | enum `block` / `linear` / `softLinear` / `spline` | `softLinear` | — | — | Interpolation between lattice values. |
| `fractal` | enum `basic` / `turbulentBasic` / `turbulentSmooth` / `turbulentSharp` / `dynamic` / `dynamicProgressive` / `dynamicTwist` / `max` / `rocky` / `smeary` / `swirly` / `threads` / `turbulentSmear` / `cloudy` / `strands` / `smoky` | `turbulentBasic` | — | — | Octave combination (basic, turbulentBasic, turbulentSmooth). |
| `invert` | boolean | false | — | — | Invert the noise. |
| `contrast` | number | 100 | — | A | Contrast around 0.5. |
| `brightness` | number | 0 | — | A | Added brightness (percent of 1). |
| `overflow` | enum `clip` / `softClamp` / `wrapBack` / `allowHdr` | `clip` | — | — | What happens to values outside 0–1. |
| `rotation` | angle ° | 0 | — | A | Rotation of the noise. |
| `uniformScaling` | boolean | true | — | — | Use `scale` for both axes. |
| `scale` | percent | 100 | 0–100 (soft) | A | Feature size (one lattice cell is 2 · scale px). |
| `scaleWidth` | percent | 100 | 0–100 (soft) | A | Horizontal feature size when not uniform. |
| `scaleHeight` | percent | 100 | 0–100 (soft) | A | Vertical feature size when not uniform. |
| `offset` | point `[x, y]` | `center` | — | A | Lattice origin (After Effects' Offset Turbulence). |
| `perspectiveOffset` | boolean | false | — | — | (ignored) Offset sub-octaves by perspective. |
| `complexity` | number | 6 | 1–20 (clamped) | A | Number of octaves (fractional). |
| `subInfluence` | percent | 70 | 0–100 (soft) | A | Amplitude ratio between octaves. |
| `subScale` | percent | 56 | 0–100 (soft) | A | Size ratio between octaves. |
| `subRotation` | angle ° | 0 | — | A | Rotation added per octave. |
| `subOffset` | point `[x, y]` | `[0, 0]` | — | A | Offset added per octave (px). |
| `centerSubscale` | boolean | false | — | — | (ignored) Scale sub-octaves about the center. |
| `evolution` | angle ° | 0 | — | A | Evolution; one revolution moves one lattice unit. |
| `cycleEvolution` | boolean | false | — | — | Loop the evolution after `cycle` revolutions. |
| `cycle` | integer | 1 | 1–100 (clamped) | — | Revolutions per loop. |
| `evolutionOptions.turbulenceFactor` | number | 0.5 | 0–10 (clamped) | A | How much faster each finer octave evolves. |
| `randomSeed` | integer | 0 | 0–100000 (clamped) | — | After Effects' random seed. |
| `opacity` | percent | 100 | 0–100 (soft) | A | Opacity of the generated pixels. |
| `mode` | blend mode (any of the 38; see 20-utility-controls.md) | `normal` | — | — | Blend mode of the generated pixels over the layer. |
| `composite` | enum `replace` / `over` / `under` / `inside` | `replace` | — | — | How generated pixels combine with the layer: replace, over, under, or inside (only where the layer is opaque). |

Every instance also takes `expand` (number px or `"none"`); see 01-effects-basics.md.

### `generate.eyedropperFill`

After Effects: Eyedropper Fill · Phase: P2 · Status: implemented · Tiling: tiled · Reads: — · Reads time: no · Device: CPU

Fills with the colour sampled at `samplePoint` (current frame).

| Parameter | Type | Default | Range | Anim | What it does |
|---|---|---|---|---|---|
| `samplePoint` | point `[x, y]` | `center` | — | A | Where the colour is sampled. |
| `sampleRadius` | length px | 0 | ≥ 0 (clamped) | A | Radius of the averaged disc (px). |
| `averagePixelColors` | enum `skipEmpty` / `all` / `allPremultiplied` / `includingAlpha` | `skipEmpty` | — | — | How the disc's pixels are averaged. |
| `maintainOriginalAlpha` | boolean | false | — | — | Keep the layer's alpha. |
| `blendWithOriginal` | percent | 0 | 0–100 (soft) | A | Mix of the untouched layer in the result. |

Every instance also takes `expand` (number px or `"none"`); see 01-effects-basics.md.

### `generate.ccThreads`

After Effects: CC Threads · Phase: P2 · Status: implemented · Tiling: tiled · Reads: — · Reads time: no · Device: CPU

Woven-thread texture over the layer.

| Parameter | Type | Default | Range | Anim | What it does |
|---|---|---|---|---|---|
| `width` | length px | 50 | ≥ 0 (clamped) | A | Cell width (px). |
| `height` | length px | 50 | ≥ 0 (clamped) | A | Cell height (px). |
| `overlaps` | integer | 1 | 1–20 (clamped) | A | Threads per twill step. |
| `direction` | angle ° | 0 | — | A | Rotation of the weave. |
| `center` | point `[x, y]` | `center` | — | A | Where the weave is anchored. |
| `coverage` | percent | 80 | 0–100 (soft) | A | The thread's share of its cell. |
| `shadowing` | percent | 50 | 0–100 (soft) | A | Darkening across the thread and where it dives under. |
| `texture` | percent | 10 | 0–100 (soft) | A | Fibre texture along the thread. |

Every instance also takes `expand` (number px or `"none"`); see 01-effects-basics.md.

### `generate.fractal`

After Effects: Fractal · Phase: P2 · Status: implemented · Tiling: tiled · Reads: — · Reads time: no · Device: CPU

Mandelbrot/Julia set generator; the escape iteration is f64 (EffectCraft notes it cannot run in f32 shaders).

| Parameter | Type | Default | Range | Anim | What it does |
|---|---|---|---|---|---|
| `set` | enum `mandelbrot` / `mandelbrotInverse` / `mandelbrotOverJulia` / `mandelbrotInverseOverJulia` / `julia` / `juliaInverse` | `mandelbrot` | — | — | Which set is drawn. |
| `equation` | enum `z2` / `z3` / `z4` | `z2` | — | — | The iterated power. |
| `mandelbrot.x` | number | -0.74 | -2–2 (soft) | A | Mandelbrot centre (real). |
| `mandelbrot.y` | number | 0.15 | -2–2 (soft) | A | Mandelbrot centre (imaginary). |
| `mandelbrot.magnification` | number | 0 | -5–30 (clamped) | A | Mandelbrot zoom (powers of two). |
| `mandelbrot.escapeLimit` | number | 4 | 1.01–1000 (clamped) | A | Mandelbrot escape radius. |
| `julia.x` | number | 0 | -2–2 (soft) | A | Julia centre (real). |
| `julia.y` | number | 0 | -2–2 (soft) | A | Julia centre (imaginary). |
| `julia.magnification` | number | 0 | -5–30 (clamped) | A | Julia zoom (powers of two). |
| `julia.escapeLimit` | number | 4 | 1.01–1000 (clamped) | A | Julia escape radius. |
| `postInversionOffset` | point `[x, y]` | `[0, 0]` | — | A | Offset added after the inversion. |
| `color.overlay` | boolean | false | — | — | Draw the set over the layer. |
| `color.transparency` | boolean | false | — | — | The inside of the set is transparent. |
| `color.palette` | enum `lightnessGradient` / `hueWheel` / `blackAndWhite` / `solidColor` | `lightnessGradient` | — | — | How the escape count is coloured. |
| `color.hue` | angle ° | 0 | — | A | Base hue of the palette. |
| `color.cycleSteps` | integer | 32 | 1–1000 (clamped) | A | Escape counts per palette cycle. |
| `color.cycleOffset` | angle ° | 0 | — | A | Phase of the palette cycle. |
| `color.edgeHighlight` | boolean | false | — | — | Lighten the band edges. |
| `oversample.method` | enum `edgeDetect` / `bruteForce` | `edgeDetect` | — | — | Where to supersample. |
| `oversample.factor` | integer | 2 | 1–9 (clamped) | — | Samples per axis where supersampled. |

Every instance also takes `expand` (number px or `"none"`); see 01-effects-basics.md.

<!-- gen:catalogue-generate-1:end -->
