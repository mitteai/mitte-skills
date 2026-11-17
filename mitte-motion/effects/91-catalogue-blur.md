# Blur & sharpen: every parameter

Generated from `rexx-engine effects` by scripts/skills-effects-catalogue.py; do not edit by hand. Index: [90-catalogue.md](90-catalogue.md).

<!-- gen:catalogue-blur-1:start -->
### `blur.gaussian`

After Effects: Gaussian Blur / Gaussian Blur (Legacy) · Phase: P1 · Status: implemented · Tiling: whole · Reads: — · Reads time: no · Device: GPU when the whole stack lowers, else CPU

True Gaussian whose visible extent is `radius` (σ = radius / 3).

| Parameter | Type | Default | Range | Anim | What it does |
|---|---|---|---|---|---|
| `radius` | length px | 0 | ≥ 0 (clamped) | A | Visible extent of the blur in layer px (σ = radius / 3). |
| `dims` | enum `both` / `horizontal` / `vertical` | `both` | — | — | Which axes are blurred. |
| `repeatEdges` | boolean | false | — | — | Sample clamped layer-edge pixels instead of transparency outside the layer. |

Every instance also takes `expand` (number px or `"none"`); see 01-effects-basics.md.

### `blur.fast`

After Effects: Fast Box Blur · Phase: P1 · Status: implemented · Tiling: whole · Reads: — · Reads time: no · Device: GPU when the whole stack lowers, else CPU

Running-sum box with fractional radius (the partial edge pixel weighted), iterated.

| Parameter | Type | Default | Range | Anim | What it does |
|---|---|---|---|---|---|
| `radius` | length px | 0 | ≥ 0 (clamped) | A | Box half-width in layer px (fractional). |
| `iterations` | integer | 3 | 1–6 (clamped) | — | Number of box passes; 3 ≈ Gaussian. |
| `dims` | enum `both` / `horizontal` / `vertical` | `both` | — | — | Which axes are blurred. |
| `repeatEdges` | boolean | false | — | — | Sample clamped layer-edge pixels instead of transparency outside the layer. |

Every instance also takes `expand` (number px or `"none"`); see 01-effects-basics.md.

### `blur.box`

After Effects: Box Blur · Phase: P2 · Status: implemented · Tiling: whole · Reads: — · Reads time: no · Device: GPU when the whole stack lowers, else CPU

As `blur.fast` with one iteration by default (the visible box shape is the point); transparent outside the layer.

| Parameter | Type | Default | Range | Anim | What it does |
|---|---|---|---|---|---|
| `radius` | length px | 0 | ≥ 0 (clamped) | A | Box half-width in layer px (fractional). |
| `iterations` | integer | 1 | 1–6 (clamped) | — | Number of box passes. |
| `dims` | enum `both` / `horizontal` / `vertical` | `both` | — | — | Which axes are blurred. |

Every instance also takes `expand` (number px or `"none"`); see 01-effects-basics.md.

### `blur.directional`

After Effects: Directional Blur · Phase: P1 · Status: implemented · Tiling: tiled · Reads: — · Reads time: no · Device: GPU when the whole stack lowers, else CPU

Line integral along the direction, sample count = ceil(length) · 2 with linear interpolation; linear-light.

| Parameter | Type | Default | Range | Anim | What it does |
|---|---|---|---|---|---|
| `direction` | angle ° | 0 | — | A | Blur direction in degrees (0 = up, 90 = right). |
| `length` | length px | 10 | ≥ 0 (clamped) | A | Total length of the blur line in layer px. |

Every instance also takes `expand` (number px or `"none"`); see 01-effects-basics.md.

### `blur.radial`

After Effects: Radial Blur / CC Radial Fast Blur / CC Radial Blur · Phase: P1 · Status: implemented · Tiling: whole · Reads: — · Reads time: no · Device: GPU when the whole stack lowers, else CPU

Zoom averages the source along the segment from the pixel `P` toward `center` `C`, the points `C + (P − C)·(1 − a·t)` for `t` in (0, 1) with `a` = `amount` / 100 capped at 0.95, transparent outside the source; spin averages along the arc about `C` over `amount` degrees.

| Parameter | Type | Default | Range | Anim | What it does |
|---|---|---|---|---|---|
| `type` | enum `spin` / `zoom` | `zoom` | — | — | Spin (degrees) or zoom (percent of the distance to the center). |
| `amount` | number | 10 | — | A | Degrees for spin, percent of distance for zoom. |
| `center` | point `[x, y]` | `center` | — | A | Center of the blur. |
| `quality` | enum `draft` / `best` | `best` | — | — | Best samples adaptively by arc length. |

Every instance also takes `expand` (number px or `"none"`); see 01-effects-basics.md.

### `blur.sharpen`

After Effects: Sharpen · Phase: P1 · Status: implemented · Tiling: tiled · Reads: — · Reads time: no · Device: GPU when the whole stack lowers, else CPU

3×3 Laplacian-based sharpen on display-encoded luma, clamped to avoid ringing beyond the input's local range.

