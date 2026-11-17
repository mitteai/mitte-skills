# Captions: the four `caption.*` components in depth

Word-timed captions are a library component, not a layer type: `mitte/caption.highlight@1`, `caption.karaoke`, `caption.minimal`, `caption.pop` share one param interface, so switching style is changing `use`. They are **engine-backed**: the normalizer builds the pages from the word timings (`engine/crates/rexx-normalize/src/passes/captions.rs`, with the word sugar of `passes/words.rs`), cloning the library file's `group` reference layer for each page. Spec: 12 §12.7, 10 §10.9, 5 §5.10.

```json
{ "id": "captions", "type": "component", "use": "mitte/caption.highlight@1", "in": 0.6,
  "props": {
    "words": "$data.@transcript.words",
    "group": { "maxWords": 3, "maxChars": 18, "breakOn": "punctuation" },
    "style": { "font": "$theme.font.display", "size": "$theme.type.size.3", "case": "upper", "fill": "#FFFFFF", "weight": 800, "stroke": { "color": "#000000", "width": 8 } },
    "active": { "fill": "$theme.color.accent", "scale": 108 },
    "position": "safe-bottom", "lines": 2 } }
```

## Params (shared by the four styles)

| Param | Type | Default (`highlight`) | What the engine does with it |
|---|---|---|---|
| `words` | list (1–50,000) of `{ text, start, end, speaker?, emphasis? }` | required | Word timings in seconds **relative to the instance's `in`**; make `in` equal the voice layer's `in`. `start`/`end` accept any time form. The list is usually `$data.@<asset>.words` (a `data` asset holding the spec 10 §10.9 object: JSON, or an SRT/WebVTT file, below) or `$data.<path>`. Locally map a data asset with `--assets`. |
| `group.maxWords` | number 1–8 | 3 | Words per page. |
| `group.maxChars` | number 6–48 | 18 | Characters per line: a page breaks before a word that would take it past `maxChars × lines`. |
| `group.breakOn` | `punctuation` \| `pause` \| `none` | `punctuation` | `punctuation` also ends a page after a word ending in `.`, `!` or `?`; `pause` ends a page at a silence longer than `group.pause` between two words; `none` uses only the counts. |
| `group.pause` | time 0.1–2 | 0.35 | The silence that ends a page under `breakOn: "pause"`. |
| `style` | text style + `case` | display font, `size.3`, `upper`, 800, stroke 8 | Laid over the reference layer's style (any spec 5 character-style field passes through). `case` (`none`, `upper`, `lower`, `title`) rewrites the words before layout. |
| `active.fill`, `.scale`, `.weight`, `.opacity` | color, 100–140, number, percent | accent, 108, null, — | The spoken word's style: the `_wordsActive` animator of spec 5 §5.10 on each page (`scale` becomes `[s, s]`). |
| `active.y` | px | 0 | The spoken word's vertical offset (a `position` offset on the animator). |
| `active.background`, `active.radius` | color, px | null, `$theme.radius.s` | A pill behind the spoken word: one rounded rect per word (`pill<p>-<k>`), on screen for that word's spoken span, measured by the engine from the page's text and parented to the page. With a pill a page is one line of point text (no wrapping). |
| `active` = `null` | | | No active style (plain group captions). |
| `emoji.enabled`, `.map`, `.maxPerMinute` | boolean, object, 0–60 | false, {}, 6 | When enabled, a word whose lowercased letters are a key of `map` or of the built-in map (about 250 common words: `money` 💰, `fire` 🔥, `stop` 🛑, `love` ❤️, `idea` 💡, …) pops its emoji above the page at the word's start (`emoji<p>-<k>`, Noto Color Emoji at 1.1 × the style size, `popIn`, parented to the page), at most `maxPerMinute` a minute (spaced at least 60 / maxPerMinute s apart; the first match wins). |
| `position` | `safe-bottom` \| `safe-center` \| `safe-top` \| `[x, y]` | `safe-bottom` | A keyword aligns each page to the comp's or variant's safe box (`align: { "to": "safe", "x": "center", "y": … }`); a literal `[x, y]` (percentages allowed) places the page's centre there. |
| `lines` | 1–3 | 2 | Multiplies the character budget; the page wraps inside its box (86 % × 30 % of the parent frame). |
| `enter` | `pop` \| `rise` \| `fade` \| `none` | `pop` | Each page's entrance at its first word: `pop` scales 94 → 100 % with the theme's emphasis ease over `dur.xs`; `rise` 16 px over `dur.s`; `fade` over `dur.xs` (`caption.minimal`: a 10 px rise over `dur.s` on the enter ease); `none` cuts in. `caption.pop`'s `pop` scales every word in from 40 % with `back.out(2.2)`, staggered by the theme's base stagger. |

A page that would hold a word wider than its box shrinks (`overflow: shrink`, down to 0.4 × the size) instead of breaking the word.

### The four styles

