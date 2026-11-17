# Particles 3: rendering, connecting lines, Form fields, explode and assemble, presets, limits, export

Spec 9 §9.8–9.14.

## `render` (layer level)

| Field | Type | Default | Notes |
|---|---|---|---|
| `motionBlur` | `off` / `comp` / `streaks` / `subframes` | `comp` | `comp`: follows the layer's `motionBlur` switch and the comp shutter, drawn as streaks. `streaks`: each particle stretched along its exact path over the shutter (analytic, curved paths in 4 segments). `subframes`: `samples` sub-frame renders averaged (exact for spinning textured sprites, costs N×). `streaks` and `subframes` do not need the layer switch. |
| `depthOfField` | `off` / `camera` / `squared` | `off` | 3D layer with an active camera with DOF: per-particle circle of confusion as a larger, dimmer sprite; `squared` exaggerates. |
| `depthSort` | boolean | true (3D) | Back-to-front for `normal` blending; `add`/`screen` skip it. |
| `shadowlets` | object | none | `{ "light": light layer id (required), "opacity": 30, "softness": 40, "colorize": "#000000", "resolution": 8–128 (64; `doc.type` outside) }`: self-shadowing through a density volume (3D layers). |
| `fog` | object | none | `{ "near": z, "far": z, "color" }` (3D layers). On a 2D layer `depthOfField`, `depthSort`, `shadowlets` and `fog` are ignored with one `render.unsupported` info at `render`. |
| `samples` | integer | the comp's | For `subframes`, 1–64 (`doc.type` outside). |
| `resolution` | percent | 100 | Render the buffer smaller and upscale bicubically (draft, very soft particles). |

Particles render in linear light into a premultiplied float buffer; `add` particles exceed 1.0 and a `light.glow` after the layer blooms them. A 3D layer joins its 3D run through the comp camera as one screen-aligned card at the layer's anchor depth (no per-particle occlusion against cards). `quality: "draft"` draws every other particle at doubled opacity.

## Connecting lines (`lines`, Plexus)

```json
"lines": { "maxDistance": 140, "maxPerParticle": 4, "width": 1.2, "color": "fromParticles", "opacity": 60, "falloff": "linear",
           "triangles": { "opacity": 14, "maxDistance": 110 }, "points": { "size": 3 }, "blend": "add", "connectTo": ["logo"] }
```

| Field | Default | Notes |
|---|---|---|
| `maxDistance` | 120 | px in particle space (x, y, z on a 3D layer). |
| `minDistance` | 0 | Closer pairs are not connected. |
| `maxPerParticle` | 5 | 1–64; each particle keeps its nearest candidates, pairs accepted nearest first while both ends have room. |
| `width` | 1 | px (scaled by the layer / camera at the ends). |
| `widthFalloff` | false | width × (1 − d / maxDistance). |
| `color` | `"fromParticles"` | Interpolates the two ends' colours; or one colour. |
| `opacity` | 50 | Percent × `falloff` × the ends' opacity. |
| `falloff` | `linear` | `linear` 1 − u, `smooth` 1 − smoothstep(u), `none`. |
| `triangles` | none | `{ "opacity": 20, "maxDistance": the lines' }`: fills mutually connected triples (low-poly mesh). |
| `points` | none | `{ "size": 3 }`: a dot on each connected particle. |
| `blend` | `add` | `normal`/`add`/`screen`/`lighten`. |
| `connectTo` | none | Shape or text layer ids whose path / glyph vertices join the network (≤ 65,536 per system; a vertex links to particles only). Another layer type, or the particle layer itself: `ref.layer`. |

None of these is animatable (a keyed value is `doc.type`). The search is a fixed-order uniform grid (≤ 8,192 candidates per node), the frame's pair budget `limit.particle_lines` (2,000,000; the farthest pairs are dropped with one warning per layer).

## Form fields: `displace`, `sizeBy`, `opacityBy`, `colorBy`

A `grid` emitter with `rate: 0`, one burst at 0, a `life` longer than the layer and no velocity is a static field (Trapcode Form); these per-frame modifiers animate it (they are not integrated, so a frame depends only on its own time). They apply to any system, not only grids; none is animatable.

