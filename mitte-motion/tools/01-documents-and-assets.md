# 01 · Documents, `doc_url`, `library:` URIs, `data`, variants, assets

What every tool that takes a document shares (`service/src/shared.rs`, `service/src/assets.rs`, spec 1 §1.7,
03-architecture §3.4). The document itself (its fields, layers, tweens) is the `language` area; this page is the
contract at the tool boundary.

## `doc` versus `doc_url`

| Input | Type | Rule |
|---|---|---|
| `doc` | object | The motion document inline, a JSON object with `"motion": 1`. Not a string. Capped at `REXX_MAX_DOC_BYTES` (1 MiB default; the engine's own `limit.doc_size` is 2 MB) once re-encoded. |
| `doc_url` | string | An `https:` URL of a `.motion.json`, or a `library:<namespace>/<path>@<version>` URI of a document the library ships. Fetched like an asset (same host rules and caps), then capped at `REXX_MAX_DOC_BYTES`. |

From the assistant, always `doc_url`: the document is written as part files and joined with `fs.concat` (or one file
continued with `fs.write` `append: true`) into a `.motion.json` in the user's library, and every tool takes that
file's url. Inline `doc` is for callers that already hold a small document. Inside the document, an asset the
assistant made or found is named by its `@url_…` reference as `src`; the reference is substituted with the real url
when the part file is saved, so the saved document carries fetchable urls and the assistant never writes one by hand.

Exactly one. Both → `400 bad_request` "provide either doc or doc_url, not both"; neither → `400` "provide the document
as doc (a JSON object) or doc_url (an https URL or a library:<namespace>/<path>@<version> URI of a .motion.json)".
A `doc_url` starting with `@` (an unsubstituted `@url_<asset>` reference) → `400` "doc_url must be an https URL; the
@… reference was not resolved to one". Unparseable JSON → `400` "the document is not valid JSON: …". Over the cap →
`413 too_large` "the document is N KB; the limit is M KB". Everything else about the document's shape is the engine's
to report as diagnostics.

The shell reads only four things out of the document before the engine runs: `assets` (to materialize), `output`
(defaults for `motion.render`), `variants` (ids), and which comps have `markers[].from.audio` (audio that
`motion.check` must fetch). Declaring more than `REXX_MAX_ASSETS` (512) assets is `413` before any fetch.

## `library:` URIs (spec 1 §1.7, spec 12 §12.6.2)

`library:<namespace>/<path>@<version>` names a file the engine image ships under
`<library root>/<namespace>/assets/<path>.<ext>`; the extension is dropped from the reference. Resolution happens in
the service, no network:

- the URI must end in `@<version>` where version is digits separated by dots (`1`, `1.2.0`); the version is checked
  for syntax only;
- the path has at least two segments (`namespace/name`), each lowercase `a-z 0-9 - _ .`, not empty, not starting with
  a dot;
- an exact file name wins; otherwise exactly one file may match the stem (`title-card` → `title-card.motion.json`);
  two matches are ambiguous; a directory, a symlink leaving the library, or no file is refused;
- the file is hashed, sniffed, probed and counted like a fetched asset (per-asset and per-document caps, billed MB),
  never copied.

A bad `library:` asset `src` is the diagnostic `asset.bad_url` at `/assets/<id>/src` (a `400` with
`error.data.diagnostics`, not an `ok: false` check result); a bad `library:` `doc_url` or `video` is a `400` whose
message starts with `asset.bad_url: <id>: <why>`. Without a library on the box: `500 internal` "the asset library is
not installed on this box".

Documents the library ships today (`library/mitte/assets/demo/`), usable as `doc_url` or `video`:

| URI | What |
|---|---|
| `library:mitte/demo/title-card@1` | the title card (the registry's inline example document, 16:9 with `vertical` and `square` variants) |
| `library:mitte/demo/lower-third@1` | a transparent lower third (alpha renders, interchange exports) |
| `library:mitte/demo/kinetic-quote@1` | kinetic typography, 12 s |
| `library:mitte/demo/data-story@1` | bar chart and counters from `data`, 10 s |
| `library:mitte/demo/classic-3d@1` | cards under a moving camera (the camera-path export example) |
| `library:mitte/demo/glow@1`, `library:mitte/demo/trim-paths@1`, `library:mitte/demo/text-on-path@1`, `library:mitte/demo/reels-presets@1`, `library:mitte/demo/glass-loop@1` | effect and preset demos |
| `library:mitte/demo/showreel@1`, `library:mitte/demo/p3-reel@1`, `library:mitte/demo/p3-reel-2@1`, `library:mitte/demo/p4-reel@1` | the reels (physics, lit 3D, HDR, morphing, transitions) |
| `library:mitte/demo/tracking-clip@1` | `tracking-clip.mp4`, the `motion.track` example clip |
| `library:mitte/demo/logo@1` | `logo.svg`, the SVG import example |
| `library:mitte/demo/badge@1` | `badge.lottie`, the dotLottie import example |

`library:` works wherever a URL is taken: `doc_url`, asset `src`, `motion.convert` `url`, `motion.track` `video` and
`base`. The `mitte/sfx/*` sound pack of spec 12 is not shipped (`asset.bad_url`).

## `data`

A JSON object merged over the document's own `data` (templated documents: one document, many renders). Accepted by
`motion.check`, `motion.frames`, `motion.render` and `motion.convert` (export) with the same meaning; `null` or
absent means no overlay. The engine reads it from `--data data.json`; invalid JSON there is `doc.json` at `/data`.
Templates (`$data.*`, `{{ … }}`) are resolved after the merge, so a key the document lacks still resolves.

## `variant` and `variants`

A variant id names an entry of the document's `variants` map (`"vertical": {"size": [1080, 1920], "override": {…}}`).
`"default"` (or an empty string) is the root comp. `motion.check`, `motion.frames` and `motion.convert` take one
`variant`; `motion.render` takes `variants: [...]` (deduplicated, at most `REXX_MAX_VARIANTS` = 6, each rendered as
its own labelled file) or one `variant`, not both ("use either variants or variant, not both"). An unknown id is the
engine's `ref.variant_unknown`.

## Asset materialization

The engine has no network: the service fetches every declared asset before the engine starts and hands it
`assets.json` (`id → {path, sha256, bytes, content_type, probe, deferred}`).

| Rule | Detail |
|---|---|
| Scheme | `https:` only (`http:` only with the test knob `allow_http`); no credentials in the URL; a literal IP is checked like a resolved one |
| Addresses | every DNS answer is checked against loopback, RFC 1918, link-local and cloud-metadata ranges, CGNAT, multicast and their IPv6 forms; one blocked answer poisons the host; every redirect (at most 3) is re-checked; no proxy |
| Response | status must be 200; the body streams to disk with its SHA-256 computed on the way |
| Caps | `REXX_MAX_ASSET_BYTES` (512 MB) per asset, `REXX_MAX_ASSETS_TOTAL_BYTES` (2 GB) per document, one `materialize` call bounded at 120 s (connect timeout 10 s) |
| Type | the magic bytes win over the `Content-Type` header, which wins over the extension; the result must agree with the declared `type` (`image`, `video`, `audio`, `font` by category; `data`/`track` as JSON, text, octet-stream or `application/vnd.mitte.*`; `sim` as octet-stream; `svg` is an image; `lottie`, `model`, `lut` are not sniffed, the engine validates them); an undeclared type only refuses HTML |
| Pin | `sha256` (64 hex, optional `sha256:` prefix) is verified; a cache lookup by hash skips the fetch |
| Cache | content-addressed under `<REXX_CACHE_ROOT>/assets` (`objects/<sha256>`, `meta/`, `urls/` keyed by the URL without its query), hard-linked into the job's scratch; LRU by atime (janitor) |
| Probe | `ffprobe` for video and audio: container, duration, size, fps, codecs, channels, sample rate, rotation, colour space, alpha; cached beside the object; a failed probe is not an error |

Refusals are `400 bad_request` with the reason first in the message (they are not diagnostics; nothing ran):

| Message prefix | Meaning |
|---|---|
| `asset.bad_id: …` | an asset without an id, or two with one id |
| `asset.bad_url: <id>: …` | not a URL, not https, credentials, a blocked address, a redirect refused, a `library:` URI that resolves to nothing |
| `asset.bad_hash: <id>: …` | `sha256` is not 64 hex characters |
| `asset.hash_mismatch: <id>: …` | the content does not match the pin |
| `asset.type_mismatch: <id> …` | the bytes contradict the declared type; or an HTML page where media was expected |
| `asset.bad_type: <id>: …` | an unknown declared type |
| `asset.empty: <id> …` | a zero-byte body |
| `asset.unreachable: <id>: …` | non-200, timeout or reset ("transient; retry may succeed") |
| `asset.too_large: …` | over the per-asset or per-document cap (`413`) |

What `motion.check` fetches: fonts, `sim` assets (locked bakes), the audio assets a comp's `markers[].from` analyses,
and every `library:` asset (local). Every other https asset is **deferred**: the manifest carries the probe
metadata the cache already has (size, duration) or nothing, and the engine must not read it. `motion.frames`,
`motion.render` and `motion.convert` materialize everything.

`stats.assets[]` of `motion.check` reports each asset's `source` (the `src` as given), `bytes` and `layers` (how
many layers use it), so a caller can verify what was used.

## Output files

Every output is uploaded under `u/<uid>/rexx/<tool>/<request id>/<name>` (`<tool>` without `motion.`): `default.mp4`,
`default-poster.png`, `frame-00.png`, `sheet.png`, `main.json`, `images/<file>`, `<clip>.track.json`,
`<clip>.track-sheet.png`, `canonical.motion.json`, `<hash>.sim`. Content types: `.motion.json` →
`application/vnd.mitte.motion+json`, `.track.json` → `application/vnd.mitte.track+json`, `.camera.json` →
`application/json`, `.lottie` → `application/zip`, `.sim` → `application/octet-stream`; everything else by extension.
