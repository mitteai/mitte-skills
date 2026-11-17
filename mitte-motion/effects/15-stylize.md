# Stylize

44 ids. Parameters: [91-catalogue-stylize-1.md](91-catalogue-stylize-1.md), [91-catalogue-stylize-2.md](91-catalogue-stylize-2.md). The shadows, outlines, glitch, halftone, dither, grain, noise and print looks.

| Effect | Use it for | Neutral |
|---|---|---|
| `stylize.dropShadow` | In layer space (rotates with the layer): `color`, `opacity`, `direction` (135 = down-right), `distance`, `softness` (true Gaussian), `spread` percent, `shadowOnly`. For a comp-space shadow use the layer style. | `opacity: 0` |
| `stylize.longShadow` | Flat-design long shadow: exact sweep of the alpha along `direction` for `length` px, `color`, `opacity`, `fade`, `softness`. | `opacity: 0` |
| `stylize.outline` | Distance-field stroke on the alpha: `width`, `color`, `position` outside/center/inside, `softness`, `outlineOnly`. | `width: 0` |
| `stylize.roughenEdges` | Torn / printed edges: `edgeType` roughen/roughenColor/cut/spiky/rustyColor/rusty/photocopierColor/photocopier, `edgeColor`, `border`, `edgeSharpness`, `fractalInfluence`, `scale`, `stretchWidth`, `offset`, `complexity`, `evolution`, `cycleEvolution`, `randomSeed`. | `border: 0` |
| `stylize.grain` | Film grain: `amount`, `size`, `softness`, `color` mono/color, `channelIntensity`, `response` curve, `animated`, `rate` fps (12 for on-twos), `preset` none/kodak5207/kodak5219/fuji3510/ilford/16mm/8mm, `blendMode` overlay/softLight/add. | `amount: 0` |
| `stylize.noise` | Per-pixel noise: `amount`, `type` uniform/gaussian, `color`, `clip`, `seed`; a new pattern every frame. | `amount: 0` |
| `stylize.vignette` | Lumetri-style, linear light: `amount` −1…1 (negative darkens), `midpoint`, `roundness`, `feather`, `center`. | `amount: 0` |
| `stylize.ccVignette` | Lens-model: `amount`, `angleOfView`, `center`, `pinHighlights`. | `amount: 0` |
| `stylize.letterbox` | Bars outside the centred `aspect` (2.39), `color`; on an adjustment layer the rect is the comp. | `aspect: 0` |
| `stylize.mosaic` | `horizontalBlocks`/`verticalBlocks`, `sharpColors`. | — |
| `stylize.pixelate` | Cells of `size` px as `shape` square/hexagon/circle/diamond with `gap` and `gapColor`. | — |
| `stylize.scatter` | Hashed offsets up to `amount` px, `grain` both/horizontal/vertical, `randomize` per frame, `seed`. | `amount: 0` |
| `stylize.halftone` | Analytic print dots: `source` luminance/alpha, `mode` mono/cmyk/rgb/duotone, `cellSize`, `angles [c, m, y, k]`, `shape` dot/line/square/diamond/euclidean, `paper`, `ink`, `secondInk`, `softness`, `misregistration`, `blend`. | `blend: 0` |
| `stylize.dither` | `method` bayer2/bayer4/bayer8/blueNoise/floydSteinberg/atkinson/stucki, `palette` (list of colours or `1bit`/`gameboy`/`cga`/`mac`/`grayscale4`/`grayscale8`), `pixelSize`, `contrast`, `brightness`, `matchSpace` oklab/srgb. | — |
| `stylize.posterizeEdges` | `levels`, `edgeWidth`, `edgeColor`. | — |
| `stylize.glitch` | Seeded glitch events: `amount`, `blockSize [w, h]`, `blockShift`, `channelShift`, `frequency` events/s, `duration`, `slices`, `colorBlocks`, `pixelate`, `seed`. A function of (seed, time): key `amount` to a beat. | `amount: 0` |
| `stylize.rgbSplit` | Per-channel offsets `red`/`green`/`blue` points, `mode` add/screen. | all `[0, 0]` |
| `stylize.chromatic` | Lens aberration: `amount`, `center`, `mode` radial/directional, `direction`, `falloff`, `channels` rgb/rb. | `amount: 0` |
| `stylize.scanlines` | CRT: `density`, `thickness`, `opacity`, `curvature`, `mask` none/aperture/shadow/slot, `flicker`, `bloom`, `roll`, `seed`. | `opacity: 0`, no mask/curvature/bloom/flicker |
| `stylize.vhs` | `amount`, `tracking`, `chromaBleed`, `noise`, `wobble`, `colorShift`, `seed`. | `amount: 0` |
| `stylize.pixelSort` | Sort runs along `direction` whose key (`sortBy`) lies in `threshold [lo, hi]`, `order`, `maxLength`, optional `mask` layer. | `lo ≥ hi` |
| `stylize.findEdges` | Sobel edges dark on white (`invert`), mixed by `blend`. | `blend: 100` |
| `stylize.glowEdges` | Glowing edges: `width`, `brightness`, `contrast`. | — |
| `stylize.emboss` | `direction`, `relief`, `contrast`, `blend`, `color` (Color Emboss). | `blend: 100` |
| `stylize.cartoon` | `render` fill/edges/fillAndEdges, `detailRadius`, `detailThreshold`, `fillShadingSteps`, `fillShadingSmoothness`, `edgeThreshold`, `edgeWidth`, `edgeSoftness`, `edgeOpacity`. | — |
| `stylize.brushStrokes` | One capsule stroke per cell (cells 2 × `size`), in the layer's average colour along it: `angle`, `size`, `length`, `density`, `randomness`, `surface`, `blend`, `seed`. | `blend: 100` |
| `stylize.texturize` | Paper/canvas from a `texture` layer: `light`, `contrast`, `placement` tile/center/stretch. | — |
| `stylize.ascii` | Text-art: `cellSize`, `charset`, `font` (`mono` only), `color` source/mono, `foreground`/`background`. | — |
| `stylize.ccBlockLoad` | `completion`, `scanlines`, `smoothing`, `startCleared`, `bilinear`. | `completion: 0` |
| `stylize.ccBurnFilm` | `burn` percent from `center`, `seed`. | `burn: 0` |
| `stylize.ccGlass` | Bump-mapped glass from `bumpMap`'s `property`: `softness`, `height`, `displacement`, `light.*`, `shading.*`. | — |
| `stylize.ccPlastic` | As `ccGlass` with `cutMin`/`cutMax`. | — |
| `stylize.ccHexTile` | `render` normal/mirrored/rotated, `radius`, `center`, `rotate`, `smearing`. | — |
| `stylize.ccMrSmoothie` | Recolour by a map sampled between `sampleA` and `sampleB`, indexed by `flowLayer`'s `property`; `smoothness`, `phase`, `colorLoop`. | — |
| `stylize.ccRepeTile` | Grow the layer by tiling: `expandRight`/`Left`/`Down`/`Up`, `tiling` repeat/unfold/checkerFlipH/checkerFlipV/checkerFlip. | all 0 |
| `stylize.ccThresholdRgb` | Per-channel thresholds, inverts, `blendWithOriginal`. | — |
| `stylize.median` | Median of `radius` ≤ 255, `operateOnAlpha`. | `radius: 0` |
| `stylize.dustScratches` | `radius`, `threshold`, `operateOnAlpha`. | `radius: 0` |
| `stylize.noiseAlpha` | Noise on alpha: `noise` kind, `amount`, `originalAlpha`, `overflow`, `seed`, `noisePhase`, `noiseOptions.*`. | `amount: 0` |
| `stylize.noiseHls` / `stylize.noiseHlsAuto` | HLS noise: `noise`, `hue`, `lightness`, `saturation`, `grainSize`, `noisePhase` (or `noiseAnimationSpeed`). | all 0 |
| `stylize.removeGrain` | `noiseReduction.*`, `fineTuning.*`, `unsharpMask.*`, `temporalFiltering.*` (reads neighbouring frames), `sampling.*`, `preview.*`. | `amount: 0` |
| `stylize.datamosh` | Not implemented (P4): `effect.unavailable`. | — |
| `stylize.motionTrails` | Not provided: use `time.echo`. | — |

