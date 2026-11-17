# Color: every parameter (part 2 of 2)

Generated from `rexx-engine effects` by scripts/skills-effects-catalogue.py; do not edit by hand. Index: [90-catalogue.md](90-catalogue.md).

<!-- gen:catalogue-color-2:start -->
### `color.shadowHighlight`

After Effects: Shadow/Highlight · Phase: P2 · Status: implemented · Tiling: whole · Reads: — · Reads time: no · Device: CPU

`temporalSmoothing` > 0 reads neighbouring frames (`Deps::times`); `autoAmounts` analyses the current frame only.

| Parameter | Type | Default | Range | Anim | What it does |
|---|---|---|---|---|---|
| `autoAmounts` | boolean | true | — | — | Derive the amounts from the frame's mean luma. |
| `shadowAmount` | percent | 50 | 0–100 (soft) | A | How much the shadows are lifted. |
| `highlightAmount` | percent | 0 | 0–100 (soft) | A | How much the highlights are lowered. |
| `temporalSmoothing` | number | 0 | 0–4 (clamped) | A | Seconds of neighbouring frames the auto analysis averages. |
| `sceneDetect` | boolean | false | — | — | Skip neighbouring frames across a cut. |
| `moreOptions.shadowTonalWidth` | percent | 50 | 0–100 (soft) | A | How far the shadows reach up. |
| `moreOptions.shadowRadius` | length px | 30 | ≥ 0 (clamped) | A | Neighbourhood of the shadow weight (px). |
| `moreOptions.highlightTonalWidth` | percent | 50 | 0–100 (soft) | A | How far the highlights reach down. |
| `moreOptions.highlightRadius` | length px | 30 | ≥ 0 (clamped) | A | Neighbourhood of the highlight weight (px). |
| `moreOptions.colorCorrection` | number | 20 | -100–100 (clamped) | A | Saturation follows the gain. |
| `moreOptions.midtoneContrast` | number | 0 | -100–100 (clamped) | A | Contrast of the midtones. |
| `moreOptions.blackClip` | number | 0.01 | 0–49 (clamped) | A | Percent of pixels clipped at black. |
| `moreOptions.whiteClip` | number | 0.01 | 0–49 (clamped) | A | Percent of pixels clipped at white. |
| `blendWithOriginal` | percent | 0 | 0–100 (soft) | A | Mix back toward the layer. |

Every instance also takes `expand` (number px or `"none"`); see 01-effects-basics.md.

### `color.videoLimiter`

After Effects: Video Limiter · Phase: P2 · Status: implemented · Tiling: tiled · Reads: — · Reads time: no · Device: CPU

Copied from EffectCraft `ec.color.videolimiter`; params as EffectCraft.

| Parameter | Type | Default | Range | Anim | What it does |
|---|---|---|---|---|---|
| `clipLevel` | enum `90` / `95` / `100` / `105` / `109` | `100` | — | — | The level (percent of white) values are limited to. |
| `clipMethod` | enum `luma` / `chroma` / `smartLimit` | `smartLimit` | — | — | What is limited: the luma, the chroma, or both. |
| `compressionBeforeClipping` | enum `none` / `3` / `5` / `10` / `20` | `5` | — | — | Percent below the level the knee starts. |
| `gamutWarning` | boolean | false | — | — | Paint the limited pixels. |
| `gamutWarningColor` | color | `#FF0000` | — | A | The warning color. |

Every instance also takes `expand` (number px or `"none"`); see 01-effects-basics.md.

### `color.autoContrast`

After Effects: Auto Contrast / Auto Levels / Auto Color / Color Stabilizer · Phase: — · Status: not implemented (not provided: `effect.unavailable`)

Not provided: analysis-based auto adjustments (with temporal smoothing, or a reference frame) differ by frame and break determinism across chunks.

No parameters are registered: the engine answers `effect.unavailable` (the message names the phase).

<!-- gen:catalogue-color-2:end -->
