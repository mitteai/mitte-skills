# Credits: the eight `credits.*` components in depth

End credits are a **sections document** passed as the `sections` prop to one of `mitte/credits.crawl@1`, `credits.cards`, `credits.cast-card`, `credits.pairs`, `credits.grid`, `credits.song`, `credits.logos`, `credits.legal`. Seven are engine-backed: the normalizer typesets the sections itself (`engine/crates/rexx-normalize/src/passes/credits.rs`), measuring every block with the same text measurer as the measurement pass, so wrapped paragraphs and mixed sizes stack exactly. `credits.cast-card` is in-grammar (its library file's own layers), with name casing and the still choice done by the normalizer. Spec: 12 §12.8, 2 §2.13 (crawl), 14 §14.4 (lint).

```json
{ "id": "roll", "type": "component", "use": "mitte/credits.crawl@1", "in": 1,
  "props": { "sections": "$data.sections", "duration": 60,
             "font": "$theme.font.body", "nameWeight": 600, "roleWeight": 400,
             "size": 28, "lineHeight": 1.3, "gutter": 48, "columns": 4,
             "namesCase": "upper", "width": "80%", "white": "#E6E6E6" } }
```

## The sections document

`sections` is a list (1–2,000 items for the crawl and the blocks; `cast-card` accepts an empty list) in the author's order. Every item has `kind` (required) and the fields of its kind; keys that do not apply are ignored; an empty section (no role and no names, no text) is skipped.

| `kind` | Fields | How it is typeset |
|---|---|---|
| `card` | `role`, `names[]`, `join` (`&` or `and`) | the role (role style) above the names joined with ` & ` or ` and ` (name style), centred |
| `heading` | `text` | upper case, name weight, tracking 80, with half a line of extra space above |
| `pairs` | `rows[] { role, names[] }` | two columns on a centre gutter: roles right-aligned ending at centre − `gutter`/2, names left-aligned from centre + `gutter`/2, one row per entry; extra names stack under the first with the role left blank; both columns share one line pitch, so rows stay paired |
| `list` | `title`, `names[]` | the title (role style), then one name per line, centred |
| `grid` | `title`, `names[]`, `columns` | the title, then the names row-major in columns (the section's `columns`, else the component's; 0 in both = auto: 6 columns for names up to 10 characters, 5 up to 14, 4 up to 18, else 3), each column at most 9 em wide, the grid centred |
| `song` | `title`, `lines[]` | the title in typographic quotes (name style, cased per `namesCase`), then the lines (role style) |
| `text` | `text` | a centred paragraph at `size`, wrapped inside `width` |
| `legal` | `text` | a centred paragraph at round(0.75 × `size`) |
| `logos` | `image_urls[]` | each URL added as an asset `<instance>.img<n>` and drawn `fit: contain` in a cell 320 × 128 px at size 28 (scaled with `size`), `columns` per row (0 = one row), cells shrunk together when a row is wider than `width` |
| `photo` | `image_url`, `text`, `caption` | the image (asset `<instance>.img<n>`, 40 % of `width`, `fit: contain`) above the text (name style) and the caption (legal size); cards only |

**Name style:** `nameWeight` at `size`. **Role style:** `roleWeight` at round(0.85 × `size`). Leading is `lineHeight × size` throughout; sections are two leadings apart. Names follow `namesCase`: `upper` upper-cases every name but keeps a surname prefix as written when a capital follows it (`Diego McAllister` → `DIEGO McALLISTER`, `Ian MacDonald` → `IAN MacDONALD`, `O'`, `Di`, `De`, `Van`, `Von` likewise; `Mack` → `MACK`); `title` capitalises each word's first letter; `none` leaves names as written. Roles keep their case. A leading `$` in any credit is kept as text.

## Which component renders which kinds

| Component | Renders | Skipped (each with `lint.credits_kind_skipped`, info, at `/…/props/sections/<i>`) |
|---|---|---|
| `credits.crawl` | every kind but `photo` | `photo` (a photo needs a card) |
| `credits.cards` | `card`, `heading`, `text`, `legal`, `list`, `photo` | `pairs`, `grid`, `song`, `logos` |
| `credits.pairs` | `pairs`, `heading` | the rest |
| `credits.grid` | `grid`, `list` | the rest |
| `credits.song` | `song` | the rest |
| `credits.logos` | `logos` | the rest |
| `credits.legal` | `legal`, `text` | the rest |
| `credits.cast-card` | its own `name`/`role`/still (below) | — |

So one credits document can feed every component: nothing is lost silently.

## Shared style params (every credits component)

| Param | Type | Default | Use |
|---|---|---|---|
| `sections` | list | required (`[]` for `cast-card`) | the document above |
| `font` | font token or family | `$theme.font.body` (`cast-card`: `font.display`) | every text |
| `nameWeight`, `roleWeight` | 400–700 (clamped) | 600, 400 (`cast-card` 700, 400) | name and role weights |
| `size` | 12–200 px | 28 (`cards` 40, `cast-card` 64) | the name size; roles 0.85×, legal 0.75× |
| `lineHeight` | 1.2–1.45 (clamped) | 1.3 (`legal` 1.35, `cast-card` 1.2) | leading = `lineHeight × size` |
| `gutter` | px | 48 (`cast-card` 16) | the pairs gutter, grid and logo spacing |
| `columns` | 0–12 | 4 (`cast-card` 1) | grid and logo columns (0 = auto / one row) |
| `namesCase` | `upper` \| `none` \| `title` | `upper` (`song`, `legal` `none`) | above |
| `width` | `"80%"` or px | `"80%"` (`legal` `"70%"`, `cast-card` `"60%"`) | the block's width, a percentage of the **parent comp's width** |
| `white` | color | `#E6E6E6` | every text's fill. A channel above 235 is `lint.credits_white_hot` (warning, at `props/white`) on any credits component |

Own params: `credits.crawl` `speed` (whole px per frame) and `duration` (s; **set one**: `duration` wins, `speed: 3` when neither is given); `credits.cards` `transition` (`fade` \| `cut`) and `minHold` (s); `credits.cast-card` `name`, `role`, `image` (asset), `tritone`, `grain`, `hold` and the slot `still`; the blocks `hold` (their comp's duration) and `enter` (`rise` \| `fade` \| `none`); `credits.logos` `cell`, `monochrome`. Giving `speed` or `duration` to any credits component makes it a crawl.

## What each builds

- **`credits.crawl`**: the sections stacked top to bottom into one block `width` wide, every layer parented to a carrier `sheet` (an unfilled rect exactly the block's size, centred on the frame) that takes `crawl: { "dir": "up", "from": "below", "to": "above", "hold": [1, 1] }` and `motionBlur: false`. The crawl pass keys the carrier at a whole number of pixels per frame (start = the block's top at the frame's bottom edge, travel until its bottom clears the top, one second of hold before and after); with `duration` d the speed is `round(L / (d · fps))` ≥ 1, the real length `ceil(L / speed) / fps`, and `lint.crawl_duration_mismatch` reports a difference above 5 % ("The requested 60 s became 55.083 s at 2 px per frame."). Read the timing sheet (`roll.comp:sheet`) and set the instance's `out` to cover it. Body text faster than 4 px per frame at 24 fps (scaled with fps) is `lint.crawl_too_fast`.
- **`credits.cards`**: one card per qualifying section, typeset like the crawl's blocks inside the title-safe 90 % of the frame and centred on it. Each card is held for its reading time `max(minHold, 0.4 + 0.33 × words)` seconds (words = every word on the card; the first card at least 2 s), and joined by a 0.5 s fade in and out through black (`fade`) or a cut on the frame boundary (`cut`), starting at 1 s. The generated comp lasts 1 s + the cards + 1 s, and the instance's `out` defaults to that. The card layers are `s<i>-role`, `s<i>-names`, … with `in`/`out` per card; the timing sheet lists them.
- **`credits.pairs`, `.grid`, `.song`, `.logos`, `.legal`** (blocks): the sections of their kinds stacked in a comp exactly the block's measured size (`width` × its height), so the instance's `position`/`align` place the block and it stays inside its own comp. `enter: "rise"` rises every layer 12 px with the theme's tight stagger over `dur.l`; `fade` fades them in with the same stagger; `none` cuts in. The comp lasts `hold` seconds.
- **`credits.cast-card`**: the still (the `still` slot's layers, which win, or the `image` asset filling the frame with `fit: cover`), a shade gradient over the lower 40 %, the `name` (cased per `namesCase`, `nameWeight`, `size`) above the `role` (`roleWeight`, round(0.55 × `size`)) bottom-left in the title-safe box; `tritone` and `grain` switch the effects on the still. Fade in over 0.6 s, the name rises, the role fades, hold `hold` seconds, fade out. When `name` is empty and `sections` holds a `pairs` row, its first name becomes `name` and its role `as <role>`. Neither `image` nor a `still` slot is `component.param_invalid` at `props/image`.

## Delivery and pitfalls

- Editor hand-off: `output: { "format": "mov", "codec": "prores", "quality": "high", "audio": { "always": true } }`. UHD at 24 fps is the common ask (3840 × 2160 is the service's P1 cap); `size` 56 there.
- Black before and after comes from the parent comp's `background`, not the instance.
- Long credits belong in `data` (≤ 512 KB) or a `data` asset, not in layer text; the 2,000-section cap is the list's `maxItems`.
- Logo and photo URLs become assets of the instance (`<instance>.img<n>`); locally map them with `--assets` like any asset.
- Do not animate a crawl with position tweens (fractional speeds shimmer); a `crawl` and explicit position keys on one layer collide (`tween.key_collision`).
- A 5-minute crawl is cheap and admitted; admission is by estimated render time, not length (P1 caps a variant at 600 s).

Worked example (checked): `examples/concepts/06-credits-crawl.motion.json` (thirteen sections of every kind, `duration: 60` at 24 fps, ProRes output).
