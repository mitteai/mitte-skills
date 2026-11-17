# Sound pack and fonts

## The sound pack `mitte/sfx.*`

Eight short clips ship as library audio assets (spec 12 §12.6.4), synthesized in-house by `library/mitte/sfx/make.py` from seeded noise, sines and envelopes and dedicated CC0 (`library/ATTRIBUTION.md`): `library/mitte/assets/sfx/<name>.wav`, 48 kHz 24-bit mono, true peak at or under −6 dBTP, the clips long enough for an integrated loudness within 2 LU of the pack's median (about −21 LUFS). Use one as an ordinary `audio` layer: `"asset": "library:mitte/sfx/hit.soft@1"`, or declare `{ "hit": { "src": "library:mitte/sfx/hit.soft@1", "type": "audio" } }` under `assets`; the service resolves the URI from the image's library, no fetch. The P2 `sound` hook on preset uses (`"sound": "hit.soft"`) is **not implemented**: add the audio layer at the preset's start yourself.

| URI | Length | Character | Typical use |
|---|---|---|---|
| `library:mitte/sfx/whoosh.soft@1` | 0.55 s | airy filtered-noise swell, no tail | `slideIn`, `maskReveal`, lower-third entrances |
| `library:mitte/sfx/whoosh.hard@1` | 0.38 s | fast, bright, Doppler-shaped noise pass | whip transitions, `kinetic.slam` approach |
| `library:mitte/sfx/hit.soft@1` | 0.69 s | padded low thud, short tail | logo resolve, a word landing (`kinetic.stomp`) |
| `library:mitte/sfx/hit.deep@1` | 1.30 s | sub-heavy impact, 1 s tail | trailer title lands, countdown zero |
| `library:mitte/sfx/riser.short@1` | 1.21 s | rising noise and pitch sweep ending clean | into a reveal or a cut; countdown 3-2-1 |
| `library:mitte/sfx/tick@1` | 0.04 s | dry click | cursor clicks, counter steps, countdown ticks |
| `library:mitte/sfx/pop@1` | 0.15 s | soft bubble pop | `popIn` on icons, `caption.pop` words, emoji |
| `library:mitte/sfx/swell@1` | 1.94 s | warm low tonal swell, slow attack and release | end cards, quote cards, soft reveals |

