# Tracking 3: using tracks in documents

All track sugar is **authored only**: the Tracks normalization pass (pass 21, after expressions, before physics) loads each referenced track asset, checks its `source.sha256` against the footage layer's asset (`track.source_mismatch`) and its version (`track.version`), writes **linear keyframes at every comp frame** (`keysPerFrame` per frame) for every reference, and removes the sugar. Canonical documents contain only keys, `distort.cornerPin` effects, camera keys and nulls; After Effects and Lottie receive those keys.

The track is an asset of type `track`; the footage is a `video` asset on a layer of the same comp:

```json
"assets": { "clip": { "src": "https://media.mitte.ai/u/a1/clip.mp4", "type": "video" },
            "shoeTk": { "src": "https://media.mitte.ai/u/a1/clip.track.json", "type": "track" } }
```

## A property follows a track (`{ "track": … }`)

Any spatial property (layer `position`, `anchor`, point-type effect parameters such as `light.rays` `center`) can take its value from a track item:

```json
"position": { "track": { "asset": "shoeTk", "item": "heel", "layer": "clip", "use": "position",
                         "offset": [0, -120], "smooth": 0.1, "lost": "hold", "range": [0.5, 8], "keysPerFrame": 1 } }
```

| Field | Default | Notes |
|---|---|---|
| `asset` | required | A `track` asset (`track.asset_type` otherwise; a track that cannot be read is `track.asset_missing`). |
| `item` | the only item | Item id; `"pair"` for a two-point solve; `track.item_missing` when absent from the file. |
| `layer` | required | The footage layer the track was computed on, in the same comp, 2D (`track.layer_3d`), not parented in a cycle with the target (`track.cycle`). Its `box`/`fit`/`focus`, transform (keys, drivers, expressions) and timing (`offset`, `stretch`, `timeRemap`, `loop`) map source pixels and source time into comp space and comp time, so the graphic stays attached when the clip is trimmed, slowed, scaled into a split-screen box or moved. |
| `use` | `position` | `position` replaces the property. `rotation` and `scale` (from the `pair` item, or a `shape` point track) **compose** with a base: `{ "value": 30, "track": { "use": "rotation", … } }` adds, `{ "value": [100, 100], "track": { "use": "scale", … } }` multiplies; the base may also be keys. Face tracks: `position` of a `landmark`, `rotation` the head roll; `scale` on a face track is `track.type_mismatch`. |
| `offset` | `[0, 0]` | Added in the target's parent space after mapping. `"keep"`: computed so the target's position at the first tracked frame equals its authored position (the "attach where I put it" behaviour). |
| `smooth` | 0 | Seconds of confidence-weighted Gaussian smoothing (σ = smooth / 2), ignoring lost samples. Removes jitter. |
| `lost` | `hold` | `hold` the last good value; `extrapolate` the last 0.2 s of velocity, decaying; `hide` fades the target's opacity to 0 over lost spans (linear keys: from 100 two comp frames before the first lost frame to 0 on it, and back to 100 two frames after the last; conflicts with animated opacity: `track.hide_conflict`). |
| `range` | the overlap of target and footage | `[in, out]` comp seconds the track drives the property; outside, the property's other keys or value apply. |
| `keysPerFrame` | 1 | 1–4; 2 or more gives motion-blur sub-samples true intermediate positions (lint `lint.track_fast_motion` suggests it above 40 px per frame with motion blur on). |
| `landmark` | `center` | Face tracks: one of the 26 landmark names or `center`. |

Drivers and expressions still apply on top of a tracked value (a `wiggle` sees the tracked position as its base). A target with `timeRemap`, or with `stretch` ≠ 100 and `keysPerFrame` > 1, cannot take tracked keys (`track.target_timing`). The same code refuses a reference that needs more keys than a property may hold (10,000: frames × `keysPerFrame`, so 5.5 minutes at 30 fps with one key per frame, 83 s with four); the pass never writes a shortened key list that would freeze the target mid-clip. Shorten `range`, lower `keysPerFrame`, or split the target over several layers.

A static base `value` (or `keys`) beside a `rotation` or `scale` track is the base the tracked delta composes with (`{ "value": 30, "track": { "use": "rotation", … } }` writes keys at 30 + the tracked rotation); beside a `position` track it is still `anim.value_and_keys` (the track replaces the position).

Mapping, per key time T: layer time through the footage layer's `timeRemap` or `offset`/`stretch` (and `loop`); the sample at that source time (linear between the two nearest samples; corners per corner; rotation unwrapped; a lost neighbour makes the result lost); source px → layer space through `box`/`fit`/`focus`; layer → comp through the footage layer's full transform at T; comp → the target's parent space; `offset`; and the key is written at the target's own layer time.

## `pin`: corner pin to a planar (or face) track

```json
{ "id": "newScreen", "type": "image", "asset": "appShot",
  "pin": { "asset": "phoneTk", "item": "screen", "layer": "clip", "fit": "cover", "inset": 4, "smooth": 0.05, "lost": "hold" },
  "matte": { "layer": "handMatte", "mode": "alphaInverted" } }
```

