# Using components: instances, props, slots, what normalization produces

A component is a parameterized comp (a local one under `components`, or a library one `mitte/<name>@1`); an **instance** is a layer of type `component` that sets its params. Everything here is verified against engine 0.1.48 (`engine/crates/rexx-normalize/src/passes/components.rs`). Every library component's params are in `91-components-<group>.md`; writing components is `04-components-writing.md`.

## The instance layer

```json
{ "id": "lt", "type": "component", "use": "mitte/lower-third.bar@1", "in": 4, "collapse": false,
  "props": { "name": "Ada Lovelace", "role": "Analyst, Engine Co.", "hold": 2.5, "side": "left" },
  "align": { "to": "safe", "x": "left", "y": "bottom" } }
```

| Field | Notes |
|---|---|
| `use` | a local component id or a library reference (`00-overview.md`). `component.unknown` when neither. |
| `props` | param values. Omitted params take their `default`; a `null` value counts as omitted. `$theme`, `$data`, `$data.@asset` references and `{{ }}` templates are resolved in props before validation (a template that produces a too-long text fails `maxChars`). Unknown names: `component.unknown_param` ("The component has no param "nmae"." hint "Did you mean "name"? Valid params: name, role, …"). |
| `slots` | map slot name → list of layers (or `"$slots.<name>"` inside a component definition, `04`). Unknown slot: `component.slot_unknown` ("Component "mitte/transition.push@1" declares no slot "c"." with the valid names); an empty required slot: `component.slot_required` ("The slot "b" is required." hint "Give it layers under `slots.b`."). |
| `in`, `out`, `dur` | the instance's span. `out` defaults to `in` + the generated comp's duration; `dur` is accepted on an instance as `out = in + dur`. `in` and `out` may be marker forms of the instance's comp (`"in": "@step3"`, `"@drop+0.5"`); the default `out` is derived from the resolved `in`. |
| `collapse` | default `true` (blend modes, 3D and motion blur inside behave as if the layers sat in the parent). `false` renders a flat precomp. |
| all common layer fields | `position`, `origin`, `align`, `scale`, `rotation`, `opacity`, `parent`, `matte`, `blend`, `effects`, `masks`, `motionBlur`, `offset`, `stretch`, `enabled`, `transitionIn/Out` apply to the instance as a whole. Tweens in the parent timeline target the instance id (`"target": "lt"`). |

### Param validation (what `component.param_invalid` checks)

| Param type | Checked |
|---|---|
| `number` | type (a number, or a percentage string `"50%"`), `min`/`max` ("hold: 99 is above the maximum 30."), `step` counted from `min` (or 0): "n: 0.7 is not a multiple of step 0.5 (from 0)." |
| `time` | a number of seconds, a time string (`"2s"`) or a marker form (`"@drop"`, `"@drop+0.5"`); `min`/`max` in seconds on the first two ("hold: 99 s is above the maximum 30 s."; frame forms like `"12f"` and markers are not range-checked) |
| `text` | on a string: `maxChars` ("name: 51 characters is more than maxChars 40."), `maxLines` counted on explicit line breaks ("title: 3 lines is more than maxLines 2."; wrapping is not measured); spans, numbers and font tokens pass unchecked (several library components declare a font as a `text` param) |
| `enum` | `values` ("side: "top" is not one of left, right.") |
| `boolean` | `true`/`false` |
| `list` | a list, `minItems`/`maxItems` ("series: 0 items is fewer than minItems 1."), and every row against `item` with the row's pointer (`/props/rows/0/value`, "rows[0].value: 12 is above the maximum 10."); `item` field defaults are filled into every row |
| `object` | an object; every field against its spec, a missing `required` field ("rows[1]: the field "label" is required.") |
| `color` | parses as a color ("accent: "notacolor" is not a color.") |
| `vector` | a list of ≥ 2; numeric components against `min`/`max`; percent strings pass |
| `asset`, `preset`, `ease`, `font` | nothing beyond required-ness (`layer`: see `04-components-writing.md`) |

A `$theme`/`$data`/`$props` reference or a `{{ }}` template is checked once it resolves (in a nested component, when the outer props reach it). A required param with no value is `component.param_required` ("The param "series" is required." hint "Add "series" to `props`."). Validation runs on the **resolved** value, so a template or `$data` reference that resolves to a bad value fails here with the same codes.

