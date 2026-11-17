# Keying & matte: every parameter

Generated from `rexx-engine effects` by scripts/skills-effects-catalogue.py; do not edit by hand. Index: [90-catalogue.md](90-catalogue.md).

<!-- gen:catalogue-keying-1:start -->
### `key.difference`

After Effects: Difference Matte · Phase: P3 · Status: implemented · Tiling: whole · Reads: other layers · Reads time: no · Device: CPU

Implemented: the largest difference of the display-encoded straight R, G, B and alpha against the other layer, centred on this one; `blurBeforeDifference` is a Gaussian of σ = half the length on both before comparing; a null or missing `layer` passes the layer through.

| Parameter | Type | Default | Range | Anim | What it does |
|---|---|---|---|---|---|
| `layer` | layer id | none | — | — | The clean plate to compare with (centred on this layer). |
| `layerSource` | enum `source` / `masks` / `effects` | `effects` | — | — | What of the other layer is read (spec 7 §7.6). |
| `tolerance` | percent | 15 | 0–100 (soft) | A | Difference at or below which a pixel is keyed out. |
| `softness` | percent | 0 | 0–100 (soft) | A | Ramp above the tolerance over which pixels fade in. |
| `blurBeforeDifference` | length px | 0 | ≥ 0 (clamped) | A | Blur of both layers before comparing them (px). |

Every instance also takes `expand` (number px or `"none"`); see 01-effects-basics.md.

### `matte.refine`

After Effects: Refine Soft Matte · Phase: P3 · Status: implemented · Tiling: whole · Reads: — · Reads time: no · Device: CPU

Guided-filter refinement against the layer's color; for hair edges on AI or keyed footage.

| Parameter | Type | Default | Range | Anim | What it does |
|---|---|---|---|---|---|
| `smooth` | percent | 0 | 0–100 (soft) | A | Regularisation of the guided filter: smoother, less edge-following. |
| `feather` | percent | 0 | 0–100 (soft) | A | Blur of the refined matte, percent of the radius. |
| `choke` | number | 0 | -100–100 (clamped) | A | Shrinks (positive) or grows the matte. |
| `shiftEdge` | number | 0 | -100–100 (clamped) | A | Moves the soft edge out (positive) or in. |
| `reduceChatter` | percent | 0 | 0–100 (soft) | A | Average with the neighbouring frames where they agree. |
| `decontaminate` | boolean | true | — | — | Pull edge colours toward their surroundings. |
| `decontaminationAmount` | percent | 100 | 0–100 (soft) | A | How far the edge colours move. |
| `motionBlur` | boolean | false | — | — | Average the matte over the comp shutter. |
| `radius` | length px | 8 | ≥ 0 (clamped) | A | Window radius of the guided filter (px). |

Every instance also takes `expand` (number px or `"none"`); see 01-effects-basics.md.

### `key.unmult`

After Effects: Unmult (AE 26.0) · Phase: P1 · Status: implemented · Tiling: tiled · Reads: — · Reads time: no · Device: GPU when the whole stack lowers, else CPU

Derives alpha from brightness and divides it out: drop fire, light leaks, flares shot on black over anything.

| Parameter | Type | Default | Range | Anim | What it does |
|---|---|---|---|---|---|
| `threshold` | number | 0 | 0–0.99 (clamped) | A | Brightness below which pixels become fully transparent. |

Every instance also takes `expand` (number px or `"none"`); see 01-effects-basics.md.

### `matte.simpleChoker`

After Effects: Simple Choker · Phase: P1 · Status: implemented · Tiling: whole · Reads: — · Reads time: no · Device: CPU

Distance-field based (fractional, smooth when animated); reads `\|choke\|` + 2 px beyond an output tile.

| Parameter | Type | Default | Range | Anim | What it does |
|---|---|---|---|---|---|
| `choke` | length px, signed | 0 | any | A | Positive shrinks the matte, negative grows it (px). |

Every instance also takes `expand` (number px or `"none"`); see 01-effects-basics.md.

### `matte.set`

After Effects: Set Matte · Phase: P1 · Status: implemented · Tiling: tiled · Reads: other layers · Reads time: no · Device: CPU

Takes alpha from another layer inside the effect stack (useful when a track matte is not flexible enough, e.g. a matte that must apply before a glow).

