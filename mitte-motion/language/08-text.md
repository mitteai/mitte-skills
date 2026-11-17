# 08. Text: the text value, character and paragraph style, fonts, text on a path, animators and selectors, 3D per character, captions

Scope: spec 5 in full (fonts in the pack, styles, animators and every selector, text on a path, box text, overflow, emoji, source-text animation, `words` captions, measuring). Generated tables: `TextValue`, `Span`, `CharStyle`, `Font`, `FontToken`, `TextStrokeObject`, `StrokeOrder`, `Kerning`, `Paragraph`, `TextAlign`, `VerticalAlign`, `TextDirection`, `Overflow`, `TextPath`, `TextPathSource`, `Animator`, `Selector`, `SelectorBy`, `SelectorMode`, `RangeShape`, `RangeUnits`, `StaggerDirection`, `Grouping`, `AnchorGrouping`, `Words`, `Word`, `WordStyle`, `Paging` in `92-schema-types-*.md`.

```jsonc
{ "id": "title", "type": "text",
  "text": "Ship faster in 2027",
  "style": { "font": "Inter", "weight": 700, "size": 120, "tracking": -20, "fill": "#FFFFFF" },
  "paragraph": { "align": "center" },
  "box": [880, 400],                       // box text; absent = point text
  "path": { … }, "animators": [ … ], "grouping": { … }, "threeDPerChar": false,
  "origin": "center", "position": ["50%", "45%"] }
```

| Field | Type | Default | Animatable | Notes |
|---|---|---|---|---|
| `text` | string or spans | `""` | hold only | §1 (After Effects Source Text) |
| `style` | character style | §2 defaults | per property | applies to the whole text; spans override |
| `paragraph` | paragraph style | §3 defaults | per property | |
| `box` | `[w, h]` | none (point text) | yes | box text wraps within `w`; animatable (reflow per frame) |
| `path` | object | none | partly | text on a path (§5) |
| `animators` | list | `[]` | — | §6 |
| `grouping` | `{ anchorGrouping, alignment }` | `char`, `[0, 0]` | — | §6.5 |
| `threeDPerChar` | boolean | `false` | no | per-character 3D; needs `threeD: true` (`layer.field_not_allowed`) |
| `words`, `wordStyle`, `paging` | caption sugar | — | — | §8, authored only |

The layer origin (0, 0) is the **left end of the first baseline** for left-aligned point text, its centre for centred text, its right end for right-aligned text; box text's origin is the box's top-left. `origin: "center"` or `"baseline"` measures the ink bounds for you ([05](05-layers.md) §5).

## 1. The text value

```jsonc
"text": "Hello world"
"text": [ { "text": "Revenue up " }, { "text": "38%", "id": "num", "style": { "weight": 800, "fill": "$theme.color.accent" } },
          { "text": "\nyear over year", "style": { "size": 64, "fill": "#FFFFFFB3" } } ]
"text": "Q{{$data.quarter}} revenue: {{$data.revenue | currency:USD:0}}"
"text": { "keys": [ { "t": 0, "v": "Plan" }, { "t": 1, "v": "Build" }, { "t": 2, "v": "Ship" } ] }    // hold keys switch the text
"text": { "value": "0", "expr": "Math.round(linear(time, 0, 2, 0, 1250)).toLocaleString()" }       // an expression returning a string
```

