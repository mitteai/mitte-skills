# Effects: the instance, the parameters, the rules

An effect is one image operation on a layer: `{ "id", "type", "params" }` in the layer's `effects` list. The list runs in order (the first effect first, its output the next one's input), in the layer's own pixel space, after the layer's masks and before its transform, so an effect moves, scales and rotates with the layer. Every effect reads and writes premultiplied linear-light RGBA in 32-bit float: values above 1 survive, blurs and glows are physically right, and a glow's halo is never clipped at the content's edge because the layer buffer grows to fit it.

The registry is 245 ids (240 implemented; 5 specified only): [90-catalogue.md](90-catalogue.md) is the index, `91-catalogue-*.md` every parameter, and the `10-`…`20-` pages explain each family. `utility.shader` (a custom WGSL kernel) has its own pages, [30-shader.md](30-shader.md) and [31-shader-gallery.md](31-shader-gallery.md).

## The instance

```json
{ "id": "glow", "type": "light.glow",
  "params": { "threshold": 0.6, "radius": 90,
              "intensity": { "keys": [ { "t": 0, "v": 0, "ease": "expo.out" }, { "t": 0.8, "v": 1.4 } ] } },
  "blend": { "mode": "normal", "amount": 100 }, "enabled": true, "quality": "best" }
```