| Parameter | Type | Default | Range | Anim | What it does |
|---|---|---|---|---|---|
| `source` | layer id | none | — | — | The layer the matte is read from (null = this layer). |
| `sourceSource` | enum `source` / `masks` / `effects` | `effects` | — | — | What of the other layer is read (spec 7 §7.6). |
| `channel` | enum `red` / `green` / `blue` / `alpha` / `luminance` / `hue` / `lightness` / `saturation` / `full` / `off` | `alpha` | — | — | Which channel of the matte layer is used. |
| `invert` | boolean | false | — | — | Invert the matte. |
| `stretch` | boolean | true | — | — | Stretch the matte layer to this layer's rect (otherwise center it). |
| `composite` | boolean | true | — | — | Multiply with the layer's own alpha instead of replacing it. |
| `premultiply` | boolean | true | — | — | Keep the straight color under the new alpha. |

Every instance also takes `expand` (number px or `"none"`); see 01-effects-basics.md.

### `key.chroma`

After Effects: Keylight (1.2) class / Key Light · Phase: P2 · Status: implemented · Tiling: whole · Reads: — · Reads time: no · Device: CPU

A color-difference keyer with despill, for AI-generated footage on green and product shoots.

| Parameter | Type | Default | Range | Anim | What it does |
|---|---|---|---|---|---|
| `screenColor` | color | `#00FF00` | — | A | The screen color. |
| `screenGain` | percent | 100 | 0–200 (soft) | A | How much the matte is pushed. |
| `screenBalance` | percent | 50 | 0–100 (soft) | A | Weight of the larger secondary channel in the screen difference. |
| `despillBias` | color | `#BCBCBC` | — | A | Color made neutral before despilling (mid grey = none). |
| `alphaBias` | color | `#BCBCBC` | — | A | Color made neutral before the matte (mid grey = none). |
| `clipBlack` | percent | 0 | 0–100 (soft) | A | Matte values below this become transparent. |
| `clipWhite` | percent | 100 | 0–100 (soft) | A | Matte values above this become opaque. |
| `clipRollback` | length px | 0 | ≥ 0 (clamped) | A | Edge detail restored within this many px of the clipped edge. |
| `screenShrinkGrow` | length px, signed | 0 | any | A | Positive grows the matte, negative shrinks it (px). |
| `screenSoftness` | length px | 0 | ≥ 0 (clamped) | A | Gaussian softening of the matte (px). |
| `screenDespotBlack` | length px | 0 | ≥ 0 (clamped) | A | Fills holes in the matte up to this size (px). |
| `screenDespotWhite` | length px | 0 | ≥ 0 (clamped) | A | Removes specks in the matte up to this size (px). |
| `replaceMethod` | enum `none` / `source` / `hardColor` / `softColor` | `softColor` | — | — | What colors areas the clipping made opaque. |
| `replaceColor` | color | `#BCBCBC` | — | A | The replace color. |
| `view` | enum `final` / `screenMatte` / `statusView` | `final` | — | — | The final result, the screen matte, or the status view. |

Every instance also takes `expand` (number px or `"none"`); see 01-effects-basics.md.

### `key.color`

After Effects: Color Key · Phase: P2 · Status: implemented · Tiling: whole · Reads: — · Reads time: no · Device: GPU when the whole stack lowers, else CPU

Pixels whose display-encoded color is within `tolerance` (percent of full scale, per channel) of `color` become transparent; the hard matte is thinned by `edgeThin` px (negative grows) and feathered by a Gaussian of σ = `edgeFeather` / 2.

| Parameter | Type | Default | Range | Anim | What it does |
|---|---|---|---|---|---|
| `color` | color | `#00FF00` | — | A | The color to key out. |
| `tolerance` | percent | 10 | 0–100 (soft) | A | Largest per-channel distance (encoded, percent) that is keyed. |
| `edgeThin` | length px, signed | 0 | any | A | Erodes (positive) or grows (negative) the matte, px. |
| `edgeFeather` | length px | 0 | ≥ 0 (clamped) | A | Gaussian feather of the matte edge, px. |

Every instance also takes `expand` (number px or `"none"`); see 01-effects-basics.md.

### `key.luma`

After Effects: Luma Key · Phase: P2 · Status: implemented · Tiling: whole · Reads: — · Reads time: no · Device: GPU when the whole stack lowers, else CPU

Keys pixels by their display-encoded luma against `threshold` (percent of full scale): brighter or darker than it, with a `tolerance`-wide ramp, or within / outside a band of `tolerance` half-width around it; then thinned and feathered as `key.color`.

