# 11 · `motion.check`

Validate, normalize, lint and estimate a document without rendering. Sync, cost 1, max 8 concurrent, 60 s, cgroup
1 CPU / 1 GiB / 256 pids, free, daily quota 2,000 calls (`REXX_QUOTA_CHECK`), rate class `data`. Source:
`service/src/tools/check.rs`, `engine/crates/rexx-engine/src/check.rs`, spec 14 §14.5.

**Problems inside the document are the result, never a tool error**: a document with errors answers `200` with
`ok: false` and the diagnostics. Only a malformed call, a document that cannot be read, or an asset that cannot be
resolved is an HTTP error.

## Input

| Field | Type | Default | Meaning |
|---|---|---|---|
| `doc` / `doc_url` | object / string | — | Exactly one ([01](01-documents-and-assets.md)). |
| `variant` | string | `"default"` (the root comp) | The variant to check; passed as `--variant` unless empty or `default`. |
| `canonical` | `true` \| `false` \| `"url"` | absent | `true`: the canonical (expanded) document in `data.canonical`. `"url"`: upload it and return it as the file `canonical.motion.json` (content type `application/vnd.mitte.motion+json`). Anything else: `400` "canonical must be true, false or \"url\"". Large (up to 32 MB); debugging only. |
| `lint` | object | the document's `lint` block | `{ "platform": …, "disable": [ … ] }`, applied on top of the document's block for this call (`platform` replaces, `disable` adds). `platform`: `none`, `broadcast`, `youtube`, `shorts`, `reels`, `tiktok`, `story`, `square`, `linkedin`, `x`; an unknown value is the diagnostic `doc.enum` at `/lint/platform` (`ok: false`). `disable`: any warning or info code (`lint.*`, `physics.*`, `track.*`, …; a bare rule name without `lint.` also matches); errors cannot be silenced. `readingSpeed` and `contrast` are document-only (not in the tool's `lint`). |
| `data` | object | — | Merged over the document's `data`. |
| `sims` | `"url"` | absent | Upload every comp's physics bake so the document can lock it (below). Any other value: `400` "sims must be \"url\"". |

## What runs

1. Tenant check, quota (1 call), the document resolved and written to the scratch.
2. Assets materialized **for check**: fonts, `sim` assets, marker-analysed audio and `library:` files are fetched or
   read; every other https asset is deferred with the probe metadata the cache has.
3. `rexx-engine check --doc doc.json --assets assets.json [--variant v] [--data data.json] [--canonical]
   [--lint-platform p] [--lint-disable a,b] [--sims url] --sim-dir <box sim cache> --memory-mb 921`: normalization
   passes 1–25, lint, stats, the cost estimate, the backend decision, the timing sheet.
4. Exit 0: `ok: true` (warnings and infos may be present). Exit 2/3/4: `ok: false` with the diagnostics **and
   nothing else** (`stats`, `estimate`, `timing`, `canonical`, `sims` are absent, because the engine's result event is
   discarded on a non-zero exit). Exit 5 or a stall: `500 internal`.

## Output `data`

```jsonc
{
  "ok": true,
  "diagnostics": [ { "severity": "warning", "code": "lint.text_too_short_on_screen", "path": "/comps/main/layers/4",
                     "message": "…", "hint": "…", "at": 3.2, "fix": { "op": "replace", "path": "…", "value": 3.1 } } ],
  "stats": { "comps": 3, "layers": 41, "keys": 388, "expressions": 2, "duration": 15, "fps": 30, "frames": 450,
             "size": [1080, 1920], "variants": ["default", "vertical"], "fonts": ["Inter 800", "Inter 500"],
             "library": { "mitte/lower-third.bar": "1.0.0" },
             "assets": [ { "id": "logo", "source": "https://…/logo.svg", "bytes": 18312, "layers": 1 } ] },
  "estimate": { "renderSeconds": 11.2, "msPerFrame": { "p50": 22, "p95": 31, "max": 44 }, "class": "title",
                "costliest": [ { "layer": "captions", "what": "effect light.glow", "share": 0.27 } ], "frames": 450,
                "backend": "cpu", "cpuMs": 22.4, "gpuMs": 9.1, "gpuComplete": true, "requiresGpu": false, "encoder": "cpu" },
  "timing": "t      layer            span          on-screen  enters                 exits                notes\n0.00   bg …",
  "canonical": { "motion": 1, "…": "…" },           // only with canonical: true
  "sims": [ { "comp": "main", "hash": "8c1f…e2", "url": "https://media.mitte.ai/u/…/8c1f…e2.sim", "sha256": "…" } ],  // only with sims: "url"
  "engine": { "version": "0.1.48", "library": "2026.10.0", "fonts": "06acc477…" },
  "billing": { "price": { "amount": 0, "currency": "USD" } }
}
```

| Field | Meaning |
|---|---|
| `ok` | `false` when any diagnostic has `severity: "error"`. |
| `diagnostics[]` | `severity`, `code`, `path` (JSON pointer into the authored document; `""` document-level; omitted when empty), `message`, `hint` (omitted when empty); the engine also writes `related[]`, `fix` and `at` (seconds) where it has them ([30-diagnostics.md](30-diagnostics.md)). Sorted by severity, path, code; deduplicated; at most 200 (errors first). |
| `stats.comps`, `layers`, `keys`, `expressions` | counts over the canonical document (every comp). |
| `stats.duration`, `fps`, `frames`, `size` | the checked comp (the variant's): seconds, frame rate as a number, frame count, `[w, h]`. |
| `stats.variants` | the declared variant ids (empty for a canonical input). |
| `stats.fonts` | `"<family> <weight>"`, sorted. |
| `stats.library` | library **entry** name → the exact version pass 4 resolved. |
| `stats.assets[]` | one row per declared asset in id order: `id`, `source` (the `src` as written), `bytes` (the manifest's size, else the file's, else 0 for a deferred asset not in the cache), `layers` (layers whose `asset` names it). |
| `estimate.renderSeconds` | the whole render including encode, one box with every thread; the admission gate scales it to the thread share. |
| `estimate.msPerFrame` | `p50`, `p95`, `max` per-frame cost on the reference box. |
| `estimate.class` | the 08 §8.3 scene class the cost model assigned. |
| `estimate.costliest[]` | up to three: `layer` (empty for the output stage), `what` (`layer text`, `effect blur.gaussian`, `output`), `share` 0–1. |
| `estimate.frames` | frames in the main comp. |
| `estimate.backend` | `cpu` or `gpu`: the renderer a `motion.render` of this document takes on this box ([16-render-pipeline.md](16-render-pipeline.md)); the service keys the render cache with it. |
| `estimate.cpuMs`, `gpuMs` | mean per-frame milliseconds on each backend (the GPU figure includes its readback). |
| `estimate.gpuComplete` | whether the device walk renders the main comp resident (no readback at all). |
| `estimate.requiresGpu` | the document has a GPU-only effect (`utility.shader`); on a CPU job the layer passes through unshaded with `effect.requires_gpu`. |
| `estimate.encoder` | the document's `output.encoder`, `cpu` or `nvenc` (NVENC only renders on a GPU box). |
| `timing` | the timing sheet (below). |
| `canonical` | the canonical document (with `canonical: true`). |
| `sims[]` | with `sims: "url"`: `comp`, `hash` (the simulation's input hash), `url` (the uploaded `<hash>.sim` under the caller's prefix), `sha256` (of the file). |
| `engine` | `version`, `library`, `fonts` (the pack hash); empty strings are omitted. |

Extra diagnostics only `check` adds: one `convert.lottie_particles` **info** per enabled particle layer (what each
export target will do with it), `effect.unknown_param` **errors** at every parameter an enabled effect does not
declare (`/comps/main/layers/0/effects/0/params/startColor`; a group field by its dotted name, `params/shimmer.speed`;
the message lists the effect's parameters; the renderer only warns once it draws the layer), `effect.requires_gpu`
warnings when the backend decision is the CPU and the document has `utility.shader` effects, and
`effect.shader_invalid` / `effect.param_value` errors for a shader whose source, uniforms or inputs fail validation
(checked on every box, GPU or not).

### The timing sheet

A plain-text table, one row per visible layer sorted by `in` (generated layers grouped by their repeat or component),
beat markers as their own rows, at most 120 rows (longer documents get a per-comp summary):

```
t      layer            span          on-screen  enters                 exits                notes
0.00   bg               0.00–12.00    12.00      fadeIn 0.4 power2.out  –
0.20   title            0.20–4.10     3.25       rise 0.7 expo.out      fadeOut 0.3 @3.80    3 words, needs 1.0s ✓
```

Columns: `t` (start), `layer` (or group, `bars.* (×6)`), `span` (visible), `on-screen` (seconds fully visible),
`enters` (the motion named from the shape of its keys: `fadeIn`, `fadeOut`, `rise`, `drop`, `sink`, `lift`,
`slideIn`, `slideOut`, `growIn`, `growOut`, `popIn`, `scaleIn`, `scaleOut`, else the property names; then duration
and ease), `exits`, `notes` (reading-time check with ✓, counts, values, warnings by short name, `beat_hits n/m`).
A paged or word-timed text layer (a caption) is followed by one row per page, `<layer> p<n>`, with the page's span,
word count and opening words, when the pages fit in the 120 rows.

### Locking a physics take (`sims: "url"`)

The engine writes each comp's bake to `sims/<hash>.sim`; the service moves it into the box's sim cache
(`<REXX_CACHE_ROOT>/sim/<hash>.sim`, so later runs on this box read it instead of simulating), uploads it as
`<hash>.sim` under the caller's prefix (`application/octet-stream`) and copies it to the content-keyed
`rexx/cache/sim/<hash>.sim` (180-day expiry). A bake the engine listed but did not write is left out. To lock:

```jsonc
"assets": { "take": { "src": "https://media.mitte.ai/u/…/8c1f…e2.sim", "type": "sim", "sha256": "<sims[].sha256>" } },
"comps": { "main": { "physics": { "…": "…", "lock": { "asset": "take", "hash": "8c1f…e2" } } } }
```

Without object storage or a sim cache on the box: `500 internal`.

## Errors (HTTP)

| Status | When |
|---|---|
| 400 `bad_request` | neither or both of `doc`/`doc_url`; invalid JSON; `canonical` or `sims` outside their values; an asset `src` that is neither https nor a shipped `library:` file (`asset.bad_url`, with the diagnostic in `error.data.diagnostics`); a font, sim or marker-audio asset that cannot be fetched (`asset.*` message) |
| 413 `too_large` | the document over `REXX_MAX_DOC_BYTES`; more than 512 declared assets; a fetched asset over its cap |
| 429 | the daily check quota (`overloaded`) or the per-minute `data` class (`rate_limited`) |
| 500 `internal` | engine exit 5, a stalled run, `sims: "url"` without storage |
| 503 `overloaded` | budget or slot unavailable; no engine on the box |

## Examples

```json
{ "doc_url": "library:mitte/demo/title-card@1", "variant": "vertical", "lint": { "platform": "tiktok" } }
```
The vertical variant against TikTok's safe zone.

```json
{ "doc": { "motion": 1, "comps": { "main": { "size": [1920, 1080], "fps": 30, "duration": 3, "background": "#101014",
           "layers": [ { "id": "t", "type": "text", "text": "Hello", "style": { "size": 120, "fill": "#FFFFFF" },
                         "align": { "to": "comp", "x": "center", "y": "center" } } ],
           "timeline": [ { "target": "t", "preset": "fadeIn", "dur": 0.5 },
                         { "target": "t", "preset": "fadeOut", "dur": 0.4, "at": 2.4 } ] } } },
  "canonical": true }
```
A minimal document with the canonical form returned ([examples/check-minimal.motion.json](examples/check-minimal.motion.json)).

```json
{ "doc_url": "library:mitte/demo/title-card@1", "data": { "name": "Sam Okafor", "title": "Finance" }, "sims": "url" }
```
Templated data; every physics bake uploaded for locking (none for this document: `sims` is `[]`).

Registry examples: `title-card`, `tiktok-lint`, `variant-data`, `data-story`, `3d` ([91-schema-check.md](91-schema-check.md)).

Since engine 0.1.59 (K-28) `data.diagnosticsTruncated: true` says the engine capped the list at 200 (errors first),
`stats.assets[]` rows carry the declared `type`, and the `engine` block is `{ version, fonts, library, ffmpeg }`
as `rexx-engine version` reports them. `check` materializes fonts, `sim` bakes, marker audio and `library:` files
only; a `$data.@asset` reference is checked against what the cache holds (`asset.unmaterialized` otherwise).
