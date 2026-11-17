# SKILLS: the complete rexx reference for AI assistants

Start here. These pages are the reference an assistant reads before it writes a motion document or calls a
`motion.*` tool on a user's behalf: every field, option, effect, tool input, diagnostic code and library entry the
code accepts, with its type, unit, default, range and a checked example. They are generated from and verified
against the engine and service sources (engine 0.1.49); nothing here is aspirational.

## What rexx is, in ten lines

1. rexx is mitte's motion graphics engine and service: a **motion document** (one JSON object, `"motion": 1`) in, video or stills out.
2. The document model is After Effects': comps, layers, keyframes with temporal and spatial eases, masks, track mattes, 38 blend modes, effects, text animators, 2.5D cameras and lights, motion blur.
3. The authoring sugar is GSAP-shaped: tweens on a `timeline` with a position parameter, named eases, staggers, presets, components, themes, `$data` templates, percentages and `align`.
4. The engine (`rexx-engine`, Rust) normalizes the authored form to a canonical one (tweens to keys, presets, components, themes, references, placement, transitions, tracks, physics), validates, lints, renders, encodes with a pinned ffmpeg, converts to and from Lottie/dotLottie/After Effects/SVG, and tracks video.
5. It is deterministic: the same canonical document, assets and engine version give identical bytes on any box, in any frame order; no network, no clock, no wall-time randomness (seeds everywhere).
6. The service (`rexx`) exposes five tools: `motion.check`, `motion.frames`, `motion.render`, `motion.convert`, `motion.track`; it fetches `https:` assets, runs the engine in a sandbox, uploads outputs, caches renders by content, bills and quotas.
7. The workflow is read this skill → write → check (errors block, warnings never do; stats, estimate, timing sheet) → frames (look before rendering) → render (one file per variant) → convert or track when the deliverable asks for it.
8. 245 effect ids (`blur.*`, `light.*`, `color.*`, `generate.*`, `distort.*`, `stylize.*`, `keying.*`, `matte.*`, `time.*`, `transition.*`, `perspective.*`, `control.*`, `utility.*` including a sandboxed WGSL `utility.shader`), particle layers, a 2D physics world with joints and fields, and point/planar/mask/stabilize tracking are built.
9. The library (`mitte/…@1`) ships 10 themes, 9 presets and 103 components (titles, lower thirds, captions, credits, backgrounds, data, transitions, …); `library/90-catalogue.md` is the only source of valid references and their params.
10. Every problem is a diagnostic `{ severity, code, message, path, hint, fix? }` with a stable `area.name` code; unknown fields are errors everywhere, so copy shapes from these pages rather than guessing.

## Reading order

1. **this page**, then [language/01-document.md](language/01-document.md): the two forms of the document, ids, references, time values, value types and every limit;
2. [tools/00-overview.md](tools/00-overview.md): the five tools, the workflow, the HTTP envelopes, admission and quotas;
3. [library/00-overview.md](library/00-overview.md): the library, reference syntax, `library:` assets, how the catalogue is served;
4. [effects/01-effects-basics.md](effects/01-effects-basics.md): the effect instance, parameter kinds, bounds, time, seeds, GPU vs CPU;
5. then the page for what you are doing: tweens and eases ([language/02](language/02-keys-and-eases.md), [03](language/03-timeline-and-tweens.md)), text ([language/08](language/08-text.md)), components and themes ([language/13](language/13-components-themes-data.md), [library/03](library/03-components-using.md)), output ([language/14](language/14-color-and-output.md), [tools/13](tools/13-motion-render.md)), shaders ([effects/30](effects/30-shader.md)), physics ([effects/50](effects/50-physics-world-bodies.md)), tracking ([effects/60](effects/60-tracking-tool.md)), diagnostics ([tools/30](tools/30-diagnostics.md), [31](tools/31-diagnostics-2.md), [32](tools/32-lint.md)).

The `9N-*` pages of each area are generated catalogues (every schema type, every effect parameter, every tool
schema, every library entry) for lookup, not reading.

## Page index

<!-- gen:skills-index:start -->

### `language/`: SKILLS/language: the motion document, every field