| Parameter | Type | Default | Range | Anim | What it does |
|---|---|---|---|---|---|
| `type` | enum `keyOutBrighter` / `keyOutDarker` / `keyOutSimilar` / `keyOutDissimilar` | `keyOutBrighter` | — | — | Which lumas are keyed out. |
| `threshold` | percent | 50 | 0–100 (soft) | A | Luma threshold, percent of full scale (encoded). |
| `tolerance` | percent | 0 | 0–100 (soft) | A | Ramp width (brighter / darker) or band half-width (similar / dissimilar), percent. |
| `edgeThin` | length px, signed | 0 | any | A | Erodes (positive) or grows (negative) the matte, px. |
| `edgeFeather` | length px | 0 | ≥ 0 (clamped) | A | Gaussian feather of the matte edge, px. |

Every instance also takes `expand` (number px or `"none"`); see 01-effects-basics.md.

### `key.linearColor`

After Effects: Linear Color Key · Phase: P2 · Status: implemented · Tiling: tiled · Reads: — · Reads time: no · Device: GPU when the whole stack lowers, else CPU

The distance of every pixel's straight linear color to `color` in RGB, hue or chroma (normalized to [0, 1]) is mapped through a ramp from `tolerance` over `softness` to a matte; `keepColors` inverts it.

| Parameter | Type | Default | Range | Anim | What it does |
|---|---|---|---|---|---|
| `color` | color | `#00FF00` | — | A | The key color. |
| `match` | enum `rgb` / `hue` / `chroma` | `rgb` | — | — | How colors are compared. |
| `tolerance` | percent | 10 | 0–100 (soft) | A | Distance keyed in full, percent. |
| `softness` | percent | 10 | 0–100 (soft) | A | Ramp width beyond the tolerance, percent. |
| `keyOperation` | enum `keyColors` / `keepColors` | `keyColors` | — | — | Key the matching colors out, or keep only them. |

Every instance also takes `expand` (number px or `"none"`); see 01-effects-basics.md.

### `matte.spill`

After Effects: Advanced Spill Suppressor / Spill Suppressor · Phase: P2 · Status: implemented · Tiling: tiled · Reads: — · Reads time: no · Device: GPU when the whole stack lowers, else CPU

On straight linear color, per pixel: `standard` limits the key color's primary channel to the larger of the other two by `suppression`; `ultra` limits it to the mean of the other two half-way (the spill range), only for hues within a quarter turn of the key, puts the removed spill back as neutral light (so brightness is kept) and desaturates what was suppressed.

| Parameter | Type | Default | Range | Anim | What it does |
|---|---|---|---|---|---|
| `method` | enum `standard` / `ultra` | `standard` | — | — | Simple limit, or hue-aware suppression with luma correction. |
| `keyColor` | color | `#00FF00` | — | A | The screen color whose spill is removed. |
| `suppression` | percent | 100 | 0–100 (soft) | A | How much of the spill is removed. |

Every instance also takes `expand` (number px or `"none"`); see 01-effects-basics.md.

### `matte.choker`

After Effects: Matte Choker · Phase: P2 · Status: implemented · Tiling: whole · Reads: — · Reads time: no · Device: CPU

`iterations` times two stages, each a Gaussian blur of the alpha by its geometric softness (σ = softness / 2) followed by a threshold ramp centered on 0.5 + choke / 255 · 0.5 (positive chokes) of width `grayLevelSoftness`; the straight color is kept under the new alpha.

| Parameter | Type | Default | Range | Anim | What it does |
|---|---|---|---|---|---|
| `geometricSoftness1` | length px | 4 | ≥ 0 (clamped) | A | Blur of the first stage, px. |
| `choke1` | number | 0 | -127–127 (clamped) | A | Threshold shift of the first stage (positive chokes). |
| `grayLevelSoftness1` | percent | 100 | 0–100 (soft) | A | Ramp width of the first stage. |
| `geometricSoftness2` | length px | 0 | ≥ 0 (clamped) | A | Blur of the second stage, px. |
| `choke2` | number | 0 | -127–127 (clamped) | A | Threshold shift of the second stage. |
| `grayLevelSoftness2` | percent | 100 | 0–100 (soft) | A | Ramp width of the second stage. |
| `iterations` | integer | 1 | 1–100 (clamped) | — | How many times the two stages run. |

Every instance also takes `expand` (number px or `"none"`); see 01-effects-basics.md.

