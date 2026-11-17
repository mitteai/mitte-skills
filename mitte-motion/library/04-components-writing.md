# Writing components: local definitions, library files, examples, review and versioning

A component definition is a comp with params. Locally it lives under the document's `components`; in the library it is the same object wrapped in an `x-library` file. Source: spec 12 §12.3, §12.6; `engine/crates/rexx-normalize/src/passes/components.rs`; `scripts/build-library-index.py`; `library/README.md`. Worked examples (checked): `examples/concepts/04-custom-component.motion.json` (a card using every param type, a slot, forwarding, switches, templates, a repeat over a list param), `examples/concepts/04-library/…/demo.card.library.json` + `demo.card.examples.json` (a complete library entry) and `04-library-entry.motion.json` (a document using it through `--library`).

## The definition

```json
{ "components": {
    "featureCard": {
      "description": "Icon or logo, title and one line on a surface plate; pops in, holds, sinks out.",
      "params": {
        "title":  { "type": "text", "default": "Feature", "maxChars": 24, "description": "Headline, one line." },
        "icon":   { "type": "asset", "accepts": ["svg"], "default": null, "description": "SVG asset id; null shows a text badge." },
        "accent": { "type": "color", "default": "$theme.color.accent" },
        "hold":   { "type": "time", "default": 2.5, "min": 0.5, "max": 30 },
        "side":   { "type": "enum", "values": ["left", "right"], "default": "left" },
        "shadow": { "type": "boolean", "default": true },
        "enter":  { "type": "preset", "kind": "enter", "default": "slideIn" },
        "tags":   { "type": "list", "minItems": 0, "maxItems": 4, "default": ["new"], "item": { "type": "text", "maxChars": 12 } },
        "size":   { "type": "vector", "default": [560, 320] },
        "layout": { "type": "object", "fields": { "padding": { "type": "number", "default": 28 }, "gap": { "type": "number", "default": 12 } }, "default": { "padding": 28, "gap": 12 } }
      },
      "size": ["{{$props.size[0]}}", "{{$props.size[1]}}"], "duration": "auto",
      "markers": [ { "t": 0.4, "name": "landed" } ],
      "layers": [ … ], "timeline": [ … ] } } }
```

