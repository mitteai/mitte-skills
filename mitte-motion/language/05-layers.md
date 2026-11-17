# 05. Layers: every type, every common field, the transform, placement, safe areas, styles, auto-orient, type-specific fields

Scope: spec 3 (except transitions, which are [06-transitions-and-scenes.md](06-transitions-and-scenes.md)), spec 2 §2.10 timing fields, the media layer fields of spec 10 §10.2–10.3 and 10.6 (details in [11-media-and-audio.md](11-media-and-audio.md)). Shapes: [07](07-shapes.md). Text: [08](08-text.md). Masks, mattes, blending: [09](09-masks-mattes-blending.md). Cameras and lights: [10](10-3d.md). Components, repeat, slot: [13](13-components-themes-data.md). Generated tables: `Layer`, `LayerType`, `Transform`, `Origin`, `OriginName`, `Align`, `AlignX`, `AlignY`, `Safe`, `SafeObject`, `SafeBox`, `SafePreset`, `AutoOrient`, `Sampling`, `Quality`, `LayerStyles`, `ShadowStyle`, `GlowStyle`, `BevelStyle`, `SatinStyle`, `ColorOverlayStyle`, `GradientOverlayStyle`, `StrokeStyle`, `HoldMode`, `FrameBlend`, `LoopMode`, `Fit`, `FitMode`, `Channels`, `Duck`, `Fade`, `FadeObject`, `FadeCurve` in `92-schema-types-*.md`.

## 1. Layer types

| `type` | Draws | After Effects | Status (engine 0.1.48) |
|---|---|---|---|
| `solid` | a rectangle of one colour | Solid | rendered |
| `shape` | vector shapes: fills, strokes, operators | Shape layer | rendered |
| `text` | shaped, laid-out, animatable text | Text layer | rendered |
| `image` | a still image or SVG asset | Footage (still) | rendered |
| `video` | a video, image sequence or animated image asset | Footage (movie) | rendered |
| `audio` | sound only, nothing drawn | Footage (audio) | mixed |
| `comp` | another comp of the document (or an imported Lottie) | Precomp | rendered |
| `null` | nothing; a transform others parent to | Null object | rendered |
| `adjustment` | its effects on everything below it | Adjustment layer | rendered |
| `camera` | the viewpoint for 3D layers | Camera | rendered (camera + DOF) |
| `light` | lighting for 3D layers | Light | rendered (`parallel`, `spot`, `point`, `ambient`; `environment` ignored with an info) |
| `particles` | a particle system (spec 9) | Particular | rendered (sprites, lines, Form; the `model` render mode is not built: `render.unsupported` skips that system); see [effects/40](../effects/40-particles-layer-emitters.md) |
| `model` | a glTF model | Advanced 3D | never rendered (`3d.advanced_not_built`; interchange only) |
| `component` | an instance of a component | MOGRT instance | authored → a collapsed `comp` layer |
| `repeat` | N copies of a template layer | duplicated layers | authored → N layers |
| `slot` | inside a component definition: where the instance's layers go | — | authored → a comp layer |

There is no `html` layer: web content enters as rendered video, SVG as shapes or vector footage, Lottie as comps.

## 2. Common fields

```jsonc
{ "id": "title", "name": "Title", "type": "text",
  "in": 0.5, "out": 6, "dur": 5.5, "offset": 0, "stretch": 100, "timeRemap": { … }, "frameBlend": "off", "preserveFps": false,
  "parent": "rig", "keepPlace": false, "enabled": true, "visible": true,
  "transform": { … },                       // or the transform properties directly on the layer
  "threeD": false, "autoOrient": "off", "motionBlur": false,
  "blend": "normal", "matte": { "layer": "m", "mode": "alpha" }, "preserveTransparency": false,
  "masks": [ … ], "effects": [ … ], "styles": { … }, "material": { … },
  "quality": "best", "sampling": "bicubic", "collapse": false, "guide": false,
  "origin": "center", "align": { … }, "measureAt": 0,          // authored placement
  "transitionIn": { … }, "transitionOut": { … }, "crawl": { … }, // authored
  "body": { … }, "pin": { … }, "stabilize": { … } }               // physics (spec 19), tracking (spec 18)
```

