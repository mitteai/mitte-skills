# Time: every parameter

Generated from `rexx-engine effects` by scripts/skills-effects-catalogue.py; do not edit by hand. Index: [90-catalogue.md](90-catalogue.md).

<!-- gen:catalogue-time-1:start -->
### `time.difference`

After Effects: Time Difference · Phase: P3 · Status: implemented · Tiling: tiled · Reads: other layers · Reads time: no · Device: CPU

Implemented: a `target` layer is read at the frame's own time (7.6); `timeOffset` applies only to the layer itself (`target` null); a time or layer the renderer does not supply reads as transparent.

| Parameter | Type | Default | Range | Anim | What it does |
|---|---|---|---|---|---|
| `target` | layer id | none | — | — | The layer to compare with (null = this layer at `timeOffset`). |
| `targetSource` | enum `source` / `masks` / `effects` | `effects` | — | — | What of the other layer is read (spec 7 §7.6). |
| `timeOffset` | number | 0 | -3600–3600 (clamped) | A | Seconds from the frame the layer is compared at. |
| `contrast` | number | 0 | 0–100 (clamped) | A | Gain of the difference: 1 + contrast / 25. |
| `absoluteDifference` | boolean | true | — | — | \|a − b\| instead of 0.5 + (a − b) / 2. |
| `alphaChannel` | enum `original` / `target` / `blend` / `max` / `fullOn` / `lightnessOfResult` / `maxOfResult` / `alphaDifference` / `alphaDifferenceOnly` | `original` | — | — | Where the result's alpha comes from. |

Every instance also takes `expand` (number px or `"none"`); see 01-effects-basics.md.

### `time.posterize`

After Effects: Posterize Time · Phase: P1 · Status: implemented · Tiling: tiled · Reads: — · Reads time: no · Device: CPU

Quantizes the time the layer's **content** is evaluated at (source, masks, and the effects above it in the stack, with their keyframes), through the upstream-time override of [7.5](#75-time-randomness-and-determinism).

| Parameter | Type | Default | Range | Anim | What it does |
|---|---|---|---|---|---|
| `fps` | number | 24 | ≥ 0 (clamped) | A | Frame rate the upstream content is held at (0 = off). |

Every instance also takes `expand` (number px or `"none"`); see 01-effects-basics.md.

### `time.echo`

After Effects: Echo · Phase: P2 · Status: implemented · Tiling: tiled · Reads: other times · Reads time: no · Device: CPU

Motion trails: the layer (after its earlier effects) at `t + i · echoTime` for *i* = 1 … `count`, declared as `Deps::times` and supplied by the renderer as `Inputs::times` (a declared time the renderer does not supply reads as transparent), combined with the frame itself (*i* = 0) in order of *i* by `operator`, each weighted `startingIntensity · decay^i`: `add` sums, `maximum` / `minimum` take the extremes per channel, `screen` screens, `compositeInBack` puts every later echo behind what is there, `compositeInFront` on top, `blend` averages.

| Parameter | Type | Default | Range | Anim | What it does |
|---|---|---|---|---|---|
| `echoTime` | number | -0.041666666666666664 | — | A | Seconds between echoes (negative = earlier frames; default −1 / fps). |
| `count` | integer | 1 | 0–32 (clamped) | A | Number of echoes. |
| `startingIntensity` | number | 1 | 0–1 (clamped) | A | Weight of the frame itself. |
| `decay` | number | 1 | 0–1 (clamped) | A | Weight ratio between consecutive echoes. |
| `operator` | enum `add` / `maximum` / `minimum` / `screen` / `compositeInBack` / `compositeInFront` / `blend` | `compositeInBack` | — | — | How the echoes combine. |

Every instance also takes `expand` (number px or `"none"`); see 01-effects-basics.md.

### `time.strobe`

After Effects: Strobe Light · Phase: P2 · Status: implemented · Tiling: tiled · Reads: — · Reads time: yes · Device: CPU

