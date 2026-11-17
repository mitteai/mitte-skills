# 13. Themes, data and templates, components, repeat, layout

Scope: spec 12 §12.1–12.5 (all authored form: the normalizer expands everything). The library's catalog of themes, presets and components belongs to the library area (`library/90-catalogue.md`); this page defines the constructs. Generated tables: `Theme`, `ThemeTokens`, `ColorToken`, `FontToken`, `TypeTokens`, `SpaceTokens`, `MotionTokens`, `SpringParams`, `TextureTokens`, `StylesValue`, `Brand`, `Component`, `ComponentSize`, `ComponentDuration`, `Param`, `ParamType`, `Slot`, `SlotContent`, `RepeatData`, `Layout`, `LayoutAlign`, `LayoutJustify`, `LayoutPath`, `PathSpacing`, `StackDirection`, `Cell`, `Padding` in `92-schema-types-*.md`.

## 1. Themes

Named tokens any value may reference with `$theme.<path>`. Presets and library components use tokens, so one brand changes every component.

```jsonc
"theme": {
  "use": "mitte/clean@1",                                   // start from a library theme
  "override": { "color": { "accent": "#FF4D00" }, "font": { "display": { "family": "Space Grotesk", "weight": 700 } } },
  "brand": { "asset": "brandKit" }                           // a data asset holding a partial theme + font assets
}
```

Or inline in full (no `use`). Merge order: library theme → brand kit → `override`; objects deep-merge, arrays (`palette`, `space.scale`) replace. No `theme` at all: `mitte/default@1` applies, so presets always resolve. A theme cannot reference other tokens except the colour modifiers on its own colours (`"surface": "$theme.color.bg.lighter"`). A missing token is `ref.unresolved`; a wrongly typed one `theme.invalid`. Tokens resolve once: animate the property, not the token. Library themes: `mitte/default@1`, `clean`, `midnight`, `editorial`, `bold`, `soft`, `mono`, `neon`, `corporate`, `retro` (values in `library/90-catalogue.md`).

### 1.1 Token groups (defaults are `mitte/default@1`)

| Group | Token | Type | Default | Used by |
|---|---|---|---|---|
| `color` | `bg`, `fg`, `accent`, `muted`, `surface`, `line` | colour | `#0B0B0F`, `#F5F5F7`, `#7C5CFF`, `#8A8A99`, `#16161D`, `#2A2A35` | backgrounds, text, highlights, plates, dividers |
| | `palette` | list of colours | `#7C5CFF #22D3EE #F472B6 #FACC15 #34D399` | charts, repeat items (`$theme.color.palette.$index` wraps) |
| | `positive`, `negative`, `warning` | colour | `#34D399`, `#F87171`, `#FACC15` | data stories |
| `font` | `display`, `body`, `mono` | font token `{ family, weight, style?, tracking?, axes? }` (any character-style field) | Inter 800 (tracking −20), Inter 500, JetBrains Mono 500 | `"font": "$theme.font.display"`: the family becomes `font`, the other fields become style defaults the style's own fields override |
| `type` | `base` | fraction of the shorter side | 0.042 | `$theme.type.size.<n>` |
| | `ratio` | number | 1.333 | modular scale |
| | `lineHeight` | number | 1.15 | library components' leading |
| `space` | `unit`, `scale` | fraction, list | 0.0125, `[0, 1, 2, 3, 4, 6, 8, 12, 16, 24]` | `$theme.space.<n>` |
| `radius` | `s`, `m`, `l`, `pill` | px | 8, 16, 32, 9999 | rounded rectangles |
| `motion.dur` | `xs`, `s`, `base`, `l`, `xl`, `transition` | seconds | 0.15, 0.3, 0.5, 0.8, 1.2, 0.5 | tween, preset and transition durations |
| `motion.stagger` | `tight`, `base`, `loose` | seconds | 0.02, 0.05, 0.1 | stagger `each` |
| `ease` | `default`, `enter`, `exit`, `move`, `emphasis`, `linear`, `transition` | ease | `power2.out`, `expo.out`, `power2.in`, `[0.2, 0, 0, 1]`, `back.out(1.7)`, `linear`, `power3.inOut` | tweens without an ease; enter/exit presets; moves; pops; loops; transitions |
| `spring` | `gentle`, `snappy`, `bouncy` | `{ bounce, duration }` or `{ stiffness, damping, mass }` | `{0, 0.5}`, `{0.15, 0.35}`, `{0.3, 0.6}` | `"ease": "$theme.spring.snappy"` |
| `texture` | `grain`, `grainSize`, `vignette`, `halftone` | 0–1, px, 0–1, 0–1 | 0, 1, 0, 0 | > 0 adds a `_texture` adjustment layer (grain / vignette / `stylize.halftone`) on top of the root comp, a full-frame cost on every frame |
| `styles` | `<name>` | a layer-styles object | none | `"styles": "$theme.styles.card"` on a layer |

