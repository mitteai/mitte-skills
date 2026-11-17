---
name: rexx
description: Author motion documents and call the motion.* tools (guide, check, frames, render, convert, track) for motion graphics, titles, lower thirds, captions, credits, data stories, logo stings and social ads.
metadata:
  mitte-nodes: motion.check motion.frames motion.render motion.convert motion.track
---

# rexx: motion documents in, video out

Load this when a motion.* tool is loaded. The complete reference lives in this skill's folders; this page says what rexx is, how a job runs, and where to read. Never read the catalogue pages (`9N-*`) front to back: look a thing up with `fs.search` under this skill's folder.

## What rexx is, in ten lines

1. rexx is mitte's motion graphics engine and service: a **motion document** (one JSON object, `"motion": 1`) in, video or stills out.
2. The document model is After Effects': comps, layers, keyframes with temporal and spatial eases, masks, track mattes, 38 blend modes, effects, text animators, 2.5D cameras and lights, motion blur.
3. The authoring sugar is GSAP-shaped: tweens on a `timeline` with a position parameter, named eases, staggers, presets, components, themes, `$data` templates, percentages and `align`.
4. The engine normalizes the authored form to a canonical one (tweens to keys, presets, components, themes, references, placement, transitions, tracks, physics), validates, lints, renders, encodes with a pinned ffmpeg, converts to and from Lottie/dotLottie/After Effects/SVG, and tracks video.
5. It is deterministic: the same canonical document, assets and engine version give identical bytes anywhere; no network, no clock, seeds everywhere.
6. The service exposes five tools: `motion.check`, `motion.frames`, `motion.render`, `motion.convert`, `motion.track`; it fetches `https:` assets, runs the engine in a sandbox, uploads outputs, caches renders by content, bills and quotas.
7. The workflow is guide (catalog, topics, codes) → write → check (errors block, warnings never do; stats, estimate, timing sheet) → frames (look before rendering) → render (one file per variant) → convert or track when the deliverable asks for it.
8. 245 effect ids (`blur.*`, `light.*`, `color.*`, `generate.*`, `distort.*`, `stylize.*`, `keying.*`, `matte.*`, `time.*`, `transition.*`, `perspective.*`, `control.*`, `utility.*` including a sandboxed WGSL `utility.shader`), particle layers, a 2D physics world with joints and fields, and point/planar/mask/stabilize tracking are built.
9. The library (`mitte/…@1`) ships 10 themes, 9 presets and 103 components (titles, lower thirds, captions, credits, backgrounds, data, transitions, …); `library/90-catalogue.md` is the only source of valid references and their params.
10. Every problem is a diagnostic `{ severity, code, message, path, hint, fix? }` with a stable `area.name` code; unknown fields are errors everywhere, so copy shapes from these pages rather than guessing.

## How a job runs

A motion film is a project: a folder of source files the user keeps and edits, compiled into one document, rendered by url. Never a document typed into a tool call, never one file written in one go, whatever the length.

