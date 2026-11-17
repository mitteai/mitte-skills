# 2D physics 1: the world and the bodies

Rigid-body physics for 2D layers (spec 19). The comp gets one `physics` world; layers become bodies with `body`. The simulation runs **once, during normalization** (rapier2d, deterministic) and is written back as per-frame keyframes on `position` and `rotation` (whole-layer bodies) or as a per-unit animator (text bodies), plus a `sims` entry; the renderer never simulates. Frames are therefore independent, cacheable and chunkable. Physics is for interactions (many bodies colliding); one object with a physical feel is an ease (`back.out`, `bounce.out`, `spring`) or a driver, and lint says so (`physics.single_body`).

Three pages: this one (§19.3–19.4), [51-physics-forces-joints.md](51-physics-forces-joints.md) (§19.5), [52-physics-handoff-bake-art-direction.md](52-physics-handoff-bake-art-direction.md) (§19.6–19.12). Everything on these pages is implemented (engine ≥ 0.1.32: joints, fields, alpha-contour colliders, mask colliders, animated mattes, drivers and expressions in the hand-off, sleeping) except where marked.

```json
"comps": { "main": { "size": [1920, 1080], "fps": 30, "duration": 6,
  "physics": { "gravity": [0, 2400], "world": { "floor": true, "walls": ["left", "right"] }, "rate": 240, "seed": 3 },
  "layers": [
    { "id": "word", "type": "text", "text": "GRAVITY", "origin": "center", "position": ["50%", "45%"],
      "style": { "font": "Inter", "size": 220, "weight": 800 },
      "body": { "type": "dynamic", "per": "chars", "shape": "hull", "inset": 2, "restitution": 0.25, "start": 0.8,
                "settle": { "at": 3.4, "dur": 0.9, "to": "layout", "ease": "back.out(1.4)", "stagger": { "each": 0.06, "from": "start" } } } } ] } }
```

## The world: `comps.<id>.physics`