### 1.2 Derived tokens and colour modifiers

| Reference | Value |
|---|---|
| `$theme.type.size.<n>`, *n* in [−2, 8] | `base · ratio^n · shorterSide`, rounded to 0.5 px (≈ 45 px at 1080p for `size.0`; `size.4` ≈ 143; `size.6` ≈ 254) |
| `$theme.space.<n>` | `unit · scale[n] · shorterSide` |
| `$theme.color.palette.<i>` | `palette[i mod len]` |
| `<colour reference>.a10` … `.a90`, `.lighter`, `.darker`, `.on` | alpha 10–90 %; ±12 % OKLab lightness; black or white, whichever contrasts more. On **any** colour-typed reference (`$theme.color.accent.a20`, `$props.accent.on`, `$item.color.darker`, `$data.brand.primary.a50`); on a non-colour it is `ref.unresolved` |

Spring tokens: `bounce` in [−1, 1], `duration` > 0 → `stiffness = (2π/duration)²`, `damping = 4π(1 − bounce)/duration` for `bounce ≥ 0`, `4π/((1 + bounce)·duration)` below; mass 1.

### 1.3 Brand kits

`"brand": { "asset": "brandKit" }` names a `data` asset (JSON) holding a partial theme (usually `color`, `font`, font `assets`) and optional `logo` assets; its font files become assets `brand.font.<n>`.

## 2. Data and templates

`data` is any JSON (≤ 512 KB; larger as a `data` asset: JSON, or CSV which becomes rows keyed by the header with numeric cells parsed, read as `$data.@<assetId>`; until it is fetched every such reference reads an empty table, `[]`, with one `asset.unmaterialized` info, so the document checks before the fetch; a path missing from a fetched asset is `ref.unresolved`). The service merges tool-input `data` over the document's, so one document renders many videos. `$data.<path>` where a whole value is needed; `{{ … }}` templates inside strings.

### 2.1 Template strings

A string containing `{{ … }}`; each placeholder holds one expression and an optional format after `|`:

```jsonc
"text": "Q{{$data.quarter}} revenue"
"text": "{{$data.revenue | currency:USD:0}}"               // $4,182,000
"text": "{{$data.growth | percent:1}} year over year"       // 12.4% (the input is a fraction)
"text": "Launching {{$data.launch | date:MMMM d}}"           // Launching March 14
"text": "{{$item.label}}: {{$item.value | number:0}}"
"size": "{{$props.size * 0.6}}", "at": "{{$props.hold + 0.2}}", "enabled": "{{$props.style == 'pill'}}"
"text": "{{$props.value | $props.format}}"                   // the format slot from a text param
```

| Format | Arguments | Example (`en-US`) |
|---|---|---|
| `number` | decimals (default auto), `compact` | `4182000 \| number:0` → `4,182,000`; `number:1:compact` → `4.2M` |
| `currency` | ISO code (`USD`, `EUR`, `GBP`, `JPY`, `INR`, `KRW`, `BRL`, `CHF`, …), decimals | `19.5 \| currency:EUR` → `€19.50` |
| `percent` | decimals | `0.124 \| percent:1` → `12.4%` |
| `date` | a CLDR pattern | `2027-03-14 \| date:EEE d MMM` → `Sun 14 Mar` |
| `time` | — | `95 \| time` → `1:35` (or `h:mm:ss`) |
| `upper`, `lower`, `title` | — | case conversion (Unicode-aware) |
| `pad` | width, char | `7 \| pad:2:0` → `07` |
| `default` | fallback text | `$data.subtitle \| default:` → empty when missing: the only way a missing reference is not an error |

