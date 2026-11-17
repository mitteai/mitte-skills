# Recipes: fifteen briefs as compact patterns, re-verified against engine 0.1.48

The retired authoring guide's recipe sections (`library/guide/12-recipes.md`, `12b-recipes-2.md`, `12c-recipes-3.md`, gone with `motion.guide`) were written for P1 and name components that did not exist; this page merges them, replaces "build it from primitives" with the library components that now ship, and marks what the cookbook proves. Each row: default length, beat structure, what to build it from, theme, variants, and the cookbook document that implements it (`11-cookbook-1.md`, `12-cookbook-2.md`).

| Brief | Length | Structure (times) | Build from | Theme | Variants | Cookbook |
|---|---|---|---|---|---|---|
| Product launch teaser | 15 s | 0–1.5 logo sting → 1.5–4.5 kinetic headline → 4.5–11 three feature cards → 11–15 end card; cut on beats | `logo.sting`, `title.kinetic` or `kinetic.words`, `ui.card-stack` (or three local card instances with `in` 4.5/5.0/5.5), `cta.endcard`; `markers.from` beats, `@beat*` | `bold`, `midnight` | 16:9, 9:16, 1:1 | 05, 04 |
| Explainer scene | 30–60 s | title 0–3 → 3–5 numbered steps at voice-over phrase times → summary | `explainer.step` per step (`connector: false` on the last), `in` at phrase times, an `audio` VO layer | `clean`, `soft` | 16:9, 4:5 | 16 |
| Kinetic quote | 10–15 s | words land in groups, the last hardest; attribution at the end; grain | `kinetic.words` (one word per beat, `tilt`) then `quote.card`; or text layers with `/words` tweens and `kinetic.slam`, a rig null `shake` | `editorial`, `mono` | 16:9, 1:1 | 17 |
| Data story | 10–20 s | title → chart draws, bars grow with a stagger and count up → highlight → KPIs → takeaway | `scenes` of `title.card`, `chart.bar` (`series` from `data`, `highlight`), `stat.row`, a kinetic takeaway; `transition.wipe`, `push`, `transition.shape` | `clean` | 16:9, 1:1 | 03 |
| Social ad 9:16 with captions | 15 s | hook in the first 1.5 s → footage with captions → offer → CTA at 12 s; `safe` and `lint.platform` set | `video` `fit: cover` + vignette grade, `title.kinetic`, `caption.pop` or `caption.highlight` (`$data.@transcript.words`), `title.highlight`, `cta.endcard`, VO + music | `bold` | 9:16 master; 1:1, 16:9 | 04, 06 |
| Logo sting | 3–6 s | mark pops 0.2–1.1 → glow flash at the resolve → tagline → blur out; a hit on the resolve | `logo.sting` (SVG asset, `glow`, `tagline`), `particles.confetti` at a marker, `toneMap: "soft"`; an `audio` hit when you have one (the sfx pack is not shipped) | `neon`, `midnight` | 16:9 | 05 |
| UI / product demo | 10–20 s | device floats in → cursor to the control → click → punch zoom → pull back → fade | `screen.demo` (`moves` with `click` and `zoom`, a recording or drawn screen in the `screen` slot), `ui.toast`/`ui.notification` for the result | `soft`, `clean` | 16:9 | 18 |
| Event promo | 15–20 s | date and place → speaker lower thirds over portraits → countdown → CTA; beat-cut | `title.card`, `lower-third.pill` over `image` portraits, `countdown`, `cta.subscribe`, `scenes` with `push`/`maskWipe` | `bold`, `corporate` | 16:9, 9:16, 1:1 | 20, 01 |
| Podcast audiogram | 20–30 s | cover + show title → bar meter pulses with the voice → captions → guest lower third → end frame | the bar-meter pattern below, `caption.minimal` or `caption.karaoke`, `image` cover, `lower-third.minimal` | `mono`, `midnight` | 1:1 master; 9:16 | 06 (+ the meter) |
| Lyric video | 30–60 s | title card before the vocal → lines on `@beat*` → karaoke fill follows the vocal → background pulses on the kick | `lyrics` (timed `lines`), or `caption.karaoke`; `markers.from` beats with `tempo`; `bg.gradient-mesh` whose `drift` or a solid's gradient scale takes an `audio` driver | `retro`, `neon` | 16:9, 9:16 | 08 |
| Map route | 10–15 s | map → route draws with a marker riding it → pins at the stops → destination | `map.route` (`route` SVG path data in component px, `from`/`to`), `map.pin`, `callout.line` / `callout.arrow` | `clean` | 16:9 | 19 |
| Countdown | 5–15 s | N…1 one per second with a draining ring → final reveal | `countdown` (fixed at 3-2-1 + `go`); for longer counts a `repeat` with `count` and per-index `in`/`out` | `bold`, `neon` | 16:9, 9:16 | 20 |
| Testimonial | 15–25 s | card slides in → quote by words → name, role → stars → next card pushes the first | `testimonial.card` per quote (`avatar` image asset, `stars`), `social.comment` for a reply sticker, `scenes` with `push` | `soft`, `corporate` | 1:1, 16:9 | — |
| Tutorial lower thirds | 30–60 s | footage with chapter titles at cuts and a lower third per speaker or step | `video` with its audio, `title.chapter` at cuts, `lower-third.bar`/`.split`/`.news` with `hold`, `align` to the safe corner | `corporate`, `clean` | 16:9 | 01, 12 |
| End card | 5–8 s | logo pops → line → URL and handles → button pulses; a loop variant keeps the held state | `cta.endcard` (`duration`), `social.frame` on 9:16; `variants.loop.override.timeline` disabling exit entries by id for a loop | any brand theme | 16:9, 9:16, 1:1 | 04, 20 |
| Credits | 1–8 min | black → roll → black | `credits.crawl` from a `sections` document (`06-credits.md`); the cards and blocks are not usable yet | `default` | 16:9 UHD | concepts/06, 15 |

