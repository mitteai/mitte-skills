# Stylize: every parameter (part 1 of 2)

Generated from `rexx-engine effects` by scripts/skills-effects-catalogue.py; do not edit by hand. Index: [90-catalogue.md](90-catalogue.md).

<!-- gen:catalogue-stylize-1:start -->
### `stylize.median`

After Effects: Median / Median (Legacy) · Phase: P2 · Status: implemented · Tiling: whole · Reads: — · Reads time: no · Device: CPU

Median filter; neutral value `radius: 0`.

| Parameter | Type | Default | Range | Anim | What it does |
|---|---|---|---|---|---|
| `radius` | length px | 0 | ≥ 0 (clamped) | A | Window half-width in px (0–255, rounded). |
| `operateOnAlpha` | boolean | false | — | — | Take the median of the alpha too. |

Every instance also takes `expand` (number px or `"none"`); see 01-effects-basics.md.

### `stylize.dustScratches`

After Effects: Dust & Scratches · Phase: P2 · Status: implemented · Tiling: whole · Reads: — · Reads time: no · Device: CPU

Median where the pixel differs from its neighbourhood median by more than `threshold`.

| Parameter | Type | Default | Range | Anim | What it does |
|---|---|---|---|---|---|
| `radius` | length px | 1 | ≥ 0 (clamped) | A | Window half-width in px (0–255, rounded). |
| `threshold` | number | 0 | 0–255 (clamped) | A | Smallest difference replaced (0–255). |
| `operateOnAlpha` | boolean | false | — | — | Take the median of the alpha too. |

Every instance also takes `expand` (number px or `"none"`); see 01-effects-basics.md.

### `stylize.noiseAlpha`

After Effects: Noise Alpha · Phase: P2 · Status: implemented · Tiling: tiled · Reads: — · Reads time: no · Device: CPU

Noise on the alpha channel; the `animation` kinds advance with `noisePhase`.

| Parameter | Type | Default | Range | Anim | What it does |
|---|---|---|---|---|---|
| `noise` | enum `uniformRandom` / `squaredRandom` / `uniformAnimation` / `squaredAnimation` | `uniformRandom` | — | — | The noise distribution and whether it animates. |
| `amount` | percent | 0 | 0–100 (soft) | A | Noise strength. |
| `originalAlpha` | enum `add` / `clamp` / `scale` / `edges` | `clamp` | — | — | How the noise meets the layer's alpha. |
| `overflow` | enum `clip` / `wrapBack` / `wrap` | `clip` | — | — | What happens outside 0–1. |
| `seed` | integer seed | 0 | — | — | Random seed (spec 7 §7.5). |
| `noisePhase` | angle ° | 0 | — | A | Phase of the noise (360° = a new pattern). |
| `noiseOptions.cycleNoise` | boolean | false | — | — | Repeat the patterns every `cycle` revolutions. |
| `noiseOptions.cycle` | integer | 1 | 1–100 (clamped) | — | Revolutions per cycle. |

Every instance also takes `expand` (number px or `"none"`) and `seed`; see 01-effects-basics.md.

### `stylize.noiseHls`

After Effects: Noise HLS · Phase: P2 · Status: implemented · Tiling: tiled · Reads: — · Reads time: no · Device: CPU

Noise in HLS, advanced by `noisePhase`.

| Parameter | Type | Default | Range | Anim | What it does |
|---|---|---|---|---|---|
| `noise` | enum `uniform` / `squared` / `grain` | `uniform` | — | — | The noise distribution. |
| `hue` | percent | 0 | 0–100 (soft) | A | Hue noise. |
| `lightness` | percent | 0 | 0–100 (soft) | A | Lightness noise. |
| `saturation` | percent | 0 | 0–100 (soft) | A | Saturation noise. |
| `grainSize` | number | 1 | 0.1–100 (clamped) | A | Grain cell size in px (`grain`). |
| `noisePhase` | angle ° | 0 | — | A | Phase of the noise (360° = a new pattern). |

Every instance also takes `expand` (number px or `"none"`); see 01-effects-basics.md.

### `stylize.noiseHlsAuto`

After Effects: Noise HLS Auto · Phase: P2 · Status: implemented · Tiling: tiled · Reads: — · Reads time: yes · Device: CPU

Noise HLS animated by time × `noiseAnimationSpeed`.

| Parameter | Type | Default | Range | Anim | What it does |
|---|---|---|---|---|---|
| `noise` | enum `uniform` / `squared` / `grain` | `uniform` | — | — | The noise distribution. |
| `hue` | percent | 0 | 0–100 (soft) | A | Hue noise. |
| `lightness` | percent | 0 | 0–100 (soft) | A | Lightness noise. |
| `saturation` | percent | 0 | 0–100 (soft) | A | Saturation noise. |
| `grainSize` | number | 1 | 0.1–100 (clamped) | A | Grain cell size in px (`grain`). |
| `noiseAnimationSpeed` | number | 10 | ≥ 0 (clamped) | A | Patterns per second. |

Every instance also takes `expand` (number px or `"none"`); see 01-effects-basics.md.