| Field | Fields (default) | Effect |
|---|---|---|
| `displace` | list, summed in order | A position offset per particle, by `type`: |
| · `noise` | `amount` `[x, y, z]` px (required), `scale` (300), `complexity` 1–8 (3), `evolutionSpeed` percent (50; 100 = one `scale` per second), `seed` (0) | fractal noise per axis × amount |
| · `layer` | `layer` id (required), `channel` luminance/alpha/red/green/blue (`luminance`), `amount` (required) | the map's channel (× alpha for colour channels) × amount |
| · `audio` | `asset` audio asset (required), `band` `[lo, hi]` Hz (`[20, 20000]`), `amount` (required), `falloff` `none`/`radial`, `speed` px/s (600, with `radial`) | the band's level × amount; `radial` ripples out from the emitter at `speed` |
| · `wave` | `amplitude` `[x, y, z]` (required), `wavelength` (200), `speed` px/s (100), `direction`° in xy (0 = +x) | amplitude × sin(2π (d · p − speed · t) / wavelength) |
| `sizeBy`, `opacityBy` | `{ "layer": id, "channel": luminance, "min": 0, "max": 1 }` | size / opacity × (min + (max − min) × channel), ≥ 0 |
| `colorBy` | `{ "layer": id, "mode": "multiply" | "replace" }` | multiply by the map's colour weighted by its alpha, or take its straight colour |

Layer maps are read as straight linear RGBA, bilinear, transparent outside, at the nearest comp frame to each step; on a `grid` or `box` emitter the comp frame is stretched over the emitter's x/y `size` (so a grid shows the whole frame), every other emitter reads the map in place. A field of another `displace` type is `layer.field_not_allowed`; a missing required one `doc.required`.

## `explode` and `assemble`

| Field | Fields (default) | Behaviour |
|---|---|---|
| `explode` | `at` time or marker (required), `strength` px/s (300, ≥ 0), `randomness` percent (30) | Before `at` the particles hold in place (physics does not move them); at the first step at or after `at` each gets `strength` outward from the emitter's centre (the sampled sites' centre for `layer`/`text` emitters), randomized in direction and speed by `randomness`; physics drives them from then on. |
| `assemble` | `at` (required), `dur` (1.5), `from` `"scatter"` or `[x, y, z]`, `distance` px (600), `randomness` percent (40) | Particles sit at scattered starts (50–100 % of `distance` away; or spread 5 % around the point) and fly onto their birth sites along a critically damped spring that lands exactly at `at + dur`; `randomness` lags each start by up to `randomness` × `dur` / 2. |

Grid particles have stable row-major indices, so these look the same in every render.

```json
{ "id": "form", "emitter": { "type": "grid", "position": [960, 540, 0], "size": [1920, 1080, 0], "count": [192, 108, 1], "velocity": 0, "velocityRandom": 0 },
  "emission": { "rate": 0, "bursts": [ { "at": 0, "count": 20736 } ] },
  "particle": { "life": 100, "sprite": { "type": "sphere", "feather": 30 }, "size": 4.5, "opacityOverLife": [[0, 1], [1, 1]] },
  "displace": [ { "type": "noise", "amount": [6, 6, 0], "scale": 70, "evolutionSpeed": 60, "complexity": 2 },
                { "type": "wave", "amplitude": [0, 3, 0], "wavelength": 160, "speed": 120, "direction": 0 } ],
  "sizeBy": { "layer": "word", "channel": "alpha", "min": 0, "max": 1 }, "colorBy": { "layer": "word", "mode": "replace" } }
```

## Presets: the `mitte/particles.*` components

Sixteen library components output a particle layer (sometimes with a glow) on a comp-sized canvas (`duration: "parent"`). Use them as `{ "type": "component", "use": "mitte/particles.<name>@1", "props": { … } }`; `disintegrate`, `assemble` and `form-logo` take the text or logo in their `layer` **slot** (`"slots": { "layer": [ { … a layer … } ] }`: a list of layers), positioned in frame coordinates, because a system inside the component cannot read a layer of the instance's comp. A burst `at` or `markers` prop may name a marker of the instance's comp (`"@drop"`); vector props in percent resolve against the frame.