Every `period` seconds the layer flashes for `duration` seconds (and, with `randomStrobe` percent, hashed whole periods flash at random): `operatesOnColorOnly` combines `color` with the layer's display-encoded color by `operator`, mixed back by `blend`; `makesLayerTransparent` scales the alpha by `blend`.

| Parameter | Type | Default | Range | Anim | What it does |
|---|---|---|---|---|---|
| `color` | color | `#FFFFFF` | — | A | Strobe color. |
| `blend` | percent | 0 | 0–100 (soft) | A | Mix of the original back in (or the alpha kept, when transparent). |
| `duration` | number | 0.1 | ≥ 0 (clamped) | A | Length of a flash in seconds. |
| `period` | number | 1 | ≥ 0 (clamped) | A | Seconds between flashes (0 = off). |
| `randomStrobe` | percent | 0 | 0–100 (soft) | A | Chance that a whole period flashes at random. |
| `strobe` | enum `operatesOnColorOnly` / `makesLayerTransparent` | `operatesOnColorOnly` | — | — | What a flash does. |
| `operator` | enum `copy` / `add` / `subtract` / `multiply` / `difference` / `screen` / `lighten` / `darken` | `copy` | — | — | How the color lands on the layer. |
| `seed` | integer seed | 0 | — | — | Random seed (spec 7 §7.5). |

Every instance also takes `expand` (number px or `"none"`) and `seed`; see 01-effects-basics.md.

### `time.displacement`

After Effects: Time Displacement · Phase: P2 · Status: implemented · Tiling: tiled · Reads: other layers, other times · Reads time: no · Device: CPU

Slit-scan and time-warp looks.

| Parameter | Type | Default | Range | Anim | What it does |
|---|---|---|---|---|---|
| `map` | layer id | none | — | — | The layer whose luminance offsets time (none = this layer). |
| `mapSource` | enum `source` / `masks` / `effects` | `effects` | — | — | What of the other layer is read (spec 7 §7.6). |
| `maxDisplacement` | number | 1 | ≥ 0 (clamped) | A | Time offset at white (and −offset at black), seconds. |
| `resolution` | percent | 100 | 1–1000 (soft) | A | Time steps per frame: 100 % = whole frames. |
| `stretch` | boolean | true | — | — | Stretch the map to this layer's rect (otherwise centre it). |

Every instance also takes `expand` (number px or `"none"`); see 01-effects-basics.md.

### `time.frameBlend`

After Effects: Frame Blending (as an effect) · Phase: P2 · Status: implemented · Tiling: tiled · Reads: — · Reads time: no · Device: CPU

Same as the layer's `frameBlend` ([spec 2 §2.10](02-time-and-animation.md#210-layer-timing)) but placeable inside the stack: between two comp frames of the layer, `mix` crossfades the layer (source, masks and the effects above) at the frame before and after, `flow` interpolates the two along their optical flow ([spec 10 §10.3.3](10-media-and-audio.md#1033-frame-blending): the same flow as the layer-level `flow`, estimated on the whole frame pair, cached per layer and effect).

| Parameter | Type | Default | Range | Anim | What it does |
|---|---|---|---|---|---|
| `mode` | enum `mix` / `flow` | `mix` | — | — | `mix` crossfades the two frames; `flow` interpolates them along their optical flow. |

Every instance also takes `expand` (number px or `"none"`); see 01-effects-basics.md.

### `time.ccWideTime`

After Effects: CC Wide Time · Phase: P2 · Status: implemented · Tiling: tiled · Reads: other times · Reads time: no · Device: CPU

Averages the layer over the surrounding frames (declares `Deps::times` like `time.echo`).

| Parameter | Type | Default | Range | Anim | What it does |
|---|---|---|---|---|---|
| `forwardSteps` | integer | 3 | 0–45 (clamped) | A | Frames after the frame. |
| `backwardSteps` | integer | 3 | 0–45 (clamped) | A | Frames before the frame. |
| `nativeMotionBlur` | enum `off` / `on` | `off` | — | — | Accepted; the layer's own motion blur applies. |

Every instance also takes `expand` (number px or `"none"`); see 01-effects-basics.md.

<!-- gen:catalogue-time-1:end -->