### `stylize.removeGrain`

After Effects: Remove Grain · Phase: P2 · Status: implemented · Tiling: whole · Reads: — · Reads time: no · Device: CPU

Noise reduction from samples of the current frame; `temporalFiltering.enabled` reads neighbouring frames (`Deps::times`).

| Parameter | Type | Default | Range | Anim | What it does |
|---|---|---|---|---|---|
| `preview.mode` | enum `finalOutput` / `noiseSamples` / `blendingMatte` | `finalOutput` | — | — | Viewing mode (kept for import; the final output is rendered). |
| `noiseReduction.amount` | number | 1 | 0–5 (clamped) | A | Smoothing strength. |
| `noiseReduction.passes` | integer | 1 | 1–8 (clamped) | — | Guided-filter passes. |
| `noiseReduction.mode` | enum `multichannel` / `singleChannel` | `multichannel` | — | — | Guide every channel by the luma, or each by itself. |
| `fineTuning.texture` | number | 0 | 0–1 (clamped) | A | Fine detail let back through. |
| `unsharpMask.amount` | percent | 0 | 0–500 (soft) | A | Edge contrast restored. |
| `unsharpMask.radius` | length px | 1 | ≥ 0 (clamped) | A | Unsharp mask σ in px. |
| `unsharpMask.threshold` | number | 0 | 0–255 (clamped) | A | Smallest contrast sharpened (0–255). |
| `temporalFiltering.enabled` | boolean | false | — | — | Average steady pixels with the neighbouring frames. |
| `temporalFiltering.amount` | percent | 100 | 0–100 (soft) | A | Strength of the temporal average. |
| `temporalFiltering.motionSensitivity` | number | 0.5 | 0–1 (clamped) | A | How readily moving areas are left out. |
| `sampling.numberOfSamples` | integer | 80 | 1–500 (clamped) | — | Sample boxes measured. |
| `sampling.sampleSize` | integer | 9 | 3–64 (clamped) | — | Sample box side in px. |

Every instance also takes `expand` (number px or `"none"`); see 01-effects-basics.md.

### `stylize.brushStrokes`

After Effects: Brush Strokes · Phase: P3 · Status: implemented · Tiling: tiled · Reads: — · Reads time: no · Device: CPU

After Effects' defaults.

| Parameter | Type | Default | Range | Anim | What it does |
|---|---|---|---|---|---|
| `angle` | angle ° | 135 | — | A | Stroke direction (0 = up, clockwise). |
| `size` | length px | 2 | ≥ 0 (clamped) | A | Brush size in px. |
| `length` | length px | 4 | ≥ 0 (clamped) | A | Stroke length in px. |
| `density` | number | 1 | 0–2 (clamped) | A | Share of cells that paint (1 and above: all). |
| `randomness` | number | 1 | 0–2 (clamped) | A | Variation of direction and length. |
| `surface` | enum `paintOnOriginal` / `paintOnTransparent` / `paintOnWhite` / `paintOnBlack` | `paintOnOriginal` | — | — | What the strokes are painted on. |
| `blend` | percent | 0 | 0–100 (soft) | A | Mix with the original layer. |
| `seed` | integer seed | 0 | — | — | Random seed (spec 7 §7.5). |

Every instance also takes `expand` (number px or `"none"`) and `seed`; see 01-effects-basics.md.

### `stylize.dropShadow`

After Effects: Drop Shadow · Phase: P1 · Status: implemented · Tiling: whole · Reads: — · Reads time: no · Device: CPU

In layer space (rotates with the layer; use the layer style `dropShadow` for a comp-space shadow).

| Parameter | Type | Default | Range | Anim | What it does |
|---|---|---|---|---|---|
| `color` | color | `#000000` | — | A | Shadow color. |
| `opacity` | percent | 50 | 0–100 (soft) | A | Shadow opacity. |
| `direction` | angle ° | 135 | — | A | Direction of the offset (0 = up, 135 = down-right). |
| `distance` | length px | 5 | ≥ 0 (clamped) | A | Offset in px. |
| `softness` | length px | 0 | ≥ 0 (clamped) | A | Visible blur extent in px (σ = softness / 3). |
| `spread` | percent | 0 | 0–100 (soft) | A | Dilation of the shadow before blurring, as a percent of `softness`. |
| `shadowOnly` | boolean | false | — | — | Output only the shadow. |

Every instance also takes `expand` (number px or `"none"`); see 01-effects-basics.md.

### `stylize.longShadow`

After Effects: — (flat long shadow) · Phase: P1 · Status: implemented · Tiling: whole · Reads: — · Reads time: no · Device: CPU

Exact sweep of the alpha along the direction (not repeated copies), so the shadow edge is clean at any length.

| Parameter | Type | Default | Range | Anim | What it does |
|---|---|---|---|---|---|
| `direction` | angle ° | 135 | — | A | Direction of the sweep (0 = up, 135 = down-right). |
| `length` | length px | 400 | ≥ 0 (clamped) | A | Sweep length in px. |
| `color` | color | `#000000` | — | A | Shadow color. |
| `opacity` | percent | 50 | 0–100 (soft) | A | Shadow opacity at the layer. |
| `fade` | percent | 100 | 0–100 (soft) | A | Opacity falloff along the length (100 = fades to 0 at the end). |
| `softness` | length px | 0 | ≥ 0 (clamped) | A | Visible blur extent in px (σ = softness / 3). |

