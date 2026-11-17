# Tracking 1: `motion.track`, the track types, inputs and corrections

Tracking is analysis, not rendering: `motion.track` reads a video and writes a **track file** (`<clip>.track.json`, a `track` asset) that says where something is on every frame; a document then attaches graphics to it with authored sugar that normalization turns into plain keyframes ([62-tracking-documents.md](62-tracking-documents.md)). The file format is on [61-tracking-files.md](61-tracking-files.md). Every type below is implemented by the engine (`rexx-engine track`, spec 18; the P3 types `camera` and `face` included); only `method: "ml"` is not.

## Types

| `type` | Follows | Output per frame | After Effects | Items |
|---|---|---|---|---|
| `point` | One or more small features; with 2 items and `solve: "similarity"`, one rigid pair | position (+ feature rotation and scale with `shape`); the pair's centre, rotation, scale | Track Motion | yes |
| `planar` | A flat surface (screen, sign) | four corners + the homography from the reference frame | Mocha-style planar, Corner Pin | yes |
| `mask` | The pixels inside a mask outline | the path per frame | Track Mask | yes |
| `stabilize` | The camera's 2D motion | a corrective 3×3 per frame + a crop scale | Warp Stabilizer (global) | no |
| `camera` | The camera in 3D | position, orientation, focal; a point cloud; a ground plane; a lens | 3D Camera Tracker | no |
| `face` | A face | 48-point outline, 26 named landmarks, head pose | Face Tracking | yes |

## The tool

```json
{ "video": "https://media.mitte.ai/u/a1/clip.mp4", "type": "point",
  "items": { "heel": { "at": [812, 440] } }, "preview": "sheet" }
```

| Field | Type | Default | Notes |
|---|---|---|---|
| `video` | https URL or `library:<ns>/<path>@<v>` | required | The clip (`library:mitte/demo/tracking-clip@1` is the demo clip). |
| `type` | enum | required | `point`, `planar`, `mask`, `stabilize`, `camera`, `face`. |
| `items` | map id → item | required for point/planar/mask/face; forbidden for stabilize/camera | In **source pixels** (the display frame: rotation and pixel aspect applied; pixel *i* spans [i, i+1)) on the frame at `from`. Ids follow spec 1 syntax. Limits: 32 point/face items, 8 region (planar/mask) items per call (`limit.track_items`: 64 in the engine). |
| `from` | seconds ≥ 0 | the range start | The reference frame where items are defined. |
| `range` | `[start, end]` seconds | the whole clip | `end > start ≥ 0`; empty or outside the clip: `track.range_empty`. At most 120 s of footage per call (`limit.track_duration`; use `range`); a camera solve at most 3,000 frames (100 s at 30 fps), refused up front with `413`. |
| `direction` | `forward` / `backward` / `both` | `forward` (`both` when `from` is past the range start) | Which way the open ends are tracked from `from`. |
| `method` | `classic` / `ml` | `classic` | `ml` is refused by the service ("retry with method classic") and by the engine (`track.unavailable`). |
| `options` | object | defaults | Below. |
| `corrections` | list | `[]` | Below. |
| `base` | https URL | none | A previous track of the same type: only the segments corrections split are re-tracked (point and planar items; mask items re-track whole). `items` may be omitted with a base in the design; **today the engine still requires `items`**. |
| `preview` | `none` / `sheet` | `none` | `sheet`: also return a contact sheet with the track drawn on 12 frames plus the worst-confidence ones, coloured by confidence. Always ask for it: it is how you judge a track. |
| `solve` | `similarity` | none | `point` with exactly two items: solve them as one rigid pair (adds the item `pair`). |
| `stabilize` | object | defaults | `{ "mode": "smooth" | "lock" (smooth), "smoothness": seconds (0.5; σ = smoothness · fps / 2 frames), "model": "position" | "similarity" | "perspective" (similarity), "crop": "auto" | "none" (auto: the largest centred rectangle valid on every frame), "maxScale": 1.15 }`. |
| `camera` | object | defaults | `{ "focal": "fixed" | "variable" | horizontal angle of view in degrees (1–170), "features": 16–2000 (400), "ground": [[x, y], …] three or more picks on the floor at `from` }`. Any other key is `track.request_invalid`; lens estimation always runs and is kept only when it cuts the reprojection error by ≥ 20 %. |

### Items