| Parameter | Type | Default | Range | Anim | What it does |
|---|---|---|---|---|---|
| `amount` | number | 0 | 0–500 (clamped) | A | Sharpen amount (After Effects 0–500). |

Every instance also takes `expand` (number px or `"none"`); see 01-effects-basics.md.

### `blur.unsharp`

After Effects: Unsharp Mask · Phase: P1 · Status: implemented · Tiling: whole · Reads: — · Reads time: no · Device: CPU

Classic unsharp mask on display-encoded luma.

| Parameter | Type | Default | Range | Anim | What it does |
|---|---|---|---|---|---|
| `amount` | percent | 50 | 0–100 (soft) | A | Strength of the mask. |
| `radius` | length px | 1 | ≥ 0 (clamped) | A | Gaussian σ of the mask in layer px. |
| `threshold` | number | 0 | 0–255 (clamped) | A | Minimum luma difference (0–255) that is sharpened. |

Every instance also takes `expand` (number px or `"none"`); see 01-effects-basics.md.

### `blur.bilateral`

After Effects: Bilateral Blur · Phase: P2 · Status: implemented · Tiling: tiled · Reads: — · Reads time: no · Device: CPU

Edge-preserving; skin smoothing, painterly looks.

| Parameter | Type | Default | Range | Anim | What it does |
|---|---|---|---|---|---|
| `radius` | length px | 5 | ≥ 0 (clamped) | A | Window radius in px. |
| `threshold` | percent | 20 | 0–100 (soft) | A | Luma difference (percent) beyond which neighbours stop contributing. |
| `colorize` | boolean | true | — | — | Keep the color (false outputs grey). |

Every instance also takes `expand` (number px or `"none"`); see 01-effects-basics.md.

### `blur.smart`

After Effects: Smart Blur · Phase: P2 · Status: implemented · Tiling: tiled · Reads: — · Reads time: no · Device: CPU

| Parameter | Type | Default | Range | Anim | What it does |
|---|---|---|---|---|---|
| `radius` | length px | 3 | ≥ 0 (clamped) | A | Window radius in px. |
| `threshold` | percent | 25 | 0–100 (soft) | A | Luma difference (percent) within which neighbours are averaged. |
| `mode` | enum `normal` / `edgeOnly` / `edgeOverlay` | `normal` | — | — | The blur, its edges only, or the edges over the blur. |

Every instance also takes `expand` (number px or `"none"`); see 01-effects-basics.md.

### `blur.channel`

After Effects: Channel Blur · Phase: P2 · Status: implemented · Tiling: whole · Reads: — · Reads time: no · Device: CPU

Per-channel Gaussian (on unpremultiplied color for RGB).

| Parameter | Type | Default | Range | Anim | What it does |
|---|---|---|---|---|---|
| `red` | length px | 0 | ≥ 0 (clamped) | A | Visible blur extent of the red channel in px. |
| `green` | length px | 0 | ≥ 0 (clamped) | A | Visible blur extent of the green channel in px. |
| `blue` | length px | 0 | ≥ 0 (clamped) | A | Visible blur extent of the blue channel in px. |
| `alpha` | length px | 0 | ≥ 0 (clamped) | A | Visible blur extent of the alpha channel in px. |
| `dims` | enum `both` / `horizontal` / `vertical` | `both` | — | — | Which axes are blurred. |
| `repeatEdges` | boolean | false | — | — | Sample clamped layer-edge pixels instead of transparency outside the layer. |

Every instance also takes `expand` (number px or `"none"`); see 01-effects-basics.md.

### `blur.compound`

After Effects: Compound Blur · Phase: P2 · Status: implemented · Tiling: whole · Reads: other layers · Reads time: no · Device: CPU

Per-pixel Gaussian radius from map luminance; computed with a blur pyramid and trilinear interpolation between levels (fast, smooth).

| Parameter | Type | Default | Range | Anim | What it does |
|---|---|---|---|---|---|
| `map` | layer id | none | — | — | The layer whose luminance sets the blur radius (null = this layer). |
| `mapSource` | enum `source` / `masks` / `effects` | `effects` | — | — | What of the other layer is read (spec 7 §7.6). |
| `maxRadius` | length px | 20 | ≥ 0 (clamped) | A | Blur extent where the map is white, in px. |
| `invert` | boolean | false | — | — | Blur where the map is black instead. |
| `stretch` | boolean | true | — | — | Stretch the map to this layer's rect (otherwise center it). |

Every instance also takes `expand` (number px or `"none"`); see 01-effects-basics.md.

### `blur.tiltShift`

After Effects: — (common plugin look) · Phase: P2 · Status: implemented · Tiling: whole · Reads: — · Reads time: no · Device: CPU

Variable blur that grows with distance from a focus band; uses the `blur.compound` pyramid, or the lens kernel at best quality.