| Form | Meaning |
|---|---|
| string | one run in the layer's `style`; `\n` (or `\r\n`) is a hard line break; U+2028 a line break without paragraph spacing; a tab advances to the next tab stop (`paragraph.tabSize × size` px) |
| array of spans | each span: `text` (required), `style` (partial character style merged over the layer's), `id` (makes the span targetable: `"title/span:num"`, `fitTo.span`) |

Text is NFC-normalized; every character count (units, `textIndex`, `maxChars`) counts **grapheme clusters**. Words are UAX 29 words with punctuation attached to the preceding word, one word per CJK ideograph, and whitespace as gaps that follow the preceding word. A text value is never read as a number (`"42%"` is three characters; `countUp` counts the `42`). ≤ 10,000 characters per layer (`text.too_long`). Non-animatable style fields (font, italic, features) change through source-text keys with span arrays.

## 2. Character style

| Field | Type | Default | Anim. | Notes |
|---|---|---|---|---|
| `font` | family name or font token `{ family, weight?, style?, tracking?, axes? }` | `$theme.font.body` (Inter 500 in the default theme) | no | a token's fields become defaults the style's own fields override; matching is case-insensitive, ignoring spaces and hyphens |
| `weight` | 1–1000 | `400` | yes | variable fonts animate smoothly; static fonts snap to the nearest face (hold). `weight` and `axes.wght` are one property (both is an error) |
| `italic` | boolean | `false` | no | the italic face, or the `ital`/`slnt` axis |
| `size` | px (em size) | `$theme.type.size.0` (≈ 45 px at 1080p) | yes | |
| `leading` | px or `"auto"` | `"auto"` (1.2 × size) | yes | baseline to baseline |
| `tracking` | thousandths of an em | `0` | yes | after **every** character including the last; the trailing advance counts toward the line width, so animated tracking shifts centred text left by half the growth |
| `kerning` | `metrics` \| `optical` \| `none` | `metrics` | no | `optical` (After Effects "Optical") is treated as `metrics` today |
| `fill` | colour, gradient, or `null` | `#FFFFFF` | yes | `null` = no fill; a gradient spans the layer's bounds unless its points are given |
| `stroke` | `{ color, width (px, animatable), join: miter \| round \| bevel, order: fillOverStroke \| strokeOverFill \| allFillsOverAllStrokes \| allStrokesOverAllFills }` or `null` | `null` | partly | After Effects' four stroke orders |
| `allCaps`, `smallCaps`, `superscript`, `subscript`, `underline`, `strike` | boolean | `false` | no | small caps via `smcp` (synthesized at 70 % when absent); sup/sub via `sups`/`subs`; underline and strike from the font's metrics |
| `baselineShift` | px | `0` | yes | up positive |
| `horizontalScale`, `verticalScale` | percent | `100` | yes | |
| `fontFeatures` | map tag → integer | `{}` | no | `{ "tnum": 1, "ss01": 1, "liga": 0 }`; `tnum` keeps counters from jittering |
| `axes` | map tag → number | `{}` | yes (each) | variable axes (`wght`, `wdth`, `slnt`, `ital`, `opsz`, custom), ≤ 16; clamped to the font's range; a tag the font lacks is the info `font.axis_missing` |
| `opticalSize` | `auto` or number | `auto` | no | `auto` sets `opsz` to the size when the font has the axis |
| `language` | BCP-47 | `en` | no | shaping (localized forms) and line breaking |

Every animatable field animates per layer (keys on `style.size`) and per character through animators (§6).

## 3. Paragraph and layout

| Field | Default | Values / notes |
|---|---|---|
| `align` | `left` | `left`, `center`, `right`, `justify`, `justifyLastLeft`, `justifyLastCenter`, `justifyLastRight`, `justifyAll`, `start`, `end` (resolved per paragraph by its base direction). Justify modes apply to box text only; on point text the info `lint.paragraph_needs_box` |
| `verticalAlign` | `top` | `top`, `center`, `bottom` (box text) |
| `spaceBefore`, `spaceAfter` | `0` | px between paragraphs |
| `indent` | `0` | px on the start side |
| `firstLineIndent` | `0` | px, may be negative (hanging) |
| `direction` | `auto` | `auto` (UAX 9 from the first strong character), `ltr`, `rtl`; bidi reordering is implemented |
| `overflow` | `visible` | `visible`, `clip` (hide lines beyond the box), `shrink` (reduce `size` and leading in 0.5 px steps until the text fits, down to `minSize`); box text only |
| `minSize` | `8` | px, for `shrink` |
| `maxLines` | none | truncate after this many lines |
| `ellipsis` | `false` | add `…` to the last visible line when truncated |
| `hyphenate` | `false` | **accepted, no effect** (no hyphenation pass in engine 0.1.48) |
| `balance` | `false` | **accepted, no effect** (no line balancing) |
| `tabSize` | `2` | tab stops every `tabSize × size` px |

Point text (no `box`) breaks only at hard breaks; alignment is relative to the origin. Box text wraps within `w` (UAX 14 with the `language`'s rules); the box is not a clip unless `overflow: "clip"`. Vertical writing is not accepted. Shaping: HarfRust per run (bidi level, script, font, style), Parley layout, Arabic/Hebrew/Indic/Thai/CJK/emoji shape correctly; a variable axis animated with keys reshapes at 1/64-unit quantization.

**Emoji** render from the bundled Noto Color Emoji (COLRv1, vector): solid and gradient paint layers rasterized like outlines, so they scale and animate per character. A colour glyph paints its own layers: `fill`/`stroke` do not apply to it; the unit's opacity, clip and blur do. Bitmap emoji in a font asset are resampled (`lint.bitmap_emoji_scaled` above 150 %).

## 4. Fonts

Families are referenced by name from the bundled pack (no asset needed) or from a `font` asset ([01](01-document.md) §6: `type: "font"`, `fontFamily`, `index`; TTF, OTF, WOFF, WOFF2, TTC). Resolution: family lookup (assets first, then the pack; case-insensitive, spaces and hyphens ignored) → face by `weight`, `italic`, width (CSS Fonts 4 matching; variable families set axes) → a missing family is `font.not_found` (the hint lists the five nearest names; never a silent fallback) → per-grapheme fallback for uncovered characters: other faces of the family → the theme's `font.fallback` list → Noto Sans for the script → Noto Color Emoji → Noto Sans Symbols 2 (`font.fallback_used` warning; `font.missing_glyphs` when nothing covers them) → a pack family whose files are missing on a box lays out with estimated metrics and an info. No system fonts, ever.

| Category | Families |
|---|---|
| Neutral sans | Inter, Inter Display, Manrope, DM Sans, Plus Jakarta Sans, Figtree, Onest, Geist, Public Sans, IBM Plex Sans, Source Sans 3, Work Sans, Noto Sans |
| Geometric sans | Poppins, Montserrat, Outfit, Urbanist, Lexend, Sora, Red Hat Display, Albert Sans |
| Grotesque / display sans | Space Grotesk, Bricolage Grotesque, Archivo, Familjen Grotesk, Schibsted Grotesk, Hanken Grotesk, Unbounded, Syne |
| Condensed / impact | Anton, Bebas Neue, Oswald, Barlow Condensed, Archivo Narrow, League Gothic, Big Shoulders Display |
| Serif | Playfair Display, Instrument Serif, Fraunces, DM Serif Display, Libre Caslon Text, Cormorant, EB Garamond, Lora, Source Serif 4, Newsreader, Noto Serif |
| Rounded | Nunito, Quicksand, Fredoka, Baloo 2, M PLUS Rounded 1c |
| Display / expressive | Rubik, Righteous, Bungee, Monoton, Rubik Mono One, Shrikhand, Abril Fatface |
| Handwritten / script | Caveat, Kalam, Permanent Marker, Dancing Script, Pacifico, Homemade Apple |
| Monospace | JetBrains Mono, IBM Plex Mono, Space Mono, Fira Code, DM Mono, Geist Mono |
| Script fallback | Noto Sans Arabic, Noto Naskh Arabic, Noto Sans Hebrew, Noto Sans Devanagari, Noto Sans Bengali, Noto Sans Tamil, Noto Sans Thai, Noto Sans Georgian, Noto Sans Armenian, Noto Sans Ethiopic, Noto Sans JP, Noto Sans KR, Noto Sans SC, Noto Sans TC, Noto Serif JP |
| Emoji and symbols | Noto Color Emoji (COLRv1), Noto Sans Symbols 2, Noto Sans Math |

Variable axes depend on the family: `wght` on most; `opsz` and `SOFT` on Fraunces; `wdth` on Bricolage Grotesque; no pack family has `slnt`. The exact pack (version hash) is reported by `motion.check` and `rexx-engine version`.

## 5. Text on a path

```jsonc
"path": { "source": { "mask": "curve" }, "firstMargin": 0, "lastMargin": 0, "perpendicular": true, "forceAlign": false, "reverse": false }
"path": { "source": { "shape": "ribbon.contents.spine" } }
"path": { "source": { "v": [[0, 0], [300, -120], [600, 0]], "in": [[0, 0], [-80, 0], [0, 0]], "out": [[0, 0], [80, 0], [0, 0]] } }
```

| Field | Type | Default | Anim. | Notes |
|---|---|---|---|---|
| `source` | `{ "mask": id }`, `{ "shape": "layer.contents.item" }`, or a path value | required | the source path animates | a `none`-mode mask on this layer (After Effects' way), a path item of a shape layer in the same comp (converted into the text layer's space once at the measure time, stored as a mask; an animated source or transform is sampled per frame into linear path keys), or an inline path; missing: `text.path_invalid` |
| `firstMargin`, `lastMargin` | px | `0` | yes | where text starts / ends along the path; animate `firstMargin` to slide text |
| `perpendicular` | boolean | `true` | no | rotate each character to the tangent |
| `forceAlign` | boolean | `false` | no | spread characters between the margins |
| `reverse` | boolean | `false` | no | run backwards (text flips to the other side) |

Characters advance by arc length and sit by their baseline centre; paragraph alignment applies along the path. Box text on a path is `text.path_box`.

## 6. Animators

An animator holds property values; its selectors decide how strongly each unit (character, word, line) receives them. Tweens on `title/chars` compile to animators with a `stagger` selector ([03](03-timeline-and-tweens.md) §5).

```jsonc
"animators": [{ "id": "wave", "props": { "position": [0, -30], "fill": "#FFD166" },
  "selectors": [{ "type": "range", "by": "chars", "shape": "triangle", "start": 0, "end": 30,
                  "offset": { "value": 0, "oscillate": { "freq": 0.5, "amp": 100, "wave": "saw" } } }] }]
```

### 6.1 Animator properties

**Offset** properties add `value · a`; **target** properties blend from the unit's base toward `value` by *a*; the one **replace** property applies when *a* > 0.5; *a* is the combined selector amount in [−1, 1]. All are animatable.

| Prop | Kind | Unit / notes |
|---|---|---|
| `anchor`, `position` | offset | px, unit space (3D with `threeDPerChar`) |
| `scale` | target | percent: unit scale = 100 + (value − 100)·a |
| `skew`, `skewAxis`, `rotation` (= `rotationZ`) | offset | degrees |
| `rotationX`, `rotationY` | offset | degrees; only with `threeDPerChar`, else ignored with a `layer.field_not_allowed` warning |
| `opacity`, `fillOpacity`, `strokeOpacity` | target | percent (an animator with `opacity: 0` hides fully selected units) |
| `fill`, `stroke` | target | colour, mixed in the interpolation space (*a* clamped to [0, 1]) |
| `fillHue`, `fillSaturation`, `fillBrightness` | offset | degrees / percent |
| `strokeWidth` | offset | px |
| `tracking` | offset | thousandths of an em (changes layout) |
| `trackingType` | switch | `beforeAndAfter`, `before`, `after` |
| `lineAnchor` | offset | percent 0–100: alignment of tracking within a line |
| `lineSpacing` | offset | px added between lines |
| `characterOffset` | offset (rounded per animator, summed) | code points, within `characterRange` (scramble/decode effects) |
| `characterRange` | switch | `preserveCase` (default), `full`, `{ "set": "A-Z0-9" }` (literals plus `a-b` ranges, ≤ 4,096 characters) |
| `characterValue` | replace | a code point every selected character becomes |
| `blur` | offset | px per unit (a Gaussian on the unit's own glyphs, σ = value/3) |
| `clip` | offset | `{ top, bottom, left, right }` percent of the unit's bounds hidden from each edge (what `maskReveal` on units compiles to); rendered since engine 0.1.13 |
| `axes.<tag>`, `weight` (= `axes.wght`) | offset | axis units |

An unknown prop is `doc.unknown_field` with the nearest animator properties as the hint. All animators apply in array order; offsets sum, targets apply in order. Layout-affecting props (`tracking`, `trackingType`, `lineAnchor`, `lineSpacing`, `characterOffset`, `characterValue`) run in a first pass before layout; the transform and appearance props in a second pass over the new layout.

### 6.2 Selectors and modes

Selectors combine in order by `mode` (the first selector's mode is ignored): `add` min(1, a+s), `subtract` max(0, a−s), `intersect` a·s (default), `min`, `max`, `difference` |a−s|. An animator with no selectors applies to all units at amount 1.

**Range** (After Effects' area model: a unit's amount is the average of the shape over its share of the 0–100 % axis, so animated edges produce soft partial selections)

| Field | Default | Anim. | Notes |
|---|---|---|---|
| `by` | `chars` | no | `chars`, `charsExcludingSpaces`, `words`, `lines` |
| `units` | `percent` | no | `percent` or `index` (an index past the unit count is the warning `text.unit_out_of_range`) |
| `start`, `end`, `offset` | `0`, `100` (or the unit count), `0` | yes | `offset` is added to both; the usual thing to animate for cascades |
| `amount` | `100` | yes | percent, −100–100 |
| `shape` | `square` | no | `square`, `rampUp`, `rampDown`, `triangle`, `round`, `smooth` |
| `smoothness` | `100` | yes | `square` only: each interior edge becomes a ramp `smoothness % × one unit` wide |
| `easeHigh`, `easeLow` | `0` | yes | −100–100 power curves on the ramps near 1 / near 0 |
| `randomizeOrder` | `false` | no | units take random positions in the range |
| `seed` | `0` | no | used as it is |

**Wiggly**: `by`, `maxAmount` (100) A, `minAmount` (−100) A, `wigglesPerSecond` (2) A, `correlation` (50) A (percent of a shared noise stream; 100 moves all units together), `temporalPhase`, `spatialPhase` (0, degrees) A, `lockDimensions` (false: the same random value for every dimension of a vector), `seed` (0, combined with layer and animator id), `mode`.

**Expression**: `by`, `amount`: an expression evaluated per unit with `textIndex` (1-based), `textTotal`, `selectorValue` (percent from the previous selectors, a scalar) bound, returning percent (or a vector per axis); a runtime error warns at the selector and reads 0 (a budget overrun still fails the frame). Example: `"amount": "ease(time, textIndex * 0.05, textIndex * 0.05 + 0.5, 100, 0)"`.

**Stagger** (this spec's canonical extension: an exact per-unit timing curve)

| Field | Default | Notes |
|---|---|---|
| `by` | `chars` | `chars`, `words`, `lines` |
| `skipSpaces` | `false` | whitespace gets no slot (it follows the preceding unit's amount) |
| `start` | `0` | layer time of the first unit's start |
| `each` or `amount` | required | delay per unit in stagger order, or the total spread ([03](03-timeline-and-tweens.md) §6 semantics) |
| `dur` | `0` | each unit's transition length (0 = a switch) |
| `ease` | `linear` | any ease, springs and curves included; may overshoot (amounts beyond 0–100 %) |
| `direction` | `in` | `in`: 0 → 100 % over the unit's window (values arrive); `out`: 100 → 0 % (values release) |
| `from` | `start` | `start`, `end`, `center`, `edges`, `random`, an index |
| `distribution` | `linear` | the ease that distributes start times |
| `seed` | `0` | for `random` |
| `mode` | `intersect` | |

Unit *k* starts at `start + distribution(d_k/d_max)·d_max·each`; at layer time *t*: `u = clamp((t − s_k)/dur, 0, 1)`, `p = ease(u)`, amount = `p` (`in`) or `1 − p` (`out`).

### 6.3 Grouping and anchors

`"grouping": { "anchorGrouping": "char" | "word" | "line" | "all", "alignment": [x%, y%] }`: the pivot units rotate and scale around (each character, word centre, line, or the whole block) and its offset from each group's baseline centre in percent of the group's size (`[0, -50]` pivots on the visual centre).

### 6.4 Per-character 3D

`threeDPerChar: true` on a 3D text layer: each unit is a 3D card (z in `position`, `rotationX`/`rotationY`, intersections, shadows, depth of field). Each card runs the layer's masks and effects at its rest pose in layer space, then the layer's and the unit's transforms place it.

### 6.5 Unit addressing

`title/chars`, `title/chars!` (skip whitespace), `title/words`, `title/lines`, `title/span:price`, `title/span:price/chars`. Ligatures are disabled (`liga: 0`, `clig: 0`) when an animator treats a ligature's characters differently (`lint.ligatures_disabled`); Arabic is never split per character (per-character animation applies to whole words, with a warning).

## 7. Source-text animation and the text presets

`text` keys are hold keys; `expr` may return a string. Compile targets: `typeOn`/`typeOff` → an `opacity: 0` animator with an index-unit `range` selector keyed 0 → *n* over *n/cps* seconds (optional cursor: a blinking rect shape layer placed by expression); `scrambleIn`/`scrambleOut` → a `wiggly` selector on `characterOffset` (with `characterRange.set` from `chars`) under a keyed index `range`, plus an opacity animator; `countUp` → `text: { "value": "", "expr": "formatNumber(…)" }` with `tnum`; `trackIn` → keys on `style.tracking`; `highlight`/`underline` → shape layers with `fitTo` (optionally on a span) animated with `growIn`.

## 8. Captions on a text layer

```jsonc
{ "id": "cap", "type": "text",
  "words": [ { "text": "This", "start": 0.00, "end": 0.18 }, { "text": "changes", "start": 0.18, "end": 0.53 }, { "text": "everything", "start": 0.53, "end": 1.13 } ],
  "wordStyle": { "active": { "fill": "$theme.color.accent", "scale": 112 }, "past": { "opacity": 100 }, "future": { "opacity": 35 } },
  "paging": { "maxWords": 3, "maxChars": 18 } }
```

`words` (authored only) is the one word-timing shape (`{ text, start, end }` in seconds, [11](11-media-and-audio.md) §9). It builds the text per page (hold keys on `text` at each page's first word; pages of at most `maxWords` words or `maxChars` characters) and three animators per page (`_wordsPast`, `_wordsActive`, `_wordsFuture`: the `wordStyle` props under word-indexed `range` selectors keyed to the word times; a gap keeps the previous word active). The `caption.*` library components carry typesetting, placement and emoji on top of this.

## 9. Measuring

Glyph box (default; After Effects `sourceRectAtTime(t, false)`): each line from its tallest ascender to the last baseline plus descender, across the advance widths. With extents (`includeExtents`): the glyph outlines plus stroke width and animator offsets. Ink box: the tight outline union (lint contrast and collision). Static placement bakes measured numbers at normalization (a canonical document edited to another font keeps the old numbers); live placement and `fitTo` re-measure per frame.

## 10. Examples

`examples/08-text.json`: spans with ids, every character-style field, every paragraph field on box text (`shrink`, `maxLines`, `ellipsis`, `justify`), a variable axis animated, `fontFeatures`, text on a mask path and on a shape path, animators with every property kind and every selector type (`range` with each shape, `wiggly`, `expression`, `stagger`), `grouping`, source-text keys, and a `words` caption layer. Checks with 0 errors; expected warnings: `font.fallback_used` (the emoji falls back to Noto Color Emoji), `lint.text_too_short_on_screen` on the long box paragraph, and `lint.stagger_too_fast` on the span tween written without a `stagger` (all units of the span start together).
