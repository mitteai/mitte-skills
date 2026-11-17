# 09. Masks, track mattes, preserve transparency, adjustment layers, collapse, the 38 blend modes, the no-clamp rule

Scope: spec 6 in full. Generated tables: `Mask`, `MaskMode`, `MaskShape`, `MaskMotionBlur`, `FeatherFalloff`, `VariableFeatherPoint`, `FeatherSide`, `Matte`, `MatteMode`, `BlendMode`, `BlendingSpace` in `92-schema-types-*.md`.

## 0. Conventions

Pixels are premultiplied RGBA in the comp's working space, scene-linear f32. Colours may exceed 1 (HDR); alpha is in [0, 1]. Unless a mode says otherwise, compositing is the W3C model (also After Effects'): `αr = αs + αb − αs·αb`, `Cr = (1 − αb)·Cs + (1 − αs)·Cb + αs·αb·B(b, s)` with straight colours `s = Cs/αs`, `b = Cb/αb` and the mode's blend function `B`. `B(b, s) = s` is ordinary "over".

**The no-clamp rule.** Values above 1 survive every composite: *unbounded* modes use them as they are (normal, dissolve, dancingDissolve, darken, lighten, multiply, add, linearDodge, linearBurn, subtract, divide, difference, classicDifference, exclusion, darkerColor, lighterColor, hue, saturation, color, luminosity, the stencil/silhouette modes, alphaAdd, luminescentPremul); *range-limited* modes clamp `b` and `s` to [0, 1] first (screen, overlay, softLight, hardLight, linearLight, vividLight, pinLight, hardMix, colorBurn, colorDodge, classicColorBurn, classicColorDodge), and lint warns when one of those is used on a layer whose values exceed 1 (`lint.blend_clamps_hdr`; use `add` or `screen` on glows, which `light.glow` does internally). Only the output stage clips or tone-maps ([14](14-color-and-output.md) §4). With `color.blending: "display"` every blend, opacity mix, feather and motion-blur accumulation happens on display-encoded values (After Effects' non-linearized default).

## 1. Masks

A closed path in the layer's own space that limits where the layer shows. Masks combine in list order into one coverage map that multiplies the layer's alpha **before** its effects (effects that want the unmasked layer use their own mask parameters).

```jsonc
"masks": [
  { "id": "window", "mode": "add", "path": { "v": [[0,0],[800,0],[800,450],[0,450]], "closed": true }, "feather": 24, "expansion": 0, "opacity": 100 },
  { "id": "hole", "mode": "subtract", "shape": "ellipse", "center": [400, 225], "size": [160, 160], "feather": { "keys": [ { "t": 0, "v": 0 }, { "t": 1, "v": 40 } ] } },
  { "id": "soft", "mode": "intersect", "path": "M0 0 L800 0 L800 450 L0 450 Z", "feather": [60, 10], "featherFalloff": "linear", "inverted": false, "motionBlur": "layer", "rotobezier": false }
]
```

| Field | Type | Default | Anim. | Notes |
|---|---|---|---|---|
| `id` | id | `_mask<n>` | — | name masks you reference (text on a path, effects) |
| `mode` | enum | `add` | no | §1.2 |
| `path` | path value or SVG string | — | yes | layer space; an open path is closed with a straight segment for coverage (a `none`-mode path stays open for effects and text on a path); exactly one of `path` / `shape` |
| `shape` | enum | — | — | authored primitive (§1.1) |
| `inverted` | boolean | `false` | no | use `1 − coverage` before combining |
| `feather` | number or `[fx, fy]` | `0` | yes | px: the width of the soft band from 0 % to 100 % coverage, centred on the expanded edge; `[fx, fy]` feathers per axis |
| `featherFalloff` | `smooth` \| `linear` | `smooth` | no | Gaussian band (σ = feather/4.65) or a straight ramp |
| `expansion` | number | `0` | yes | px: grows (+) or shrinks (−) the mask by offsetting its edge, before feathering |
| `opacity` | percent | `100` | yes | scales this mask's coverage |
| `motionBlur` | `layer` \| `on` \| `off` | `layer` | no | whether an animating path is motion-blurred: with the layer's switch, always, never |
| `rotobezier` | boolean | `false` | no | tangents computed (Catmull-Rom through the vertices); `in`/`out` ignored |
| `variableFeather` | list | none | yes | **not built** (P3): `[{ "segment", "t", "radius", "side": outer \| inner \| both }]` |

### 1.1 Shape masks (authored)

| `shape` | Fields (defaults) |
|---|---|
| `rect` | `center` (the layer centre), `size` (the layer size) |
| `roundedRect` | `center`, `size`, `radius` (16) |
| `ellipse` | `center`, `size` |
| `polygon` | `center`, `radius` (100), `points` (6), `rotation` (0), `roundness` (0) |
| `star` | `center`, `outerRadius` (100), `innerRadius` (50), `points` (5), `rotation` (0), `outerRoundness` (0), `innerRoundness` (0) |

Numeric fields accept percentages of the layer's content bounds (`"center": ["50%", "50%"]`) and animate (one path key per distinct key time; key times take any time form, frames such as `"30f"` included). The generated paths use the same vertex construction as the shape primitives, so a rect mask and a rect shape morph identically.

### 1.2 Mask modes

Each mask gives a coverage `m` in [0, 1] (analytic coverage of the path at the layer's final raster resolution, expanded, feathered, × opacity/100, inverted if asked). Masks combine in list order into `A`:

| `mode` | Combine | Notes |
|---|---|---|
| `none` | ignored for coverage | the path stays available to effects and text on a path |
| `add` | `A = min(1, A + m)` | After Effects' arithmetic: two overlapping 50 % masks give 100 % |
| `subtract` | `A = max(0, A − m)` | |
| `intersect` | `A = min(A, m)` | |
| `lighten` | `A = max(A, m)` | |
| `darken` | `A = min(A, m)` | |
| `difference` | `A = |A − m|` | |

Initial value: `A` starts at 0 when the first active mask is `add`, `lighten` or `difference`; at 1 when it is `subtract`, `intersect` or `darken` (a lone subtract mask cuts a hole in the full layer). No active masks: `A = 1`. The layer's alpha and premultiplied colour are multiplied by `A`. Coverage is computed in the space the layer is rasterized in (vector layers: at output resolution under their final transform), so feathers stay exact at any scale; an animating mask with motion blur is accumulated over the shutter samples. Masks on a `null`: `layer.field_not_allowed`.

## 2. Track mattes

```jsonc
{ "id": "footage", "type": "video", "asset": "hero", "matte": { "layer": "titleShape", "mode": "alpha" } },
{ "id": "titleShape", "type": "text", "text": "OCEAN", "style": { "size": 420, "weight": 900 } }
```

| Field | Default | Notes |
|---|---|---|
| `layer` | required | the matte source: **any** layer of the same comp (above or below, adjacent or not: After Effects' 2023+ model); not itself (`layer.matte_self`) |
| `mode` | `alpha` | `alpha` (α), `alphaInverted` (1 − α), `luma` (premultiplied luminance, clamped to [0, 1]), `lumaInverted` |

The source is evaluated at the same time through its full pipeline (source, masks, effects, styles, transform, opacity, its own matte) into comp space; outside its `[in, out)` the matte is empty (an inverted matte then shows fully). The target's premultiplied colour and alpha are multiplied by the matte value after its opacity and before its blend. **The source is hidden by default** (`visible: false` unless the document sets `visible: true`; the info `lint.matte_source_hidden` names it). Many targets may share one source (rendered once). Chains are allowed (depth ≤ 8, `matte.depth`); cycles are `matte.cycle`. A `comp` layer as source is a precomp matte (one animated group mattes several layers). The source's blend mode is ignored for its matte role. A 3D source is seen through the camera; a 3D target with a matte renders on its own and composites through the 2D path.

## 3. Preserve transparency

`"preserveTransparency": true` (After Effects' "T" switch): the layer paints only where the backdrop already has alpha, leaving the backdrop's alpha unchanged (`k = αb`; `Cr = (1 − αs·k)·Cb + αs·k·B(b, s)`; `αr = αb`). A gradient or texture that should show only on the text below it, without a matte.

## 4. Adjustment layers

An `adjustment` layer has no pixels: its `effects` apply to the composite `C` of every layer below it in the same comp (effects see the full backdrop, so blurs pull in surrounding pixels). With coverage `k` = its rectangle (`size`, transformed) × its masks × `opacity/100` × its matte: `result = C + k·(E(C) − C)` for `normal`, or `blend(C, E(C), mode)·k + C·(1 − k)` for any other mode (the adjusted backdrop blended as a source over the unchanged backdrop). A full-comp adjustment at opacity 100 with `normal` is exactly `E(C)`. Its `in`/`out` limit when it applies; its transform moves its rectangle and masks, not the backdrop; no effects = no change; inside a nested comp it affects only that comp's layers below it; a 3D adjustment projects its rectangle through the camera but still adjusts the flat 2D composite.

## 5. Collapse transformations

A `comp` layer normally renders its nested comp to an intermediate image at the nested size and transforms it like footage. With `collapse: true` (After Effects' collapse transformations; the default for component instances) the nested layers render **directly into the parent**, the comp layer's transform composed onto each nested layer's world transform:

- vector layers inside stay sharp at any scale; content outside the nested rectangle is **not** clipped; nested 3D layers join the parent's 3D run (the parent's camera and lights); the nested `background` is not drawn; motion blur uses the parent's shutter;
- blend modes pass through to the parent's layers below the comp layer, provided the comp layer has no masks, effects, styles, matte, `timeRemap`, a `hold` other than `none`, and blend `normal`; otherwise the nested layers are composited together first (still unclipped, at the parent's resolution, an isolated 3D run) and the result is masked, effected and blended as one layer;
- the comp layer's `opacity` multiplies each nested layer's opacity when modes pass through, the group's alpha otherwise.

## 6. Blend modes

`blend` on a layer (also on shape groups and paints) selects one of After Effects' 38 modes, all rendered. Names are After Effects' in lowerCamelCase.

| Group | `blend` | Formula (`B(b, s)` unless stated) |
|---|---|---|
| normal | `normal` | `s` (source-over) |
| | `dissolve` | per pixel either fully the source or the backdrop: `hash(seed, x, y) < αs`; the seed derives from the layer id, constant over time |
| | `dancingDissolve` | as `dissolve` with the frame index in the hash (the pattern changes every frame) |
| darken | `darken` | `min(b, s)` per channel |
| | `multiply` | `b·s` |
| | `colorBurn` | `1` if `b ≥ 1`; `0` if `s ≤ 0`; else `1 − min(1, (1 − b)/s)` (range-limited) |
| | `classicColorBurn` | the legacy burn on premultiplied values: `clamp(Cb·(1 − αs) + Cs·(1 − αb) + αs·αb − min(αs·αb, (αb − Cb)·αs·αs / max(Cs, ε)), 0, αr)`; compatibility only |
| | `linearBurn` | `b + s − 1`, floored at 0, unbounded above |
| | `darkerColor` | `s` if `Y(s) < Y(b)` else `b` (whole colour) |
| lighten | `add` | not a `B` function: `Cr = Cb + Cs`, `αr = αs + αb − αs·αb`; unbounded, keeps HDR energy: the mode for glows, light leaks, particles |
| | `lighten` | `max(b, s)` per channel |
| | `screen` | `b + s − b·s` (range-limited) |
| | `colorDodge` | `0` if `b ≤ 0`; `1` if `s ≥ 1`; else `min(1, b/(1 − s))` (range-limited) |
| | `classicColorDodge` | legacy dodge on premultiplied values: `clamp(Cb·(1 − αs) + Cs·(1 − αb) + min(αs·αb, Cb·αs·αs / max(αs − Cs, ε)), 0, αr)`; compatibility only |
| | `linearDodge` | `b + s` as a `B` function (differs from `add` only on semi-transparent pixels, as in After Effects) |
| | `lighterColor` | `s` if `Y(s) > Y(b)` else `b` |
| contrast (all range-limited) | `overlay` | `hardLight(s, b)`: `2·b·s` if `b ≤ 0.5`, else `1 − 2·(1 − b)·(1 − s)` |
| | `softLight` | W3C: `b − (1 − 2s)·b·(1 − b)` if `s ≤ 0.5`; else `b + (2s − 1)·(D(b) − b)`, `D(b) = ((16b − 12)·b + 4)·b` if `b ≤ 0.25` else `√b` |
| | `hardLight` | `2·b·s` if `s ≤ 0.5`, else `screen(b, 2s − 1)` |
| | `linearLight` | `clamp(b + 2s − 1, 0, 1)` |
| | `vividLight` | `colorBurn(b, 2s)` if `s ≤ 0.5`, else `colorDodge(b, 2s − 1)` |
| | `pinLight` | `min(b, 2s)` if `s ≤ 0.5`, else `max(b, 2s − 1)` |
| | `hardMix` | `1` if `b + s ≥ 1`, else `0`, per channel |
| inversion | `difference` | `\|b − s\|` |
| | `classicDifference` | `Cr = \|Cb − Cs\|` on premultiplied values |
| | `exclusion` | `b + s − 2·b·s` |
| | `subtract` | `max(0, b − s)` |
| | `divide` | `b/s` for `s > 0`; for `s ≤ 0`: `0` if `b ≤ 0`, else 65504 |
| component (non-separable, W3C helpers with the working space's luminance weights) | `hue` | `SetLum(SetSat(s, Sat(b)), Lum(b))` |
| | `saturation` | `SetLum(SetSat(b, Sat(s)), Lum(b))` |
| | `color` | `SetLum(s, Lum(b))` |
| | `luminosity` | `SetLum(b, Lum(s))` |
| matte / alpha | `stencilAlpha` | `Cr = Cb·αs`, `αr = αb·αs`: the layer's alpha cuts out everything below |
| | `stencilLuma` | `k = clamp(Y(Cs), 0, 1)`; `Cr = Cb·k`, `αr = αb·k` |
| | `silhouetteAlpha` | `Cr = Cb·(1 − αs)`, `αr = αb·(1 − αs)`: punches a hole through everything below |
| | `silhouetteLuma` | `k = clamp(Y(Cs), 0, 1)`; `Cr = Cb·(1 − k)`, `αr = αb·(1 − k)` |
| | `alphaAdd` | `Cr = Cs + Cb`, `αr = min(1, αs + αb)`: joins complementary alpha edges without a seam |
| | `luminescentPremul` | `Cr = Cs + (1 − αs)·Cb`, `αr = αs + αb − αs·αb` without clamping `Cs` to `αs`: light rendered over black with a computed alpha adds instead of clipping |

`Y` is the working space's luminance (Rec.709 weights `0.2126, 0.7152, 0.0722`; ACEScg its own). A stencil/silhouette layer is never skipped at opacity 0. Lottie carries 18 modes; the rest export as `normal` with `convert.lottie_blend`.

## 7. Order of operations

The compositor walks the layers bottom to top with a running backdrop (starting as the comp `background`). For each enabled, visible layer in its span: an adjustment layer applies §4; otherwise source → masks → effects (over the layer's raster rect, clipped to what reaches the comp) → style elements → transform into comp space with motion-blur samples → × opacity → × matte → blend (below-layer style elements, the layer with its mode or preserve-transparency rule, above-layer style elements). A run of consecutive 3D layers is one unit ([10](10-3d.md) §7); collapsed comp layers expand in place. The result is the output (root comp) or the source of a comp layer.

## 8. Examples

`examples/09-masks-mattes-blending.json`: every mask mode and every shape mask with percent fields, feather per axis and `featherFalloff`, `expansion`, `inverted`, `rotobezier`, mask `motionBlur`; alpha and luma mattes (one source shared by two targets, an inverted one, a chain, a comp as a matte, a source kept visible); `preserveTransparency`; an adjustment layer with a mask and a non-normal blend; a collapsed comp whose blend modes pass through; and one solid per blend mode over a gradient. Checks with 0 errors; the infos `lint.matte_source_hidden` are the expected result of the hidden-by-default rule.
