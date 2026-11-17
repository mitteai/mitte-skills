# 01. The document: top level, ids, references, assets, time, variants, values, limits

Scope: spec 1 (document), the parts of spec 10 §10.1 that live on the asset object, spec 12 §12.2.2 (data size). Every field of the top-level object, of a comp, of an asset, of a marker, of a variant; every time form; every value type; every limit. Generated field tables: `90-schema-reference.md` (root object), `92-schema-types-*.md` (`Comp`, `Asset`, `Marker`, `MarkerFrom`, `Variant`, `Override`, `LintConfig`).

## 1. What a document is

One JSON object, `"motion": 1`, describing compositions, layers, animation, assets and default output. Data, not code: the only executable text is an `expr` string ([12-expressions.md](12-expressions.md)), run in a sandbox with no I/O and a step budget. Same canonical document + same assets + same engine version = identical pixels and bytes.

**Two forms, one schema.**

| Form | Written by | May contain |
|---|---|---|
| Authored | you | everything canonical plus sugar: `timeline` tweens, presets, components, `repeat`, `$theme`/`$data`/`$props` references, `{{ }}` templates, percentages, `origin`/`align`, relative values (`"+=40"`), named eases, shape presets, `scenes`, `crawl`, `words`, camera sugar |
| Canonical | the normalizer | comps, layers, explicit keyframes, catalog ease names, expressions, effects; every value resolved; colours as linear `{r,g,b,a}` objects; plus `sims` (physics bakes) |

Canonical form is a subset of authored form (normalizing it is the identity). `motion.check` with `canonical: true` returns it. An authored document that contains canonical-only constructs (`sims`, `{ "sim", "body" }`, the `_physics` animator) is `doc.canonical_only`.

## 2. Top level

```jsonc
{
  "motion": 1,                              // required, integer; newer major: doc.version_unsupported; missing: doc.version_missing
  "meta": { "title": "Q4 teaser", "notes": "free text" },   // never affects rendering; passed through
  "theme": { "use": "mitte/clean@1" },      // 13-components-themes-data.md
  "data": { "sales": [12, 19, 33] },        // any JSON ≤ 512 KB
  "assets": { "logo": { "src": "https://media.mitte.ai/u/abc/logo.svg" } },
  "components": { "card": { … } },          // local component definitions
  "presets": { "riseBlur": { … } },         // local motion presets
  "comps": { "main": { … } },               // required, ≥ 1
  "main": "main",                           // the comp that renders
  "variants": { "vertical": { "size": [1080, 1920] } },
  "output": { "format": "mp4" },            // defaults; tool input overrides field by field
  "lint": { "platform": "tiktok", "disable": [], "readingSpeed": 3, "contrast": 3 }
}
```

| Field | Type | Required | Default | Notes |
|---|---|---|---|---|
| `motion` | integer | yes | — | `1`. |
| `meta` | object of strings | no | `{}` | Free-form; exported as comments. `meta.canonical: true` marks a canonical document. |
| `theme` | object | no | `mitte/default@1` applies | A theme is **always** in effect. [13-components-themes-data.md](13-components-themes-data.md) §1. |
| `data` | any JSON | no | `null` | `limit.data_size` above 512 KB; larger data is a `data` asset read as `$data.@<assetId>`. |
| `assets` | map id → asset | no | `{}` | §6 below. ≤ 512 assets, ≤ 4 GB (service: 512 MB per asset, 2 GB total). |
| `components` | map id → component | no | `{}` | [13-components-themes-data.md](13-components-themes-data.md) §3. |
| `presets` | map id → preset | no | `{}` | [04-presets-and-drivers.md](04-presets-and-drivers.md) §2. |
| `comps` | map id → comp | yes | — | ≤ 256 (`limit.comps`). Empty map: `doc.no_comps`. |
| `main` | comp id | no | `"main"` if it exists, else the only comp | Otherwise `doc.main_ambiguous`. |
| `variants` | map id → variant | no | `{}` | §9. |
| `output` | object | no | engine defaults | [14-color-and-output.md](14-color-and-output.md) §5. |
| `lint` | object | no | `{}` | `platform` (`none`, `broadcast`, `youtube`, `reels`, `tiktok`, `shorts`, `story`, `square`, `linkedin`, `x`), `disable` (lint codes), `readingSpeed` (words/s, 3), `contrast` (ratio, 3). Never affects rendering. |
| `sims` | map hash → bake | canonical only | — | Written by the normalizer (physics). |
| `x-*` | any | no | — | Passed through untouched, in any object. |