1. **Decide what the piece is.** A brief that names the content (a lower third, a data story, captions) is built from its recipe. An open brief ("impress me", "something beautiful", "show what you can do") is a showpiece, built around one visual idea and at least three of the engine's own powers that no slideshow tool has: a WGSL shader background (`effects/30-shader.md`, `effects/31-shader-gallery.md`), particles (`effects/40-particles-layer-emitters.md` and on), a physics world with bodies and forces (`effects/50-physics-world-bodies.md` and on), real 3D layers under a moving camera and lights (`language/`), a path morph under a gradient stroke, an audio-driven property, a time effect (echo, posterize), a library transition beyond a push (glitch, lightLeak, filmBurn, morph). Words sliding in and out are not a showpiece; type, if any, comes last, large, few words, held long enough to read. The demos (`library/08-demos-reels.md`) and the example documents show syntax, never ideas: their palettes, motifs, words and scene order are not reused, and a piece that resembles the showreel (a morph with a zigzag ring and a rounded square, four cards under lights, an orb trail) is a failed brief, whatever it renders like.
2. **Read what the piece needs**: `fs.search` under this skill's folder, `language/` for the document, `library/90-catalogue.md` for every valid `mitte/…@n` reference, `library/10-recipes.md` for the shapes, the effects pages for the parameters, `tools/30-diagnostics.md` for a code.
3. **Make the project folder**: `fs.mkdir /Library/<title>` (`fs.write` creates no folders). Everything below goes in it.
4. **Write `index.md`** first, the film on one page: the title, the mood in a phrase, a palette of four or five hex colours chosen for this piece (never the default theme's, never a demo's), the theme, one motif that recurs, then the scenes in order as a table: scene id, seconds, what happens, which engine powers carry it, and the transition into the next. The index is the plan the user reads and the plan every scene file follows.
5. **Write one scene file per scene**, `scenes/NN-<id>.json`, each a complete JSON object holding that comp alone: `{"comps": {"<id>": { "size": [1920, 1080], "fps": 30, "duration": …, "layers": […], "timeline": […] }}}`. One scene file per step (a step is one tool call; the next step continues). A scene file is small, so it is written whole and fixed whole.
6. **Write `main.json`**: the document's head and root comp in one object: `{"motion": 1, "meta": {…}, "theme": {…}, "assets": {…}, "data": {…}, "variants": {…}, "output": {…}, "comps": {"main": { "size", "fps", "duration": "auto", "scenes": [ {"comp": "<id>", "dur": …}, {"transition": {…}}, … ], "layers": [ music, grain ] }}}`. A generated or library file (the music, a clip, a logo) goes into `assets` by its `@url_…` reference as its `src`; the reference becomes the real url when the file is saved, so never write a url by hand.
7. **Compile with `fs.merge_json`**: `{"paths": ["main.json", "scenes/01-….json", "scenes/02-….json", …], "path": "/Library/<title>/<title>.motion.json"}`. The merge is a deep merge of objects, so every scene lands under one `comps` next to `main` with no commas, heads or tails to get right. A fix is one scene file rewritten and the same `fs.merge_json` into `file:<id>` of the document, which becomes its next version.
8. **`motion.check`** the compiled document by `doc_url`, always, before frames or render. Fix every error, then weigh the warnings; read the estimate and the timing sheet. The tools take no inline document from the assistant.
9. **`motion.frames`** with `sheet: true` (a contact sheet, 1920 px wide by default; `width` sets it) to look before rendering.
10. **`motion.render`**, one file per variant, by `doc_url`. `motion.convert` or `motion.track` only when the deliverable asks.

The folder the user ends with:

```
/Library/Orbit launch film/
  index.md
  main.json
  scenes/01-logo.json
  scenes/02-headline.json
  …
  Orbit launch film.motion.json
  Orbit launch film.mp4
```

## Where to read

Each folder has its own `README.md` index with one line per page; [README.md](README.md) at the root is the whole index and the reading order.

| folder | what it holds | start with |
|---|---|---|
| `language/` | the motion document, every field: document, keys and eases, timeline and tweens, presets and drivers, layers, transitions and scenes, shapes, text, masks and blending, 3D, media and audio, expressions, components and themes, colour and output, the property index | `language/01-document.md` |
| `tools/` | the five tools, every option and every diagnostic code, the render pipeline, lint, limits | `tools/00-overview.md` |
| `library/` | themes, presets, every component by group, captions, credits, transitions, demos, two cookbooks of complete documents | `library/00-overview.md`, then `library/10-recipes.md` |
| `effects/` | the effect instance, every family (blur, light, colour, generate, distort, stylize, keying, time, transition, perspective, utility), shaders, particles, physics, tracking | `effects/01-effects-basics.md` |

The `9N-*` pages of each folder are generated catalogues (every schema type, every effect parameter, every tool schema, every library entry) for lookup, not reading. Examples under each folder's `examples/` are checked documents to copy shapes from.
