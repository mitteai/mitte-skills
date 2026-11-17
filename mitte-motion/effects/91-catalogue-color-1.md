# Color: every parameter (part 1 of 2)

Generated from `rexx-engine effects` by scripts/skills-effects-catalogue.py; do not edit by hand. Index: [90-catalogue.md](90-catalogue.md).

<!-- gen:catalogue-color-1:start -->
### `color.levels`

After Effects: Levels / Levels (Individual Controls) · Phase: P1 · Status: implemented · Tiling: tiled · Reads: — · Reads time: no · Device: GPU when the whole stack lowers, else CPU

Values 0–1 in display encoding (After Effects 32 bpc Levels uses 0–1).

| Parameter | Type | Default | Range | Anim | What it does |
|---|---|---|---|---|---|
| `channel` | enum `rgb` / `red` / `green` / `blue` / `alpha` | `rgb` | — | — | Which channel the top-level numbers adjust. |
| `inBlack` | number | 0 | — | A | Input black (encoded 0–1). |
| `inWhite` | number | 1 | — | A | Input white (encoded 0–1). |
| `gamma` | number | 1 | 0.1–10 (clamped) | A | Input gamma. |
| `outBlack` | number | 0 | — | A | Output black. |
| `outWhite` | number | 1 | — | A | Output white. |
| `clipBlack` | boolean | true | — | — | Clamp inputs below `inBlack` to the output black. |
| `clipWhite` | boolean | true | — | — | Clamp inputs above `inWhite` to the output white (false keeps HDR values). |
| `red.inBlack` | number | 0 | — | A | Per-channel input black. |
| `red.inWhite` | number | 1 | — | A | Per-channel input white. |
| `red.gamma` | number | 1 | 0.1–10 (clamped) | A | Per-channel gamma. |
| `red.outBlack` | number | 0 | — | A | Per-channel output black. |
| `red.outWhite` | number | 1 | — | A | Per-channel output white |
| `green.inBlack` | number | 0 | — | A | Per-channel input black. |
| `green.inWhite` | number | 1 | — | A | Per-channel input white. |
| `green.gamma` | number | 1 | 0.1–10 (clamped) | A | Per-channel gamma. |
| `green.outBlack` | number | 0 | — | A | Per-channel output black. |
| `green.outWhite` | number | 1 | — | A | Per-channel output white |
| `blue.inBlack` | number | 0 | — | A | Per-channel input black. |
| `blue.inWhite` | number | 1 | — | A | Per-channel input white. |
| `blue.gamma` | number | 1 | 0.1–10 (clamped) | A | Per-channel gamma. |
| `blue.outBlack` | number | 0 | — | A | Per-channel output black. |
| `blue.outWhite` | number | 1 | — | A | Per-channel output white |
| `alpha.inBlack` | number | 0 | — | A | Per-channel input black. |
| `alpha.inWhite` | number | 1 | — | A | Per-channel input white. |
| `alpha.gamma` | number | 1 | 0.1–10 (clamped) | A | Per-channel gamma. |
| `alpha.outBlack` | number | 0 | — | A | Per-channel output black. |
| `alpha.outWhite` | number | 1 | — | A | Per-channel output white |

Every instance also takes `expand` (number px or `"none"`); see 01-effects-basics.md.

### `color.curves`

After Effects: Curves · Phase: P1 · Status: implemented · Tiling: tiled · Reads: — · Reads time: no · Device: GPU when the whole stack lowers, else CPU

Monotone cubic (Fritsch–Carlson) through points; endpoints extrapolate linearly above 1 so HDR values are not clipped.

| Parameter | Type | Default | Range | Anim | What it does |
|---|---|---|---|---|---|
| `rgb` | curve `[[x, y], …]` | `[[0, 0], [1, 1]]` | — | A | Master curve applied to all three channels. |
| `red` | curve `[[x, y], …]` | `[[0, 0], [1, 1]]` | — | A | Red curve. |
| `green` | curve `[[x, y], …]` | `[[0, 0], [1, 1]]` | — | A | Green curve. |
| `blue` | curve `[[x, y], …]` | `[[0, 0], [1, 1]]` | — | A | Blue curve. |
| `alpha` | curve `[[x, y], …]` | `[[0, 0], [1, 1]]` | — | A | Alpha curve (on straight alpha). |
| `space` | enum `display` / `linear` | `display` | — | — | Whether the curves see encoded or linear values. |

Every instance also takes `expand` (number px or `"none"`); see 01-effects-basics.md.

### `color.hueSaturation`

After Effects: Hue/Saturation / Color Balance (HLS) · Phase: P1 · Status: implemented · Tiling: tiled · Reads: — · Reads time: no · Device: GPU when the whole stack lowers, else CPU

Hue rotation in OKLCh by default (`space: "oklch"`), so a hue shift keeps perceived lightness; `space: "hsl"` reproduces After Effects exactly.

