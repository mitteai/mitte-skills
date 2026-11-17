# Distort: every parameter (part 1 of 2)

Generated from `rexx-engine effects` by scripts/skills-effects-catalogue.py; do not edit by hand. Index: [90-catalogue.md](90-catalogue.md).

<!-- gen:catalogue-distort-1:start -->
### `distort.transform`

After Effects: Transform (effect) · Phase: P1 · Status: implemented · Tiling: tiled · Reads: parameter history · Reads time: no · Device: CPU

A transform inside the effect stack (before other effects), with its own motion blur: the standard trick to motion-blur a layer that is otherwise static, and to transform before a glow.

| Parameter | Type | Default | Range | Anim | What it does |
|---|---|---|---|---|---|
| `anchor` | point `[x, y]` | `center` | — | A | Anchor point the scale, skew and rotation act about. |
| `position` | point `[x, y]` | `center` | — | A | Where the anchor lands. |
| `uniformScale` | boolean | true | — | — | Use `scale` for both axes. |
| `scale` | percent | 100 | -10000–10000 (soft) | A | Uniform scale. |
| `scaleX` | percent | 100 | -10000–10000 (soft) | A | Horizontal scale when not uniform. |
| `scaleY` | percent | 100 | -10000–10000 (soft) | A | Vertical scale when not uniform. |
| `skew` | number | 0 | -85–85 (clamped) | A | Skew in degrees. |
| `skewAxis` | angle ° | 0 | — | A | Axis the skew acts along. |
| `rotation` | angle ° | 0 | — | A | Rotation in degrees, clockwise. |
| `opacity` | percent | 100 | 0–100 (soft) | A | Opacity. |
| `useCompShutterAngle` | boolean | true | — | — | Motion-blur with the comp's shutter angle. |
| `shutterAngle` | number | 0 | 0–720 (clamped) | A | Own shutter angle when not using the comp's (0 = no blur). |

Every instance also takes `expand` (number px or `"none"`); see 01-effects-basics.md.

### `distort.displacement`

After Effects: Displacement Map · Phase: P1 · Status: implemented · Tiling: tiled · Reads: other layers · Reads time: no · Device: CPU

Map value 0.5 = no displacement (display-encoded map values, as After Effects).

| Parameter | Type | Default | Range | Anim | What it does |
|---|---|---|---|---|---|
| `map` | layer id | none | — | — | The layer whose pixels displace this one. |
| `mapSource` | enum `source` / `masks` / `effects` | `effects` | — | — | What of the other layer is read (spec 7 §7.6). |
| `horizontal` | enum `red` / `green` / `blue` / `alpha` / `luminance` / `hue` / `lightness` / `saturation` / `full` / `half` / `off` | `red` | — | — | Map channel for horizontal displacement. |
| `maxHorizontal` | length px, signed | 5 | any | A | Horizontal displacement at map value 1 (px). |
| `vertical` | enum `red` / `green` / `blue` / `alpha` / `luminance` / `hue` / `lightness` / `saturation` / `full` / `half` / `off` | `green` | — | — | Map channel for vertical displacement. |
| `maxVertical` | length px, signed | 5 | any | A | Vertical displacement at map value 1 (px). |
| `fit` | enum `center` / `stretch` / `tile` | `center` | — | — | How a map of a different size lines up with the layer. |
| `wrap` | boolean | false | — | — | Wrap source reads around the layer rect. |
| `expandOutput` | boolean | true | — | — | Grow the output by the maximum displacement. |

Every instance also takes `expand` (number px or `"none"`); see 01-effects-basics.md.

### `distort.waveWarp`

After Effects: Wave Warp · Phase: P1 · Status: implemented · Tiling: tiled · Reads: — · Reads time: yes · Device: GPU when the whole stack lowers, else CPU

Flags, heat haze, wavy text.

| Parameter | Type | Default | Range | Anim | What it does |
|---|---|---|---|---|---|
| `waveType` | enum `sine` / `square` / `triangle` / `sawtooth` / `circle` / `semicircle` / `uncircle` / `noise` / `smoothNoise` | `sine` | — | — | Wave shape. |
| `height` | length px | 10 | ≥ 0 (clamped) | A | Wave amplitude in px. |
| `width` | length px | 40 | ≥ 0 (clamped) | A | Wavelength in px. |
| `direction` | angle ° | 90 | — | A | Direction the wave travels (0 = up, 90 = right). |
| `speed` | number | 1 | — | A | Cycles per second. |
| `pinning` | enum `none` / `allEdges` / `center` / `left` / `top` / `right` / `bottom` / `horizontalEdges` / `verticalEdges` | `none` | — | — | Edges whose pixels stay put. |
| `phase` | angle ° | 0 | — | A | Wave phase. |
| `antialiasing` | enum `low` / `medium` / `high` | `high` | — | — | low = bilinear, medium/high = bicubic. |

Every instance also takes `expand` (number px or `"none"`); see 01-effects-basics.md.

### `distort.offset`

After Effects: Offset / Motion Tile · Phase: P1 · Status: implemented · Tiling: tiled · Reads: — · Reads time: no · Device: GPU when the whole stack lowers, else CPU