| Field | Type | Default | Notes |
|---|---|---|---|
| `id` | id | required | unique in the comp |
| `name` | string | `id` | display name; the After Effects layer name on export |
| `type` | enum | required | §1 |
| `in` | time | `0` | comp time the layer starts showing |
| `out` | time | comp duration, or `in + length·\|stretch\|/100` for finite media | exclusive; > `in` (`layer.empty_span`) |
| `dur` | time | — | authored: `out = in + dur`; with `out` it is an error |
| `offset` | time | `in` for `video`, `audio`, `comp`, `particles`; else `0` | comp time at which layer time is 0 (After Effects "start time") |
| `stretch` | percent | `100` | 200 = half speed; negative reverses within `[in, out)`; 0 is `layer.zero_stretch` |
| `timeRemap` | animatable time | none | `video` and `comp` only (`layer.time_remap_type`) |
| `frameBlend` | `off` \| `mix` \| `flow` | `off` | media and comp layers ([11](11-media-and-audio.md) §3.3) |
| `preserveFps` | boolean | `false` | `comp` layers: sample the nested comp at its own frame times instead of continuous time |
| `parent` | layer id | none | same comp (`layer.parent_other_comp`), no cycles (`layer.parent_cycle`), any type but `audio`; a camera or light may be a parent; a 2D child of a 3D parent is `layer.parent_2d_to_3d` |
| `keepPlace` | boolean | `false` | authored: convert the child's rest pose into the parent's space so assigning the parent does not move it (a percent `position` is resolved against the comp, then converted, under any parent transform); absolute position/rotation/scale keys with it are `place.keep_place_with_keys` |
| `enabled` | boolean or template | `true` | `false` removes the layer entirely (rendering, expressions, exporters); inside components and repeat templates `$props.x` or `{{ … }}`; tweens whose targets were dropped are no-ops (`tween.target_disabled`) |
| `visible` | boolean | `true` (`false` when the layer is a matte source) | After Effects' eyeball: an invisible layer still evaluates (matte source, parent, expression target, audio source) |
| `threeD` | boolean | `false` | [10](10-3d.md) |
| `autoOrient` | enum | `off` | `off`, `path`, `camera`, `pointOfInterest` (§7) |
| `motionBlur` | boolean | `false` | opt into the comp's shutter |
| `blend` | enum | `normal` | one of the 38 modes ([09](09-masks-mattes-blending.md) §6) |
| `matte` | `{ layer, mode }` | none | `alpha`, `alphaInverted`, `luma`, `lumaInverted` |
| `preserveTransparency` | boolean | `false` | paint only where the backdrop already has alpha |
| `masks` | list | `[]` | [09](09-masks-mattes-blending.md) §1 |
| `effects` | list | `[]` | effect instances (the effects area) |
| `styles` | object or `$theme.styles.<name>` | `{}` | §8 |
| `material` | object | After Effects defaults | 3D material options ([10](10-3d.md) §2) |
| `quality` | `best` \| `draft` | `best` | `draft`: nearest sampling, effects' draft paths, per-card 3D sorting |
| `sampling` | `nearest` \| `bilinear` \| `bicubic` \| `lanczos` | `bicubic` | the resampling filter for raster sources (image, video, non-collapsed comp): Mitchell–Netravali (B = C = 1/3) by default, Lanczos-3 for sharp stills; ignored for vector layers and integer translations |
| `collapse` | boolean | `false` (`true` for component instances) | `comp` layers: collapse transformations ([09](09-masks-mattes-blending.md) §5) |
| `guide` | boolean | `false` | renders in `motion.frames` previews with `guides: true`, never in outputs |
| `origin`, `align`, `measureAt` | | | placement sugar, §5 |
| `transitionIn`, `transitionOut` | object | none | [06](06-transitions-and-scenes.md) |
| `crawl` | object | none | [03](03-timeline-and-tweens.md) §7 |
| `body`, `pin`, `stabilize` | object | none | physics world body; corner-pin / stabilize from a track (not in this area) |

**Rasterization.** Vector layers (shape, text, solid, SVG image) are always rasterized at their final transform, so scaling to 400 % stays sharp. Raster sources are rendered at their own resolution and resampled with `sampling`. A shape or text layer **with effects** is rasterized in layer space and resampled instead; the normalizer drops identity effects (a knob at the literal 0 at every key) and the renderer skips effects that are identities at a frame, so a dormant `_blur` costs nothing.

