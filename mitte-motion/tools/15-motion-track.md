# 15 · `motion.track`

Analyse a video and return a **track file** a document can attach graphics to: follow points, a planar surface, a
masked object, the camera's shake, the camera in 3D (a solve) or a face. Analysis only; nothing is rendered. A
job tool (`sync: false`), cost 2, max 2 concurrent, 10 min, cgroup 4 CPU / 4 GiB, output asset type `text`, rate
class `render`, daily quota 600 footage seconds (`REXX_QUOTA_TRACK_SECONDS`). Source: `service/src/tools/track.rs`,
`engine/crates/rexx-engine/src/track.rs`, `rexx-track/src/request.rs`, spec 18 §18.4–18.8, 06 §6.7.

## Input

| Field | Type | Default | Meaning |
|---|---|---|---|
| `video` | https URL or `library:` URI (required) | — | The clip. `@…` or anything else: `400` "video must be an https URL of the clip (or a library:… URI of a clip the library ships)". |
| `type` | enum (required) | — | `point`, `planar`, `mask`, `stabilize`, `camera`, `face`. |
| `items` | map id → item | — | Required for `point`, `planar`, `mask`, `face`; forbidden for `stabilize`, `camera` ("stabilize takes no items"). Coordinates are **source pixels on the frame at `from`**. Caps: `REXX_MAX_TRACK_ITEMS` = 32 point/face items, 8 planar/mask items (`413`). |
| `from` | seconds ≥ 0 | the range start | Where the items are defined. Negative: `400`. |
| `range` | `[start, end]` seconds | the whole clip | `end > start ≥ 0`. The analysed footage must be ≤ `REXX_MAX_TRACK_DURATION` (120 s): `413` "Ns of footage; the limit is 120s per call (use range)". |
| `direction` | enum | `forward` (`both` when `from` is inside the range) | `forward`, `backward`, `both`. |
| `method` | enum | `classic` | `classic`; `ml` answers `503 overloaded` "the hosted tracker is not available yet; retry with method \"classic\"". |
| `options` | object | | `channel`: `luminance` (default), `red`, `green`, `blue`, `saturation` (`rgb` is tracked as luminance); `blur` px (0); `enhance` (false); `threshold` 0–1 (0.8); `onLowConfidence`: `adapt` (default), `continue`, `extrapolate`, `stop`; `adaptEveryFrame` (false); `shape` (true: estimate each feature's rotation and scale); `reanchor` (planar, 10 frames). Unknown keys are `track.request_invalid`. |
| `corrections` | list | `[]` | `{ "item", "t", "at": [x, y] }` (point), `{ "item", "t", "corners": [TL, TR, BR, BL] }` (planar), `{ "item", "t", "outline": {path} }` (mask, same vertex count). Each needs `item`, `t` and exactly its type's value field ("corrections[i] needs item, t and at, corners or outline"); the wrong kind is `track.correction_kind`. Corrected frames are fixed; the segments either side are re-tracked from both ends. |
| `base` | https URL or `library:` | | A previous track file of the same type; only the segments the corrections split are re-tracked (point and planar; mask items re-track whole). `items` are still required with `base`. |
| `preview` | enum | `none` | `sheet`: also return a contact sheet with the track drawn (below). Always ask for it. |
| `solve` | enum | | `similarity`: with two `point` items, solve them as one rigid pair (adds the item `pair`: centre, rotation, scale). |
| `stabilize` | object | | For `type: "stabilize"`: `mode` `smooth` (default) \| `lock`; `smoothness` seconds (0.5); `model` `position` \| `similarity` (default) \| `perspective`; `crop` `auto` (default) \| `none`; `maxScale` (1.15). Unknown keys: `track.request_invalid`. |
| `camera` | object | | For `type: "camera"`: `focal` `"fixed"` (default) \| `"variable"` \| a horizontal angle of view in degrees (1–170, inclusive); `features` 16–2000 (400); `ground`: three or more `[x, y]` points on the floor at `from`. Any other key: `400` "camera.<k> is not a camera option (focal, features, ground)". Camera solves are **job-only**: on `/v1/run` `413` "camera solves run as jobs; submit via POST /v1/jobs". A camera solve takes at most 3,000 frames (the clip's rate, 30 fps when unknown): a longer range is `413` "… a camera solve takes at most 3000 per call (use range)". |

### Items by type

```jsonc
// point: at (required), feature [w, h] (default 5 % of the shorter side, min 8 px), search [w, h] (3 × feature), searchOffset [dx, dy] (0, 0)
"items": { "heel": { "at": [812, 440], "feature": [48, 48], "search": [144, 144] }, "toe": { "at": [1010, 452] } }
// planar: region (a polygon of ≥ 3 points) and/or corners [TL, TR, BR, BL]; by: "region" (default with a region) | "points"
"items": { "screen": { "region": [[790, 410], [1030, 420], [1020, 880], [780, 870]] } }
"items": { "sign": { "corners": [[100, 80], [400, 90], [395, 300], [98, 290]], "by": "points" } }
// mask: path (spec 4 path object: v, in, out, closed) and model
"items": { "car": { "path": { "v": [[…]], "in": [[…]], "out": [[…]], "closed": true }, "model": "positionScaleRotation" } }
// face: at, a point on the face's skin
"items": { "host": { "at": [960, 420] } }
```

Mask `model`: `position`, `positionScale`, `positionScaleRotation` (default), `positionScaleRotationSkew`,
`perspective`. The service checks the grammar before the engine runs (`point`/`face` items need `at`; `planar` needs
`region` or `corners`; `mask` needs `path`); the engine checks the rest (`track.request_invalid`,
`track.region_outside`, `track.search_too_small`, `track.no_texture`, `track.too_few_features`, …).

## What runs

The clip is fetched (and probed with ffprobe for its duration); `base` is fetched; admission: 8 s of box time per
footage second (unknown duration counts as 120 s) against the sync budget on `/v1/run`; the track-seconds quota is
charged (footage rounded up). Cache lookup by key (below); else `rexx-engine track --video <file> --request
track.json --out out/<stem>.track.json [--base <file>] [--preview out/<stem>.track-sheet.png] --deadline …` where
`track.json` is the request's `type`, `method`, `items`, `range`, `from`, `direction`, `options`, `corrections`,
`solve`, `stabilize`, `camera`. The classic tracker is deterministic (fixed pyramids, iteration counts, counter-seeded
RANSAC).

## Output

`files`: `{ "track": url, "preview": url }` (`<stem>.track.json`, content type `application/vnd.mitte.track+json`;
`<stem>.track-sheet.png`), the stem being the video URL's last path segment kept to `[A-Za-z0-9_-]`, else `clip`.

```jsonc
{ "type": "planar", "frames": 360,
  "summary": { "screen": { "tracked": 342, "lost": 18, "corrected": 0, "meanConfidence": 0.93, "lostSpans": [[7.2, 7.8]] } },
  "ms": 2840, "method": "classic", "cache_hit": false, "footage_s": 12.0,
  "warnings": [ { "severity": "warning", "code": "track.lost_long", "path": "/items/screen", "message": "…", "at": 7.2 } ],
  "billing": { "price": { "amount": 0.02, "currency": "USD" } } }
```

| Field | Meaning |
|---|---|
| `type`, `method` | as tracked. |
| `frames` | samples of the longest item. |
| `summary.<item>` | `tracked`, `lost`, `corrected` counts; `meanConfidence` over tracked frames; `lostSpans` `[[t0, t1], …]`. The single item of a stabilize track is `stabilize`, of a camera track `camera`; a two-point solve adds `pair`. |
| `ms` | wall time. |
| `cache_hit` | the track came from the cache (no warnings then). |
| `footage_s` | the analysed span (the file's `range`, else the source duration). |
| `warnings[]` | `track.lost_long`, `track.low_confidence`, `track.drift`, `track.solve_poor`, with `at` in source seconds and `path` into the request (`/items/<id>`, `/corrections/0`). |

Usable when `meanConfidence ≥ 0.85` with no lost span over 0.5 s in the part you use.

### The track file (spec 18 §18.6)

`{ "track": 1, "type", "source": { "asset", "sha256", "size", "fps", "duration", "rotation" }, "range", "from",
"direction", "method", "options", "corrections", "engine", "fields", "items": { "<id>": { "reference", "samples",
"fields"? } }, "segments", "summary" }`. Samples are tuples per source frame; `fields` names the layout per type:
point `[t, x, y, c, f, r, s]`; planar `[t, corners, h, c, f]`; mask `[t, path, c, f]`; stabilize `[t, m, c, f]`;
camera `[t, position, orientation, focal, c, f]` plus a `camera` block (`lens`, `reprojection`, `points`, `ground`,
`model`); face `[t, outline, landmarks, pose, c, f]`. Flags `f`: `t` tracked, `a` adapted, `x` extrapolated, `d`
degraded, `c` corrected, `l` lost. A document attaches it as an asset of type `track` (`sha256` must match the
footage layer's asset) and references it with a `track` property reference, `pin`, `stabilize`, a camera `solve`
or a face reference (the `language` area, spec 18 §18.7).

### The preview sheet

Twelve frames spread across the range plus the four worst-confidence frames, four cells per row, each at most 480 px
wide (never upscaled), the source time in the corner; a crosshair per point (a cross when lost), the quad of a
planar item, the vertex outline of a mask (bezier handles ignored), the crop window of a stabilize; coloured by
confidence: green ≥ 0.85, amber ≥ 0.6, red below or lost, blue when pinned by a correction.

### Cache key

`sha256(engine version ‖ video sha256 ‖ type ‖ items ‖ range ‖ from ‖ direction ‖ method ‖ options ‖ solve ‖
stabilize ‖ camera ‖ sha256(corrections) ‖ base hash)`, each JSON part with sorted keys. Entries live under
`rexx/cache/track/` for 90 days after last use; a hit is free and copies the track (and the sheet, when asked)
into the caller's prefix.

## Errors

| Status | When |
|---|---|
| 400 `bad_request` | a bad `video`/`base` URL; an unknown `type`; items missing or given where forbidden; an item without its field; a bad `range`/`from`/correction/camera option; `method: "ml"` ("not available yet; use method \"classic\""); the engine's `track.*` errors (`track.request_invalid`, `track.region_outside`, `track.search_too_small`, `track.no_texture`, `track.too_few_features`, `track.from_fixed`, `track.correction_kind`, `track.range_empty`, `track.solve_failed`, `track.unavailable`); a clip that cannot be read or decoded (`asset.*`, `media.*`) |
| 413 `too_large` | over 32 point / 8 region items; footage over 120 s; a camera solve on `/v1/run` or over 3,000 frames; an estimate over the sync budget |
| 429 | the track-seconds quota (`overloaded`), the `render` class per minute (`rate_limited`) |
| 503 `overloaded` | budget/slots; no engine |
| 500 `internal` | "tracking produced no file", an unreadable track file, exit 5 |

## Examples

```json
{ "video": "library:mitte/demo/tracking-clip@1", "type": "point", "items": { "tag": { "at": [240, 300] } }, "preview": "sheet" }
```
Follow one point with a preview.

```json
{ "video": "library:mitte/demo/tracking-clip@1", "type": "planar",
  "items": { "screen": { "corners": [[510, 180], [770, 180], [770, 360], [510, 360]] } }, "preview": "sheet",
  "corrections": [ { "item": "screen", "t": 3.2, "corners": [[512, 182], [772, 180], [771, 361], [510, 362]] } ] }
```
A screen with one correction at 3.2 s.

```json
{ "video": "library:mitte/demo/tracking-clip@1", "type": "stabilize", "range": [0, 6],
  "stabilize": { "mode": "smooth", "smoothness": 0.8, "model": "similarity", "crop": "auto", "maxScale": 1.2 } }
```
Smooth the first six seconds.

```json
{ "video": "https://media.mitte.ai/u/a1/walk.mp4", "type": "camera", "camera": { "focal": "fixed", "features": 400, "ground": [[512, 900], [1400, 910], [960, 1020]] } }
```
A camera solve with a picked ground plane (submit to `/v1/jobs`).

Registry examples: `point`, `planar`, `stabilize` ([95-schema-track.md](95-schema-track.md)).