### `matte.alphaLevels`

After Effects: — · Phase: P2 · Status: implemented · Tiling: tiled · Reads: — · Reads time: no · Device: GPU when the whole stack lowers, else CPU

Levels on alpha only (convenience): α′ = ((α − `inBlack`) / (`inWhite` − `inBlack`))^(1/γ), clamped; the straight color is kept.

| Parameter | Type | Default | Range | Anim | What it does |
|---|---|---|---|---|---|
| `inBlack` | number | 0 | 0–1 (clamped) | A | Alpha mapped to 0. |
| `inWhite` | number | 1 | 0–1 (clamped) | A | Alpha mapped to 1. |
| `gamma` | number | 1 | 0.1–10 (clamped) | A | Gamma of the alpha ramp. |

Every instance also takes `expand` (number px or `"none"`); see 01-effects-basics.md.

### `key.extract`

After Effects: Extract · Phase: P2 · Status: implemented · Tiling: tiled · Reads: — · Reads time: no · Device: CPU

Keys by a channel's range.

| Parameter | Type | Default | Range | Anim | What it does |
|---|---|---|---|---|---|
| `channel` | enum `luminance` / `red` / `green` / `blue` / `alpha` | `luminance` | — | — | The channel keyed by its range. |
| `blackPoint` | number | 0 | 0–255 (clamped) | A | Below this code value the pixel is keyed out. |
| `whitePoint` | number | 255 | 0–255 (clamped) | A | Above this code value the pixel is keyed out. |
| `blackSoftness` | number | 0 | 0–255 (clamped) | A | Fade-out width below the black point. |
| `whiteSoftness` | number | 0 | 0–255 (clamped) | A | Fade-out width above the white point. |
| `invert` | boolean | false | — | — | Keep the keyed range instead. |

Every instance also takes `expand` (number px or `"none"`); see 01-effects-basics.md.

### `key.colorRange`

After Effects: Color Range · Phase: P2 · Status: implemented · Tiling: tiled · Reads: — · Reads time: no · Device: CPU

Keys a box in the chosen colour space.

| Parameter | Type | Default | Range | Anim | What it does |
|---|---|---|---|---|---|
| `fuzziness` | number | 0 | 0–255 (clamped) | A | Width of the soft edge around the box. |
| `colorSpace` | enum `lab` / `yuv` / `rgb` | `lab` | — | — | The space the box lives in. |
| `min.l` | number | 0 | 0–255 (clamped) | A | Lower bound of L / Y / R. |
| `max.l` | number | 255 | 0–255 (clamped) | A | Upper bound of L / Y / R. |
| `min.a` | number | 0 | 0–255 (clamped) | A | Lower bound of a / U / G. |
| `max.a` | number | 100 | 0–255 (clamped) | A | Upper bound of a / U / G. |
| `min.b` | number | 128 | 0–255 (clamped) | A | Lower bound of b / V / B. |
| `max.b` | number | 255 | 0–255 (clamped) | A | Upper bound of b / V / B. |

Every instance also takes `expand` (number px or `"none"`); see 01-effects-basics.md.

### `key.colorDifference`

After Effects: Color Difference Key · Phase: P2 · Status: implemented · Tiling: tiled · Reads: — · Reads time: no · Device: CPU

Two partial mattes (A and B) combined, the classic blue-screen matte.

| Parameter | Type | Default | Range | Anim | What it does |
|---|---|---|---|---|---|
| `view` | enum `source` / `uncorrectedMatteA` / `correctedMatteA` / `uncorrectedMatteB` / `correctedMatteB` / `uncorrectedMatte` / `correctedMatte` / `finalOutput` / `abMatteCorrectedFinal` | `finalOutput` | — | — | What is shown. |
| `keyColor` | color | `#0000FF` | — | A | The screen colour. |
| `colorMatchingAccuracy` | enum `faster` / `moreAccurate` | `faster` | — | — | Encoded (faster) or linear values. |
| `partialA.inBlack` | number | 0 | 0–255 (clamped) | A | Partial A input black. |
| `partialA.inWhite` | number | 255 | 0–255 (clamped) | A | Partial A input white. |
| `partialA.gamma` | number | 1 | 0.01–10 (clamped) | A | Partial A gamma. |
| `partialA.outBlack` | number | 0 | 0–255 (clamped) | A | Partial A output black. |
| `partialA.outWhite` | number | 255 | 0–255 (clamped) | A | Partial A output white. |
| `partialB.inBlack` | number | 0 | 0–255 (clamped) | A | Partial B input black. |
| `partialB.inWhite` | number | 255 | 0–255 (clamped) | A | Partial B input white. |
| `partialB.gamma` | number | 1 | 0.01–10 (clamped) | A | Partial B gamma. |
| `partialB.outBlack` | number | 0 | 0–255 (clamped) | A | Partial B output black. |
| `partialB.outWhite` | number | 255 | 0–255 (clamped) | A | Partial B output white. |
| `matte.inBlack` | number | 0 | 0–255 (clamped) | A | Matte input black. |
| `matte.inWhite` | number | 255 | 0–255 (clamped) | A | Matte input white. |
| `matte.gamma` | number | 1 | 0.01–10 (clamped) | A | Matte gamma. |

