# The library: what it is, how references resolve, how to check a document

The library is the set of **themes**, **presets** and **components** every motion document can use by reference, plus the **assets** shipped next to them (demo documents, a logo, clips) and the **font pack**. It lives in the repository under `library/` and is compiled into the engine image, so resolution is local and offline: nothing is fetched. Engine 0.1.48, library version `2026.10.0`: 10 themes, 9 presets (3 packs), 103 components in 15 groups, 206 example documents. Every entry is version `1.0.0`, phase P1 or P3, and `status: draft` (no designer has signed any entry off yet; the engine resolves drafts regardless).

Sources of truth, in order: the library files (`library/mitte/**/*.library.json`), `library/index.json` (the generated catalogue, rendered as `90-catalogue.md`), the normalizer (`engine/crates/rexx-normalize/src/library.rs`, `passes/library_refs.rs`, `passes/components.rs`, `passes/theme.rs`, `passes/presets.rs`), then spec 12. Where this page says "spec gap", the code and the spec disagree and the code is documented.

## Pages in this area

| Page | Covers |
|---|---|
| `00-overview.md` | this page: references, versions, resolution, assets, the catalogue, diagnostics, checking locally |
| `01-themes.md` | the theme object, every token group and token, derived tokens, modifiers, springs, textures, styles, brand kits, merge rules, the ten themes compared |
| `02-presets.md` | using library presets, the three packs, writing a custom preset, every rule the engine enforces |
| `03-components-using.md` | instances: `use`, `props`, `slots`, versions, what normalization produces, param validation, placement, variants, nesting |
| `04-components-writing.md` | writing a component (local and library): every definition field, param types, structure switches, slots, `x-library` files, examples files, the index script, review and versioning rules |
| `05-captions.md` | the four `caption.*` components in depth: params, defaults per style, the word-timings input, what the engine builds, what it does not build yet |
| `06-credits.md` | the eight `credits.*` components in depth: the `sections` document, shared style params, crawl speed and duration, what the engine builds |
| `07-transitions.md` | transitions as components: slots `a`/`b`, using them in `scenes` and by hand, writing one, the 14 shipped transition components |
| `08-demos-reels.md` | every demo asset (`library:mitte/demo/…`), the three reels scene by scene with the constructs to copy |
| `09-sound-fonts.md` | the sound pack (eight synthesized CC0 clips) and every font family in the pack with license, roles and scripts |
| `10-recipes.md` | the fifteen brief recipes, re-verified against engine 0.1.48 |
| `11-cookbook-1.md`, `12-cookbook-2.md` | twenty complete documents for common briefs, each checked with `rexx-engine check` |
| `90-catalogue.md` | generated index of every entry |
| `91-components-<group>.md` | generated: every component with every param, slot, example and note (15 files) |
| `92-themes.md`, `93-presets.md` | generated: every theme token, every preset with its tweens |
| `examples/` | every example document on these pages; `scripts/skills-library-check.py` checks them all |

## Reference syntax

A library reference is `<namespace>/<name>@<version>`:

| Part | Syntax | Notes |
|---|---|---|
| namespace | `mitte` | The only namespace that ships. `team/<team>/` and `user/` are P4 and do not resolve today. |
| name | `^[a-z][a-z0-9-]*(\.[a-z][a-z0-9-]*)*$` | Lower-case words joined by hyphens inside a segment and dots between segments: `lower-third.bar`, `caption.pop`, `particles.burst-on-beat`, `kinetic.slam`, `clean`. Names are references, not ids: they may contain dots. |
| version | `@1`, `@1.2`, `@1.2.0` | One to three dot-separated integers. Required: `mitte/clean` without `@` is not a library reference. |

The validator checks the shape before anything resolves: `"use": "Mitte/Bad@1"` (an upper-case letter, a missing version, a fourth version segment) is `component.unknown` with the hint "Write `<namespace>/<name>@<version>`, e.g. `mitte/lower-third.bar@2`." and stops the check there (pass 3, before library resolution).

Where references appear:

| Where | Field | Kind |
|---|---|---|
| `theme.use` | `"use": "mitte/clean@1"` | theme |
| a `component` layer | `"use": "mitte/lower-third.bar@1"` | component |
| a timeline entry or a `preset` param | `"preset": "mitte/kinetic.slam@1"` | preset |
| a `scenes` transition | `"type": "mitte/transition.glass-swipe@1"` | component with slots `a` and `b` (`07-transitions.md`) |
| an asset `src`, or a layer's `asset` | `"src": "library:mitte/demo/logo@1"` | library asset (below), not an entry |

