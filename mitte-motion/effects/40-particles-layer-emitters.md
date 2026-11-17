# Particles 1: the layer, systems, emitters, emission

A `particles` layer simulates one to eight particle systems and draws them as its pixels. The target is Trapcode Particular: sub-frame emission, curl-noise turbulence, sprites in linear light, 3D through the comp camera. Every field below is accepted by the engine (`rexx-doc` rejects unknown fields with `doc.unknown_field`) and rendered, except where marked. The three pages: this one (spec 9 §9.1–9.4), [41-particles-properties-physics.md](41-particles-properties-physics.md) (§9.5–9.7) and [42-particles-render-lines-form-presets.md](42-particles-render-lines-form-presets.md) (§9.8–9.14).

```json
{ "id": "sparks", "type": "particles", "seed": 7, "preroll": 0, "timeStep": "1/240", "space": "comp",
  "position": [640, 700], "motionBlur": true,
  "systems": [ { "id": "main",
    "emitter": { "type": "point", "direction": [0, 0, 0], "spread": 22, "velocity": 520, "velocityRandom": 35, "rate": 260 },
    "particle": { "life": 1.5, "lifeRandom": 40, "sprite": "glowSphere", "size": 7, "sizeOverLife": [[0, 1], [1, 0.25]],
                  "palette": ["#FFFFFF", "#FFB347", "#7C5CFF"], "blend": "add" },
    "physics": { "gravity": 540, "air": { "resistance": 0.35, "turbulence": { "position": 70, "scale": 90 } } } } ],
  "render": { "motionBlur": "streaks" } }
```

A particles layer is a layer in every sense: `in`/`out`, a transform, masks, effects, matte, `blend`, `threeD`, `motionBlur`. The library's `mitte/particles.*` components wrap the common looks ([42](42-particles-render-lines-form-presets.md)).

## Layer fields

| Field | Type | Default | Notes |
|---|---|---|---|
| `systems` | list of systems | required | 1–8 (`limit.particle_systems`). Drawn together with a shared depth sort. |
| `seed` | integer | 0 | Mixed with each system's `id`: two systems with the same settings differ. |
| `preroll` | time | 0 | Simulate this long before the layer's `in` so it starts full (snow already falling). ≤ 30 s (`limit.preroll`). Emission runs through the preroll (`emission.start` defaults to `in − preroll`). |
| `timeStep` | `"1/240"`, `"1/480"`, `"1/960"` | `"1/240"` | Fixed simulation step. Raise only for very fast particles against thin colliders. Changing it changes the simulation. |
| `space` | `comp` / `layer` | `comp` | `comp`: the layer's transform places the **emitter** at the moment of emission only; particles then live in comp space (sparks trail a moving emitter), the buffer is comp-sized and not transformed by the layer, and masks are taken in comp coordinates. `layer`: the whole buffer is transformed by the layer like any other pixels (a snow globe that moves with its layer). |
| `render` | object | see [42](42-particles-render-lines-form-presets.md) | Motion blur, depth of field, depth sort, shadowlets, fog, samples, resolution. |
| `threeD` | boolean | false | Particles render through the comp camera with depth; `false` ignores z. |
| `limits` | object | none | Lower caps for this layer: `{ "particles", "births", "lines" }`, each at most the engine cap (`doc.type` above it; [42](42-particles-render-lines-form-presets.md) *Limits*). |

Percentages inside particle fields resolve **against the comp** (a particle layer draws in comp space) and only in the pixel vectors named `position`, `size`, `center`, `origin`, `from`, `amount`, `amplitude` (emitter position/size, vortex and attractor positions, `assemble.from`, Form `amount`/`amplitude`): x and z of the comp width, y of its height. A percentage anywhere else reads as the field's default. References (`$theme.…`) do not resolve inside systems; put a theme colour on the layer or pass it through a component prop.

## A system

| Field | Type | Default | Notes |
|---|---|---|---|
| `id` | id | `_system<n>` | Part of every random value. |
| `enabled` | boolean | true | A disabled system is left out. |
| `emitter` | object | required | Below. |
| `emission` | object | defaults | Below. The short fields `rate`, `rateRandom`, `bursts`, `stop`, `emitFrom` may be written on the emitter instead (the normalizer moves them); `emission.start` is written in `emission` (the path emitter has its own `start`). |
| `particle` | object | defaults | [41](41-particles-properties-physics.md). |
| `physics` | object | none | [41](41-particles-properties-physics.md). |
| `aux` | object | none | The sub-system, [41](41-particles-properties-physics.md). |
| `lines` | object | none | Plexus lines, [42](42-particles-render-lines-form-presets.md). |
| `displace`, `sizeBy`, `opacityBy`, `colorBy`, `explode`, `assemble` | | none | The Form modifiers and the fly-in, [42](42-particles-render-lines-form-presets.md). |

## Emitters

`emitter.type` picks the shape; each type accepts the common fields plus its own. A field of another type is `layer.field_not_allowed`; a missing required one is `doc.required`.