**Unknown fields are errors everywhere** (`doc.unknown_field`; the hint lists valid names, nearest first), except inside `meta` and keys starting with `x-`. A misspelt key is never silently ignored.

**Stability.** Everything that gives a `motion: 1` document its meaning is frozen: field defaults, the ease catalog, the built-in presets, normalization rules. New behaviour arrives as opt-in fields; library entries are versioned (`mitte/<name>@<major>`).

## 3. Identifiers

- Syntax `^[A-Za-z][A-Za-z0-9_-]{0,63}$`, case-sensitive. No dots, no slashes (path separators), no leading `_` (`doc.reserved_id`; reserved for engine-generated ids: `_blur`, `_tw3`, `_effect1`, `_mask1`, `_physics`, `_texture`, `_camrig`, `_whip`, `_glitch`). Invalid: `doc.id_invalid`; duplicate among siblings: `doc.id_duplicate`.
- Scope: unique among siblings of one kind (layer ids per comp, shape items per group, effects per layer, masks per layer, animators per layer, comps, assets, components, presets, variants, markers by name).
- Generated ids use dots and are stable: `bars.3`, `bars.jan`, `lt1.comp`, `scene.0`, `burst.lottie`, `logo.contents.leaf`. Authors cannot write dots, so they never collide.
- `id` is required on layers; optional on masks, effects, shape items, animators, keys, tweens (unnamed items get `_effect1`, `_mask1`, … by position: stable only until the list is reordered). Name what you will edit later.
- `name` is optional display text (After Effects layer name on export), defaults to the id.
- Library entry names (`lower-third.bar`, `mitte/kinetic.slam@1`) are references, not ids: dots are part of the name.

## 4. Compositions

```jsonc
"comps": { "main": {
  "size": [1920, 1080],       // required; integers 1..16384 per side
  "fps": 30,                  // required; number 1–240 or "24000/1001" | "30000/1001" | "60000/1001"
  "duration": 8,              // required unless `scenes`; > 0; "auto" only with scenes
  "background": "#0B0B0F",    // colour; default "#00000000"; ignored when rendering with alpha
  "pixelAspect": 1,           // display aspect; rendering is always square-pixel
  "start": 0,                 // timecode offset shown in exports only
  "color": { "working": "linear-srgb", "blending": "linear", "interpolation": "oklab" },
  "motionBlur": { "shutterAngle": 180, "shutterPhase": -90, "samples": 16, "adaptiveLimit": 128, "enabled": true },
  "markers": [ { "t": 2.13, "name": "beat1" } ],
  "safe": "reels",            // or { "action": 0.05, "title": 0.10 } (05-layers.md §6)
  "globalLight": { "angle": 120, "altitude": 30 },   // shared by layer styles; animatable
  "renderer3d": "classic",    // the only renderable value ("advanced" → 3d.advanced_not_built)
  "physics": { … },           // 2D physics world (spec 19; not in this area)
  "scenes": [ … ],            // authored: scene sequence (06-transitions-and-scenes.md)
  "timeline": [ … ],          // authored: tweens (03-timeline-and-tweens.md)
  "layers": [ … ]             // required; may be empty; paint order first = bottom
} }
```

