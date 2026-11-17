# 14 · `motion.convert`

Export a document to its canonical form, Lottie, dotLottie, an After Effects script or the camera path; import a
Lottie, dotLottie or SVG file as an editable document. Sync, cost 1, max 4 concurrent, 120 s, cgroup 1 CPU / 1 GiB,
free, daily quota 500 calls (`REXX_QUOTA_CONVERT`), rate class `data`, output asset type `text`. Source:
`service/src/tools/convert.rs`, `engine/crates/rexx-engine/src/convert.rs`, spec 15, 06 §6.6.

A call is **either** an export (`doc`/`doc_url` + `to`) **or** an import (`from` + `url`); both → `400` "convert is
either an export (doc + to) or an import (from + url), not both"; neither → `400` "give doc (or doc_url) with to for
an export, or from with url for an import". `to` outside its list: `400` "to must be one of canonical, lottie,
dotlottie, aejsx, camera"; `from` outside its list: `400` "from must be one of lottie, dotlottie, svg"; an empty
`url` or one starting with `@`: `400` "url must be an https URL of the file to import".

## Input

| Field | Type | Values | Meaning |
|---|---|---|---|
| `doc` / `doc_url` | | | Export: the document, exactly one. |
| `to` | enum | `canonical`, `lottie`, `dotlottie`, `aejsx`, `camera` | Export target (default `canonical` in the engine, but the service requires it). |
| `variant` | id | | Export: the variant (exporters read the normalized document of that variant). |
| `data` | object | | Export: merged over the document's `data`. |
| `from` | enum | `lottie`, `dotlottie`, `svg` | Import source format. |
| `url` | https URL or `library:` URI | | Import: the file. Fetched as an asset (`svg` sniffed as an image, `lottie` as data, `dotlottie` unsniffed; the engine checks it starts with `PK`). |
| `options` | object | below | Any value outside its list is the diagnostic `doc.enum` at `/options/<name>` (a `400`); `options` that is not an object is `doc.type` at `/options`. Unknown option names are ignored. |

### Options

| Option | Applies to | Values | Default | Meaning |
|---|---|---|---|---|
| `text` | lottie, dotlottie | `layer`, `outlines` | `layer` | `layer`: Lottie text layers (`ty: 5`; needs the fonts at playback). `outlines`: glyph shapes; the exporter has no shaped outlines yet, so the layer is written as `layer` with the info `convert.lottie_text_outlines`. |
| `bake_expressions` | lottie, dotlottie, aejsx | boolean | `true` (Lottie); `false` (AE) | Bake drivers, loops, springs and expressions to fitted keyframes, or write them as expressions. |
| `bake_fps` | lottie, dotlottie, aejsx | number > 0 | the comp's fps | Sampling rate for baking (and for `render_unsupported` sequences). |
| `bake_tolerance` | lottie, dotlottie, aejsx | number > 0 | `0.005` | Maximum error of baked or fitted curves as a fraction of the property's range (positions 0.25 px when tighter). |
| `effects` | lottie, dotlottie | `drop`, `players` | `drop` | Lottie has no effects: drop them, or write lottie-web effect objects for the few players render (`generate.fill`, `color.tint`, `color.tritone`, `stylize.dropShadow`, `blur.gaussian`, `control.*`). `render` is `doc.enum` ("\"render\" is P3"). |
| `render_unsupported` | lottie, dotlottie | boolean | `false` | Render each particle layer with this binary (a child `render`, CPU backend, the comp isolated to that layer with cameras and lights kept) to a transparent PNG sequence at `bake_fps` (else the comp's rate) and embed it as image layers in a precomp; transparent frames are skipped; one info `convert.lottie_particles` reports the frame count and the added MB. A layer that cannot be rendered: a `convert.lottie_particles` warning, the layer dropped. |
| `embed_images` | lottie | boolean | `true` | `false` writes the images as `images/<file>` next to the JSON (returned as extra files, stored under that relative path so the JSON's `u: "images/"` resolves). Only PNG, JPEG and WebP assets up to 64 MB are embedded or written. dotLottie always packs images inside the archive. |
| `ae_min_version` | aejsx | version string | computed | Raise (never lower) the minimum After Effects version the script requires. |
| `ae_prerender` | aejsx | boolean | `true` | Render each particle layer to a ProRes 4444 clip with alpha, stored as `assets/<comp>-<layer>.mov` next to the script (an extra `video` file), which the script imports into a precomp `<layer> (rendered particles)`. `false` drops them with `convert.ae_layer_unsupported`. Left unset, the service first checks the document and turns it off when the engine's estimate for the clips (`renderSeconds` once per particle layer, scaled to the one core the child render gets under the tool's CPU quota) is above this call's prerender budget (a quarter of the tool's 120 s timeout, at most the sync budget): the export then carries the warning `convert.prerender_skipped` and `data.prerender_skipped` (`estimate_seconds`, `budget_seconds`, `layers`). Pass `true` to render anyway. |
| `font_map` | aejsx | object `{ "<family>": "<PostScript name>" }` | | Font names the script uses; a family without one gets a synthesized name (`convert.ae_font_unmapped`). |
| `comp_id` | svg, lottie, dotlottie import | id | `main` | The root comp's id. |
| `fps` | svg import | number > 0 | `30` | The comp's frame rate. |
| `duration` | svg import | seconds > 0 | `5` | The comp's duration. |
| `layers` | svg import | `top-groups` (default), `single` | | One shape layer per top-level `<g>` or one layer for everything. |
| `theme` | dotlottie import | theme id | the manifest's first | The dotLottie theme applied to the file's slots (a missing one is reported and ignored). |
| `animation` | dotlottie import | animation id | the manifest's first | Which animation to import. |