| `type` | Shape | Own fields (default) |
|---|---|---|
| `point` | A point. | — |
| `box` | A box volume or its surface. | `size` `[w, h, d]` A (`[200, 200, 0]`); `surface` (false) |
| `sphere` | A sphere volume or shell. | `radius` A (100); `surface` (false) |
| `disc` | A flat disc or ring in the emitter's xy plane. | `radius` A (100); `innerRadius` A (0); `orientation` `[x, y, z]`° A |
| `grid` | Points on a regular grid (Form). Burst particle *j* takes cell *j* mod nx·ny·nz row-major (x fastest); rate births walk the cells; the points span the full `size`. | `size` `[w, h, d]` A; `count` `[nx, ny, nz]` (`[20, 20, 1]`); `jitter` percent of a cell A (0) |
| `layer` | The pixels of another layer of the comp (birth sites with a one-pixel jitter). | `layer` id (required); `layerSource` `source`/`masks`/`effects` (`effects`); `sample` `alpha`/`edges`/`luminance` (`alpha`); `threshold` A (0.5); `colorFromLayer` (true): particles take the pixel's colour; `time` `current` (the source at the nearest comp frame to each step) / `still` (sampled once at its in point) |
| `text` | A text layer's glyphs. | `layer` id of a text layer (required); `sample` `fill`/`outline` (`fill`); `units` `all`/`chars`/`words` (`all`); `unitStagger` time (0): emission moves through the units in order (writing-on with sparks). Not a text layer: `doc.type`. |
| `path` | Along a path. | `path` (required): a mask id of this layer, or `"<layer>.contents.<item>"` of a shape layer (converted into this layer's space at the measure time); `distribution` `even`/`random` (`random`; `even` places a burst at equal arc lengths and a stream by the golden-ratio sequence); `start`/`end` percent A (0, 100): animate them for a moving emission head; `normalVelocity` (false): emit along the path normal |
| `light` | One point emitter per listed light layer; position, colour and intensity come from the lights. | `lights` list of light layer ids (required) |
| `model` | Not built: the renderer skips the system with `render.unsupported`. | — |

Common emitter fields:

| Field | Type | Default | Notes |
|---|---|---|---|
| `position` | point3d A | `[0, 0, 0]` | Layer space in both `space` modes, relative to the layer's anchor; the layer's default position is the comp centre, so `[0, 0, 0]` sits at the comp centre by default. |
| `rotation` | `[x, y, z]`° A | `[0, 0, 0]` | Rotates the shape and its `direction`. |
| `direction` | enum or `[x, y, z]`° A | `uniform` | `uniform` all directions; `outwards` away from the centre (spheres, boxes, text, layer sites); `directional` along the rotation; `bidirectional` both ways; `disc` within the emitter's plane. Angles are `directional` applied to the base direction **−y (up)**: `[0, 0, 0]` emits up, `[0, 0, 90]` right, `[0, 0, 180]` down (as effect angles). |
| `spread` | degrees A | 20 | Cone half-angle of random deviation. |
| `velocity` | px/s A | 100 | Speed at birth. |
| `velocityRandom` | percent A | 20 | Uniform variation of speed. |
| `velocityDistribution` | number A | 0 | > 0 biases toward slow particles: speed × *u*^d, *u* uniform in [0, 1]. |
| `inheritVelocity` | percent A | 0 | Fraction of the emitter's own velocity added to each particle. |
| `emitWhileMoving` | object | none | `{ "minSpeed": px/s (0), "rateFromSpeed": false }`: emit only above `minSpeed`; with `rateFromSpeed` the rate is multiplied by speed / max(`minSpeed`, 1). |

A 2D layer (`threeD: false`) keeps directions and turbulence in the xy plane and never moves z.

## Emission

| Field | Type | Default | Notes |
|---|---|---|---|
| `rate` | per second A | 100 | Fractional accumulation is exact: 2.5/s is five particles every two seconds at evenly spaced times. |
| `rateRandom` | percent A | 0 | Per-step variation. |
| `bursts` | list | `[]` | `{ "at": time or "@marker" or "@prefix*", "count": n, "repeat": 0, "interval": time }`. `at` is layer time; a marker is a comp marker converted through the layer's `in`, `offset`, `stretch`; `"@beat*"` bursts on every marker whose name starts with `beat`. A marker inside a component's comp reads the host's markers (up to 16 levels). |
| `start` | time | layer `in` (− `preroll`) | When emission starts (layer time). |
| `stop` | time | layer `out` | When it stops; live particles finish their lives. Before an explicit `start`: `doc.type`. |
| `emitFrom` | `step` / `frame` | `step` | `step`: exact sub-frame birth times (smooth streams at any speed); `frame`: births on frame times only (a stepped look). |

Validation (`motion.check`): `rate` ≥ 0, burst `count` ≥ 0 and `at` finite, `spread` ≥ 0, percent fields 0–100, `count` entries ≥ 1, a `layer`/`text`/`path`/`light` emitter must name an existing layer or path (`ref.layer`; a system whose source cannot be sampled at render time emits nothing with a `ref.layer` warning), and the caps below. Limits are checked before rendering from the emission settings (alive ≈ `rate` × max life × (1 + `lifeRandom`) + Σ burst counts; births = `rate` × span + bursts), so an over-limit document is rejected up front; a simulation that still reaches a cap drops later births with a `limit.particles` warning.

## A moving emission head

```json
{ "id": "trail", "type": "particles", "seed": 3,
  "masks": [ { "id": "arc", "shape": "ellipse", "mode": "none", "size": [800, 400] } ],
  "systems": [ { "id": "head",
    "emitter": { "type": "path", "path": "arc", "distribution": "even",
                 "start": { "keys": [ { "t": 0, "v": 0 }, { "t": 3, "v": 100 } ] }, "end": { "keys": [ { "t": 0, "v": 2 }, { "t": 3, "v": 100 } ] },
                 "normalVelocity": true, "velocity": 40, "spread": 30, "rate": 400 },
    "particle": { "life": 1.2, "sprite": "sphere", "size": 4, "color": "#FFB347", "blend": "add", "sizeOverLife": [[0, 1], [1, 0]] },
    "physics": { "air": { "resistance": 0.8, "turbulence": { "position": 30, "scale": 60 } } } } ] }
```

Full example: `examples/particles-emitters.motion.json` (every emitter type on one comp).
