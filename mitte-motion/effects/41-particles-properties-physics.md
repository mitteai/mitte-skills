# Particles 2: particle properties, sprites, physics, the aux system

Spec 9 §9.5–9.7. Fields marked **A** are animatable (keys, drivers, expressions, evaluated at every simulation step); values "sampled at birth" are read at the particle's birth time and held.

## `particle`

| Field | Type | Default | Notes |
|---|---|---|---|
| `life` | seconds A (at birth) | 3 | |
| `lifeRandom` | percent | 0 | |
| `sprite` | name or object | `sphere` | Below. |
| `size` | px A (at birth) | 10 | Diameter. |
| `sizeRandom` | percent | 0 | |
| `sizeOverLife` | curve | `[[0, 1], [1, 1]]` | Multiplier over normalized life (0 birth, 1 death), Catmull-Rom with monotone-limited tangents; `[t, v]` pairs in time order, t in 0–1, v ≥ 0, at least one point. |
| `opacity` | percent A (at birth) | 100 | |
| `opacityRandom` | percent | 0 | |
| `opacityOverLife` | curve | `[[0, 1], [0.9, 1], [1, 0]]` | The default fades the last 10 % so particles never pop out. |
| `color` | colour A (at birth) | `#FFFFFF` | |
| `colorRandom` | percent | 0 | OKLCh hue ± percent × 180°, lightness × (1 ± percent / 2). |
| `colorOverLife` | object | none | `{ "type": "gradient", "stops": [[t, colour], …], "mode": "replace" | "multiply" }` over life; or `{ "type": "fromBirth", "gradient": stops or a gradient object, "by": "random" | "emitterPosition" | "time" }`: one colour per particle picked at birth (confetti palettes by position or time); keyed gradient-object stops are read once, at the simulation's first step. |
| `palette` | list of colours | none | Each particle picks one at random (seeded). The confetti case. |
| `rotation` | `[x, y, z]`° (at birth) | `[0, 0, 0]` | 2D layers use z only. |
| `rotationRandom` | percent | 0 | ± percent of a full turn per axis. |
| `spin` | `[x, y, z]`°/s | `[0, 0, 0]` | Angular velocity. |
| `spinRandom` | percent | 0 | |
| `orientToMotion` | boolean | false | Sprites face their direction of travel (streaks, rain, birds). |
| `faceCamera` | boolean | true | Billboards; `false` lets x/y rotation show on textured quads (fluttering paper). |
| `blend` | `normal` / `add` / `screen` / `lighten` | `normal` | How particles combine with each other. `add` in linear light makes overlapping sparks glow and, with a `light.glow` after the layer, bloom. |
| `glow` | object | none | `{ "size": percent of the sprite (300), "opacity": percent (25), "feather": percent (100) }`: a soft halo per particle. |

### Sprites

`"sprite": "sphere"` or `"sprite": { "type": "star", "points": 6, "rotation": 15 }`; an object without `type` is a sphere, an object with `texture` is a textured quad.

| Sprite | Look | Object fields (default) |
|---|---|---|
| `sphere` | Soft disc | `feather` percent of the radius (50) |
| `glowSphere` | Hard core with a halo | — |
| `star` | 4- or 6-pointed star | `points` 4 or 6 (4), `rotation`° (0) |
| `cloudlet` | Very soft puff (smoke, clouds) | — |
| `streaklet` | A core plus trailing sub-dots along the motion | `streakCount`, `streakSize` percent of the core |
| `square` | Hard square (pixel looks) | — |
| `line` | A segment oriented to motion | `length` px, or `lengthFromVelocity` px per px/s (rain, warp stars) |
| `ribbon` | A strip through the particle's past positions (magic trails) | `segments` ≤ 64 (16), `width` px (0 = the size), `widthOverLength` curve (head 0 → tail 1). History costs `segments` × particles positions. |
| `{ "texture": … }` | A layer, comp or image asset drawn on each particle | `texture.layer` (a hidden layer, often a precomp) **or** `texture.asset` (image), `texture.time` `still`/`current`/`random`/`loop`/`birth` (`still`), `texture.frames` ≤ 64 (16) distinct texture times cached (`birth` holds the frame at birth, the last cached one for a birth past `frames` ÷ fps), `texture.colorize` (multiply by the particle colour), `texture.aspect` (width / height); plus `aspect` on the sprite object. The frames are cropped to the layer's content. |

