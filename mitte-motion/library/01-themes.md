# Themes: the theme object, every token, derived tokens, modifiers, brand kits, the ten themes

A theme is a set of named tokens. Any value in a document may be a token reference `$theme.<path>`; presets, library components and text defaults read tokens, so one theme gives a whole document one color and motion language. A theme is **always** in effect: with no `theme` field the engine uses `mitte/default@1`. Source: `engine/crates/rexx-normalize/src/passes/theme.rs` (pass 5), `refs.rs` (resolution), `passes/defaults.rs` (textures), the theme files under `library/mitte/themes/`, spec 12 §12.1.

## The theme object

```json
{ "theme": {
    "use": "mitte/clean@1",
    "brand": { "asset": "brandKit" },
    "override": { "color": { "accent": "#FF4D00" }, "font": { "display": { "family": "Space Grotesk", "weight": 700, "tracking": -20 } } } } }
```

| Field | Type | Notes |
|---|---|---|
| `use` | library reference (theme kind) | `mitte/<name>@1`. Unknown name: `ref.library_unknown`; unknown version: `ref.library_version`. |
| `brand` | `{ "asset": "<data asset id>" }` | A JSON `data` asset holding a partial theme (any of the ten groups). Merged between `use` and `override`. If the asset is not available at check time the engine reports `asset.unmaterialized` (info) and skips it; an unreadable or non-JSON kit is `asset.data_invalid` (error). |
| `override` | partial theme | Deep-merged last. |
| any token group written directly (`color`, `font`, …) | partial theme | An inline theme. It is **also deep-merged over the default theme**, not a replacement: an inline theme with only `color.accent` keeps every other default token. Inline groups merge after `override`. |

Unknown keys anywhere in a theme object are `doc.unknown_field` ("Valid fields: color, font, type, space, radius, motion, ease, spring, texture, styles"). Merge order, each step a deep merge (objects merge, arrays such as `palette` and `space.scale` replace): built-in default → the library's `mitte/default@1` → `use` → `brand` kit → `override` → inline groups. A theme may refer to its own tokens with `$theme.…` (`"surface": "$theme.color.bg.darker"`); these resolve in one pass against the merged result, without recursion.

Validation after the merge (`theme.invalid`): every `color.*` token (or every element of a color list) must parse as a color ("The color token "accent" is not a color: "blueish"." hint "Use a hex, rgb(), oklch(), or named color."); every `ease.*` token must be a catalogue ease (reported as `anim.ease_unknown`, "Ease "wobbly" is not in the catalog."); every `font.*` token must be an object with `family` (the schema already requires it: `doc.required` "Required field "family" is missing").

An inline `font.body` token (`"theme": { "font": { "body": { … } } }`, no `use`) is a font like any other token: the validator reads the theme's groups as token maps, so a font named `body` (or `pre`, `sim`) is never mistaken for a bake reference.

## Token groups and every token

