# Utility and expression controls: every parameter

Generated from `rexx-engine effects` by scripts/skills-effects-catalogue.py; do not edit by hand. Index: [90-catalogue.md](90-catalogue.md).

<!-- gen:catalogue-utility-1:start -->
### `control.slider`

After Effects: Slider Control · Phase: P1 · Status: implemented · Tiling: tiled · Reads: — · Reads time: no · Device: — (no pixels)

An expression control: carries a value, touches no pixels; allowed on `null`, `camera` and `light` layers.

| Parameter | Type | Default | Range | Anim | What it does |
|---|---|---|---|---|---|
| `value` | number | 0 | — | A | The slider value. |
| `min` | number | 0 | — | — | UI hint: slider minimum. |
| `max` | number | 100 | — | — | UI hint: slider maximum. |

Every instance also takes `expand` (number px or `"none"`); see 01-effects-basics.md.

### `control.angle`

After Effects: Angle Control · Phase: P1 · Status: implemented · Tiling: tiled · Reads: — · Reads time: no · Device: — (no pixels)

An expression control: carries a value, touches no pixels; allowed on `null`, `camera` and `light` layers.

| Parameter | Type | Default | Range | Anim | What it does |
|---|---|---|---|---|---|
| `value` | angle ° | 0 | — | A | The angle value. |

Every instance also takes `expand` (number px or `"none"`); see 01-effects-basics.md.

### `control.point`

After Effects: Point Control · Phase: P1 · Status: implemented · Tiling: tiled · Reads: — · Reads time: no · Device: — (no pixels)

An expression control: carries a value, touches no pixels; allowed on `null`, `camera` and `light` layers.

| Parameter | Type | Default | Range | Anim | What it does |
|---|---|---|---|---|---|
| `value` | point `[x, y]` | `[0, 0]` | — | A | The point value. |

Every instance also takes `expand` (number px or `"none"`); see 01-effects-basics.md.

### `control.point3d`

After Effects: 3D Point Control · Phase: P1 · Status: implemented · Tiling: tiled · Reads: — · Reads time: no · Device: — (no pixels)

An expression control: carries a value, touches no pixels; allowed on `null`, `camera` and `light` layers.

| Parameter | Type | Default | Range | Anim | What it does |
|---|---|---|---|---|---|
| `value` | point3d `[x, y, z]` | `[0, 0, 0]` | — | A | The 3D point value. |

Every instance also takes `expand` (number px or `"none"`); see 01-effects-basics.md.

### `control.color`

After Effects: Color Control · Phase: P1 · Status: implemented · Tiling: tiled · Reads: — · Reads time: no · Device: — (no pixels)

An expression control: carries a value, touches no pixels; allowed on `null`, `camera` and `light` layers.

| Parameter | Type | Default | Range | Anim | What it does |
|---|---|---|---|---|---|
| `value` | color | `#FFFFFF` | — | A | The color value. |

Every instance also takes `expand` (number px or `"none"`); see 01-effects-basics.md.

### `control.checkbox`

After Effects: Checkbox Control · Phase: P1 · Status: implemented · Tiling: tiled · Reads: — · Reads time: no · Device: — (no pixels)

An expression control: carries a value, touches no pixels; allowed on `null`, `camera` and `light` layers.

| Parameter | Type | Default | Range | Anim | What it does |
|---|---|---|---|---|---|
| `value` | boolean | false | — | A | The checkbox value (hold when animated). |

Every instance also takes `expand` (number px or `"none"`); see 01-effects-basics.md.

### `control.layer`

After Effects: Layer Control · Phase: P1 · Status: implemented · Tiling: tiled · Reads: other layers · Reads time: no · Device: — (no pixels)

Not animatable.

An expression control: carries a value, touches no pixels; allowed on `null`, `camera` and `light` layers.

| Parameter | Type | Default | Range | Anim | What it does |
|---|---|---|---|---|---|
| `value` | layer id | none | — | — | The layer reference. |

Every instance also takes `expand` (number px or `"none"`); see 01-effects-basics.md.

### `control.dropdown`