## 3. The transform

Every layer except `audio`. Properties may be written under `transform` or directly on the layer (`"position": …`); both resolve to the same property.

| Property | Type | Unit | Default | Notes |
|---|---|---|---|---|
| `anchor` | vector2 (vector3 in 3D) | px, layer space | per type (§4) | the point that sits at `position` and that scale and rotation pivot around; spatial |
| `position` | vector2/3 | px, parent space | comp centre | spatial; may be separated into `x`/`y`/`z` |
| `scale` | vector2/3 | percent | `[100, 100(, 100)]` | negative mirrors; not clamped |
| `rotation` | number | degrees, clockwise | `0` | = `rotationZ` on 3D layers (writing both is an error) |
| `opacity` | number | percent 0–100 | `100` | multiplies the layer's alpha after effects and masks; **not inherited** by children |
| `skew` | number | degrees −85–85 | `0` | our extension (After Effects layers have none; Lottie `sk`); exported as a Transform effect |
| `skewAxis` | number | degrees | `0` | direction of the shear (Lottie `sa`) |
| `orientation` | vector3 | degrees | `[0, 0, 0]` | 3D only; interpolated by quaternion slerp |
| `rotationX`, `rotationY`, `rotationZ` | number | degrees | `0` | 3D only; Euler numbers (720 = two turns) |
| `pointOfInterest` | vector3 | px | comp centre, z 0 | cameras and lights |

Order: 2D `p' = T(position) · R(rotation) · K(skew, skewAxis) · S(scale/100) · T(−anchor) · p`; 3D `T · Rz · Ry · Rx · O(orientation) · S · T(−anchor)`. World = `local(parent_n) · … · local(parent_1) · local(layer)`. Only the transform is inherited: not opacity, effects, masks, blend, motion blur, visibility. A 3D layer may be parented to a 2D layer (treated as 3D with z = 0).

**Parenting does not move the child.** Values are read in the parent's space; there is no After Effects-style jump compensation. To attach without moving, write values relative to the parent or set `keepPlace: true` (the normalizer converts the rest pose at the child's `in`; relative tweens then move from it).

## 4. Default anchor and position; content bounds

| Layer | Default `anchor` | Default `position` | Content bounds (`origin`, `align`, `fitTo`, lint) |
|---|---|---|---|
| `solid` | `[w/2, h/2]` | comp centre | `[0, 0, w, h]` |
| `image`, `video` | the source centre | comp centre | the source rectangle, or `box` when `fit` is set |
| `comp` | the nested comp's centre | comp centre | the nested comp's rectangle |
| `shape` | `[0, 0]` | comp centre | the union of the contents' **untrimmed** bounds plus paint extents (stroke width, miter allowance) |
| `text` | `[0, 0]`: the first baseline's left / centre / right end per alignment; box text: the box's top-left | comp centre | the laid-out ink bounds (`sourceRectAtTime`) |
| `null` | `[0, 0]` | comp centre | a point |
| `adjustment` | centre of its rectangle | comp centre | the comp rectangle |
| `particles` | `[0, 0]` | comp centre | the emitter's bounds |

"Comp centre" is `[w/2, h/2]` (`[w/2, h/2, 0]` in 3D).

## 5. Placement (authored only)

Pixel coordinates break when text changes length or a variant changes aspect. Placement sugar states intent; the normalizer resolves it to `anchor`/`position` (or to expressions when it must follow something that animates).

### 5.1 Percentages

```jsonc
"position": ["50%", "80%"]      // of the comp (or variant) size
"anchor":   ["50%", "100%"]     // of the layer's content bounds: bottom centre
{ "t": 0, "v": ["-20%", "50%"] } // allowed in key values; mixed with numbers: [120, "50%"]
```

In `position` a percentage is relative to the comp: allowed without a parent, or under a parent chain that only **translates** (a positioned rig null); a parent that scales, rotates or skews is `place.percent_with_parent`. In `anchor` it is relative to the content bounds at the measure time.

### 5.2 `origin`

Sets `anchor` to a named point of the content bounds, so `position` places that point. `origin` with an explicit `anchor` is `place.anchor_conflict`.

