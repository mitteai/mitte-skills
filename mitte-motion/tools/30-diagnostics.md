# 30 · Diagnostics: the format, the exit classes, and the document codes

Every problem the engine finds is a **diagnostic** against the document the author wrote. This page: the record,
how it reaches the caller, how to work through a list, and the codes of the normalizer and validator (document
structure, references, animation, tweens, presets, components, placement, paths, layers, text, fonts).
[31-diagnostics-2.md](31-diagnostics-2.md) has assets, effects, expressions, limits, tracking, physics, the
renderer, media, output, encoding, interchange and internals; [32-lint.md](32-lint.md) the lint rules;
[33-codes-inventory.md](33-codes-inventory.md) the generated cross-check. Sources: spec 14, `rexx-doc/src/diag.rs`,
the crate `codes` modules, `service/src/engine.rs`.

## The record

```jsonc
{ "severity": "error",                               // error | warning | info
  "code": "tween.unknown_label",                     // stable, <area>.<name>
  "message": "Position \"outro+=0.2\" uses the label \"outro\", which is not defined.",
  "path": "/comps/main/timeline/7/at",               // RFC 6901 pointer into YOUR document ("" = document level)
  "hint": "Define it with {\"label\": \"outro\", \"at\": …} before this tween, or use one of: intro, beat1.",
  "related": [ { "path": "/comps/main/timeline/0", "message": "labels defined here: intro" } ],   // optional
  "fix": { "op": "replace", "path": "/comps/main/timeline/7/at", "value": "intro+=0.2" },         // optional JSON Patch
  "at": 3.2 }                                        // optional: the comp time, seconds
```

- `error` blocks: `motion.check` answers `ok: false`; `frames`, `render`, `convert` refuse (`400`) before any
  pixel, nothing charged. `warning` and `info` never block; they come back in `check.diagnostics`,
  `frames.diagnostics`, `render.variants.<id>.warnings`, `convert.warnings`, `track.warnings`.
- `path` points at what you wrote even when the problem was found in something generated from it (a key from a
  tween, a layer from a component): diagnostics are mapped back through the source map. A filled default points at
  the nearest authored ancestor. The service's own refusals use `/output/<field>`, `/doc/output/<field>`,
  `/assets/<id>/src`; `motion.frames` time errors `/times`; `motion.convert` options `/options/<name>`;
  `motion.track` request errors `/items/<id>`, `/corrections/<i>`, `/method`, `/type`.
- `fix` is a JSON Patch operation (`add`, `replace`, `remove`) you may apply literally; it is never applied for
  you. `hint` lists valid values (up to 20, else the nearest by edit distance).
- Lists are sorted by severity (errors first), then path, then code, deduplicated, capped at 200 per run; a
  frame's own diagnostics are deduplicated by code and path across frames (so one per condition, not per frame).

## How it reaches the caller

| Path | Shape |
|---|---|
| `motion.check` | `data.ok`, `data.diagnostics` (`200` either way) |
| `frames`, `render`, `convert`, `track` on `/v1/run` with an error | `400 bad_request`; `error.message` = `"bad_request: the document is invalid: <path>: <message>; … (+N more)"` (the first three), `error.data.diagnostics` = all of them |
| the same on `/v1/jobs` | the job's `error: {code, message}` only (no `data`); check first |
| an asset problem (exit 3) | `400`, message "an asset could not be used: …" |
| a limit (exit 4) | `400`, message "the document exceeds a resource limit: …" |
| a service refusal before the engine (`output.*`, `asset.bad_url`) | `400` with one diagnostic in `error.data.diagnostics`, as the engine would report it |
| warnings on success | the tool's `diagnostics`/`warnings` list (`lint.disable` silences any warning or info, never an error) |

Exit classes (`rexx-engine`): 2 invalid, 3 asset, 4 limit (`limit.*`, `render.deadline`, `encode.timeout`,
`cancelled`), 5 internal (`internal.*`, `encode.*` other than timeout) → `500`, escalated. Within one run the most
specific class wins.

## Working through a list

1. Fix every error top-down; apply `fix` where present; re-check. At most three rounds, then tell the user what
   could not be resolved.
2. The tables below give the trigger and
   the fix for every code.
3. A warning you disagree with goes into `lint.disable` (document or per call), once, with a reason.

## `doc.*` document structure (errors)