Every instance also takes `expand` (number px or `"none"`); see 01-effects-basics.md.

### `stylize.mosaic`

After Effects: Mosaic · Phase: P1 · Status: implemented · Tiling: tiled · Reads: — · Reads time: no · Device: CPU

Pixelation; blocks average in linear light unless `sharpColors`.

| Parameter | Type | Default | Range | Anim | What it does |
|---|---|---|---|---|---|
| `horizontalBlocks` | integer | 10 | 1–4000 (clamped) | A | Cells across the layer. |
| `verticalBlocks` | integer | 10 | 1–4000 (clamped) | A | Cells down the layer. |
| `sharpColors` | boolean | false | — | — | Use each cell's center pixel instead of its average. |

Every instance also takes `expand` (number px or `"none"`); see 01-effects-basics.md.

### `stylize.roughenEdges`

After Effects: Roughen Edges · Phase: P1 · Status: implemented · Tiling: whole · Reads: — · Reads time: no · Device: CPU

Hand-made, printed, torn-paper edges; animated "boil" with `evolution` on twos.

| Parameter | Type | Default | Range | Anim | What it does |
|---|---|---|---|---|---|
| `edgeType` | enum `roughen` / `roughenColor` / `cut` / `spiky` / `rustyColor` / `rusty` / `photocopierColor` / `photocopier` | `roughen` | — | — | Edge style. |
| `edgeColor` | color | `#000000` | — | A | Band color for the `…Color` types. |
| `border` | length px | 8 | ≥ 0 (clamped) | A | How far the edge is eaten into, in px. |
| `edgeSharpness` | number | 1 | 0.1–100 (clamped) | A | Slope of the new edge (1 = 1 px anti-aliased). |
| `fractalInfluence` | number | 1 | 0–1 (clamped) | A | How much the noise shapes the edge. |
| `scale` | percent | 100 | 0–100 (soft) | A | Noise feature size (cells of scale / 2 px). |
| `stretchWidth` | number | 0 | -100–100 (clamped) | A | Horizontal stretch of the noise, percent. |
| `offset` | point `[x, y]` | `[0, 0]` | — | A | Noise offset in px. |
| `complexity` | number | 2 | 1–6 (clamped) | A | Noise octaves. |
| `evolution` | angle ° | 0 | — | A | Noise evolution; animate on twos for boil. |
| `cycleEvolution` | boolean | false | — | — | Loop the evolution after `cycle` revolutions. |
| `cycle` | integer | 1 | 1–100 (clamped) | — | Revolutions per loop. |
| `randomSeed` | integer | 0 | 0–100000 (clamped) | — | After Effects' random seed. |

Every instance also takes `expand` (number px or `"none"`); see 01-effects-basics.md.

### `stylize.grain`

After Effects: Add Grain / Match Grain · Phase: P1 · Status: implemented · Tiling: tiled · Reads: — · Reads time: yes · Device: GPU when the whole stack lowers, else CPU

Film-like grain from **one tileable noise texture per frame**, a function of (seed, frame time quantized by `rate`, `size`): band-limited (not white), one mono field, modulated per channel by `color` and `channelIntensity` (`mono` applies the field as is; `color` reads the one texture at three fixed offsets, so the channels are fully decorrelated), blended in **linear light** with a gain chosen so the visible amount at mid-grey matches `amount` in perceptual terms, scaled by `response` at the pixel's luminance.

| Parameter | Type | Default | Range | Anim | What it does |
|---|---|---|---|---|---|
| `amount` | percent | 30 | 0–100 (soft) | A | Grain strength. |
| `size` | number | 1 | 0.1–64 (clamped) | A | Grain size in px. |
| `softness` | number | 0.5 | 0–1 (clamped) | A | Mix toward a coarser, softer octave. |
| `color` | enum `mono` / `color` | `color` | — | — | Monochrome or per-channel grain. |
| `channelIntensity` | point3d `[x, y, z]` | `[1, 1, 1]` | — | A | Per-channel grain gain. |
| `response` | curve `[[x, y], …]` | `[[0, 0.2], [0.25, 0.8], [0.5, 1], [0.75, 0.7], [1, 0.25]]` | — | A | Grain weight by encoded luminance. |
| `animated` | boolean | true | — | — | Change the pattern over time. |
| `rate` | number | 0 | ≥ 0 (clamped) | A | Pattern changes per second (0 = the comp frame rate). |
| `preset` | enum `none` / `kodak5207` / `kodak5219` / `fuji3510` / `ilford` / `16mm` / `8mm` | `none` | — | — | Film-stock preset (sets size, softness and channel balance unless overridden). |
| `blendMode` | enum `overlay` / `softLight` / `add` | `overlay` | — | — | How the grain lands on the image. |
| `seed` | integer seed | 0 | — | — | Random seed (spec 7 §7.5). |