| `origin` | Anchor at |
|---|---|
| `top-left`, `top`, `top-right` | the top edge: left, middle, right |
| `left`, `center`, `right` | the vertical middle |
| `bottom-left`, `bottom`, `bottom-right` | the bottom edge |
| `baseline-left`, `baseline`, `baseline-right` | text only: the first line's baseline at the left / middle / right of the ink bounds |
| `[fx, fy]` | fractions of the bounds (`[0.5, 1]` = bottom centre) |

### 5.3 `align`

```jsonc
"align": { "to": "safe", "x": "left", "y": "bottom", "margin": 0 }
"align": { "to": "title", "y": "below", "gap": 24, "x": "left" }
"align": { "to": "comp", "x": "center", "y": "center", "offset": [0, -40], "live": false }
```

Sets `position` (and, unless `origin` is given, `anchor`) so the content bounds line up with a target box.

| Field | Type | Default | Notes |
|---|---|---|---|
| `to` | `comp` \| `safe` \| `action` \| `title` \| layer id | `comp` | the comp rectangle; the title-safe box (`safe` = `title`); the action-safe box; another layer's content bounds in comp space |
| `x` | `left` \| `center` \| `right` \| `before` \| `after` \| null | null | `before`/`after` (layer targets only): entirely to the left / right of the target; null leaves x alone |
| `y` | `top` \| `center` \| `bottom` \| `above` \| `below` \| null | null | `above`/`below` (layer targets only) |
| `margin` | number or `[mx, my]` | `0` | inset from the box edges for `left`/`right`/`top`/`bottom` |
| `gap` | number | `0` | distance for `before`/`after`/`above`/`below` |
| `offset` | `[dx, dy]` | `[0, 0]` | added after alignment |
| `live` | boolean | `false` | §5.5 |

With animated `position` the alignment is the **rest pose**: relative tween values (`"y": "+=60"`) move from it; absolute position keys are `place.align_with_absolute_keys`. `align` needs no parent or an identity-transform null parent. Layer targets resolve in dependency order; a cycle is `place.align_cycle`.

### 5.4 `fitTo`

Auto-sizing boxes (the plate behind a name) are a `fitTo` on a `rect` item inside a shape layer, never a layer field and never on a solid: [07-shapes.md](07-shapes.md) §8.4.

### 5.5 Measure time and live placement

- **Static** (default for `origin` and `align`): bounds are measured once at the layer's `in` (or `measureAt: <time>`), ignoring the layer's own transform animation and text animators; canonical form holds plain numbers.
- **Live** (`live: true`; the default for `fitTo`): the normalizer writes an expression reading `sourceRectAtTime()` of the target every frame, in the form `aligned(t) + (value − rest)`, so relative tweens still move the layer relative to its live place. Absolute position keys with `live: true` are `place.align_with_absolute_keys`. Costs one bounds query per frame per layer (cached per layer and frame).

## 6. Safe areas

```jsonc
"safe": { "action": 0.05, "title": 0.10 }                                         // fractions of the shorter side, all edges
"safe": { "title": { "top": 0.14, "bottom": 0.35, "left": 0.06, "right": 0.06 } }  // per edge: fractions of that axis, or "120px"
"safe": "reels"                                                                    // a platform preset
"safe": { "preset": "tiktok", "action": 0.03 }                                     // a preset, overriding one box
```

| Field | Type | Default | Notes |
|---|---|---|---|
| `action` | number or edges object | `0.05` | action-safe: keep important motion inside |
| `title` | number or edges object | `0.10` | title-safe: keep text inside; must lie inside `action` (`safe.title_outside_action`) |
| `preset` | enum | none | one of the presets below |

| Preset | Top | Bottom | Left | Right | Source |
|---|---|---|---|---|---|
| `broadcast` | 10 % | 10 % | 10 % | 10 % | classic title-safe (action-safe 5 %) |
| `youtube` | 5 % | 5 % | 5 % | 5 % | 90 % title-safe for 16:9 |
| `reels` | 14 % | 35 % | 6 % | 6 % | Meta ads guide (269 / 672 / 65 / 65 px at 1080 × 1920) |
| `tiktok` | 8 % | 21 % | 6 % | 11 % | in-feed UI; the right side holds the action buttons |
| `shorts` | 6 % | 21 % | 6 % | 11 % | YouTube Shorts overlay |
| `story` | 14 % | 18 % | 6 % | 6 % | Instagram / Facebook Stories |
| `square` | 5 % | 5 % | 5 % | 5 % | 1:1 feed posts |
| `linkedin` | 5 % | 12 % | 5 % | 5 % | feed video; the bottom holds the caption and CTA |
| `x` | 5 % | 10 % | 5 % | 5 % | feed video; the bottom holds the caption strip |

