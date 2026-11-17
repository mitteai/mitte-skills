# 2D physics 3: the hand-off, the bake, settle, seeds and locks, limits, diagnostics

Spec 19 §19.6–19.13.

## The keyframe-to-physics hand-off

A dynamic body with `start` after the world's `start` is designed first and simulated after:

1. **Before `start`** the layer follows its own animation (keys, eases, drivers, expressions, spatial tangents); in the world it is kinematic (others collide with it) or a ghost (`before: "ghost"`).
2. **At `start`** it becomes dynamic with the layer's pose at `start` and the velocity of the designed motion (the backward difference at the simulation step: `v = (p(start) − p(start − 1/rate)) · rate`, spin likewise), plus the body's own `velocity` and `spin`. The approach driven by a driver or an expression is written into the canonical document as per-frame keys up to the hand-off, so the designed motion survives. `audio` drivers are the one thing the pass does not evaluate (normalization decodes no audio): they read as the value before them.
3. **After `start`** the simulation owns `position` and `rotation`; later keys are ignored (`physics.keys_after_start`).

A `start` inside a tween's span discards the rest of the tween; end the tween at `start` so the pieces arrive with their tween velocity (spec 19 §19.14.3 throws four logo pieces in with `power2.in` tweens ending at 0.6 s and hands off at 0.6 s).

## The bake

Physics is normalization pass 22, after spatial paths, expressions and tracks. Per comp with `physics`: compute the input hash → use a locked or cached bake if one matches → else build the world (floor, walls, colliders in sorted body-id order, kinematic tracks sampled at `rate`), step from `start` to `end` applying forces and hand-offs, apply `settle`, write the bake and rewrite the comp.

**What the canonical document gets** (the keys form, what `motion.check` returns today): per-frame `position`/`rotation` keys on whole-layer bodies (linear segments, unwrapped rotation, rest spans trimmed into holds), one range-selected animator per unit on text bodies (`_physics…`), and a top-level `sims` map: `{ "<hash>": { "comp", "rate", "start", "steps", "bodies", "asset" } }`. Keys are the canonical form (spec 19 §19.7.5): the `{ "sim": hash, "body": id }` references and the `_physics` animator of earlier drafts are not produced, there is no `bake` option, and motion blur between frames is linear (a bounce inside one shutter interval does not show). The `.sim` file is the cache and lock store and an inspection artefact; the renderer never reads it.

**The input hash** covers only what can change the simulation: the engine and Rapier versions, the `physics` object (times in ticks), every body (its `body`, its pose at `start`, the collider geometry as built, kinematic poses per step), the comp size and safe box. Colours, opacity, effects, non-body layers and anything outside the span do not change it: editing them reuses the bake.

**Caches.** Unlocked bakes live in the box's sim cache (`--sim-dir`, `/var/cache/rexx/sim/<hash>.sim`, LRU); `check --sims` writes new ones to the job's scratch and lists them as `sims: [{ comp, hash, file }]`, and the service uploads each as a `sim` asset and returns `{ comp, hash, url, sha256 }` (`motion.check` with `sims: "url"`). A `.sim` file is the binary `MESIM` v1 sidecar (header, body table, deflated XOR-delta tracks, the labelled hash parts, a CRC); over 64 MB is `limit.physics_bake`.

**Sampling.** The renderer reads the keys like any keyframes; motion blur sub-samples see the per-frame linear segments. Bodies whose content is static are rasterized once and resampled along the baked path.

## Settle

`settle` blends a body from the simulation into a target pose, so things tumble freely and still end where the layout needs them.

| Field | Type | Default | Notes |
|---|---|---|---|
| `at` | time | required | When blending starts. From `at` the body is kinematic, following the blend, so others still collide with where it is. |
| `dur` | time | 0.6 | |
| `to` | `layout` / `initial` / `rest` / `{ "position": [x, y], "rotation": deg }` | `layout` | `layout`: where the layer's own animation puts it at `at + dur` (a text unit: its laid-out place). `initial`: the pose at its `start`. `rest`: the simulated pose at `at`, frozen. An object: an explicit pose (`physics.settle_target` when malformed). |
| `ease` | ease | `power2.inOut` | Overshooting eases (`back.out`) overshoot the target: a good snap. |
| `stagger` | stagger object | none | For `per` text bodies: offsets `at` per unit in body-unit order. A whole-layer body is one unit; give several bodies their own `at`. |

The blend: x, y and rotation are frozen at their simulated values at `at` and mixed to the target by the eased weight; the target rotation is taken modulo 360° nearest the simulated one (a body that rolled two turns settles the short way; a difference still over 90° warns `physics.settle_spin`).

## Seeds and variations

The same inputs give the same take; change `seed` for another. Only the random fields see it: `vary`, impulse `spread`, explosion `spin`, wind `turbulence`. `motion.frames` with `"seeds": [1, 2, 3, 4]` and `"sheet": true` simulates once per seed and returns one contact sheet with a row per seed (≤ 6 seeds); when the document's `vary` is all zero the tool uses `{ "velocity": 60, "spin": 45, "rotation": 4, "position": 0 }` for the exploration and says so, so the chosen take is written back with both `seed` and `vary`. Each variation's bake lands in the sim cache.