Every instance also takes `expand` (number px or `"none"`) and `seed`; see 01-effects-basics.md.

### `stylize.vignette`

After Effects: — (Lumetri vignette) · Phase: P1 · Status: implemented · Tiling: tiled · Reads: — · Reads time: no · Device: GPU when the whole stack lowers, else CPU

In linear light (darkens like an optical vignette).

| Parameter | Type | Default | Range | Anim | What it does |
|---|---|---|---|---|---|
| `amount` | number | -0.3 | -1–1 (clamped) | A | Negative darkens the edges, positive lightens; 0 is neutral. |
| `midpoint` | percent | 50 | 0–100 (soft) | A | Where the falloff is centered (percent of the center-to-corner distance). |
| `roundness` | number | 0 | -100–100 (clamped) | A | Positive toward a circle, negative toward a rectangle. |
| `feather` | percent | 50 | 0–100 (soft) | A | Width of the falloff. |
| `center` | point `[x, y]` | `center` | — | A | Center of the vignette. |

Every instance also takes `expand` (number px or `"none"`); see 01-effects-basics.md.

### `stylize.outline`

After Effects: — (Stroke on alpha) · Phase: P1 · Status: implemented · Tiling: whole · Reads: — · Reads time: no · Device: CPU

Distance-field outline of the layer's alpha: crisp at any width (After Effects needs a shape layer or the Stroke layer style for this).

| Parameter | Type | Default | Range | Anim | What it does |
|---|---|---|---|---|---|
| `width` | length px | 4 | ≥ 0 (clamped) | A | Stroke width in px. |
| `color` | color | `#FFFFFF` | — | A | Stroke color. |
| `position` | enum `outside` / `center` / `inside` | `outside` | — | — | Where the stroke sits relative to the edge. |
| `softness` | length px | 0 | ≥ 0 (clamped) | A | Softening of the stroke edges in px. |
| `outlineOnly` | boolean | false | — | — | Output only the stroke. |

Every instance also takes `expand` (number px or `"none"`); see 01-effects-basics.md.

### `stylize.halftone`

After Effects: — (Color Halftone, print looks) · Phase: P2 · Status: implemented · Tiling: tiled · Reads: — · Reads time: no · Device: CPU

Analytic, anti-aliased dots computed per pixel (no texture), so cells stay crisp at any scale and animate smoothly: per plate, the pixel's own tone sets the size of a dot (line, square, diamond, or Euclidean dot) in a `cellSize` grid rotated by the plate's angle, and the pixel is covered where it lies inside that dot, anti-aliased over 1 px or `softness` percent of a cell.

| Parameter | Type | Default | Range | Anim | What it does |
|---|---|---|---|---|---|
| `source` | enum `luminance` / `alpha` | `luminance` | — | — | What the dot size follows: the luminance or the alpha. |
| `mode` | enum `mono` / `cmyk` / `rgb` / `duotone` | `mono` | — | — | Plates: one ink, four process inks, three additive, two inks. |
| `cellSize` | length px | 10 | ≥ 0 (clamped) | A | Screen cell size in px. |
| `angles` | list of `angle` | `[15, 75, 0, 45]` | — | A | Screen angles of the c, m, y and k plates (mono and duotone use the k angle, rgb c/m/y). |
| `shape` | enum `dot` / `line` / `square` / `diamond` / `euclidean` | `dot` | — | — | Dot shape. |
| `paper` | color | `#FFFFFF` | — | A | Paper color (mono, duotone, cmyk). |
| `ink` | color | `#000000` | — | A | Ink color (mono, duotone, and the k plate of cmyk). |
| `secondInk` | color | `#2A6FB5` | — | A | Second ink of `duotone` (the c angle). |
| `softness` | percent | 0 | 0–100 (soft) | A | Edge softness of the dots, as a percent of the cell size. |
| `misregistration` | length px | 0 | ≥ 0 (clamped) | A | Offset between the plates in px (a cheap-print look). |
| `blend` | percent | 100 | 0–100 (soft) | A | Mix of the halftone over the original. |

Every instance also takes `expand` (number px or `"none"`); see 01-effects-basics.md.

### `stylize.dither`

After Effects: — (dither looks) · Phase: P2 · Status: implemented · Tiling: tiled · Reads: — · Reads time: no · Device: CPU

The display-encoded color, after `brightness` and `contrast`, is matched to the nearest palette color in OKLab or encoded sRGB (the first of equal distances), after an ordered threshold (Bayer 2/4/8, blue noise: per pixel, stable in time) or with error diffusion (`floydSteinberg`, `atkinson`, `stucki`: a fixed raster scan over the whole layer, deterministic, but it shimmers when content moves; that is the look).