Three more briefs the reels prove: a 3D title filmed through the comp's camera (`09`), a tracked label on footage (`10`: `rexx-engine track` / `motion.track` first, then `position.track`), and a real-3D element from 3d-service brought back as a 2D `video` layer between the engine's own 3D layers (`08-demos-reels.md`, P3 reel 2 scene `mass`; the three calls: write the document with the camera move and a placeholder `video` asset, `motion_convert` with `to: "camera"`, `mesh_scene_video` with that camera path, then put the clip's URL in the asset).

## Rules shared by all of them

- Plan the beat outline first (moments with times), then layers per moment, then the timeline in time order with a `label` per moment.
- One focal point at a time; hierarchy by `$theme.type.size`; holds ≥ reading time (the timing sheet says `needs 1.0s ✓`); exits shorter than entrances with `.in` eases; motion blur on fast layers; a resolved last frame for 0.5–1 s; music fades (`fadeOut` on the audio layer; `lint.duration_mismatch` otherwise).
- Music: `"markers": [{ "from": { "audio": "music", "detect": "beats", "prefix": "beat", "tempo": 120 } }]`, then `"at": "@beat4"`. Speech yields no beats; use labels, markers or word timings. Offline the detection finds nothing (`lint.beats_none`); the service analyses the file.
- Footage: `fit: "cover"`, `mute: true` under a VO, a grade adjustment above it (`stylize.vignette` with a negative `amount` darkens the edges), stroked text or a plate over it. Cutting in with `sourceIn` shifts caption timings by the same amount.
- Variants: place with `align` and percentages so a variant needs few overrides; override only `box`, `style.size`, `enabled`, caption `lines`/`group`, instance `props` and placement.
- Data in `data`; long timings in `data` assets; ids on anything you may edit later.
- Before rendering: a clean `motion.check`, `motion.frames` (`auto`, `sheet`, `trails`) to look, then the taste checklist.

## Pattern: a reusable card

`examples/concepts/04-custom-component.motion.json` is the full version (every param type, a slot, `enabled` switches). The shape of it:

```json
{ "components": { "featureCard": {
    "description": "Icon, title, and one line on a surface plate; pops in, holds, sinks out.",
    "params": { "title": { "type": "text", "default": "Feature", "maxChars": 24 }, "line": { "type": "text", "default": "", "maxChars": 60 },
                "icon": { "type": "asset", "accepts": ["svg"], "default": null }, "hold": { "type": "time", "default": 2.5 } },
    "size": [560, 320], "duration": "auto",
    "layers": [ { "id": "plate", "type": "shape", "shape": "roundedRect", "size": [560, 320], "radius": "$theme.radius.l", "fill": "$theme.color.surface", "origin": "center", "position": [280, 160] },
                { "id": "title", "type": "text", "text": "$props.title", "style": { "font": "$theme.font.display", "size": "$theme.type.size.2", "fill": "$theme.color.fg" }, "origin": "top-left", "position": [28, 104] } ],
    "timeline": [ { "target": "plate", "preset": "popIn", "at": 0 }, { "target": "title", "preset": "rise", "props": { "distance": 16 }, "at": "<0.15" },
                  { "target": ["plate", "title"], "preset": "sink", "at": "+=$props.hold" } ] } } }
```

Three instances with `in` 4.5, 5.0, 5.5 and `align`/`position` make a feature section; `ui.card-stack` is the library's ready-made version.

## Pattern: a bar meter driven by audio

`examples/concepts/10-recipe-meter.motion.json` (checked; offline the drivers rest at their floor and the beats are empty):

```json
{ "id": "meter", "type": "repeat", "count": 24,
  "layout": { "type": "stack", "direction": "row", "gap": 14, "justify": "center", "align": "end", "box": ["10%", "55%", "80%", "20%"] },
  "layer": { "type": "shape", "shape": "roundedRect", "size": [22, 120], "radius": 11, "fill": "$theme.color.accent", "origin": "bottom",
             "scale": { "value": [100, 100], "audio": { "asset": "music", "band": ["{{60 + $index * 110}}", "{{170 + $index * 110}}"], "gain": [0, 160], "smooth": 0.08, "floor": 0.05 } } } }
```

Each bar listens to its own band; `origin: "bottom"` keeps them on a baseline. A kick that pops on onsets: `"scale": { "value": [100, 100], "audio": { "asset": "music", "band": [30, 150], "gain": [45, 45], "mode": "onset", "decay": 0.3 } }`.

## Pattern: captions from a transcript

`{ "transcript": { "src": "https://…/vo.words.json", "type": "data" } }` → `"words": "$data.@transcript.words"` on any `caption.*` instance whose `in` equals the voice layer's `in` (`05-captions.md`; cookbook 06).

## Pattern: a scene sequence with library transitions

`scenes` of same-size comps joined by `{ "transition": { "type": "mitte/transition.wipe@1", "dur": 0.7, "props": { "angle": 100 } } }` or a built-in type; the root comp's own layers (music, a logo bug, captions) sit above every scene (`07-transitions.md`; cookbook 03).
