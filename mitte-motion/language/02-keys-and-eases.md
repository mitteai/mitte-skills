# 02. Keyframes, eases, motion paths, loops, separate dimensions, layer timing, motion blur

Scope: spec 2 §2.1–2.5, 2.10–2.12, 2.14 (keys, every ease form and every catalog name, interpolation, motion paths, roving keys, loops, layer timing, motion blur, separate dimensions). Tweens and staggers: [03-timeline-and-tweens.md](03-timeline-and-tweens.md). Presets and drivers: [04-presets-and-drivers.md](04-presets-and-drivers.md). Generated tables: `Key`, `Ease`, `SpringEaseObject`, `CurveEase`, `DimsEase`, `AeEaseObject`, `AeInfluence`, `KeyPath`, `LoopSpec`, `LoopObject`, `MotionBlurSettings` in `92-schema-types-*.md`.

Design rule: canonical animation is After Effects animation (keys with temporal and spatial interpolation, loops, drivers, time remap); authored animation is GSAP-shaped (tweens). The normalizer compiles tweens to keys exactly.

## 1. Keyframes

```jsonc
"position": { "keys": [
  { "t": 0,   "v": [960, 1200], "ease": "expo.out" },
  { "t": 0.8, "v": [960, 540],  "ease": "hold" },
  { "t": 3.0, "v": [960, 540],  "ease": [0.7, 0, 0.84, 0] },
  { "t": 3.6, "v": [960, -200] }
]}
```

| Field | Type | Required | Notes |
|---|---|---|---|
| `t` | time | yes | In the **layer's** time (= comp time unless the layer has `offset`/`stretch`, §10). Strictly increasing (`anim.unsorted_keys`); two keys at one tick: `anim.duplicate_key`. |
| `v` | value | yes | The property's type. May be a `$` reference or a percent string (positions, anchors) in authored form. |
| `ease` | ease | no | The curve of the segment that **starts at this key**. Default `linear`, always: the theme's `ease.default` applies to tweens and presets, never to explicit keys. Ignored on the last key. |
| `path` | `{ in, out }`, `"auto"`, `"continuous"`, `{ "type": "continuous", in?, out? }` | no | Spatial properties only (§7); on a non-spatial property `anim.path_on_nonspatial`. |
| `rove` | boolean | no | Roving key (§8). Not on the first or last key (`anim.rove_endpoint`); never on tween-generated keys. |
| `aeIn`, `aeOut` | `{ speed, influence }` | no | After Effects speed/influence on this key (§4). Authored only. |
| `firstVertex` | integer or `"auto"` | no | Path-valued keys (masks, shape paths): the vertex of this key's path that matches vertex 0 of the previous key's. Authored only; the normalizer rotates the path and removes it ([07-shapes.md](07-shapes.md) §5). |
| `id` | id | no | For editing tools. |

Before the first key the property holds the first key's value; after the last, the last value, unless a loop (§9) says otherwise. ≤ 10,000 keys per property (`limit.keys`).

## 2. Eases: every form