Defaults are `mitte/default@1` (identical to the engine's built-in copy). Every group is optional in an override or brand kit.

| Group | Token | Type | Default | Used by |
|---|---|---|---|---|
| `color` | `bg` | color | `#0B0B0F` | comp backgrounds (`"background": "$theme.color.bg"`), plates in library components |
| | `fg` | color | `#F5F5F7` | primary text |
| | `accent` | color | `#7C5CFF` | highlights, bars, underlines, the active caption word, buttons |
| | `muted` | color | `#8A8A99` | secondary text, roles, chart captions |
| | `surface` | color | `#16161D` | cards, lower-third plates, pills |
| | `line` | color | `#2A2A35` | dividers, chart grid, progress tracks |
| | `palette` | list of colors (5 in every library theme; any length) | `["#7C5CFF", "#22D3EE", "#F472B6", "#FACC15", "#34D399"]` | charts, repeat items: `$theme.color.palette.<i>` wraps (`palette.7` is `palette.2` with five colors), `$theme.color.palette.$index` inside a repeat |
| | `positive`, `negative`, `warning` | color | `#34D399`, `#F87171`, `#FACC15` | deltas, LIVE labels, toasts |
| `font` | `display`, `body`, `mono` | font token `{ family, weight, style?, tracking?, axes? }` | Inter 800 tracking −20 / Inter 500 / JetBrains Mono 500 | `"font": "$theme.font.display"` in a text style: `family` becomes the font and the other fields become style defaults that the style's own `weight`, `tracking`, `axes` override. `family` must be a pack family or a document font asset's `fontFamily` (`09-sound-fonts.md`) |
| `type` | `base` | fraction of the comp's shorter side | `0.042` (45.4 px at 1080) | `$theme.type.size.<n>` |
| | `ratio` | number | `1.333` | the modular scale |
| | `lineHeight` | number | `1.15` | default leading in library components |
| `space` | `unit` | fraction of the shorter side | `0.0125` (13.5 px at 1080) | `$theme.space.<n>` |
| | `scale` | list of numbers | `[0, 1, 2, 3, 4, 6, 8, 12, 16, 24]` | index n of `$theme.space.<n>`; identical in all ten themes |
| `radius` | `s`, `m`, `l`, `pill` | pixels | `8`, `16`, `32`, `9999` | rounded rectangles (`"radius": "$theme.radius.m"`) |
| `motion.dur` | `xs`, `s`, `base`, `l`, `xl` | seconds | `0.15`, `0.3`, `0.5`, `0.8`, `1.2` | preset and tween durations |
| | `transition` | seconds | `0.5` | default `dur` of layer and scene transitions and of the library transition components |
| `motion.stagger` | `tight`, `base`, `loose` | seconds | `0.02`, `0.05`, `0.1` | `"stagger": "$theme.motion.stagger.base"` |
| `ease` | `default` | ease | `power2.out` | tweens that give no ease |
| | `enter` | ease | `expo.out` | enter presets |
| | `exit` | ease | `power2.in` | exit presets |
| | `move` | ease | `[0.2, 0, 0, 1]` | position changes between two on-screen states; `ui.cursor` moves |
| | `emphasis` | ease | `back.out(1.7)` | emphasis presets, pops |
| | `linear` | ease | `linear` (`steps(8)` in `mono`, `steps(12)` in `retro`) | continuous loops |
| | `transition` | ease | `power3.inOut` | layer and scene transitions |
| `spring` | `gentle`, `snappy`, `bouncy` | `{ bounce, duration }` (bounce −1…1, duration > 0) or `{ stiffness, damping, mass }` | `{0, 0.5}`, `{0.15, 0.35}`, `{0.3, 0.6}` | `"ease": "$theme.spring.snappy"` on a tween or preset use; the canonical key carries the spring object as its ease (`{ "ease": { "spring": { "bounce": 0.25, "duration": 0.55 } } }`) |
| `texture` | `grain` | 0–1 | `0` | when > 0 the normalizer appends an adjustment layer `_texture` on top of the root comp with `stylize.grain` (`amount` = grain × 100, `size` = `grainSize`) |
| | `grainSize` | px | `1` | the grain's `size` |
| | `vignette` | 0–1 | `0` | when > 0, `stylize.vignette` with `amount` = −vignette on the same `_texture` layer |
| | `halftone`, `halftoneSize` | 0–1, px | 0, 6 | when `halftone` > 0, a CMYK `stylize.halftone` (`cellSize` = `halftoneSize`, `blend` = halftone × 100) goes first on the same `_texture` layer, under grain and vignette; `retro` sets 0.18 at 7 px |
| `styles` | `<name>` | a layer-styles object | none | `"styles": "$theme.styles.card"` on a layer: the token holds a **whole** styles object (`{ "dropShadow": { … } }`) and is referenced for the whole `styles` field. `clean` and `soft` ship `styles.dropShadow` that way (`"styles": "$theme.styles.dropShadow"`). A token that is not a styles object is `theme.invalid` at `/theme/styles/<name>` (an authored theme is schema-checked first: `doc.unknown_field`) |

The `_texture` layer is added to every comp that is rendered as a root (the main comp; a variant inherits it), spans the comp's whole duration, and is a full-frame effect on every frame: four library themes set a texture (`midnight`, `editorial`, `neon`, `retro`), which is why their descriptions mention cost.

## Derived tokens and modifiers

| Reference | Value | Verified |
|---|---|---|
| `$theme.type.size.<n>` | `base · ratio^n · shorterSide`, rounded to 0.5 px. Negative steps are written `size.-1`, `size.-2`. | `clean` at 1080p: `size.0` = 43 px, `size.5` = 131.5, `size.8` = 257.5, `size.-2` = 27.5; `default`: `size.0` ≈ 45.5, `size.4` ≈ 143, `size.6` ≈ 254. The engine accepts any integer n (spec says −2…8; `size.9` resolves to 322 px under `clean`). |
| `$theme.space.<n>` | `unit · scale[n] · shorterSide` | `space.3` = 40.5 px, `space.9` = 324 px at 1080p. An index past the scale is `ref.unresolved`. |
| `$theme.color.palette.<i>` | `palette[i mod len]` | `palette.7` = `palette.2` |
| `<color ref>.a10` … `.a90` | the color with alpha 0.10 … 0.90 (tens only: `.a5`, `.a95`, `.a150` are `ref.unresolved`, "not a field or a color modifier (a10…a90, lighter, darker, on)") | `accent.a40` → `{ r, g, b, a: 0.4 }` |
| `<color ref>.lighter`, `.darker` | ±12 % OKLab lightness | |
| `<color ref>.on` | black or white, whichever contrasts more | `clean` `accent.on` = white, `bg.on` = black |
| modifiers on `$props.<color>`, `$item.<color>`, `$data.<color>` | the same (any color-typed reference) | used by library components (`$props.color.a20`) |

A modifier on a non-color (`$theme.motion.dur.base.on`) and any unknown path (`$theme.color.nope`, `$theme.colour.accent`) is `ref.unresolved` ("Reference "$theme.color.nope" does not resolve (no field "nope").", at the referencing field). Tokens resolve once at normalization; animate the property, never the token.

## Brand kits

```json
{ "assets": { "brandKit": { "src": "https://media.mitte.ai/u/p0/brand-kit.json", "type": "data" } },
  "theme": { "use": "mitte/clean@1", "brand": { "asset": "brandKit" }, "override": { "color": { "muted": "#5B6472" } } } }
```

The kit file is a partial theme: `{ "color": { "accent": "#00875A", "palette": [ … ] }, "font": { "display": { "family": "Space Grotesk", "weight": 700, "tracking": -15 } }, "motion": { "dur": { "base": 0.4 } } }`. Verified: the kit's `accent` and `palette` replace the theme's (arrays replace whole), `font.display` deep-merges over `clean`'s (its `tracking` −25 stays when the kit gives none), `override` still wins over the kit. A kit's `fonts` (a list of font URLs or `{ "src", "fontFamily" }`) become document assets `brand.font.<n>` of type `font` (spec 12 §12.1.4); an id the document already declares is kept. The assets are declared only: the service fetches what the authored document declares, so a brand font must still be declared as a `font` asset in the document for a service render until the fetcher reads kits, and the CLI does not register document font assets yet (`09-sound-fonts.md`). Locally, map the asset to a file with `--assets` (`examples/concepts/01-theme-brand-kit.assets.json`).

## Which theme

| Theme | Look | Reach for it when |
|---|---|---|
| `default` | neutral dark, Inter | nothing else fits; the engine's fallback |
| `clean` | white, near-black type, electric blue, Inter Display, 1.25 scale, `styles.dropShadow` | data stories, explainers, product pages, anything that must read like a document |
| `midnight` | navy-black, cyan accent, Space Grotesk/Manrope, grain 0.06, vignette 0.25 | tech launches, title cards, feature tours |
| `editorial` | warm paper, Fraunces (opsz 144, SOFT 30)/Source Serif 4, brick red, 1.414 scale, grain 0.15, vignette 0.12, long sine eases, `gentle` spring is over-damped (bounce −0.1) | quotes, documentaries, culture, long-form titles |
| `bold` | near-black, hot orange, Unbounded 800/Plus Jakarta Sans, 1.5 scale, 0.1–0.9 s durations, bouncy springs | social ads, hooks, sports, launch teasers |
| `soft` | lilac off-white, lavender, Nunito, radius 12/24/48, gentle springs, `styles.dropShadow` | wellness, consumer apps, UI demos, friendly explainers |
| `mono` | black/white/one green, JetBrains Mono everywhere, radius 0, `linear` = `steps(8)` | developer tools, terminals, kinetic type |
| `neon` | black, magenta, pure-neon palette, Syne/Sora, vignette 0.35, grain 0.05 | logo stings, music, nightlife; pair with `output.toneMap: "soft"` and `light.glow` |
| `corporate` | navy, mid-blue, IBM Plex Sans/Mono, 1.25 scale, no overshoot (springs critically damped), vignette 0.1 | finance, enterprise, interviews, lower thirds |
| `retro` | cream, burnt orange, Bricolage Grotesque (wdth 90)/Work Sans, grain 0.3, vignette 0.3, `linear` = `steps(12)`, `enter` = `back.out(1.2)`, `emphasis` = `elastic.out(1, 0.5)` | throwback, music, lifestyle, zines |

## Every value of every theme

Generated from the theme files (`92-themes.md` lists each theme token by token).

<!-- gen:library-theme-values:start -->
| Theme | `color` bg / fg / accent / muted / surface / line | `palette` | positive / negative / warning | `font` display / body / mono | `type` base · ratio · lineHeight | `radius` s/m/l | `motion.dur` xs/s/base/l/xl/transition | `motion.stagger` tight/base/loose | `ease` default / enter / exit / move / emphasis / linear / transition | `spring` gentle / snappy / bouncy (bounce, duration) | `texture` grain / grainSize / vignette | `styles` |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| `bold` | #0D0D0D / #FFFFFF / #FF3D00 / #9A9A9A / #1A1A1A / #333333 | #FF3D00 #FFD600 #00E5FF #D500F9 #76FF03 | #76FF03 / #FF1744 / #FFD600 | Unbounded 800 (-10) / Plus Jakarta Sans 600 (0) / Space Mono 700 (0) | 0.046 · 1.5 · 1.0 | 4/12/28 | 0.1/0.22/0.38/0.6/0.9/0.35 | 0.015/0.04/0.08 | "power3.out" / "power4.out" / "power3.in" / [0.2, 0, 0, 1] / "back.out(2.4)" / "linear" / "power4.inOut" | (0.05, 0.4) / (0.22, 0.3) / (0.38, 0.5) | 0 / 1 / 0 | none |
| `clean` | #FFFFFF / #0B0B0F / #2563EB / #6B7280 / #F3F4F6 / #E5E7EB | #2563EB #0EA5E9 #F59E0B #10B981 #EF4444 | #059669 / #DC2626 / #D97706 | Inter Display 700 (-25) / Inter 450 (0) / Geist Mono 500 (0) | 0.04 · 1.25 · 1.2 | 6/12/24 | 0.15/0.28/0.45/0.7/1.0/0.45 | 0.02/0.05/0.09 | "power2.out" / "expo.out" / "power2.in" / [0.2, 0, 0, 1] / "back.out(1.4)" / "linear" / "power3.inOut" | (0, 0.45) / (0.12, 0.32) / (0.25, 0.55) | 0 / 1 / 0 | {"dropShadow": {"dropShadow": {"color": "#0B0B0F", "opacity": 18, "angle": 90, "distance": 16, "size": 40}}} |
| `corporate` | #10213A / #F2F5F9 / #2F6FED / #93A3B8 / #1A2F4F / #2C4368 | #2F6FED #5FA8E8 #8FB8D9 #F0B429 #3DBE8B | #3DBE8B / #E05C5C / #F0B429 | IBM Plex Sans 600 (-10) / IBM Plex Sans 400 (0) / IBM Plex Mono 400 (0) | 0.038 · 1.25 · 1.25 | 4/8/16 | 0.15/0.3/0.5/0.8/1.2/0.5 | 0.03/0.06/0.1 | "power2.out" / "power3.out" / "power2.in" / [0.4, 0, 0.2, 1] / "power2.inOut" / "linear" / "power2.inOut" | (0, 0.5) / (0, 0.35) / (0.05, 0.5) | 0 / 1 / 0.1 | none |
| `default` | #0B0B0F / #F5F5F7 / #7C5CFF / #8A8A99 / #16161D / #2A2A35 | #7C5CFF #22D3EE #F472B6 #FACC15 #34D399 | #34D399 / #F87171 / #FACC15 | Inter 800 (-20) / Inter 500 (0) / JetBrains Mono 500 (0) | 0.042 · 1.333 · 1.15 | 8/16/32 | 0.15/0.3/0.5/0.8/1.2/0.5 | 0.02/0.05/0.1 | "power2.out" / "expo.out" / "power2.in" / [0.2, 0, 0, 1] / "back.out(1.7)" / "linear" / "power3.inOut" | (0, 0.5) / (0.15, 0.35) / (0.3, 0.6) | 0 / 1 / 0 | none |
| `editorial` | #F4EDE2 / #1E1A16 / #B5452E / #7A6E63 / #EADFCF / #D9CCB9 | #B5452E #2E5E4E #C99A2E #4A5B8C #8C4A6B | #2E5E4E / #B5452E / #C99A2E | Fraunces 600 (-10, axes {"opsz": 144, "SOFT": 30}) / Source Serif 4 400 (0) / IBM Plex Mono 400 (0) | 0.044 · 1.414 · 1.25 | 2/4/8 | 0.2/0.4/0.7/1.1/1.6/0.8 | 0.03/0.07/0.14 | "sine.out" / [0.16, 1, 0.3, 1] / "sine.in" / [0.4, 0, 0.2, 1] / "power2.inOut" / "linear" / "sine.inOut" | (-0.1, 0.9) / (0, 0.6) / (0.1, 0.8) | 0.15 / 1.4 / 0.12 | none |
| `midnight` | #060A1A / #EAF0FF / #4CC9F0 / #8B97B8 / #0E1630 / #1C2750 | #4CC9F0 #7B61FF #F72585 #FFD166 #06D6A0 | #06D6A0 / #F72585 / #FFD166 | Space Grotesk 700 (-15) / Manrope 500 (0) / Geist Mono 500 (0) | 0.042 · 1.333 · 1.15 | 8/18/36 | 0.15/0.3/0.55/0.85/1.3/0.55 | 0.025/0.06/0.11 | "power3.out" / "expo.out" / "power3.in" / [0.2, 0, 0, 1] / "back.out(2.0)" / "linear" / "expo.inOut" | (0, 0.55) / (0.15, 0.38) / (0.3, 0.65) | 0.06 / 1.2 / 0.25 | none |
| `mono` | #000000 / #FFFFFF / #00FF88 / #8C8C8C / #111111 / #2E2E2E | #00FF88 #FFFFFF #B3B3B3 #666666 #333333 | #00FF88 / #FF4D4D / #FFD24D | JetBrains Mono 700 (-20) / JetBrains Mono 400 (0) / JetBrains Mono 400 (0) | 0.036 · 1.25 · 1.3 | 0/0/2 | 0.12/0.25/0.4/0.65/1.0/0.4 | 0.02/0.04/0.08 | "expo.out" / "expo.out" / "expo.in" / [0.2, 0, 0, 1] / "back.out(1.5)" / "steps(8)" / "expo.inOut" | (0, 0.4) / (0.1, 0.3) / (0.2, 0.5) | 0 / 1 / 0 | none |
| `neon` | #050507 / #FFFFFF / #FF2BD6 / #8F8AA3 / #111018 / #262433 | #FF2BD6 #00F0FF #B026FF #FAFF00 #00FF85 | #00FF85 / #FF2B5C / #FAFF00 | Syne 800 (-10) / Sora 500 (0) / Space Mono 400 (0) | 0.044 · 1.414 · 1.1 | 6/14/28 | 0.12/0.28/0.5/0.8/1.2/0.45 | 0.02/0.05/0.1 | "expo.out" / "expo.out" / "expo.in" / [0.2, 0, 0, 1] / "back.out(2.2)" / "linear" / "power4.inOut" | (0, 0.5) / (0.18, 0.33) / (0.35, 0.6) | 0.05 / 1 / 0.35 | none |
| `retro` | #F2E4C9 / #2B1D14 / #E0652C / #7D6A58 / #E8D6B3 / #CDB892 | #E0652C #F2B134 #3C7A6A #7F4F8F #D94F5C | #3C7A6A / #D94F5C / #F2B134 | Bricolage Grotesque 800 (-15, axes {"wdth": 90}) / Work Sans 500 (0) / Space Mono 400 (0) | 0.042 · 1.333 · 1.15 | 6/14/30 | 0.17/0.33/0.5/0.8/1.2/0.5 | 0.04/0.08/0.12 | "power2.out" / "back.out(1.2)" / "power2.in" / [0.3, 0, 0.1, 1] / "elastic.out(1, 0.5)" / "steps(12)" / "power3.inOut" | (0.05, 0.55) / (0.2, 0.38) / (0.35, 0.65) | 0.3 / 1.6 / 0.3 | none |
| `soft` | #FBF7FF / #2B2440 / #A78BFA / #8E86A6 / #FFFFFF / #E9E1F7 | #A78BFA #F9A8D4 #FDE68A #99E9D5 #93C5FD | #5FCDA8 / #F08A8A / #F2C94C | Nunito 800 (-10) / Nunito 500 (0) / DM Mono 400 (0) | 0.04 · 1.333 · 1.25 | 12/24/48 | 0.18/0.35/0.55/0.85/1.3/0.6 | 0.03/0.06/0.12 | "power2.out" / "expo.out" / "sine.in" / [0.2, 0, 0, 1] / "back.out(1.3)" / "linear" / "power2.inOut" | (0, 0.6) / (0.08, 0.4) / (0.2, 0.7) | 0 / 1 / 0 | {"dropShadow": {"dropShadow": {"color": "#2B2440", "opacity": 14, "angle": 90, "distance": 24, "size": 64}}} |

Every theme's `space` is `{"unit": 0.0125, "scale": [0, 1, 2, 3, 4, 6, 8, 12, 16, 24]}` and `radius.pill` is 9999.
<!-- gen:library-theme-values:end -->

## Rules

- Never write a literal color or font where a token exists: variants and brand swaps then cost nothing, and the ten themes restyle every library component.
- Hierarchy by `type.size` steps: headline `size.5`–`size.6`, subline `size.2`, body `size.0`, captions `size.3` on 9:16.
- Stick to token names in the table; a reference to a token the theme does not define is an error, not a fallback.
- A font family from a theme must exist in the pack (`build-library-index.py` checks the library themes against `fonts/pack.toml`; the engine falls back with `lint.font_fallback_used` on an unknown family in a document).

Worked examples (all checked): `examples/concepts/01-theme-override.motion.json` (every derived token, modifier, spring and style token on a `soft` override), `01-theme-brand-kit.motion.json` (+ `.assets.json`), `01-theme-inline.motion.json`.

```json
{ "theme": { "use": "mitte/soft@1",
    "override": { "color": { "accent": "#FF4D00", "surface": "$theme.color.bg.darker" },
                  "font": { "display": { "family": "Space Grotesk", "weight": 700, "tracking": -20 } },
                  "motion": { "dur": { "base": 0.4 } }, "texture": { "grain": 0.1, "vignette": 0.2 },
                  "styles": { "card": { "dropShadow": { "color": "#2B2440", "opacity": 30, "angle": 90, "distance": 18, "size": 48 } } } } } }
```

```json
{ "id": "chipLabel", "type": "text", "text": "Get started",
  "style": { "font": "$theme.font.body", "size": "$theme.type.size.0", "fill": "$theme.color.accent.on" } }
```

```json
{ "target": ["chip", "chipLabel"], "preset": "scaleIn", "ease": "$theme.spring.bouncy", "at": "<0.15" }
```