| Code | Fires when | Fix |
|---|---|---|
| `doc.json` | the text is not valid JSON (also the `--data` overlay, at `/data`, and `convert` `--options`) | repair the JSON; `message` has line and column |
| `doc.duplicate_key` | an object repeats a key | remove the duplicate |
| `doc.version_missing` | no `"motion"` field | add `"motion": 1` |
| `doc.version_unsupported` | `motion` newer than the engine | use `1` |
| `doc.unknown_field` | a field this object does not define (`meta` and `x-*` are allowed); also an unknown text-animator property | the hint lists the valid fields, nearest first; copy shapes from the guide |
| `doc.required` | a required field is missing (`size`, `fps`, `duration`, `layers`, a shape item's field, `layer` on a track reference) | add it |
| `doc.type` | the wrong JSON type, a non-finite or absurd number, a shape or physics field out of range; `motion.frames` times outside the comp (`/times`); `convert` options not an object | use the type and range the hint names |
| `doc.enum` | a value outside its list (`lint.platform`, `safe_overlay`, `convert` options `text`/`effects`, codecs, eases spelled as enums) | pick one of the listed values |
| `doc.id_invalid` | an id outside `^[A-Za-z_][A-Za-z0-9_-]{0,63}$` | letters, digits, `_`, `-`; no dots, slashes, spaces |
| `doc.id_duplicate` | two siblings share an id | rename one |
| `doc.main_ambiguous` | no `main` field, no comp `main`, more than one comp | name the root comp `main` or set `"main"` |
| `doc.no_comps` | `comps` is empty | add a comp |
| `doc.reserved_id` | an authored id starts with `_` | drop the underscore (generated ids only) |
| `doc.time_needs_comp` | a frame-based time (`"12f"`, timecode) where no comp rate applies: `output.range`, asset `sequence`, `markers.from` | seconds |
| `doc.canonical_only` | `sims`, a `{sim, body}` reference or a `_physics` animator in an authored document | remove; let the normalizer write them |
| `doc.range_invalid` | (audio mixer) a mix range that ends before it starts | fix `output.range` / the layer's `in`/`out` |
| `doc.time_overflow` | (audio mixer) a tick computation overflowed (absurd times) | use times inside the comp |

## `ref.*` references (errors)

| Code | Fires when | Fix |
|---|---|---|
| `ref.unresolved` | `$theme.…`, `$data.…`, `$props.…`, `$item.…` names nothing | only tokens the theme defines; check the `data` path; `library/90-catalogue.md` lists tokens |
| `ref.template` | a `{{ … }}` template is malformed or its arithmetic fails (division by zero, non-number) | fix the expression |
| `ref.format` | an unknown format name or bad arguments in a template (`currency:USD:0`) | spec 12 §12.2.1's formats |
| `ref.layer` | `parent`, `matte.layer`, `fitTo`, `follow.path`, `align.to`, a tween target names no layer in the comp | declare it or fix the id |
| `ref.comp` | a comp layer (or `main`) names no comp; also `frames`/`render` asked for a comp that does not exist (`/main`) | fix the id |
| `ref.asset` | a layer, font or effect names an undeclared asset id | declare it in `assets` |
| `ref.library_unknown` | a `mitte/…@n` reference names no library entry | `library/90-catalogue.md` for the exact ref |
| `ref.library_version` | the entry exists, not at that version | the hint lists available versions |
| `ref.variant_unknown` | the requested `variant` is not defined | the document's `variants` keys |
| `ref.variant_layer` | a variant override names a layer the root comp lacks | fix the id |
| `ref.marker` | a time names a marker that does not exist (forces, `measureAt`, `motion.frames` times) | an existing `@name`; a tween's `at` is `tween.unknown_marker` |

## `anim.*` keyframes, eases, drivers (errors)

| Code | Fires when | Fix |
|---|---|---|
| `anim.not_animatable` | keys, drivers or `expr` on a static-only property | a static value |
| `anim.duplicate_key` | two keys at one tick | merge them |
| `anim.unsorted_keys` | key times not increasing | sort them |
| `anim.value_type` | a key value of the wrong shape (a vector on opacity) | match the property |
| `anim.ease_unknown` | an ease name outside the catalog | the hint's nearest names (`power2.out`, `expo.out`, …) |
| `anim.ease_params` | bad ease parameters (`steps(0)`, bezier x outside 0–1) | spec 2 §2.2 |
| `anim.ease_on_spatial_dims` | per-dimension eases on a spatial property | one ease |
| `anim.path_on_nonspatial` | `path` tangents on a non-spatial property | remove them |
| `anim.rove_endpoint` | `rove: true` on the first or last key | only inner keys rove |
| `anim.loop_too_few_keys` | a loop with fewer than two keys | two keys |
| `anim.driver_params` | a driver missing or with invalid fields (`wiggle` without `amp`) | spec 2 §2.9 |
| `anim.dimension_mix` | the whole vector and a separate dimension both keyed explicitly | one or the other (tweens may mix) |
| `anim.spring_unstable` | spring parameters that never settle (damping ≤ 0) | positive damping |
| `anim.value_and_keys` | more than one of `value`, `keys`, `track`, `sim` on one property | exactly one; a base `value` or `keys` beside a `rotation` or `scale` `track` is allowed (the base the tracked delta composes with) |
| `anim.separate_discards_path` | separating a position with spatial tangents or roving keys (spec-only today) | separate explicitly or drop the tangents |

## `tween.*` the timeline (errors unless marked)

| Code | Fires when | Fix |
|---|---|---|
| `tween.no_action` | none of `from`, `to`, `fromTo`, `set`, `preset` | add one |
| `tween.multiple_actions` | more than one of them | one per entry |
| `tween.unknown_target` | the target resolves to nothing (no layer, unit, item or effect; a templated or `bars.*` target matching nothing) | the hint; `repeat` ids are `<id>.<index>` |
| `tween.target_disabled` (info) | every target was dropped (`enabled: false`, a repeat with zero rows); the tween is a no-op | expected for param-gated content |
| `tween.unknown_label` | `at` names an undefined label | define `{"label": …}` earlier, or use the hint's labels |
| `tween.unknown_marker` | `at` names an undefined marker | read the beat rows in the timing sheet |
| `tween.bad_position` | `at` is not a position expression (`<`, `>`, `+=`, a label, `@marker`, a number) | spec 2 §2.6.2 |
| `tween.unknown_property` | a `from`/`to` property the target lacks | the hint lists shorthands and properties |
| `tween.relative_type` | `"+=40"` on a non-numeric property | an absolute value |
| `tween.both_relative` | a `fromTo` with both ends relative | one absolute end |
| `tween.key_collision` | a generated key lands on an explicit key of the same property (also `crawl`) | move one by a frame |
| `tween.text_unit_property` | a property text units cannot take | `opacity`, `fill`, `stroke`, `scale`, `weight`, `axes.*`, offsets |
| `tween.set_with_duration` | `set` with `dur` > 0 | drop `dur` |
| `tween.auto_duration` | `dur: "auto"` without a spring ease | a number, or a spring |
| `tween.negative_time` | the tween starts before 0 (and the layer's `in` is not before 0) | later `at` |
| `tween.no_paint` | a `fill`/`color`/`stroke`/`strokeWidth` shorthand on a shape with no such item | add the item |
| `tween.stagger_params` | neither or both of `each`/`amount`, a negative delay, a grid that cannot hold the targets, `from` out of range, `[col,row]`/`axis` without `grid` | spec 2 §2.7 |

## `preset.*`, `component.*`, `repeat.*`, `data.*`, `layout.*`, `theme.*`

| Code | Fires when | Fix |
|---|---|---|
| `preset.unknown` | an unknown preset name | the hint; `library/90-catalogue.md` |
| `preset.param` | bad preset props | the preset's params |
| `preset.cycle` | presets using each other in a loop | break it |
| `preset.target_kind` | a preset on a layer kind it has no meaning for (`drawOn` without a stroked path) | add the stroke; another preset |
| `component.unknown` | an unknown component ref | the catalog |
| `component.unknown_param` | a prop the component lacks | the hint lists params |
| `component.param_invalid` | wrong type, out of range, over `maxChars`/`maxLines` | shorten, retype |
| `component.param_required` | a required prop missing | add it |
| `component.slot_unknown` | a slot the component lacks | the catalog's `slots` |
| `component.slot_required` | a `required: true` slot left empty | fill it |
| `component.cycle` | components instantiating each other | break it |
| `component.depth` | instances nested more than 4 deep inside definitions | flatten |
| `repeat.data_not_list` | `repeat.data` is not a list | a list (or `$data.rows`) |
| `repeat.id_template` | generated ids not unique or invalid | a template with `$index` |
| `data.bad_point` | a `points` row that is not two numbers, or a `keys` row missing a named field | fix the row |
| `layout.invalid` | a `grid` with neither `columns` nor `rows`, or an unknown layout `type` (at the repeat's or comp's `layout`) | spec 12 §12.5 |
| `layout.overflow` (w) | items a `stack` or `grid` placed outside its box (the message names them) | fewer items, smaller gap or cell, larger box |
| `theme.invalid` | a token of the wrong type (a font where a colour goes) | fix the override |

## `place.*`, `safe.*`, `path.*`, `gradient.*`, `matte.*`

| Code | Fires when | Fix |
|---|---|---|
| `place.anchor_conflict` | `origin` and an explicit `anchor` on one layer | one of the two |
| `place.percent_with_parent` | a percentage position (or `align`) under a parent that scales, rotates or skews | pixels, or a translate-only parent |
| `place.align_with_absolute_keys` | `align` with absolute position keys | relative tween values |
| `place.align_cycle` | align targets in a cycle | break it |
| `place.keep_place_with_keys` | `keepPlace` with absolute position keys | drop one |
| `safe.title_outside_action` | the comp's title-safe box larger than its action-safe box | `title` ≥ `action` inset |
| `path.morph_count` | `morph.match: "index"` across keys with different vertex counts | `match: "auto"` or equal counts |
| `path.multiple_subpaths` | several subpaths where one is expected (a mask, a path key) | one subpath |
| `path.invalid` | vertex and tangent arrays of different lengths, a malformed path string; at render a path that cannot be rasterized | fix the path |
| `path.unavailable` (w) | a later-phase shape item or gradient kind; ignored (none today: `feather` and `freeform` are built) | remove it |
| `gradient.stops_resampled` (info) | gradient stop keys with different counts resampled to one list | expected |
| `matte.cycle`, `matte.depth` | mattes in a cycle (at each member's `matte/layer`); a chain deeper than 8 (at the chain's head); the renderer's own guard for both is `render.matte` | simplify the chain |

## `layer.*`, `3d.*`, `text.*`, `font.*`

| Code | Fires when | Fix |
|---|---|---|
| `layer.field_not_allowed` | a field foreign to the layer type (`text` on a solid; `masks`/`styles`/`matte`/`blend` on a null; a non-`control.*` effect on a null, camera or light; `threeDPerChar` without `threeD`); as a warning, 3D animator fields without `threeDPerChar` | remove the field or change the type |
| `layer.empty_span` | `out` ≤ `in` | fix the times |
| `layer.parent_cycle` | parenting in a cycle (at render `render.parent`) | break it |
| `layer.parent_2d_to_3d` | a 2D layer parented to a 3D one (cameras and lights count as 3D) | `threeD: true` on the child |
| `layer.comp_cycle` | a comp contains itself, or nesting over 16 (at render `render.cycle`, `render.depth`) | un-nest |
| `layer.matte_self` | a layer mattes itself | another layer |
| `layer.camera_not_3d` (w) | a camera in a comp with no 3D layer and no collapsed comp layer (at the camera) | `threeD: true` |
| `layer.light_invalid` (w) | a light with non-finite or out-of-range values (beyond ±10⁹ px); skipped | fix the values |
| `layer.time_remap_type` | `timeRemap` on a layer without source time (solid, shape, text) | footage or a comp layer |
| `layer.freeze_conflict` | `freeze` with `timeRemap`, `speed`, `loop`, `sourceIn`/`sourceOut` | one timing control |
| `layer.transition_needs_pair` | a two-layer transition (`push`, `reveal`, `morph`, `fadeThrough`) used one-sided | a one-sided type, or `scenes` |
| `layer.scene_size` | a scene comp whose size differs from the root's | match sizes |
| `layer.styles_on_adjustment` | `styles` on an adjustment layer | remove |
| `layer.zero_stretch` | `stretch: 0` or `speed: 0` | a non-zero value |
| `layer.camera_invalid` | (3D renderer) a camera value not finite or outside the renderer's bounds | finite zoom/position |
| `layer.transform_invalid` | (3D renderer) a card's transform, size, opacity or source mapping not finite or empty | finite values |
| `3d.renderer_mismatch` (w) | a collapsed comp layer whose comp's `renderer3d` differs from this comp's; it renders as an isolated group (at `collapse`) | the same `renderer3d` |
| `text.too_long` | over 10,000 characters in a layer | split the text |
| `text.unit_out_of_range` (w) | a selector addresses units beyond the text | fix the range |
| `text.path_invalid` | text-on-path names a mask or shape path that does not exist | an existing path |
| `text.path_box` | box text on a path | point text |
| `font.not_found` | a family/weight/style in neither the pack nor the document's font assets | the hint's five nearest families, or a `font` asset |
| `font.missing_glyphs` (w) | characters no font in the chain covers (`.notdef` boxes) | another font; `message` lists them |
| `font.fallback_used` (w) | characters taken from a fallback font (emoji, CJK) | expected; check the look |
| `font.axis_missing` (info) | an `axes` tag the font lacks; ignored | drop it |
| `font.pack_missing` (w) | no font pack on the box: every text layer is then `font.not_found` | install the pack (`--fonts`) |
| `font.pack_invalid` (w) | the pack failed to load (hash mismatch, unreadable) | reinstall |