## Version resolution

The engine loads every `*.library.json` under its library root once at startup (recursively, 12 directory levels deep; a file that does not parse is skipped silently). Each file's `meta.version` (semver, default `1.0.0` when absent) applies to every entry in it. A reference resolves to the **newest stored version whose leading components equal the requested ones**, among entries of the requested kind:

| Request | Matches | Today |
|---|---|---|
| `@1` | newest `1.x.y` | `1.0.0` for every entry |
| `@1.0` | newest `1.0.y` | `1.0.0` |
| `@1.0.0` | exactly `1.0.0` | `1.0.0`; pin this for byte-reproducible renders |
| `@2`, `@1.1`, `@1.0.1` | nothing | `ref.library_version`, hint "Available versions: 1.0.0." |

Minor and patch updates apply automatically at the next render (a `@1` document picks up a `1.1.0` when it ships). The resolved versions of a checked document are in `motion.check`'s `stats.library` (`{"mitte/midnight": "1.0.0", "mitte/transition.glass-swipe": "1.0.0"}`), so a caller can pin them. Themes used through `theme.use`, components, library presets and library transitions are all recorded; library assets are not (they are not versioned on disk: the `@1` of an asset is the library version it ships in and selects nothing).

Kinds are separate maps: `mitte/clean@1` as a component `use` is `ref.library_unknown` even though the theme exists; `mitte/lower-third.bar@1` as a `preset` is `preset.unknown` (the preset pass reports unknown presets with its own code and a did-you-mean list of built-in and local presets).

## Where the engine finds the library

`rexx-engine` looks for the library directory in this order: `--library <dir>`, `$REXX_LIBRARY`, `/opt/rexx/library` (the image), then `<checkout>/library` when the binary runs inside the repository. The service does the same (`REXX_LIBRARY`, `/opt/rexx/library`, the checkout) and mounts it read-only into the engine's jail. `rexx-engine version` reports the library version it found (`"library": "2026.10.0"`, read from `index.json`). Without a library directory every `mitte/…` reference is `ref.library_unknown`; without `mitte/default@1` the theme pass uses the identical built-in copy of the default theme, so presets still resolve.

## Library assets: `library:` URIs

A `library:` URI names a file shipped under the namespace's `assets/` directory: `library:mitte/<path>@<version>` resolves to `<library>/mitte/assets/<path>.<ext>`. Rules (engine `library.rs::asset_path`):

- Segments are lower-case letters, digits, `-`, `_` and `.`, none starting with a dot; the version is digits and dots and selects nothing.
- The last segment is a file **stem**: `library:mitte/demo/logo@1` finds `logo.svg`. Exactly one file may answer to the stem; a reference that names the full file name (`library:mitte/demo/tracking-clip.mp4@1`) wins over a stem match. Two files sharing a stem make the stem reference ambiguous and it fails.
- The file must be a regular file under the canonical library root (no symlink escapes).
- The service rejects a `library:` URI that resolves to nothing with `asset.bad_url` (a 400), the same code as any non-`https:` source. The **CLI is more lenient**: `rexx-engine check` records the asset with `bytes: 0` and raises nothing (so a misspelt `library:mitte/sfx/hit.sfot@1` passes a local check and fails on the service).
- A layer's `asset` field or a component's `asset` param may carry the URI directly; the normalizer declares it under the id `<layer id>.asset`.

What ships today (`library/mitte/assets/`): `demo/` (`08-demos-reels.md` lists every file) and `sfx/`, the eight clips of the `mitte/sfx.*` sound pack (`09-sound-fonts.md`). There are no device-bezel, icon or texture assets: components draw their device frames with shapes, and spec 12 no longer names bezel assets.

Demo documents are also loadable by the service as `doc_url: "library:mitte/demo/title-card@1"` (a `library:` URI of a `.motion.json` is accepted wherever `doc_url` is).

## The catalogue: `index.json`

`library/index.json` is generated by `scripts/build-library-index.py` from the library files and is what `90-catalogue.md` renders. Top level: `library` (`mitte`), `version` (`2026.10.0`), `generated`, `spec`, `thumbnails` (`{ "base": "thumbnails", "note": … }`: placeholders, no thumbnail has been rendered), `counts`, `entries[]`.

