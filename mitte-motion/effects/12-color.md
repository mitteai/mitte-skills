# Color

34 ids. Parameters: [91-catalogue-color-1.md](91-catalogue-color-1.md), [91-catalogue-color-2.md](91-catalogue-color-2.md). All run per pixel. Rows that take 0–1 or 0–255 inputs work on **display-encoded** values (what a colorist expects); `color.exposure`, `color.whiteBalance`, `color.lut` with a linear `inputSpace` and `color.grade`'s exposure work in **linear light**.

| Effect | Use it for | Neutral |
|---|---|---|
| `color.levels` | Levels: `channel` rgb/red/green/blue/alpha with `inBlack`/`inWhite`/`gamma`/`outBlack`/`outWhite` (0–1 encoded), `clipBlack`/`clipWhite` (false keeps HDR), per-channel groups `red`/`green`/`blue`/`alpha` with the same five fields. | defaults |
| `color.curves` | Curves: `rgb`, `red`, `green`, `blue`, `alpha` as `[[x, y], …]` (monotone cubic; linear past 1 so HDR is kept), `space` display/linear. | identity curves |
| `color.hueSaturation` | `hue` °, `saturation` −100…100, `lightness`, `colorize` + `colorizeHue`/`colorizeSaturation`, `range` master/reds/yellows/greens/cyans/blues/magentas, `space` `oklch` (keeps perceived lightness) or `hsl` (After Effects exact). | all 0 |
| `color.exposure` | Linear-light gain: `exposure` stops, `offset`, `gamma`; `channels` master/individual with per-channel triples. | 0 / 0 / 1 |
| `color.brightnessContrast` | `brightness` −150…150, `contrast` −100…100, `legacy`. | 0 / 0 |
| `color.vibrance` | `vibrance` (saturates the unsaturated, protects skin hues), `saturation`. | 0 / 0 |
| `color.balance` | `shadows`/`midtones`/`highlights` `[r, g, b]` −100…100, `preserveLuminosity`. | all 0 |
| `color.tint` | Luminance → `black`…`white` colours, `amount`. | `amount: 0` |
| `color.tritone` | `highlights`/`midtones`/`shadows` colours, `amount`. | `amount: 0` |
| `color.gradientMap` | Luminance (or `input` red/green/blue/alpha/hue/saturation) → `gradient`; `phase`, `cycles` (animated colour cycling), `amount`, `modifyAlpha`. | `amount: 0` |
| `color.lut` | A `.cube` LUT asset (`lut`), `amount`, `inputSpace` display/linear/logC/slog3/acescct, `interpolation` tetrahedral/trilinear. `utility.applyLut` is the same effect under its After Effects name. | `amount: 0` |
| `color.invert` | `channel` rgb/red/green/blue/alpha/luminance/hue, `amount`. | `amount: 0` |
| `color.channelMixer` | 12 numbers `rr rg rb rc gr gg gb gc br bg bb bc` (percent; `rc` is the constant), `monochrome`. | identity |
| `color.posterize` | `levels` 2–255, `dither`. | — |
| `color.threshold` | `level` 0–1, `softness` 0–1. | — |
| `color.blackWhite` | Six hue weights `reds`…`magentas` −200…300, `tint` colour or null. | — |
| `color.selective` | Selective Color: per range (`reds`…`blacks`) `[c, m, y, k]`, `method` relative/absolute. | all 0 |
| `color.whiteBalance` | `temperature` (+ warms), `tint` (+ magenta), or `neutral` colour that should be grey; Bradford adaptation in linear light. | 0 / 0, no `neutral` |
| `color.grade` | Lumetri in one effect: `exposure`, `contrast`, `highlights`, `shadows`, `whites`, `blacks`, `temperature`, `tint`, `saturation`, `vibrance`, `fadedFilm`, `sharpen`, wheels `lift`/`gamma`/`gain`/`offset` `[r, g, b]`, `lut` + `lutAmount`, `vignette.amount`/`midpoint`/`roundness`/`feather`. Runs as the ordered chain of the single effects. | all at rest |
| `color.changeColor` | Recolour one colour without a mask: `from`, `to` (or `hueShift`/`lightnessShift`/`saturationShift`), `tolerance`, `softness`, `match` rgb/hue/chroma. | no `to`, no shifts |
| `color.leaveColor` | Keep one colour, desaturate the rest: `keep`, `amount`, `tolerance`, `softness`. | `amount: 0` |
| `color.broadcastColors` | Legalizer: `locale` ntsc/pal, `howToMakeSafe`, `maxSignal` IRE 90–120. | — |
| `color.ccColorNeutralizer` | Per-range cast removal: `shadowsUnbalance`→`shadowsBalance`, midtones, highlights; `pinning`, `blendWithOriginal`, `darks`, `brights`, `contrast`. | balanced = unbalanced |
| `color.ccColorOffset` | Per-channel phase `redPhase`/`greenPhase`/`bluePhase`, `overflow` wrap/solarize/polarize. | all 0 |
| `color.ccKernel` | A 3×3 convolution `k1`…`k9` / `scale` + `offset`, `absolute`. | k5 = 1 |
| `color.ccToner` | Up to five tone stops (`tones` duotone/tritone/pentone): `highlights`, `brights`, `midtones`, `darktones`, `shadows`, `blendWithOriginal`. | — |
| `color.colorLink` | Fill the layer with one colour sampled from `sourceLayer` (`sample` average/median/brightest/… , `clip`, `stencilOriginalAlpha`, `opacity`, `blendingMode`). | `opacity: 0` |
| `color.equalize` | Histogram equalization of the frame: `style` rgb/brightness/photoshop, `amount`. | `amount: 0` |
| `color.gammaPedestalGain` | `blackStretch` and per channel `red`/`green`/`blue` `gamma`/`pedestal`/`gain`. | defaults |
| `color.arbitraryMap` | A Photoshop `.amp` map (`map`: a 1-D LUT asset or 256 values), `phase`, `applyPhaseMapToAlpha`. | no map |
| `color.photoFilter` | `filter` (20 presets or `custom`), `color`, `density`, `preserveLuminosity`. | `density: 0` |
| `color.shadowHighlight` | `autoAmounts`, `shadowAmount`, `highlightAmount`, `temporalSmoothing` s (reads neighbouring frames), `sceneDetect`, `moreOptions.*`, `blendWithOriginal`. | — |
| `color.videoLimiter` | `clipLevel`, `clipMethod`, `compressionBeforeClipping`, `gamutWarning` + colour. | — |
| `color.autoContrast` | Not provided (frame-dependent analysis breaks determinism): `effect.unavailable`. Use `color.levels` with numbers from `motion.check`'s analysis. | — |