The portrait presets (`reels`, `tiktok`, `shorts`, `story`) are defined for 9:16 and fall back to `broadcast` on other aspects; the rest apply at any aspect. `lint.platform` takes the same names; `align: { "to": "safe" }` and `lint.text_outside_safe_area` use the box. Variants usually set their own preset ([01](01-document.md) §8).

## 7. Auto-orient

| `autoOrient` | Effect | Layers |
|---|---|---|
| `off` | none | all |
| `path` | adds the motion-path tangent angle to `rotation` (2D) or the orientation (3D); with separated position uses the velocity direction; keeps the last direction when still | layers with animated position |
| `camera` | 3D layers face the active camera (billboards) | 3D layers |
| `pointOfInterest` | cameras and lights aim at their `pointOfInterest` (two-node behaviour; the default for two-node cameras and spot/parallel lights) | cameras, lights |

`rotation` applies on top (an arrow drawn pointing up: `autoOrient: "path"` with `rotation: 90`).

## 8. Layer styles

```jsonc
"styles": { "dropShadow": { "color": "#000000", "opacity": 35, "angle": 90, "distance": 12, "size": 32 },
            "stroke": { "color": "$theme.color.accent", "size": 4, "position": "outside" } }
"styles": "$theme.styles.card"
```

The nine After Effects / Photoshop layer styles, rendered since engine 0.1.12. A style is present when its key is; `{}` means all defaults; `enabled: false` keeps it but off. Every numeric parameter is animatable. Geometry is computed in layer space after masks and effects; each style is an element with its own blend mode: `dropShadow` and `outerGlow` composite **below** the layer, the others **above** it in table order; the elements share the layer's transform, motion blur, opacity and matte. Angles use the comp's `globalLight` unless `useGlobalLight: false`. On an `adjustment` layer: `layer.styles_on_adjustment`; on a `null`: `layer.field_not_allowed`. The theme may define sets (`theme.styles.<name>`).

| Style | Parameters (default) |
|---|---|
| `dropShadow`, `innerShadow` | `blend` (`multiply`), `color` (`#000000`), `opacity` (75), `useGlobalLight` (true), `angle` (120; the shadow falls opposite), `distance` (5), `spread` (drop) / `choke` (inner) (0, percent), `size` (5, blur), `noise` (0, percent), `knockout` (true, drop only: the layer knocks the shadow out under itself), `enabled` |
| `outerGlow`, `innerGlow` | `blend` (`screen`), `opacity` (75), `noise` (0), `color` (`#FFFFBE`, or a gradient mapped across `range`), `technique` (`softer` \| `precise`), `source` (`edge` \| `center`, inner only), `spread` / `choke` (0), `size` (5), `range` (50, contour), `jitter` (0) |
| `bevelEmboss` | `style` (`outerBevel` \| `innerBevel` \| `emboss` \| `pillowEmboss` \| `strokeEmboss`; `innerBevel`), `technique` (`smooth` \| `chiselHard` \| `chiselSoft`), `depth` (100, 1–1000), `direction` (`up` \| `down`), `size` (5), `soften` (0), `useGlobalLight` (true), `angle` (120), `altitude` (30), `highlightBlend` (`screen`), `highlightColor` (`#FFFFFF`), `highlightOpacity` (75), `shadowBlend` (`multiply`), `shadowColor` (`#000000`), `shadowOpacity` (75) |
| `satin` | `blend` (`multiply`), `color` (`#000000`), `opacity` (50), `angle` (19), `distance` (11), `size` (14), `invert` (true) |
| `colorOverlay` | `blend` (`normal`), `color` (`#FF0000`), `opacity` (100) |
| `gradientOverlay` | `blend` (`normal`), `opacity` (100), `gradient` (black → white; only its `stops`, `opacityStops`, `midpoints`, `interpolation` are used), `reverse` (false), `style` (`linear` \| `radial` \| `angle` \| `reflected` \| `diamond`), `align` (true, align with the layer), `angle` (90), `scale` (100), `offset` (`[0, 0]`) |
| `stroke` | `color` (`#FF0000`), `size` (3), `opacity` (100), `position` (`outside` \| `inside` \| `center`), `blend` (`normal`) |

