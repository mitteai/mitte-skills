# 2D physics 2: forces, fields, joints

Spec 19 §19.5. Forces live in `physics.forces` (≤ 256), joints in `physics.joints` (≤ 1,000). Every force type is implemented, every joint type too (engine ≥ 0.1.30).

## Targets and times

`targets` (default `"*"`, all dynamic bodies) is one string or a list: a body id (`"logo"`), a layer id with `per` (all its unit bodies), a text-unit selector (`"word/chars"`), a wildcard (`"bars.*"`), a group (`"group:icons"`), or `"*"`. A target that matches nothing is `physics.unknown_target`. Times are comp times in any spec 1 form, markers included (`"@beat9"`).

## Impulse

An instant change of velocity.

```json
{ "type": "impulse", "at": "@beat9", "targets": "group:icons", "vector": [0, -900], "spin": 0,
  "spread": { "vector": [250, 150], "spin": 240 }, "stagger": { "each": 0.03, "from": "center" } }
```

| Field | Type | Default | Notes |
|---|---|---|---|
| `at` | time | required | |
| `targets` | target(s) | `"*"` | |
| `vector` | `[vx, vy]` px/s | `[0, 0]` | Added to each target's velocity. |
| `spin` | °/s | 0 | Added to angular velocity. |
| `mode` | `velocity` / `impulse` | `velocity` | `velocity` is mass-independent (everything jumps the same); `impulse` divides by mass. |
| `spread` | `{ "vector": [jx, jy], "spin": s }` | none | Per-target random addition, uniform in ±j, seeded by the world `seed` and the body id. |
| `stagger` | stagger object | none | Applies to the targets at staggered times (spec 2 §2.7 `each`, `from`, …). |

## Explosion

A radial impulse from a point.

```json
{ "type": "explosion", "at": 2.0, "center": [960, 700], "strength": 1800, "radius": 900, "falloff": "smooth", "spin": 300 }
```

| Field | Type | Default | Notes |
|---|---|---|---|
| `at` | time | required | |
| `center` | `[x, y]` comp px, or a layer id | required | A layer id uses that layer's anchor position at `at`. |
| `strength` | px/s | required | Velocity added at the centre, directed away (negative implodes). |
| `radius` | px | 600 | Beyond it nothing is affected. |
| `falloff` | `none` / `linear` / `smooth` | `smooth` | 1, 1 − x, or 1 − (3x² − 2x³) with x = d / radius. `inverseSquare` here is `physics.unavailable`. |
| `spin` | °/s | 0 | Random spin up to ±this, seeded. |
| `mode`, `targets` | | `velocity`, `"*"` | As impulse. |

## Fields

Continuous forces over a span. Common fields:

| Field | Type | Default | Notes |
|---|---|---|---|
| `targets` | target(s) | `"*"` | |
| `from` (alias `at`) | time | the simulation start | |
| `to` (alias `until`) | time | the simulation end | |
| `ramp` | seconds | 0 | Weight rises 0 → 1 over `ramp` after `from` and falls over `ramp` before `to`. |
| `mode` | `acceleration` / `force` | `acceleration` | Mass-independent acceleration, or a force (heavy bodies move less). Not on `drag`. |

| Type | Own fields | Effect |
|---|---|---|
| `wind` | `vector` `[ax, ay]` px/s² (`[0, 0]`); `turbulence` `{ "amount": px/s² (0), "scale": px (100), "speed": cells/s (0.5) }` | Constant acceleration plus seeded two-octave curl noise (`scale` ≤ 0 is `doc.type`). |
| `attractor` | `center`, `strength` px/s² (negative repels), `radius` (600), `falloff` (`linear`) | Pull toward a point. |
| `vortex` | `center`, `strength` px/s² tangential (positive clockwise), `pull` px/s² inward (0), `radius` (600), `falloff` (`linear`) | Swirl around a point. |
| `drag` | `amount` 1/s | Extra linear damping over the span (slow-motion "thickening"). |

`center` is a point `[x, y]` (default the comp centre), the id of a whole-layer **body** (the field follows its live simulated position), or any other layer's id (its anchor position from its own animation, sampled over the span). Falloff at distance r for radius R: `none` 1 inside / 0 outside; `linear` 1 − r/R inside / 0 outside; `inverseSquare` 1 inside / (R/r)² outside (the one that reaches across the frame).

```json
{ "type": "attractor", "center": "target", "strength": 900, "radius": 250, "falloff": "inverseSquare", "from": 0, "to": 3, "ramp": 0.4 },
{ "type": "wind", "from": 2.5, "to": 5, "vector": [120, 0], "turbulence": { "amount": 300, "scale": 400, "speed": 0.8 }, "targets": "sign" }
```

## Joints

Every end (`a`, `b`, a chain's `from`/`to`) is a body (a layer id) or a fixed comp point `{ "point": [x, y] }`; at least one end is a body and the two differ (`doc.type`); an end naming no body is `physics.unknown_target`. Every joint takes an optional `id` (diagnostics name it; default `_<type><index>`).

| Type | Fields | Use |
|---|---|---|
| `hinge` | `a`, `b`, `at` (the pivot, a comp point at the start; default the point end, or `b`'s anchor), `limits` `[min°, max°]` relative to the start pose (`[0, 0]` holds it), `motor` `{ "speed": °/s, "maxTorque": n }` | Swinging signs, doors, pendulums, flaps. |
| `rope` | `a`, `b`, `anchorA`, `anchorB` (body-local px), `length` (default the anchors' start distance) | A tether, slack until taut. Not drawn. |
| `spring` | `a`, `b`, `anchorA`, `anchorB`, `restLength` (start distance), `stiffness` 1/s² (50, ≈ 1.1 Hz, mass-independent), `damping` 1/s (2) | Bouncy connections. |
| `weld` | `a`, `b` | Two bodies act as one. |
| `chain` | `from`, `to`, `anchorFrom`, `anchorTo`, `links` 2–64 (8), `length` (the anchors' gap), `linkWidth` px (8), `style` `{ "stroke": colour, "width": px }` or `"hidden"`, `settle` (a body `settle` for every link; `to` `layout`/`initial`/`rest`), `motionBlur` | A hanging chain of capsule bodies joined by hinges. |

Hinge and weld ends do not collide with each other; rope and spring ends do. A chain expands in normalization into `links` capsule bodies `<id>.link0…`, `links + 1` hinges `<id>.j0…`, and one generated shape layer per link (inserted under the lowest body layer it hangs from, drawing the link as a round-capped stroke); a chain no longer than its gap is laid taut, a longer one sags on a parabola. Link bodies count toward the 2,000-body cap and are what forces target.

```json
"joints": [
  { "id": "hang", "type": "chain", "from": { "point": [540, 0] }, "to": "sign", "anchorTo": [0, -130], "links": 10, "length": 380, "linkWidth": 10, "style": { "stroke": "#3A3A3A", "width": 6 } },
  { "id": "door", "type": "hinge", "a": { "point": [700, 260] }, "b": "flap", "limits": [-10, 80] },
  { "id": "tether", "type": "rope", "a": { "point": [760, 600] }, "b": "ball", "length": 260 },
  { "id": "bob", "type": "spring", "a": { "point": [560, 900] }, "b": "box", "anchorB": [0, -50], "restLength": 120, "stiffness": 60, "damping": 1.5 }
]
```

Full example: `examples/physics-joints.motion.json` (a sign on a chain kicked by an impulse and swayed by turbulent wind; a hinge, a rope, a spring; an attractor and a vortex in a nested zero-g comp).