Device: `color.levels`, `curves`, `hueSaturation`, `exposure`, `brightnessContrast`, `tint`, `tritone`, `gradientMap`, `lut`, `invert`, `selective`, `vibrance`, `balance`, `channelMixer`, `posterize`, `threshold`, `blackWhite`, `whiteBalance`, `changeColor`, `leaveColor` lower to the device as pointwise maps; the rest are CPU.

## Patterns

**A grade on everything.** One `color.grade` on an adjustment layer at the top: `exposure` 0.2, `contrast` 10, `temperature` 8, `saturation` 110, `vignette: { "amount": 0.3 }`. Keep it one effect; its order matches Lumetri.

**Brand duotone.** `color.gradientMap` with a two-stop gradient and `amount` keyed for a reveal; `interpolation: "oklab"` (default) keeps midtones clean:

```json
{ "id": "duo", "type": "color.gradientMap",
  "params": { "gradient": { "stops": [[0, "#1B1F3B"], [1, "#FFB347"]] }, "amount": { "keys": [ { "t": 0, "v": 0 }, { "t": 1, "v": 100 } ] } } }
```

**Per-channel Levels.** `"red": { "gamma": 1.2 }` beside the top-level numbers; a channel field absent falls back to the top-level value.

**LUT.** Declare the asset (`"assets": { "look": { "src": "https://…/film.cube", "type": "lut" } }`) and reference it: `{ "type": "color.lut", "params": { "lut": "look", "amount": 80 } }`. A LUT that cannot be loaded is `effect.missing_input` and the effect is skipped.

**Thermal / colour-cycle looks.** `color.gradientMap` with `cycles` 2 and `phase` keyed 0 → 100.

**Change a product colour.** `color.changeColor` `from: "#D7263D"`, `to: "#2E86AB"`, `tolerance` 20, `softness` 15, `match: "hue"`.

Full example: `examples/color-family.motion.json`.