## Locking a take

1. `motion.check` with `"sims": "url"` uploads the comp's bake and returns `sims: [{ "comp", "hash", "url", "sha256" }]`.
2. Declare it and lock: `"assets": { "take1": { "src": "<url>", "type": "sim", "sha256": "…" } }`, `"physics": { …, "lock": { "asset": "take1", "hash": "<hash>" } }`.
3. Every later normalization recomputes the hash: equal → the locked take stands in for the simulation (no stepping); different → **stale**: simulated fresh with `physics.lock_stale` naming the changed inputs (`gravity`, `body c00 collider`, `force 1 (new)`, …, from the labelled parts in the file); `"force": true` keeps the stale take as long as every body id still exists with the same kind and start step and the timing is unchanged (`physics.lock_forced` info; `physics.lock_bodies_mismatch` otherwise). `lock.asset` must be a declared `sim` asset that reads and holds `lock.hash` (`physics.lock_missing`); a lock without `hash` just records the asset.

## Determinism, performance, limits

Same inputs and engine version → a byte-identical bake on every box (Rapier pinned with `enhanced-determinism`, sorted insertion, `libm` initial values, one thread per comp; the golden bakes are hashed per track in CI). Cost: tens of ms for a word per character, 0.3–2 s for a 300–500 body pile, 3–15 s at the 2,000-body cap; `physics.many_bodies` warns above 500.

| Limit | Value | Code |
|---|---|---|
| Bodies per comp (text units and chain links included) | 2,000 | `limit.physics_bodies` |
| Simulation rate | 60–960 Hz, ≥ fps | `physics.rate_range` |
| Simulated span | ≤ the comp, ≤ the rendered-duration cap | `physics.span` |
| Encoded bake | 64 MB | `limit.physics_bake` |
| Convex parts / vertices per part | 64 / 256 | `physics.shape_too_complex` |
| Joints, forces per comp | 1,000, 256 | `limit.physics_joints`, `limit.physics_forces` |

**Tunnelling.** A body that moves more than half its thinnest dimension in one step near another collider warns `physics.tunneling_risk` (body and time): raise `rate`, `inset: -2`, or `ccd: true`.

## Diagnostics

Errors block rendering; warnings and infos do not (silence by code with `lint.disable`).

| Code | Severity | Meaning |
|---|---|---|
| `physics.no_world` / `physics.no_bodies` | error | `body` without `physics`, or `physics` without a body. |
| `physics.body_not_allowed`, `physics.layer_3d`, `physics.parent_moves`, `physics.per_not_text` | error | Where a body may sit ([50](50-physics-world-bodies.md)). |
| `physics.text_animator_conflict`, `physics.text_layer_animates` | error | A `per` body's units or layer move during the span. |
| `physics.shape_empty`, `physics.shape_too_complex` | error | No collidable geometry; decomposition over the caps. |
| `physics.unknown_target` | error | A force or joint target matches no body. |
| `physics.rate_range`, `physics.span` | error | Out-of-range rate or span. |
| `physics.unavailable` | error | `inverseSquare` on an explosion, or more than 30 named groups. |
| `physics.non_finite` | error | The solver produced NaN/∞ (extreme values); the bake is discarded. |
| `physics.lock_missing`, `physics.lock_bodies_mismatch`, `physics.settle_target`, `physics.cycle`, `physics.reserved_group` | error | See their sections. |
| `limit.physics_bodies`, `limit.physics_bake`, `limit.physics_joints`, `limit.physics_forces` | error | The limits above. |
| `physics.lock_stale` | warning | The locked take no longer matches; simulated fresh. |
| `physics.overlap_at_start`, `physics.tunneling_risk` | warning | Names the pair / body and time. |
| `physics.unknown_group` | warning | A `collides` entry names a group no body is in (nor `world`); it admits nothing. |
| `physics.keys_after_start`, `physics.content_animates`, `physics.static_animates`, `asset.unreadable` | warning | Ignored animation; a box fallback for unreadable pixels. |
| `physics.unsettled_at_end` | warning | Bodies still moving > 2 px/frame at the comp's end without `settle`. |
| `physics.offscreen` | warning | A body leaves the comp for good while visible. |
| `physics.settle_spin`, `physics.rate_low`, `physics.many_bodies` | warning | See their sections. |
| `physics.single_body`, `physics.seed_no_effect`, `physics.lock_forced`, `physics.soft_stack`, `physics.idle_span` | info | Advice. |

## Interchange

After Effects and Lottie receive the per-frame keys (a `.jsx` header note says the motion was simulated); a text-unit body exports as a text animator with a range selector; chain link layers export as the shape layers they are. The `.sim` file is an engine cache artefact, not an interchange format.