| Parameter | Type | Default | Range | Anim | What it does |
|---|---|---|---|---|---|
| `hue` | angle ° | 0 | — | A | Hue rotation in degrees. |
| `saturation` | number | 0 | -100–100 (clamped) | A | Saturation change. |
| `lightness` | number | 0 | -100–100 (clamped) | A | Lightness change. |
| `colorize` | boolean | false | — | — | Replace every hue with `colorizeHue` at `colorizeSaturation`. |
| `colorizeHue` | angle ° | 0 | — | A | Colorize hue. |
| `colorizeSaturation` | percent | 25 | 0–100 (soft) | A | Colorize saturation. |
| `range` | enum `master` / `reds` / `yellows` / `greens` / `cyans` / `blues` / `magentas` | `master` | — | — | Which hue range the top-level numbers adjust. |
| `space` | enum `oklch` / `hsl` | `oklch` | — | — | OKLCh (lightness-preserving) or After Effects' HSL. |
| `reds.hue` | angle ° | 0 | — | A | Per-range hue rotation. |
| `reds.saturation` | number | 0 | -100–100 (clamped) | A | Per-range saturation change. |
| `reds.lightness` | number | 0 | -100–100 (clamped) | A | Per-range lightness change. |
| `yellows.hue` | angle ° | 0 | — | A | Per-range hue rotation. |
| `yellows.saturation` | number | 0 | -100–100 (clamped) | A | Per-range saturation change. |
| `yellows.lightness` | number | 0 | -100–100 (clamped) | A | Per-range lightness change. |
| `greens.hue` | angle ° | 0 | — | A | Per-range hue rotation. |
| `greens.saturation` | number | 0 | -100–100 (clamped) | A | Per-range saturation change. |
| `greens.lightness` | number | 0 | -100–100 (clamped) | A | Per-range lightness change. |
| `cyans.hue` | angle ° | 0 | — | A | Per-range hue rotation. |
| `cyans.saturation` | number | 0 | -100–100 (clamped) | A | Per-range saturation change. |
| `cyans.lightness` | number | 0 | -100–100 (clamped) | A | Per-range lightness change. |
| `blues.hue` | angle ° | 0 | — | A | Per-range hue rotation. |
| `blues.saturation` | number | 0 | -100–100 (clamped) | A | Per-range saturation change. |
| `blues.lightness` | number | 0 | -100–100 (clamped) | A | Per-range lightness change. |
| `magentas.hue` | angle ° | 0 | — | A | Per-range hue rotation. |
| `magentas.saturation` | number | 0 | -100–100 (clamped) | A | Per-range saturation change. |
| `magentas.lightness` | number | 0 | -100–100 (clamped) | A | Per-range lightness change. |

Every instance also takes `expand` (number px or `"none"`); see 01-effects-basics.md.

### `color.exposure`

After Effects: Exposure · Phase: P1 · Status: implemented · Tiling: tiled · Reads: — · Reads time: no · Device: GPU when the whole stack lowers, else CPU

Linear-light multiply by 2^exposure (the correct way to brighten HDR content).

| Parameter | Type | Default | Range | Anim | What it does |
|---|---|---|---|---|---|
| `exposure` | number | 0 | — | A | Stops. |
| `offset` | number | 0 | — | A | Linear offset added after the exposure multiply. |
| `gamma` | number | 1 | 0.1–10 (clamped) | A | Gamma correction (`v^(1/gamma)`). |
| `channels` | enum `master` / `individual` | `master` | — | — | Master numbers or the per-channel triples. |
| `red.exposure` | number | 0 | — | A | Red stops (individual). |
| `red.offset` | number | 0 | — | A | Red offset (individual). |
| `red.gamma` | number | 1 | 0.1–10 (clamped) | A | Red gamma (individual). |
| `green.exposure` | number | 0 | — | A | Green stops (individual). |
| `green.offset` | number | 0 | — | A | Green offset (individual). |
| `green.gamma` | number | 1 | 0.1–10 (clamped) | A | Green gamma (individual). |
| `blue.exposure` | number | 0 | — | A | Blue stops (individual). |
| `blue.offset` | number | 0 | — | A | Blue offset (individual). |
| `blue.gamma` | number | 1 | 0.1–10 (clamped) | A | Blue gamma (individual). |

Every instance also takes `expand` (number px or `"none"`); see 01-effects-basics.md.

### `color.brightnessContrast`

After Effects: Brightness & Contrast · Phase: P1 · Status: implemented · Tiling: tiled · Reads: — · Reads time: no · Device: GPU when the whole stack lowers, else CPU

Non-legacy: contrast pivots around 0.5 display-encoded (After Effects/Photoshop modern behavior).

| Parameter | Type | Default | Range | Anim | What it does |
|---|---|---|---|---|---|
| `brightness` | number | 0 | -150–150 (clamped) | A | Brightness. |
| `contrast` | number | 0 | -100–100 (clamped) | A | Contrast. |
| `legacy` | boolean | false | — | — | After Effects' legacy (linear offset) formulas. |