| Field | Type | Default | Notes |
|---|---|---|---|
| `description` | string | — | Required in the library (the index script fails without it); the text the assistant chooses by. |
| `params` | map name → param | `{}` | Names follow the id syntax. Every param needs a `default` unless `required: true`; `default: null` means unset (the index script enforces this for library entries; the engine treats a missing default as `null`). |
| `size` | `[w, h]` numbers, percentages of the instance's parent comp, templates, or `"auto"` | required | `"auto"` measures the content (`split.screen`, the credits blocks). Templated sizes resolve before placement. |
| `duration` | time, `"auto"`, `"parent"`, `$props.x`, template | `"auto"` | See `03-components-using.md` §"What normalization produces". `"{{count($props.words) * $props.beat + $props.hold + 0.35}}"` is a valid duration (`kinetic.words`). |
| `fps` | rate | the instance's comp | Rarely set. |
| `layers` | list | required | As in a comp. No `background` (a collapsed comp's background is never drawn): draw a plate. `$props.*` anywhere, including `enabled`, `parent`, `origin`, `box`, shape item sizes, effect params. |
| `timeline` | list | `[]` | As in a comp; `at` may be `$props.x`, `"+=$props.hold"`, `"{{$props.hold + 0.2}}"`, `"@marker"`, a tween `id` used as a label (`"count-0.15"`). Dropped entirely for engine-built `caption.*` and `credits.*`. |
| `markers` | list | `[]` | Markers of the generated comp; a comp shown once also reads its host's markers for names it lacks (`particles.*` use `"at": "@drop"` from the parent). |
| `layout` | layout object | none | Places `children` (or every layer) once at normalization; `box` defaults to `size`. |
| `motionBlur` | comp motion-blur object | none | |
| `slots` | map name → `{ size, fit, required, description }` | `{}` | `size` `[w, h]` (numbers, percentages of the parent, or `$props.x`); `fit` `cover` \| `contain` \| `fill` \| `none`; `required` (default false). A `slot` layer `{ "id": "art", "type": "slot", "slot": "art", … }` in `layers` is where the content goes; it accepts the common layer fields and may be a tween target. |
| `thumbnail`, `tags` | time, list | middle, `[]` | Library only (catalogue frame time, catalogue tags). |
| `x-engine`, `x-notes` | object, string | — | Library only: engine-backed marker and reviewer notes (both pass the unknown-field check because of the `x-` prefix). |

### Param types

| `type` | Value | Extra fields | Checked at the instance (`03`) |
|---|---|---|---|
| `text` | string | `maxChars`, `maxLines`, `multiline` | `maxChars` |
| `number` | number (or a percent string) | `min`, `max`, `step` | `min`/`max` |
| `color` | color | — | parses as a color |
| `time` | time | `min`, `max` | not range-checked |
| `asset` | asset id | `accepts` | nothing; declare the asset in the document and pass its id |
| `enum` | string | `values` (required) | `values` |
| `boolean` | boolean | — | type |
| `ease` | ease | — | nothing |
| `preset` | preset name | `kind` (`enter`, `exit`, `emphasis`, `loop`) | nothing; used as `"preset": "$props.enter"` |
| `list` | array | `item` (a param spec), `minItems`, `maxItems` | item count; item-object field defaults are filled into every row |
| `object` | object | `fields` (map of param specs) | nothing; field defaults are filled |
| `vector` | `[x, y]` | `min`, `max` | a list of ≥ 2; percent strings allowed |
| `layer` | a layer id of the instance's comp | `accepts` | the layer exists in the instance's comp and its type is in `accepts` (`component.param_invalid` "light: "box" is a solid layer; the param accepts light."). The layer and its parent chain are copied into the generated comp as hidden `_host.<id>` layers (in the generated comp's time, with the host's tweens and keys; a moved, scaled or rotated instance gets two `_host.<instance>.rig0/rig1` nulls that undo its transform) and `$props.<name>` reads `_host.<id>`, so `parent`, `matte`, `fitTo`, `align.to` and `shadowlets.light` inside the definition reach it |
| `font` | font token object | — | nothing; used as `"font": "$props.font"` |

Every param should carry a `description` (required by the index script for library entries). A list item that is an object declares `fields`, each a param spec: `"item": { "type": "object", "fields": { "label": { "type": "text", "required": true }, "value": { "type": "number", "required": true } } }`.

### What you can and cannot do inside a definition

- **Values from params**: `"text": "$props.title"`, `"fill": "$props.accent"`, `"$props.accent.on"` (color modifiers work on `color` params), `"{{$props.size[0] / 2}}"` (arithmetic anywhere a template is allowed: layer fields, shape item sizes, `at`, `dur`, `size`, `box`, preset `props`), `"{{$props.value | $props.format}}"` (a format from a param), `"{{$props.n | pad:2:0}}"`. One format per placeholder; `|` chains are `ref.format`.
- **Structure switches**: a param cannot swap layers or change a type. Use the template-able `enabled` field on layers, tweens, drivers and repeats: `"enabled": "$props.shadow"`, `"enabled": "{{$props.icon == null}}"`, `"enabled": "{{$props.line != ''}}"`, `"enabled": "{{count($props.tags) > 0}}"`. A disabled layer is removed before the timeline compiles; a tween whose every target was dropped is a no-op (`tween.target_disabled`, info). One layer per alternative (`num` and `glyph` in `explainer.step`; an `image` and a `video` layer each enabled by the param that selects it).
- **Lists**: a `repeat` with `"data": "$props.<list>"` stamps one layer per item (`$item`, `$item.<field>`, `$index`, `$count`); `count($props.list)`, `sum($props.series.value, $index)`, `max($props.lines.end)` aggregate it. A repeat template cannot carry tweens; target the copies from the component's timeline (`"target": "tags.*"`) or key them from `$item` fields (`lyrics`, `kinetic.words`).
- **Slots**: declare under `slots`, place a `slot` layer. Inside a definition a nested instance fills its slots from the definition (`"slots": { "screen": [ { "type": "slot", "slot": "screen" } ] }`, as `screen.demo` does) or forwards one whole: `"slots": { "art": "$slots.pic" }`. `$slots.<name>` is valid only inside a definition declaring that slot.
- **Nesting**: layers may be instances of local or library components (`screen.demo` nests `ui.cursor` and `device.laptop`; `transition.light-leak` nests `light-leak`).
- **Theme and data**: `$theme` and `$data` are the document's. Prefer tokens to literals everywhere except where the look is defined by a literal (a caption's black stroke, a device's black bezel, macOS traffic lights).
- **Not expressible**: an enum that switches geometry (`chart.bar` has no orientation; `transition.mask-wipe` is a circle), a boolean that removes a tween without `enabled`, a `fitTo` that fixes one dimension, a running sum across siblings for anything but `sum(list, n)`, keyframes generated from a number (`countdown` is fixed at 3), reading a layer of the instance's comp from inside (hence slots for particle targets).

### Library entries that show the patterns

`lower-third.bar` (fitTo plate, `align` chains, preset params, a label defined by a tween id), `chart.bar` (repeat over a list param under a `layout`, templated tween target `bars.{{$props.highlight | lower}}`, `enabled` on the highlight tweens), `chart.donut` (`sum($props.series.value, $index)` per segment), `explainer.step` (two layers switched by `enabled`), `stat.counter` (`{{$props.value | $props.format}}`, `clamp` in a rotation), `transition.wipe` (null rig, keys templated from `$props.dur`, alpha matte, `enabled: "{{$props.bar > 0}}"`), `screen.demo` (nested library instances and slot forwarding), `kinetic.words` (duration from `count()`), `ui.cursor` (a repeat whose template's `in`/`offset` come from `$item.t`). Their files are named in `91-components-<group>.md`.

## A library file (`x-library`)

```json
{ "x-library": {
    "meta": { "name": "demo.card", "version": "1.0.0", "phase": "P1", "kind": "component", "status": "draft",
              "description": "…", "tags": ["demo", "card"], "author": "…", "license": "MIT",
              "examples": "demo.card.examples.json", "spec": ["12 §12.3.1"], "x-notes": "…" },
    "components": { "demo.card": { "description": "…", "params": { … }, "size": [800, 240], "duration": "auto", "thumbnail": 1.0, "tags": ["card"], "layers": [ … ], "timeline": [ … ] } } } }
```

| Rule | Enforced by |
|---|---|
| One top-level key `x-library` with `meta` and exactly one of `themes`, `presets`, `components` | engine loader (a file without `x-library` is ignored) and `build-library-index.py --check` |
| The map is keyed by the entry's full dotted name (`demo.card`); `meta.name` equals it (a preset pack's `meta.name` is the pack, its entries `pack.name`) | index script (ref derived from the key) |
| `meta.version` is semver `major.minor.patch`; the reference `mitte/<name>@<major>` resolves to the newest matching version; a file with no version is `1.0.0` | engine loader, index script |
| `meta.namespace` (optional, default `mitte`) is the prefix of the reference | engine loader |
| File location `library/<namespace>/<kind>/<group>/<name>.library.json`, one component per file; group directories are organizational (the name carries no group prefix: `lower-thirds/lower-third.bar.library.json`) | convention |
| `meta.status` is `draft` until a motion designer approves the entry (`meta.reviewedBy` names them); `phase` is the phase it shipped in | review (`library/README.md`); nothing in the engine reads them |
| Every component has `description`; every param has `description` and a `default` or `required: true`; enums have `values` | `build-library-index.py --check` |
| Every theme file has all nine token groups and names only pack fonts | index script |
| A sibling `<name>.examples.json` with exactly two examples whose docs have `"motion": 1`, a main comp with layers, and instantiate the entry | index script |

The examples file:

```json
{ "x-library-examples": {
    "component": "mitte/demo.card@1",
    "golden": { "variants": ["default", "vertical", "square"], "frames": ["thumbnail", "25%", "50%", "90%"], "dir": "golden/demo.card/" },
    "examples": [
      { "id": "plain", "title": "Default props on the clean theme", "doc": { "motion": 1, "theme": { "use": "mitte/clean@1" }, "comps": { … }, "variants": { "vertical": { "size": [1080, 1920] }, "square": { "size": [1080, 1080] } } } },
      { "id": "long-hold", "title": "…", "doc": { … } } ] } }
```

Each `doc` is a complete, renderable document with a theme, the instance, any assets or data it needs (placeholder URLs under `https://media.mitte.ai/u/p0/`) and the two other aspect-ratio variants. `golden` names what library CI will render (not running yet: no golden frames or thumbnails are committed). Spec 12 §12.6.1 names the entries as the repository has them: `{ "id", "title", "doc" }` (or prop sets under `meta.examples`).

To test an entry without installing it: put the file under any directory tree and point the engine at it (`rexx-engine check --doc x.motion.json --library <that dir>`; the loader recurses, and `mitte/default@1` falls back to the built-in copy), as `examples/concepts/04-library-entry.motion.json` does through `meta.x-skills.library`. To ship it: add the file and its examples under `library/mitte/components/<group>/`, run `python3 scripts/build-library-index.py` (regenerates `library/index.json`; `--check` validates only), run `motion.check` on both examples (no errors; lint warnings only when waived in `x-notes` with a reason), then bump the engine version (the library ships inside the engine tarball; `CLAUDE.md`).

## Review and versioning

Review (spec 12 §12.6.3, `library/README.md`): a motion designer authored or approved it; two examples rendered at 16:9, 9:16 and 1:1; clean `motion.check`; descriptions proven on three briefs; the version follows the rules below. Approval is a PR that flips `status` and names `reviewedBy`.

| Change | Bump |
|---|---|
| Fixes that do not change params (easing, a stroke width, a wrong token); golden frames may change | patch `1.0.0` → `1.0.1` |
| New params whose defaults reproduce the old look, new slots, better rendering | minor `1.0` → `1.1` |
| Removing or renaming a param, changing a default's look, changing `duration: "auto"` timing, a theme token value that moves pixels | major `1` → `2` (old majors stay ≥ 12 months) |

Every entry today is `1.0.0`; a new library release is an engine release because the library is compiled into the image.

## Writing a theme or a preset pack

A theme file is `{ "x-library": { "meta": { "name": "clean", "kind": "theme", … }, "themes": { "clean": { color, font, type, space, radius, motion, ease, spring, texture, styles? } } } }` with every group present (`01-themes.md` lists each token; `92-themes.md` shows ten complete files' values). A preset pack is `{ "x-library": { "meta": { "name": "kinetic", "kind": "preset", … }, "presets": { "kinetic.slam": { description, params, dur, ease, tweens } } } }` (`02-presets.md`).