| Style | `group.maxWords` / `maxChars` | `style` | `active` | `emoji.enabled` | `lines` | `enter` | Look |
|---|---|---|---|---|---|---|---|
| `caption.highlight` | 3 / 18 | display, `size.3`, `upper`, 800, stroke 8 | accent, 108 % | false | 2 | `pop` | the page pops in, the spoken word takes the accent (and a pill with `active.background`) |
| `caption.karaoke` | 4 / 22 | display, `size.3`, `title`, 800, stroke 6 | accent, 100 % | false | 2 | `none` | the accent sweeps through each word character by character over exactly its spoken span; sung words stay accent |
| `caption.minimal` | 6 / 32 | **body** font, `size.1`, `none`, 600, stroke 0 | none unless the instance gives `active` | false | 2 | `fade` | small sentence-case lines, gentle fade and 10 px rise per page |
| `caption.pop` | 2 / 12 | display, `size.4`, `upper`, 900, stroke 10 | accent, 112 % | true | 1 | `pop` | one or two heavy words, each scaling in with overshoot, a drop shadow (the theme's `styles.dropShadow` when it has one), emoji |

## What the engine builds

The generated comp `<instance>.comp` (the parent frame's size; its duration runs to the last word) holds, per page *p*:

- `group<p>`: a text layer (the reference `group` layer with the instance's style), `in` at the page's first word and `out` at the next page's first word (the last page at its last word's end), its text the page's words, and the per-page animators: `_wordsActive` keyed with hold keys at every word's `start` to `[k, k + 1]` (indices restart per page; a gap keeps the previous word active), or for karaoke `_karaoke`, a `range` selector by characters whose `end` runs linearly from the word's first character to its last between the word's `start` and `end` and holds in the gaps.
- `pill<p>-<k>` per word when `active.background` is set; `emoji<p>-<k>` per matched word when emoji are on.
- A timeline entry per page for `enter`, and a `popIn` per emoji.

The timing sheet (`motion.check` → `timing`) lists every page layer with its span, so the page breaks are visible before rendering. On 16:9 the 30 %-tall box is taller than the title-safe band, so `lint.text_outside_safe_area` can fire on the box while the words sit inside it; a page that cuts to the next is `lint.missing_exit` by design.

## The word-timings file

```json
{ "language": "en",
  "words": [ { "text": "Ship", "start": 0.42, "end": 0.71 }, { "text": "faster", "start": 0.71, "end": 1.18, "emphasis": true },
             { "text": "with", "start": 1.30, "end": 1.44 }, { "text": "mitte.", "start": 1.44, "end": 1.95 } ] }
```

Declared as `{ "transcript": { "src": "https://…/vo.words.json", "type": "data" } }` and read as `$data.@transcript.words`. Times are in the media's own time; the instance's `in` must equal the voice or footage layer's `in`. JSON and CSV data assets are parsed as data; an **SRT or WebVTT** file (a `WEBVTT` header, or a cue number followed by a `-->` timing line) becomes the same `{ "words": [ … ] }` object with each cue's words spread evenly across the cue, and the caption reports `media.captions_cue_level` (word highlights are approximate). A `words` value that is not a list is `ref.unresolved`. Words missing `start` are dropped; a missing `end` equals `start`.

## Rules

- Set `safe` (`"tiktok"`, `"reels"`, `"shorts"`, `"story"`, `"youtube"`, `"square"`, `"broadcast"` or `{ "action", "title" }`) and `lint.platform` on the comp and per variant; `position: "safe-bottom"` then clears the platform's UI.
- Order the layers: footage, grade, captions, then an end card that should cover them.
- 9:16: `size.3` or larger (`lint.tiny_text` below ≈ 2.5 % of the shorter side on portrait); stroke 6–10 px at 1080 wide; `caption.minimal` needs a plate or a darker grade instead.
- Variants: `"captions": { "props": { "lines": 1, "group": { "maxWords": 2, "maxChars": 14 } } }` in a square override is the usual change (an object param is deep-merged: give the whole `group` you want).

## Hand-built captions on a text layer

For a look the components do not give (dimmed future words, a custom box, a per-speaker colour), a text layer takes the same `words` list plus `wordStyle` and `paging` (spec 5 §5.10) and compiles to page keys and animators on that one layer, with all three styles:

```json
{ "id": "hand", "type": "text", "in": 2.2,
  "words": [ { "text": "Built", "start": 0.0, "end": 0.3 }, { "text": "by", "start": 0.3, "end": 0.5 }, { "text": "hand.", "start": 0.5, "end": 1.0 } ],
  "wordStyle": { "active": { "fill": "$theme.color.accent", "scale": 112 }, "past": { "opacity": 100 }, "future": { "opacity": 35 } },
  "paging": { "maxWords": 3, "maxChars": 18 },
  "style": { "font": "$theme.font.display", "size": "$theme.type.size.3", "fill": "#FFFFFF" },
  "origin": "center", "position": ["50%", "50%"] }
```

`wordStyle.past`, `active`, `future` each take character-style props (`fill`, `opacity`, `scale`, `weight`); an empty object emits no animator. Keys are in layer time. `paging` is optional (no paging = one page; it has no `breakOn`, the components do). Everything else about the layer is yours.

Worked examples (checked): `examples/concepts/05-captions.motion.json` (a 9:16 ad with footage, grade, `caption.highlight`, a voice layer, square and landscape variants overriding `lines` and `group`) and `05-captions-styles.motion.json` (the three styles stacked on the same `$data.words`, and the hand-built layer).