Every instance also takes `expand` (number px or `"none"`); see 01-effects-basics.md.

### `color.tint`

After Effects: Tint · Phase: P1 · Status: implemented · Tiling: tiled · Reads: — · Reads time: no · Device: GPU when the whole stack lowers, else CPU

Maps luminance between two colors.

| Parameter | Type | Default | Range | Anim | What it does |
|---|---|---|---|---|---|
| `black` | color | `#000000` | — | A | Color that black maps to. |
| `white` | color | `#FFFFFF` | — | A | Color that white maps to. |
| `amount` | percent | 100 | 0–100 (soft) | A | Mix with the input. |

Every instance also takes `expand` (number px or `"none"`); see 01-effects-basics.md.

### `color.tritone`

After Effects: Tritone · Phase: P1 · Status: implemented · Tiling: tiled · Reads: — · Reads time: no · Device: GPU when the whole stack lowers, else CPU

| Parameter | Type | Default | Range | Anim | What it does |
|---|---|---|---|---|---|
| `highlights` | color | `#FFFFFF` | — | A | Color at luminance 1. |
| `midtones` | color | `#C8A064` | — | A | Color at luminance 0.5. |
| `shadows` | color | `#000000` | — | A | Color at luminance 0. |
| `amount` | percent | 100 | 0–100 (soft) | A | Mix with the input. |

Every instance also takes `expand` (number px or `"none"`); see 01-effects-basics.md.

### `color.gradientMap`

After Effects: Colorama (simplified) / Gradient Map · Phase: P1 · Status: implemented · Tiling: tiled · Reads: — · Reads time: no · Device: GPU when the whole stack lowers, else CPU

Duotones, thermal looks, animated color cycling (`phase`).

| Parameter | Type | Default | Range | Anim | What it does |
|---|---|---|---|---|---|
| `gradient` | gradient | gradient `#000000` → `#FFFFFF` (oklab) | — | A | The colors the input maps to. |
| `input` | enum `luminance` / `red` / `green` / `blue` / `alpha` / `hue` / `saturation` | `luminance` | — | — | Which value of the pixel drives the lookup (encoded). |
| `phase` | percent | 0 | 0–100 (soft) | A | Shifts the lookup along the gradient (animate for color cycling). |
| `cycles` | number | 1 | ≥ 0 (clamped) | A | Repetitions of the gradient over the input range. |
| `amount` | percent | 100 | 0–100 (soft) | A | Mix with the input. |
| `modifyAlpha` | boolean | false | — | — | Use the gradient's alpha (multiplied with the pixel alpha). |

Every instance also takes `expand` (number px or `"none"`); see 01-effects-basics.md.

### `color.lut`

After Effects: Apply Color LUT / Lumetri LUT · Phase: P1 · Status: implemented · Tiling: tiled · Reads: — · Reads time: no · Device: GPU when the whole stack lowers, else CPU

Tetrahedral interpolation (no banding in skies).

| Parameter | Type | Default | Range | Anim | What it does |
|---|---|---|---|---|---|
| `lut` | asset id | none | — | — | The `.cube` LUT asset (1D or 3D). |
| `amount` | percent | 100 | 0–100 (soft) | A | Mix with the input. |
| `inputSpace` | enum `display` / `linear` / `logC` / `slog3` / `acescct` | `display` | — | — | The encoding the LUT expects. |
| `interpolation` | enum `tetrahedral` / `trilinear` | `tetrahedral` | — | — | 3D LUT interpolation. |

Every instance also takes `expand` (number px or `"none"`); see 01-effects-basics.md.

### `color.invert`

After Effects: Invert · Phase: P1 · Status: implemented · Tiling: tiled · Reads: — · Reads time: no · Device: GPU when the whole stack lowers, else CPU

On display-encoded values (what an author expects "invert" to look like).

| Parameter | Type | Default | Range | Anim | What it does |
|---|---|---|---|---|---|
| `channel` | enum `rgb` / `red` / `green` / `blue` / `alpha` / `luminance` / `hue` | `rgb` | — | — | What is inverted. |
| `amount` | percent | 100 | 0–100 (soft) | A | Mix with the input. |

Every instance also takes `expand` (number px or `"none"`); see 01-effects-basics.md.

### `color.vibrance`

After Effects: Vibrance · Phase: P2 · Status: implemented · Tiling: tiled · Reads: — · Reads time: no · Device: GPU when the whole stack lowers, else CPU

Display-encoded, per pixel: `saturation` scales the HSL saturation; `vibrance` adds saturation in proportion to how unsaturated a color is ((1 − s) · min(s, 0.5)), weighted down by up to 60 % for skin-tone hues (10°–50°).