| Page | One line |
|---|---|
| [language/README.md](language/README.md) | the area's own index, sources and spec-gap summary |
| [language/01-document.md](language/01-document.md) | 01. The document: top level, ids, references, assets, time, variants, values, limits |
| [language/02-keys-and-eases.md](language/02-keys-and-eases.md) | 02. Keyframes, eases, motion paths, loops, separate dimensions, layer timing, motion blur |
| [language/03-timeline-and-tweens.md](language/03-timeline-and-tweens.md) | 03. The timeline: tweens, the position parameter, targets, property names, text-unit tweens, staggers, crawl |
| [language/04-presets-and-drivers.md](language/04-presets-and-drivers.md) | 04. Presets (using, defining, every built-in), drivers, and the data bindings on keys |
| [language/05-layers.md](language/05-layers.md) | 05. Layers: every type, every common field, the transform, placement, safe areas, styles, auto-orient, type-specific fields |
| [language/06-transitions-and-scenes.md](language/06-transitions-and-scenes.md) | 06. Transitions: `transitionIn` / `transitionOut`, scene sequences, the whole catalog |
| [language/07-shapes.md](language/07-shapes.md) | 07. Shapes: every item kind, evaluation order, the path value, paints, gradients, morphing, every operator, authoring sugar, `fitTo` |
| [language/08-text.md](language/08-text.md) | 08. Text: the text value, character and paragraph style, fonts, text on a path, animators and selectors, 3D per character, captions |
| [language/09-masks-mattes-blending.md](language/09-masks-mattes-blending.md) | 09. Masks, track mattes, preserve transparency, adjustment layers, collapse, the 38 blend modes, the no-clamp rule |
| [language/10-3d.md](language/10-3d.md) | 10. 3D: layers and materials, cameras and depth of field, camera sugar, lights, the classic renderer, ordering, nested comps |
| [language/11-media-and-audio.md](language/11-media-and-audio.md) | 11. Media and audio: interpretation, image and video layers, sequences, Lottie and SVG sources, audio layers, the mixdown, ducking, analysis, captions input |
| [language/12-expressions.md](language/12-expressions.md) | 12. Expressions: the whole subset, every function and object the host provides |
| [language/13-components-themes-data.md](language/13-components-themes-data.md) | 13. Themes, data and templates, components, repeat, layout |
| [language/14-color-and-output.md](language/14-color-and-output.md) | 14. Colour and output: writing colours, working colour, input colour, output transforms, the whole `output` block |
| [language/15-property-index.md](language/15-property-index.md) | 15. The property index: addressing any property, units, ranges and clamps, what animates, authored-only constructs |
| [language/90-schema-reference.md](language/90-schema-reference.md) | 90. Schema reference: every type |
| [language/91-animatable-paths.md](language/91-animatable-paths.md) | 91. Every animatable property path |
| [language/92-schema-types-1.md](language/92-schema-types-1.md) | 92.1 Schema types `AcceptsShadows` … `AnimatedValue2` |
| [language/92-schema-types-2.md](language/92-schema-types-2.md) | 92.2 Schema types `AnimatedValue3` … `BodyType` |
| [language/92-schema-types-3.md](language/92-schema-types-3.md) | 92.3 Schema types `Bounce` … `Duck` |
| [language/92-schema-types-4.md](language/92-schema-types-4.md) | 92.4 Schema types `Ease` … `GeometryBevel` |
| [language/92-schema-types-5.md](language/92-schema-types-5.md) | 92.5 Schema types `GifDither` … `Key4` |
| [language/92-schema-types-6.md](language/92-schema-types-6.md) | 92.6 Schema types `Key5` … `LineFalloff` |
| [language/92-schema-types-7.md](language/92-schema-types-7.md) | 92.7 Schema types `LineJoin` … `OutputFormat` |
| [language/92-schema-types-8.md](language/92-schema-types-8.md) | 92.8 Schema types `OutputQuality` … `Safe` |
| [language/92-schema-types-9.md](language/92-schema-types-9.md) | 92.9 Schema types `SafeBox` … `StopsOrGradient` |
| [language/92-schema-types-10.md](language/92-schema-types-10.md) | 92.10 Schema types `StrokeOrder` … `Vortex` |
| [language/92-schema-types-11.md](language/92-schema-types-11.md) | 92.11 Schema types `Wall` … `ZigzagPer` |

### `tools/`: SKILLS/tools: the `motion.*` tools, every option, every code