Every instance also takes `expand` (number px or `"none"`); see 01-effects-basics.md.

### `key.screen`

After Effects: Screen Key · Phase: P2 · Status: implemented · Tiling: whole · Reads: — · Reads time: no · Device: CPU

Screen-difference keyer, the small sibling of `key.chroma`.

| Parameter | Type | Default | Range | Anim | What it does |
|---|---|---|---|---|---|
| `view` | enum `finalResult` / `screenMatte` / `status` / `source` | `finalResult` | — | — | The final result, the matte, the status view or the source. |
| `screenColor` | color | `#6CE189` | — | A | The screen colour. |
| `screenGain` | number | 100 | 0–200 (clamped) | A | Gain of the screen difference. |
| `screenBalance` | percent | 50 | 0–100 (soft) | A | Weight of the larger secondary channel. |
| `despill` | percent | 100 | 0–100 (soft) | A | How much of the screen spill is removed from the foreground. |
| `clipBlack` | percent | 0 | 0–100 (soft) | A | Matte values below this are 0. |
| `clipWhite` | percent | 100 | 0–100 (soft) | A | Matte values above this are 1. |
| `screenPreblur` | length px | 0 | ≥ 0 (clamped) | A | Blur of the layer before the matte is taken (px). |
| `screenShrinkGrow` | number | 0 | -50–50 (clamped) | A | Positive grows the matte, negative shrinks it (px). |
| `screenSoftness` | length px | 0 | ≥ 0 (clamped) | A | Gaussian softening of the matte (px). |
| `edgeColor` | enum `screenSubtract` / `source` | `screenSubtract` | — | — | Subtract the screen from the edges or keep the source. |

Every instance also takes `expand` (number px or `"none"`); see 01-effects-basics.md.

### `key.ccWireRemoval`

After Effects: CC Simple Wire Removal · Phase: P2 · Status: implemented · Tiling: tiled · Reads: — · Reads time: no · Device: CPU

Paints out the line between the two points; `frameOffset` reads another frame (`Deps::times`).

| Parameter | Type | Default | Range | Anim | What it does |
|---|---|---|---|---|---|
| `pointA` | point `[x, y]` | `["25%", "25%"]` | — | A | One end of the wire. |
| `pointB` | point `[x, y]` | `["75%", "75%"]` | — | A | The other end. |
| `removalStyle` | enum `fade` / `frameOffset` / `displace` / `displaceHorizontal` | `displace` | — | — | How the wire is painted out. |
| `thickness` | length px | 5 | ≥ 0 (clamped) | A | Wire thickness in px. |
| `slope` | percent | 0 | 0–100 (soft) | A | Soft edge, percent of the thickness. |
| `mirrorBlend` | percent | 0 | 0–100 (soft) | A | Mix of the far side. |
| `frameOffset` | integer | 0 | -100–100 (clamped) | A | Frames away for `frameOffset`. |

Every instance also takes `expand` (number px or `"none"`); see 01-effects-basics.md.

### `matte.keyCleaner`

After Effects: Key Cleaner · Phase: P2 · Status: implemented · Tiling: whole · Reads: — · Reads time: no · Device: CPU

Recovers edge detail after a keyer; `reduceChatter` reads neighbouring frames (`Deps::times`).

| Parameter | Type | Default | Range | Anim | What it does |
|---|---|---|---|---|---|
| `additionalEdgeRadius` | length px | 3 | ≥ 0 (clamped) | A | Edge band width for the color recovery (px). |
| `reduceChatter` | boolean | false | — | — | Average with the neighbouring frames where they agree. |
| `alphaContrast` | percent | 100 | 100–500 (soft) | A | Contrast of the matte. |
| `strength` | percent | 100 | 0–100 (soft) | A | How much the edge colors are recovered. |