Device: `stylize.grain`, `stylize.vignette`, `stylize.noise`, `stylize.letterbox` lower to the device.

## Patterns

**Film finish.** On an adjustment layer at the top: `stylize.grain` (`preset: "kodak5219"`, `amount` 25, `rate` 24) then `stylize.vignette` (`amount` −0.35, `feather` 60). Both are pointwise and cheap.

**Glitch on the beat.** `stylize.glitch` with `amount` keyed from 0 to 80 for 0.15 s at each marker (`"t": "@beat*"` keys are not a thing; use the marker times), `blockSize` `[120, 10]`, `channelShift` 12, `colorBlocks: true`; add `stylize.rgbSplit` with `red: [-6, 0]`, `blue: [6, 0]` under it for a constant split.

**Halftone poster.** `stylize.halftone` `mode: "duotone"`, `cellSize` 9, `ink: "#1B1F3B"`, `secondInk: "#D7263D"`, `paper: "#F4F1EA"`, `shape: "dot"`; keep it last so the dots are not blurred.

**1-bit / Game Boy.** `stylize.dither` `method: "bayer4"`, `palette: "gameboy"`, `pixelSize` 3.

**Sticker outline.** `stylize.outline` `width` 8, `color` white, `position: "outside"`; then `stylize.dropShadow` `distance` 6, `softness` 10.

**Torn paper boil.** `stylize.roughenEdges` `edgeType: "roughen"`, `border` 12, `scale` 60, `evolution` keyed with a `steps(n)` ease (held values, on twos) for the hand-made look.

Full example: `examples/stylize-family.motion.json`.