| Page | One line |
|---|---|
| [tools/README.md](tools/README.md) | the area's own index, sources and spec-gap summary |
| [tools/00-overview.md](tools/00-overview.md) | 00 · The rexx service and the `motion.*` tools |
| [tools/01-documents-and-assets.md](tools/01-documents-and-assets.md) | 01 · Documents, `doc_url`, `library:` URIs, `data`, variants, assets |
| [tools/11-motion-check.md](tools/11-motion-check.md) | 11 · `motion.check` |
| [tools/12-motion-frames.md](tools/12-motion-frames.md) | 12 · `motion.frames` |
| [tools/13-motion-render.md](tools/13-motion-render.md) | 13 · `motion.render` |
| [tools/14-motion-convert.md](tools/14-motion-convert.md) | 14 · `motion.convert` |
| [tools/15-motion-track.md](tools/15-motion-track.md) | 15 · `motion.track` |
| [tools/16-render-pipeline.md](tools/16-render-pipeline.md) | 16 · The render pipeline: estimate, backends, the cache, chunking, HDR, NVENC |
| [tools/30-diagnostics.md](tools/30-diagnostics.md) | 30 · Diagnostics: the format, the exit classes, and the document codes |
| [tools/31-diagnostics-2.md](tools/31-diagnostics-2.md) | 31 · Diagnostics: assets, effects, expressions, limits, tracking, physics, render, media, output, encode, convert |
| [tools/32-lint.md](tools/32-lint.md) | 32 · Lint: every rule, its threshold and its fix |
| [tools/33-codes-inventory.md](tools/33-codes-inventory.md) | 33 · Diagnostic code inventory (generated) |
| [tools/40-limits.md](tools/40-limits.md) | 40 · Limits, caps and budgets in one place |
| [tools/50-engine-cli.md](tools/50-engine-cli.md) | 50 · The engine CLI: `rexx-engine` |
| [tools/60-service-config.md](tools/60-service-config.md) | 60 · Service configuration, health and metrics |
| [tools/90-schemas.md](tools/90-schemas.md) | 90 · The registry: schemas, instructions, examples (generated) |
| [tools/91-schema-check.md](tools/91-schema-check.md) | Registry entry: `motion.check` (generated) |
| [tools/92-schema-frames.md](tools/92-schema-frames.md) | Registry entry: `motion.frames` (generated) |
| [tools/93-schema-render.md](tools/93-schema-render.md) | Registry entry: `motion.render` (generated) |
| [tools/94-schema-convert.md](tools/94-schema-convert.md) | Registry entry: `motion.convert` (generated) |
| [tools/95-schema-track.md](tools/95-schema-track.md) | Registry entry: `motion.track` (generated) |

### `library/`: SKILLS / library: the complete reference of the rexx library for AI assistants