Wraps around the layer edges (seamless scrolling backgrounds).

| Parameter | Type | Default | Range | Anim | What it does |
|---|---|---|---|---|---|
| `shift` | point `[x, y]` | `[0, 0]` | — | A | Shift in px; content wraps around the layer rect. |
| `blend` | percent | 0 | 0–100 (soft) | A | Mix of the original with the shifted copy. |

Every instance also takes `expand` (number px or `"none"`); see 01-effects-basics.md.

### `distort.cornerPin`

After Effects: Corner Pin / CC Power Pin · Phase: P2 · Status: implemented · Tiling: tiled · Reads: — · Reads time: no · Device: CPU

The projective map (homography) that takes the layer rect's corners to the four points, inverse-mapped per pixel with perspective-correct sampling (bicubic at `high`, bilinear at `low` or in draft, as every distortion here).

| Parameter | Type | Default | Range | Anim | What it does |
|---|---|---|---|---|---|
| `topLeft` | point `[x, y]` | `["0%", "0%"]` | — | A | Where the layer's top-left corner lands. |
| `topRight` | point `[x, y]` | `["100%", "0%"]` | — | A | Where the top-right corner lands. |
| `bottomLeft` | point `[x, y]` | `["0%", "100%"]` | — | A | Where the bottom-left corner lands. |
| `bottomRight` | point `[x, y]` | `["100%", "100%"]` | — | A | Where the bottom-right corner lands. |
| `antialiasing` | enum `low` / `high` | `high` | — | — | low = bilinear, high = bicubic. |

Every instance also takes `expand` (number px or `"none"`); see 01-effects-basics.md.

### `distort.bulge`

After Effects: Bulge / CC Lens · Phase: P2 · Status: implemented · Tiling: tiled · Reads: — · Reads time: no · Device: CPU