| Entry field | Present on | Meaning |
|---|---|---|
| `ref`, `kind`, `name`, `version`, `phase`, `status`, `description`, `tags`, `file`, `thumbnail` | all | `ref` is `mitte/<name>@<major>`; `kind` is `theme`, `preset` or `component`; `file` the library file; `thumbnail` a placeholder path |
| `params[]` | presets, components | `{ name, type, default?, required?, description, values?, min?, max?, maxChars?, kind?, accepts?, minItems?, maxItems?, fields?, item? }`; `fields` and `item` nest the same shape |
| `size`, `duration`, `slots[]` (names only), `engineBacked`, `examples[]` (`{ id, title, thumbnail }`) | components | |
| `dur`, `ease` | presets | the preset's own duration and ease (often `$theme.…`) |
| `tokens[]` | themes | the token group names present |

`90-catalogue.md` is the same data as Markdown. A `description` is the text the assistant is meant to choose by; every param has one.

What ships (library 2026.10.0), by group; every name is `mitte/<name>@1`, its params are on the group's `91-components-<group>.md` page and the concept pages named:

| Group | Components | Page |
|---|---|---|
| backgrounds (3) | `bg.aurora`, `bg.gradient-mesh`, `bg.grid` | [91-components-backgrounds.md](91-components-backgrounds.md) |
| captions (4, engine-backed) | `caption.highlight`, `caption.karaoke`, `caption.minimal`, `caption.pop` | [05-captions.md](05-captions.md) |
| credits (8, engine-backed) | `credits.cards`, `credits.cast-card`, `credits.crawl`, `credits.grid`, `credits.legal`, `credits.logos`, `credits.pairs`, `credits.song` | [06-credits.md](06-credits.md) |
| data (11) | `chart.bar`, `chart.compare`, `chart.donut`, `chart.line`, `chart.share`, `progress.bar`, `progress.ring`, `stat.counter`, `stat.row`, `timeline.dates`, `timeline.steps` | [91-components-data.md](91-components-data.md) |
| explainers (1) | `explainer.step` | [91-components-explainers.md](91-components-explainers.md) |
| logo (6) | `logo.reveal.draw`, `logo.reveal.glass`, `logo.reveal.glitch`, `logo.reveal.mask`, `logo.reveal.shine`, `logo.sting` | [91-components-logo.md](91-components-logo.md) |
| lower-thirds (6) | `lower-third.bar`, `lower-third.minimal`, `lower-third.news`, `lower-third.pill`, `lower-third.split`, `lower-third.stacked` | [91-components-lower-thirds.md](91-components-lower-thirds.md) |
| maps, callouts, layouts (5) | `callout.arrow`, `callout.line`, `map.pin`, `map.route`, `split.screen` | [91-components-maps.md](91-components-maps.md) |
| music (1) | `lyrics` | [91-components-music.md](91-components-music.md) |
| overlays (2) | `film-burn`, `light-leak` | [91-components-overlays.md](91-components-overlays.md) |
| particles (16) | `particles.assemble`, `particles.bokeh`, `particles.burst-on-beat`, `particles.confetti`, `particles.disintegrate`, `particles.dust`, `particles.embers`, `particles.fireworks`, `particles.form-logo`, `particles.magic-trail`, `particles.plexus`, `particles.rain`, `particles.smoke`, `particles.snow`, `particles.sparks`, `particles.starfield` | [91-components-particles.md](91-components-particles.md) |
| social (8) | `countdown`, `cta.endcard`, `cta.subscribe`, `social.comment`, `social.frame`, `social.poll`, `social.story`, `testimonial.card` | [91-components-social.md](91-components-social.md) |
| titles (9) | `kinetic.words`, `quote.card`, `title.card`, `title.chapter`, `title.highlight`, `title.kinetic`, `title.reveal`, `title.stack`, `title.typewriter` | [91-components-titles.md](91-components-titles.md) |
| transitions (13) | `transition.glass-lens`, `transition.glass-swipe`, `transition.glitch`, `transition.iris`, `transition.light-leak`, `transition.mask-wipe`, `transition.push`, `transition.shape-wipe`, `transition.shape`, `transition.stripes`, `transition.whip`, `transition.wipe`, `transition.zoom` | [07-transitions.md](07-transitions.md) |
| ui (10) | `browser.window`, `device.laptop`, `device.phone`, `screen.demo`, `ui.card-stack`, `ui.chat`, `ui.cursor`, `ui.notification`, `ui.search`, `ui.toast` | [91-components-ui.md](91-components-ui.md) |