| Parameter | Type | Default | Range | Anim | What it does |
|---|---|---|---|---|---|
| `vibrance` | number | 0 | -100–100 (clamped) | A | Saturation added mostly to muted colors. |
| `saturation` | number | 0 | -100–100 (clamped) | A | Plain saturation change. |

Every instance also takes `expand` (number px or `"none"`); see 01-effects-basics.md.

### `color.balance`

After Effects: Color Balance · Phase: P2 · Status: implemented · Tiling: tiled · Reads: — · Reads time: no · Device: GPU when the whole stack lowers, else CPU

Display-encoded: adds half of each offset per channel, weighted by the pixel's luma (shadows below 0.5, highlights above, midtones between); `preserveLuminosity` keeps the luma.

| Parameter | Type | Default | Range | Anim | What it does |
|---|---|---|---|---|---|
| `shadows` | point3d `[x, y, z]` | `[0, 0, 0]` | — | A | Red, green and blue offsets of the shadows (−100…100). |
| `midtones` | point3d `[x, y, z]` | `[0, 0, 0]` | — | A | Offsets of the midtones. |
| `highlights` | point3d `[x, y, z]` | `[0, 0, 0]` | — | A | Offsets of the highlights. |
| `preserveLuminosity` | boolean | true | — | — | Keep each pixel's luma. |

Every instance also takes `expand` (number px or `"none"`); see 01-effects-basics.md.

### `color.channelMixer`

After Effects: Channel Mixer · Phase: P2 · Status: implemented · Tiling: tiled · Reads: — · Reads time: no · Device: GPU when the whole stack lowers, else CPU

Display-encoded: each output channel is a percent mix of the input channels plus a constant; `monochrome` writes the red row to all three.

| Parameter | Type | Default | Range | Anim | What it does |
|---|---|---|---|---|---|
| `rr` | number | 100 | -200–200 (clamped) | A | Mixer entry, percent. |
| `rg` | number | 0 | -200–200 (clamped) | A | Mixer entry, percent. |
| `rb` | number | 0 | -200–200 (clamped) | A | Mixer entry, percent. |
| `rc` | number | 0 | -200–200 (clamped) | A | Mixer entry, percent. |
| `gr` | number | 0 | -200–200 (clamped) | A | Mixer entry, percent. |
| `gg` | number | 100 | -200–200 (clamped) | A | Mixer entry, percent. |
| `gb` | number | 0 | -200–200 (clamped) | A | Mixer entry, percent. |
| `gc` | number | 0 | -200–200 (clamped) | A | Mixer entry, percent. |
| `br` | number | 0 | -200–200 (clamped) | A | Mixer entry, percent. |
| `bg` | number | 0 | -200–200 (clamped) | A | Mixer entry, percent. |
| `bb` | number | 100 | -200–200 (clamped) | A | Mixer entry, percent. |
| `bc` | number | 0 | -200–200 (clamped) | A | Mixer entry, percent. |
| `monochrome` | boolean | false | — | — | Use the red row for every channel. |

Every instance also takes `expand` (number px or `"none"`); see 01-effects-basics.md.

### `color.posterize`

After Effects: Posterize · Phase: P2 · Status: implemented · Tiling: tiled · Reads: — · Reads time: no · Device: GPU when the whole stack lowers, else CPU

Display-encoded: each channel rounded to one of `levels` values; `dither` adds ±½ step of blue noise before rounding, to break up bands.

| Parameter | Type | Default | Range | Anim | What it does |
|---|---|---|---|---|---|
| `levels` | integer | 8 | 2–255 (clamped) | A | Values per channel. |
| `dither` | boolean | false | — | — | Blue-noise dither before rounding. |

Every instance also takes `expand` (number px or `"none"`); see 01-effects-basics.md.

### `color.threshold`

After Effects: Threshold / CC Threshold · Phase: P2 · Status: implemented · Tiling: tiled · Reads: — · Reads time: no · Device: GPU when the whole stack lowers, else CPU

Display-encoded luma: white at or above `level`, black below, with a `softness`-wide ramp for an anti-aliased threshold.

| Parameter | Type | Default | Range | Anim | What it does |
|---|---|---|---|---|---|
| `level` | number | 0.5 | 0–1 (clamped) | A | Luma threshold (encoded). |
| `softness` | number | 0 | 0–1 (clamped) | A | Width of the ramp around the threshold. |

Every instance also takes `expand` (number px or `"none"`); see 01-effects-basics.md.

### `color.blackWhite`

After Effects: Black & White · Phase: P2 · Status: implemented · Tiling: tiled · Reads: — · Reads time: no · Device: GPU when the whole stack lowers, else CPU

Display-encoded: a grey from the luma, raised or lowered by the six hue weights (interpolated around the wheel) in proportion to the saturation; `tint` applies its hue and saturation.