| Component | Props (default; range) |
|---|---|
| `particles.confetti` | `at` (0), `origin` (`["50%", "100%"]`), `palette` (5 colours; 1–16), `amount` (300; 10–5000), `spread`° (35; 0–180), `power` px/s (1800; 100–6000) |
| `particles.sparks` | `origin` (`["50%", "55%"]`), `rate` (180; 1–5000), `direction`° from up (0; −180–180), `color` (`#FFB347`), `floor` y px (1000) |
| `particles.snow` | `density` /s (120; 1–5000), `wind` px/s (40; −1000–1000), `sizeRange` `[min, max]` px (`[3, 9]`) |
| `particles.dust` | `density` (40; 1–2000), `color` (`#FFE9C7`), `light` layer (null; shadowlets) |
| `particles.embers` | `rate` (60; 1–3000), `color` (`#FF7A2A`), `rise` px/s (140; 0–2000) |
| `particles.bokeh` | `count` (40; 1–1000), `palette` (4 colours), `size` px (120; 4–800), `iris` `round`/… (`round`) |
| `particles.starfield` | `count` (800; 10–20000), `speed` px/s (400; 1–20000), `warp` boolean (false) |
| `particles.burst-on-beat` | `markers` (`"@beat*"`), `palette`, `amount` per burst (60; 1–5000) |
| `particles.disintegrate` | slot `layer`; `at` (0.5), `dur` (1.5; 0.1–30), `direction` enum (`right`), `wind` px/s (320), `turbulence` px/s (90) |
| `particles.assemble` | slot `layer`; `at` (0.2), `dur` (1.6; 0.1–30), `from` `[x, y]` frame px (null = scatter) |
| `particles.magic-trail` | `path` SVG path data in frame px, `dur` (2; 0.1–60), `color` (`#7AE7FF`), `length` s the trail lingers (0.8; 0.05–10) |
| `particles.plexus` | `count` (180; 2–5000), `maxDistance` px (170; 10–1000), `color` (`#7CC4FF`), `depth` px (600; 0 = flat) |
| `particles.smoke` | `origin` (`["50%", "85%"]`), `rate` (40; 1–1000), `color` (`#B4B9C2`), `light` layer (null) |
| `particles.rain` | `density` /s (400; 1–20000), `angle`° (12; −60–60), `floor` y px (1040) |
| `particles.fireworks` | `at` (0), `count` (160; 1–5000), `palette` (4 colours), `origin` (`["50%", "100%"]`) |
| `particles.form-logo` | slot `layer`; `gridDensity` dots across (120; 8–400), `noise` px (40; 0–2000) |

```json
{ "id": "boom", "type": "component", "use": "mitte/particles.confetti@1",
  "props": { "at": "@drop", "origin": ["50%", "100%"], "palette": "$theme.color.palette", "amount": 300 } },
{ "id": "dust", "type": "component", "use": "mitte/particles.disintegrate@1", "props": { "at": 0.6, "dur": 1.2, "direction": "right" },
  "slots": { "layer": [ { "id": "word", "type": "text", "text": "DUST", "origin": "center", "position": [960, 540], "style": { "size": 200, "weight": 800, "fill": "#FFB347" } } ] } }
```

## Determinism and limits

Every system is simulated once per job from `in − preroll` with the fixed step, checkpointed every second (in memory; on disk as `<hash>.psim` under `--sim-dir` for chunked renders), and each frame draws the nearest checkpoint stepped forward or the samples kept for the job's frames: the same bytes in any frame order and thread count. Every random value is a counter hash of (layer seed, system id, particle index, purpose). Changing `timeStep` or `preroll` changes the simulation; nothing else about the render does.

| Limit | Value | Code |
|---|---|---|
| Systems per layer | 8 | `limit.particle_systems` |
| Alive per system / per layer (aux included) | 1,000,000 / 2,000,000 | `limit.particles` (checked before rendering from the emission settings; a cap reached while simulating drops later births with a warning) |
| Births per layer | 50,000,000 | `limit.particle_births` |
| Sprite pixels per frame (alive × largest diameter², glow halo included, each at most the frame) | 128 frames (at least 128 × 1080p) | `limit.particles` (message gives the computed px) |
| `preroll` | 30 s | `limit.preroll` |
| Line pairs per frame | 2,000,000 | `limit.particle_lines` (warning; farthest pairs dropped) |
| Ribbon `segments`, texture `frames` | 64, 64 | clamped |
| Shadowlet `resolution` | 8–128 per side | `doc.type` outside |

A layer's `limits: { "particles", "births", "lines" }` lowers these for itself (a value above the engine's cap is `doc.type`).

## What is not implemented

- `physics.flock` (P4): accepted; `check` warns `render.unsupported` at the field, the render skips it.
- The `model` emitter: skipped with `render.unsupported`.
- A 3D layer as a `bounce.layers` collider plane (P4: the layer is skipped as a collider, an info `render.unsupported`), per-particle occlusion against 3D cards.


## Export

After Effects: each enabled particle layer is rendered to a ProRes 4444 clip with alpha and placed as footage in a precomp `<layer> (rendered particles)` (`convert.ae_rendered`, info; `ae_prerender: false` skips the layer with `convert.ae_layer_unsupported`). Lottie: not representable; `convert.lottie_particles` warns and omits the layer, or with `render_unsupported: true` embeds a PNG sequence at `bake_fps`; `motion.check` reports one `convert.lottie_particles` info per particle layer. Canonical JSON is lossless.

Full examples: `examples/particles-form.motion.json` (a Plexus, a Form grid drawing a word, an explode, an assemble), `examples/particles-presets.motion.json` (four presets).