| Parameter | Type | Default | Range | Anim | What it does |
|---|---|---|---|---|---|
| `focusCenter` | point `[x, y]` | `center` | — | A | A point on the focus line. |
| `focusAngle` | angle ° | 90 | — | A | Direction of the focus band (0 = up: a vertical band; 90: horizontal). |
| `focusWidth` | length px | 200 | ≥ 0 (clamped) | A | Width of the sharp band in px. |
| `falloff` | length px | 300 | ≥ 0 (clamped) | A | Distance over which the blur reaches `radius`, in px. |
| `radius` | length px | 20 | ≥ 0 (clamped) | A | Blur extent far from the band, in px. |
| `iris` | enum `triangle` / `square` / `pentagon` / `hexagon` / `heptagon` / `octagon` / `nonagon` / `decagon` / `circle` | `circle` | — | — | Iris shape of the lens kernel (P3; ignored). |

Every instance also takes `expand` (number px or `"none"`); see 01-effects-basics.md.

### `blur.ccCross`

After Effects: CC Cross Blur · Phase: P2 · Status: implemented · Tiling: whole · Reads: — · Reads time: no · Device: CPU

A horizontal and a vertical blur combined by `transferMode`.

| Parameter | Type | Default | Range | Anim | What it does |
|---|---|---|---|---|---|
| `radiusX` | length px | 10 | ≥ 0 (clamped) | A | Horizontal box half-width in px. |
| `radiusY` | length px | 10 | ≥ 0 (clamped) | A | Vertical box half-width in px. |
| `transferMode` | enum `blend` / `add` / `screen` / `lighten` | `blend` | — | — | How the two blurs combine. |

Every instance also takes `expand` (number px or `"none"`); see 01-effects-basics.md.

### `blur.ccVector`

After Effects: CC Vector Blur · Phase: P2 · Status: implemented · Tiling: whole · Reads: — · Reads time: no · Device: CPU

Blur along the layer's own gradient field (the map is the layer itself, softened by `mapSoftness`).

| Parameter | Type | Default | Range | Anim | What it does |
|---|---|---|---|---|---|
| `type` | enum `natural` / `constantLength` / `perpendicular` / `directionCenter` / `directionFading` | `natural` | — | — | Where the blur direction comes from. |
| `amount` | length px | 10 | ≥ 0 (clamped) | A | Segment length in px. |
| `angleOffset` | angle ° | 0 | — | A | Added to every direction. |
| `mapSoftness` | percent | 15 | 0–100 (soft) | A | Blur of the luma map (σ = half of it, px). |

Every instance also takes `expand` (number px or `"none"`); see 01-effects-basics.md.

### `blur.camera`

After Effects: Camera Lens Blur · Phase: P3 · Status: implemented · Tiling: whole · Reads: other layers · Reads time: no · Device: CPU

Scatter-as-gather bokeh with an iris kernel, in linear light so highlights bloom into bright bokeh discs (the reason to use this instead of Gaussian).

| Parameter | Type | Default | Range | Anim | What it does |
|---|---|---|---|---|---|
| `radius` | length px | 10 | ≥ 0 (clamped) | A | Bokeh radius (px). |
| `iris` | object (group of the dotted parameters below) | none | — | — | The iris: `shape`, `roundness`, `rotation`, `aspect`, `diffraction`. |
| `iris.shape` | enum `triangle` / `square` / `pentagon` / `hexagon` / `heptagon` / `octagon` / `nonagon` / `decagon` / `circle` | `hexagon` | — | — | Shape of the iris (the bokeh). |
| `iris.roundness` | percent | 0 | 0–100 (soft) | A | Rounds the polygon toward a circle. |
| `iris.rotation` | angle ° | 0 | — | A | Rotation of the iris. |
| `iris.aspect` | number | 1 | 0.1–4 (clamped) | A | Horizontal stretch of the iris. |
| `iris.diffraction` | percent | 0 | 0–500 (soft) | A | Weight of the outer rim of each disc (100 = a natural halo, 500 = a ring). |
| `depthMap` | layer id | none | — | — | A depth layer: the radius at a pixel is `radius · \|depth − focus\|`. |
| `depthMapSource` | enum `source` / `masks` / `effects` | `effects` | — | — | What of the other layer is read (spec 7 §7.6). |
| `depthChannel` | enum `luminance` / `alpha` | `luminance` | — | — | Which channel of the depth map is the depth. |
| `focus` | percent | 0 | 0–100 (soft) | A | The depth (percent) that stays sharp. |
| `invertDepth` | boolean | false | — | — | Reverse the depth map. |
| `highlights` | object (group of the dotted parameters below) | none | — | — | Highlight boost: `gain`, `threshold`, `saturation`. |
| `highlights.gain` | number | 0 | ≥ 0 (clamped) | A | Extra brightness of pixels above the threshold. |
| `highlights.threshold` | number | 1 | — | A | Working-space luminance from which a pixel is boosted. |
| `highlights.saturation` | percent | 0 | 0–100 (soft) | A | How much colour boosted highlights keep (0 = white). |

Every instance also takes `expand` (number px or `"none"`); see 01-effects-basics.md.

### `blur.reduceInterlace`

After Effects: Reduce Interlace Flicker · Phase: P4 · Status: not implemented (P4: `effect.unavailable`)

Only for broadcast deliverables.

No parameters are registered: the engine answers `effect.unavailable` (the message names the phase).

<!-- gen:catalogue-blur-1:end -->