| Type | Item fields (default) |
|---|---|
| `point` | `at` `[x, y]` (required); `feature` `[w, h]` (5 % of the shorter side, min 8; 54 px at 1080p); `search` `[w, h]` (3 × feature; must contain the motion between two frames); `searchOffset` `[dx, dy]` (`[0, 0]`). |
| `planar` | `region` polygon of ≥ 3 points inside the frame (preferred), and/or `corners` four points TL, TR, BR, BL (default the region's four points or its bounding quad; `"region"` says so explicitly); `by` `features` (default with a region: features inside it, a RANSAC homography, re-registered to the reference every `options.reanchor` frames) or `points` (the four corners as point tracks; the only option with corners alone). |
| `mask` | `path` `{ "v": [[x, y], …], "in": [[dx, dy], …], "out": [[dx, dy], …], "closed": true }` (spec 4 path, relative tangents; required); `model` `position` / `positionScale` / `positionScaleRotation` (default) / `positionScaleRotationSkew` / `perspective`. |
| `face` | `at` `[x, y]` (required): a point on the face's skin (a cheek) with the face toward the camera; no face there is `track.no_texture`. Weak on profiles and occlusion. |

### Options (all types; defaults filled into the file)

| Option | Default | Meaning |
|---|---|---|
| `channel` | `luminance` | `luminance`, `red`, `green`, `blue`, `saturation`, `rgb` (the three channels matched jointly). |
| `blur` | 0 | Pre-process blur radius in px (noise, grain). |
| `enhance` | false | Edge enhancement for low-contrast features. |
| `threshold` | 0.8 | Confidence below which `onLowConfidence` acts. |
| `onLowConfidence` | `adapt` | `adapt` keep and re-sample the feature (After Effects' default; follows occluders), `continue` keep as is (flag `t`), `extrapolate` continue the motion for ≤ 0.5 s then `lost` (flag `x`), `stop` end the item (`lost` after). For features that pass behind things use `extrapolate`. |
| `adaptEveryFrame` | false | Re-sample every frame (changing appearance; drifts). |
| `shape` | true | Also estimate each feature's rotation and scale (`r`, `s`). |
| `reanchor` | 10 | Planar: re-register to the reference frame every n frames (drift control). |

### Corrections

A correction pins an item's value on one frame; it becomes a new anchor, the feature is re-sampled there, and the segments either side are tracked from both ends and blended by confidence × proximity.

```json
"corrections": [
  { "item": "heel", "t": 3.20, "at": [905, 470] },
  { "item": "screen", "t": 6.10, "corners": [[820, 400], [1060, 412], [1048, 868], [808, 858]] },
  { "item": "car", "t": 4.00, "outline": { "v": [[…]], "in": [[…]], "out": [[…]], "closed": true } }
]
```

The value field must match the item's type: `at` (point), `corners` (planar), `outline` (mask; the same vertex count as the item's `path`). Stabilize, camera and face tracks take no corrections (`track.correction_kind`); re-run them with other options or re-place a face item at `from`. Once a track exists, an item placed on another frame than `from` is `track.from_fixed`: enter it as a correction.

## Output

`files`: the track (label `track`) and the sheet (label `preview`). `data`: `type`, `frames`, `summary` per item (`tracked`, `lost`, `corrected`, `meanConfidence`, `lostSpans [[t0, t1], …]`), `ms`, `method`, `cache_hit`, `footage_s`, `warnings`, `billing`. A track is usable when mean confidence is ≥ 0.85 with no lost span over 0.5 s in the part you use; a camera solve when `reprojection` is under 1.5 px.

Runs: point/planar/mask/stabilize/face tracks of short clips run synchronously (admission at 8 s of box time per second of footage); **camera solves always run as jobs** (a sync camera request is refused with "submit via POST /v1/jobs"). Cost 2, timeout 10 minutes for every type, 4 CPU / 4 GiB. Results are cached by every input (engine version, the video's sha256, type, items, range, from, direction, method, options, solve, stabilize, camera, corrections, base): an identical request returns at once.

## Diagnostics

| Code | Severity | Meaning |
|---|---|---|
| `track.region_outside` | error | An item's feature, search region or polygon is outside the frame at `from`. |
| `track.search_too_small` | error | Search smaller than the feature. |
| `track.no_texture` | error | Too little texture (flat colour, sky), or no face at `at`. |
| `track.too_few_features` | error | Fewer than 8 features in a region. |
| `track.from_fixed` | error | An item placed on another frame once a track exists. |
| `track.correction_kind` | error | A correction's value does not match the item's type, wrong vertex count, or a correction on a stabilize/camera/face track. |
| `track.request_invalid` | error | Malformed request: unknown type, missing item fields, `from` outside `range`, a correction `t` outside `range`, a `base` of another type, a camera option other than `focal`/`features`/`ground`. |
| `track.range_empty` | error | No source frame in `range`. |
| `limit.track_items`, `limit.track_duration` | error | Over the per-call caps. |
| `track.solve_failed` | error | Camera: no parallax and no rotation, or a mostly moving scene. |
| `track.unavailable` | error | `method: "ml"`. |
| `track.lost_long` | warning | An item lost for > 1 s or 25 % of the range. |
| `track.low_confidence` | warning | Mean confidence below 0.7. |
| `track.drift` | warning | Planar re-anchoring corrected > 3 px at some frame. |
| `track.solve_poor` | warning | Camera: reprojection error > 1.5 px, or `ground` picks that fit no plane (no `ground` in the file). |

## Worked requests

```json
{ "video": "https://…/shoe.mp4", "type": "point", "items": { "heel": { "at": [812, 440] } }, "options": { "onLowConfidence": "extrapolate" }, "preview": "sheet" }
{ "video": "https://…/hand.mp4", "type": "planar", "items": { "screen": { "region": [[790, 410], [1030, 420], [1020, 880], [780, 870]] } }, "preview": "sheet" }
{ "video": "https://…/walk.mp4", "type": "stabilize", "stabilize": { "mode": "smooth", "smoothness": 0.8, "model": "similarity" } }
{ "video": "https://…/lobby.mp4", "type": "camera", "camera": { "focal": "fixed", "ground": [[420, 880], [1500, 900], [960, 1040]] } }
{ "video": "https://…/host.mp4", "type": "face", "items": { "host": { "at": [960, 420] } }, "preview": "sheet" }
```

The engine form the service writes is `rexx-engine track --video <file> --request <json> --out <file.track.json> [--base <file>] [--preview <png|sheet|none>]`; `examples/assets/camera-scene.point.track.json` and `camera-scene.stabilize.track.json` were made that way from the golden clip (36 frames at 480 × 270) with `{ "type": "point", "items": { "mark": { "at": [240, 135] } }, "options": { "threshold": 0.7 } }` and `{ "type": "stabilize", "stabilize": { "mode": "smooth" } }`.