| Page | One line |
|---|---|
| [library/README.md](library/README.md) | the area's own index, sources and spec-gap summary |
| [library/00-overview.md](library/00-overview.md) | what the library is, reference syntax and versions, where the engine finds it, `library:` assets, the catalogue, diagnostics, checking a document locally |
| [library/01-themes.md](library/01-themes.md) | the theme object and merge order, every token group and token, derived tokens and color modifiers, springs, textures, styles, brand kits, the ten themes compared and every value |
| [library/02-presets.md](library/02-presets.md) | using presets, the three library packs, the built-in names, writing a preset, every rule the engine enforces |
| [library/03-components-using.md](library/03-components-using.md) | instances: `use`, `props`, `slots`, `in`/`out`, `collapse`; param validation; what normalization produces; placement; variants; repeats of instances; nesting; engine-backed components |
| [library/04-components-writing.md](library/04-components-writing.md) | the definition format, every param type, structure switches, slots and forwarding, the `x-library` file and examples file, testing, review and versioning |
| [library/05-captions.md](library/05-captions.md) | the four `caption.*` components: shared params, per-style defaults, the word-timings input, what the engine builds and what it does not yet |
| [library/06-credits.md](library/06-credits.md) | the eight `credits.*` components: the sections document, shared style params, crawl speed and duration, what the engine builds |
| [library/07-transitions.md](library/07-transitions.md) | transitions as components in `scenes`, by hand, and how to write one; the 14 shipped transition components |
| [library/08-demos-reels.md](library/08-demos-reels.md) | every `library:mitte/demo/…` asset and the three reels scene by scene with the constructs to copy |
| [library/09-sound-fonts.md](library/09-sound-fonts.md) | the planned sound pack (not shipped) and every font family with license, roles, scripts and build |
| [library/10-recipes.md](library/10-recipes.md) | fifteen briefs as patterns mapped to the components that ship and to the cookbook |
| [library/11-cookbook-1.md](library/11-cookbook-1.md) | Cookbook 1: ten complete documents for common briefs |
| [library/12-cookbook-2.md](library/12-cookbook-2.md) | Cookbook 2: ten more complete documents |
| [library/90-catalogue.md](library/90-catalogue.md) | generated index of every entry (themes, presets, components by group) |
| [library/91-components-backgrounds.md](library/91-components-backgrounds.md) | Catalogue: Backgrounds components |
| [library/91-components-captions.md](library/91-components-captions.md) | Catalogue: Captions components |
| [library/91-components-credits.md](library/91-components-credits.md) | Catalogue: Credits components |
| [library/91-components-data.md](library/91-components-data.md) | Catalogue: Data components |
| [library/91-components-explainers.md](library/91-components-explainers.md) | Catalogue: Explainers components |
| [library/91-components-logo.md](library/91-components-logo.md) | Catalogue: Logo components |
| [library/91-components-lower-thirds.md](library/91-components-lower-thirds.md) | Catalogue: Lower thirds components |
| [library/91-components-maps.md](library/91-components-maps.md) | Catalogue: Maps, callouts and layouts components |
| [library/91-components-music.md](library/91-components-music.md) | Catalogue: Music components |
| [library/91-components-overlays.md](library/91-components-overlays.md) | Catalogue: Overlays components |
| [library/91-components-particles.md](library/91-components-particles.md) | Catalogue: Particles components |
| [library/91-components-social.md](library/91-components-social.md) | Catalogue: Social components |
| [library/91-components-titles.md](library/91-components-titles.md) | Catalogue: Titles components |
| [library/91-components-transitions.md](library/91-components-transitions.md) | Catalogue: Transitions components |
| [library/91-components-ui.md](library/91-components-ui.md) | Catalogue: UI and product components |
| [library/92-themes.md](library/92-themes.md) | generated: every token of every theme |
| [library/93-presets.md](library/93-presets.md) | generated: every preset with params and tweens |

### `effects/`: SKILLS/effects: every effect, custom shaders, particles, physics, tracking