The aux system takes textured sprites too (its frames are cached apart from the main system's).

## `physics`

Forces act in the particle space (`comp` or `layer`), in px and seconds. Gravity, drag and wind are per system; the aux may override `gravity` and `air`.

| Field | Type | Default | Notes |
|---|---|---|---|
| `gravity` | number px/s² A, or `[x, y, z]` A | 0 | A number pulls down (+y). |
| `air.resistance` | number A | 0 | Linear drag toward the wind, integrated implicitly (`v' = (v + a·dt + wind·resistance·dt) / (1 + resistance·dt)`): stable at any value; a huge resistance holds particles at `gravity / resistance`. |
| `air.resistanceRotation` | boolean | false | Drag also slows spin. |
| `air.wind` | `[x, y, z]` px/s A | `[0, 0, 0]` | Particles accelerate toward the wind velocity in proportion to `resistance`. |
| `air.turbulence` | object | none | Curl noise, below. |
| `air.spherical` | object | none | `{ "strength" px/s² A (negative pulls in), "position" point3d A, "radius" A, "feather" percent of the radius A }`. |
| `attractors` | list | `[]` | `{ "position" point3d A, "strength" px/s² A (negative repels), "radius" A, "falloff": "linear" (1 − r/R inside) | "inverseSquare" (full inside, (R/r)² outside) | "none" (full inside, 0 outside) }`. |
| `vortices` | list | `[]` | `{ "position" A, "axis" [x, y, z] A ([0, 0, 1]), "strength" °/s at the axis fading linearly to `radius` A (0 = no falloff), "inward" px/s toward the axis A }`. |
| `bounce` | object | none | `{ "floor": { "y": A, "enabled": true }, "walls": false (the comp's left and right edges), "layers": [ids] (the alpha of 2D layers; a 3D layer's plane is not built: `render.unsupported` info), "elasticity": 50, "friction": 10, "collisionEvent": "bounce" | "stick" | "kill" | "spawn" }`. `spawn` dies and emits the aux there. A static layer's alpha is sampled once, an animated one at the nearest comp frame to each step. |
| `fields` | list | `[]` | `{ "layer": id, "channel": "rg" (red/green as a vector, 0.5 = zero) | "luminance" (its gradient toward brighter pixels), "strength" A (100), "mode": "velocity" (px/s) | "force" (px/s²) }`: a map pushes particles (a `generate.curlNoise` `vectorField` solid, a painted map). |
| `flock` | object | none | **Not implemented** (P4): accepted; `check` warns `render.unsupported` at `physics/flock` and the render skips it. |

Turbulence (`air.turbulence`): the curl of a 3D (4D with evolution) gradient-noise potential, divergence-free, so particles swirl and stream instead of bunching.

| Field | Default | Meaning |
|---|---|---|
| `position` A | 0 | Displacement strength, px/s: the main "how much swirl" control. |
| `rotation` A | 0 | Induced spin, °/s (tumbling confetti). |
| `scale` A | 100 | Swirl size in px (one lattice unit). |
| `complexity` | 3 | Octaves, 1–8. |
| `octaveMultiplier` | 0.5 | Gain of each finer octave. |
| `octaveScale` | 1.5 | Scale ratio of each finer octave. |
| `evolutionSpeed` A | 50 | Percent; 100 moves the field one `scale` per second; 0 freezes it. |
| `evolutionOffset` A | 0 | Offset into the field's time. |
| `moveWithWind` A | 80 | Percent: the field drifts with `air.wind` (one moving air mass). |
| `affectSize`, `affectOpacity` A | 0 | Percent: the field also modulates size and opacity (flickering embers), 1 + p × n. |
| `seed` | 0 | |

## `aux`: the sub-system

A second, simpler system whose emitters are the main system's particles: trails behind each, or bursts when they die or collide. Aux particles have no aux of their own and draw no `lines`; they count against the system's caps (`check` counts one bounce per particle for `atBounce`; extra bounces past the caps are dropped while simulating, with a warning).

| Field | Default | Notes |
|---|---|---|
| `emit` | `continuously` | `continuously` (per second per main particle), `atBirth`, `atDeath`, `atBounce` (needs `physics.bounce`): `rate` particles per event. |
| `rate` A | 30 | |
| `startEmit`, `stopEmit` | 0, 100 | Percent of the main particle's life during which it emits. |
| `life`, `lifeRandom`, `sprite`, `size`, `sizeRandom`, `sizeOverLife`, `opacity`, `opacityRandom`, `opacityOverLife`, `color`, `colorRandom`, `colorOverLife`, `palette`, `blend`, `rotation`, `rotationRandom`, `spin`, `spinRandom`, `orientToMotion`, `faceCamera`, `glow` | as `particle` | A textured `sprite` on the aux draws its own texture. |
| `colorFromMain` | 0 | Percent mix of the parent's current colour at emission. |
| `inheritVelocity` | 0 | Percent of the parent's velocity. |
| `velocity` A, `spread` A | 0, 180 | Cone about the parent's motion. |
| `physics` | the main's gravity and air | May override `gravity`, `air`, `attractors`, `vortices`; the other forces are the main's. |

```json
"aux": { "emit": "continuously", "rate": 60, "life": 0.4, "sprite": "sphere", "size": 3, "sizeOverLife": [[0, 1], [1, 0]],
         "colorFromMain": 100, "inheritVelocity": 10, "velocity": 20, "spread": 180,
         "opacityOverLife": [[0, 0.8], [1, 0]], "physics": { "gravity": 50, "air": { "resistance": 1 } }, "blend": "add" }
```

## Patterns

**Sparks that bounce on the floor and leave embers.** `physics.gravity` 900, `bounce: { "floor": { "y": 1000 }, "elasticity": 35, "friction": 20 }`, `aux.emit: "atBounce"` with `rate` 6 and a short life.

**Confetti.** A `box` emitter at the top with `direction: [0, 0, 180]`, `sprite: { "texture": { "layer": "shapes", "time": "random", "frames": 6, "colorize": true } }`, `palette` of brand colours, `faceCamera: false`, `rotationRandom` 100, `spin` `[200, 300, 120]`, `air.resistance` 1.2, `air.turbulence` `{ "position": 40, "rotation": 120 }`.

**Smoke.** `cloudlet` sprites, `size` 40 growing (`sizeOverLife` `[[0, 0.3], [1, 1.4]]`), `opacityOverLife` `[[0, 0], [0.2, 0.35], [1, 0]]`, `air.turbulence.position` 60, slow `velocity`.

Full example: `examples/particles-physics.motion.json`.