| Field | Type | Default | Notes |
|---|---|---|---|
| `size` | `[w, h]` | — | Output comp ≤ 7680 × 4320 engine / 3840 × 2160 service (`limit.frame_size`); nested comps ≤ 16,384 px per side and 64 MP. |
| `fps` | number or rational string | — | `23.976`, `29.97`, `59.94` are read as the exact rationals. Service cap 1–60 (`limit.fps`). Frame *n* starts at `n / fps`. |
| `duration` | time or `"auto"` | — | Nothing outside `[0, duration)` renders; layers may extend past it. `"auto"` = the end of the scene sequence. Service cap 600 s per variant (`limit.duration`), admitted by estimated render time. |
| `background` | colour | transparent black | Painted under all layers; exported as the comp background (a solid for Lottie). |
| `pixelAspect` | number > 0 | `1` | Interchange only; non-1 stretches at output. |
| `start` | time | `0` | Display offset. |
| `color` | object | | `working`: `linear-srgb` \| `acescg`; `blending`: `linear` \| `display`; `interpolation`: `oklab` \| `srgb`. Nested comps inherit unless they set their own. [14-color-and-output.md](14-color-and-output.md) §2. |
| `motionBlur` | object | see values | `shutterAngle` 0–720 (hold keys only), `shutterPhase` −360–360 (hold keys only), `samples` 2–256 (minimum per frame), `adaptiveLimit` ≥ samples (maximum), `enabled` comp switch. Layers opt in with `motionBlur: true`. [02-keys-and-eases.md](02-keys-and-eases.md) §11. |
| `markers` | list | `[]` | §8. |
| `safe` | number, edges object, preset, or `{ preset, action, title }` | `{ action: 0.05, title: 0.10 }` | [05-layers.md](05-layers.md) §6. |
| `globalLight` | `{ angle, altitude }` | `{ 120, 30 }` | Both animatable. |
| `renderer3d` | `classic` \| `advanced` | `classic` | [10-3d.md](10-3d.md). |
| `timeline`, `scenes` | list | `[]`, none | Authored only. |
| `layers` | list | — | ≤ 2,000 after normalization (`limit.layers`); nesting depth ≤ 16 (`limit.nesting`). |

**Paint order.** Layers paint in array order: the **first is at the bottom**, each later layer over the ones before (SVG/HTML order; After Effects lists the reverse, and the exporters reverse). Exception: within a run of adjacent 3D layers, depth decides ([10-3d.md](10-3d.md) §7). Shape `contents` are the other exception: first item on top ([07-shapes.md](07-shapes.md) §2).

## 5. Paths and references