| Parameter | Type | Default | Range | Anim | What it does |
|---|---|---|---|---|---|
| `method` | enum `bayer2` / `bayer4` / `bayer8` / `blueNoise` / `floydSteinberg` / `atkinson` / `stucki` | `bayer4` | — | — | Ordered (per pixel) or error-diffusion (per frame scan) method. |
| `palette` | list of `color, or a preset name: 1bit, gameboy, cga, mac, grayscale4, grayscale8` | `["#000000", "#FFFFFF"]` | — | A | Colors to match to (or a preset name). |
| `pixelSize` | length px | 1 | ≥ 0 (clamped) | A | Dither on blocks of this many px. |
| `contrast` | number | 0 | -100–100 (clamped) | A | Contrast before matching, percent. |
| `brightness` | number | 0 | -100–100 (clamped) | A | Brightness before matching, percent. |
| `matchSpace` | enum `oklab` / `srgb` | `oklab` | — | — | Where the nearest palette color is measured. |

Every instance also takes `expand` (number px or `"none"`); see 01-effects-basics.md.

### `stylize.glitch`

After Effects: — (digital glitch) · Phase: P2 · Status: implemented · Tiling: tiled · Reads: — · Reads time: yes · Device: CPU

Seeded glitch events, one per `1 / frequency` seconds slot at a hashed offset inside the slot, each lasting `duration`.

| Parameter | Type | Default | Range | Anim | What it does |
|---|---|---|---|---|---|
| `amount` | percent | 50 | 0–100 (soft) | A | Share of the slices an event affects. |
| `blockSize` | point `[x, y]` | `[80, 12]` | — | A | Block width and slice height in px. |
| `blockShift` | length px | 40 | ≥ 0 (clamped) | A | Largest horizontal slice shift in px. |
| `channelShift` | length px | 8 | ≥ 0 (clamped) | A | Largest red/blue channel offset in px. |
| `frequency` | number | 6 | ≥ 0 (clamped) | A | Glitch events per second. |
| `duration` | number | 0.08 | ≥ 0 (clamped) | A | Length of one event in seconds. |
| `seed` | integer seed | 0 | — | — | Random seed (spec 7 §7.5). |
| `slices` | boolean | true | — | — | Shift horizontal slices. |
| `colorBlocks` | boolean | false | — | — | Fill some blocks of affected slices with flat colors. |
| `pixelate` | boolean | false | — | — | Pixelate some affected slices. |

Every instance also takes `expand` (number px or `"none"`) and `seed`; see 01-effects-basics.md.

### `stylize.rgbSplit`

After Effects: — (RGB split / channel offset) · Phase: P2 · Status: implemented · Tiling: tiled · Reads: — · Reads time: no · Device: CPU

Each channel is read from the layer shifted by its own offset (bilinear); `add` takes the channels as they are, `screen` screens them onto the unshifted layer; the alpha is the union of the three.

| Parameter | Type | Default | Range | Anim | What it does |
|---|---|---|---|---|---|
| `red` | point `[x, y]` | `[-4, 0]` | — | A | Offset of the red channel in px. |
| `green` | point `[x, y]` | `[0, 0]` | — | A | Offset of the green channel in px. |
| `blue` | point `[x, y]` | `[4, 0]` | — | A | Offset of the blue channel in px. |
| `mode` | enum `add` / `screen` | `add` | — | — | Replace the channels, or screen them onto the original. |

Every instance also takes `expand` (number px or `"none"`); see 01-effects-basics.md.

### `stylize.chromatic`

After Effects: — (chromatic aberration) · Phase: P2 · Status: implemented · Tiling: tiled · Reads: — · Reads time: no · Device: CPU

Lens-like: the red and blue channels are read from the layer displaced along the axis from `center` (`radial`: by `amount · (d / R)^falloff`, *d* the distance from the center and *R* the farthest corner; red outward, blue inward) or along `direction` (`directional`, uniform); `channels: rgb` also moves green by half the blue displacement, so the three fan out in spectral order.

| Parameter | Type | Default | Range | Anim | What it does |
|---|---|---|---|---|---|
| `amount` | length px | 4 | ≥ 0 (clamped) | A | Largest channel displacement in px. |
| `center` | point `[x, y]` | `center` | — | A | Center of the radial displacement. |
| `mode` | enum `radial` / `directional` | `radial` | — | — | Displacement grows with the distance from the center, or is uniform. |
| `direction` | angle ° | 90 | — | A | Direction of the uniform displacement (0 = up, 90 = right). |
| `falloff` | number | 1 | 0.1–8 (clamped) | A | Exponent of the radial growth. |
| `channels` | enum `rgb` / `rb` | `rb` | — | — | Move red and blue only, or all three. |

Every instance also takes `expand` (number px or `"none"`); see 01-effects-basics.md.

### `stylize.pixelSort`

After Effects: — (pixel sorting) · Phase: P2 · Status: implemented · Tiling: whole · Reads: other layers · Reads time: no · Device: CPU

Along rows (`direction` nearer horizontal) or columns of the layer rect, every run of consecutive pixels whose key (read from the display-encoded straight color) lies in `threshold` (and that the `mask` layer passes, where given) is sorted by that key, ascending toward +x / +y or descending, in runs of at most `maxLength` px; a stable sort, so the result is a pure function of the frame.