| Field | Type | Default | Notes |
|---|---|---|---|
| `gravity` | `[gx, gy]` px/s² | `[0, 2400]` | +y is down. 2400 is snappier than real gravity (a 1080 drop in ≈ 0.95 s); `[0, 981]` reads floaty; `[0, 0]` zero-g. Not animatable. |
| `world.floor` | `true` / `false` / y px | `false` | A static half-plane: `true` at the bottom of `bounds`, a number at that comp-space y. |
| `world.walls` | list of `left`, `right`, `top` | `[]` | Static half-planes at the edges of `bounds`. |
| `world.bounds` | `"comp"`, `"safe"`, `[x, y, w, h]` | `"comp"` | The box `floor: true` and `walls` refer to (`safe`: the title-safe box). |
| `world.friction` | ≥ 0 | 0.6 | Floor and walls. |
| `world.restitution` | 0–1 | 0.1 | Floor and walls. |
| `world.thickness` | px | 200 | Slab thickness outside `bounds` (stops fast bodies tunnelling). |
| `rate` | Hz | 240 | 60–960 and ≥ the comp's fps (`physics.rate_range`); below 4 × fps lint `physics.rate_low`. |
| `substeps` | 1–8 | 1 | Solver substeps per step. |
| `iterations` | 1–16 | 4 | Velocity iterations per substep (`substeps × iterations` is Rapier's solver iterations). Stacks of three or more resting bodies stay crisp at 4 × 8 (lint `physics.soft_stack` at the defaults). |
| `seed` | integer | 0 | Seeds `vary`, impulse `spread`, explosion `spin`, wind `turbulence`. A world with no random field ignores it (`physics.seed_no_effect`). |
| `vary` | `{ velocity, spin, rotation, position }` | all 0 | Per-body random jitter of initial conditions (px/s, °/s, °, px), seeded by `seed` and the body id. |
| `start` | time | 0 | Comp time the simulation starts; bodies with a later `start` are kinematic until theirs. |
| `end` | time or `"auto"` | `"auto"` | `auto`: stop 0.5 s after every dynamic body sleeps with nothing left to wake it (no force still to come, no open field span, no hand-off or settle pending, no kinematic body whose animation or matte still changes; a paddle keyed for the first second counts as still after it), at the latest the comp's end; every body then holds its last pose. An explicit time simulates to it with sleeping off. `physics.idle_span` (info) when nothing moved for > 2 s before `end`. |
| `forces` | list | `[]` | ≤ 256 (`limit.physics_forces`), [51](51-physics-forces-joints.md). |
| `joints` | list | `[]` | ≤ 1,000 (`limit.physics_joints`), [51](51-physics-forces-joints.md). |
| `lock` | `{ "asset", "hash", "force" }` or null | null | A locked bake, [52](52-physics-handoff-bake-art-direction.md). |

Units: px, seconds, degrees, px/s, °/s. Internally 100 px = 1 m (Rapier's `length_unit`). A comp with `physics` and no body is `physics.no_bodies`; a `body` in a comp without `physics` is `physics.no_world`. A nested comp has its own world; its bodies never meet the parent's.

## A body: `layer.body`

Allowed on `solid`, `shape`, `text`, `image`, `video`, `comp` layers, and on `null` with an explicit `shape` (an invisible collider); anything else is `physics.body_not_allowed`. The layer must be 2D and not parented to a 3D layer (`physics.layer_3d`); its parent, if any, must not move during the simulation (`physics.parent_moves`; a static null rig is fine, and children of a body ride along).

| Field | Type | Default | Notes |
|---|---|---|---|
| `type` | `dynamic` / `static` / `kinematic` | `dynamic` | dynamic: moved by the simulation; static: never moves (a shelf); kinematic: follows its own keys, drivers and expressions and pushes dynamic bodies without being pushed back (a sweeping bar, a tracked object, an animated matte). |
| `shape` | `auto`, `box`, `circle`, `capsule`, `hull`, `decompose`, `path`, or an object | `auto` | Below. |
| `per` | null, `chars`, `words`, `lines` | null | Text layers only (`physics.per_not_text`): one body per unit. |
| `density` | > 0 | 1 | Mass = density × area (relative values matter). |
| `mass` | > 0 | none | Overrides density. |
| `friction` | ≥ 0 | 0.4 | Combined by geometric mean. |
| `restitution` | 0–1 | 0.2 | Bounciness; combined by max. |
| `linearDamping`, `angularDamping` | ≥ 0 | 0.05, 0.1 | Decay per second. |
| `velocity` | `[vx, vy]` px/s | `[0, 0]` | Added to the hand-off velocity. |
| `spin` | °/s | 0 | Added to the hand-off spin (positive = clockwise). |
| `start` | time | `physics.start`, or the layer's `in` if later | When the simulation takes the body over; before it the layer follows its own animation ([52](52-physics-handoff-bake-art-direction.md)). |
| `before` | `kinematic` / `ghost` | `kinematic` | Before `start`: others collide with it along its keys, or not at all. |
| `settle` | object | none | Blend into a target pose, [52](52-physics-handoff-bake-art-direction.md). |
| `fixAxes` | list of `x`, `y`, `rotation` | `[]` | Degrees of freedom held fixed (`["rotation"]`: slides but never tilts). |
| `group` | id | none | Collision group name; `world` is reserved (`physics.reserved_group`); ≤ 30 named groups per comp (`physics.unavailable` beyond). |
| `collides` | list of groups or `"all"` | `"all"` | Symmetric filtering: a pair collides only when each admits the other's group. Floor and walls are the implicit group `world`. A name no body has as its `group` warns `physics.unknown_group`. |
| `inset` | px | 0 | Shrinks (positive) or grows (negative) the collider; inset text slightly so it does not float on its anti-aliased edge. |
| `ccd` | boolean | false | Continuous collision detection for fast thin bodies. |

What a dynamic body controls: the layer's `position` and `rotation` from `start` on (keys after `start` are ignored, `physics.keys_after_start`); everything else animates normally (scale changes after `start` do not resize the collider, `physics.content_animates`). Body ids: the layer id, or `<layer>.c<i>` / `.w<i>` / `.l<i>` for text units (counting units that became bodies, from 0); forces and joints target these.

### Colliders

Built from the layer's content at the body's `start`, in layer space through the layer's scale and skew, with the anchor as origin.

| Layer | `auto` | Notes |
|---|---|---|
| `solid` | the solid's box | masks are ignored unless `shape` is `path` or `{ "mask": id }` |
| `shape` | from the filled and stroked outline at `start` (path operators applied): a circle if one equal-radius ellipse, a round box if one rectangle, a convex polygon if convex, else `decompose` | |
| `text` | one body: the convex hull of all glyph outlines; with `per`, the hull of each unit's glyphs | `decompose` keeps letter concavities |
| `image`, `video` | the convex hull of the alpha contour (alpha ≥ 0.5, traced and simplified at 1 px) | `decompose` keeps concavities and holes; `box` keeps the content box; a video traces the frame shown at `start` |
| `comp` | the content-bounds box | `hull` renders the nested comp at half resolution and takes its contour's hull; `decompose` keeps concavities; a Lottie comp layer traces the Lottie's own alpha |
| `null` | — | needs an explicit shape |

Explicit shapes, in layer px relative to the anchor: `{ "box": [w, h], "at": [dx, dy], "radius": r }`, `{ "circle": r }`, `{ "capsule": [length, radius] }` (horizontal), `{ "polygon": [[x, y], …] }`, `{ "mask": id }` (one closed mask of the layer). `shape: "path"` uses every additive, non-inverted, enabled closed mask of the layer (a mask without `mode` counts as additive); not for `per` text bodies.

Rules: decomposition is capped at 64 convex parts of 256 vertices (`physics.shape_too_complex`: simplify or use `hull`); nothing collidable at `start` is `physics.shape_empty`; pixels that cannot be read fall back to the content box with `asset.unreadable`; two dynamic colliders overlapping by > 0.5 px at the start warn `physics.overlap_at_start` (space them, `inset`, or stagger `start`). Contour times ignore `timeRemap`.

**Animated mattes.** A `kinematic` body on a `video` layer (`auto`/`hull`/`decompose`) or a `comp` layer (`hull`/`decompose`) rebuilds its collider from the footage's alpha at every comp frame of the span (held between frames, capped at 1,800 frames with `physics.content_animates` beyond): letters land on a segmented person. A frame change carries no velocity (bodies are pushed out by de-penetration, so a fast-growing matte nudges rather than bats; a body fully inside a matte is not pushed out).

### Text bodies

`per: "chars" | "words" | "lines"`: whitespace never becomes a body; ligatures are disabled; each unit's collider is its glyph hull (or decomposition) at the unit's laid-out position. The unit's pivot follows the layer's `grouping.anchorGrouping` (default `char`; `word` with `per: "words"`) and `grouping.alignment` (baseline centre by default; `[0, -50]` for the visual centre). The layer itself does not move: the bake drives the units through a generated range-selected animator per unit (`_physics…`), evaluated first; other animators (colour, opacity, blur) still apply, but animators that move units during the span are `physics.text_animator_conflict`. Animators that move units *before* `start` are the units' kinematic motion: each body follows its unit's `position`/`rotation` offset (and the layer's own motion before `start`), so it hands off from where it is drawn with that velocity (a lift into place that ends at `start` tosses the letters on); `tracking`/`scale`/`anchor` offsets before `start` are not followed, and an `expression` selector leaves the motion out with `physics.content_animates`; and the layer's own transform must be static over the span (`physics.text_layer_animates`; animate a parent null before `start` instead).

### Static and kinematic

A static body is placed once at the simulation start (animating its layer warns `physics.static_animates`). A kinematic body's pose is evaluated from its layer's keys, eases, drivers and expressions at every step (not only at frames), and the solver moves it there with the velocity that reaches that pose; a kinematic body whose motion depends on a dynamic body's pose is `physics.cycle`. A kinematic layer may also be driven by a track ([62-tracking-documents.md](62-tracking-documents.md)): bodies then collide with the tracked object between frames too.

Full example: `examples/physics-letters.motion.json` (letters fall, pile up, settle back; a static container; a kinematic sweep).