For the large, hot, physically based glow use the `light.glow` effect (HDR, linear light); the style matches After Effects' simpler glow for interchange.

## 9. Rendering of one layer

1. Source (vector layers rasterized at their final transform). 2. Masks. 3. Effects in list order. 4. Style geometry. 5. Transform into comp space (with motion-blur samples; 3D through the camera). 6. Opacity. 7. Track matte. 8. Blend onto the layers below (below-layer style elements, the layer, above-layer style elements). A layer at opacity 0 with no matte, track-matte or adjustment role is skipped for the frame (a stencil-blend layer never is).

## 10. Type-specific fields

### `solid`

| Field | Type | Default | Notes |
|---|---|---|---|
| `color` | animatable colour | `#808080` | |
| `size` | `[w, h]` | the comp size | not animatable (scale it, or use a shape `rect`) |

### `shape`

`contents` (the item list, [07](07-shapes.md)), or the preset sugar `shape` + `size`/`radius`/`position`/`sides`/`points`/`outer`/`inner`/`roundness`/`from`/`to`/`head`/`headAngle`/`closed`/`smooth`/`startAngle`/`endAngle`/`thickness` with paint shorthands `fill`, `stroke`, `gradient`; or `fromSvg` / `svg` + `fit` + paint overrides ([07](07-shapes.md) §8).

### `text`

`text`, `style`, `paragraph`, `box`, `path`, `animators`, `grouping`, `threeDPerChar`, `words`/`wordStyle`/`paging` ([08](08-text.md)).

### `image`

| Field | Type | Default | Notes |
|---|---|---|---|
| `asset` | asset id | required | an `image` or `svg` asset, or a `video` asset with `frame` |
| `fit` | `none` \| `contain` \| `cover` \| `fill` | `none` | how the source is sized into `box`: natural size placed by `focus`; uniform fit with transparent bars; uniform fill, cropped to the box; stretched. `fit` without `box` uses the comp size (a full-frame background) |
| `box` | `[w, h]` px | the `crop` size, else the natural size | the rectangle in layer space (origin top-left); the content bounds. Static: keys are `anim.not_animatable` (animate `scale`) |
| `crop` | `[x, y, w, h]` source px | the whole image | after orientation |
| `frame` | time | `0` | a `video` or animated image used as a still: the source time |
| `focus` | `[fx, fy]` 0–1 | `[0.5, 0.5]` | the point kept in view when `cover` crops, or where the image sits when space is left; `[0, 0]` = top-left |

An animated GIF/WebP/AVIF on an image layer without `frame` plays as footage. SVG images are vector footage, re-rasterized at the drawn scale.

### `video`

`asset` (a `video` asset, an image sequence, or an animated image), `fit`/`box`/`crop`/`focus` as `image`, and:

| Field | Type | Default | Notes |
|---|---|---|---|
| `sourceIn`, `sourceOut` | time | `0`, end | authored: the source span (`offset = in − sourceIn·stretch/100`; `sourceOut` sets `out`; not with `out`/`dur`) |
| `speed` | number > 0 | `1` | authored: `stretch = 100 / speed`; 0 is `layer.zero_stretch`; ramps need `timeRemap` |
| `reverse` | boolean | `false` | authored: negates `stretch`, keeps `[in, out)` |
| `loop` | boolean | `false` | repeat the source until `out` (the asset `loop` is a fixed count); with `timeRemap` it is `media.loop_and_remap` |
| `hold` | `none` \| `first` \| `last` \| `both` | `both` | what shows before the first / after the last source frame: transparent or the held edge frame |
| `freeze` | time | none | authored: hold one source frame for the whole span (a one-key hold `timeRemap`; audio muted); not with `timeRemap`, `speed`, `loop`, `sourceIn`, `sourceOut` (`layer.freeze_conflict`) |
| `audio` | boolean | `true` | whether the embedded audio plays |
| `volume` | animatable dB | `0` | |
| `pan` | animatable −100–100 | `0` | |
| `fadeIn`, `fadeOut` | time or `{ dur, curve }` | `0` | authored → volume keys |
| `mute` | boolean | `false` | drop the audio from the mix |
| `audioTrack` | integer | `0` | which audio stream |

