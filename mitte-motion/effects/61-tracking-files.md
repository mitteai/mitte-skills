# Tracking 2: the track file

`motion.track` writes one JSON file per run (`<clip>.track.json`, a mitte text asset). A document references it as an asset of type `track`; the tool returns its `summary` to you instead of the whole file. The file binds to the video by the video's **sha256**: a document whose footage layer's asset has another hash fails with `track.source_mismatch`.

## Envelope

```json
{ "track": 1, "type": "point",
  "source": { "asset": "clip", "sha256": "085b…6ae", "size": [480, 270], "fps": "24", "duration": 1.5, "rotation": 0 },
  "range": [0, 1.5], "from": 0, "direction": "forward", "method": "classic",
  "options": { "channel": "luminance", "blur": 0, "enhance": false, "threshold": 0.7, "onLowConfidence": "adapt", "adaptEveryFrame": false, "shape": true, "reanchor": 10 },
  "corrections": [], "engine": "0.1.48",
  "fields": ["t", "x", "y", "c", "f", "r", "s"],
  "items": { "mark": { "reference": { "t": 0, "at": [240, 135], "feature": [14, 14] },
                       "samples": [[0, 240, 135, 1, "t", 0, 1], [0.041667, 240.21, 135.31, 0.87, "t", -1.87, 1.11], …] } },
  "segments": { "mark": [ { "range": [0, 1.5], "direction": "forward" } ] },
  "summary": { "mark": { "tracked": 36, "lost": 0, "corrected": 0, "meanConfidence": 0.74, "lostSpans": [] } },
  "warnings": [] }
```

| Field | Meaning |
|---|---|
| `track` | Format version (1). A newer version than the engine knows is `track.version`. |
| `type` | The track type. |
| `source` | `asset` the id the engine was given (informational), `sha256` of the video bytes (binding), `size` the display size (rotation and pixel aspect applied), `fps` as an exact rational string, `duration` seconds, `rotation`. |
| `range`, `from`, `direction`, `method`, `options` | As requested, defaults filled. |
| `corrections` | As given. |
| `engine` | The engine version that wrote it. |
| `fields` | The order of values in every sample tuple for this type (below); an item may carry its own `fields` (the `pair` item). |
| `items` | Per item: `reference` (the item as given at `from`, defaults filled: `at`, `feature`, `corners`, `path`), `samples` (one tuple per source frame in the range, in time order), optional `fields`. |
| `segments` | Per item: the anchor-bounded spans with the direction each was tracked (`both` between two anchors, `forward`/`backward` for an open end). A re-track with `base` reuses a segment only when its bounds, anchors and direction match. |
| `summary` | Per item: counts by flag, mean confidence over tracked frames, lost spans. |
| `solve` | `"similarity"` for a two-point solve. |
| `stabilize` | `{ "mode", "model", "cropScale" }` for a stabilize track. |
| `camera` | `{ "lens", "reprojection", "points", "ground", "model" }` for a camera track (below). |
| `warnings` | The run's diagnostics (`track.low_confidence`, `track.lost_long`, `track.drift`, `track.solve_poor`). |

**Flags** (the `f` field of every sample): `t` tracked (confidence ≥ threshold), `a` adapted (feature re-sampled on this frame), `x` extrapolated (motion continued at low confidence), `d` degraded (a region type fitted with a simpler model), `c` corrected (pinned), `l` lost (the numbers repeat the last good value and are not measurements). Confidence `c` is 0–1.

## Per type

| Type | `fields` | Notes |
|---|---|---|
| `point` | `["t", "x", "y", "c", "f", "r", "s"]` | Position in source px; `r` feature rotation in degrees and `s` scale, relative to the segment's anchor (they restart at 0 and 1 after each correction). With `solve: "similarity"` an extra item `pair` has its own `"fields": ["t", "x", "y", "rotation", "scale", "c", "f"]`: the two points' centre, unwrapped rotation, scale relative to the reference frame. |
| `planar` | `["t", "corners", "h", "c", "f"]` | `corners` `[[TL], [TR], [BR], [BL]]`; `h` the 3×3 homography from the reference frame, row-major 9 values; `c` the inlier ratio. |
| `mask` | `["t", "path", "c", "f"]` | `path` a spec 4 path object (`v`, `in`, `out`, `closed`). |
| `stabilize` | `["t", "m", "c", "f"]` | `m` the corrective 3×3 (source → stabilized), row-major; the single item's id is `stabilize`; `stabilize.cropScale` is the global crop scale (`mode`, `model` beside it). |
| `camera` | `["t", "position", "orientation", "focal", "c", "f"]` | The single item is `camera`. Coordinates follow After Effects (x right, y down, z into the screen) in source pixels at the reference depth: the reference camera sits at `[w/2, h/2, −focal]` with orientation `[0, 0, 0]`, the median depth lands at z = 0. `orientation` is unwrapped `[x, y, z]` degrees (Rz · Ry · Rx); `focal` in source px; `c = 1 − error / 4 px`; `f` is `t`, `x` (interpolated between solved frames) or `l`. |
| `face` | `["t", "outline", "landmarks", "pose", "c", "f"]` | `outline` the 48-point polygon; `landmarks` a map of the 26 names below to `[x, y]`; `pose` `[yaw, pitch, roll]` degrees; `c` the share of landmarks found. `reference` carries `at`. |

Camera extras: `lens` `{ "k1", "k2", "radius" }` (radial distortion `p_d = p (1 + k1 ρ² + k2 ρ⁴)` about the centre, ρ = distance / `radius`, `radius` = half the frame diagonal; both 0 when the lens solve was not kept), `reprojection` (mean error in px, the quality score; > 1.5 is `track.solve_poor`), `points` `[[x, y, z, r, g, b, frames, error], …]` (colours as integers 0–255; anchors name a point by its index), `ground` `{ "origin", "normal", "xAxis" }` (absent for tripod solves or when no plane was found; `normal` points up, so usually negative y), `model` `general` / `flat` / `tripod`.

The 26 face landmarks: `leftEyebrowInner`, `leftEyebrowMiddle`, `leftEyebrowOuter`, `rightEyebrowInner`, `rightEyebrowMiddle`, `rightEyebrowOuter`, `leftEyeInner`, `leftEyeOuter`, `leftEyeTop`, `leftEyeBottom`, `leftPupil`, `rightEyeInner`, `rightEyeOuter`, `rightEyeTop`, `rightEyeBottom`, `rightPupil`, `noseTip`, `leftNostril`, `rightNostril`, `mouthLeft`, `mouthRight`, `mouthTop`, `mouthBottom`, `chin`, `leftJaw`, `rightJaw`; plus `center` (the outline's centroid) when a document asks for a landmark.

Sizes: a point track is about 40 bytes per item per frame; a planar track about 200; a face track about 2 KB per frame; a camera track adds the point cloud (50–500 KB). A document reads a track file up to 16 MB (its own cap, not the 512 KB `data` cap); a larger one is `track.asset_missing`. The three files under `examples/assets/` are real outputs for the 36-frame golden clip (`camera-scene.point.track.json`, `camera-scene.stabilize.track.json`, `camera-scene.camera.track.json`).

## Determinism and caching

The classic tracker is deterministic on the CPU (fixed pyramids and iteration counts, counter-seeded RANSAC, `libm`, items tracked independently): the same request on the same clip gives the same bytes. The service caches by every input, corrections and the `base` track included, so a corrected re-track never returns the uncorrected result; per item and segment, results are cached under the segment's bounds and anchor values, so adding a correction re-tracks only the two segments it splits.
