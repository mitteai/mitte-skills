# The effect catalogue: index

Generated from `rexx-engine effects` by scripts/skills-effects-catalogue.py; do not edit by hand (the engine version is not written here so a version bump alone does not stale the page). Each row links to its family page (usage, examples) and to the generated parameter page of its category.

<!-- gen:catalogue-index:start -->
Registry: 245 ids, 240 implemented, 5 specified only (`blur.reduceInterlace`, `color.autoContrast`, `stylize.datamosh`, `stylize.motionTrails`, `perspective.3dGlasses`).

Columns: **Tiling** `tiled` (per band of rows; a tile is a pure function of its input region), `whole` (one call over the whole output: recursive blurs, distance fields) or `backdrop` (comp space, reads the composite below; must be last).
**Reads** are the inputs beyond the layer's own pixels at the default parameters (`layer` and mask-id parameters count once one is set). **Time** `yes` means the pixels depend on the frame time beyond the evaluated parameters (the layer image cache never reuses the layer across frames). **Device**: `GPU when the whole stack lowers` effects have a device lowering (engine 15 §15.3 step C); a layer's stack runs on the GPU only when every effect in it lowers, every `blend.mode` is `normal`, no effect has `mask`, and the device has f64 for the recursive Gaussian; otherwise the stack runs on the CPU (the frame's other work may still run on the device). `utility.shader` is GPU only (`effect.requires_gpu` on the CPU).

## Blur & sharpen

Usage: [10-blur-sharpen.md](10-blur-sharpen.md). Parameters: [91-catalogue-blur.md](91-catalogue-blur.md).

| Type | After Effects | Phase | Status | Tiling | Reads | Time | Device | Note |
|---|---|---|---|---|---|---|---|---|
| `blur.gaussian` | Gaussian Blur / Gaussian Blur (Legacy) | P1 | implemented | whole | — | no | GPU when the whole stack lowers, else CPU | True Gaussian whose visible extent is `radius` (σ = radius / 3). |
| `blur.fast` | Fast Box Blur | P1 | implemented | whole | — | no | GPU when the whole stack lowers, else CPU | Running-sum box with fractional radius (the partial edge pixel weighted), iterated. |
| `blur.box` | Box Blur | P2 | implemented | whole | — | no | GPU when the whole stack lowers, else CPU | As `blur.fast` with one iteration by default (the visible box shape is the point); transparent outside the layer. |
| `blur.directional` | Directional Blur | P1 | implemented | tiled | — | no | GPU when the whole stack lowers, else CPU | Line integral along the direction, sample count = ceil(length) · 2 with linear interpolation; linear-light. |
| `blur.radial` | Radial Blur / CC Radial Fast Blur / CC Radial Blur | P1 | implemented | whole | — | no | GPU when the whole stack lowers, else CPU | Zoom averages the source along the segment from the pixel `P` toward `center` `C`, the points `C + (P − C)·(1 − a·t)` for `t` in (0, 1) with `a` = `amount` / 100 capped at 0.95, transparent outside the source; spin averages along the arc about `C` over `amount` degrees. |
| `blur.sharpen` | Sharpen | P1 | implemented | tiled | — | no | GPU when the whole stack lowers, else CPU | 3×3 Laplacian-based sharpen on display-encoded luma, clamped to avoid ringing beyond the input's local range. |
| `blur.unsharp` | Unsharp Mask | P1 | implemented | whole | — | no | CPU | Classic unsharp mask on display-encoded luma. |
| `blur.bilateral` | Bilateral Blur | P2 | implemented | tiled | — | no | CPU | Edge-preserving; skin smoothing, painterly looks. |
| `blur.smart` | Smart Blur | P2 | implemented | tiled | — | no | CPU |  |
| `blur.channel` | Channel Blur | P2 | implemented | whole | — | no | CPU | Per-channel Gaussian (on unpremultiplied color for RGB). |
| `blur.compound` | Compound Blur | P2 | implemented | whole | other layers | no | CPU | Per-pixel Gaussian radius from map luminance; computed with a blur pyramid and trilinear interpolation between levels (fast, smooth). |
| `blur.tiltShift` | — (common plugin look) | P2 | implemented | whole | — | no | CPU | Variable blur that grows with distance from a focus band; uses the `blur.compound` pyramid, or the lens kernel at best quality. |
| `blur.ccCross` | CC Cross Blur | P2 | implemented | whole | — | no | CPU | A horizontal and a vertical blur combined by `transferMode`. |
| `blur.ccVector` | CC Vector Blur | P2 | implemented | whole | — | no | CPU | Blur along the layer's own gradient field (the map is the layer itself, softened by `mapSoftness`). |
| `blur.camera` | Camera Lens Blur | P3 | implemented | whole | other layers | no | CPU | Scatter-as-gather bokeh with an iris kernel, in linear light so highlights bloom into bright bokeh discs (the reason to use this instead of Gaussian). |
| `blur.reduceInterlace` | Reduce Interlace Flicker | P4 | not implemented (P4: `effect.unavailable`) | — | — | no | CPU | Only for broadcast deliverables. |

## Light & glow

Usage: [11-light-glow.md](11-light-glow.md). Parameters: [91-catalogue-light.md](91-catalogue-light.md).

| Type | After Effects | Phase | Status | Tiling | Reads | Time | Device | Note |
|---|---|---|---|---|---|---|---|---|
| `light.glow` | Glow, at Deep Glow quality | P1 | implemented | whole | — | no | GPU when the whole stack lowers, else CPU | A multi-scale bloom: the thresholded source is downsampled into a mip pyramid (up to 10 levels), each level blurred, and the levels summed with weights that approximate the chosen falloff kernel up to `radius`. |
| `light.bloom` | — (highlight bloom) | P1 | implemented | whole | — | no | GPU when the whole stack lowers, else CPU | Preset-like specialization of `light.glow` for adjustment layers: only values above 1.0 bloom. |
| `light.rays` | CC Light Rays / Trapcode Shine | P1 | implemented | tiled | — | no | CPU | Radial line integral (god rays) from the thresholded source toward `center`, with exponential decay exp(−3*t*) along the ray; shimmer modulates by angular noise for animated streaks. |
| `light.flare` | Lens Flare / Optical Flares-lite | P2 | implemented | tiled | other layers | no | CPU | A procedural flare built from elements placed along the axis from `center` through the comp center. |
| `light.leak` | — (light leak overlays) | P2 | implemented | tiled | — | yes | CPU | A generator of drifting, overexposed blotches of light (procedural, seeded; animated by low-frequency curl noise). |
| `light.energy` | Saber (Video Copilot) | P2 | implemented | whole | mask paths | no | CPU | Strokes a path (mask, the layer's alpha edge, or a text layer's glyph outlines) with a hot core and a large physically-based glow (the `light.glow` pyramid), displaced along the normal by animated curl noise. |
| `light.neon` | — (neon tube look) | P2 | implemented | whole | — | no | CPU | Convenience over `light.energy` on the layer's outline with no distortion and a white-hot core. |
| `light.ccLightBurst` | CC Light Burst 2.5 | P2 | implemented | tiled | — | no | CPU | Radial burst of the layer's pixels from `center` (`light.rays` is the Trapcode-class version). |
| `light.ccLightSweep` | CC Light Sweep | P2 | implemented | whole | — | no | CPU | A band of light swept across the layer with a highlight on the alpha edge (logo sheens). |
| `light.ccSpotlight` | CC Spotlight | P2 | implemented | tiled | — | no | CPU | 2D spotlight shading cast from `from` toward `to` (no comp lights). |
| `light.godrays3d` | — | P3 | implemented | tiled | — | no | CPU | Rays from a 3D point projected through the comp camera. |

## Color

Usage: [12-color.md](12-color.md). Parameters: [91-catalogue-color-1.md](91-catalogue-color-1.md), [91-catalogue-color-2.md](91-catalogue-color-2.md).

| Type | After Effects | Phase | Status | Tiling | Reads | Time | Device | Note |
|---|---|---|---|---|---|---|---|---|
| `color.levels` | Levels / Levels (Individual Controls) | P1 | implemented | tiled | — | no | GPU when the whole stack lowers, else CPU | Values 0–1 in display encoding (After Effects 32 bpc Levels uses 0–1). |
| `color.curves` | Curves | P1 | implemented | tiled | — | no | GPU when the whole stack lowers, else CPU | Monotone cubic (Fritsch–Carlson) through points; endpoints extrapolate linearly above 1 so HDR values are not clipped. |
| `color.hueSaturation` | Hue/Saturation / Color Balance (HLS) | P1 | implemented | tiled | — | no | GPU when the whole stack lowers, else CPU | Hue rotation in OKLCh by default (`space: "oklch"`), so a hue shift keeps perceived lightness; `space: "hsl"` reproduces After Effects exactly. |
| `color.exposure` | Exposure | P1 | implemented | tiled | — | no | GPU when the whole stack lowers, else CPU | Linear-light multiply by 2^exposure (the correct way to brighten HDR content). |
| `color.brightnessContrast` | Brightness & Contrast | P1 | implemented | tiled | — | no | GPU when the whole stack lowers, else CPU | Non-legacy: contrast pivots around 0.5 display-encoded (After Effects/Photoshop modern behavior). |
| `color.tint` | Tint | P1 | implemented | tiled | — | no | GPU when the whole stack lowers, else CPU | Maps luminance between two colors. |
| `color.tritone` | Tritone | P1 | implemented | tiled | — | no | GPU when the whole stack lowers, else CPU |  |
| `color.gradientMap` | Colorama (simplified) / Gradient Map | P1 | implemented | tiled | — | no | GPU when the whole stack lowers, else CPU | Duotones, thermal looks, animated color cycling (`phase`). |
| `color.lut` | Apply Color LUT / Lumetri LUT | P1 | implemented | tiled | — | no | GPU when the whole stack lowers, else CPU | Tetrahedral interpolation (no banding in skies). |
| `color.invert` | Invert | P1 | implemented | tiled | — | no | GPU when the whole stack lowers, else CPU | On display-encoded values (what an author expects "invert" to look like). |
| `color.vibrance` | Vibrance | P2 | implemented | tiled | — | no | GPU when the whole stack lowers, else CPU | Display-encoded, per pixel: `saturation` scales the HSL saturation; `vibrance` adds saturation in proportion to how unsaturated a color is ((1 − s) · min(s, 0.5)), weighted down by up to 60 % for skin-tone hues (10°–50°). |
| `color.balance` | Color Balance | P2 | implemented | tiled | — | no | GPU when the whole stack lowers, else CPU | Display-encoded: adds half of each offset per channel, weighted by the pixel's luma (shadows below 0.5, highlights above, midtones between); `preserveLuminosity` keeps the luma. |
| `color.channelMixer` | Channel Mixer | P2 | implemented | tiled | — | no | GPU when the whole stack lowers, else CPU | Display-encoded: each output channel is a percent mix of the input channels plus a constant; `monochrome` writes the red row to all three. |
| `color.posterize` | Posterize | P2 | implemented | tiled | — | no | GPU when the whole stack lowers, else CPU | Display-encoded: each channel rounded to one of `levels` values; `dither` adds ±½ step of blue noise before rounding, to break up bands. |
| `color.threshold` | Threshold / CC Threshold | P2 | implemented | tiled | — | no | GPU when the whole stack lowers, else CPU | Display-encoded luma: white at or above `level`, black below, with a `softness`-wide ramp for an anti-aliased threshold. |
| `color.blackWhite` | Black & White | P2 | implemented | tiled | — | no | GPU when the whole stack lowers, else CPU | Display-encoded: a grey from the luma, raised or lowered by the six hue weights (interpolated around the wheel) in proportion to the saturation; `tint` applies its hue and saturation. |
| `color.leaveColor` | Leave Color | P2 | implemented | tiled | — | no | GPU when the whole stack lowers, else CPU | Display-encoded: desaturates by `amount` every pixel whose RGB distance to `keep` is past `tolerance`, ramping over `softness`. |
| `color.changeColor` | Change Color / Change to Color | P2 | implemented | tiled | — | no | GPU when the whole stack lowers, else CPU | Display-encoded: pixels matching `from` by `match` within `tolerance`, ramping over `softness`, take `to`'s hue, saturation and lightness when `to` is set, else are shifted by the three shifts. |
| `color.whiteBalance` | — (Lumetri temperature/tint) | P2 | implemented | tiled | — | no | GPU when the whole stack lowers, else CPU | Bradford chromatic adaptation in linear light from a source white to the working space's D65: `temperature` moves the source white along the CIE daylight locus (positive = a bluer source, so the image warms), `tint` across it (positive = magenta), or `neutral` sets the source white to a color that should come out grey. |
| `color.selective` | Selective Color | P2 | implemented | tiled | — | no | GPU when the whole stack lowers, else CPU |  |
| `color.grade` | Lumetri Color (basic + creative + wheels) | P2 | implemented | whole | — | no | CPU | One effect for "make it look graded". |
| `color.broadcastColors` | Broadcast Colors | P2 | implemented | tiled | — | no | CPU | Broadcast legalizer on display-encoded values. |
| `color.ccColorNeutralizer` | CC Color Neutralizer | P2 | implemented | tiled | — | no | CPU | Per-range cast removal: each range's `unbalance` colour is mapped to its `balance` colour. |
| `color.ccColorOffset` | CC Color Offset | P2 | implemented | tiled | — | no | CPU | Per-channel phase offset (one revolution = the channel's full range), overflow by `overflow`. |
| `color.ccKernel` | CC Kernel | P2 | implemented | tiled | — | no | CPU | 3×3 convolution (`k1` top-left … `k9` bottom-right) divided by `scale`, plus `offset`. |
| `color.ccToner` | CC Toner | P2 | implemented | tiled | — | no | CPU | Luma-mapped toning with up to five stops (`color.tritone` is the three-stop case). |
| `color.colorLink` | Color Link | P2 | implemented | whole | other layers | no | CPU | Fills the layer with one colour sampled from `sourceLayer` at the same comp time (per frame, so deterministic). |
| `color.equalize` | Equalize | P2 | implemented | whole | — | no | CPU | Histogram equalization of the current frame only (no temporal smoothing, so chunk-safe). |
| `color.gammaPedestalGain` | Gamma/Pedestal/Gain | P2 | implemented | tiled | — | no | CPU | Display-encoded per-channel pedestal, gain and gamma. |
| `color.arbitraryMap` | PS Arbitrary Map | P2 | implemented | tiled | — | no | CPU | Per-channel lookup from a Photoshop arbitrary map. |
| `color.photoFilter` | Photo Filter | P2 | implemented | tiled | — | no | CPU | Photographic colour filter, display-encoded. |
| `color.shadowHighlight` | Shadow/Highlight | P2 | implemented | whole | — | no | CPU | `temporalSmoothing` > 0 reads neighbouring frames (`Deps::times`); `autoAmounts` analyses the current frame only. |
| `color.videoLimiter` | Video Limiter | P2 | implemented | tiled | — | no | CPU | Copied from EffectCraft `ec.color.videolimiter`; params as EffectCraft. |
| `color.autoContrast` | Auto Contrast / Auto Levels / Auto Color / Color Stabilizer | — | not implemented (not provided: `effect.unavailable`) | — | — | no | CPU | Not provided: analysis-based auto adjustments (with temporal smoothing, or a reference frame) differ by frame and break determinism across chunks. |

## Generate

Usage: [13-generate.md](13-generate.md). Parameters: [91-catalogue-generate-1.md](91-catalogue-generate-1.md), [91-catalogue-generate-2.md](91-catalogue-generate-2.md).

| Type | After Effects | Phase | Status | Tiling | Reads | Time | Device | Note |
|---|---|---|---|---|---|---|---|---|
| `generate.fill` | Fill | P1 | implemented | tiled | mask paths | no | GPU when the whole stack lowers, else CPU | Recolors the layer's alpha; the standard way to color a footage matte or a logo. |
| `generate.gradient` | Gradient Ramp | P1 | implemented | tiled | — | no | GPU when the whole stack lowers, else CPU | Dithered by default so 8-bit renders of soft gradients do not band: blue noise of ±½ LSB at 8 bits, applied **in linear light** scaled by the encoded LSB step at the pixel's value (a lookup table of step sizes over the linear range), so the effect never encodes and decodes a pixel; it differs from a dither applied in encoded space by at most 1 LSB. |
| `generate.gradient4` | 4-Color Gradient | P1 | implemented | tiled | — | no | GPU when the whole stack lowers, else CPU | Inverse-distance blend with exponent *q* = 200 / `blend` (100 = inverse square); the classic "mesh gradient" background. |
| `generate.fractalNoise` | Fractal Noise | P1 | implemented | tiled | — | no | GPU when the whole stack lowers, else CPU | P1 ships a plain fractional-Brownian-motion noise with the full parameter set, enough for backgrounds, displacement sources, and transitions. |
| `generate.grid` | Grid | P1 | implemented | tiled | — | no | GPU when the whole stack lowers, else CPU | Background grids for tech/UI looks; anti-aliased lines at any border width. |
| `generate.checkerboard` | Checkerboard | P2 | implemented | tiled | — | no | CPU | Cells of `size` px from `anchor`, alternately `color` and transparent, with `feather` px soft edges (half a pixel of anti-aliasing otherwise). |
| `generate.circle` | Circle | P2 | implemented | tiled | — | no | CPU | A disc of `radius` px about `center`, or a ring whose inner edge is `edgeRadius`, a `thickness` in px, or a thickness in percent of the radius (the last also scaling the feathers by the radius), with outer and inner feathers, optionally inverted. |
| `generate.ellipse` | Ellipse | P2 | implemented | tiled | — | no | CPU | A ring of `thickness` px on the ellipse `width` × `height` about `center`, `inside` at its middle fading to `outside` at its edges, with a `softness` percent edge. |
| `generate.beam` | Beam | P2 | implemented | tiled | — | no | CPU | A segment of `length` percent of the path from `start` to `end`, positioned by `time` percent along it, `startThickness` to `endThickness` px wide (the thickness follows the beam's position between the points with `3dPerspective`, its own tail and head otherwise), `inside` at the middle fading to `outside` at the edges. |
| `generate.cells` | Cell Pattern | P2 | implemented | tiled | — | no | CPU | Worley/Voronoi cells of `size` px: one hashed point per cell, scattered by `disperse` (0 = a grid) and circling with `evolution` (one revolution per circle), shaped by `pattern` (the `…Hq` kinds take 4 × 4 samples per pixel over a wider neighbourhood), pushed through `contrast` and `overflow`, optionally inverted and tiled every `tiling.cellsHorizontal` × `tiling.cellsVertical` cells. |
| `generate.lensFlareSimple` | Lens Flare | P2 | implemented | tiled | — | no | CPU | After Effects' built-in flare, for imported projects; `light.flare` is the better one. |
| `generate.meshGradient` | — (mesh/freeform gradients) | P2 | implemented | tiled | — | no | CPU | Freeform gradient with radial basis interpolation in OKLab, optionally warped by animated noise: the animated "aurora blob" background. |
| `generate.curlNoise` | Curl Noise (AE 26.3) | P2 | implemented | tiled | — | no | CPU | Divergence-free noise; `vectorField` outputs a displacement map (red/green), `flowLines` draws advected streaks (silky "flow field" generative look). |
| `generate.stroke` | Stroke | P2 | implemented | whole | mask paths | no | CPU | Strokes masks of the layer; for shape layers prefer the shape stroke ([spec 4](04-shapes.md)). |
| `generate.vegas` | Vegas | P2 | implemented | whole | mask paths | no | CPU | Marching-ants / chasing lights along contours. |
| `generate.scribble` | Scribble | P2 | implemented | whole | mask paths | yes | CPU | Hand-drawn scribble fills: a strong 2026 "human-made" look. |
| `generate.radioWaves` | Radio Waves | P2 | implemented | whole | mask paths, parameter history | yes | CPU | Concentric ripples; ping/notification effects. |
| `generate.audioSpectrum` | Audio Spectrum | P2 | implemented | whole | other layers, mask paths | no | CPU | Spectrum from the audio analysis of [spec 10](10-media-and-audio.md#audio-analysis) (FFT computed once per render, deterministic). |
| `generate.audioWaveform` | Audio Waveform | P2 | implemented | whole | other layers, mask paths | no | CPU |  |
| `generate.turbulentNoise` | Turbulent Noise | P2 | implemented | tiled | — | no | GPU when the whole stack lowers, else CPU | The Turbulent Noise variant of the fractal-noise engine: `turbulenceFactor` folds the noise per octave. |
| `generate.eyedropperFill` | Eyedropper Fill | P2 | implemented | tiled | — | no | CPU | Fills with the colour sampled at `samplePoint` (current frame). |
| `generate.ccThreads` | CC Threads | P2 | implemented | tiled | — | no | CPU | Woven-thread texture over the layer. |
| `generate.fractal` | Fractal | P2 | implemented | tiled | — | no | CPU | Mandelbrot/Julia set generator; the escape iteration is f64 (EffectCraft notes it cannot run in f32 shaders). |
| `generate.advancedLightning` | Advanced Lightning / Lightning (obsolete) | P2 | implemented | whole | — | no | CPU | Seeded, `conductivityState` animates the bolt. |
| `generate.paintBucket` | Paint Bucket | P3 | implemented | whole | — | no | CPU | Implemented: a 4-connected flood fill over the layer rect from `fillPoint`; `tolerance` is in display-encoded 0–255 codes; `featherSoftness` and `spreadRadius` (not in After Effects' panel by these names) are the radii of `feather` and `spread`/`choke`; the fill composites normally over the layer (After Effects' blending modes and View Threshold are not provided). |
| `generate.writeOn` | Write-on | P3 | implemented | whole | parameter history | no | CPU | Paint a stroke by keyframing the brush; signatures, hand-drawn reveals. |
| `generate.ccGlueGun` | CC Glue Gun | P2 | implemented | tiled | parameter history | no | CPU | Blobs of "glue" laid along the animated `brushPosition` over the last `timeSpan` seconds (reads the parameter's history, `Deps::param_samples`). |

## Distort

Usage: [14-distort.md](14-distort.md). Parameters: [91-catalogue-distort-1.md](91-catalogue-distort-1.md), [91-catalogue-distort-2.md](91-catalogue-distort-2.md).

| Type | After Effects | Phase | Status | Tiling | Reads | Time | Device | Note |
|---|---|---|---|---|---|---|---|---|
| `distort.transform` | Transform (effect) | P1 | implemented | tiled | parameter history | no | CPU | A transform inside the effect stack (before other effects), with its own motion blur: the standard trick to motion-blur a layer that is otherwise static, and to transform before a glow. |
| `distort.displacement` | Displacement Map | P1 | implemented | tiled | other layers | no | CPU | Map value 0.5 = no displacement (display-encoded map values, as After Effects). |
| `distort.waveWarp` | Wave Warp | P1 | implemented | tiled | — | yes | GPU when the whole stack lowers, else CPU | Flags, heat haze, wavy text. |
| `distort.offset` | Offset / Motion Tile | P1 | implemented | tiled | — | no | GPU when the whole stack lowers, else CPU | Wraps around the layer edges (seamless scrolling backgrounds). |
| `distort.cornerPin` | Corner Pin / CC Power Pin | P2 | implemented | tiled | — | no | CPU | The projective map (homography) that takes the layer rect's corners to the four points, inverse-mapped per pixel with perspective-correct sampling (bicubic at `high`, bilinear at `low` or in draft, as every distortion here). |
| `distort.bulge` | Bulge / CC Lens | P2 | implemented | tiled | — | no | CPU | Inside the ellipse `radiusX` × `radiusY` about `center` the source is pulled toward the center by `height · (1 − d²)^taper / 2` (negative heights push; `taper` is a number, not After Effects' checkbox: higher makes the sides shallower), fading out over the outer 10 % of the layer with `pinEdges`. |
| `distort.ripple` | Ripple | P2 | implemented | tiled | — | yes | CPU | Concentric waves of `width` px wavelength and `height` px amplitude about `center`, fading to nothing at `radius` percent of the layer, traveling outward at `speed` cycles per second; `asymmetric` ripples also move sideways a quarter wave out of step. |
| `distort.twirl` | Twirl / Twirl (Legacy) | P2 | implemented | tiled | — | no | CPU | Rotates the source about `center` by `angle` at the center, falling off quadratically to nothing at `radius`. |
| `distort.spherize` | Spherize | P2 | implemented | tiled | — | no | CPU | Wraps the source onto a sphere of `radius` px about `center` (`d → asin(d / R) / (π/2)`). |
| `distort.polar` | Polar Coordinates | P2 | implemented | tiled | — | no | CPU | `rectToPolar` reads the layer rect as (angle → x, radius → y) around its center, `polarToRect` the reverse, mixed with the identity by `interpolation`; reads are clamped to the layer rect. |
| `distort.mirror` | Mirror | P2 | implemented | tiled | — | no | CPU | The half-plane past the line through `center` perpendicular to `angle` shows the other half reflected; `angle` is the direction of the reflected half (0 = right, so the right side mirrors the left; 90 = down). |
| `distort.turbulent` | Turbulent Displace | P2 | implemented | tiled | — | no | CPU | Displaces every pixel by `amount` px of `generate.fractalNoise`'s noise (`size` px cells, `complexity` octaves, `evolution`): two independent noises for `turbulent`, the noise gradient for `bulge`, its rotation for `twist` (the `…Smoother` kinds use a gentler octave falloff), one axis for `vertical`/`horizontal`, the same noise on both axes for `cross`. |
| `distort.motionTile` | Motion Tile | P2 | implemented | tiled | — | no | CPU | The layer rect repeated in tiles of `tileWidth` × `tileHeight` percent of it, centered on `center`, over an output of `outputWidth` × `outputHeight` percent of the layer about its center; `mirrorEdges` flips alternate tiles, `phase` slides alternate rows (columns with `horizontalPhaseShift`). |
| `distort.kaleidoscope` | CC Kaleida | P2 | implemented | tiled | — | no | CPU | The plane around `center` is divided into wedges (`dia` 6, `octo` 8, `cross` 4 and `tri` 3 mirrored wedges; `wheel` 12 unmirrored) rotated by `rotation`; every pixel reads the first wedge at `size` percent scale, so one wedge of the source repeats around the center. |
| `distort.magnify` | Magnify | P2 | implemented | tiled | — | no | CPU | Inside a circle or square of `size` px about `center` (feathered over `feather` px) the source appears magnified by `magnification`, read nearest-pixel (`standard`), bicubic (`softSharp`) or jittered (`scatter`), blended by `blending` at `opacity` over the layer; outside, the layer (with `blending: none`, nothing). |
| `distort.lens` | Optics Compensation / Lens Distortion | P2 | implemented | tiled | — | no | CPU | Barrel distortion of a lens with `fov` degrees across the layer's width, height or diagonal about `center`: a pixel at distance *r* reads the source at `f · tan(r / r_ref · fov / 2)` with `f = r_ref / tan(fov / 2)`; `reverse` applies the inverse (pincushion), and `resizing` lets the stretched corners grow the output (up to 2×, 4× or, for `unlimited`, 8× the layer). |
| `distort.meshWarp` | Mesh Warp | P2 | implemented | tiled | — | no | CPU | Bezier patch mesh. |
| `distort.bezierWarp` | Bezier Warp | P2 | implemented | tiled | — | no | CPU |  |
| `distort.ccFlo` | CC Flo Motion | P2 | implemented | tiled | — | no | CPU |  |
| `distort.ccBend` | CC Bend It | P2 | implemented | tiled | — | no | CPU |  |
| `distort.ccBender` | CC Bender | P2 | implemented | tiled | — | no | CPU | Bends the layer between `base` and `top`. |
| `distort.ccSlant` | CC Slant | P2 | implemented | tiled | — | no | CPU | Shears the layer about `floor`. |
| `distort.ccSmear` | CC Smear | P2 | implemented | tiled | — | no | CPU | Drags the pixels around `from` toward `to`. |
| `distort.ccSplit` | CC Split | P2 | implemented | tiled | — | no | CPU | Opens a slit between the two points. |
| `distort.ccSplit2` | CC Split 2 | P2 | implemented | tiled | — | no | CPU | As `distort.ccSplit` with the two sides opened independently. |
| `distort.ccTiler` | CC Tiler | P2 | implemented | tiled | — | no | CPU | Tiles scaled copies of the layer about `center`. |
| `distort.ccGriddler` | CC Griddler | P2 | implemented | tiled | — | no | CPU | Tiles the layer into a rotated, scaled grid. |
| `distort.warp` | Warp | P2 | implemented | tiled | — | no | CPU | The fifteen Photoshop warp styles, inverse-mapped. |
| `distort.ccBlobbylize` | CC Blobbylize | P2 | implemented | whole | other layers | no | CPU | Lit blobs shaped by the blob layer's `property`. |
| `distort.ccScatterize` | CC Scatterize | P2 | implemented | whole | — | no | CPU | Pixels scattered (seeded) and twisted; `scatter: 0` is the identity. |
| `distort.glass` | — ("liquid glass" / refraction) | P3 | implemented | backdrop | other layers, the backdrop | no | CPU (backdrop; the GPU walk declines the whole frame) | The 2025–2027 glass look (Apple Liquid Glass and its imitators). |
| `distort.liquify` | Liquify (simplified) | P3 | implemented | whole | — | no | CPU | Implemented as a precomputed displacement field from the strokes (no painting state): dabs every quarter radius along each polyline into a mesh over the layer rect. |
| `distort.smear` | Smear | P3 | implemented | whole | mask paths | no | CPU | Implemented: `stretch` is After Effects' Percent (how far the warp applies); the elasticity is fixed at After Effects' "Absolutely Normal"; both outlines are resampled to at most 256 points and rasterized (which side of each a pixel is on), and the two distances a pixel's weight uses are exact at samples every 8 px and at every pixel within a cell of an outline, interpolated between the samples elsewhere (engine 0.1.55 and earlier measured them exactly at every pixel; the planes agree within a pixel or so far from the outlines, exactly near them); the displacement is capped at the layer's larger side (16–1024 px). |
| `distort.ccRipplePulse` | CC Ripple Pulse | P2 | implemented | tiled | parameter history | no | CPU | Rings emitted by the history of `pulseLevel` over the last `timeSpan` seconds (`Deps::param_samples`). |
| `distort.reshape` | Reshape | P2 | implemented | tiled | mask paths | no | CPU | Warps the source mask's region onto the destination mask; needs mask paths as parameters, like `generate.stroke`. |

## Stylize

Usage: [15-stylize.md](15-stylize.md). Parameters: [91-catalogue-stylize-1.md](91-catalogue-stylize-1.md), [91-catalogue-stylize-2.md](91-catalogue-stylize-2.md).

| Type | After Effects | Phase | Status | Tiling | Reads | Time | Device | Note |
|---|---|---|---|---|---|---|---|---|
| `stylize.median` | Median / Median (Legacy) | P2 | implemented | whole | — | no | CPU | Median filter; neutral value `radius: 0`. |
| `stylize.dustScratches` | Dust & Scratches | P2 | implemented | whole | — | no | CPU | Median where the pixel differs from its neighbourhood median by more than `threshold`. |
| `stylize.noiseAlpha` | Noise Alpha | P2 | implemented | tiled | — | no | CPU | Noise on the alpha channel; the `animation` kinds advance with `noisePhase`. |
| `stylize.noiseHls` | Noise HLS | P2 | implemented | tiled | — | no | CPU | Noise in HLS, advanced by `noisePhase`. |
| `stylize.noiseHlsAuto` | Noise HLS Auto | P2 | implemented | tiled | — | yes | CPU | Noise HLS animated by time × `noiseAnimationSpeed`. |
| `stylize.removeGrain` | Remove Grain | P2 | implemented | whole | — | no | CPU | Noise reduction from samples of the current frame; `temporalFiltering.enabled` reads neighbouring frames (`Deps::times`). |
| `stylize.brushStrokes` | Brush Strokes | P3 | implemented | tiled | — | no | CPU | After Effects' defaults. |
| `stylize.dropShadow` | Drop Shadow | P1 | implemented | whole | — | no | CPU | In layer space (rotates with the layer; use the layer style `dropShadow` for a comp-space shadow). |
| `stylize.longShadow` | — (flat long shadow) | P1 | implemented | whole | — | no | CPU | Exact sweep of the alpha along the direction (not repeated copies), so the shadow edge is clean at any length. |
| `stylize.mosaic` | Mosaic | P1 | implemented | tiled | — | no | CPU | Pixelation; blocks average in linear light unless `sharpColors`. |
| `stylize.roughenEdges` | Roughen Edges | P1 | implemented | whole | — | no | CPU | Hand-made, printed, torn-paper edges; animated "boil" with `evolution` on twos. |
| `stylize.grain` | Add Grain / Match Grain | P1 | implemented | tiled | — | yes | GPU when the whole stack lowers, else CPU | Film-like grain from **one tileable noise texture per frame**, a function of (seed, frame time quantized by `rate`, `size`): band-limited (not white), one mono field, modulated per channel by `color` and `channelIntensity` (`mono` applies the field as is; `color` reads the one texture at three fixed offsets, so the channels are fully decorrelated), blended in **linear light** with a gain chosen so the visible amount at mid-grey matches `amount` in perceptual terms, scaled by `response` at the pixel's luminance. |
| `stylize.vignette` | — (Lumetri vignette) | P1 | implemented | tiled | — | no | GPU when the whole stack lowers, else CPU | In linear light (darkens like an optical vignette). |
| `stylize.outline` | — (Stroke on alpha) | P1 | implemented | whole | — | no | CPU | Distance-field outline of the layer's alpha: crisp at any width (After Effects needs a shape layer or the Stroke layer style for this). |
| `stylize.halftone` | — (Color Halftone, print looks) | P2 | implemented | tiled | — | no | CPU | Analytic, anti-aliased dots computed per pixel (no texture), so cells stay crisp at any scale and animate smoothly: per plate, the pixel's own tone sets the size of a dot (line, square, diamond, or Euclidean dot) in a `cellSize` grid rotated by the plate's angle, and the pixel is covered where it lies inside that dot, anti-aliased over 1 px or `softness` percent of a cell. |
| `stylize.dither` | — (dither looks) | P2 | implemented | tiled | — | no | CPU | The display-encoded color, after `brightness` and `contrast`, is matched to the nearest palette color in OKLab or encoded sRGB (the first of equal distances), after an ordered threshold (Bayer 2/4/8, blue noise: per pixel, stable in time) or with error diffusion (`floydSteinberg`, `atkinson`, `stucki`: a fixed raster scan over the whole layer, deterministic, but it shimmers when content moves; that is the look). |
| `stylize.glitch` | — (digital glitch) | P2 | implemented | tiled | — | yes | CPU | Seeded glitch events, one per `1 / frequency` seconds slot at a hashed offset inside the slot, each lasting `duration`. |
| `stylize.rgbSplit` | — (RGB split / channel offset) | P2 | implemented | tiled | — | no | CPU | Each channel is read from the layer shifted by its own offset (bilinear); `add` takes the channels as they are, `screen` screens them onto the unshifted layer; the alpha is the union of the three. |
| `stylize.chromatic` | — (chromatic aberration) | P2 | implemented | tiled | — | no | CPU | Lens-like: the red and blue channels are read from the layer displaced along the axis from `center` (`radial`: by `amount · (d / R)^falloff`, *d* the distance from the center and *R* the farthest corner; red outward, blue inward) or along `direction` (`directional`, uniform); `channels: rgb` also moves green by half the blue displacement, so the three fan out in spectral order. |
| `stylize.pixelSort` | — (pixel sorting) | P2 | implemented | whole | other layers | no | CPU | Along rows (`direction` nearer horizontal) or columns of the layer rect, every run of consecutive pixels whose key (read from the display-encoded straight color) lies in `threshold` (and that the `mask` layer passes, where given) is sorted by that key, ascending toward +x / +y or descending, in runs of at most `maxLength` px; a stable sort, so the result is a pure function of the frame. |
| `stylize.scanlines` | — (CRT) | P2 | implemented | tiled | — | no | CPU | `density` dark lines over the layer height, each covering `thickness` percent of its period at `opacity`, anti-aliased by their pixel coverage; a phosphor `mask` (`aperture` grille, `shadow` mask, `slot` mask) attenuates the other two channels per column; `flicker` dims whole frames by a hashed amount; `roll` scrolls the lines at that many periods per second; `curvature` barrel-warps the image; `bloom` adds a blurred copy. |
| `stylize.vhs` | — (VHS) | P2 | implemented | tiled | — | yes | CPU | Rows jitter horizontally by `wobble` px of slow noise, a tracking band of `tracking` percent of the height drifts down the frame with a stronger shift and noise, the bottom 4 % carries head-switching noise, the chroma (the encoded color minus its luma) is averaged over `chromaBleed` px and offset by `colorShift` px, and hashed tape noise of `noise` percent is added to the luma; all scaled by `amount`, the noise and the band functions of (`seed`, frame). |
| `stylize.noise` | Noise | P2 | implemented | tiled | — | yes | GPU when the whole stack lowers, else CPU | Hashed per-pixel noise of `amount` added to the display-encoded straight color (`uniform`, or the sum of two uniforms for `gaussian`), per channel with `color` or the same for every channel; `clip` clamps to [0, 1], otherwise values wrap around (the integer-overflow look). |
| `stylize.findEdges` | Find Edges | P2 | implemented | tiled | — | no | CPU | The Sobel gradient magnitude of the display-encoded luma (reads clamped into the layer rect), dark on white (white on dark with `invert`) at the pixel's alpha, mixed with the original by `blend`. |
| `stylize.emboss` | Emboss / Color Emboss | P2 | implemented | tiled | — | no | CPU | The difference between the layer sampled `relief` px along `direction` and against it (bilinear, clamped to the layer rect), scaled by `contrast`: a grey relief around mid grey, or added to the pixel's own color with `color` (Color Emboss); mixed with the original by `blend`. |
| `stylize.glowEdges` | Glowing Edges / Find Edges + Glow | P2 | implemented | whole | — | no | CPU | The Sobel edge magnitude of the display-encoded luma, spread by a Gaussian of σ = `width` / 2 and scaled by `brightness`, then pushed through `contrast` about mid grey; the edges glow in the layer's own colors (plus a quarter of white, so dark edges still show) on black, at the layer's alpha. |
| `stylize.pixelate` | — | P2 | implemented | tiled | — | no | CPU | The layer rect in cells of `size` px (a square grid, or a pointy-top hexagonal lattice for `hexagon`), each cell the linear-light mean of its pixels, drawn as a square, circle, diamond or hexagon of `size − gap` px with `gapColor` at the cell's alpha between; pixels outside the layer rect pass through. |
| `stylize.scatter` | Scatter | P2 | implemented | tiled | — | no | CPU | Every output pixel reads the layer at a hashed offset of up to `amount` px (nearest pixel) along both axes or one; `randomize` changes the pattern every frame. |
| `stylize.letterbox` | — | P2 | implemented | tiled | — | no | GPU when the whole stack lowers, else CPU | Bars of `color` over the layer rect outside the centered `aspect` frame (top and bottom when the layer is taller than the aspect, left and right when wider), anti-aliased at fractional edges; on an adjustment layer the layer rect is the comp. |
| `stylize.posterizeEdges` | — | P2 | implemented | tiled | — | no | CPU | The display-encoded color quantized to `levels` per channel, with `edgeColor` drawn where the quantized luma level differs from any neighbour within `edgeWidth` px (the eight directions). |
| `stylize.cartoon` | Cartoon | P2 | implemented | whole | — | no | CPU | Bilateral + quantize + edge detect; turns footage into flat illustration. |
| `stylize.texturize` | Texturize | P2 | implemented | tiled | other layers | no | CPU | Paper and canvas textures (with an image asset of the texture). |
| `stylize.ccBlockLoad` | CC Block Load | P2 | implemented | whole | — | no | CPU | Progressive block-by-block image loading. |
| `stylize.ccBurnFilm` | CC Burn Film | P2 | implemented | tiled | — | no | CPU | Film burning away from `center` as `burn` grows. |
| `stylize.ccGlass` | CC Glass | P2 | implemented | whole | other layers | no | CPU | Bump-mapped glass surface lit by the effect light; refracts by `displacement`. |
| `stylize.ccHexTile` | CC HexTile | P2 | implemented | tiled | — | no | CPU | Hexagonal tiling of the layer. |
| `stylize.ccMrSmoothie` | CC Mr. Smoothie | P2 | implemented | whole | other layers | no | CPU | Recolours by a colour map sampled from the image between `sampleA` and `sampleB`, indexed by the flow layer's `property`. |
| `stylize.ccPlastic` | CC Plastic | P2 | implemented | whole | other layers | no | CPU | Bump-mapped plastic surface lit by the effect light. |
| `stylize.ccRepeTile` | CC RepeTile | P2 | implemented | tiled | — | no | CPU | Grows the layer by tiling it outward (`output_bounds` grows by the four expands). |
| `stylize.ccThresholdRgb` | CC Threshold RGB | P2 | implemented | tiled | — | no | CPU | Per-channel threshold (`color.threshold` is the luma one). |
| `stylize.ccVignette` | CC Vignette | P2 | implemented | tiled | — | no | CPU | Lens-model vignette (`stylize.vignette` is the Lumetri one). |
| `stylize.ascii` | — | P2 | implemented | tiled | — | no | CPU | Text-art look; glyphs rasterized via the text engine. |
| `stylize.datamosh` | — (datamosh) | P4 | not implemented (P4: `effect.unavailable`) | — | — | no | CPU | Needs codec motion vectors; uses an optical-flow field from the decoder path. |
| `stylize.motionTrails` | — (echo-based trails) | — | not implemented (not provided: `effect.unavailable`) | — | — | no | CPU | Use `time.echo`. |

## Keying & matte

Usage: [16-keying-matte.md](16-keying-matte.md). Parameters: [91-catalogue-keying.md](91-catalogue-keying.md).

| Type | After Effects | Phase | Status | Tiling | Reads | Time | Device | Note |
|---|---|---|---|---|---|---|---|---|
| `key.difference` | Difference Matte | P3 | implemented | whole | other layers | no | CPU | Implemented: the largest difference of the display-encoded straight R, G, B and alpha against the other layer, centred on this one; `blurBeforeDifference` is a Gaussian of σ = half the length on both before comparing; a null or missing `layer` passes the layer through. |
| `matte.refine` | Refine Soft Matte | P3 | implemented | whole | — | no | CPU | Guided-filter refinement against the layer's color; for hair edges on AI or keyed footage. |
| `key.unmult` | Unmult (AE 26.0) | P1 | implemented | tiled | — | no | GPU when the whole stack lowers, else CPU | Derives alpha from brightness and divides it out: drop fire, light leaks, flares shot on black over anything. |
| `matte.simpleChoker` | Simple Choker | P1 | implemented | whole | — | no | CPU | Distance-field based (fractional, smooth when animated); reads `\|choke\|` + 2 px beyond an output tile. |
| `matte.set` | Set Matte | P1 | implemented | tiled | other layers | no | CPU | Takes alpha from another layer inside the effect stack (useful when a track matte is not flexible enough, e.g. a matte that must apply before a glow). |
| `key.chroma` | Keylight (1.2) class / Key Light | P2 | implemented | whole | — | no | CPU | A color-difference keyer with despill, for AI-generated footage on green and product shoots. |
| `key.color` | Color Key | P2 | implemented | whole | — | no | GPU when the whole stack lowers, else CPU | Pixels whose display-encoded color is within `tolerance` (percent of full scale, per channel) of `color` become transparent; the hard matte is thinned by `edgeThin` px (negative grows) and feathered by a Gaussian of σ = `edgeFeather` / 2. |
| `key.luma` | Luma Key | P2 | implemented | whole | — | no | GPU when the whole stack lowers, else CPU | Keys pixels by their display-encoded luma against `threshold` (percent of full scale): brighter or darker than it, with a `tolerance`-wide ramp, or within / outside a band of `tolerance` half-width around it; then thinned and feathered as `key.color`. |
| `key.linearColor` | Linear Color Key | P2 | implemented | tiled | — | no | GPU when the whole stack lowers, else CPU | The distance of every pixel's straight linear color to `color` in RGB, hue or chroma (normalized to [0, 1]) is mapped through a ramp from `tolerance` over `softness` to a matte; `keepColors` inverts it. |
| `matte.spill` | Advanced Spill Suppressor / Spill Suppressor | P2 | implemented | tiled | — | no | GPU when the whole stack lowers, else CPU | On straight linear color, per pixel: `standard` limits the key color's primary channel to the larger of the other two by `suppression`; `ultra` limits it to the mean of the other two half-way (the spill range), only for hues within a quarter turn of the key, puts the removed spill back as neutral light (so brightness is kept) and desaturates what was suppressed. |
| `matte.choker` | Matte Choker | P2 | implemented | whole | — | no | CPU | `iterations` times two stages, each a Gaussian blur of the alpha by its geometric softness (σ = softness / 2) followed by a threshold ramp centered on 0.5 + choke / 255 · 0.5 (positive chokes) of width `grayLevelSoftness`; the straight color is kept under the new alpha. |
| `matte.alphaLevels` | — | P2 | implemented | tiled | — | no | GPU when the whole stack lowers, else CPU | Levels on alpha only (convenience): α′ = ((α − `inBlack`) / (`inWhite` − `inBlack`))^(1/γ), clamped; the straight color is kept. |
| `key.extract` | Extract | P2 | implemented | tiled | — | no | CPU | Keys by a channel's range. |
| `key.colorRange` | Color Range | P2 | implemented | tiled | — | no | CPU | Keys a box in the chosen colour space. |
| `key.colorDifference` | Color Difference Key | P2 | implemented | tiled | — | no | CPU | Two partial mattes (A and B) combined, the classic blue-screen matte. |
| `key.screen` | Screen Key | P2 | implemented | whole | — | no | CPU | Screen-difference keyer, the small sibling of `key.chroma`. |
| `key.ccWireRemoval` | CC Simple Wire Removal | P2 | implemented | tiled | — | no | CPU | Paints out the line between the two points; `frameOffset` reads another frame (`Deps::times`). |
| `matte.keyCleaner` | Key Cleaner | P2 | implemented | whole | — | no | CPU | Recovers edge detail after a keyer; `reduceChatter` reads neighbouring frames (`Deps::times`). |
| `matte.refineHard` | Refine Hard Matte | P2 | implemented | whole | — | no | CPU | The hard-edged sibling of `matte.refine`; `reduceChatter` and `useMotionBlur` read neighbouring frames (`Deps::times`). |
| `key.innerOuter` | Inner/Outer Key | P2 | implemented | whole | mask paths | no | CPU | Matte from an inner and an outer mask with colour-based edge estimation and decontamination; needs mask paths as parameters, like `generate.stroke`. |

## Time

Usage: [17-time.md](17-time.md). Parameters: [91-catalogue-time.md](91-catalogue-time.md).

| Type | After Effects | Phase | Status | Tiling | Reads | Time | Device | Note |
|---|---|---|---|---|---|---|---|---|
| `time.difference` | Time Difference | P3 | implemented | tiled | other layers | no | CPU | Implemented: a `target` layer is read at the frame's own time (7.6); `timeOffset` applies only to the layer itself (`target` null); a time or layer the renderer does not supply reads as transparent. |
| `time.posterize` | Posterize Time | P1 | implemented | tiled | — | no | CPU | Quantizes the time the layer's **content** is evaluated at (source, masks, and the effects above it in the stack, with their keyframes), through the upstream-time override of [7.5](#75-time-randomness-and-determinism). |
| `time.echo` | Echo | P2 | implemented | tiled | other times | no | CPU | Motion trails: the layer (after its earlier effects) at `t + i · echoTime` for *i* = 1 … `count`, declared as `Deps::times` and supplied by the renderer as `Inputs::times` (a declared time the renderer does not supply reads as transparent), combined with the frame itself (*i* = 0) in order of *i* by `operator`, each weighted `startingIntensity · decay^i`: `add` sums, `maximum` / `minimum` take the extremes per channel, `screen` screens, `compositeInBack` puts every later echo behind what is there, `compositeInFront` on top, `blend` averages. |
| `time.strobe` | Strobe Light | P2 | implemented | tiled | — | yes | CPU | Every `period` seconds the layer flashes for `duration` seconds (and, with `randomStrobe` percent, hashed whole periods flash at random): `operatesOnColorOnly` combines `color` with the layer's display-encoded color by `operator`, mixed back by `blend`; `makesLayerTransparent` scales the alpha by `blend`. |
| `time.displacement` | Time Displacement | P2 | implemented | tiled | other layers, other times | no | CPU | Slit-scan and time-warp looks. |
| `time.frameBlend` | Frame Blending (as an effect) | P2 | implemented | tiled | — | no | CPU | Same as the layer's `frameBlend` ([spec 2 §2.10](02-time-and-animation.md#210-layer-timing)) but placeable inside the stack: between two comp frames of the layer, `mix` crossfades the layer (source, masks and the effects above) at the frame before and after, `flow` interpolates the two along their optical flow ([spec 10 §10.3.3](10-media-and-audio.md#1033-frame-blending): the same flow as the layer-level `flow`, estimated on the whole frame pair, cached per layer and effect). |
| `time.ccWideTime` | CC Wide Time | P2 | implemented | tiled | other times | no | CPU | Averages the layer over the surrounding frames (declares `Deps::times` like `time.echo`). |

## Transition

Usage: [18-transition.md](18-transition.md). Parameters: [91-catalogue-transition.md](91-catalogue-transition.md).

| Type | After Effects | Phase | Status | Tiling | Reads | Time | Device | Note |
|---|---|---|---|---|---|---|---|---|
| `transition.linearWipe` | Linear Wipe | P1 | implemented | tiled | — | no | CPU |  |
| `transition.radialWipe` | Radial Wipe | P1 | implemented | tiled | — | no | CPU | Clock wipes, pie-chart reveals. |
| `transition.venetianBlinds` | Venetian Blinds | P2 | implemented | tiled | — | no | CPU | Slats of `width` px perpendicular to `direction`, each closing over `completion` percent of its width, with a `feather` px soft edge. |
| `transition.gradientWipe` | Gradient Wipe | P2 | implemented | tiled | other layers | no | CPU | Hides the pixels whose gradient luma (display-encoded, of the `gradient` layer placed by `placement`, or of the layer itself) is below `completion`, with a `softness` ramp; `invert` reverses the order. |
| `transition.blockDissolve` | Block Dissolve | P2 | implemented | tiled | — | no | CPU | Blocks of `blockWidth` × `blockHeight` px (anchored at the layer origin) vanish in a hashed order as `completion` grows; `softEdges` anti-aliases block edges that fall between pixels (4 × 4 sub-samples), `feather` blurs the mask (Gaussian). |
| `transition.iris` | Iris Wipe / CC Shape Wipe | P2 | implemented | tiled | other layers | no | CPU | A `shape` (circle, square, diamond, star or regular polygon of `points`, heart, or the alpha of `shapeLayer`) about `center`, rotated by `rotation`, that covers the whole layer at `completion` 0 and shrinks to nothing at 100, with a `feather` px edge; pixels outside it are hidden. |
| `transition.ccGridWipe` | CC Grid Wipe | P2 | implemented | tiled | — | no | CPU | Grid of tiles closing from `center`. |
| `transition.ccRadialScaleWipe` | CC Radial ScaleWipe | P2 | implemented | tiled | — | no | CPU | Radial scale-away from `center`. |
| `transition.ccScaleWipe` | CC Scale Wipe | P2 | implemented | tiled | — | no | CPU | Stretches the layer away from `center` along `direction` (no `completion`: animate `stretch`). |
| `transition.ccLightWipe` | CC Light Wipe | P2 | implemented | tiled | — | no | CPU | A glowing edge of `color` that eats the layer from `center`. |
| `transition.ccJaws` | CC Jaws | P2 | implemented | tiled | — | no | CPU | Two jagged halves opening from `center`. |
| `transition.ccLineSweep` | CC Line Sweep | P2 | implemented | tiled | — | no | CPU | Staggered slanted lines sweeping across. |
| `transition.ccImageWipe` | CC Image Wipe | P2 | implemented | tiled | other layers | no | CPU | Wipe ordered by a layer's `property` (`transition.gradientWipe` is the luma-only After Effects one). |
| `transition.ccGlassWipe` | CC Glass Wipe | P2 | implemented | whole | other layers | no | CPU | Gradient-driven wipe that refracts the edge; needs a second layer to reveal ([7.6](#76-reading-other-layers)). |
| `transition.ccWarpoMatic` | CC WarpoMatic | P2 | implemented | whole | other layers | no | CPU | Warps both layers by the reactor layer while cross-fading; needs a second layer ([7.6](#76-reading-other-layers)). |
| `transition.ccTwister` | CC Twister | P2 | implemented | tiled | other layers | no | CPU | Ribbon twist about `axis` that reveals `backside`. |
| `transition.pageTurn` | CC Page Turn | P2 | implemented | tiled | other layers | no | CPU | Page curl from `fold`. |
| `transition.cardWipe` | Card Wipe | P2 | implemented | whole | other layers | no | CPU | 3D card flip of a grid, drawn by the effect's own per-card homographies (EffectCraft's `card3d`: camera system, lighting, material), not the comp's 3D renderer. |

## Perspective

Usage: [19-perspective.md](19-perspective.md). Parameters: [91-catalogue-perspective.md](91-catalogue-perspective.md).

| Type | After Effects | Phase | Status | Tiling | Reads | Time | Device | Note |
|---|---|---|---|---|---|---|---|---|
| `perspective.sphere` | CC Sphere | P3 | implemented | tiled | other layers | no | CPU | Wraps the layer onto a sphere (planets, globes, spinning logo balls); ray-cast per pixel with antialiasing. |
| `perspective.cylinder` | CC Cylinder | P3 | implemented | tiled | other layers | no | CPU | Implemented: ray-cast against the rotated cylinder, seen orthographically; `position`'s z does not show; the cylinder is open (no end caps). |
| `perspective.bevelAlpha` | Bevel Alpha | P2 | implemented | whole | — | no | CPU | Signed-distance-based bevel (smooth on any shape). |
| `perspective.bevelEdges` | Bevel Edges | P2 | implemented | tiled | — | no | CPU |  |
| `perspective.dropShadow3d` | Radial Shadow / Drop Shadow in 3D | P2 | implemented | whole | — | no | CPU |  |
| `perspective.ccEnvironment` | CC Environment | P2 | implemented | whole | other layers | no | CPU | Reflection-maps the environment layer onto the layer's luminance/alpha relief (EffectCraft's construction; no comp camera). |
| `perspective.3dGlasses` | 3D Glasses | P4 | not implemented (P4: `effect.unavailable`) | — | — | no | CPU | Anaglyph; kept for parity only. |

## Utility and expression controls

Usage: [20-utility-controls.md](20-utility-controls.md). Parameters: [91-catalogue-utility.md](91-catalogue-utility.md).

| Type | After Effects | Phase | Status | Tiling | Reads | Time | Device | Note |
|---|---|---|---|---|---|---|---|---|
| `control.slider` | Slider Control | P1 | implemented | tiled | — | no | — (no pixels) |  |
| `control.angle` | Angle Control | P1 | implemented | tiled | — | no | — (no pixels) |  |
| `control.point` | Point Control | P1 | implemented | tiled | — | no | — (no pixels) |  |
| `control.point3d` | 3D Point Control | P1 | implemented | tiled | — | no | — (no pixels) |  |
| `control.color` | Color Control | P1 | implemented | tiled | — | no | — (no pixels) |  |
| `control.checkbox` | Checkbox Control | P1 | implemented | tiled | — | no | — (no pixels) |  |
| `control.layer` | Layer Control | P1 | implemented | tiled | other layers | no | — (no pixels) | Not animatable. |
| `control.dropdown` | Dropdown Menu Control | P1 | implemented | tiled | — | no | — (no pixels) |  |
| `utility.growBounds` | Grow Bounds | P1 | implemented | tiled | — | no | CPU | Rarely needed, since bounds grow automatically ([7.4](#74-bounds-and-region-of-interest)); kept so imported After Effects projects map one to one. |
| `utility.applyLut` | Apply Color LUT | P1 | implemented | tiled | — | no | GPU when the whole stack lowers, else CPU | Alias of `color.lut`. |
| `utility.removeColorMatting` | Remove Color Matting | P1 | implemented | tiled | — | no | CPU | Premultiplied-against-a-color footage cleanup. |
| `utility.hdrCompander` | HDR Compander | P2 | implemented | tiled | — | no | CPU |  |
| `utility.shiftChannels` | Shift Channels | P2 | implemented | tiled | — | no | CPU |  |
| `utility.channelCombiner` | Channel Combiner | P2 | implemented | tiled | other layers | no | CPU | Enum lists pinned to After Effects' at P2. |
| `utility.minMax` | Minimax | P2 | implemented | whole | — | no | CPU |  |
| `utility.setChannels` | Set Channels | P2 | implemented | tiled | other layers | no | CPU |  |
| `utility.colorProfile` | Color Profile Converter | P2 | implemented | tiled | — | no | CPU | Explicit space conversion inside a stack ([spec 13](13-color-and-output.md)). |
| `utility.ccOverbrights` | CC Overbrights | P2 | implemented | tiled | — | no | CPU | Paints pixels above 1.0 in `highlightColor` (a diagnostic; `motion.check` is the usual tool). |
| `utility.hdrHighlightCompression` | HDR Highlight Compression | P2 | implemented | tiled | — | no | CPU | Rolls values above 1.0 into range by `amount` (`utility.hdrCompander` is the invertible pair). |
| `utility.arithmetic` | Arithmetic | P2 | implemented | tiled | — | no | GPU when the whole stack lowers, else CPU | Per-channel arithmetic with a constant, on display-encoded 0–255 values. |
| `utility.blend` | Blend | P2 | implemented | tiled | other layers | no | CPU | Blends with another layer by one of five legacy modes (for anything else use the layer's `blend`, [spec 6](06-masks-mattes-blending.md)). |
| `utility.calculations` | Calculations | P2 | implemented | tiled | other layers | no | CPU | Photoshop Calculations: a channel of this layer blended with a channel of another. |
| `utility.ccComposite` | CC Composite | P2 | implemented | tiled | other layers | no | CPU | Composites the layer's unprocessed source back over the effect chain so far (the one effect that reads the chain's input). |
| `utility.compoundArithmetic` | Compound Arithmetic | P2 | implemented | tiled | other layers | no | CPU | Layer-to-layer arithmetic. |
| `utility.solidComposite` | Solid Composite | P2 | implemented | tiled | — | no | GPU when the whole stack lowers, else CPU | Composites the layer over a solid colour. |
| `utility.shader` | — (custom shader) | P4 | implemented | whole | — | yes | GPU only | GPU-only (renders on the GPU pool; on a CPU box, or in a job the backend decision puts on the CPU, `effect.requires_gpu` and the layer passes through unshaded; `motion.check` says so in advance as `estimate.requiresGpu`). |
<!-- gen:catalogue-index:end -->