`library/mitte/sfx/pack.toml` lists each clip's length, peak, RMS level and SHA-256; `python3 library/mitte/sfx/make.py --check` proves the committed files are what the script writes. Replacing a clip's take is a new name (a render's audio must not change under the same URI).

## The font pack

Text layers name a family (`"font": "Inter"` or a theme token whose `family` is one); the engine resolves it from the pack (case-insensitive, spaces and hyphens ignored) or from a document `font` asset (`{ "src": "https://…/Brand.ttf", "type": "font", "fontFamily": "Brand" }`). No system fonts, ever. The pack is defined by `fonts/pack.toml` (version, pinned google/fonts commit, per-family files with sizes and blob hashes), locked by `fonts/pack.lock` (sha256 per file and a pack hash that `rexx-engine version` reports as `fonts`), attributed in `fonts/ATTRIBUTION.md`, and fetched by `python3 fonts/fetch.py` into `fonts/files/` (gitignored, ~148 MB, 328 files). Every family is OFL-1.1 or Apache-2.0 with its licence file beside the fonts. A family a document names that is not in the pack and not an asset falls back (`lint.font_fallback_used`); the theme files are checked against the pack by `build-library-index.py`.

Families used by the library themes: Inter, Inter Display, Geist Mono, Space Grotesk, Manrope, Fraunces, Source Serif 4, IBM Plex Mono, Unbounded, Plus Jakarta Sans, Space Mono, Nunito, DM Mono, JetBrains Mono, Syne, Sora, IBM Plex Sans, Bricolage Grotesque, Work Sans; components also set Noto Sans Symbols 2 (badges), Caveat (`callout.arrow`) and Abril Fatface (the reel's ampersand). Colour emoji render from Noto Color Emoji's bitmap build (`lint.bitmap_emoji_scaled` at large sizes); the library notes say colour emoji inside component text do not render yet.

Variable families expose their axes through a font token's or style's `axes` (`{ "opsz": 144, "SOFT": 30 }` on Fraunces, `{ "wdth": 90 }` on Bricolage Grotesque, `wght` everywhere a `[wght]` file exists); static families (Poppins, Barlow Condensed, IBM Plex Mono, Space Mono, DM Mono, Kalam, the Zen Maru Gothic weights) take only the listed weights.

### Every family

Generated from `fonts/pack.toml`.

<!-- gen:library-fonts:start -->
Pack version `2026.10`, pinned to google/fonts commit `2c605eeda2de57af2b34822b79986f5140299862`; 89 families. Columns: license, roles (what the family is for), scripts, build (variable axes or static weights from the file names), notes.

| Family | License | Designer | Roles | Scripts | Build | Notes |
|---|---|---|---|---|---|---|
| Inter | OFL-1.1 | Rasmus Andersson | sans, text | latin, latin-ext, cyrillic, greek | variable [opsz,wght] + italic |  |
| Inter Display | see alias | — | sans, display |  | alias of Inter, axes {"opsz": 32} | Not a separate family on google/fonts: Inter's opsz axis at 32 is Inter Display. |
| Manrope | OFL-1.1 | Mikhail Sharanda | sans, text | latin, latin-ext, cyrillic, greek | variable [wght] |  |
| DM Sans | OFL-1.1 | Colophon Foundry | sans, text | latin, latin-ext | variable [opsz,wght] + italic |  |
| Plus Jakarta Sans | OFL-1.1 | Tokotype | sans, text | latin, latin-ext, cyrillic | variable [wght] + italic |  |
| Figtree | OFL-1.1 | Erik Kennedy | sans, text | latin, latin-ext | variable [wght] + italic |  |
| Onest | OFL-1.1 | Dmitri Voloshin, Andrey Kudryavtsev | sans, text | latin, latin-ext, cyrillic, symbols, math | variable [wght] |  |
| Geist | OFL-1.1 | Andrés Briganti, Mateo Zaragoza, Guillermo Rauch, Evil Rabbit, José Rago, Facundo Santana | sans, text | latin, latin-ext, cyrillic | variable [wght] + italic |  |
| Public Sans | OFL-1.1 | USWDS, Dan Williams, Pablo Impallari, Rodrigo Fuenzalida | sans, text | latin, latin-ext | variable [wght] + italic |  |
| IBM Plex Sans | OFL-1.1 | Mike Abbink, Bold Monday | sans, text | latin, latin-ext, cyrillic, greek | variable [wdth,wght] + italic |  |
| Source Sans 3 | OFL-1.1 | Paul D. Hunt | sans, text | latin, latin-ext, cyrillic, greek | variable [wght] + italic |  |
| Work Sans | OFL-1.1 | Wei Huang | sans, text | latin, latin-ext | variable [wght] + italic |  |
| Noto Sans | OFL-1.1 | Google | sans, text, fallback | latin, latin-ext, cyrillic, greek, devanagari | variable [wdth,wght] + italic |  |
| Poppins | OFL-1.1 | Indian Type Foundry, Jonny Pinhorn, Ninad Kale | sans, text, display | latin, latin-ext, devanagari | static: Bold, BoldItalic, Italic, Medium, MediumItalic, Regular, SemiBold, SemiBoldItalic |  |
| Montserrat | OFL-1.1 | Julieta Ulanovsky, Sol Matas, Juan Pablo del Peral, Jacques Le Bailly | sans, text, display | latin, latin-ext, cyrillic | variable [wght] + italic |  |
| Outfit | OFL-1.1 | Smartsheet Inc, Rodrigo Fuenzalida | sans, text, display | latin, latin-ext | variable [wght] |  |
| Urbanist | OFL-1.1 | Corey Hu | sans, text | latin, latin-ext | variable [wght] + italic |  |
| Lexend | OFL-1.1 | Bonnie Shaver-Troup, Thomas Jockin, Santiago Orozco, Héctor Gómez, Superunion | sans, text | latin, latin-ext | variable [wght] |  |
| Sora | OFL-1.1 | Jonathan Barnbrook, Julián Moncada | sans, text, display | latin, latin-ext | variable [wght] |  |
| Red Hat Display | OFL-1.1 | MCKL | sans, display | latin, latin-ext | variable [wght] + italic |  |
| Albert Sans | OFL-1.1 | Andreas Rasmussen | sans, text | latin, latin-ext | variable [wght] + italic |  |
| Space Grotesk | OFL-1.1 | Florian Karsten | sans, text, display | latin, latin-ext | variable [wght] |  |
| Bricolage Grotesque | OFL-1.1 | Mathieu Triay | sans, text, display | latin, latin-ext | variable [opsz,wdth,wght] |  |
| Archivo | OFL-1.1 | Omnibus-Type | sans, text, display | latin, latin-ext | variable [wdth,wght] + italic |  |
| Familjen Grotesk | OFL-1.1 | Familjen STHLM AB | sans, text | latin, latin-ext | variable [wght] + italic |  |
| Schibsted Grotesk | OFL-1.1 | Bakken & Bæck, Henrik Kongsvoll | sans, text | latin, latin-ext | variable [wght] + italic |  |
| Hanken Grotesk | OFL-1.1 | Alfredo Marco Pradil, Hanken Design Co. | sans, text | latin, latin-ext, cyrillic | variable [wght] + italic |  |
| Unbounded | OFL-1.1 | NaN | sans, display | latin, latin-ext, cyrillic | variable [wght] |  |
| Syne | OFL-1.1 | Bonjour Monde, Lucas Descroix, George Triantafyllakos | sans, display | latin, latin-ext, greek | variable [wght] |  |
| Anton | OFL-1.1 | Vernon Adams | sans, display | latin, latin-ext | static: Regular |  |
| Bebas Neue | OFL-1.1 | Ryoichi Tsunekawa | sans, display | latin, latin-ext | static: Regular |  |
| Oswald | OFL-1.1 | Vernon Adams, Kalapi Gajjar, Cyreal | sans, display, text | latin, latin-ext, cyrillic | variable [wght] |  |
| Barlow Condensed | OFL-1.1 | Jeremy Tribby | sans, display, text | latin, latin-ext | static: Bold, BoldItalic, Italic, Medium, MediumItalic, Regular, SemiBold, SemiBoldItalic |  |
| Archivo Narrow | OFL-1.1 | Omnibus-Type | sans, text | latin, latin-ext | variable [wght] + italic |  |
| League Gothic | OFL-1.1 | Tyler Finck, Caroline Hadilaksono, Micah Rich | sans, display | latin, latin-ext | variable [wdth] |  |
| Big Shoulders Display | OFL-1.1 | Patric King | sans, display | latin, latin-ext | variable [wght] |  |
| Playfair Display | OFL-1.1 | Claus Eggers Sørensen | serif, display | latin, latin-ext, cyrillic | variable [wght] + italic |  |
| Instrument Serif | OFL-1.1 | Rodrigo Fuenzalida, Jordan Egstad | serif, display | latin, latin-ext | static: Italic, Regular |  |
| Fraunces | OFL-1.1 | Undercase Type, Phaedra Charles, Flavia Zimbardi | serif, display, text | latin, latin-ext | variable [SOFT,WONK,opsz,wght] + italic |  |
| DM Serif Display | OFL-1.1 | Colophon Foundry | serif, display | latin, latin-ext | static: Italic, Regular |  |
| Libre Caslon Text | OFL-1.1 | Pablo Impallari | serif, text | latin, latin-ext | variable [wght] + italic |  |
| Cormorant | OFL-1.1 | Christian Thalmann | serif, display, text | latin, latin-ext, cyrillic | variable [wght] + italic |  |
| EB Garamond | OFL-1.1 | Georg Duffner, Octavio Pardo | serif, text | latin, latin-ext, cyrillic, greek | variable [wght] + italic |  |
| Lora | OFL-1.1 | Cyreal | serif, text | latin, latin-ext, cyrillic, symbols, math | variable [wght] + italic |  |
| Source Serif 4 | OFL-1.1 | Frank Grießhammer | serif, text | latin, latin-ext, cyrillic, greek | variable [opsz,wght] + italic |  |
| Newsreader | OFL-1.1 | Production Type | serif, text | latin, latin-ext | variable [opsz,wght] + italic |  |
| Noto Serif | OFL-1.1 | Google | serif, text, fallback | latin, latin-ext, cyrillic, greek, math | variable [wdth,wght] + italic |  |
| Nunito | OFL-1.1 | Vernon Adams, Cyreal, Jacques Le Bailly | sans, text | latin, latin-ext, cyrillic | variable [wght] + italic |  |
| Quicksand | OFL-1.1 | Andrew Paglinawan | sans, text, display | latin, latin-ext | variable [wght] |  |
| Fredoka | OFL-1.1 | Milena Brandão, Hafontia | sans, display | latin, latin-ext, hebrew | variable [wdth,wght] |  |
| Baloo 2 | OFL-1.1 | Ek Type | sans, display, text | latin, latin-ext, devanagari | variable [wght] |  |
| Zen Maru Gothic | OFL-1.1 | Yoshimichi Ohira | sans, text, display | latin, latin-ext, cyrillic, greek, cjk-jp | static: Bold, Medium, Regular | Replaces the spec's M PLUS Rounded 1c, whose google/fonts directory ships no license file (never has); Zen Maru Gothic is the OFL rounded Japanese sans with one. Spec fix pending in mitteai/docs. |
| Rubik | OFL-1.1 | Hubert and Fischer, Meir Sadan, Cyreal, Daniel Grumer, Omaima Dajani | sans, text, display | latin, latin-ext, cyrillic, arabic, hebrew | variable [wght] + italic |  |
| Righteous | OFL-1.1 | Astigmatic | display | latin, latin-ext | static: Regular |  |
| Bungee | OFL-1.1 | David Jonathan Ross | display | latin, latin-ext | static: Regular |  |
| Monoton | OFL-1.1 | Vernon Adams | display | latin | static: Regular |  |
| Rubik Mono One | OFL-1.1 | Hubert and Fischer | display, mono | latin, latin-ext, cyrillic, hebrew | static: Regular |  |
| Shrikhand | OFL-1.1 | Jonny Pinhorn | display | latin, latin-ext | static: Regular |  |
| Abril Fatface | OFL-1.1 | TypeTogether | serif, display | latin, latin-ext | static: Regular |  |
| Caveat | OFL-1.1 | Impallari Type | handwriting | latin, latin-ext, cyrillic | variable [wght] |  |
| Kalam | OFL-1.1 | Indian Type Foundry | handwriting | latin, latin-ext, devanagari | static: Bold, Regular |  |
| Permanent Marker | Apache-2.0 | Font Diner | handwriting, display | latin | static: Regular |  |
| Dancing Script | OFL-1.1 | Impallari Type | handwriting | latin, latin-ext | variable [wght] |  |
| Pacifico | OFL-1.1 | Vernon Adams, Jacques Le Bailly, Botjo Nikoltchev, Ani Petrova | handwriting, display | latin, latin-ext, cyrillic | static: Regular |  |
| Homemade Apple | Apache-2.0 | Font Diner | handwriting | latin | static: Regular |  |
| JetBrains Mono | OFL-1.1 | JetBrains, Philipp Nurullin, Konstantin Bulenkov | mono, text | latin, latin-ext, cyrillic, greek | variable [wght] + italic |  |
| IBM Plex Mono | OFL-1.1 | Mike Abbink, Bold Monday | mono, text | latin, latin-ext, cyrillic | static: Bold, BoldItalic, Italic, Medium, MediumItalic, Regular, SemiBold, SemiBoldItalic |  |
| Space Mono | OFL-1.1 | Colophon Foundry | mono, text, display | latin, latin-ext | static: Bold, BoldItalic, Italic, Regular |  |
| Fira Code | OFL-1.1 | The Mozilla Foundation, Telefonica S.A., Nikita Prokopov | mono, text | latin, latin-ext, cyrillic, greek | variable [wght] |  |
| DM Mono | OFL-1.1 | Colophon Foundry | mono, text | latin, latin-ext | static: Italic, Medium, MediumItalic, Regular |  |
| Geist Mono | OFL-1.1 | Andrés Briganti, Mateo Zaragoza, Guillermo Rauch, Evil Rabbit, José Rago, Facundo Santana | mono, text | latin, latin-ext, cyrillic | variable [wght] + italic |  |
| Noto Sans Arabic | OFL-1.1 | Google | sans, text, fallback | latin, latin-ext, symbols, math, arabic | variable [wdth,wght] |  |
| Noto Naskh Arabic | OFL-1.1 | Google | serif, text, fallback | latin, latin-ext, symbols, math, arabic | variable [wght] |  |
| Noto Sans Hebrew | OFL-1.1 | Google | sans, text, fallback | latin, latin-ext, cyrillic, greek, hebrew | variable [wdth,wght] |  |
| Noto Sans Devanagari | OFL-1.1 | Google | sans, text, fallback | latin, latin-ext, devanagari | variable [wdth,wght] |  |
| Noto Sans Bengali | OFL-1.1 | Google | sans, text, fallback | latin, latin-ext, bengali | variable [wdth,wght] |  |
| Noto Sans Tamil | OFL-1.1 | Google | sans, text, fallback | latin, latin-ext, tamil | variable [wdth,wght] |  |
| Noto Sans Thai | OFL-1.1 | Google | sans, text, fallback | latin, latin-ext, thai | variable [wdth,wght] |  |
| Noto Sans Georgian | OFL-1.1 | Google | sans, text, fallback | latin, latin-ext, cyrillic, greek, symbols, math, georgian | variable [wdth,wght] |  |
| Noto Sans Armenian | OFL-1.1 | Google | sans, text, fallback | latin, latin-ext, armenian | variable [wdth,wght] |  |
| Noto Sans Ethiopic | OFL-1.1 | Google | sans, text, fallback | latin, latin-ext, ethiopic | variable [wdth,wght] |  |
| Noto Sans JP | OFL-1.1 | Google | sans, text, fallback | latin, latin-ext, cyrillic, cjk-jp | variable [wght] |  |
| Noto Sans KR | OFL-1.1 | Google | sans, text, fallback | latin, latin-ext, cyrillic, cjk-kr | variable [wght] |  |
| Noto Sans SC | OFL-1.1 | Google | sans, text, fallback | latin, latin-ext, cyrillic, cjk-sc | variable [wght] |  |
| Noto Sans TC | OFL-1.1 | Google | sans, text, fallback | latin, latin-ext, cyrillic, cjk-tc | variable [wght] |  |
| Noto Serif JP | OFL-1.1 | Google | serif, text, fallback | latin, latin-ext, cyrillic, cjk-jp | variable [wght] |  |
| Noto Color Emoji | OFL-1.1 | Google | fallback | emoji | static: Regular | google/fonts ships the CBDT bitmap build, which is what P1 uses (spec 5.4); the COLRv1 build for P2 comes from googlefonts/noto-emoji and is not in this pack yet. |
| Noto Sans Symbols 2 | OFL-1.1 | Google | fallback | latin, latin-ext, symbols, math | static: Regular |  |
| Noto Sans Math | OFL-1.1 | Google | fallback |  | static: Regular |  |

Fallback chain: per script `{"Latn": "Noto Sans", "Grek": "Noto Sans", "Cyrl": "Noto Sans", "Arab": "Noto Sans Arabic", "Hebr": "Noto Sans Hebrew", "Deva": "Noto Sans Devanagari", "Beng": "Noto Sans Bengali", "Taml": "Noto Sans Tamil", "Thai": "Noto Sans Thai", "Geor": "Noto Sans Georgian", "Armn": "Noto Sans Armenian", "Ethi": "Noto Sans Ethiopic", "Hira": "Noto Sans JP", "Kana": "Noto Sans JP", "Jpan": "Noto Sans JP", "Hang": "Noto Sans KR", "Kore": "Noto Sans KR", "Hans": "Noto Sans SC", "Hant": "Noto Sans TC", "Bopo": "Noto Sans TC", "Zmth": "Noto Sans Math", "Zsye": "Noto Color Emoji", "Zsym": "Noto Sans Symbols 2"}`; Han order `["Noto Sans JP", "Noto Sans SC", "Noto Sans TC", "Noto Sans KR"]`; terminal `["Noto Color Emoji", "Noto Sans Symbols 2"]`. WASM core families: `["Inter", "Noto Sans"]` (subsets `["latin", "latin-ext", "greek", "cyrillic"]`).
<!-- gen:library-fonts:end -->