An `asset` param takes an asset id or a URL (`https:`, `library:`). A URL is declared as the document asset `<instance>.<param>` (`"props": { "logo": "https://…/brand.svg" }` on instance `sting` declares `sting.logo`; when that id already names another source, `<comp>.<instance>.<param>`), with the type of the param's single `accepts` entry, else of the file extension (`.png` image, `.svg` svg, `.mp4` video, `.mp3`/`.wav` audio, `.json` data or lottie, `.cube` lut), and the service fetches it like any declared asset. Locally, map that id with `--assets`. Only instances in the document's comps (and their slot content) are seen by the service; a URL written inside a component definition is declared by the engine but not fetched, so pass such files in from the instance. A `library:` URI in a layer's `asset` field is declared automatically as `<layer id>.asset`.

## What normalization produces

For an instance `lt` of a component with definition `D` in comp `main`:

1. A generated comp `lt.comp` (an instance inside a generated comp whose id is already taken becomes `<host>.<id>.comp`: nested instances `c` five levels deep become `c.comp`, `c.c.comp`, `c.c.c.comp`, …), built from `D.layers` with every `$props` replaced, `D.timeline`, `D.markers`, `D.layout`, `D.motionBlur`; disabled layers removed; each `slot` layer replaced by a comp layer showing `lt.slot.<name>` (a comp of the slot's `size`, the host's `fps` and `duration`, holding the provided layers, `collapse: true`).
2. The instance becomes a comp layer `{ "id": "lt", "type": "comp", "comp": "lt.comp", "collapse": true, "x-component": { "use", "props" } }` with every other layer field kept. `x-component` carries the fully resolved props (defaults filled, references resolved) for round-tripping.
3. Size: `D.size` `[w, h]` (numbers or percentages of the **instance's parent comp**: `["100%", "100%"]` is the parent's size); `"auto"` is measured from the content later. Duration: `D.duration` `"auto"` = the end of the last timeline entry, key or layer `out` (an instance of `lower-third.bar` with `hold: 2` lasts 3.27 s; `caption.*` ends at the last word's `end`); a number or `$props.x`; `"parent"` = `out − in` of the instance (`bg.grid` with `in: 2, out: 6` makes a 4 s comp; with no `out`, until the parent comp's end).
4. `out`: when the instance gives none, `in + duration` for a timed component (it disappears when its animation ends), the parent's end for `duration: "parent"`. An `out` later than the generated comp's end shows nothing for the remainder (the instance is a comp layer with no hold), so set `out` only to **cut** an instance short or to size a `"parent"` component.
5. `stats.library` records the resolved version.

Resolution rule inside the definition: percentages, `$theme.type.size.<n>`, `$theme.space.<n>`, `align` targets (`safe`, `comp`, `action`) resolve against the instance's **parent comp**, so a component looks the same inline and instanced and its text scales with the variant; only pixel `position` values are in the component's own canvas.

## Placing an instance

An instance is placed like any layer. The generated comp's canvas is `D.size`; use `origin` plus `position`/`align` on the instance: `"origin": "center", "position": ["50%", "40%"]` centres a 1400 × 800 `logo.sting`; `"align": { "to": "safe", "x": "left", "y": "bottom" }` parks a lower third in the title-safe corner (match `side` to the edge). Full-frame components (`size ["100%", "100%"]`: every `particles.*`, `bg.*`, overlay, transition, caption, `social.frame`, `social.story`, `map.pin`, `callout.*`, `kinetic.words`, `lyrics`, `ui.cursor`, `cta.endcard`, the credits) need no placement; their own params take percentages of the frame. A device mockup is huge on purpose (`device.phone` 1290 × 2652): `"scale": [28, 28]` on the instance.

Variants: `variants.<id>.override.<instance id>` deep-merges into the instance, so `"props": { "side": "right" }` changes one prop, `"enabled": false` drops the instance, and `align`/`position` reposition it; everything else re-resolves per variant (verified in `examples/concepts/03-instances.motion.json` for `vertical` and `square`).

## Slots