| Page | One line |
|---|---|
| [effects/README.md](effects/README.md) | the area's own index, sources and spec-gap summary |
| [effects/01-effects-basics.md](effects/01-effects-basics.md) | Effects: the instance, the parameters, the rules |
| [effects/10-blur-sharpen.md](effects/10-blur-sharpen.md) | Blur & sharpen |
| [effects/11-light-glow.md](effects/11-light-glow.md) | Light & glow |
| [effects/12-color.md](effects/12-color.md) | Color |
| [effects/13-generate.md](effects/13-generate.md) | Generate (and the noise and audio-driven generators) |
| [effects/14-distort.md](effects/14-distort.md) | Distort (including glass and the backdrop rules) |
| [effects/15-stylize.md](effects/15-stylize.md) | Stylize |
| [effects/16-keying-matte.md](effects/16-keying-matte.md) | Keying & matte |
| [effects/17-time.md](effects/17-time.md) | Time |
| [effects/18-transition.md](effects/18-transition.md) | Transition |
| [effects/19-perspective.md](effects/19-perspective.md) | Perspective |
| [effects/20-utility-controls.md](effects/20-utility-controls.md) | Utility and expression controls |
| [effects/30-shader.md](effects/30-shader.md) | `utility.shader`: custom WGSL effects |
| [effects/31-shader-gallery.md](effects/31-shader-gallery.md) | Shader gallery: seven checked, rendered `utility.shader` effects |
| [effects/40-particles-layer-emitters.md](effects/40-particles-layer-emitters.md) | Particles 1: the layer, systems, emitters, emission |
| [effects/41-particles-properties-physics.md](effects/41-particles-properties-physics.md) | Particles 2: particle properties, sprites, physics, the aux system |
| [effects/42-particles-render-lines-form-presets.md](effects/42-particles-render-lines-form-presets.md) | Particles 3: rendering, connecting lines, Form fields, explode and assemble, presets, limits, export |
| [effects/50-physics-world-bodies.md](effects/50-physics-world-bodies.md) | 2D physics 1: the world and the bodies |
| [effects/51-physics-forces-joints.md](effects/51-physics-forces-joints.md) | 2D physics 2: forces, fields, joints |
| [effects/52-physics-handoff-bake-art-direction.md](effects/52-physics-handoff-bake-art-direction.md) | 2D physics 3: the hand-off, the bake, settle, seeds and locks, limits, diagnostics |
| [effects/60-tracking-tool.md](effects/60-tracking-tool.md) | Tracking 1: `motion.track`, the track types, inputs and corrections |
| [effects/61-tracking-files.md](effects/61-tracking-files.md) | Tracking 2: the track file |
| [effects/62-tracking-documents.md](effects/62-tracking-documents.md) | Tracking 3: using tracks in documents |
| [effects/90-catalogue.md](effects/90-catalogue.md) | The effect catalogue: index |
| [effects/91-catalogue-blur.md](effects/91-catalogue-blur.md) | Blur & sharpen: every parameter |
| [effects/91-catalogue-color-1.md](effects/91-catalogue-color-1.md) | Color: every parameter (part 1 of 2) |
| [effects/91-catalogue-color-2.md](effects/91-catalogue-color-2.md) | Color: every parameter (part 2 of 2) |
| [effects/91-catalogue-distort-1.md](effects/91-catalogue-distort-1.md) | Distort: every parameter (part 1 of 2) |
| [effects/91-catalogue-distort-2.md](effects/91-catalogue-distort-2.md) | Distort: every parameter (part 2 of 2) |
| [effects/91-catalogue-generate-1.md](effects/91-catalogue-generate-1.md) | Generate: every parameter (part 1 of 2) |
| [effects/91-catalogue-generate-2.md](effects/91-catalogue-generate-2.md) | Generate: every parameter (part 2 of 2) |
| [effects/91-catalogue-keying.md](effects/91-catalogue-keying.md) | Keying & matte: every parameter |
| [effects/91-catalogue-light.md](effects/91-catalogue-light.md) | Light & glow: every parameter |
| [effects/91-catalogue-perspective.md](effects/91-catalogue-perspective.md) | Perspective: every parameter |
| [effects/91-catalogue-stylize-1.md](effects/91-catalogue-stylize-1.md) | Stylize: every parameter (part 1 of 2) |
| [effects/91-catalogue-stylize-2.md](effects/91-catalogue-stylize-2.md) | Stylize: every parameter (part 2 of 2) |
| [effects/91-catalogue-time.md](effects/91-catalogue-time.md) | Time: every parameter |
| [effects/91-catalogue-transition.md](effects/91-catalogue-transition.md) | Transition: every parameter |
| [effects/91-catalogue-utility.md](effects/91-catalogue-utility.md) | Utility and expression controls: every parameter |

<!-- gen:skills-index:end -->

## Conventions

- **Sources of truth**, in order: the code (`engine/crates`, `service/src`), the machine-readable outputs
  (`rexx-engine effects`, `engine/schema/motion-1.json`, `library/index.json`, the service's `/v1/registry`), then
  `docs/spec` and `docs/proposal` (the contract), then `SKILL.md`.
- **`> **Spec gap:**` notes** mark where the code and the contract disagree; the page documents the code. Every note
  is collected in [SPEC-GAPS.md](SPEC-GAPS.md), grouped by chapter, for the next docs sync.
- **Generated sections** sit between `<!-- gen:<name>:start -->` / `<!-- gen:<name>:end -->` markers (or are whole
  generated files) and come from `scripts/skills-*.py`; edit the generator, not the text. Hand-written sections still
  name every item, which the completeness check enforces.
- **Examples** are files under `<area>/examples/`, each a complete document (or a tool input) that the area's checker
  runs through `rexx-engine check` (and tool inputs through the published schemas): zero errors; the warnings an
  example is expected to raise are named in its page (the library examples list them in `meta.x-skills.expectWarnings`).
- **`python3 scripts/check-skills.py --engine <rexx-engine>`** runs every generator in `--check` mode, every example
  checker, and the completeness check (every effect id, every schema type and field, every tool input field, every
  diagnostic code, every library entry must appear in these pages); CI runs it in the engine gate.
  `--fix` runs the generators in write mode after changing effects, the schema, the tools, the codes or the library.
- **Units and casing**: document fields are lowerCamelCase, tool inputs snake_case; `opacity` 0–100, `scale` percent,
  `rotation` degrees, times in seconds unless a `"12f"` / `"@marker"` / `"50%"` string says otherwise.