| Parameter | Type | Default | Range | Anim | What it does |
|---|---|---|---|---|---|
| `direction` | angle ° | 90 | — | A | Sort direction (0 = up, 90 = right); rows or columns, whichever is nearer. |
| `threshold` | point `[x, y]` | `[0.25, 0.8]` | — | A | Key range `[lo, hi]` of the pixels that take part. |
| `sortBy` | enum `luminance` / `hue` / `saturation` / `red` / `green` / `blue` | `luminance` | — | — | The sort key. |
| `order` | enum `ascending` / `descending` | `ascending` | — | — | Sort order along the direction. |
| `maxLength` | length px | 400 | ≥ 0 (clamped) | A | Longest run that is sorted, in px. |
| `mask` | layer id | none | — | — | Only pixels where this layer is bright take part (optional). |
| `maskSource` | enum `source` / `masks` / `effects` | `effects` | — | — | What of the other layer is read (spec 7 §7.6). |

Every instance also takes `expand` (number px or `"none"`); see 01-effects-basics.md.

### `stylize.scanlines`

After Effects: — (CRT) · Phase: P2 · Status: implemented · Tiling: tiled · Reads: — · Reads time: no · Device: CPU

`density` dark lines over the layer height, each covering `thickness` percent of its period at `opacity`, anti-aliased by their pixel coverage; a phosphor `mask` (`aperture` grille, `shadow` mask, `slot` mask) attenuates the other two channels per column; `flicker` dims whole frames by a hashed amount; `roll` scrolls the lines at that many periods per second; `curvature` barrel-warps the image; `bloom` adds a blurred copy.

| Parameter | Type | Default | Range | Anim | What it does |
|---|---|---|---|---|---|
| `density` | number | 360 | ≥ 1 (clamped) | A | Lines over the layer height. |
| `thickness` | percent | 50 | 0–100 (soft) | A | Dark share of each line period. |
| `opacity` | percent | 30 | 0–100 (soft) | A | Darkness of the lines. |
| `curvature` | percent | 0 | 0–100 (soft) | A | Barrel curvature of the image. |
| `mask` | enum `none` / `aperture` / `shadow` / `slot` | `none` | — | — | Phosphor mask pattern. |
| `flicker` | percent | 0 | 0–100 (soft) | A | Per-frame brightness flicker. |
| `bloom` | number | 0 | ≥ 0 (clamped) | A | Blurred glow added on top. |
| `roll` | number | 0 | — | A | Line scroll in periods per second. |
| `seed` | integer seed | 0 | — | — | Random seed (spec 7 §7.5). |

Every instance also takes `expand` (number px or `"none"`) and `seed`; see 01-effects-basics.md.

### `stylize.vhs`

After Effects: — (VHS) · Phase: P2 · Status: implemented · Tiling: tiled · Reads: — · Reads time: yes · Device: CPU

Rows jitter horizontally by `wobble` px of slow noise, a tracking band of `tracking` percent of the height drifts down the frame with a stronger shift and noise, the bottom 4 % carries head-switching noise, the chroma (the encoded color minus its luma) is averaged over `chromaBleed` px and offset by `colorShift` px, and hashed tape noise of `noise` percent is added to the luma; all scaled by `amount`, the noise and the band functions of (`seed`, frame).

| Parameter | Type | Default | Range | Anim | What it does |
|---|---|---|---|---|---|
| `amount` | percent | 60 | 0–100 (soft) | A | Overall strength. |
| `tracking` | percent | 10 | 0–100 (soft) | A | Height of the tracking band, percent of the layer. |
| `chromaBleed` | length px | 6 | ≥ 0 (clamped) | A | Horizontal chroma smear in px. |
| `noise` | percent | 30 | 0–100 (soft) | A | Tape noise strength. |
| `wobble` | length px | 3 | ≥ 0 (clamped) | A | Horizontal row jitter in px. |
| `colorShift` | length px, signed | 2 | any | A | Horizontal chroma offset in px. |
| `seed` | integer seed | 0 | — | — | Random seed (spec 7 §7.5). |

Every instance also takes `expand` (number px or `"none"`) and `seed`; see 01-effects-basics.md.

### `stylize.noise`

After Effects: Noise · Phase: P2 · Status: implemented · Tiling: tiled · Reads: — · Reads time: yes · Device: GPU when the whole stack lowers, else CPU

Hashed per-pixel noise of `amount` added to the display-encoded straight color (`uniform`, or the sum of two uniforms for `gaussian`), per channel with `color` or the same for every channel; `clip` clamps to [0, 1], otherwise values wrap around (the integer-overflow look).

| Parameter | Type | Default | Range | Anim | What it does |
|---|---|---|---|---|---|
| `amount` | percent | 20 | 0–100 (soft) | A | Noise strength. |
| `type` | enum `uniform` / `gaussian` | `uniform` | — | — | Noise distribution. |
| `color` | boolean | true | — | — | Per-channel noise (otherwise monochrome). |
| `clip` | boolean | true | — | — | Clamp to [0, 1] instead of wrapping. |
| `seed` | integer seed | 0 | — | — | Random seed (spec 7 §7.5). |

Every instance also takes `expand` (number px or `"none"`) and `seed`; see 01-effects-basics.md.