**Property paths** (tween targets, `follow.path`, expressions' spec names): ids and property names joined by `.`:

```
title.transform.position        title.position (transform segment optional)
title.position.y                one dimension (separate dimensions, 02 §12)
logo.contents.ring.trim.end     a shape item's property
title.effects.glow.radius       an effect parameter; effects.glass.specular.angle for object-valued params
title.text.animators.rise.offset
bars.*.transform.scale          every layer of a repeat (tween targets only)
```

The first segment is a layer of the **current comp**; comps are never part of a path (expressions reach other comps with `comp("id")`).

**`$` references** (authored only; a whole string; resolved once at normalization, never live):

| Reference | Resolves to | Scope |
|---|---|---|
| `$theme.<path>` | a theme token: `$theme.color.accent`, `$theme.ease.enter`, `$theme.font.display`, `$theme.type.size.5`, `$theme.space.4`, `$theme.radius.m`, `$theme.motion.dur.base`, `$theme.motion.stagger.base`, `$theme.spring.snappy`, `$theme.styles.card`, `$theme.color.palette.$index` | anywhere |
| `$data.<path>` | a value from `data`: `$data.sales.2`, `$data.rows.0.label`, `$data.rows[$index - 1]`, `$data.@transcript.words` (a `data` asset) | anywhere |
| `$props.<name>` | a component parameter | inside a component definition |
| `$item`, `$item.<path>`, `$index`, `$count` | the current repeat element, its 0-based index, the count | inside a repeat template |
| `$parent.item`, `$parent.index` | the enclosing repeat's element and index | nested repeat templates |
| `$target` | the layer a preset is applied to (`"$target/chars"`, `"$target.effects.glow"`) | inside a preset definition |
| `$slots.<name>` | forward the outer component's slot | nested instances inside a definition |
| `$comp.width`, `$comp.height`, `$comp.aspect` | the size of the comp the value resolves against (inside a component, the instance's parent comp or variant) and width / height | anywhere; `{{round($props.n / $comp.aspect)}}` |
| `<colour ref>.a10` … `.a90`, `.lighter`, `.darker`, `.on` | modifiers on any colour-typed reference: alpha 10–90 %, ±12 % OKLab lightness, black or white whichever contrasts more (`$theme.color.accent.a20`, `$props.accent.on`, `$item.color.darker`, `$data.brand.primary.a50`) | anywhere |

Rules: a string is a reference only when it is `$` followed by a letter and the whole string is the reference. `$400`, `$`, `$ off` are literal. A literal that starts with `$`+letter is written doubled: `"$$5 off"`. Unresolved: `ref.unresolved` (with the JSON pointer). To build text from pieces use templates: `"Q{{$data.quarter}} revenue"` ([13-components-themes-data.md](13-components-themes-data.md) §2). List indexes past the end and reads through `null` yield `null` (use `| default:`), a missing root is still `ref.unresolved`.

## 6. Assets

```jsonc
"assets": {
  "logo":    { "src": "https://media.mitte.ai/u/abc/logo.svg" },                         // type detected
  "hero":    { "src": "https://media.mitte.ai/u/abc/hero.mp4", "type": "video", "sha256": "…" },
  "music":   { "src": "https://media.mitte.ai/u/abc/track.mp3" },
  "display": { "src": "https://media.mitte.ai/u/abc/Acme-Variable.ttf", "type": "font", "fontFamily": "Acme Sans" },
  "grade":   { "src": "https://media.mitte.ai/u/abc/teal-orange.cube", "type": "lut" },
  "burst":   { "src": "https://media.mitte.ai/u/abc/confetti.lottie", "type": "lottie" },
  "boom":    { "src": "https://media.mitte.ai/u/abc/explosion.zip", "type": "video", "sequence": { "pattern": "boom_%04d.png", "start": 1, "fps": 24 } },
  "words":   { "src": "https://media.mitte.ai/u/abc/vo.words.json", "type": "data" },
  "mark":    { "src": "library:mitte/demo/logo@1" }                                       // shipped with the engine, no network
}
```

| Field | Type | Default | Notes |
|---|---|---|---|
| `src` | URL | required | `https:` (the service fetches before the render: public addresses, ≤ 3 redirects, 512 MB per asset, 120 s) or `library:<namespace>/<path>@<version>` (resolved from the engine image's library directory; the extension is dropped, naming it wins over a stem match; the version is checked for syntax only). Anything else is `asset.bad_url` (`golden:` is for the test corpus). A layer's `asset` or a component's `asset` param may carry a `library:` URI directly; the normalizer declares it under `<layer id>.asset`. Platform assets: write the media URL (mitte's tool layer substitutes `@url_<id>`). |
| `type` | enum | detected from content type and magic bytes | `image`, `video`, `audio`, `font`, `svg`, `lottie`, `model` (interchange only), `lut`, `data`, `track` (a `*.track.json` from `motion.track`), `sim` (a locked physics bake). A declared type that does not match the file is `asset.type_mismatch`. |
| `sha256` | hex string | none | Pins the content; a mismatch is `asset.hash_mismatch`. Makes a render reproducible if the URL changes. |
| `colorSpace` | enum | from file metadata, else `srgb` | `srgb`, `display-p3`, `rec709`, `rec2020`, `rec2020-pq`, `rec2020-hlg`, `linear-srgb`, `acescg`. Images, video, sequences. |
| `range` | `full` \| `limited` | from tags (limited for Y'CbCr, full for RGB codecs and MJPEG) | Video signal range. |
| `alpha` | enum | from file (`straight` PNG/WebP/AVIF/TIFF, `premultiplied` EXR/ProRes 4444) | `straight`, `premultiplied`, `ignore` (opaque), `stacked-bottom`, `stacked-right` (colour in one half, alpha as luma in the other; the layer's size is the colour half). |
| `fps` | rate | from the file | Conform video / sequence / animated image to a rate (source frame *n* shows at `n / fps`; its audio is muted). |
| `orient` | `auto` \| `ignore` | `auto` | EXIF orientation (images), display-matrix rotation (phone video). |
| `pixelAspect` | number > 0 | from the file (SAR), else 1 | Non-square sources are resampled to square pixels at decode. |
| `field` | `progressive` \| `upper` \| `lower` | from the file | Interlaced sources are deinterlaced (`bwdif`). |
| `loop` | integer ≥ 1 | `1` | Interpret-footage loop count: the source becomes *n* times longer (a layer's default `out` uses `duration × loop`). Distinct from the layer's boolean `loop`. |
| `sequence` | `{ pattern, start, fps }` | none | Image sequence in a zip: `pattern` printf-style with one integer field (`frame_%04d.png`), `start` (default: the lowest number; gaps hold the previous frame, `media.sequence_gap`), `fps` (30). ≤ 20,000 frames (`limit.sequence_frames`). `start` and `fps` are plain numbers, never frame forms (`doc.time_needs_comp`). |
| `audioTrack`, `videoTrack` | integer ≥ 0 | `0` | Stream selection in multi-stream files. |
| `fontFamily` | string | from the font | Fonts: the family name text layers use. Several assets with one `fontFamily` form one family (one per static weight). |
| `index` | integer | `0` | Fonts: the face inside a TTC/OTC collection. |

Fonts in the engine's pack need no asset ([08-text.md](08-text.md) §4); declare a font asset for a brand font (TTF, OTF, WOFF, WOFF2; malformed is `asset.invalid_font`). An asset the engine cannot read is `asset.unreadable`; one that was not fetched before a `check` is `asset.unmaterialized` (info: the layer shows nothing, sizes come from a probe where possible). Media interpretation details and formats: [11-media-and-audio.md](11-media-and-audio.md) §1.

## 7. Time

### 7.1 Time values

Every time field (key `t`, `in`, `out`, `dur`, `offset`, marker `t`, `range`, stagger `each`, …) accepts:

| Form | Example | Meaning |
|---|---|---|
| number | `1.5` | seconds; parsed as decimal text, so `0.1`, `"0.1s"` and `"100ms"` are the same tick |
| `"<n>s"` | `"1.5s"` | seconds |
| `"<n>ms"` | `"250ms"` | milliseconds |
| `"<n>f"` | `"12f"` | frames at the comp's rate |
| timecode | `"00:00:01:12"`, drop-frame `"00:01:00;02"` | hours:minutes:seconds:frames at the comp's rate |
| marker | `"@beat3"` | the marker's time in the same comp |
| marker ± offset | `"@beat3+0.25"`, `"@intro-2f"` | marker time plus or minus a time |

Frame-based forms (`f`, timecode, marker offsets in frames) need a frame rate and are valid only **inside a comp** (layers, keys, markers, timeline). In `output.range`, an asset's `sequence`, and `markers[].from` parameters they are `doc.time_needs_comp`. In a variant that overrides `fps` they re-resolve against the variant's rate. Tween `at` positions accept more forms ([03-timeline-and-tweens.md](03-timeline-and-tweens.md) §2).

### 7.2 Internal time

Time is an integer count of ticks, 254,016,000,000 per second (divides exactly by every common rate incl. 24000/1001, 30000/1001, 60000/1001, and by 48 kHz and 44.1 kHz). Seconds round to the nearest tick, so frame boundaries never drift. Animation is evaluated at **continuous time**: any tick may be sampled (motion blur, frame blending, time remapping, `output.fps` all depend on it).

### 7.3 Markers

```jsonc
"markers": [
  { "t": 0.0,  "name": "intro" },
  { "t": 2.13, "name": "beat1", "dur": 0.1 },
  { "from": { "audio": "music", "detect": "beats", "prefix": "beat", "tempo": 120, "meter": 4, "min": 0.1, "fallback": "none" } }
]
```

| Field | Type | Default | Notes |
|---|---|---|---|
| `t` | time | required | A named time. |
| `name` | id | required | Marker names follow the id syntax; unique per comp. |
| `dur` | time | `0` | Informs exporters and lint only. |
| `from.audio` | asset id | required in `from` | An `audio` or `video` asset to analyse. |
| `from.detect` | `beats` \| `onsets` \| `downbeats` | required | Tempo-tracked beats; transients; bar starts (with `meter`). |
| `from.prefix` | string | required | Generated markers are `<prefix>1`, `<prefix>2`, … in time order. |
| `from.tempo` | BPM | estimated | Replaces the estimate (fixes half/double-tempo errors). |
| `from.meter` | integer | `4` | Beats per bar for `downbeats`. |
| `from.min` | 0–1 | none | Drop onsets weaker than this strength. |
| `from.fallback` | `none` \| `grid` | `none` | When nothing is detected: no markers (info `lint.beats_none`) or a metronome grid at `tempo` (or 120 BPM) from the first onset (info `lint.beats_grid`). |

A marker's own `t` takes every time form, including another marker (`{ "t": "@intro+0.5", "name": "title" }`, in any order in the list); a marker whose `t` names an unknown marker or a cycle (`a` at `@b`, `b` at `@a`) is `ref.marker` at that `t`. Detected markers are plain markers in the canonical document, clipped to the comp's duration (`"@beat40"` past the end is `tween.unknown_marker`). Where a list of marker times is accepted (particle bursts, physics impulses), `"@beat*"` means every marker whose name starts with `beat` (the `*` only at the end). Beat detection is reliable on produced, percussive music and unreliable on speech, ambient and classical audio (`lint.beats_unstable`); for voice-over use labels or word timings. Detection details: [11-media-and-audio.md](11-media-and-audio.md) §8.

## 8. Variants

One piece of motion in several aspect ratios: a variant is the root comp at another size with overrides.

```jsonc
"variants": {
  "vertical": {
    "size": [1080, 1920], "fps": 30, "duration": 15,
    "safe": "tiktok", "lint": { "platform": "tiktok" },
    "override": {
      "title":    { "style": { "size": 140 } },                // partial layer object, deep-merged
      "subtitle": { "align": { "y": "bottom", "margin": 320 } },
      "sidebar":  { "enabled": false },                        // removes the layer in this variant
      "captions": { "props": { "lines": 1 } },                 // component instances change through props
      "timeline": { "intro": { "dur": 0.4 } }                  // timeline entries by their id
    }
  },
  "square": { "size": [1080, 1080], "safe": "square" }
}
```

| Field | Notes |
|---|---|
| `size` | required; same rules as a comp's `size` |
| `fps`, `duration` | optional overrides of the root comp's |
| `safe` | this variant's safe areas (a preset name or margins, as the comp field); `align: { "to": "safe" }` and the safe-area lint use it |
| `lint` | overrides the document's lint configuration (usually `platform`) |
| `override` | map of root-comp layer id → partial layer object, deep-merged before normalization. Arrays are replaced, not merged. `enabled: false` removes a layer. Only existing root-comp layers (`ref.variant_layer` otherwise); component instances via `props`; timeline entries by `id` under `override.timeline`. New layers or entries cannot be added (put them in the root with `enabled: false` and enable per variant). |

Percentages, `align`, `origin`, `$theme.type.size.<n>` and `$theme.space.<n>` re-resolve against the variant's size, so a document placed relatively often needs no overrides. An unknown variant name in a tool call is `ref.variant_unknown`. The tools render one variant per call (`variant`) or several in one job (`variants: [...]`, ≤ 6), sharing normalization.

## 9. Values and units

| Type | Written as | Notes |
|---|---|---|
| number | JSON number | finite (`doc.type` otherwise) |
| vector | `[x, y]` or `[x, y, z]` | a 2D value on a 3D property gets `z = 0` |
| percent | `"50%"` | authored only: comp size for positions, content bounds for anchors ([05-layers.md](05-layers.md) §5) |
| angle | number | degrees, positive = clockwise on screen (y points down) |
| colour | string or object | [14-color-and-output.md](14-color-and-output.md) §1 |
| gradient | object | [07-shapes.md](07-shapes.md) §6 |
| path | object or SVG path string | [07-shapes.md](07-shapes.md) §4 |
| text | string or spans | [08-text.md](08-text.md) §1 |
| enum | string | listed per property; animatable with hold keys only where stated |
| boolean | JSON boolean | not animatable unless stated (then hold only) |
| time | §7.1 | |

**After Effects units** (so documents convert without arithmetic):

| Property | Unit | Range | Default |
|---|---|---|---|
| `opacity` | percent | 0–100 | 100 |
| `scale` | percent per axis | any (negative mirrors) | `[100, 100]` (`[100, 100, 100]` in 3D) |
| `rotation` | degrees | any (720 = two turns) | 0 |
| `position`, `anchor` | pixels in the parent's / layer's space | any | per layer type |
| `trim.start`, `trim.end` | percent of path length | 0–100 | 0, 100 |
| `trim.offset` | degrees (360 = one full path length) | any | 0 |
| text `tracking` | thousandths of an em | any | 0 |
| audio `volume` | decibels | any (`-inf` or ≤ −96 mutes) | 0 |

`opacity: 0.6` is almost invisible; lint reports it (`lint.opacity_fraction`, with a `fix`).

## 10. Animatable values

Every property marked *animatable* accepts four shapes:

```jsonc
"opacity": 100                                                              // 1. static
"opacity": { "keys": [ { "t": 0, "v": 0, "ease": "expo.out" }, { "t": 0.6, "v": 100 } ] }   // 2. keyframes
"rotation": { "value": 0, "wiggle": { "freq": 2, "amp": 4 } }               // 3. base + drivers
"position": { "value": [960, 540], "expr": "value + [0, Math.sin(time * 6) * 20]" }   // 4. + expression
```

They combine: `{ "keys": [...], "loop": "cycle", "wiggle": {...}, "expr": "..." }`. A value object holds exactly one base source: `value`, `keys` (or the authored list binding `keys: { from, t, v }`), `track` (authored, tracking), or `sim` (canonical, physics; with `body`, and `pre` holding the property's keys before the body's `start`, the keyframe-to-physics hand-off); two is `anim.value_and_keys`. Keys or drivers on a non-animatable property: `anim.not_animatable`; a value of the wrong type: `anim.value_type`.

Evaluation order, fixed:

0. **Time remap**: `loop` / `loopIn` map *t* into the keyed span outside it.
1. **Base**: the static value, the keyframe interpolation at the remapped time, or the bake sample.
2. **Drivers**, in this order: `follow`, `spring`, `wiggle`, `noise`, `oscillate`, `audio` (`spring` replaces the value; the others add).
3. **Expression**: `expr` runs with `value` bound to the result of 1–2 and returns the final value.
4. **Clamp** to the property's range (opacity 0–100, trim 0–100, stroke width ≥ 0, …). Properties without a listed range are not clamped (`scale` may be negative). Clamping is silent at render; lint reports key values outside the range.

Keys, eases, loops: [02-keys-and-eases.md](02-keys-and-eases.md). Drivers: [04-presets-and-drivers.md](04-presets-and-drivers.md) §3. Expressions: [12-expressions.md](12-expressions.md). The complete list of animatable paths: [91-animatable-paths.md](91-animatable-paths.md).

## 11. Limits

Engine ceilings; the service may cap lower, and `motion.check` validates against the service's current caps, so a document that passes check never fails a render on a limit. Count limits are checked before expansion from declared counts.

| Limit | Engine | Service | Code |
|---|---|---|---|
| Authored document size | 2 MB | 2 MB (inline `doc` 1 MiB; use `doc_url` above) | `limit.doc_size` |
| Canonical size | 32 MB | same | `limit.canonical_size` |
| `data` | 512 KB | same | `limit.data_size` |
| Comps | 256 | same | `limit.comps` |
| Layers per comp (after normalization) | 2,000 | same | `limit.layers` |
| Comp nesting depth | 16 | same | `limit.nesting` |
| Keys per property / total | 10,000 / 1,000,000 | same | `limit.keys`, `limit.keys_total` |
| `repeat` count | 1,000 per repeat, 10,000 per document | same | `limit.repeat` |
| Output frame | 7680 × 4320 | 3840 × 2160 | `limit.frame_size` |
| Rendered duration | 30 min | 600 s per variant | `limit.duration` |
| Frame rate | 1–240 | 1–60 | `limit.fps` |
| Expression steps | 100,000 per evaluation; 5 × 10⁸ per check or render | same | `expr.budget`, `limit.expr_total` |
| Image pixels per asset | 64 MP, 16,384 px per side | same | `limit.image_size` / `media.image_too_large` |
| Archives (sequence zips, dotLottie) | 2 GB unpacked, ratio ≤ 100, ≤ 1,000 entries | same | `limit.archive` |
| SVG | 50,000 nodes, `use` depth 16 | same | `limit.svg` |
| Lottie import | 20 MB, 5,000 layers, precomp depth 16 | same | `limit.lottie`, `limit.nesting` |
| Gradient stops | 64 | same | resampled, no error |
| Assets | 512, 4 GB total | 512 MB per asset, 2 GB total | `limit.assets` |
| Video / audio sources per render | 32 / 64 | same | `limit.video_sources`, `limit.audio_sources` |
| Normalization wall clock | 20 s | same | `limit.normalize_time` |
| 3D run | 256 drawable layers; 64 lights (w); 8 shadow lights (w) | same | `limit.3d_run_layers`, `limit.3d_lights`, `limit.3d_shadow_lights` |
| Physics | 2,000 bodies, 64 MB bake, 256 forces, 1,000 joints | same | `limit.physics_*` |
| Tracking | 10 min of footage, 64 items | 120 s | `limit.track_duration`, `limit.track_items` |

## 12. A complete minimal document

`examples/01-minimal.json`:

```json
{
  "motion": 1,
  "comps": {
    "main": {
      "size": [1920, 1080], "fps": 30, "duration": 3, "background": "#0B0B0F",
      "layers": [
        { "id": "title", "type": "text", "text": "Hello, 2027",
          "style": { "font": "Inter", "weight": 700, "size": 160, "fill": "#FFFFFF" },
          "origin": "center", "position": ["50%", "50%"] }
      ],
      "timeline": [
        { "target": "title", "from": { "opacity": 0, "y": "+=60" }, "at": 0.2, "dur": 0.7, "ease": "expo.out" }
      ]
    }
  }
}
```

What normalization does: resolves `"50%"` and `origin: "center"` into a pixel anchor (from the measured text bounds) and position; turns the tween into keyframe pairs (the `y` tween becomes whole-vector `position` keys with x held, because a single keyed dimension is rejoined); keeps `expo.out` as a catalog name; converts every colour to a linear float object; fills every default. Canonical (abbreviated):

```jsonc
{ "motion": 1, "main": "main", "comps": { "main": {
  "size": [1920, 1080], "fps": 30, "duration": 3,
  "background": { "r": 0.0033465, "g": 0.0033465, "b": 0.004777, "a": 1 },
  "layers": [ { "id": "title", "type": "text", "in": 0, "out": 3, "text": "Hello, 2027",
    "style": { "font": "Inter", "weight": 700, "size": 160, "fill": { "r": 1, "g": 1, "b": 1, "a": 1 } },
    "transform": {
      "anchor": [414.18, -58.2],
      "position": { "keys": [ { "t": 0.2, "v": [960, 600], "ease": "expo.out" }, { "t": 0.9, "v": [960, 540] } ] },
      "opacity":  { "keys": [ { "t": 0.2, "v": 0, "ease": "expo.out" }, { "t": 0.9, "v": 100 } ] } } } ] } } }
```

Other examples for this page: `examples/01-variants.json` (three aspect ratios with relative placement, overrides, a disabled layer, per-variant safe areas), `examples/01-markers-assets.json` (markers, marker-relative layer and tween times, every time form, a rational `fps`, a `library:` asset, `meta`, `x-` pass-through, `lint`) and `examples/01-https-asset.json` (an `https:` asset that `check` has not fetched: the info `asset.unmaterialized`, no error).