| Parameter | Type | Default | Range | Anim | What it does |
|---|---|---|---|---|---|
| `reds` | percent | 40 | -200–300 (soft) | A | Weight of the reds. |
| `yellows` | percent | 60 | -200–300 (soft) | A | Weight of the yellows. |
| `greens` | percent | 40 | -200–300 (soft) | A | Weight of the greens. |
| `cyans` | percent | 60 | -200–300 (soft) | A | Weight of the cyans. |
| `blues` | percent | 20 | -200–300 (soft) | A | Weight of the blues. |
| `magentas` | percent | 80 | -200–300 (soft) | A | Weight of the magentas. |
| `tint` | color | none | — | A | Tint color (none = grey). |

Every instance also takes `expand` (number px or `"none"`); see 01-effects-basics.md.

### `color.leaveColor`

After Effects: Leave Color · Phase: P2 · Status: implemented · Tiling: tiled · Reads: — · Reads time: no · Device: GPU when the whole stack lowers, else CPU

Display-encoded: desaturates by `amount` every pixel whose RGB distance to `keep` is past `tolerance`, ramping over `softness`.

| Parameter | Type | Default | Range | Anim | What it does |
|---|---|---|---|---|---|
| `keep` | color | `#FF0000` | — | A | The color that keeps its saturation. |
| `amount` | percent | 100 | 0–100 (soft) | A | How much the rest is desaturated. |
| `tolerance` | percent | 10 | 0–100 (soft) | A | Distance kept in full, percent. |
| `softness` | percent | 10 | 0–100 (soft) | A | Ramp beyond the tolerance, percent. |

Every instance also takes `expand` (number px or `"none"`); see 01-effects-basics.md.

### `color.changeColor`

After Effects: Change Color / Change to Color · Phase: P2 · Status: implemented · Tiling: tiled · Reads: — · Reads time: no · Device: GPU when the whole stack lowers, else CPU

Display-encoded: pixels matching `from` by `match` within `tolerance`, ramping over `softness`, take `to`'s hue, saturation and lightness when `to` is set, else are shifted by the three shifts.

| Parameter | Type | Default | Range | Anim | What it does |
|---|---|---|---|---|---|
| `from` | color | `#FF0000` | — | A | The color to change. |
| `to` | color | none | — | A | The color it becomes (none = use the shifts). |
| `hueShift` | angle ° | 0 | — | A | Hue shift in degrees. |
| `lightnessShift` | number | 0 | -100–100 (clamped) | A | Lightness shift, percent. |
| `saturationShift` | number | 0 | -100–100 (clamped) | A | Saturation shift, percent. |
| `tolerance` | percent | 15 | 0–100 (soft) | A | Distance changed in full, percent. |
| `softness` | percent | 10 | 0–100 (soft) | A | Ramp beyond the tolerance, percent. |
| `match` | enum `rgb` / `hue` / `chroma` | `hue` | — | — | How colors are compared with `from`. |

Every instance also takes `expand` (number px or `"none"`); see 01-effects-basics.md.

### `color.whiteBalance`

After Effects: — (Lumetri temperature/tint) · Phase: P2 · Status: implemented · Tiling: tiled · Reads: — · Reads time: no · Device: GPU when the whole stack lowers, else CPU

Bradford chromatic adaptation in linear light from a source white to the working space's D65: `temperature` moves the source white along the CIE daylight locus (positive = a bluer source, so the image warms), `tint` across it (positive = magenta), or `neutral` sets the source white to a color that should come out grey.

| Parameter | Type | Default | Range | Anim | What it does |
|---|---|---|---|---|---|
| `temperature` | number | 0 | -100–100 (clamped) | A | Warmer (positive) or cooler. |
| `tint` | number | 0 | -100–100 (clamped) | A | Magenta (positive) or green. |
| `neutral` | color | none | — | A | A color that should be neutral grey (sets the source white). |

Every instance also takes `expand` (number px or `"none"`); see 01-effects-basics.md.

### `color.selective`

After Effects: Selective Color · Phase: P2 · Status: implemented · Tiling: tiled · Reads: — · Reads time: no · Device: GPU when the whole stack lowers, else CPU

| Parameter | Type | Default | Range | Anim | What it does |
|---|---|---|---|---|---|
| `reds` | list of `[cyan, magenta, yellow, black] percents −100…100` | `[0, 0, 0, 0]` | — | A | The cyan, magenta, yellow and black adjustments of this range. |
| `yellows` | list of `[cyan, magenta, yellow, black] percents −100…100` | `[0, 0, 0, 0]` | — | A | The cyan, magenta, yellow and black adjustments of this range. |
| `greens` | list of `[cyan, magenta, yellow, black] percents −100…100` | `[0, 0, 0, 0]` | — | A | The cyan, magenta, yellow and black adjustments of this range. |
| `cyans` | list of `[cyan, magenta, yellow, black] percents −100…100` | `[0, 0, 0, 0]` | — | A | The cyan, magenta, yellow and black adjustments of this range. |
| `blues` | list of `[cyan, magenta, yellow, black] percents −100…100` | `[0, 0, 0, 0]` | — | A | The cyan, magenta, yellow and black adjustments of this range. |
| `magentas` | list of `[cyan, magenta, yellow, black] percents −100…100` | `[0, 0, 0, 0]` | — | A | The cyan, magenta, yellow and black adjustments of this range. |
| `whites` | list of `[cyan, magenta, yellow, black] percents −100…100` | `[0, 0, 0, 0]` | — | A | The cyan, magenta, yellow and black adjustments of this range. |
| `neutrals` | list of `[cyan, magenta, yellow, black] percents −100…100` | `[0, 0, 0, 0]` | — | A | The cyan, magenta, yellow and black adjustments of this range. |
| `blacks` | list of `[cyan, magenta, yellow, black] percents −100…100` | `[0, 0, 0, 0]` | — | A | The cyan, magenta, yellow and black adjustments of this range. |
| `method` | enum `relative` / `absolute` | `relative` | — | — | Scale by the existing ink, or apply as is. |