Themes (10): `bold`, `clean`, `corporate`, `default`, `editorial`, `midnight`, `mono`, `neon`, `retro`, `soft` ([01-themes.md](01-themes.md)). Presets (9, three packs): `editorial.rise`, `editorial.fade`, `kinetic.slam`, `kinetic.stomp`, `kinetic.flip`, `kinetic.stretch`, `ui.pop`, `ui.slide`, `ui.fade` ([02-presets.md](02-presets.md)).

## Diagnostics that come from library use

| Code | Severity | When | Message shape and hint |
|---|---|---|---|
| `component.unknown` | error | `use` is not a valid library reference, or names no local component | `"X" is not a valid library reference.` / `"x" is not a component of this document.` with a did-you-mean |
| `ref.library_unknown` | error | the name resolves to no entry of that kind | `"mitte/nope.thing@1" names no library entry (mitte/nope.thing).` hint: check the catalogue |
| `ref.library_version` | error | the entry exists, the version does not | `The library entry "mitte/lower-third.bar" exists but not at version "2".` hint: `Available versions: 1.0.0.` |
| `preset.unknown` | error | a `mitte/…` preset that does not resolve | `Unknown preset "…".` with a did-you-mean over built-in and local presets |
| `asset.bad_url` | error (service) | a `library:` URI that names no file, two files, or leaves the library | the CLI does not raise it |
| `component.*` | error | instance problems: `03-components-using.md` | |
| `theme.invalid`, `ref.unresolved` | error | theme problems: `01-themes.md` | |

## Checking a document locally

```
rexx-engine check --doc <file.motion.json> --library <repo>/library [--canonical] [--assets <manifest.json>] [--data <overlay.json>] [--variant <id>] [--lint-platform <p>] [--lint-disable <code>]…
```

Output is one JSON event per line: `diagnostic` events (`severity`, `code`, `message`, `hint`, `path`) and one `result` event whose `data` holds `ok`, `doc_hash`, `stats` (with `stats.library`), `estimate`, `timing` (the timing sheet) and, with `--canonical`, the normalized document (`data.canonical`). Exit 0 with no errors; 2 on validation errors. Assets at `https:` URLs are not fetched: image and video layers get `asset.unmaterialized` (info, placement falls back to the box or comp size) and a `data` asset referenced as `$data.@id` is `ref.unresolved` (error), so a local check of a captions document needs inline words or an `--assets` manifest (`{ "<id>": { "path": "<local file>" } }`). Fonts come from `--fonts`, `$REXX_FONTS`, `/opt/rexx/fonts` or `<checkout>/fonts/files`.

`scripts/skills-library-check.py` runs this on every document under `SKILLS/library/examples/` (`REXX_ENGINE_BIN=<binary> python3 scripts/skills-library-check.py`).

A complete document that uses every kind of reference (`examples/concepts/00-library-refs.motion.json`; checks clean apart from one declared lint false positive on `lower-third.bar`):

```json
{
  "motion": 1,
  "theme": { "use": "mitte/midnight@1", "override": { "color": { "accent": "#FF4D00" } } },
  "assets": { "logo": { "src": "library:mitte/demo/logo@1", "type": "svg" } },
  "comps": {
    "main": {
      "size": [1920, 1080], "fps": 30, "duration": 7, "background": "$theme.color.bg",
      "layers": [
        { "id": "mark", "type": "shape", "fromSvg": "logo", "fit": { "width": 360 }, "origin": "center", "position": ["50%", "38%"] },
        { "id": "word", "type": "text", "text": "Motion",
          "style": { "font": "$theme.font.display", "size": "$theme.type.size.5", "fill": "$theme.color.fg" },
          "origin": "top", "align": { "to": "mark", "y": "below", "gap": "$theme.space.4", "x": "center" } },
        { "id": "lt", "type": "component", "use": "mitte/lower-third.bar@1", "in": 2.5,
          "props": { "name": "Ada Lovelace", "role": "Analyst, Engine Co.", "hold": 2 },
          "align": { "to": "safe", "x": "left", "y": "bottom" } }
      ],
      "timeline": [
        { "target": "mark", "preset": "popIn", "at": 0.2 },
        { "target": "word", "preset": "mitte/kinetic.slam@1", "props": { "from": 180 }, "at": 0.5 },
        { "target": ["mark", "word"], "preset": "fadeOut", "dur": 0.4, "at": 6.4 }
      ]
    }
  }
}
```

## Spec gaps found on this page

> **Spec gap:** the CLI does not report a `library:` asset that resolves to nothing; the service does (`asset.bad_url`).