After Effects: Dropdown Menu Control · Phase: P1 · Status: implemented · Tiling: tiled · Reads: — · Reads time: no · Device: — (no pixels)

An expression control: carries a value, touches no pixels; allowed on `null`, `camera` and `light` layers.

| Parameter | Type | Default | Range | Anim | What it does |
|---|---|---|---|---|---|
| `items` | list of `string` | `[]` | — | A | The menu items. |
| `value` | integer | 1 | 1–1000000 (clamped) | A | The selected item, 1-based as in After Effects (hold when animated). |

Every instance also takes `expand` (number px or `"none"`); see 01-effects-basics.md.

### `utility.growBounds`

After Effects: Grow Bounds · Phase: P1 · Status: implemented · Tiling: tiled · Reads: — · Reads time: no · Device: CPU

Rarely needed, since bounds grow automatically ([7.4](#74-bounds-and-region-of-interest)); kept so imported After Effects projects map one to one.

| Parameter | Type | Default | Range | Anim | What it does |
|---|---|---|---|---|---|
| `pixels` | length px | 100 | ≥ 0 (clamped) | — | Margin added on every side (px). |

Every instance also takes `expand` (number px or `"none"`); see 01-effects-basics.md.

### `utility.applyLut`

After Effects: Apply Color LUT · Phase: P1 · Status: implemented · Tiling: tiled · Reads: — · Reads time: no · Device: GPU when the whole stack lowers, else CPU

Alias of `color.lut`.

| Parameter | Type | Default | Range | Anim | What it does |
|---|---|---|---|---|---|
| `lut` | asset id | none | — | — | The `.cube` LUT asset (1D or 3D). |
| `amount` | percent | 100 | 0–100 (soft) | A | Mix with the input. |
| `inputSpace` | enum `display` / `linear` / `logC` / `slog3` / `acescct` | `display` | — | — | The encoding the LUT expects. |
| `interpolation` | enum `tetrahedral` / `trilinear` | `tetrahedral` | — | — | 3D LUT interpolation. |

Every instance also takes `expand` (number px or `"none"`); see 01-effects-basics.md.

### `utility.removeColorMatting`

After Effects: Remove Color Matting · Phase: P1 · Status: implemented · Tiling: tiled · Reads: — · Reads time: no · Device: CPU

Premultiplied-against-a-color footage cleanup.

| Parameter | Type | Default | Range | Anim | What it does |
|---|---|---|---|---|---|
| `backgroundColor` | color | `#000000` | — | A | The color the footage was matted against. |
| `clipHdr` | boolean | false | — | — | Clamp the result to 1. |

Every instance also takes `expand` (number px or `"none"`); see 01-effects-basics.md.

### `utility.hdrCompander`

After Effects: HDR Compander · Phase: P2 · Status: implemented · Tiling: tiled · Reads: — · Reads time: no · Device: CPU

| Parameter | Type | Default | Range | Anim | What it does |
|---|---|---|---|---|---|
| `mode` | enum `compress` / `expand` | `compress` | — | — | Compress HDR values into 0–1, or expand them back. |
| `gain` | number | 1 | 1–100 (clamped) | A | The value that compresses to 1. |
| `gamma` | number | 1 | 0.1–10 (clamped) | A | Curve of the compression. |

Every instance also takes `expand` (number px or `"none"`); see 01-effects-basics.md.

### `utility.shiftChannels`

After Effects: Shift Channels · Phase: P2 · Status: implemented · Tiling: tiled · Reads: — · Reads time: no · Device: CPU

| Parameter | Type | Default | Range | Anim | What it does |
|---|---|---|---|---|---|
| `takeAlphaFrom` | enum `red` / `green` / `blue` / `alpha` / `luminance` / `hue` / `lightness` / `saturation` / `full` / `half` / `off` | `alpha` | — | — | Source of the output alpha. |
| `takeRedFrom` | enum `red` / `green` / `blue` / `alpha` / `luminance` / `hue` / `lightness` / `saturation` / `full` / `half` / `off` | `red` | — | — | Source of the output red. |
| `takeGreenFrom` | enum `red` / `green` / `blue` / `alpha` / `luminance` / `hue` / `lightness` / `saturation` / `full` / `half` / `off` | `green` | — | — | Source of the output green. |
| `takeBlueFrom` | enum `red` / `green` / `blue` / `alpha` / `luminance` / `hue` / `lightness` / `saturation` / `full` / `half` / `off` | `blue` | — | — | Source of the output blue. |

Every instance also takes `expand` (number px or `"none"`); see 01-effects-basics.md.

### `utility.channelCombiner`

After Effects: Channel Combiner · Phase: P2 · Status: implemented · Tiling: tiled · Reads: other layers · Reads time: no · Device: CPU

Enum lists pinned to After Effects' at P2.

| Parameter | Type | Default | Range | Anim | What it does |
|---|---|---|---|---|---|
| `source` | enum `rgbToHls` / `hlsToRgb` / `rgbToYuv` / `yuvToRgb` / `lightness` / `hue` / `saturation` / `luminance` / `maxRgb` / `minRgb` / `red` / `green` / `blue` / `alpha` / `straightAlpha` / `gray` | `rgbToHls` | — | — | What is read from the pixel (After Effects' From list). |
| `from` | enum `red` / `green` / `blue` / `alpha` / `luminance` / `hue` / `lightness` / `saturation` / `max` / `min` | `luminance` | — | — | Alias of `source` for the single-value sources; used when `source` is absent. |
| `to` | enum `red` / `green` / `blue` / `alpha` / `luminance` / `hue` / `lightness` / `saturation` / `max` / `min` | `luminance` | — | — | Which channel a single value goes to. |
| `useSecondLayer` | layer id | none | — | — | Read the values from this layer instead (null = this layer). |
| `useSecondLayerSource` | enum `source` / `masks` / `effects` | `effects` | — | — | What of the other layer is read (spec 7 §7.6). |
| `invert` | boolean | false | — | — | Invert the read values. |

Every instance also takes `expand` (number px or `"none"`); see 01-effects-basics.md.

### `utility.minMax`

After Effects: Minimax · Phase: P2 · Status: implemented · Tiling: whole · Reads: — · Reads time: no · Device: CPU

| Parameter | Type | Default | Range | Anim | What it does |
|---|---|---|---|---|---|
| `operation` | enum `minimum` / `maximum` / `minThenMax` / `maxThenMin` | `maximum` | — | — | Minimum, maximum, or one then the other. |
| `radius` | length px | 0 | ≥ 0 (clamped) | A | Window half-width in px (fractional). |
| `channel` | enum `color` / `alpha` / `alphaAndColor` / `red` / `green` / `blue` | `color` | — | — | Which channels the window runs over. |
| `direction` | enum `both` / `horizontal` / `vertical` | `both` | — | — | Which axes the window spans. |
| `dontShrinkEdges` | boolean | false | — | — | Extend the layer's edge pixels instead of treating the outside as 0. |

Every instance also takes `expand` (number px or `"none"`); see 01-effects-basics.md.

### `utility.setChannels`

After Effects: Set Channels · Phase: P2 · Status: implemented · Tiling: tiled · Reads: other layers · Reads time: no · Device: CPU

| Parameter | Type | Default | Range | Anim | What it does |
|---|---|---|---|---|---|
| `red.source` | layer id | none | — | — | Layer the red channel is taken from (none = this layer). |
| `red.channel` | enum `red` / `green` / `blue` / `alpha` / `luminance` / `hue` / `lightness` / `saturation` / `full` / `half` / `off` | `red` | — | — | Channel of its source that becomes red. |
| `green.source` | layer id | none | — | — | Layer the green channel is taken from (none = this layer). |
| `green.channel` | enum `red` / `green` / `blue` / `alpha` / `luminance` / `hue` / `lightness` / `saturation` / `full` / `half` / `off` | `green` | — | — | Channel of its source that becomes green. |
| `blue.source` | layer id | none | — | — | Layer the blue channel is taken from (none = this layer). |
| `blue.channel` | enum `red` / `green` / `blue` / `alpha` / `luminance` / `hue` / `lightness` / `saturation` / `full` / `half` / `off` | `blue` | — | — | Channel of its source that becomes blue. |
| `alpha.source` | layer id | none | — | — | Layer the alpha channel is taken from (none = this layer). |
| `alpha.channel` | enum `red` / `green` / `blue` / `alpha` / `luminance` / `hue` / `lightness` / `saturation` / `full` / `half` / `off` | `alpha` | — | — | Channel of its source that becomes alpha. |
| `stretch` | boolean | true | — | — | Stretch other layers to this layer's rect (otherwise centre them). |

Every instance also takes `expand` (number px or `"none"`); see 01-effects-basics.md.

### `utility.colorProfile`

After Effects: Color Profile Converter · Phase: P2 · Status: implemented · Tiling: tiled · Reads: — · Reads time: no · Device: CPU

Explicit space conversion inside a stack ([spec 13](13-color-and-output.md)).

| Parameter | Type | Default | Range | Anim | What it does |
|---|---|---|---|---|---|
| `inputSpace` | enum `working` / `srgb` / `rec709` / `rec2020` / `displayP3` / `acescg` | `working` | — | — | How the layer's values are read. |
| `linearizeInput` | boolean | false | — | — | Read the input as linear whatever its profile's transfer. |
| `outputSpace` | enum `working` / `srgb` / `rec709` / `rec2020` / `displayP3` / `acescg` | `working` | — | — | How the output is encoded. |
| `linearizeOutput` | boolean | false | — | — | Write the output linear whatever its profile's transfer. |
| `intent` | enum `perceptual` / `relativeColorimetric` / `saturation` / `absoluteColorimetric` | `relativeColorimetric` | — | — | What happens to colors outside the output gamut. |

Every instance also takes `expand` (number px or `"none"`); see 01-effects-basics.md.

### `utility.ccOverbrights`

After Effects: CC Overbrights · Phase: P2 · Status: implemented · Tiling: tiled · Reads: — · Reads time: no · Device: CPU

Paints pixels above 1.0 in `highlightColor` (a diagnostic; `motion.check` is the usual tool).

| Parameter | Type | Default | Range | Anim | What it does |
|---|---|---|---|---|---|
| `channel` | enum `maxRgb` / `red` / `green` / `blue` / `alpha` / `luminance` | `maxRgb` | — | — | Which value is checked. |
| `highlightColor` | color | `#FF0000` | — | A | Painted where the value exceeds 1. |

Every instance also takes `expand` (number px or `"none"`); see 01-effects-basics.md.

### `utility.hdrHighlightCompression`

After Effects: HDR Highlight Compression · Phase: P2 · Status: implemented · Tiling: tiled · Reads: — · Reads time: no · Device: CPU

Rolls values above 1.0 into range by `amount` (`utility.hdrCompander` is the invertible pair).

| Parameter | Type | Default | Range | Anim | What it does |
|---|---|---|---|---|---|
| `amount` | percent | 100 | 0–100 (soft) | A | How much of the roll-off applies. |

Every instance also takes `expand` (number px or `"none"`); see 01-effects-basics.md.

### `utility.arithmetic`

After Effects: Arithmetic · Phase: P2 · Status: implemented · Tiling: tiled · Reads: — · Reads time: no · Device: GPU when the whole stack lowers, else CPU

Per-channel arithmetic with a constant, on display-encoded 0–255 values.

| Parameter | Type | Default | Range | Anim | What it does |
|---|---|---|---|---|---|
| `operator` | enum `and` / `or` / `xor` / `add` / `subtract` / `difference` / `min` / `max` / `blockAbove` / `blockBelow` / `slice` / `multiply` / `screen` | `add` | — | — | How each channel combines with its constant. |
| `redValue` | number | 0 | 0–255 (clamped) | A | Red constant (0–255). |
| `greenValue` | number | 0 | 0–255 (clamped) | A | Green constant (0–255). |
| `blueValue` | number | 0 | 0–255 (clamped) | A | Blue constant (0–255). |
| `clip` | boolean | true | — | — | Clamp the result to 0–1. |

Every instance also takes `expand` (number px or `"none"`); see 01-effects-basics.md.

### `utility.blend`

After Effects: Blend · Phase: P2 · Status: implemented · Tiling: tiled · Reads: other layers · Reads time: no · Device: CPU

Blends with another layer by one of five legacy modes (for anything else use the layer's `blend`, [spec 6](06-masks-mattes-blending.md)).

| Parameter | Type | Default | Range | Anim | What it does |
|---|---|---|---|---|---|
| `blendWithLayer` | layer id | none | — | — | The layer blended in (null = this layer). |
| `blendWithLayerSource` | enum `source` / `masks` / `effects` | `effects` | — | — | What of the other layer is read (spec 7 §7.6). |
| `mode` | enum `crossfade` / `colorOnly` / `tintOnly` / `darkenOnly` / `lightenOnly` | `crossfade` | — | — | The legacy blend mode. |
| `blendWithOriginal` | percent | 0 | 0–100 (soft) | A | Mix back toward the layer. |
| `ifLayerSizesDiffer` | enum `center` / `stretch` | `center` | — | — | How the other layer is placed on the layer rect. |

Every instance also takes `expand` (number px or `"none"`); see 01-effects-basics.md.

### `utility.calculations`

After Effects: Calculations · Phase: P2 · Status: implemented · Tiling: tiled · Reads: other layers · Reads time: no · Device: CPU

Photoshop Calculations: a channel of this layer blended with a channel of another.

| Parameter | Type | Default | Range | Anim | What it does |
|---|---|---|---|---|---|
| `inputChannel` | enum `rgba` / `gray` / `red` / `green` / `blue` / `alpha` | `rgba` | — | — | What of the layer is used. |
| `invertInput` | boolean | false | — | — | Invert the input channel. |
| `secondLayer` | layer id | none | — | — | The layer blended in (null = none). |
| `secondLayerSource` | enum `source` / `masks` / `effects` | `effects` | — | — | What of the other layer is read (spec 7 §7.6). |
| `secondLayerChannel` | enum `rgba` / `gray` / `red` / `green` / `blue` / `alpha` | `rgba` | — | — | What of the second layer is used. |
| `secondLayerOpacity` | percent | 100 | 0–100 (soft) | A | Opacity of the second layer. |
| `invertSecondLayer` | boolean | false | — | — | Invert the second layer's channel. |
| `stretchSecondLayerToFit` | boolean | true | — | — | Stretch the second layer to the layer rect. |
| `blendingMode` | blend mode (any of the 38; see 20-utility-controls.md) | `normal` | — | — | Blend mode of the second layer over the first (spec 6). |
| `preserveTransparency` | boolean | false | — | — | Keep the layer's own alpha. |

Every instance also takes `expand` (number px or `"none"`); see 01-effects-basics.md.

### `utility.ccComposite`

After Effects: CC Composite · Phase: P2 · Status: implemented · Tiling: tiled · Reads: other layers · Reads time: no · Device: CPU

Composites the layer's unprocessed source back over the effect chain so far (the one effect that reads the chain's input).

| Parameter | Type | Default | Range | Anim | What it does |
|---|---|---|---|---|---|
| `opacity` | percent | 100 | 0–100 (soft) | A | Opacity of the original. |
| `compositeOriginal` | enum `inFront` / `inBack` / `add` / `multiply` / `screen` / `overlay` / `softLight` / `hardLight` / `darken` / `lighten` / `difference` / `hue` / `saturation` / `color` / `luminosity` / `stencilAlpha` | `inFront` | — | — | How the original combines with the chain. |
| `rgbOnly` | boolean | false | — | — | Keep the chain's alpha. |
| `original` | layer id | none | — | — | The unprocessed source (null = the input of this effect). |
| `originalSource` | enum `source` / `masks` / `effects` | `source` | — | — | What of the `original` layer is read (spec 7 §7.6). |

Every instance also takes `expand` (number px or `"none"`); see 01-effects-basics.md.

### `utility.compoundArithmetic`

After Effects: Compound Arithmetic · Phase: P2 · Status: implemented · Tiling: tiled · Reads: other layers · Reads time: no · Device: CPU

Layer-to-layer arithmetic.

| Parameter | Type | Default | Range | Anim | What it does |
|---|---|---|---|---|---|
| `secondSource` | layer id | none | — | — | The second layer (null = this layer). |
| `secondSourceSource` | enum `source` / `masks` / `effects` | `effects` | — | — | What of the other layer is read (spec 7 §7.6). |
| `operator` | enum `copy` / `add` / `subtract` / `multiply` / `difference` / `and` / `or` / `xor` / `lighten` / `darken` / `minimum` / `maximum` / `screen` / `overlay` / `hardLight` | `copy` | — | — | The channel operation. |
| `operateOnChannels` | enum `rgb` / `argb` / `alpha` | `rgb` | — | — | Which channels are combined. |
| `overflowBehavior` | enum `clip` / `wrap` / `scale` | `clip` | — | — | What happens to values outside 0–1. |
| `stretchSecondSourceToFit` | boolean | true | — | — | Stretch the second layer to the layer rect. |
| `blendWithOriginal` | percent | 0 | 0–100 (soft) | A | Mix back toward the layer. |

Every instance also takes `expand` (number px or `"none"`); see 01-effects-basics.md.

### `utility.solidComposite`

After Effects: Solid Composite · Phase: P2 · Status: implemented · Tiling: tiled · Reads: — · Reads time: no · Device: GPU when the whole stack lowers, else CPU

Composites the layer over a solid colour.

| Parameter | Type | Default | Range | Anim | What it does |
|---|---|---|---|---|---|
| `sourceOpacity` | percent | 100 | 0–100 (soft) | A | Opacity of the layer over the solid. |
| `color` | color | `#FFFFFF` | — | A | The solid's color. |
| `opacity` | percent | 100 | 0–100 (soft) | A | Opacity of the solid. |
| `blendingMode` | enum `normal` / `add` / `multiply` / `screen` / `overlay` / `softLight` / `hardLight` / `darken` / `lighten` / `difference` / `color` / `luminosity` | `normal` | — | — | Blend mode of the layer over the solid. |

Every instance also takes `expand` (number px or `"none"`); see 01-effects-basics.md.

### `utility.shader`

After Effects: — (custom shader) · Phase: P4 · Status: implemented · Tiling: whole · Reads: — · Reads time: yes · Device: GPU only

GPU-only (renders on the GPU pool; on a CPU box, or in a job the backend decision puts on the CPU, `effect.requires_gpu` and the layer passes through unshaded; `motion.check` says so in advance as `estimate.requiresGpu`).

| Parameter | Type | Default | Range | Anim | What it does |
|---|---|---|---|---|---|
| `code` | string | required | — | — | WGSL source with `fn effect(uv: vec2f, t: f32) -> vec4f`; `input`, `input1`…`input4`, `samp`, `rexx` and `params` are bound by the engine (spec 7 §7.9.11). |
| `params` | object of uniforms (see 30-shader.md) | `{}` | — | A | Declared uniforms `{ name: { type: float/vec2/vec3/vec4/color, default } }`, read as `params.<name>`; each `default` is animatable on its own (keys, drivers, expressions) at `effects.<id>.params.<name>.default`. A bare value is typed by its shape. |
| `budgetMs` | number | 0 | ≥ 0 (clamped) | A | The dispatch's GPU time budget in milliseconds (`effect.shader_timeout` past it, the layer unshaded for the frame); 0 is the job's: 50 ms of device time on a hardware adapter (10× that on the wall clock of the dispatch and its readback where the adapter has no timestamp queries), none on a software adapter. |
| `inputs` | list of `layer ids` | `[]` | — | A | Up to four other layers of the comp, read in the shader as `input1`…`input4` (each over its own uv square). |

Every instance also takes `expand` (number px or `"none"`); see 01-effects-basics.md.

<!-- gen:catalogue-utility-1:end -->