Inside the ellipse `radiusX` × `radiusY` about `center` the source is pulled toward the center by `height · (1 − d²)^taper / 2` (negative heights push; `taper` is a number, not After Effects' checkbox: higher makes the sides shallower), fading out over the outer 10 % of the layer with `pinEdges`.

| Parameter | Type | Default | Range | Anim | What it does |
|---|---|---|---|---|---|
| `center` | point `[x, y]` | `center` | — | A | Center of the bulge. |
| `radiusX` | length px | 50 | ≥ 0 (clamped) | A | Horizontal radius in px. |
| `radiusY` | length px | 50 | ≥ 0 (clamped) | A | Vertical radius in px. |
| `height` | number | 1 | -4–4 (clamped) | A | Bulge height (negative pinches). |
| `taper` | number | 0 | 0–100 (clamped) | A | Taper radius: higher makes the sides shallower. |
| `antialiasing` | enum `low` / `high` | `high` | — | — | low = bilinear, high = bicubic. |
| `pinEdges` | boolean | false | — | — | Keep the layer's edges in place. |

Every instance also takes `expand` (number px or `"none"`); see 01-effects-basics.md.

### `distort.ripple`

After Effects: Ripple · Phase: P2 · Status: implemented · Tiling: tiled · Reads: — · Reads time: yes · Device: CPU

Concentric waves of `width` px wavelength and `height` px amplitude about `center`, fading to nothing at `radius` percent of the layer, traveling outward at `speed` cycles per second; `asymmetric` ripples also move sideways a quarter wave out of step.

| Parameter | Type | Default | Range | Anim | What it does |
|---|---|---|---|---|---|
| `radius` | percent | 100 | 0–100 (soft) | A | Reach of the ripples, percent of the layer (100 = the edge). |
| `center` | point `[x, y]` | `center` | — | A | Center of the ripples. |
| `type` | enum `asymmetric` / `symmetric` | `asymmetric` | — | — | Asymmetric ripples also move sideways. |
| `speed` | number | 1 | — | A | Cycles per second. |
| `width` | length px | 40 | ≥ 0 (clamped) | A | Wavelength in px. |
| `height` | length px | 10 | ≥ 0 (clamped) | A | Amplitude in px. |
| `phase` | angle ° | 0 | — | A | Wave phase. |
| `antialiasing` | enum `low` / `high` | `high` | — | — | low = bilinear, high = bicubic. |

Every instance also takes `expand` (number px or `"none"`); see 01-effects-basics.md.

### `distort.twirl`

After Effects: Twirl / Twirl (Legacy) · Phase: P2 · Status: implemented · Tiling: tiled · Reads: — · Reads time: no · Device: CPU

Rotates the source about `center` by `angle` at the center, falling off quadratically to nothing at `radius`.

| Parameter | Type | Default | Range | Anim | What it does |
|---|---|---|---|---|---|
| `angle` | angle ° | 0 | — | A | Rotation at the center, degrees. |
| `radius` | percent | 50 | 0–100 (soft) | A | Reach, percent of the layer's larger side. |
| `center` | point `[x, y]` | `center` | — | A | Center of the twirl. |
| `antialiasing` | enum `low` / `high` | `high` | — | — | low = bilinear, high = bicubic. |

Every instance also takes `expand` (number px or `"none"`); see 01-effects-basics.md.

### `distort.spherize`

After Effects: Spherize · Phase: P2 · Status: implemented · Tiling: tiled · Reads: — · Reads time: no · Device: CPU

Wraps the source onto a sphere of `radius` px about `center` (`d → asin(d / R) / (π/2)`).

| Parameter | Type | Default | Range | Anim | What it does |
|---|---|---|---|---|---|
| `radius` | length px | 100 | ≥ 0 (clamped) | A | Sphere radius in px. |
| `center` | point `[x, y]` | `center` | — | A | Center of the sphere. |
| `antialiasing` | enum `low` / `high` | `high` | — | — | low = bilinear, high = bicubic. |

Every instance also takes `expand` (number px or `"none"`); see 01-effects-basics.md.

### `distort.polar`

After Effects: Polar Coordinates · Phase: P2 · Status: implemented · Tiling: tiled · Reads: — · Reads time: no · Device: CPU

`rectToPolar` reads the layer rect as (angle → x, radius → y) around its center, `polarToRect` the reverse, mixed with the identity by `interpolation`; reads are clamped to the layer rect.

| Parameter | Type | Default | Range | Anim | What it does |
|---|---|---|---|---|---|
| `interpolation` | percent | 0 | 0–100 (soft) | A | How far toward the converted image. |
| `conversion` | enum `rectToPolar` / `polarToRect` | `rectToPolar` | — | — | Direction of the conversion. |
| `antialiasing` | enum `low` / `high` | `high` | — | — | low = bilinear, high = bicubic. |

Every instance also takes `expand` (number px or `"none"`); see 01-effects-basics.md.

### `distort.mirror`

After Effects: Mirror · Phase: P2 · Status: implemented · Tiling: tiled · Reads: — · Reads time: no · Device: CPU

The half-plane past the line through `center` perpendicular to `angle` shows the other half reflected; `angle` is the direction of the reflected half (0 = right, so the right side mirrors the left; 90 = down).

| Parameter | Type | Default | Range | Anim | What it does |
|---|---|---|---|---|---|
| `center` | point `[x, y]` | `center` | — | A | A point on the reflection axis. |
| `angle` | angle ° | 0 | — | A | Direction of the reflected half (0 = right, 90 = down). |
| `antialiasing` | enum `low` / `high` | `high` | — | — | low = bilinear, high = bicubic. |

Every instance also takes `expand` (number px or `"none"`); see 01-effects-basics.md.

### `distort.turbulent`

After Effects: Turbulent Displace · Phase: P2 · Status: implemented · Tiling: tiled · Reads: — · Reads time: no · Device: CPU

Displaces every pixel by `amount` px of `generate.fractalNoise`'s noise (`size` px cells, `complexity` octaves, `evolution`): two independent noises for `turbulent`, the noise gradient for `bulge`, its rotation for `twist` (the `…Smoother` kinds use a gentler octave falloff), one axis for `vertical`/`horizontal`, the same noise on both axes for `cross`.

| Parameter | Type | Default | Range | Anim | What it does |
|---|---|---|---|---|---|
| `type` | enum `turbulent` / `bulge` / `twist` / `turbulentSmoother` / `bulgeSmoother` / `twistSmoother` / `vertical` / `horizontal` / `cross` | `turbulent` | — | — | Displacement kind. |
| `amount` | number | 50 | -1000–1000 (clamped) | A | Displacement in px. |
| `size` | length px | 100 | ≥ 0 (clamped) | A | Noise cell size in px. |
| `offset` | point `[x, y]` | `[0, 0]` | — | A | Noise offset in px. |
| `complexity` | number | 1 | 1–10 (clamped) | A | Noise octaves. |
| `evolution` | angle ° | 0 | — | A | Noise evolution. |
| `cycleEvolution` | boolean | false | — | — | Loop the evolution after `cycle` revolutions. |
| `cycle` | integer | 1 | 1–100 (clamped) | — | Revolutions per loop. |
| `randomSeed` | integer | 0 | 0–100000 (clamped) | — | After Effects' random seed. |
| `pinning` | enum `none` / `all` / `horizontal` / `vertical` / `horizontalVertical` / `allLocked` / `horizontalLocked` / `verticalLocked` / `horizontalVerticalLocked` | `none` | — | — | Edges whose pixels stay put. |
| `resizeLayer` | boolean | false | — | — | Grow the output by the displacement. |
| `antialiasing` | enum `low` / `high` | `high` | — | — | low = bilinear, high = bicubic. |

Every instance also takes `expand` (number px or `"none"`); see 01-effects-basics.md.

### `distort.motionTile`

After Effects: Motion Tile · Phase: P2 · Status: implemented · Tiling: tiled · Reads: — · Reads time: no · Device: CPU

The layer rect repeated in tiles of `tileWidth` × `tileHeight` percent of it, centered on `center`, over an output of `outputWidth` × `outputHeight` percent of the layer about its center; `mirrorEdges` flips alternate tiles, `phase` slides alternate rows (columns with `horizontalPhaseShift`).

| Parameter | Type | Default | Range | Anim | What it does |
|---|---|---|---|---|---|
| `center` | point `[x, y]` | `center` | — | A | Center of the tile grid. |
| `tileWidth` | percent | 100 | 0–100 (soft) | A | Tile width, percent of the layer. |
| `tileHeight` | percent | 100 | 0–100 (soft) | A | Tile height, percent of the layer. |
| `outputWidth` | percent | 100 | 0–100 (soft) | A | Output width, percent of the layer. |
| `outputHeight` | percent | 100 | 0–100 (soft) | A | Output height, percent of the layer. |
| `mirrorEdges` | boolean | false | — | — | Flip alternate tiles. |
| `phase` | angle ° | 0 | — | A | Offset of alternate rows (or columns), one revolution = one tile. |
| `horizontalPhaseShift` | boolean | false | — | — | Shift columns instead of rows. |
| `antialiasing` | enum `low` / `high` | `high` | — | — | low = bilinear, high = bicubic. |

Every instance also takes `expand` (number px or `"none"`); see 01-effects-basics.md.

### `distort.kaleidoscope`

After Effects: CC Kaleida · Phase: P2 · Status: implemented · Tiling: tiled · Reads: — · Reads time: no · Device: CPU

The plane around `center` is divided into wedges (`dia` 6, `octo` 8, `cross` 4 and `tri` 3 mirrored wedges; `wheel` 12 unmirrored) rotated by `rotation`; every pixel reads the first wedge at `size` percent scale, so one wedge of the source repeats around the center.

| Parameter | Type | Default | Range | Anim | What it does |
|---|---|---|---|---|---|
| `center` | point `[x, y]` | `center` | — | A | Center of the pattern. |
| `size` | percent | 50 | 0–100 (soft) | A | Scale of the repeated wedge, percent. |
| `mirroring` | enum `dia` / `octo` / `cross` / `wheel` / `tri` | `dia` | — | — | Wedge layout: 6, 8, 4 mirrored wedges, 12 plain (wheel), 3 mirrored. |
| `rotation` | angle ° | 0 | — | A | Rotation of the wedges. |
| `floatingCenter` | boolean | false | — | — | Accepted for After Effects parity; the center is `center`. |
| `antialiasing` | enum `low` / `high` | `high` | — | — | low = bilinear, high = bicubic. |

Every instance also takes `expand` (number px or `"none"`); see 01-effects-basics.md.

### `distort.magnify`

After Effects: Magnify · Phase: P2 · Status: implemented · Tiling: tiled · Reads: — · Reads time: no · Device: CPU

Inside a circle or square of `size` px about `center` (feathered over `feather` px) the source appears magnified by `magnification`, read nearest-pixel (`standard`), bicubic (`softSharp`) or jittered (`scatter`), blended by `blending` at `opacity` over the layer; outside, the layer (with `blending: none`, nothing).

| Parameter | Type | Default | Range | Anim | What it does |
|---|---|---|---|---|---|
| `shape` | enum `circle` / `square` | `circle` | — | — | Shape of the magnified area. |
| `center` | point `[x, y]` | `center` | — | A | Center of the magnifier. |
| `magnification` | percent | 150 | 1–10000 (soft) | A | Magnification, percent. |
| `link` | enum `none` / `sizeToMagnification` / `sizeAndFeatherToMagnification` | `none` | — | — | What scales with the magnification. |
| `size` | length px | 50 | ≥ 0 (clamped) | A | Radius (or half side) of the area in px. |
| `feather` | length px | 0 | ≥ 0 (clamped) | A | Soft edge of the area in px. |
| `opacity` | percent | 100 | 0–100 (soft) | A | Opacity of the magnified area. |
| `scaling` | enum `standard` / `softSharp` / `scatter` | `standard` | — | — | Resampling of the magnified pixels. |
| `blending` | blend mode (any of the 38; see 20-utility-controls.md) | `normal` | — | — | Blend mode of the magnified area over the layer (`none` keeps only the area). |
| `seed` | integer seed | 0 | — | — | Random seed (spec 7 §7.5). |

Every instance also takes `expand` (number px or `"none"`) and `seed`; see 01-effects-basics.md.

### `distort.lens`

After Effects: Optics Compensation / Lens Distortion · Phase: P2 · Status: implemented · Tiling: tiled · Reads: — · Reads time: no · Device: CPU

Barrel distortion of a lens with `fov` degrees across the layer's width, height or diagonal about `center`: a pixel at distance *r* reads the source at `f · tan(r / r_ref · fov / 2)` with `f = r_ref / tan(fov / 2)`; `reverse` applies the inverse (pincushion), and `resizing` lets the stretched corners grow the output (up to 2×, 4× or, for `unlimited`, 8× the layer).

| Parameter | Type | Default | Range | Anim | What it does |
|---|---|---|---|---|---|
| `fov` | number | 0 | 0–179 (clamped) | A | Field of view in degrees. |
| `reverse` | boolean | false | — | — | Remove distortion (pincushion) instead of adding it. |
| `center` | point `[x, y]` | `center` | — | A | Optical center. |
| `fovOrientation` | enum `horizontal` / `vertical` / `diagonal` | `horizontal` | — | — | What the field of view spans. |
| `resizing` | enum `off` / `max2x` / `max4x` / `unlimited` | `off` | — | — | Growth of the output with `reverse`. |
| `antialiasing` | enum `low` / `high` | `high` | — | — | low = bilinear, high = bicubic. |

Every instance also takes `expand` (number px or `"none"`); see 01-effects-basics.md.

### `distort.meshWarp`

After Effects: Mesh Warp · Phase: P2 · Status: implemented · Tiling: tiled · Reads: — · Reads time: no · Device: CPU

Bezier patch mesh.

| Parameter | Type | Default | Range | Anim | What it does |
|---|---|---|---|---|---|
| `rows` | integer | 7 | 1–31 (clamped) | — | Patch rows. |
| `columns` | integer | 7 | 1–31 (clamped) | — | Patch columns. |
| `quality` | integer | 8 | 1–10 (clamped) | — | Subdivisions per patch. |
| `vertices` | list of `point` | `[]` | — | A | The moved vertices, row-major (empty = the rest grid). |
| `tangents` | list of `point` | `[]` | — | A | Vertex tangents (accepted, ignored: the patches are Catmull-Rom). |

Every instance also takes `expand` (number px or `"none"`); see 01-effects-basics.md.

### `distort.bezierWarp`

After Effects: Bezier Warp · Phase: P2 · Status: implemented · Tiling: tiled · Reads: — · Reads time: no · Device: CPU

| Parameter | Type | Default | Range | Anim | What it does |
|---|---|---|---|---|---|
| `topLeftVertex` | point `[x, y]` | `["0%", "0%"]` | — | A | Top-left corner. |
| `topLeftTangent` | point `[x, y]` | `["33.333333333333336%", "0%"]` | — | A | Tangent of the top edge at its left. |
| `topRightTangent` | point `[x, y]` | `["66.66666666666667%", "0%"]` | — | A | Tangent of the top edge at its right. |
| `rightTopVertex` | point `[x, y]` | `["100%", "0%"]` | — | A | Top-right corner. |
| `rightTopTangent` | point `[x, y]` | `["100%", "33.333333333333336%"]` | — | A | Tangent of the right edge at its top. |
| `rightBottomTangent` | point `[x, y]` | `["100%", "66.66666666666667%"]` | — | A | Tangent of the right edge at its bottom. |
| `bottomRightVertex` | point `[x, y]` | `["100%", "100%"]` | — | A | Bottom-right corner. |
| `bottomRightTangent` | point `[x, y]` | `["66.66666666666667%", "100%"]` | — | A | Tangent of the bottom edge at its right. |
| `bottomLeftTangent` | point `[x, y]` | `["33.333333333333336%", "100%"]` | — | A | Tangent of the bottom edge at its left. |
| `leftBottomVertex` | point `[x, y]` | `["0%", "100%"]` | — | A | Bottom-left corner. |
| `leftBottomTangent` | point `[x, y]` | `["0%", "66.66666666666667%"]` | — | A | Tangent of the left edge at its bottom. |
| `leftTopTangent` | point `[x, y]` | `["0%", "33.333333333333336%"]` | — | A | Tangent of the left edge at its top. |
| `quality` | integer | 8 | 1–10 (clamped) | — | Grid subdivisions (× 4). |

Every instance also takes `expand` (number px or `"none"`); see 01-effects-basics.md.

### `distort.ccFlo`

After Effects: CC Flo Motion · Phase: P2 · Status: implemented · Tiling: tiled · Reads: — · Reads time: no · Device: CPU

| Parameter | Type | Default | Range | Anim | What it does |
|---|---|---|---|---|---|
| `knot1` | point `[x, y]` | `["25%", "50%"]` | — | A | First knot. |
| `amount1` | number | 50 | -400–100 (clamped) | A | Pull (positive) or push (negative) of the first knot, percent. |
| `knot2` | point `[x, y]` | `["75%", "50%"]` | — | A | Second knot. |
| `amount2` | number | -50 | -400–100 (clamped) | A | Pull or push of the second knot, percent. |
| `tileEdges` | boolean | false | — | — | Wrap reads around the layer rect. |
| `antialiasing` | enum `low` / `medium` / `high` | `medium` | — | — | Samples per pixel: 1, 4 or 9. |
| `falloff` | number | 2 | 0.01–10 (clamped) | A | Exponent of the knots' falloff. |

Every instance also takes `expand` (number px or `"none"`); see 01-effects-basics.md.

### `distort.ccBend`

After Effects: CC Bend It · Phase: P2 · Status: implemented · Tiling: tiled · Reads: — · Reads time: no · Device: CPU

| Parameter | Type | Default | Range | Anim | What it does |
|---|---|---|---|---|---|
| `bend` | angle ° | 0 | — | A | Bend in degrees (sign picks the side). |
| `start` | point `[x, y]` | `["50%", "20%"]` | — | A | Where the bend starts. |
| `end` | point `[x, y]` | `["50%", "80%"]` | — | A | Where the bend ends (the arc's far end). |
| `renderPrestart` | enum `none` / `static` | `static` | — | — | Keep or drop the part before `start`. |
| `distort` | enum `legacy` / `natural` | `natural` | — | — | Accepted and ignored (After Effects' legacy mode). |

Every instance also takes `expand` (number px or `"none"`); see 01-effects-basics.md.

### `distort.ccBender`

After Effects: CC Bender · Phase: P2 · Status: implemented · Tiling: tiled · Reads: — · Reads time: no · Device: CPU

Bends the layer between `base` and `top`.

| Parameter | Type | Default | Range | Anim | What it does |
|---|---|---|---|---|---|
| `amount` | number | 0 | -200–200 (clamped) | A | How far the top bends, percent of the reference. |
| `style` | enum `bend` / `marilyn` / `sharp` / `boxer` | `bend` | — | — | The bend's profile. |
| `adjustToDistance` | boolean | false | — | — | Reference the base–top distance instead of the layer height. |
| `top` | point `[x, y]` | `["50%", "0%"]` | — | A | Where the bend is strongest. |
| `base` | point `[x, y]` | `["50%", "100%"]` | — | A | Where nothing moves. |

Every instance also takes `expand` (number px or `"none"`); see 01-effects-basics.md.

### `distort.ccSlant`

After Effects: CC Slant · Phase: P2 · Status: implemented · Tiling: tiled · Reads: — · Reads time: no · Device: CPU

Shears the layer about `floor`.

| Parameter | Type | Default | Range | Anim | What it does |
|---|---|---|---|---|---|
| `slant` | number | 0 | — | A | Shear, percent of the height above the floor. |
| `stretching` | boolean | false | — | — | Keep the sheared width (narrow the layer along the shear). |
| `height` | percent | 100 | 0–100 (soft) | A | Vertical scale about the floor. |
| `floor` | point `[x, y]` | `["50%", "100%"]` | — | A | The line that does not move. |

Every instance also takes `expand` (number px or `"none"`); see 01-effects-basics.md.

### `distort.ccSmear`

After Effects: CC Smear · Phase: P2 · Status: implemented · Tiling: tiled · Reads: — · Reads time: no · Device: CPU

Drags the pixels around `from` toward `to`.

| Parameter | Type | Default | Range | Anim | What it does |
|---|---|---|---|---|---|
| `from` | point `[x, y]` | `["35%", "50%"]` | — | A | Where the drag starts. |
| `to` | point `[x, y]` | `["65%", "50%"]` | — | A | Where the pixels are dragged to. |
| `reach` | number | 50 | -100–100 (clamped) | A | How far the pixels go, percent of the distance. |
| `radius` | length px | 50 | ≥ 0 (clamped) | A | Width of the dragged band (px). |

Every instance also takes `expand` (number px or `"none"`); see 01-effects-basics.md.

### `distort.ccSplit`

After Effects: CC Split · Phase: P2 · Status: implemented · Tiling: tiled · Reads: — · Reads time: no · Device: CPU

Opens a slit between the two points.

| Parameter | Type | Default | Range | Anim | What it does |
|---|---|---|---|---|---|
| `pointA` | point `[x, y]` | `["25%", "50%"]` | — | A | One end of the slit. |
| `pointB` | point `[x, y]` | `["75%", "50%"]` | — | A | The other end of the slit. |
| `split` | number | 50 | — | A | How wide the slit opens, percent of half the distance. |

Every instance also takes `expand` (number px or `"none"`); see 01-effects-basics.md.

### `distort.ccSplit2`

After Effects: CC Split 2 · Phase: P2 · Status: implemented · Tiling: tiled · Reads: — · Reads time: no · Device: CPU

As `distort.ccSplit` with the two sides opened independently.

| Parameter | Type | Default | Range | Anim | What it does |
|---|---|---|---|---|---|
| `pointA` | point `[x, y]` | `["25%", "50%"]` | — | A | One end of the slit. |
| `pointB` | point `[x, y]` | `["75%", "50%"]` | — | A | The other end of the slit. |
| `split1` | number | 50 | — | A | Opening of the first side, percent of half the distance. |
| `split2` | number | 50 | — | A | Opening of the second side, percent of half the distance. |

Every instance also takes `expand` (number px or `"none"`); see 01-effects-basics.md.

### `distort.ccTiler`

After Effects: CC Tiler · Phase: P2 · Status: implemented · Tiling: tiled · Reads: — · Reads time: no · Device: CPU

Tiles scaled copies of the layer about `center`.

| Parameter | Type | Default | Range | Anim | What it does |
|---|---|---|---|---|---|
| `scale` | percent | 50 | 0–100 (soft) | A | Size of each copy, percent of the layer. |
| `center` | point `[x, y]` | `center` | — | A | The copy that stays in place. |
| `blendWithOriginal` | percent | 0 | 0–100 (soft) | A | Mix of the untouched layer in the result. |

Every instance also takes `expand` (number px or `"none"`); see 01-effects-basics.md.

### `distort.ccGriddler`

After Effects: CC Griddler · Phase: P2 · Status: implemented · Tiling: tiled · Reads: — · Reads time: no · Device: CPU

Tiles the layer into a rotated, scaled grid.

| Parameter | Type | Default | Range | Anim | What it does |
|---|---|---|---|---|---|
| `horizontalScale` | percent | 100 | 0–100 (soft) | A | Horizontal scale of each tile's content. |
| `verticalScale` | percent | 100 | 0–100 (soft) | A | Vertical scale of each tile's content. |
| `tileSize` | length px | 10 | ≥ 0 (clamped) | A | Side of the tiles (px). |
| `rotation` | angle ° | 0 | — | A | Rotation of each tile's content. |
| `cutTiles` | boolean | false | — | — | Leave a gap between the tiles. |

Every instance also takes `expand` (number px or `"none"`); see 01-effects-basics.md.

### `distort.warp`

After Effects: Warp · Phase: P2 · Status: implemented · Tiling: tiled · Reads: — · Reads time: no · Device: CPU

The fifteen Photoshop warp styles, inverse-mapped.

| Parameter | Type | Default | Range | Anim | What it does |
|---|---|---|---|---|---|
| `style` | enum `arc` / `arcLower` / `arcUpper` / `arch` / `bulge` / `shellLower` / `shellUpper` / `flag` / `wave` / `fish` / `rise` / `fisheye` / `inflate` / `squeeze` / `twist` | `arc` | — | — | The warp's shape. |
| `axis` | enum `horizontal` / `vertical` | `horizontal` | — | — | The axis the shape runs along. |
| `bend` | number | 0 | -100–100 (clamped) | A | Strength of the shape. |
| `horizontalDistortion` | number | 0 | -100–100 (clamped) | A | Size change across the width. |
| `verticalDistortion` | number | 0 | -100–100 (clamped) | A | Size change across the height. |

Every instance also takes `expand` (number px or `"none"`); see 01-effects-basics.md.

### `distort.ccBlobbylize`

After Effects: CC Blobbylize · Phase: P2 · Status: implemented · Tiling: whole · Reads: other layers · Reads time: no · Device: CPU

Lit blobs shaped by the blob layer's `property`.

| Parameter | Type | Default | Range | Anim | What it does |
|---|---|---|---|---|---|
| `blobLayer` | layer id | none | — | — | The layer whose property shapes the blobs (null = this layer). |
| `blobLayerSource` | enum `source` / `masks` / `effects` | `effects` | — | — | What of the other layer is read (spec 7 §7.6). |
| `property` | enum `red` / `green` / `blue` / `alpha` / `luminance` / `hue` / `lightness` / `saturation` | `alpha` | — | — | Which property of the blob layer is the height. |
| `softness` | length px | 6 | ≥ 0 (clamped) | A | Softening of the height field (px). |
| `cutAway` | percent | 0 | 0–100 (soft) | A | Height below which the layer is cut away. |
| `light.intensity` | number | 100 | — | A | Light intensity (percent). |
| `light.color` | color | `#FFFFFF` | — | A | Light colour. |
| `light.type` | enum `distant` / `point` | `distant` | — | — | A distant or a point light. |
| `light.height` | number | 50 | — | A | Elevation of the light (percent). |
| `light.position` | point `[x, y]` | `["25%", "25%"]` | — | A | Position of a point light. |
| `light.direction` | angle ° | -45 | — | A | Direction of a distant light. |
| `shading.ambient` | number | 20 | — | A | Ambient term (percent). |
| `shading.diffuse` | number | 70 | — | A | Diffuse term (percent). |
| `shading.specular` | number | 40 | — | A | Specular term (percent). |
| `shading.roughness` | number | 0.05 | — | A | Width of the highlight. |
| `shading.metal` | percent | 100 | 0–100 (soft) | A | How much the highlight takes the surface colour. |

Every instance also takes `expand` (number px or `"none"`); see 01-effects-basics.md.

### `distort.ccScatterize`

After Effects: CC Scatterize · Phase: P2 · Status: implemented · Tiling: whole · Reads: — · Reads time: no · Device: CPU

Pixels scattered (seeded) and twisted; `scatter: 0` is the identity.

| Parameter | Type | Default | Range | Anim | What it does |
|---|---|---|---|---|---|
| `scatter` | number | 0 | ≥ 0 (clamped) | A | Jitter of each dot (px). |
| `rightTwist` | angle ° | 0 | — | A | Twist of the right half about the horizontal axis. |
| `leftTwist` | angle ° | 0 | — | A | Twist of the left half about the horizontal axis. |
| `transferMode` | enum `composite` / `add` | `composite` | — | — | Dots over each other, or added. |

Every instance also takes `expand` (number px or `"none"`); see 01-effects-basics.md.

### `distort.glass`

After Effects: — ("liquid glass" / refraction) · Phase: P3 · Status: implemented · Tiling: backdrop · Reads: other layers, the backdrop · Reads time: no · Device: CPU (backdrop; the GPU walk declines the whole frame)

The 2025–2027 glass look (Apple Liquid Glass and its imitators).

| Parameter | Type | Default | Range | Anim | What it does |
|---|---|---|---|---|---|
| `normalSource` | enum `bevel` / `layer` / `flat` | `bevel` | — | — | Where the surface normals come from. |
| `normalLayer` | layer id | none | — | — | A normal map (RGB) or height map (gray) for `normalSource: layer`. |
| `normalKind` | enum `auto` / `normal` / `height` | `auto` | — | — | How `normalLayer` is read: a tangent-space `normal` map, a gray `height` map, or `auto` (a normal map when at least half its opaque pixels are colored). |
| `bevelSize` | length px | 24 | ≥ 0 (clamped) | A | Width of the rounded bevel inside the shape's edge. |
| `bevelProfile` | enum `round` / `linear` / `smooth` / `squircle` | `squircle` | — | — | Cross-section of the bevel. |
| `refraction` | number | 1.45 | 1–3 (clamped) | A | Index of refraction (1 = no bending). |
| `thickness` | length px | 30 | ≥ 0 (clamped) | A | Distance the refracted ray travels to the backdrop. |
| `dispersion` | number | 0.02 | 0–0.5 (clamped) | A | Spread of the index of refraction between R, G and B. |
| `frost` | length px | 8 | ≥ 0 (clamped) | A | Blur of what is seen through the glass (a radius, as `blur.gaussian`). |
| `backdrop` | enum `below` / `layer` | `below` | — | — | What is seen through: the composite below, or a layer. |
| `backdropLayer` | layer id | none | — | — | The layer seen through for `backdrop: layer`. |
| `tint` | color | `#FFFFFF10` | — | A | Tint laid over what is seen through (its alpha is the strength). |
| `specular` | object (group of the dotted parameters below) | none | — | — | The specular highlight and rim light: `intensity`, `angle`, `size`, `rim`. |
| `specular.intensity` | number | 0.6 | 0–10 (clamped) | A | Strength of the highlight and the rim. |
| `specular.angle` | angle ° | -45 | — | A | Direction the light comes from (0 = up, clockwise). |
| `specular.size` | number | 0.3 | 0.01–1 (clamped) | A | Size of the highlight on the bevel. |
| `specular.rim` | percent | 40 | 0–100 (soft) | A | Brightness of the rim light along the edge. |
| `shadow` | object (group of the dotted parameters below) | none | — | — | The soft shadow under the glass: `opacity`, `softness`, `offset`. |
| `shadow.opacity` | percent | 20 | 0–100 (soft) | A | Opacity of the soft shadow under the glass. |
| `shadow.softness` | length px | 12 | ≥ 0 (clamped) | A | Blur of the shadow (a radius). |
| `shadow.offset` | point `[x, y]` | `[0, 6]` | — | A | Offset of the shadow. |
| `saturation` | percent | 110 | 0–400 (soft) | A | Saturation of what is seen through. |

Every instance also takes `expand` (number px or `"none"`); see 01-effects-basics.md.

### `distort.liquify`

After Effects: Liquify (simplified) · Phase: P3 · Status: implemented · Tiling: whole · Reads: — · Reads time: no · Device: CPU

Implemented as a precomputed displacement field from the strokes (no painting state): dabs every quarter radius along each polyline into a mesh over the layer rect.

| Parameter | Type | Default | Range | Anim | What it does |
|---|---|---|---|---|---|
| `strokes` | list of `{ points: [[x, y], …], size: length (64), pressure: percent (50), mode: push | twirl | pucker | bloat (push) }` | `[]` | — | A | Brush strokes in layer pixels, replayed in order. |
| `distortion` | percent | 100 | 0–400 (soft) | A | How much of the strokes' displacement applies. |

Every instance also takes `expand` (number px or `"none"`); see 01-effects-basics.md.

### `distort.smear`

After Effects: Smear · Phase: P3 · Status: implemented · Tiling: whole · Reads: mask paths · Reads time: no · Device: CPU

Implemented: `stretch` is After Effects' Percent (how far the warp applies); the elasticity is fixed at After Effects' "Absolutely Normal"; both outlines are resampled to at most 256 points and rasterized (which side of each a pixel is on), and the two distances a pixel's weight uses are exact at samples every 8 px and at every pixel within a cell of an outline, interpolated between the samples elsewhere (engine 0.1.55 and earlier measured them exactly at every pixel; the planes agree within a pixel or so far from the outlines, exactly near them); the displacement is capped at the layer's larger side (16–1024 px).

| Parameter | Type | Default | Range | Anim | What it does |
|---|---|---|---|---|---|
| `sourceMask` | mask id | none | — | — | Mask id of the outline that is moved. |
| `boundaryMask` | mask id | none | — | — | Mask id of the closed outline outside which nothing moves. |
| `offset` | point `[x, y]` | `[0, 0]` | — | A | How far the source outline moves (px). |
| `rotation` | angle ° | 0 | — | A | Rotation of the source outline around its centroid. |
| `scale` | percent | 100 | 1–1000 (soft) | A | Scale of the source outline around its centroid. |
| `stretch` | percent | 100 | 0–100 (soft) | A | How far the layer follows the moved outline. |

Every instance also takes `expand` (number px or `"none"`); see 01-effects-basics.md.

<!-- gen:catalogue-distort-1:end -->