The service sets two import options itself and strips them from the caller's: `files_base_url` (the run's output
directory URL, so the imported document's assets point at the files returned beside it) and `source_url` (the `url`
the file came from, for relative image references). Spec 15 §15.2.1 also lists `themes`, `ae_ease` and `ae_plugins`;
the engine ignores them today (the registry's `after-effects` example passes `ae_plugins` harmlessly).

## What runs

Export: every asset materialized; `rexx-engine convert --doc … --assets … --to <to> --out out/<name> [--variant v]
[--data …] [--options options.json]`. Import: the source fetched; `rexx-engine convert --from <from> --in <file>
--out out/<source stem>.motion.json [--options …]`. The engine decides the final extension (an `aejsx` package with
assets may come back as a `.zip`); the service keeps its base name.

## Output

The first file is the result; further files are what it references by relative path, stored next to it. `files` is
a `{label: url}` map when every label is unique (the result labelled by the target, e.g. `lottie`, or `document` on
import; extras `image`, `video`, `font`, `audio` by extension), else a plain list (two images make duplicate labels).

| Target | File | Extras |
|---|---|---|
| `canonical` | `main.motion.json` (`application/vnd.mitte.motion+json`) | — |
| `lottie` | `main.json` (Lottie 1.0.1) | `images/<file>` with `embed_images: false` |
| `dotlottie` | `main.lottie` (a zip, `application/zip`; dotLottie 2.0: one animation per variant, images in `i/`, fonts with `text: "layer"`, the document's theme tokens as themes) | — |
| `aejsx` | `main.jsx` (or `main.zip` when the package carries assets) | `assets/<comp>-<layer>.mov` per pre-rendered particle layer |
| `camera` | `main.camera.json` (`application/json`): `camera_path: 1`, `generator`, `comp`, `size`, `fps`, `fps_rational`, `duration`, `frame_count`, `convention` {units, axes, camera, rotation, projection, lens, time, dof}, `frames[]` {`frame`, `t`, `layer` (null for the default camera), `position [x,y,z]`, `quaternion [x,y,z,w]`, `euler_xyz_deg`, `matrix` (16, row-major, camera→world), `zoom` px, `film_size_mm`, `focal_length_mm`, `fov_deg`, `dof` (null or {focus_distance, aperture, blur_level})}; comp pixels, x right, y down, z into the screen; at most 216,000 frames (`limit.frames` at the comp's `duration`); `coverage` is always 1 | — |
| import (`svg`, `lottie`, `dotlottie`) | `<source stem>.motion.json` (the stem kept to `[A-Za-z0-9_-]`, else `imported.motion.json`) | Lottie/dotLottie: the embedded images, fonts and audio as `images/<file>`, `fonts/<file>`, `audio/<file>`, which the document's `assets` already point at |

```jsonc
{ "warnings": [ { "severity": "warning", "code": "convert.lottie_effect", "path": "/comps/main/layers/2/effects/0",
                  "message": "Lottie cannot express 'light.glow'; the layer is exported without it." } ],
  "coverage": 0.92,
  "billing": { "price": { "amount": 0, "currency": "USD" } } }
```

| Field | Meaning |
|---|---|
| `warnings[]` | every `convert.*` warning and info (what the target cannot carry and what was done instead), plus normalization's warnings; paths point into the authored document (export) or the Lottie JSON (import). |
| `coverage` | the share of layers no warning points into, 0–1 (three decimals; an import's infos, such as text kept as glyph outlines, are not loss); 1 for `canonical` and `camera`; imports report the engine's own, 0 included (`1` only when the engine reports none). |

An import always yields a document that passes `motion.check` (it is normalized before it is written; expressions
the compiler rejects are dropped with `convert.lottie_expression`, their keyframes kept; fonts outside the pack
become Inter with `convert.font_substituted`), with one exception: a document above 2 MB fails with `limit.doc_size`.

## Errors

| Status | When |
|---|---|
| 400 `bad_request` | export/import mixed or missing; a bad `to`/`from`/`url`; the document has errors; an option outside its list (`doc.enum` at `/options/<name>`); a source that is not valid SVG (`convert.svg_invalid`) or not a Lottie (`asset.unreadable`), or a dotLottie that is not a zip; a Lottie above the caps (`limit.lottie`: 20 MB JSON, 5,000 layers, precomp depth 16; `limit.archive`: 1,000 entries, 2 GB, ratio 100); a camera path over 216,000 frames (`limit.frames`); an asset that cannot be used |
| 413 `too_large` | document or asset caps (an import file over 256 MB is `asset.unreadable`) |
| 500 `internal` | "conversion produced no file", a listed extra file missing, engine exit 5 |

`convert.unavailable` (exit 2) is reserved for a target this build cannot convert; every listed `to` and `from` is
available in 0.1.48.

## Examples

```json
{ "doc_url": "library:mitte/demo/lower-third@1", "to": "lottie", "options": { "embed_images": false, "effects": "players" } }
```
Lottie with images as sibling files and the player-renderable effects kept.

```json
{ "doc_url": "library:mitte/demo/lower-third@1", "to": "dotlottie", "options": { "text": "outlines" } }
```
A dotLottie (today written with text layers plus `convert.lottie_text_outlines`).

```json
{ "doc_url": "library:mitte/demo/lower-third@1", "to": "aejsx", "options": { "bake_expressions": true, "font_map": { "Inter": "Inter-Bold" } } }
```
An After Effects script with expressions baked.

```json
{ "doc_url": "library:mitte/demo/classic-3d@1", "to": "camera" }
```
The camera path for a matching 3D clip (hand it to `mesh_scene_video` as `camera_path_url`).

```json
{ "from": "svg", "url": "library:mitte/demo/logo@1", "options": { "comp_id": "logo", "fps": 30, "duration": 4 } }
```
The demo logo as a shape-layer document `logo.motion.json`.

```json
{ "from": "dotlottie", "url": "library:mitte/demo/badge@1", "options": { "theme": "night" } }
```
The demo badge with its night theme, as `badge.motion.json` plus its embedded files.

Registry examples: `lottie`, `dotlottie-outlines`, `after-effects`, `camera-path`, `import-svg`, `import-dotlottie`
([94-schema-convert.md](94-schema-convert.md)).

Since engine 0.1.59 (K-29) `effects: "render"` embeds each layer with effects as a rendered image sequence (admitted
by the engine's estimate like `ae_prerender`; above the budget it is downgraded to `drop` with
`convert.prerender_skipped`), `themes` packages extra dotLottie themes (library references or `{ id, tokens }`
objects), an unknown option is a `doc.unknown_field` warning at `/options/<name>`, and the `ae_ease` and
`ae_plugins` options of earlier drafts are withdrawn (neither was built). The files envelope is the framework's
`{label: url}` map (`lottie`, `image`, …) or a `[url]` list, as 06 §6.6 now shows.