Past a non-looping source's end the last frame holds (`lint.media_past_end`).

### `audio`

`asset` (an `audio` asset, or a `video` asset for its sound), `in`/`out`/`dur`/`offset`/`stretch`/`sourceIn`/`sourceOut`/`speed`/`loop`/`timeRemap` as `video` (`speed` changes pitch), and:

| Field | Type | Default | Notes |
|---|---|---|---|
| `volume` | animatable dB | `0` | `"-inf"` or ≤ −96 mutes; keys interpolate in dB |
| `pan` | animatable −100–100 | `0` | mono: constant-power; stereo: balance |
| `fadeIn`, `fadeOut` | time or `{ "dur": time, "curve": "sine" \| "linear" \| "exp" }` | `0` | authored → `volume` keys from `in` / to `out` |
| `mute` | boolean | `false` | |
| `solo` | boolean | `false` | previews: `motion.render` refuses solo layers unless `output.allowSolo` (`media.solo_in_render`) |
| `channels` | `stereo` \| `mono` \| `left` \| `right` | `stereo` | |
| `duck` | object | none | authored → volume keys ([11](11-media-and-audio.md) §7.3) |

No transform, masks, effects or styles; never a parent; playback speed must stay within 0.01–16× (`media.audio_track_invalid`).

### `comp`

| Field | Type | Default | Notes |
|---|---|---|---|
| `comp` | comp id | required (or `lottie`) | no self-nesting (`layer.comp_cycle`); depth ≤ 16 |
| `lottie` | asset id | — | a `lottie` asset instead of `comp`: imported into a generated comp `<id>.lottie`; `lottieAnimation`, `lottieTheme` select inside a dotLottie ([11](11-media-and-audio.md) §5) |
| `collapse` | boolean | `false` | collapse transformations ([09](09-masks-mattes-blending.md) §5) |
| `timeRemap`, `frameBlend`, `preserveFps` | | | §2 |
| `loopMode` | `cycle` \| `pingpong` \| null | null | authored: loop the nested comp's duration across the span (a looped `timeRemap`) |
| `hold` | as `video` | `none` (`both` for `scenes` layers) | before the nested comp's start / after its end: transparent or held |

The nested comp renders at its own `size` and `fps` unless collapsed; it is evaluated at continuous time (`preserveFps` snaps to its frames); `frameBlend` crossfades (`mix`) or flow-interpolates (`flow`) the two nested frames around the sampled time.

### `null`

Transform only. `masks`, `styles`, `matte`, `blend` are `layer.field_not_allowed`; `effects` may hold only `control.*` expression controls (the same rule for `camera` and `light`).

### `adjustment`

| Field | Type | Default | Notes |
|---|---|---|---|
| `size` | `[w, h]` | the comp size | the rectangle the adjustment covers (layer space), so it can be scaled, masked, moved |

Applies its `effects` to the composite below within its rectangle × masks × opacity × matte ([09](09-masks-mattes-blending.md) §4).

### `camera`, `light`, `particles`, `component`, `repeat`, `slot`

[10-3d.md](10-3d.md); spec 9 (particles: [effects/40](../effects/40-particles-layer-emitters.md) to [42](../effects/42-particles-render-lines-form-presets.md)); [13-components-themes-data.md](13-components-themes-data.md).

## 11. Examples

`examples/05-layers.json`: every rendered layer type (solid, shape, text, image from a `library:` SVG, comp, a translating null rig (a rotating or scaling rig would make a percent position `place.percent_with_parent`, unless the child has `keepPlace`), `keepPlace` on a pixel-positioned child, adjustment with an effect, camera), transform fields written both ways, a parent chain, percentages, every `origin` form, `align` to comp/safe/layer with `before`/`below`/`gap`/`margin`/`offset`/`live`, `measureAt`, a per-edge `safe`, `autoOrient: "path"`, every layer style with defaults, `quality`/`sampling`/`guide`/`visible`, `in`/`out`/`dur`. `examples/05-media-layers.json`: `image` with `fit`/`box`/`focus`/`crop`/`frame`, `video` with `sourceIn`/`speed`/`loop`/`hold`/`fadeIn`, `audio` with `fadeOut`, `channels` and a `duck`, a `comp` with `loopMode` (assets are `https:` URLs, so `check` reports `asset.unmaterialized` infos and no errors).