Every instance also takes `expand` (number px or `"none"`); see 01-effects-basics.md.

### `color.grade`

After Effects: Lumetri Color (basic + creative + wheels) · Phase: P2 · Status: implemented · Tiling: whole · Reads: — · Reads time: no · Device: CPU

One effect for "make it look graded".

| Parameter | Type | Default | Range | Anim | What it does |
|---|---|---|---|---|---|
| `exposure` | number | 0 | -10–10 (clamped) | A | Stops. |
| `contrast` | number | 0 | -100–100 (clamped) | A | Contrast about mid grey. |
| `highlights` | number | 0 | -100–100 (clamped) | A | Lift or lower the highlights. |
| `shadows` | number | 0 | -100–100 (clamped) | A | Lift or lower the shadows. |
| `whites` | number | 0 | -100–100 (clamped) | A | Lift or lower the whites. |
| `blacks` | number | 0 | -100–100 (clamped) | A | Lift or lower the blacks. |
| `temperature` | number | 0 | -100–100 (clamped) | A | Warmer (positive) or cooler. |
| `tint` | number | 0 | -100–100 (clamped) | A | Magenta (positive) or green. |
| `saturation` | number | 100 | 0–200 (clamped) | A | Saturation (100 is neutral). |
| `vibrance` | number | 0 | -100–100 (clamped) | A | Saturation added mostly to muted colors. |
| `fadedFilm` | number | 0 | 0–100 (clamped) | A | Lift of the blacks (the faded-film look). |
| `sharpen` | number | 0 | 0–100 (clamped) | A | Sharpen amount. |
| `lift` | point3d `[x, y, z]` | `[0, 0, 0]` | — | A | Shadows wheel: [r, g, b] offsets (−1…1). |
| `gamma` | point3d `[x, y, z]` | `[0, 0, 0]` | — | A | Midtones wheel: [r, g, b] offsets (−1…1). |
| `gain` | point3d `[x, y, z]` | `[0, 0, 0]` | — | A | Highlights wheel: [r, g, b] offsets (−1…1). |
| `offset` | point3d `[x, y, z]` | `[0, 0, 0]` | — | A | Offset wheel: [r, g, b] added to everything (−1…1). |
| `lut` | asset id | none | — | — | A creative look LUT (`.cube`), applied after the basic correction. |
| `lutAmount` | percent | 100 | 0–100 (soft) | A | Mix of the look LUT. |
| `vignette.amount` | number | 0 | -1–1 (clamped) | A | Vignette: negative darkens the edges, positive lightens. |
| `vignette.midpoint` | percent | 50 | 0–100 (soft) | A | Vignette: where the falloff is centered. |
| `vignette.roundness` | number | 0 | -100–100 (clamped) | A | Vignette: positive toward a circle. |
| `vignette.feather` | percent | 50 | 0–100 (soft) | A | Vignette: width of the falloff. |

Every instance also takes `expand` (number px or `"none"`); see 01-effects-basics.md.

### `color.broadcastColors`

After Effects: Broadcast Colors · Phase: P2 · Status: implemented · Tiling: tiled · Reads: — · Reads time: no · Device: CPU

Broadcast legalizer on display-encoded values.

| Parameter | Type | Default | Range | Anim | What it does |
|---|---|---|---|---|---|
| `locale` | enum `ntsc` / `pal` | `ntsc` | — | — | The broadcast standard. |
| `howToMakeSafe` | enum `reduceLuminance` / `reduceSaturation` / `keyOutUnsafe` / `keyOutSafe` | `reduceLuminance` | — | — | What happens to unsafe pixels. |
| `maxSignal` | number | 110 | 90–120 (clamped) | A | Maximum signal amplitude in IRE. |

Every instance also takes `expand` (number px or `"none"`); see 01-effects-basics.md.

### `color.ccColorNeutralizer`

After Effects: CC Color Neutralizer · Phase: P2 · Status: implemented · Tiling: tiled · Reads: — · Reads time: no · Device: CPU