### `stylize.findEdges`

After Effects: Find Edges · Phase: P2 · Status: implemented · Tiling: tiled · Reads: — · Reads time: no · Device: CPU

The Sobel gradient magnitude of the display-encoded luma (reads clamped into the layer rect), dark on white (white on dark with `invert`) at the pixel's alpha, mixed with the original by `blend`.

| Parameter | Type | Default | Range | Anim | What it does |
|---|---|---|---|---|---|
| `invert` | boolean | false | — | — | White edges on black instead of dark edges on white. |
| `blend` | percent | 0 | 0–100 (soft) | A | Mix of the original back in. |

Every instance also takes `expand` (number px or `"none"`); see 01-effects-basics.md.

### `stylize.emboss`

After Effects: Emboss / Color Emboss · Phase: P2 · Status: implemented · Tiling: tiled · Reads: — · Reads time: no · Device: CPU

The difference between the layer sampled `relief` px along `direction` and against it (bilinear, clamped to the layer rect), scaled by `contrast`: a grey relief around mid grey, or added to the pixel's own color with `color` (Color Emboss); mixed with the original by `blend`.

| Parameter | Type | Default | Range | Anim | What it does |
|---|---|---|---|---|---|
| `direction` | angle ° | 135 | — | A | Direction of the light (0 = up). |
| `relief` | length px | 10 | ≥ 0 (clamped) | A | Apparent height in px (the sample distance). |
| `contrast` | percent | 100 | 0–100 (soft) | A | Strength of the relief. |
| `blend` | percent | 0 | 0–100 (soft) | A | Mix of the original back in. |
| `color` | boolean | false | — | — | Keep the layer's color (Color Emboss). |

Every instance also takes `expand` (number px or `"none"`); see 01-effects-basics.md.

### `stylize.glowEdges`

After Effects: Glowing Edges / Find Edges + Glow · Phase: P2 · Status: implemented · Tiling: whole · Reads: — · Reads time: no · Device: CPU

The Sobel edge magnitude of the display-encoded luma, spread by a Gaussian of σ = `width` / 2 and scaled by `brightness`, then pushed through `contrast` about mid grey; the edges glow in the layer's own colors (plus a quarter of white, so dark edges still show) on black, at the layer's alpha.

| Parameter | Type | Default | Range | Anim | What it does |
|---|---|---|---|---|---|
| `width` | length px | 2 | ≥ 0 (clamped) | A | Edge width in px. |
| `brightness` | number | 6 | 0–20 (clamped) | A | Edge gain. |
| `contrast` | number | 100 | 0–400 (clamped) | A | Contrast of the edges about mid grey, percent. |

Every instance also takes `expand` (number px or `"none"`); see 01-effects-basics.md.

### `stylize.pixelate`

After Effects: — · Phase: P2 · Status: implemented · Tiling: tiled · Reads: — · Reads time: no · Device: CPU

The layer rect in cells of `size` px (a square grid, or a pointy-top hexagonal lattice for `hexagon`), each cell the linear-light mean of its pixels, drawn as a square, circle, diamond or hexagon of `size − gap` px with `gapColor` at the cell's alpha between; pixels outside the layer rect pass through.

| Parameter | Type | Default | Range | Anim | What it does |
|---|---|---|---|---|---|
| `size` | length px | 8 | ≥ 0 (clamped) | A | Cell size in px. |
| `shape` | enum `square` / `hexagon` / `circle` / `diamond` | `square` | — | — | Cell shape. |
| `gap` | length px | 0 | ≥ 0 (clamped) | A | Gap between cells in px. |
| `gapColor` | color | `#000000` | — | A | Color of the gaps. |

Every instance also takes `expand` (number px or `"none"`); see 01-effects-basics.md.

### `stylize.scatter`

After Effects: Scatter · Phase: P2 · Status: implemented · Tiling: tiled · Reads: — · Reads time: no · Device: CPU

Every output pixel reads the layer at a hashed offset of up to `amount` px (nearest pixel) along both axes or one; `randomize` changes the pattern every frame.

| Parameter | Type | Default | Range | Anim | What it does |
|---|---|---|---|---|---|
| `amount` | length px | 10 | ≥ 0 (clamped) | A | Largest offset in px. |
| `grain` | enum `both` / `horizontal` / `vertical` | `both` | — | — | Axes the pixels scatter along. |
| `randomize` | boolean | false | — | — | A new pattern every frame. |
| `seed` | integer seed | 0 | — | — | Random seed (spec 7 §7.5). |

Every instance also takes `expand` (number px or `"none"`) and `seed`; see 01-effects-basics.md.

### `stylize.letterbox`

After Effects: — · Phase: P2 · Status: implemented · Tiling: tiled · Reads: — · Reads time: no · Device: GPU when the whole stack lowers, else CPU

Bars of `color` over the layer rect outside the centered `aspect` frame (top and bottom when the layer is taller than the aspect, left and right when wider), anti-aliased at fractional edges; on an adjustment layer the layer rect is the comp.