```json
{ "id": "phone", "type": "component", "use": "mitte/device.phone@1", "in": 3.5, "out": 9.5,
  "props": { "tilt": -6, "float": 10, "duration": 6 },
  "slots": { "screen": [ { "id": "screenFill", "type": "solid", "color": "$theme.color.accent", "size": [1170, 2532] },
                         { "id": "screenText", "type": "text", "text": "Hello", "style": { "font": "$theme.font.display", "size": 160, "fill": "#FFFFFF" }, "origin": "center", "position": [585, 1266] } ] },
  "scale": [28, 28], "origin": "center", "position": ["76%", "52%"] }
```

Slot content is a list of ordinary layers positioned in the slot's own pixel space (`device.phone` `screen`: 1170 × 2532; `device.laptop`: 2560 × 1600; `browser.window` `page`: 1600 × 936; transitions and particle slots: the parent frame). The slot comp is fitted with the slot's `fit` (`cover` for devices). Slot layers may be anything, including other instances; `$theme` and `$data` resolve as in the document. An empty optional slot renders nothing. Which components have slots: `device.phone`, `device.laptop`, `browser.window`, `screen.demo` (`screen`, required), `ui.cursor` (`content`), `split.screen` (`a`–`d`), every `transition.*` (`a`, `b`, required), `particles.assemble`, `particles.disintegrate`, `particles.form-logo` (`layer`, required), `credits.cast-card` (`still`).

## Repeats of instances, nesting, data

A `repeat` whose template is an instance stamps one instance per item: `"layer": { "type": "component", "use": "mitte/lower-third.pill@1", "props": { "name": "$item.name", "role": "$item.role", "initials": "$item.initials" } }` with `"ids": "{{$item.id}}"` makes `people.ada`, `people.grace` (an `ids` template must produce a valid id segment: `"ada lovelace"` is `repeat.id_template`; one format per placeholder: `{{$item.name | upper | pad:2}}` is `ref.format`). A `layout` on the repeat places the copies.

Instances nest (a component's layers may hold instances, local or library) to an authored depth of 4: an instance in the document is level 1, one inside its definition level 2; a fifth level is `component.depth` at the innermost instance ("Component instances nest 5 deep here (c1 → c2 → c3 → c4 → c5); the limit is 4."). Slot content counts at the level of the instance that supplies it. A definition that instances itself, directly or through others, is `component.cycle` ("Component "a" instances itself (a → a)."); the generated-comp guard (`component.cycle` past 16 generated levels) stays as a backstop.

A list param may be fed from `data` (`"series": "$data.rows"`) or from a data asset (`"words": "$data.@transcript.words"`, `"sections": "$data.sections"`); locally a data asset must be mapped with `--assets`, otherwise `ref.unresolved` "Data asset "transcript" is not available.".

## Engine-backed components

Sixteen components carry `x-engine`: the four `caption.*` and eight `credits.*` (the normalizer **replaces** the definition's layers and drops its timeline, building a text layer from the props: `05-captions.md`, `06-credits.md`), `chart.line` (the path through the points), `ui.cursor` (keys from `moves`), `screen.demo` (device swap and coordinate mapping) and `browser.window` (`typeUrl`). The last four stamp the reference layers like any component; what their `x-engine.derives` text promises beyond that is not all implemented (`91-components-*.md` reproduces the text; `05`/`06` say what the engine does).

## Diagnostics summary

`component.unknown`, `component.unknown_param`, `component.param_invalid`, `component.param_required`, `component.slot_unknown`, `component.slot_required`, `component.depth` (authored nesting past 4), `component.cycle` (a definition that instances itself; expansion deeper than 16), `ref.library_unknown`, `ref.library_version`, `repeat.id_template`, `ref.unresolved` (a `$data` path or data asset that does not resolve), `ref.format`. Lint inside generated comps is reported with the generated comp's path (`/comps/lt.comp/layers/1`): `lint.offscreen_while_visible` on `lower-third.bar`'s `tick`, `lint.too_many_simultaneous_moves` on `logo.sting`'s six sparkles and `lint.expensive_effect` on its glow and bloom are properties of the components, not of your document.

Worked example (checked in all three variants): `examples/concepts/03-instances.motion.json`: `bg.grid` with `duration: "parent"`, `logo.sting` with a declared SVG asset, `device.phone` with slot layers and an explicit `out`, `lower-third.bar` with `collapse: false` and `align`, a repeat of `lower-third.pill` instances from `data`, and variant overrides of props, placement and `enabled`.