Per-range cast removal: each range's `unbalance` colour is mapped to its `balance` colour.

| Parameter | Type | Default | Range | Anim | What it does |
|---|---|---|---|---|---|
| `shadowsUnbalance` | color | `#000000` | — | A | The shadows' cast. |
| `shadowsBalance` | color | `#000000` | — | A | What the shadows' cast becomes. |
| `midtonesUnbalance` | color | `#808080` | — | A | The midtones' cast. |
| `midtonesBalance` | color | `#808080` | — | A | What the midtones' cast becomes. |
| `highlightsUnbalance` | color | `#FFFFFF` | — | A | The highlights' cast. |
| `highlightsBalance` | color | `#FFFFFF` | — | A | What the highlights' cast becomes. |
| `pinning` | percent | 0 | 0–100 (soft) | A | Keep pure black and white fixed. |
| `blendWithOriginal` | percent | 0 | 0–100 (soft) | A | Mix back toward the layer. |
| `darks` | number | 0 | -100–100 (clamped) | A | Lift or lower the darks. |
| `brights` | number | 0 | -100–100 (clamped) | A | Lift or lower the brights. |
| `contrast` | number | 0 | -100–100 (clamped) | A | Slope about mid grey. |

Every instance also takes `expand` (number px or `"none"`); see 01-effects-basics.md.

### `color.ccColorOffset`

After Effects: CC Color Offset · Phase: P2 · Status: implemented · Tiling: tiled · Reads: — · Reads time: no · Device: CPU