An ease maps segment progress *u* ∈ [0, 1] (fraction of the segment's time) to value progress *p*; *p* may leave [0, 1] (overshoot).

| Form | Example | Notes |
|---|---|---|
| catalog name | `"expo.out"`, `"back.out(2.2)"`, `"steps(8, start)"` | §3. A bare family means `.out` (`"expo"` = `"expo.out"`). Unknown name: `anim.ease_unknown`; bad parameters: `anim.ease_params`. |
| cubic-bezier | `[0.2, 0, 0, 1]` | `[x1, y1, x2, y2]`, CSS/Lottie form; `x1`, `x2` ∈ [0, 1], `y` may overshoot. |
| spring string | `"spring"`, `"spring(300, 10)"` | Defaults stiffness 170, damping 26, mass 1 (ζ ≈ 0.997, no visible overshoot); `spring(stiffness, damping)`. §5. |
| spring object | `{ "spring": { "stiffness": 180, "damping": 12, "mass": 1, "velocity": 0, "settle": 0.001 } }` | §5. `damping` ≤ 0 is `anim.spring_unstable`. |
| theme spring token | `"$theme.spring.snappy"` | `{ bounce, duration }` (Apple-style) or `{ stiffness, damping, mass }`; [13-components-themes-data.md](13-components-themes-data.md) §1.3. |
| custom curve | `{ "curve": [[0, 0], [0.3, 1.15], [0.55, 0.95], [0.75, 1.02], [1, 1]] }` | Monotone-in-*u* Catmull-Rom through the points; first `(0,0)`, last `(1,1)`, *u* strictly increasing. GSAP CustomEase with points. |
| per-dimension | `{ "dims": ["expo.out", "back.out(2)"] }` | One ease per dimension of a **non-spatial** vector (scale squash-and-stretch). On a spatial property: `anim.ease_on_spatial_dims` (separate the dimensions instead, §12). |
| After Effects speed/influence | `aeIn`/`aeOut` on the keys | §4; canonical zero-delta form `{ "ae": { … } }`. |
| theme ease token | `"$theme.ease.enter"` | Resolves to any of the above. |

Catalog names and cubic-beziers are kept as written in canonical form; tokens and aliases are resolved.

## 3. The ease catalog

Every family has `.in`, `.out`, `.inOut`. Derivations: `.out(u) = 1 − .in(1 − u)`; `.inOut(u) = .in(2u)/2` for *u* < ½, else `1 − .in(2 − 2u)/2`. Parameters go in parentheses.

| Name | `.in` definition | Parameters (defaults) | Aliases / notes |
|---|---|---|---|
| `linear` | *p = u* | — | alias `none` |
| `hold` | *p = 0* for *u* < 1 | — | the value jumps at the next key |
| `power1` | *u²* | — | alias `quad` |
| `power2` | *u³* | — | alias `cubic` |
| `power3` | *u⁴* | — | alias `quart` |
| `power4` | *u⁵* | — | aliases `quint`, `strong` |
| `sine` | 1 − cos(*u*·π/2) | — | |
| `expo` | 2^(10(*u*−1)), *p*(0) forced to 0 | — | the standard "premium UI" ease; Penner's values kept, so `.in` starts with a 0.1 % step |
| `circ` | 1 − √(1 − *u²*) | — | |
| `back` | *u²*((*s*+1)*u* − *s*) | `s` (1.70158) | anticipation (`.in`) / overshoot (`.out`): `back.out(2.5)` |
| `elastic` | −*a*·2^(10(*u*−1))·sin((*u*−1−*s*)·2π/*p*), *s* = *p*/4 for *a* ≤ 1 else *p*/(2π)·asin(1/*a*) | `a` (1, amplitude ≥ 1), `p` (0.3, period) | `elastic.out(1.2, 0.35)` |
| `bounce` | Penner's four-arc bounce | — | `bounce.out` lands like a ball |
| `steps` | ⌊*u*·*n*⌋/*n* (`end`); ⌈*u*·*n*⌉/*n* (`start`); (⌊*u*·*n*⌋+1)/(*n*+1) (`both`); min(1, ⌊*u*·*n*⌋/(*n*−1)) (`none`, *n* ≥ 2) | `steps(n, jump)`: `n` integer ≥ 1; `jump` ∈ `end` (default), `start`, `both`, `none` | no `.in`/`.out`; `steps(12)` for stop-motion |
| `spring` | the spring step response | `spring(stiffness, damping)` | §5; no `.in`/`.out` |
| `easy` | cubic-bezier(0.333, 0, 0.667, 1) | — | After Effects Easy Ease; `easy.in` = (0.333, 0, 1, 1) (= AE "Easy Ease Out" on the segment's start key), `easy.out` = (0, 0, 0.667, 1) (= AE "Easy Ease In") |
| `smooth` | cubic-bezier(0.4, 0, 0.2, 1) | — | Material standard curve |
| `ease` | cubic-bezier(0.25, 0.1, 0.25, 1) | — | CSS `ease`; also `ease-in` (0.42, 0, 1, 1), `ease-out` (0, 0, 0.58, 1), `ease-in-out` (0.42, 0, 0.58, 1) |

Which ease when: entrances `expo.out`/`power3.out` (theme `ease.enter`); exits `.in` of the same family (theme `ease.exit`); position changes between on-screen states the Material curve `[0.2, 0, 0, 1]` (theme `ease.move`); pops `back.out(1.7)` (theme `ease.emphasis`); continuous loops `linear` or `sine.inOut`; cuts `hold`. Lint: `lint.linear_spatial_ease` (linear on a move > 50 px), `lint.same_ease_everywhere` (i), `lint.enter_exit_same_curve` (i).

## 4. After Effects speed and influence

```jsonc
{ "t": 0, "v": 0,   "aeOut": { "speed": 0, "influence": 75 } },
{ "t": 1, "v": 500, "aeIn":  { "speed": 0, "influence": 33.33 } }
```

`speed` is in property units per second (a per-dimension array is allowed for non-spatial vectors: `"speed": [0, 120]`); `influence` is one number, 0.1–100 percent of the segment (an array is a schema error). For a 1D segment of duration *T* and change *D* ≠ 0: `x1 = influenceOut/100`, `y1 = speedOut·x1·T/D`, `x2 = 1 − influenceIn/100`, `y2 = 1 − speedIn·(influenceIn/100)·T/D`. A missing side is After Effects' linear default (influence 16.67 %, speed = *D*/*T* per dimension). A zero-delta ("bump") segment stays canonical as `{ "ae": { "outSpeed", "outInfluence", "inSpeed", "inInfluence" } }` and is evaluated in (time, value) space.

## 5. Springs as eases

A spring ease is the normalized step response of a damped harmonic oscillator (position 0 → target 1), evaluated analytically.

| Field | Default | Meaning |
|---|---|---|
| `stiffness` | 170 | |
| `damping` | 26 | > 0 (`anim.spring_unstable` otherwise) |
| `mass` | 1 | |
| `velocity` | 0 | initial velocity in value deltas per real second, before rescaling (`1` = would cover the whole delta in one second) |
| `settle` | 0.001 | the fraction of rest that counts as settled |

The response is computed in real seconds up to its settle time *T_s*; the segment maps *u* ∈ [0, 1] to *t* = *u*·*T_s*, and the value snaps to exactly 1 at the next key. On a spatial segment the spring drives arc-length progress. On a zero-delta segment it is the identity (use the `spring` **driver** for a bump that overshoots and returns). A tween with `"dur": "auto"` and a spring ease takes *T_s* as its duration ([03-timeline-and-tweens.md](03-timeline-and-tweens.md) §1).

## 6. How progress maps to values

| Property kind | Interpolation at progress *p* |
|---|---|
| number | `a + (b − a)·p` |
| non-spatial vector (scale, size, colour components) | per component, same *p* (per-dimension *p* with `dims`) |
| spatial vector (position, anchor, point effect params, light/camera positions, gradient `from`/`to`) | the point at arc-length fraction *p* along the segment's motion path; *p* outside [0, 1] extends along the end tangent |
| colour | in the comp's `color.interpolation` space (`oklab` default, `srgb` = After Effects); alpha linear |
| angle | as a number (no shortest-path wrapping: 350 → 10 turns backwards 340°) |
| `orientation` (3D) | quaternion slerp, shortest arc (use `rotationX/Y/Z` for multi-turn spins) |
| path (masks, shapes) | per vertex and tangent, after vertex matching ([07-shapes.md](07-shapes.md) §5) |
| gradient | per stop position and colour; mismatched stop counts are resampled by the normalizer |
| text, enum, boolean | hold only |

## 7. Motion paths

Spatial properties move along a cubic Bezier from `v[k]` to `v[k+1]` with control points `v[k] + path[k].out` and `v[k+1] + path[k+1].in`.

```jsonc
{ "t": 0, "v": [200, 800],  "path": { "out": [300, -400] } },
{ "t": 1, "v": [1700, 800], "path": { "in": [-300, -400] } }      // an arc over the top
```

| `path` | Meaning |
|---|---|
| absent | **straight line** (the default, unlike After Effects' auto-Bezier) |
| `{ "in": [dx, dy(, dz)], "out": [dx, dy(, dz)] }` | explicit tangents relative to the key's value (After Effects' spatial tangents); one or both sides |
| `"auto"` | auto-Bezier: handles along `P[k+1] − P[k−1]`, in-handle one third of the chord to the previous key, out-handle one third of the chord to the next; at the ends, one third of the only chord |
| `"continuous"`, `{ "type": "continuous", "in", "out" }` | like `auto`, but explicit handles are kept collinear; with one side the other mirrors its direction keeping its own length |

Ease applies to **arc length**: `linear` is constant speed along a curve. `autoOrient: "path"` on the layer follows the tangent ([05-layers.md](05-layers.md) §7).

## 8. Roving keys

`"rove": true` on an interior key of a spatial property with ≥ 3 keys: its time is computed so the speed is even between its neighbours (chains of roving keys are solved together by arc length). The written `t` is replaced in canonical form; `rove` is kept so editors know.

## 9. Loops

```jsonc
"rotation": { "keys": [ { "t": 0, "v": 0 }, { "t": 2, "v": 360 } ], "loop": "cycle" }
"position": { "keys": [ … ], "loop": { "type": "pingpong", "keys": 2, "count": 3 } }
"scale":    { "keys": [ … ], "loopIn": "offset", "loop": "continue" }
```

`loop` extends after the last key (After Effects `loopOut`), `loopIn` before the first (`loopIn`). Either a type string or `{ "type", "keys", "count" }`.

| `type` | After the last key |
|---|---|
| `cycle` | repeat the keyed span |
| `pingpong` | backwards, forwards, alternating |
| `offset` | repeat, adding the span's total change each time (endless rotation from one 0 → 360 pair) |
| `continue` | continue at the last segment's analytic end velocity (ease derivative × *D*/*T*; nearly zero after an `expo.out`) |

`keys: n` (≥ 2) limits the span to the last (first) *n* keys (After Effects' `numKeyframes = n − 1`). `count: n` stops after *n* repeats and holds the value the last repeat ended on (for `pingpong` with odd *n* that is the span's first key). A loop needs ≥ 2 keys (`anim.loop_too_few_keys`). Time is remapped into the span before keys are evaluated, so drivers and expressions still apply after looping.

## 10. Layer timing

```jsonc
{ "id": "clip", "type": "video", "asset": "hero", "in": 2, "out": 7.5, "offset": 1.5, "stretch": 100 }
```

| Field | Type | Default | Meaning |
|---|---|---|---|
| `in` | time | `0` | comp time the layer starts showing |
| `out` | time | comp duration, or for finite media `in + length·|stretch|/100` (length = asset duration × asset `loop`) | stops (exclusive); must be > `in` (`layer.empty_span`) |
| `dur` | time | — | authored: `out = in + dur`; both `out` and `dur` is an error |
| `offset` | time | `in` for `video`, `audio`, `comp`, `particles`; else `0` | the comp time at which layer time is 0 (After Effects "start time") |
| `stretch` | percent | `100` | 200 = half speed; negative plays backwards within the same `[in, out)`; `0` is `layer.zero_stretch` |
| `timeRemap` | animatable time | none | `video` and `comp` layers only (`layer.time_remap_type`): the layer shows its source at `timeRemap(t)`; `hold` segments freeze frames; eases make ramps |
| `frameBlend` | `off` \| `mix` \| `flow` | `off` | how a slowed/remapped media or comp layer shows times between source frames ([11-media-and-audio.md](11-media-and-audio.md) §3.3) |

Layer time = `(compTime − offset)·100/stretch` for positive stretch; for negative stretch `(out − compTime)·100/|stretch|` with `offset` ignored (After Effects time-reverse). **Keyframe times are layer times**: with the defaults (offset 0, stretch 100) they equal comp times. Tweens are written in comp time and converted. Animation keyed outside `[in, out)` still evaluates (expressions may read it); it is just not drawn.

## 11. Motion blur

```jsonc
"comps": { "main": { "motionBlur": { "shutterAngle": 180, "shutterPhase": -90, "samples": 16, "adaptiveLimit": 128, "enabled": true } } }
"layers": [ { "id": "ball", "motionBlur": true } ]
```

| Field | Default | Meaning |
|---|---|---|
| `shutterAngle` | 180 | degrees 0–720; exposure = `angle/360` of a frame; hold keys only (a `whip` transition raises it to 360 for its span) |
| `shutterPhase` | −90 | degrees −360–360; the shutter opens at `phase/360` frames relative to the frame time (−90 with 180 centres the exposure); hold keys only |
| `samples` | 16 | minimum samples per frame (2–256) |
| `adaptiveLimit` | 128 | maximum; samples rise until consecutive samples move content ≤ 1 px |
| `enabled` | true | comp-wide switch |

Layers opt in with `motionBlur: true`. Samples are stratified deterministically and accumulated in linear light. Masks have their own switch (`masks[].motionBlur`). Nested comps: a comp layer with motion blur and `collapse: true` uses the parent's shutter; without collapse the nested comp's settings apply inside it. Lint: `lint.motion_blur_off_fast_motion` (> 40 px per frame without blur), `lint.motion_blur_on_scroll_text`, `lint.expr_mb_cost`.

## 12. Separate dimensions

```jsonc
"position": { "x": { "keys": [ { "t": 0, "v": 200 }, { "t": 1, "v": 1700, "ease": "expo.out" } ] }, "y": 540 }
```

`position` (2D or 3D) may be stored per dimension, each a number property with its own keys, eases, drivers (After Effects "Separate Dimensions"). Rules: a separated position is non-spatial (no motion path, eases per dimension); an unwritten dimension is **0** (write every dimension you mean); `z` exists only when written; a driver on a dimension seeds from the dimension's own path (`layer.position.x`), so `wiggle` on `.x` and `.y` are independent. The normalizer separates when tweens or keys address more than one of `.x`/`.y`/`.z`; a single keyed dimension beside static ones is rejoined into whole-vector keys. Explicit keys on both the whole vector and a dimension: `anim.dimension_mix`. Separating a property that carries `path` tangents or roving keys is refused (`anim.separate_discards_path`): remove the paths or tween the whole `position`. `scale` has no separated form (`scaleX`/`scaleY`/`scaleZ` tween shorthands write whole-vector keys).

## 13. Evaluation guarantees

Pure (a property's value is a function of time; `spring` drivers and particle systems are simulated from a fixed start with fixed steps), any order (frames in any order, in parallel, on any machine: identical), exact (tick times, f64 progress, f32 only for pixels).

## 14. Examples

`examples/02-keys-eases.json` exercises every ease form (catalog names with parameters, a bezier, a spring string and object, a custom curve, `dims`, `aeIn`/`aeOut`), a motion path with explicit tangents and `"auto"`, a roving key, `cycle`/`offset`/`pingpong` loops with `keys` and `count`, separate dimensions, `stretch`/`offset` on a comp layer with `timeRemap`, and comp motion blur with a layer opted in. It checks with 0 errors; two warnings are expected: `lint.linear_spatial_ease` on the deliberately linear path segment of `arc`, and `lint.missing_exit` on the nested comp layer, which is cut at its `out` without an exit (the spinner with `motionBlur: false` rotates in place, so it does not trip `lint.motion_blur_off_fast_motion`, which measures translation).