Locale: `data.locale`, else `output.locale`, else `en-US` (CLDR data bundled, deterministic). A reference that does not hold a valid format is `ref.format`; a malformed template `ref.template`. Templates resolve once, at normalization, wherever a template is allowed (layer fields, component definitions, timeline `at`, preset props, repeat templates).

**The placeholder grammar** (a fixed, side-effect-free expression language evaluated at normalization; not the expression language of [12](12-expressions.md)): numbers, strings (`'pill'`), `true`/`false`/`null`, references (`$data.x`, `$props.x`, `$item`, `$index`, `$count`, `$parent.item`, `$parent.index`, `$theme.x`, `$comp.width`/`.height`/`.aspect`: the size of the comp the value resolves against, the instance's parent inside a component), paths with computed segments (`$data.rows[$index - 1]`, `$theme.color.palette.$index`), arithmetic `+ − * / %` with parentheses, comparisons `== != < <= > >=` (booleans), string concatenation with `+`, and the functions:

| Function | Meaning |
|---|---|
| `min(a, b, …)`, `max(a, b, …)` | scalars; with one list argument, the list's min/max (an empty list is `ref.unresolved`) |
| `round(x)`, `floor(x)`, `ceil(x)`, `abs(x)`, `sqrt(x)` (negative is an error) | |
| `atan2(y, x)` | degrees, as `rotation` (`atan2(1, 1)` → 45) |
| `clamp(x, a, b)`, `lerp(a, b, t)` | |
| `sum(list)`, `sum(list, n)`, `sum(list, from, to)` | the whole list, the first *n* items, items `from ≤ i < to` (bounds clamp); `sum($props.series.value, $index)` is the running total before the current item |
| `count(list)` | the length (0 for an empty list) |

A path segment applied to a list maps over it (`$data.sales.value` is every row's `value`). List indexes past either end and reads through `null` give `null` (test it or use `| default:`); a missing root is `ref.unresolved`. A placeholder that is the entire string and yields a number or boolean produces that value, not a string (`"{{$index * 120}}"` → `120`). A function result that is not finite is an error. Fields that take literals only (no placeholder, engine 0.1.48): enum-valued fields (animator `wave`/`dim`, loop types, stagger `from`/`axis`, blend modes), spring physical parameters, `loop.keys`/`loop.count`, `stagger.seed`, `ae.influence`.

Numbers that should count on screen use the `countUp` preset, which keeps the format: `{ "target": "stat", "preset": "countUp", "props": { "from": 0, "format": "currency:USD:0" } }`.

## 3. Components

A reusable, parameterized piece of motion: a comp definition with params; an instance is a layer that sets them (After Effects precomp + Essential Graphics in one).

### 3.1 Definition

```jsonc
"components": {
  "lowerThird": {
    "description": "Name and role plate that slides in, holds, slides out.",
    "params": {
      "name":   { "type": "text",  "default": "Name Surname", "maxChars": 40, "description": "Person's name, one line." },
      "role":   { "type": "text",  "default": "Role", "maxChars": 60 },
      "accent": { "type": "color", "default": "$theme.color.accent" },
      "hold":   { "type": "time",  "default": 4, "min": 1.5, "max": 30 },
      "side":   { "type": "enum",  "values": ["left", "right"], "default": "left" },
      "enter":  { "type": "preset", "default": "slideIn", "kind": "enter" },
      "showRole": { "type": "boolean", "default": true }
    },
    "size": [900, 220], "duration": "auto",
    "slots": { "art": { "size": [240, 240], "fit": "cover", "description": "A picture.", "required": false } },
    "layers": [
      { "id": "bar", "type": "shape", "contents": [ { "id": "r", "type": "rect", "roundness": "$theme.radius.s", "fitTo": { "layers": ["name", "role"], "padding": [32, 24] } }, { "type": "fill", "color": "$theme.color.surface" } ] },
      { "id": "tick", "type": "shape", "align": { "to": "bar", "x": "left", "y": "center" }, "contents": [ { "type": "rect", "size": [8, 120] }, { "type": "fill", "color": "$props.accent" } ] },
      { "id": "name", "type": "text", "text": "$props.name", "style": { "font": "$theme.font.display", "size": "$theme.type.size.2", "fill": "$theme.color.fg" } },
      { "id": "role", "type": "text", "text": "$props.role", "enabled": "$props.showRole", "style": { "font": "$theme.font.body", "size": "$theme.type.size.0", "fill": "$theme.color.muted" } },
      { "id": "art", "type": "slot", "slot": "art", "position": [760, 110] }
    ],
    "layout": { "type": "stack", "direction": "column", "gap": 6, "padding": [32, 24], "children": ["name", "role"] },
    "timeline": [
      { "target": ["bar", "tick"], "preset": "$props.enter", "props": { "dir": "$props.side" }, "at": 0 },
      { "target": ["name", "role"], "preset": "rise", "stagger": "$theme.motion.stagger.base", "at": "<0.15" },
      { "target": ["bar", "tick", "name", "role"], "preset": "slideOut", "props": { "dir": "$props.side" }, "at": "+=$props.hold" }
    ]
  }
}
```

| Field | Type | Default | Notes |
|---|---|---|---|
| `description` | string | — | required for library entries (what the assistant reads) |
| `params` | map name → param | `{}` | §3.2; names follow the id syntax |
| `size` | `[w, h]`, `"auto"`, or a template | — | the component's canvas; `"auto"` = the bounds of the content at its first fully visible moment |
| `duration` | time, `"auto"`, `"parent"`, or `$props.x` | `"auto"` | `"auto"`: the end of the last timeline entry or layer `out` (a layer without `out` counts to its last key; a component with nothing timed keeps the instance's length); `"parent"`: as long as the instance (loops and captions run while it is on screen) |
| `fps` | rate | the instance's comp rate | rarely set |
| `layers`, `timeline`, `markers`, `motionBlur` | | | exactly as in a comp, with `$props` anywhere; **no `background`** (an instance is collapsed: draw a plate as a solid or rect) |
| `layout` | layout | none | §5 |
| `slots` | map name → `{ size, fit: cover \| contain \| fill \| none, description, required }` | `{}` | §3.4 |
| `thumbnail` | time | the middle | library only |
| `tags` | list of strings | `[]` | library only |

**Resolution rule**: inside a component, everything that depends on a comp resolves against the **instance's parent comp**: percentages, `$theme.type.size.<n>` and `$theme.space.<n>`, `align` targets (`safe`, `comp`, `action`), safe areas. Only `transform.position` values are in the component's own canvas. `$theme` and `$data` are the document's. Marker times inside a component (`"@drop"`) read the host comp's markers for names it lacks.

### 3.2 Params

| `type` | Value | Extra fields | Notes |
|---|---|---|---|
| `text` | string or spans | `maxChars`, `maxLines`, `multiline` (false) | over-long text is `component.param_invalid` unless the text layer shrinks |
| `number` | number | `min`, `max`, `step` | |
| `color` | colour | — | |
| `time` | time | `min`, `max` | |
| `asset` | asset id or URL | `accepts` (list of asset types) | a URL in props becomes an asset `<instance>.<param>` |
| `enum` | string | `values` (required) | |
| `boolean` | boolean | — | |
| `ease` | ease | — | |
| `preset` | preset name | `kind` (`enter`, `exit`, `emphasis`, `loop`) | lets the instance choose its own entrance or exit |
| `list` | array | `item` (a param spec per element), `minItems`, `maxItems` | feeds `repeat` inside the component |
| `object` | object | `fields` (map of param specs) | grouped settings |
| `vector` | `[x, y]` | `min`, `max` | percent strings allowed, resolved against the instance's parent comp |
| `layer` | layer id | `accepts` (layer types) | a layer **of the instance's comp** (for `fitTo`, `align.to`, `follow`, `matte`); the normalizer rewrites the reference when it expands the instance |
| `font` | font token | — | `{ family, weight, style?, tracking?, axes? }`; `"$theme.font.display"` is the usual value |

Every param needs a `default` unless `required: true`; `default: null` means unset. `description` is optional locally, required in the library. Mutually exclusive params each default to `null` and say so in their descriptions. **Params change values, not structure**: the one mechanism for structure is the template-able `enabled` on **layers, tweens and drivers** (a shape item's `enabled` is a literal boolean: `doc.type` with a reference) (`"enabled": "$props.showRole"`, `"{{$props.style == 'pill'}}"`); a dropped layer makes tweens on it no-ops (`tween.target_disabled`). `$props.x` works anywhere in the definition, including `at`, preset props, `parent`, `origin`, `size`.

### 3.3 Instances

```jsonc
{ "id": "lt1", "type": "component", "use": "lowerThird",
  "props": { "name": "Ada Lovelace", "role": "Analyst, Engine Co.", "hold": 5 },
  "slots": { "art": [ { "id": "pic", "type": "image", "asset": "shot", "fit": "cover" } ] },
  "in": 2.0, "align": { "to": "safe", "x": "left", "y": "bottom" } }
{ "id": "lt2", "type": "component", "use": "mitte/lower-third.split@2", "props": { "name": "Grace Hopper" }, "in": 9 }
```

| Field | Notes |
|---|---|
| `use` | a local component id or a library reference `mitte/<name>@<version>` (`@2` newest 2.x.y; `@2.3`; `@2.3.1` exact); unknown: `component.unknown` / `ref.library_unknown` / `ref.library_version` |
| `props` | param values; unknown keys `component.unknown_param` (the hint lists the valid ones); bad values `component.param_invalid`; missing required `component.param_required` |
| `slots` | layers per slot (§3.4); `component.slot_unknown`, `component.slot_required` |
| common layer fields | `in`, `out`, `offset`, `stretch`, `transform`, `parent`, `matte`, `blend`, `effects`, `masks`, `motionBlur`, `origin`, `align`, `collapse`, … apply to the instance as a whole |

Normalization makes a comp `<id>.comp` (`<host>.<id>.comp` when nested under another generated comp) from the definition with every `$props` replaced, its layout resolved and timeline compiled, and a **collapsed** comp layer with the instance's id (`collapse: false` renders it as a flat precomp). `out` defaults to `in + duration` of the generated comp: an instance disappears when its own animation ends (set `out` to hold it; past the generated comp's end it shows transparent, `hold: none`). With `duration: "parent"` the instance's `out` sets the comp's duration. Each instance gets its own comp (the renderer's cache deduplicates). Nesting depth ≤ 4 (`component.depth`); `component.cycle` on recursion. `motion.check` returns the resolved library versions in `stats.library`. Canonical form keeps `use` and `props` under `x-component` on the comp layer.

### 3.4 Slots

A `slot` layer (`{ "id": "art", "type": "slot", "slot": "art", … }`) in a definition is replaced by a comp layer showing a generated comp `<instance>.slot.<name>` holding the instance-supplied layers, sized to the slot's `size` and fitted with `fit`. An empty slot renders nothing unless `required: true`. The slot layer accepts the common layer fields (`in`, `out`, `transform`, `parent`, `masks`, `effects`, `matte`, `blend`, `motionBlur`, `origin`, `align`), so the component can fade, mask or matte whatever was supplied, and the timeline can target the slot by id. A nested instance fills its slots from the definition or forwards an outer slot: `"slots": { "screen": "$slots.screen" }` (valid only inside a definition that declares that slot). The library's `transition.*` components take two slots `a` (outgoing) and `b` (incoming).

## 4. Repeat

```jsonc
{ "id": "bars", "type": "repeat", "data": "$data.sales", "ids": "{{$item.label | lower}}",
  "layer": { "type": "shape",
    "contents": [ { "type": "rect", "size": [80, "{{$item.value * 12}}"] }, { "type": "fill", "color": "$theme.color.palette.$index" } ],
    "origin": "bottom", "transform": { "position": ["{{340 + $index * 120}}", 900] } } }
{ "id": "dots", "type": "repeat", "count": 12, "layout": { "type": "radial", "radius": 300, "center": ["50%", "50%"] }, "layer": { "type": "shape", "shape": "circle", "radius": 12, "fill": "#FFF" } }
```

| Field | Notes |
|---|---|
| `data` | a list or a reference to one (exactly one of `data` / `count`; `repeat.data_not_list`) |
| `count` | an integer or reference: indexes `0 … count−1` |
| `layer` | the template (no `id`); any value may use `$item`, `$item.<path>`, `$index`, `$count`, `$parent.item`, `$parent.index` |
| `layout` | places the generated layers (§5); the template's `position` is then ignored |
| `ids` | a template naming the copies (`bars.jan`) instead of `bars.0`; must be unique and valid (`repeat.id_template`) |

Copies replace the repeat entry in place (paint order; the first item at the bottom), ≤ 1,000 per repeat and 10,000 per document (`limit.repeat`), nesting ≤ 4 (the inner template sees the outer repeat as `$parent.*`). Tweens target `"bars.*"` (a tween inside the template is not allowed: timeline entries live in the comp). Expressions in copies read `index` and `thisLayer.repeatIndex`. Data bindings: `points` from a list on `polyline`/`path` items ([07](07-shapes.md) §8.4) and `keys` from a list on any animatable property ([04](04-presets-and-drivers.md) §5).

Scope references work as path segments as well as in `{{ }}` placeholders: `$theme.color.palette.$index`, `$theme.color.palette.$parent.index`, `$data.rows.$item.row` (`$item` takes the one field after it when the item is an object; `$parent.item.<field>` likewise), or bracketed for anything longer (`$data.rows[$item.pos.row]`).

## 5. Layout

Resolved once at normalization against measured content bounds into plain `position` values (no per-frame layout; animated layout between two states is P3, not built: write the target positions as tweens). On a `repeat` (places its copies), a component (`children`, or all layers), or a comp.

```jsonc
"layout": { "type": "stack", "direction": "row", "gap": 24, "align": "center", "justify": "center", "padding": [0, 0], "wrap": false, "children": ["a", "b", "c"], "box": ["10%", "40%", "80%", "20%"] }
"layout": { "type": "grid", "columns": 4, "gap": [24, 24], "cell": "auto", "align": "center" }
"layout": { "type": "radial", "radius": 360, "startAngle": -90, "sweep": 360, "center": ["50%", "50%"], "orient": false }
"layout": { "type": "path", "path": "guide", "spacing": "even", "orient": true }
```

| Type | Fields (defaults) | Places items |
|---|---|---|
| `stack` | `direction` (`row` \| `column`), `gap` (0), `align` cross-axis (`center`: `start`, `center`, `end`, `baseline`), `justify` main-axis (`start`: `start`, `center`, `end`, `space-between`, `space-around`), `padding` (`[x, y]`), `wrap` (false), `children`, `box` (`[x, y, w, h]`; default the comp, or the component's `size` inside a definition) | one after another (Figma auto-layout) |
| `grid` | `columns` (required) or `rows`, `gap` (`[gx, gy]`), `cell` (`"auto"` = the largest item, or `[w, h]`), `align` within cells, `box` | row-major cells |
| `radial` | `radius`, `startAngle` (−90 = top), `sweep` (360), `center`, `orient` (false: rotate items to face outwards) | evenly around an arc |
| `path` | `path` (a shape layer id or a path value), `spacing` (`even` by arc length, or px), `orient` (follow the tangent) | along a path |

Items are positioned by their anchor at the bounds point named by `align` (or their own `origin`). `gap`, `padding` and sizes accept `$theme.space.<n>` and percentages of the box. Items exceeding the box: `layout.overflow` (warning); inconsistent fields: `layout.invalid`.

## 6. Examples

`examples/13-theme-data.json`: an inline theme with every token group, `override` over a library theme, every colour modifier, every derived token, `data` with every template format and the whole placeholder grammar (arithmetic, comparisons, `sum`/`count`/`max`/`atan2`/`sqrt`/`clamp`/`lerp`, null-safe indexes with `default`), a `countUp` with a format. `examples/13-components-repeat-layout.json`: a local component with every param type, a slot, template-able `enabled`, `duration: "parent"`, a nested instance forwarding a slot, instances with `props`/`slots`/`align`, a data-driven `repeat` with `ids` and nested repeats, and every layout type. Both check with 0 errors.