The layer's transform is set to the identity in comp space (a pinned layer may not have its own transform keys, a parent or 3D: `track.pin_transform`); its content rect (`box` for images, video and comps; the content bounds for text and shapes) is fitted to the quad (`fit` `fill` default: mapped as is; `cover` / `contain`: first fitted to the quad's average aspect, cover spilling outside the quad unless a matte clips it), and a `distort.cornerPin` effect is appended with its four corners keyed per comp frame, moved inward by `inset` px along the diagonals. Occlusion (fingers over a screen) is a matte from a segmentation tool, not the pin's job. With a face track the quad is the face's bounding box rotated by the head roll.

## `stabilize`: inverse of a stabilize track on the video layer

```json
{ "id": "clip", "type": "video", "asset": "clip", "stabilize": { "asset": "walkStab", "amount": 100 } }
```

`position`/`similarity` tracks write `anchor`, `position`, `rotation` and `scale` keys on the video layer (which must have no transform keys of its own: `track.stabilize_transform`) plus the crop scale; `perspective` tracks append a keyed `distort.cornerPin`. `amount` 0–100 scales the correction toward identity. Graphics over a stabilized clip no longer need tracking for camera shake; they still need a point or planar track to follow objects in the scene.

## Camera `solve` and anchors

```json
{ "id": "cam", "type": "camera",
  "solve": { "asset": "camTk", "layer": "clip", "anchors": { "floor": { "on": "ground", "at": [0, 160] }, "mark": { "point": 34 } } } },
{ "id": "welcome", "type": "text", "text": "WELCOME", "threeD": true, "parent": "cam.floor", "transform": { "rotationX": -90, "position": [0, 0, 0] } }
```

The camera layer's `position`, `orientation` and `zoom` are keyed once per comp frame from the camera track (file coordinates scaled uniformly about the centres, z included; lost spans hold); it becomes a one-node camera and `solve`, `pointOfInterest`, `focalLength` are removed. The camera layer must carry no motion of its own (keys, a parent, rotations: `track.camera_layer`), and the comp needs `renderer3d: "classic"`. The footage layer must be 2D, unparented, unanimated and mapped to the comp by one uniform scale about the centres that covers it; today only a clip at the comp's own size lines up (the renderer does not apply a footage layer's `box`/`fit` to a solved camera yet).

Anchors generate 3D null layers `<cam>.<anchor>` right after the camera: `{ "on": "ground", "at": [u, v] }` on the ground plane (`at` in comp px along the plane's `xAxis` and the in-plane perpendicular, positive away from the camera; a track without a ground plane is `track.item_missing`: re-track with `camera.ground` picks or anchor to a point), or `{ "point": n }` at solved point *n* of `camera.points`. Each null is oriented to the ground plane (x along `xAxis`, y along the plane's down normal). Parent 3D layers to them: a text with `rotationX: -90` under a ground anchor lies flat on the floor; a layer with a negative y under a point anchor stands above the point. A camera track referenced from a property's `track` is `track.type_mismatch`.

## Face tracks

A property follows a landmark (`"track": { …, "landmark": "noseTip" }`; unknown names list the 26 in the hint); `use: "rotation"` follows the head roll; `pin` pins to the face quad; a mask follows the outline: `"masks": [ { "id": "face", "track": { "asset": "faceTk", "item": "host", "layer": "clip", "use": "outline" } } ]` keys the mask's `path` per frame (straight segments) in the masked layer's space. `use: "outline"` belongs only on a mask's `track` with a face track, and a mask's `track` takes only that `use`.

## Physics and tracks

A kinematic body ([50-physics-world-bodies.md](50-physics-world-bodies.md)) whose layer is driven by a track is sampled at every simulation step, so letters land on a tracked product and bounce off it between frames too.

## Document diagnostics

| Code | Meaning |
|---|---|
| `track.source_mismatch` | The track's `source.sha256` differs from the footage layer's asset. |
| `track.version` | A track format newer than the engine. |
| `track.layer_missing`, `track.layer_3d` | `layer` absent/unknown, or a 3D footage layer. |
| `track.pin_transform`, `track.stabilize_transform`, `track.camera_layer` | A pinned/stabilized/solved layer carrying motion of its own (or an unsuitable footage layer for a solve). |
| `track.hide_conflict` | `lost: "hide"` on a layer whose opacity is already animated. |
| `track.item_missing`, `track.type_mismatch`, `track.asset_type`, `track.asset_missing`, `track.target_timing`, `track.cycle` | See the tables above. |
| `lint.track_fast_motion` (w) | > 40 px per frame with motion blur on and `keysPerFrame: 1`. |
| `lint.track_outside_range` (w) | The target is visible beyond the track's range. |

## Examples

`examples/tracking-point.motion.json` (a label with `offset` and `smooth`, a dot with `offset: "keep"`), `examples/tracking-stabilize.motion.json`, `examples/tracking-camera.motion.json` (a solve with a ground anchor and a point anchor), all on the 36-frame golden clip with the track files under `examples/assets/`; `scripts/skills-effects-check-examples.sh` checks them through an assets manifest (`rexx-engine check --assets`), which is what the service writes for the engine.
