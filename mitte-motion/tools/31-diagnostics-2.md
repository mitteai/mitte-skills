# 31 · Diagnostics: assets, effects, expressions, limits, tracking, physics, render, media, output, encode, convert

Continues [30-diagnostics.md](30-diagnostics.md). Severity is `error` unless marked (w) warning or (i) info.
Since engine 0.1.59 (P3 audit K-27) every code the sources emit is in spec 14's tables and every listed code is
emitted by something; [33-codes-inventory.md](33-codes-inventory.md) is the generated cross-check and `check-skills`
fails on drift. "Engine code" marks a code raised outside document validation (spec 14 §14.3 "Engine, encoder and
service codes").

## `asset.*`

| Code | Fires when | Fix |
|---|---|---|
| `asset.unreadable` | a file cannot be decoded at all (also an audio asset the mixer cannot decode, an import file that is not SVG/Lottie or over 256 MB) | a valid file |
| `asset.type_mismatch` | the declared `type` disagrees with the file (engine); the service refuses it earlier with the same prefix | fix `type` or the file |
| `asset.hash_mismatch` | the content does not match `sha256`: a service `400` whose message starts with the code and the asset id | update the pin |
| `asset.bad_url` | `src` is neither https nor a shipped `library:` file; a `golden:` URI outside the test runner | an https URL or `library:` URI |
| `asset.invalid_font` | a font file failed the OpenType sanitizer (the normalizer and the text crate) | another file |
| `asset.unmaterialized` | the engine was asked for an asset the manifest does not hold (a deferred asset read by `check`, or a service bug) | report it; for `check`, the asset is only probed |
| `asset.audio_analysis` | beat or onset detection failed (unreadable or too short audio) | a longer/decodable file; silence yields no beats, not an error |
| `asset.data_invalid` | a `data` asset (JSON/CSV) does not parse, ragged CSV rows; caption data outside spec 10 §10.9 | fix the file |
| `asset.missing` (engine code) | `track`: the video cannot be read or was not materialized (`/video`) | a readable clip |

## `effect.*`

| Code | Fires when | Fix |
|---|---|---|
| `effect.unknown_type` | a type outside the catalogue | the hint's nearest ids; `rexx-engine effects` |
| `effect.unknown_param`, `effect.param_value` | an unknown parameter; a value the kernel rejects (out of range, wrong kind) | the `effects` area tables |
| `effect.invalid_param` (engine code) | a parameter value of the wrong type or outside its hard range (the fx crate's own check) | as above |
| `effect.missing_input` (engine code) | a required input (another layer, a LUT asset, a mask path) not supplied | supply it |
| `effect.layer_cycle` | effects reading each other's layers in a cycle (`check` finds it; the renderer bounds the read recursion at 8) | break it |
| `effect.requires_gpu` (w) | a GPU-only effect (`utility.shader`) in a CPU job; the layer passes through unshaded | a GPU box, or drop the effect |
| `effect.shader_invalid` | a `utility.shader` whose source, uniforms or inputs fail the sandbox or naga (at `params/code`, `params/params`, `params/inputs`); checked at `check` on every box | fix the WGSL; no own bindings, bounded loops, ≤ 64 KiB |
| `effect.shader_timeout` (w) | a shader dispatch over its budget (`budgetMs`, else 50 ms device time); the frame renders unshaded | cheaper shader or a higher budget |
| `effect.unavailable` | an id in the catalogue but not this release (the message names the phase) | wait, or another effect |
| `effect.backdrop_not_last` (w) | a backdrop effect (`distort.glass`) not last in its list; skipped | move it last |
| `effect.backdrop_not_2d` (w) | a backdrop effect on a 3D or adjustment layer; skipped | a 2D layer |

## `expr.*`

| Code | Fires when | Fix |
|---|---|---|
| `expr.syntax` | a parse error (line and column in the message) | fix the expression |
| `expr.unknown_name` | an identifier that is neither a local nor in the library | spec 11's names |
| `expr.unknown_layer` (engine code) | a statically named layer or comp that does not exist | the layer id |
| `expr.unknown_property` | a statically known property access that does not exist (`transform.positon`) | the hint |
| `expr.arity` | wrong argument count | the signature |
| `expr.undeclared` | assignment to an undeclared name inside a function | `var` |
| `expr.math_random` | `Math.random` | the seeded `random()` |
| `expr.type` (engine code) | a static or dynamic type error | matching types |
| `expr.cycle` | expressions reading each other in a cycle | break it |
| `expr.budget` | the per-evaluation step budget (100,000) exceeded at render time (with the time) | simplify; fewer loops |
| `expr.runtime` | any other runtime error (calling a non-function, index out of range), with the time | fix the expression |
| `expr.depth`, `expr.memory` | call depth over 64; over 16 MB of heap in one evaluation | simplify |
| `expr.no_layer`, `expr.no_key` | `layer(n)` / `key(i)` out of range | fix the index |
| `expr.no_value`, `expr.non_finite` | the property received `null`/`undefined`; `NaN`/`±Infinity` | return a value |
| `expr.vector_op` | an operation After Effects does not define on vectors (`[1,2] * [3,4]`) | component-wise |
| `expr.result_type` | the wrong shape for the property | match it |

## `limit.*` (and the other exit-4 codes)

| Code | Fires when |
|---|---|
| `limit.doc_size`, `limit.canonical_size`, `limit.data_size` | 2 MB authored, 32 MB canonical, 512 KB `data` |
| `limit.comps`, `limit.layers`, `limit.nesting`, `limit.keys`, `limit.keys_total`, `limit.repeat` | 256; 2,000 per comp (also at render, `render.layers_capped` drops extras); 16; 10,000 per property; 1,000,000; 1,000 per repeat / 10,000 per document |
| `limit.frame_size`, `limit.duration`, `limit.fps` | the output comp or a variant over the cap (nested comps 16,384 px / 64 MP); over the duration cap (also an audio mix over 30 min); fps outside 1–60 (engine 1–240) |
| `limit.assets` | over 512 assets |
| `limit.particles`, `limit.particle_systems`, `limit.particle_births`, `limit.particle_lines` (w), `limit.preroll` | spec 9 §9.11 |
| `limit.audio_sources`, `limit.audio_duration` (decoded audio over the in-memory cap, 3,600 s), `limit.sequence_frames`, `limit.lottie`, `limit.caption_words`, `limit.archive`, `limit.svg` | spec 10 §10.10 (video sources are not capped: one decoder per source and direction, bounded by `limit.memory`) |
| `limit.track_duration`, `limit.track_items` | over 10 min of footage per file; over 64 items |
| `limit.3d_run_layers`, `limit.3d_lights` (w), `limit.3d_shadow_lights` (w) | over 256 drawables; over 64 lights (rest dropped); over 8 shadow casters |
| `limit.physics_bodies`, `limit.physics_bake`, `limit.physics_joints`, `limit.physics_forces` | 2,000; 64 MB; 1,000; 256 |
| `limit.expr_total` | 5 × 10⁸ expression steps in one check or render (the message names the costliest properties) |
| `limit.memory` | RSS over `--memory-mb` after cache eviction |
| `limit.frames` | over 64 `frames` times; a camera path over 216,000 frames |
| `limit.gpu_unavailable`, `limit.gpu_memory` | `--backend gpu` without a usable adapter; a texture or readback the GPU share cannot hold |
| `render.deadline`, `encode.timeout`, `cancelled` | a frame past the deadline; the encoder past its wall limit; `SIGTERM` |

## `track.*` (the tool's request, then the document's references)

| Code | Fires when | Fix |
|---|---|---|
| `track.request_invalid` | malformed request: unknown `type`, an item missing its field, unknown option keys, `from` outside `range`, a `base` of another type | the grammar in [15-motion-track.md](15-motion-track.md) |
| `track.region_outside` | a feature, search region or polygon outside the frame at `from` | move it inside |
| `track.search_too_small` | search region smaller than the feature | enlarge `search` |
| `track.no_texture` | too little texture at the point (flat colour, sky); no face at a face `at` | a corner or edge; `planar` with a larger region |
| `track.too_few_features` | fewer than 8 features in a region | a bigger, more textured region |
| `track.from_fixed` | an item placed on a frame other than `from` after the track exists | place at `from` or use a correction |
| `track.correction_kind` | the wrong value field for the item's type; an outline with another vertex count; a correction on a stabilize/camera/face track | match the type |
| `track.range_empty` | `range` holds no source frame | a range inside the clip |
| `track.solve_failed` | a camera that cannot be solved (no parallax or rotation, too little static scene) | footage with camera motion over a static scene |
| `track.unavailable` | `method: "ml"` (and the service refuses it first, `400`) | `classic` |
| `track.cancelled`, `track.internal` (engine codes) | the tracker was stopped; a tracker bug (exit 5) | retry; report |
| `track.lost_long` (w), `track.low_confidence` (w), `track.drift` (w), `track.solve_poor` (w) | lost over 1 s or 25 %; mean confidence under 0.7; planar re-anchoring over 3 px; reprojection over 1.5 px or `ground` fitting no plane | corrections, another region, a cleaner clip |
| `track.source_mismatch`, `track.version`, `track.asset_type`, `track.asset_missing`, `track.item_missing`, `track.type_mismatch` | the document's track asset: hash differs from the footage asset; a newer format; not `type: "track"`; not materialized; `item` not in the file; the wrong reference kind for the type | re-track the right clip; declare the asset as `track`; use the item and kind the file has |
| `track.layer_missing`, `track.layer_3d`, `track.pin_transform`, `track.stabilize_transform`, `track.camera_layer`, `track.hide_conflict`, `track.target_timing` | the footage layer missing or 3D; a pinned/stabilized layer with its own transform keys or parent; a solved camera with its own keys, or footage not uniformly mapped; `lost: "hide"` on animated opacity; `timeRemap`/`stretch` with `keysPerFrame` > 1 or more keys than `limit.keys` (frames × `keysPerFrame`) | keep the footage layer plain and 2D; let the track write the keys; shorten `range` or lower `keysPerFrame` on a long clip |

## `physics.*`

Errors: `physics.no_world` (a `body` without comp `physics`), `physics.no_bodies` (`physics` without bodies),
`physics.body_not_allowed` (the layer type, or a null without `shape`), `physics.layer_3d`, `physics.parent_moves`
(the parent animates in the span), `physics.per_not_text`, `physics.text_animator_conflict`, `physics.shape_empty`
(no collidable geometry at `start`), `physics.shape_too_complex` (over 64 parts / 256 vertices),
`physics.unknown_target` (a force or joint target matches no body), `physics.rate_range` (outside 60–960 or below
fps), `physics.span` (outside the comp or over the cap), `physics.unavailable` (joints, fields beyond `wind`/`drag`,
`per: "lines"`, `ccd`, animated-matte colliders, over 30 groups), `physics.non_finite` (the solver produced NaN),
`physics.lock_missing` (the locked bake is not a declared `sim` asset, unreadable, or another take),
`physics.lock_bodies_mismatch`, `physics.settle_target` (malformed `settle.to`), `physics.text_layer_animates`,
`physics.cycle` (a kinematic body depending on a dynamic pose), `physics.reserved_group` (`world`).
Warnings: `physics.lock_stale` (re-simulated; names the changed inputs), `physics.overlap_at_start` (> 0.5 px),
`physics.tunneling_risk` (raise `rate`, `inset: -2`), `physics.keys_after_start`, `physics.content_animates`,
`physics.static_animates` (use `kinematic`), `physics.unsettled_at_end` (add `settle`), `physics.offscreen`,
`physics.settle_spin` (> 90°), `physics.rate_low` (< 4 × fps), `physics.many_bodies` (> 500).
Infos: `physics.single_body` (an ease is cheaper), `physics.seed_no_effect`, `physics.lock_forced`,
`physics.idle_span` (shorten `end`).

## `render.*` (from `frames` and `render`)

| Code | Fires when |
|---|---|
| `render.cycle`, `render.depth` | a comp containing itself; nesting over 16 (the renderer's counterparts of `layer.comp_cycle`) |
| `render.expression_budget` | the per-frame expression budget exhausted; the frame fails |
| `render.layers_capped` (w) | a comp over the layer cap; extras dropped |
| `render.unsupported` | a construct this release does not render (`model` layers, environment lights as an info) |
| `render.deadline` | the frame did not finish within `--deadline` |
| `render.invalid` (w) | a value that cannot be rendered (non-finite transform, empty size); the layer is skipped for the frame |
| `render.bounds` (w) | a layer's bounds clamped to the comp-space cap |
| `render.matte` (w), `render.parent` (w) | a matte chain over 8 or cyclic (ignored); a parent cycle (rendered unparented) |
| `render.gpu_lost` | the device was lost or missed a readback deadline; the service re-runs on the CPU once |
| `render.gpu_declined` (i) | the `info` event: the GPU declined the job, it rendered on the CPU |
| `render.styles_unsupported` (i) | reserved; never emitted since 0.1.12 |
| `render.options_invalid` (engine code) | (3D renderer) inconsistent render options; a bug |

## `media.*`

| Code | Fires when |
|---|---|
| `media.missing` | a layer names an asset not in the manifest; renders transparent |
| `media.decode_failed` | one frame failed to decode; the layer renders transparent for that frame |
| `media.image_too_large`, `media.video_too_large` | over 16,384 px / 64 MP; over 7680 × 4320 |
| `media.loop_and_remap` | `loop` and `timeRemap` on one layer (at `loop`) |
| `media.sequence_gap` (w) | an image sequence with missing frame numbers; each holds the frame before it (once per asset, at `/assets/<id>`, naming the numbers) |
| `media.captions_cue_level` (w) | captions built from SRT/WebVTT cues: word times spread evenly across each cue (at the instance's `props/words`) |
| `media.solo_in_render` | a `solo` audio layer in `render` without `output.allowSolo` (at the layer's `solo`); `frames` and `check` accept it |
| `media.audio_invalid`, `media.audio_track_invalid`, `media.duck_invalid` | an unmixable clip (zero channels, non-finite samples); unusable timing (speed outside 0.01–16, `out` ≤ `in`); a duck rule naming no audible track or with negative times |
| `media.audio_channels` (engine code) | a channel layout the mixer cannot downmix (it takes 1, 2 and 6) |
| `media.audio_effect_unsupported` (engine code) | a per-track audio effect (a later phase) |
| `media.unreadable`, `media.decode`, `media.timeout`, `media.unsupported` (engine codes; the renderer maps the first and last onto `asset.unreadable`, the others onto `media.decode_failed`; `media.unsupported` is also a codec ffmpeg cannot decode) | the media crate's own failures: unparseable file, a broken stream, a decoder over its time budget, a codec or pixel format this build lacks |

## `output.*` and `encode.*`

| Code | Fires when | Fix |
|---|---|---|
| `output.format_unavailable` | (service) a format this box's ffmpeg cannot write | the registry's enum |
| `output.codec_container` | a codec the container cannot hold; a codec on an image format | spec 13 §13.5's table |
| `output.alpha_unsupported` | alpha with a format or codec that cannot carry it (the hint lists the rows that can) | another row, or `"stacked"` |
| `output.hdr_unsupported` | `hdr` with an image/sequence format, `h264`/`vp9`/`prores`, alpha, profile `main` | `hevc`/`av1`, no alpha |
| `output.encoder_unsupported` | `nvenc` with prores/vp9/alpha/pq/4:2:2/4:4:4 AV1/images/tiny frames, or on a box without it | `cpu`, or change the output |
| `output.size_aspect`, `output.size_odd` | `output.size` off the comp's aspect by over 1 px; an odd explicit size for a chroma-subsampled format | keep the aspect; even sizes |
| `output.pixel_format` | a `pixelFormat` the codec cannot encode, alpha formats without `alpha`, 8-bit with `hdr` | drop it |
| `output.value` (engine code) | any other output setting outside its domain: `scale` outside 0.25–2, `size` with `scale`, `crf` outside 0–63 (51 for NVENC), `bitrate` 0, `fps` over 240, `gif.colors` outside 2–256, `gif.fps` outside 1–50, `pcm` outside `mov`, `audio.bitrate` 0, `hdrPeak` without `pq` or outside 100–10,000, a `profile` of another codec or on an image, an NVENC `preset` outside `p1`–`p7`, an unknown `--format`/`--codec`/`--quality`/`--alpha`/`--hdr`/`--encoder` value, an empty range, `frames --format`/`--depth`/`--seeds` outside their values | the message's domain |
| `output.audio_invalid`, `output.wav_invalid`, `output.write_failed` (the last an engine code) | unusable master audio settings; a malformed mixed WAV; the WAV could not be written | fix `output.audio`; report |
| `encode.timeout` (exit 4) | the encoder ran past its wall limit | shorter range, draft quality, a job |
| `encode.audio`, `encode.ffmpeg`, `encode.frame`, `encode.order`, `encode.io`, `encode.still` (exit 5, engine codes) | the mixdown failed; ffmpeg exited with an error; a frame of the wrong size; frames submitted out of order; an I/O failure; a PNG/WebP writer failure | escalated; retry once |

## `convert.*` (warnings unless marked)

Lottie/dotLottie export: `convert.ease_subdivided` (i), `convert.lottie_blend`, `convert.lottie_blending`,
`convert.lottie_collapse`, `convert.lottie_baked`, `convert.lottie_expression_unsupported`,
`convert.lottie_driver_unsupported`, `convert.lottie_text_outlines` (i), `convert.lottie_gradient_resampled` (i),
`convert.lottie_gradient_unsupported`, `convert.lottie_unsupported`, `convert.lottie_hdr_color`,
`convert.lottie_motion_blur`, `convert.lottie_layer_style`, `convert.lottie_effect`, `convert.lottie_frame_blend`,
`convert.lottie_feather`, `convert.lottie_mask_feather` (i), `convert.lottie_matte_order`, `convert.lottie_merge`,
`convert.lottie_offset_copies`, `convert.lottie_text_spans`, `convert.lottie_text_animator`, `convert.lottie_video`,
`convert.lottie_audio` (i), `convert.lottie_adjustment`, `convert.lottie_particles` (dropped; info with
`render_unsupported` and from `check`), `convert.lottie_3d_dropped`, `convert.lottie_3d_flattened`.
Import: `convert.lottie_expression`, `convert.font_substituted`, `convert.lottie_unsupported`,
`convert.lottie_text_animator`, `convert.lottie_effect`; SVG: `convert.svg_rasterized`, `convert.svg_unsupported`,
`convert.svg_invalid` (**error**); `convert.svg_pattern`, `convert.svg_filter`, `convert.svg_text` (a pattern fill
or stroke, a filter, a `<text>` element dropped, each under its own code since 0.1.59).
After Effects: `convert.ae_ease_baked`, `convert.ae_layer_skew`, `convert.ae_gradient_stops`,
`convert.ae_gradient_unsupported`, `convert.ae_lut_manual`, `convert.ae_feather`, `convert.ae_font_axes`,
`convert.ae_text_layout`, `convert.ae_color_mixed`, `convert.ae_rendered` (i), `convert.ae_plugin_field`,
`convert.ae_effect_unsupported`, `convert.ae_effect_params` (i), `convert.ae_layer_unsupported`,
`convert.ae_shape_unsupported`, `convert.ae_expression_unsupported`, `convert.ae_driver_unsupported`,
`convert.ae_driver_approx` (i), `convert.ae_loop_count`, `convert.ae_font_unmapped` (i),
`convert.ae_feature_skipped`, `convert.ae_sampling` (i). `convert.unavailable` (error, engine code): a target this
build cannot convert. `convert.prerender_skipped` (warning, service): the sync `motion.convert` left the
particle layers out of an After Effects export because the engine's estimate for their clips was above the call's
budget (`data.prerender_skipped` has the numbers; pass `ae_prerender: true` to render them anyway). Meanings: spec
15 §15.9 and [14-motion-convert.md](14-motion-convert.md).

## `internal.*`, `cancelled`

`internal.io` (an input file the service handed over cannot be read, a bad flag value), `internal.usage` (a bad
command line), `internal.panic` (a caught panic: the location is logged, never the document), `internal.track`: all
exit 5 → `500`, escalated; nothing to fix in the document. `cancelled`: the run received `SIGTERM` (exit 4).