Per-channel phase offset (one revolution = the channel's full range), overflow by `overflow`.

| Parameter | Type | Default | Range | Anim | What it does |
|---|---|---|---|---|---|
| `redPhase` | angle ° | 0 | — | A | Red shift (360° = the full range). |
| `greenPhase` | angle ° | 0 | — | A | Green shift. |
| `bluePhase` | angle ° | 0 | — | A | Blue shift. |
| `overflow` | enum `wrap` / `solarize` / `polarize` | `wrap` | — | — | What happens past 1. |

Every instance also takes `expand` (number px or `"none"`); see 01-effects-basics.md.

### `color.ccKernel`

After Effects: CC Kernel · Phase: P2 · Status: implemented · Tiling: tiled · Reads: — · Reads time: no · Device: CPU

3×3 convolution (`k1` top-left … `k9` bottom-right) divided by `scale`, plus `offset`.

| Parameter | Type | Default | Range | Anim | What it does |
|---|---|---|---|---|---|
| `k1` | number | 0 | — | A | Top-left weight. |
| `k2` | number | 0 | — | A | Top weight. |
| `k3` | number | 0 | — | A | Top-right weight. |
| `k4` | number | 0 | — | A | Left weight. |
| `k5` | number | 1 | — | A | Center weight. |
| `k6` | number | 0 | — | A | Right weight. |
| `k7` | number | 0 | — | A | Bottom-left weight. |
| `k8` | number | 0 | — | A | Bottom weight. |
| `k9` | number | 0 | — | A | Bottom-right weight. |
| `scale` | number | 1 | — | A | The sum is divided by this. |
| `offset` | number | 0 | -1–1 (clamped) | A | Added to the result. |
| `absolute` | boolean | false | — | — | Take the magnitude of the result. |

Every instance also takes `expand` (number px or `"none"`); see 01-effects-basics.md.

### `color.ccToner`

After Effects: CC Toner · Phase: P2 · Status: implemented · Tiling: tiled · Reads: — · Reads time: no · Device: CPU

Luma-mapped toning with up to five stops (`color.tritone` is the three-stop case).

| Parameter | Type | Default | Range | Anim | What it does |
|---|---|---|---|---|---|
| `tones` | enum `duotone` / `tritone` / `pentone` | `tritone` | — | — | How many stops the ramp has. |
| `highlights` | color | `#FFFFFF` | — | A | The top stop. |
| `brights` | color | `#DBC7A3` | — | A | The stop between midtones and highlights (pentone). |
| `midtones` | color | `#8C6E47` | — | A | The middle stop (tritone, pentone). |
| `darktones` | color | `#422E1A` | — | A | The stop between shadows and midtones (pentone). |
| `shadows` | color | `#000000` | — | A | The bottom stop. |
| `blendWithOriginal` | percent | 0 | 0–100 (soft) | A | Mix back toward the layer. |

Every instance also takes `expand` (number px or `"none"`); see 01-effects-basics.md.

### `color.colorLink`

After Effects: Color Link · Phase: P2 · Status: implemented · Tiling: whole · Reads: other layers · Reads time: no · Device: CPU

Fills the layer with one colour sampled from `sourceLayer` at the same comp time (per frame, so deterministic).

| Parameter | Type | Default | Range | Anim | What it does |
|---|---|---|---|---|---|
| `sourceLayer` | layer id | none | — | — | The layer sampled (null = this layer). |
| `sourceLayerSource` | enum `source` / `masks` / `effects` | `effects` | — | — | What of the other layer is read (spec 7 §7.6). |
| `sample` | enum `average` / `median` / `brightest` / `darkest` / `maxRgb` / `minRgb` / `averageAlpha` / `medianAlpha` / `maxAlpha` / `minAlpha` | `average` | — | — | Which statistic of the source is the color. |
| `clip` | percent | 0 | 0–100 (soft) | A | Fraction of extreme pixels ignored. |
| `stencilOriginalAlpha` | boolean | true | — | — | Keep the layer's alpha. |
| `opacity` | percent | 100 | 0–100 (soft) | A | Opacity of the sampled color. |
| `blendingMode` | enum `normal` / `add` / `multiply` / `screen` / `overlay` / `softLight` / `hardLight` / `darken` / `lighten` / `difference` / `hue` / `color` / `luminosity` | `normal` | — | — | Blend mode of the color over the layer. |

Every instance also takes `expand` (number px or `"none"`); see 01-effects-basics.md.

### `color.equalize`

After Effects: Equalize · Phase: P2 · Status: implemented · Tiling: whole · Reads: — · Reads time: no · Device: CPU

Histogram equalization of the current frame only (no temporal smoothing, so chunk-safe).

| Parameter | Type | Default | Range | Anim | What it does |
|---|---|---|---|---|---|
| `style` | enum `rgb` / `brightness` / `photoshop` | `rgb` | — | — | Which histogram is equalized. |
| `amount` | percent | 100 | 0–100 (soft) | A | How much of the equalization is applied. |

Every instance also takes `expand` (number px or `"none"`); see 01-effects-basics.md.

### `color.gammaPedestalGain`

After Effects: Gamma/Pedestal/Gain · Phase: P2 · Status: implemented · Tiling: tiled · Reads: — · Reads time: no · Device: CPU

Display-encoded per-channel pedestal, gain and gamma.

| Parameter | Type | Default | Range | Anim | What it does |
|---|---|---|---|---|---|
| `blackStretch` | number | 0 | 0–4 (clamped) | A | Lift of the low values. |
| `red.gamma` | number | 1 | 0.1–10 (clamped) | A | Red gamma. |
| `red.pedestal` | number | 0 | -2–2 (clamped) | A | Red value at black. |
| `red.gain` | number | 1 | 0–4 (clamped) | A | Red value at white. |
| `green.gamma` | number | 1 | 0.1–10 (clamped) | A | Green gamma. |
| `green.pedestal` | number | 0 | -2–2 (clamped) | A | Green value at black. |
| `green.gain` | number | 1 | 0–4 (clamped) | A | Green value at white. |
| `blue.gamma` | number | 1 | 0.1–10 (clamped) | A | Blue gamma. |
| `blue.pedestal` | number | 0 | -2–2 (clamped) | A | Blue value at black. |
| `blue.gain` | number | 1 | 0–4 (clamped) | A | Blue value at white. |

Every instance also takes `expand` (number px or `"none"`); see 01-effects-basics.md.

### `color.arbitraryMap`

After Effects: PS Arbitrary Map · Phase: P2 · Status: implemented · Tiling: tiled · Reads: — · Reads time: no · Device: CPU

Per-channel lookup from a Photoshop arbitrary map.

| Parameter | Type | Default | Range | Anim | What it does |
|---|---|---|---|---|---|
| `map` | asset id | none | — | — | The Photoshop arbitrary map (`.amp`): a 1D LUT or a list of 256 values; none = identity. |
| `phase` | number | 0 | — | A | Rotation of the lookup (255 = one turn). |
| `applyPhaseMapToAlpha` | boolean | false | — | — | Map the alpha as well. |

Every instance also takes `expand` (number px or `"none"`); see 01-effects-basics.md.

### `color.photoFilter`

After Effects: Photo Filter · Phase: P2 · Status: implemented · Tiling: tiled · Reads: — · Reads time: no · Device: CPU

Photographic colour filter, display-encoded.

| Parameter | Type | Default | Range | Anim | What it does |
|---|---|---|---|---|---|
| `filter` | enum `warming85` / `warmingLba` / `warming81` / `cooling80` / `coolingLbb` / `cooling82` / `red` / `orange` / `yellow` / `green` / `cyan` / `blue` / `violet` / `magenta` / `sepia` / `deepRed` / `deepBlue` / `deepEmerald` / `deepYellow` / `underwater` / `custom` | `warming85` | — | — | The filter preset, or `custom`. |
| `color` | color | `#ED8A17` | — | A | The custom filter color. |
| `density` | percent | 25 | 0–100 (soft) | A | Strength of the filter. |
| `preserveLuminosity` | boolean | true | — | — | Keep the input's luma. |

Every instance also takes `expand` (number px or `"none"`); see 01-effects-basics.md.

<!-- gen:catalogue-color-1:end -->