Every instance also takes `expand` (number px or `"none"`); see 01-effects-basics.md.

### `matte.refineHard`

After Effects: Refine Hard Matte · Phase: P2 · Status: implemented · Tiling: whole · Reads: — · Reads time: no · Device: CPU

The hard-edged sibling of `matte.refine`; `reduceChatter` and `useMotionBlur` read neighbouring frames (`Deps::times`).

| Parameter | Type | Default | Range | Anim | What it does |
|---|---|---|---|---|---|
| `smooth` | percent | 20 | 0–100 (soft) | A | Smoothing of the edge band. |
| `feather` | percent | 0 | 0–100 (soft) | A | Feather of the matte, percent of the radius. |
| `choke` | number | 0 | -100–100 (clamped) | A | Shrinks (positive) or grows the matte. |
| `reduceChatter` | percent | 0 | 0–100 (soft) | A | Average with the neighbouring frames where they agree. |
| `useMotionBlur` | boolean | false | — | — | Average the matte over the shutter. |
| `motionBlur.samples` | integer | 16 | 1–64 (clamped) | — | Shutter samples. |
| `motionBlur.shutterAngle` | number | 180 | 0–720 (clamped) | A | Shutter angle in degrees. |
| `motionBlur.higherQuality` | boolean | false | — | — | Twice the samples. |
| `decontaminate` | boolean | true | — | — | Pull edge colors toward their surroundings. |
| `decontamination.amount` | percent | 100 | 0–100 (soft) | A | How far the edge colors move. |
| `decontamination.extendWhereSmoothed` | boolean | true | — | — | Also where the refinement made the matte partial. |
| `decontamination.increaseRadius` | length px | 0 | ≥ 0 (clamped) | A | More decontamination radius (px). |
| `decontamination.viewMap` | boolean | false | — | — | Show the decontamination strength instead. |
| `radius` | length px | 3 | ≥ 0 (clamped) | A | Edge band width (px). |
| `alphaContrast` | percent | 300 | 100–1000 (soft) | A | Contrast of the matte. |
| `invert` | boolean | false | — | — | Invert the matte. |

Every instance also takes `expand` (number px or `"none"`); see 01-effects-basics.md.

### `key.innerOuter`

After Effects: Inner/Outer Key · Phase: P2 · Status: implemented · Tiling: whole · Reads: mask paths · Reads time: no · Device: CPU

Matte from an inner and an outer mask with colour-based edge estimation and decontamination; needs mask paths as parameters, like `generate.stroke`.

| Parameter | Type | Default | Range | Anim | What it does |
|---|---|---|---|---|---|
| `foreground` | mask id | none | — | — | Mask id of the inner outline: inside it the layer is kept. |
| `background` | mask id | none | — | — | Mask id of the outer outline: outside it the layer is dropped. |
| `additionalForeground` | list of mask ids | `[]` | — | — | Up to 10 more inner mask ids. |
| `additionalBackground` | list of mask ids | `[]` | — | — | Up to 10 more outer mask ids. |
| `singleMaskHighlightRadius` | length px | 0 | ≥ 0 (clamped) | A | With inner outlines only: the width of the estimated band on either side of them (px). |
| `cleanupForeground` | list of `{ path: mask id, brushRadius: length (10), brushPressure: percent (80) }` | `[]` | — | A | Up to 10 brush strokes along mask paths that paint the matte opaque. |
| `cleanupBackground` | list of `{ path: mask id, brushRadius: length (10), brushPressure: percent (80) }` | `[]` | — | A | Up to 10 brush strokes along mask paths that paint the matte transparent. |
| `edgeThin` | number | 0 | -10–10 (clamped) | A | Shrinks (positive) or grows (negative) the matte (px). |
| `edgeFeather` | length px | 0 | ≥ 0 (clamped) | A | Softens the matte edge (px). |
| `edgeThreshold` | percent | 0 | 0–100 (soft) | A | Matte values below this become transparent. |
| `invertExtraction` | boolean | false | — | — | Inverts the matte. |
| `blendWithOriginal` | percent | 0 | 0–100 (soft) | A | Mixes the original layer back in. |

Every instance also takes `expand` (number px or `"none"`); see 01-effects-basics.md.

<!-- gen:catalogue-keying-1:end -->