| Field | Type | Default | What it does |
|---|---|---|---|
| `id` | id | `_effect<n>` (1-based) | Unique within the layer. Paths and tween targets use it: `title.effects.glow.radius`. Name every effect you animate. |
| `type` | catalogue id | required | One of the ids in [90-catalogue.md](90-catalogue.md). Unknown: `effect.unknown_type` (error, with a "did you mean" suggestion within a small edit distance). A specified-only id: `effect.unavailable` (error; the message names the phase). |
| `name` | string | none | Display name. Expressions' `effect("name")` look an effect up by `id` first, then by `name`. |
| `enabled` | boolean | `true` | The fx switch. `false` skips the effect as if absent. Not animatable. |
| `params` | object | all defaults | Parameter name → value (below). Unknown names: `effect.unknown_param`. |
| `mask` | object | none | `{ "masks": ["m1", …], "invert": false, "feather": 0 }`: the effect's output is mixed with its input through the region made of those masks of the same layer (`feather` px, animatable), After Effects' Compositing Options → Masks. Unknown fields are rejected. |
| `blend` | object | `{ "mode": "normal", "amount": 100 }` | `amount` is After Effects' Effect Opacity (percent, animatable, 0–100): the output is mixed with the input, `input · (1 − k) + output · k`. `mode` is any of the 38 blend modes ([20-utility-controls.md](20-utility-controls.md) lists them): the output is blended as a source over the input by that mode (on display-encoded values when the comp's `color.blending` is `display`). A partial mix keeps the input's rect, so the chain's running rect does not grow past it. |
| `quality` | enum `best` / `draft` | `best` | `draft` lets an effect take its documented shortcuts (fewer samples, nearest sampling). The render setting `quality: "draft"` sets it for every effect in previews. |
| `expand` | number px or `"none"` | automatic | Written inside `params`. Overrides the automatic bounds growth with a fixed margin, or `"none"` clips the output to the input rect (After Effects' behaviour without Grow Bounds). Not animatable. Rarely needed. |
| `seed` | integer | 0 | Written inside `params`; accepted by every effect, used by those with randomness (the catalogue marks them). |

Where effects apply: on **adjustment layers** to the composite of everything below (inside the adjustment layer's bounds, masks and opacity); on **comp layers** to the nested comp's render; on **text and shape layers** after rasterization. Only expression controls (`control.*`) are allowed on `null`, `camera` and `light` layers. The tween shorthand `blur` adds `{ "id": "_blur", "type": "blur.gaussian" }` at the end of the list if it is missing (in front of a trailing backdrop effect).

A comp-space shadow or glow that must not rotate with the layer is a layer style (`styles.dropShadow`, …, spec 3 §3.6), not an effect; or put the effect on an adjustment layer above.

## Parameter values

Every parameter is written by name inside `params`. The generated pages give each one's **type**, **default**, **range** and whether it is **animatable** (`A`).

**Animatable parameters** take the four animatable shapes of spec 1 §1.11: a static value; `{ "keys": [ { "t", "v", "ease" }, … ] }`; `{ "value": …, "keys": … }`; a driver (`{ "value": 4, "wiggle": { … } }`) or an expression (`{ "expr": "…" }`). Tweens address them by path (`effects.<id>.<param>`, and `effects.<id>.<group>.<field>` for sub-parameters). Enums and booleans are hold-only when animated. `layer`, `asset`, `path`, mask-list, gradient and curve parameters are not animatable (a gradient is read as a whole; a curve animates only as a whole when the point counts match at every key). Non-finite numbers read as 0.

**Ranges.** A `(clamped)` range is a hard range: the value is clamped on read, silently. A `(soft)` range is After Effects' slider range: documentation only, any value is accepted. `length` is clamped at 0 unless marked signed. A value of the wrong JSON type is `effect.invalid_param` (error).

| Kind (catalogue) | Write it as | Notes |
|---|---|---|
| number, integer, percent | a number | Integers are rounded on read. Percent is 0–100 unless the range says otherwise (`frac` = value / 100). A boolean `true`/`false` reads as 1/0. |
| length px | a number | Layer pixels before the layer's scale: a 10 px blur on a layer scaled to 50 % looks like 5 px in the comp. |
| angle ° | a number | Degrees clockwise, 0 = up for directions (90 = right), as After Effects. |
| point `[x, y]` | `[x, y]`, `["50%", "20%"]`, `"center"` | The layer's own pixel space, (0, 0) at the layer origin: the top-left of the source for solids, images, video and comp layers; the layer origin (anchor reference) of text and shape layers. Authored percent strings and `"center"` are baked to numbers at the measure time against the content rect. Catalogue *defaults* written as `"center"` or percent are not baked: they resolve at render time against the chain's running rect (the raster rect for the first effect, the previous effect's output rect after a growing effect). Write a number to pin a point. |
| point3d `[x, y, z]` | `[x, y, z]` | Layer space plus z. Effects get no comp camera: `light.flare`'s and `light.godrays3d`'s `center3d` use x and y only. |
| angle3d | `[x°, y°, z°]` | Rotations about x, y, z (R = Rz · Ry · Rx), animated per component, never scaled with the layer. |
| color | `"#RRGGBB"`, `"#RRGGBBAA"`, a CSS name, `[r, g, b]`/`[r, g, b, a]` working-space floats, `{ "r", "g", "b", "a" }`, `"$theme.color.x"` | Converted to the comp's working space (scene-linear by default); may exceed 1. `null` is "none" where the row allows it (`color.blackWhite` `tint`). |
| enum | the name string | Not in the list: `effect.invalid_param`. Hold-only when animated. |
| boolean | `true`/`false` (also `"true"`/`"false"` or a non-zero number) | Hold-only. |
| layer id | `"otherLayer"` or `null` | A layer of the same comp (see *Reading other layers*). Static. |
| asset id | `"lutAsset"` | An image, video or LUT asset declared in `assets`. Static. |
| gradient | `{ "stops": [[0, "#000"], [1, "#FFF"]], "interpolation": "oklab" }` | 2–64 stops; `interpolation` `oklab` (default), `srgb`, `linear`. Static. |
| curve `[[x, y], …]` | `[[0, 0], [0.5, 0.6], [1, 1]]` | Monotone control points in [0, 1]. |
| mask id, list of mask ids | `"m1"`, `["m1", "m2"]` (also `"all"` where the row says) | Masks of the same layer. |
| list of `{…}` | an array of objects with the fields the row names | Item fields named `position`/`center` are points (`[x, y]`, `["20%", "30%"]` of the layer rect, or `"center"`); fields the descriptor marks `length` are layer px; a keyed item field (`"position": { "keys": … }`) animates on its own (`distort.meshWarp` vertices, `generate.gradient4` points). At most 1,024 items. |
| blend mode | one of the 38 names | `normal`, `add`, `screen`, `multiply`, … (the full list is in [20-utility-controls.md](20-utility-controls.md)). |
| object (group) | `{ "field": …, … }` or the flat dotted names | See *Groups* below. |
| integer seed | an integer | Default 0. The pixels are a pure function of (seed, effect id, layer id, pixel, time): change `seed` for a different take. |
| string | a string | `utility.shader`'s `code`. Never animated. |
| object of uniforms | `{ "name": { "type", "default" } }` | `utility.shader`'s `params`; [30-shader.md](30-shader.md). |

**Groups.** Every head of dotted parameters is an object you may write either way: `"specular": { "intensity": 0.8, "angle": -30 }` or `"specular.intensity": 0.8, "specular.angle": -30`. Each field is read by its own dotted name and animates on its own (`effects.glass.specular.angle` in a tween). A field the schema does not declare is `effect.unknown_param` by its dotted name; a group written as anything but an object is `effect.unknown_param`. Declared groups (`distort.glass` `specular`/`shadow`, `blur.camera` `iris`, `light.rays` `shimmer`, `light.glow` `dirt`, `color.levels` `red`/`green`/`blue`/`alpha`, `color.grade` `vignette`, …) are listed in the generated pages with a `group` row followed by their `group.field` rows.

**Per-channel overrides.** `color.levels` reads `red.inBlack` and falls back to the top-level `inBlack` when the channel field is absent; the same pattern holds wherever a row says "per-channel overrides".

## Colour and precision

- Everything runs in premultiplied linear f32 in the comp's working space. A glow can push a pixel to 6.0; a later `color.exposure` of −2 brings it back instead of clipping.
- Colour-correction effects that take 0–1 inputs (`color.levels`, `color.curves`, `color.threshold`, `color.posterize`, `color.channelMixer`, the display-encoded rows) work on display-encoded values (the sRGB curve applied per channel in the working primaries, exactly invertible). Optical effects (blur, glow, exposure, white balance, lens) work on linear values. The catalogue note of each row says which.
- Effects that change colour work on unpremultiplied colour and re-multiply. Fully transparent pixels stay transparent unless the effect generates (generators, shadows, glows, outlines).

## Bounds

A layer's pixels live in its content rect (the source size; the ink box of text; the comp size for comp layers). Each effect declares where its output can be non-transparent and the renderer grows the buffer to fit (a blur of radius *r* grows the rect by 3*r*; a drop shadow by its offset plus softness; a generator never grows past the layer's raster rect). Growth is capped in comp space at the comp grown by 25 % per side (4× the comp for 3D layers); an input already past the cap keeps its extent. `expand` overrides the growth per instance. The renderer also clips each effect's output to what the next effect (and finally the transform) reads, so a gaussian after a radial zoom clips the zoom to what the gaussian needs; none of this moves a default point or changes pixels.

Generators (`generate.*`) fill the layer's **raster rect**: the content rect plus a 1 px anti-aliasing halo. `"0%"`/`"100%"` points lie on the halo's outer edge, `"50%"` is the content centre. On text and shape layers a generator draws only where the layer has content unless its `composite` says otherwise (`replace` / `over` / `under` / `inside`; the host layer fills the default: `replace` on solids, `over` elsewhere).

## Time, randomness, evolution

- An effect renders at the layer time the renderer asks for, any tick (motion-blur samples, time remap). Parameters are evaluated at that time.
- Effects that read other times (`time.echo`, `time.displacement`, `time.frameBlend`, `time.ccWideTime`, `time.difference`, `matte.keyCleaner`/`matte.refineHard`/`matte.refine` chatter reduction, `color.shadowHighlight` `temporalSmoothing`, `stylize.removeGrain` `temporalFiltering`, `key.ccWireRemoval` `frameOffset`) declare them; the renderer supplies the layer (source, masks and the effects above) at each. `time.posterize` instead changes the time everything above it is evaluated at. `distort.transform` with its own shutter samples its parameters at shutter sub-times; `generate.ccGlueGun` and `distort.ccRipplePulse` read a parameter's history.
- Randomness is a counter hash of (`seed`, effect id, layer id, coordinates, and the evolution or time for animated noise). No wall clock, no frame counter, no thread order: the same document gives the same pixels in any frame order on any box. Noise effects animate through `evolution` (degrees; `cycleEvolution` + `cycle` loop seamlessly) or a `speed`.
- Effects whose pixels depend on the frame time beyond their parameters are marked **Time: yes** in the index (`stylize.grain` while `animated`, `distort.waveWarp`/`distort.ripple` with a `speed`, `stylize.glitch`, `stylize.vhs`, `stylize.noise`, `time.strobe`, `light.leak`, `generate.scribble`, `generate.radioWaves`, `stylize.noiseHlsAuto`, `utility.shader`): the static-layer cache never reuses such a layer across frames.
- `quality: "draft"` changes sampling counts, never random sequences.

## Reading other layers

Parameters of kind `layer id` read another layer of the same comp, rendered at the same comp time, flat, in its own layer space; its transform, styles, matte and opacity are never applied. Each comes with `<param>Source`: `"source"` (raw pixels; a comp layer's render), `"masks"` (after its masks) or `"effects"` (after masks and effects, the default). Where the row has `fit`: `"center"`, `"stretch"`, `"tile"` line a map of another size up with this layer. The other layer need not be visible (`"visible": false` is the usual way to hide a map). A read cycle (A displaces by B, B by A, or a layer reading itself) through the default `"effects"` source is the error `effect.layer_cycle` from `motion.check`, at the parameter that closes it (`/comps/main/layers/1/effects/0/params/map`); a `"source"` or `"masks"` read does not run the other layer's effects and never makes a cycle. Unchecked, the renderer still bounds nested reads at 8 (past that a read is transparent).

```json
{ "id": "warp", "type": "distort.displacement",
  "params": { "map": "noiseMap", "mapSource": "effects", "horizontal": "red", "maxHorizontal": 40,
              "vertical": "green", "maxVertical": 40, "fit": "stretch" } }
```

**Backdrop effects** (`distort.glass`, tiling `backdrop`) read what is *behind* the layer in the comp. They run in comp space at the compositing step, after the layer's transform, with the composite below as their second input; the layer's opacity and matte apply to their output. Rules: last in the layer's list (`effect.backdrop_not_last`; normalization moves a generated `_blur` in front of it), on a 2D, non-adjustment layer outside a 3D run (`effect.backdrop_not_2d`: skipped), lengths in comp pixels (layer px × the layer's mean scale), `layer` parameters read as comp-space images, and a layer read as someone else's input is read without its backdrop effect. A document with a backdrop effect renders on the CPU (the GPU walk declines the plan). Details in [14-distort.md](14-distort.md).

## Phases, availability, diagnostics

Every row has a phase (P1–P4). All P1–P3 rows and `utility.shader` (P4) are implemented; the five ids `blur.reduceInterlace` (P4), `stylize.datamosh` (P4), `perspective.3dGlasses` (P4), `color.autoContrast` and `stylize.motionTrails` (not provided) are `effect.unavailable`. The EffectCraft-derived rows (the re-baseline of 2026-10-08, "P2b" in earlier drafts of spec 7) are phase `P2` in the registry and in spec 7 alike.

| Code | Severity | When |
|---|---|---|
| `effect.unknown_type` | error | `type` is not a catalogue id (the message suggests the nearest). |
| `effect.unavailable` | error | A specified-only id (the message names the phase). |
| `effect.unknown_param` | error | A name the effect does not declare (dotted for a group field). |
| `effect.invalid_param` | error | A value of the wrong type (a string for a number, an enum name not in the list). |
| `effect.missing_input` | warning | A required input was not supplied (a LUT asset that failed to load, a mask id that names no mask); the effect is skipped. |
| `effect.param_value` | warning | The effect failed at render time on its evaluated parameters (a kernel's own check, a failing backdrop effect); it is skipped and the layer composites without it. |
| `effect.backdrop_not_last` | error | A backdrop effect followed by another effect. |
| `effect.backdrop_not_2d` | warning | A backdrop effect on a 3D layer, a layer of a 3D run, or an adjustment layer; it is skipped. |
| `effect.requires_gpu` | warning | A GPU-only effect in a job that renders on the CPU; the layer passes through unshaded (`motion.check` says so in advance). |
| `effect.shader_invalid` | error | `utility.shader` source, uniforms or inputs fail the sandbox or naga's validation ([30-shader.md](30-shader.md)). |
| `effect.shader_timeout` | warning | A shader dispatch passed its time budget; the layer renders unshaded for that frame. |
| `limit.frame_size` | error | An effect's buffer would exceed the frame-size limits. |
| `lint.expensive_effect` | warning | One effect takes over 30 % of the frame budget, or a frame over 500 ms at 1080p. |
| `lint.echo_static_source` | warning | `time.echo` on a layer whose source is static while its transform moves: the echo shows nothing (precompose the moving layer). |

## CPU and GPU

A job renders on one backend, decided before the first frame (`motion.check` reports `estimate.backend`, `cpuMs`, `gpuMs`, `gpuComplete`, `requiresGpu`; `rexx-engine --backend auto|cpu|gpu`). On the GPU backend a layer's effect stack runs on the device when every effect in it has a device lowering (the **Device** column of [90-catalogue.md](90-catalogue.md): the blur, glow, grade, generator and pointwise colour rows), every `blend.mode` is `normal`, no effect has a `mask`, and the recursive Gaussian has f64 on the device; otherwise that stack runs on the CPU and the rest of the frame may still use the device. The pixels of a GPU stack match the CPU's within the compare tolerance, not byte for byte. `utility.shader` runs only on the GPU. A backdrop effect (`distort.glass`) makes the whole job CPU.

## Neutral values and identity

Each row's note names its **neutral value**, the parameters at which the effect is a no-op (a blur of radius 0, `light.glow` `intensity: 0`, `stylize.vignette` `amount: 0`, `transition.*` `completion: 0`). At its neutral value an effect is skipped bit for bit, so animating from the neutral value is free until the first non-neutral frame. Rows that say "No neutral value" always change pixels (`distort.mirror`, `stylize.halftone`, `key.*`): disable them with `enabled: false` or `blend.amount: 0` instead.

## A complete example

`examples/basics-stack.motion.json`: a title with a blur, a glow keyed in, grain, a masked tint and an effect-opacity mix.

```json
{ "motion": 1,
  "comps": { "main": { "size": [1280, 720], "fps": 30, "duration": 3, "background": "#0B0B0F",
    "layers": [
      { "id": "title", "type": "text", "text": "EFFECTS", "origin": "center", "position": [640, 360],
        "style": { "font": "Inter", "weight": 800, "size": 160, "fill": "#F7F3E8" },
        "masks": [ { "id": "left", "shape": "ellipse", "mode": "none", "size": [500, 500] } ],
        "effects": [
          { "id": "soft", "type": "blur.gaussian", "params": { "radius": { "keys": [ { "t": 0, "v": 40, "ease": "expo.out" }, { "t": 0.8, "v": 0 } ] } } },
          { "id": "glow", "type": "light.glow",
            "params": { "threshold": 0.6, "radius": 90, "tint": "#FFB347",
                        "intensity": { "keys": [ { "t": 0.4, "v": 0 }, { "t": 1.2, "v": 1.4 } ] } } },
          { "id": "tint", "type": "color.tint", "params": { "black": "#1B1F3B", "white": "#7CF2FF", "amount": 100 },
            "mask": { "masks": ["left"], "feather": 12 }, "blend": { "mode": "normal", "amount": 70 } },
          { "id": "grain", "type": "stylize.grain", "params": { "amount": 20, "size": 1.2, "preset": "kodak5219" } }
        ] }
    ] } } }
```

The text's mask `left` has `"mode": "none"`, so it does not cut the layer and serves only as the tint's region (a mask in `mask.masks` with any other mode still clips the layer as masks do). The glow's `intensity` starts at its neutral value, so frames before 0.4 s skip it. `motion.check` reports `lint.expensive_effect` for the glow: a glow costs about 15 ms per 720p frame, which is normal and only a warning.