| Parameter | Type | Default | Range | Anim | What it does |
|---|---|---|---|---|---|
| `aspect` | number | 2.39 | ≥ 0 (clamped) | A | Aspect ratio of the visible frame (0 = no bars). |
| `color` | color | `#000000` | — | A | Bar color. |

Every instance also takes `expand` (number px or `"none"`); see 01-effects-basics.md.

### `stylize.posterizeEdges`

After Effects: — · Phase: P2 · Status: implemented · Tiling: tiled · Reads: — · Reads time: no · Device: CPU

The display-encoded color quantized to `levels` per channel, with `edgeColor` drawn where the quantized luma level differs from any neighbour within `edgeWidth` px (the eight directions).

| Parameter | Type | Default | Range | Anim | What it does |
|---|---|---|---|---|---|
| `levels` | integer | 6 | 2–255 (clamped) | A | Levels per channel. |
| `edgeWidth` | length px | 1 | ≥ 0 (clamped) | A | Width of the outlines in px (0 = none). |
| `edgeColor` | color | `#000000` | — | A | Outline color. |

Every instance also takes `expand` (number px or `"none"`); see 01-effects-basics.md.

### `stylize.cartoon`

After Effects: Cartoon · Phase: P2 · Status: implemented · Tiling: whole · Reads: — · Reads time: no · Device: CPU

Bilateral + quantize + edge detect; turns footage into flat illustration.

| Parameter | Type | Default | Range | Anim | What it does |
|---|---|---|---|---|---|
| `render` | enum `fill` / `edges` / `fillAndEdges` | `fillAndEdges` | — | — | The flat fill, the edge lines, or both. |
| `detailRadius` | length px | 8 | ≥ 0 (clamped) | A | Radius of the edge-preserving smoothing in px. |
| `detailThreshold` | percent | 10 | 0–100 (soft) | A | Luma difference (percent) within which detail is smoothed away. |
| `fillShadingSteps` | number | 8 | 1–64 (clamped) | A | Number of flat shading levels. |
| `fillShadingSmoothness` | percent | 70 | 0–100 (soft) | A | Softness of the steps between levels. |
| `edgeThreshold` | number | 1.5 | 0–5 (clamped) | A | Gradient magnitude at which a line is drawn. |
| `edgeWidth` | number | 1.5 | 0–10 (clamped) | A | Line width in px. |
| `edgeSoftness` | percent | 60 | 0–100 (soft) | A | Softness of the line's threshold. |
| `edgeOpacity` | percent | 100 | 0–100 (soft) | A | Opacity of the lines. |

Every instance also takes `expand` (number px or `"none"`); see 01-effects-basics.md.

### `stylize.texturize`

After Effects: Texturize · Phase: P2 · Status: implemented · Tiling: tiled · Reads: other layers · Reads time: no · Device: CPU

Paper and canvas textures (with an image asset of the texture).

| Parameter | Type | Default | Range | Anim | What it does |
|---|---|---|---|---|---|
| `texture` | layer id | none | — | — | The layer whose luminance is the relief. |
| `textureSource` | enum `source` / `masks` / `effects` | `effects` | — | — | What of the other layer is read (spec 7 §7.6). |
| `light` | angle ° | 135 | — | A | Direction the light comes from (0 = up, clockwise). |
| `contrast` | number | 1 | 0–2 (clamped) | A | Strength of the relief. |
| `placement` | enum `tile` / `center` / `stretch` | `tile` | — | — | Tile the texture over the layer, center it, or stretch it to fit. |

Every instance also takes `expand` (number px or `"none"`); see 01-effects-basics.md.

### `stylize.ccBlockLoad`

After Effects: CC Block Load · Phase: P2 · Status: implemented · Tiling: whole · Reads: — · Reads time: no · Device: CPU

Progressive block-by-block image loading.

| Parameter | Type | Default | Range | Anim | What it does |
|---|---|---|---|---|---|
| `completion` | percent | 0 | 0–100 (soft) | A | How much of the image has loaded. |
| `scanlines` | boolean | true | — | — | New blocks arrive row by row. |
| `smoothing` | boolean | true | — | — | Soften the arrival. |
| `startCleared` | boolean | true | — | — | Start from nothing rather than the coarsest block. |
| `bilinear` | boolean | false | — | — | Interpolate between block centres. |

Every instance also takes `expand` (number px or `"none"`); see 01-effects-basics.md.

### `stylize.ccBurnFilm`

After Effects: CC Burn Film · Phase: P2 · Status: implemented · Tiling: tiled · Reads: — · Reads time: no · Device: CPU

Film burning away from `center` as `burn` grows.

| Parameter | Type | Default | Range | Anim | What it does |
|---|---|---|---|---|---|
| `burn` | percent | 0 | 0–100 (soft) | A | How far the burn has spread. |
| `center` | point `[x, y]` | `center` | — | A | Where the burn starts. |
| `seed` | integer seed | 0 | — | — | Random seed (spec 7 §7.5). |

Every instance also takes `expand` (number px or `"none"`) and `seed`; see 01-effects-basics.md.

<!-- gen:catalogue-stylize-1:end -->
