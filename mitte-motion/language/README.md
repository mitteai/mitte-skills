# SKILLS/language: the motion document, every field

The complete reference of the rexx motion document for an AI assistant that writes documents and calls the `motion.*` tools: every field, type, unit, default, range, enum value, what each option does, which diagnostic refuses what, and a checked example per concept. Sources of truth, in order: the engine code (`engine/crates`, engine 0.1.48), `engine/schema/motion-1.json`, `docs/spec/01…17`, then `SKILL.md`. Where the code and the spec disagree, the page documents the code and marks it with a `> **Spec gap:**` note. The effects catalog, the `motion.*` tool contracts and the library catalog are separate areas (`SKILLS/effects`, `SKILLS/tools`, `SKILLS/library`).

| Page | Covers |
|---|---|
| [01-document.md](01-document.md) | the two forms, the top-level object, ids, property paths and `$` references, the asset object, time values and markers, variants, value types and After Effects units, the animatable-value shapes and evaluation order, every limit, the minimal document and its canonical form |
| [02-keys-and-eases.md](02-keys-and-eases.md) | keyframes, every ease form and every catalog name with parameters, After Effects speed/influence, springs, interpolation per property kind, motion paths, roving keys, loops, layer timing, motion blur, separate dimensions |
| [03-timeline-and-tweens.md](03-timeline-and-tweens.md) | tweens (every field, relative values), the position parameter, targets, property-name shorthands, how tweens become keys, text-unit tweens, staggers, crawl |
| [04-presets-and-drivers.md](04-presets-and-drivers.md) | using and defining presets, all 54 built-in presets with their parameters as the engine defines them, every driver, the `keys` list binding and `keys.fromAudio` |
| [05-layers.md](05-layers.md) | every layer type, every common field, the transform and parenting, default anchors and bounds, percentages / `origin` / `align` / measure time, safe areas and platform presets, auto-orient, the nine layer styles, the per-layer pipeline, the type-specific fields of solid, image, video, audio, comp, null, adjustment |
| [06-transitions-and-scenes.md](06-transitions-and-scenes.md) | `transitionIn` / `transitionOut`, `scenes` sequences, the whole transition catalog with what each compiles to |
| [07-shapes.md](07-shapes.md) | every shape item kind, the evaluation order, the path value and SVG path data, paints (taper, wave, dashes), the gradient value, path morphing, every operator, shape presets, SVG import, `fitTo`, `points` from data |
| [08-text.md](08-text.md) | the text value and spans, every character and paragraph style field, the font pack and resolution, text on a path, animators (every property, every selector type), grouping, per-character 3D, unit addressing, source-text animation, `words` captions, measuring |
| [09-masks-mattes-blending.md](09-masks-mattes-blending.md) | masks (every field, shape masks, modes), track mattes, preserve transparency, adjustment layers, collapse transformations, all 38 blend modes with formulas, the no-clamp rule, the order of operations |
| [10-3d.md](10-3d.md) | 3D layers and materials, cameras and depth of field, the camera sugar (orbit, dolly, dollyZoom, handheld), lights, the classic renderer, 3D/2D ordering, nested comps, the interchange-only fields |
| [11-media-and-audio.md](11-media-and-audio.md) | asset interpretation, image and video semantics, which frame shows, frame blending incl. flow, sequences, Lottie and SVG as sources, audio layers, the mixdown and master, ducking, audio analysis, captions input, media limits |
| [12-expressions.md](12-expressions.md) | the expression language: values, grammar, vector arithmetic, every object-model member, every function, randomness, budgets and errors, idioms, what is not supported |
| [13-components-themes-data.md](13-components-themes-data.md) | themes (every token group, derived tokens, colour modifiers, brand kits), data and the whole template grammar (formats, functions), components (definition, every param type, instances, slots, versioning), repeat, layout |
| [14-color-and-output.md](14-color-and-output.md) | every colour form, working colour, input colour, output transforms (SDR, tone mapping incl. `aces2`, gamut mapping, dither, chroma, HDR), the complete `output` block, quality presets, NVENC, destinations |
| [15-property-index.md](15-property-index.md) | writing a path in each place, units / clamp ranges / defaults per property kind, what animates how, every authored-only and canonical-only construct |
| [90-schema-reference.md](90-schema-reference.md) | generated: the root object and an index of every schema type |
| [91-animatable-paths.md](91-animatable-paths.md) | generated: every animatable property path reachable from each top-level object |
| [92-schema-types-1.md](92-schema-types-1.md) … [92-schema-types-11.md](92-schema-types-11.md) | generated: every type with every field, type, requiredness and description |

Generated pages come from `scripts/skills-language-schema.py` (walks `engine/schema/motion-1.json`; `--check` diffs them for CI) and are wrapped in `<!-- gen:…:start/end -->` markers.

## Examples

`examples/*.json` holds one or more complete documents per page (`NN-*.json`). Every one checks with 0 errors against engine 0.1.48 (`python3 scripts/skills-language-check-examples.py`, which runs `rexx-engine check` on each; warnings that an example is expected to raise are named in its page). Examples use the shipped `library:mitte/demo/logo@1` asset where an asset is needed, or `https:` URLs where the point is to show media fields (`check` then reports `asset.unmaterialized` infos).

## Engine-vs-spec findings recorded in the pages

- Default mask ids are `_mask<n>` (spec 17 says `mask-<n>`) ([01](01-document.md), [15](15-property-index.md)).
- `anim.ease_on_spatial_dims` is the code for a `dims` ease on a spatial property (spec 2 says `anim.dims_on_spatial`) ([02](02-keys-and-eases.md)).
- A local preset definition does not accept `kind`; preset `params` take `{ type, default, description, values, min, max }`; `PresetKind` lacks `camera`; several built-ins have parameters the spec omits; `shimmer`, `orbit` and `dollyZoom` are approximations ([04](04-presets-and-drivers.md)).
- `morph` in a transition `type` compiles to a crossfade with the warning `effect.unavailable` ([06](06-transitions-and-scenes.md)).
- `paragraph.hyphenate` / `balance` have no effect; `kerning: "optical"` is `metrics`; the text `clip` animator and per-character 3D are built ([08](08-text.md)).
- `environment` lights, non-`fast` DOF irises and the advanced-renderer fields are accepted without effect ([10](10-3d.md)).
- `layer.content(…)` resolves items by id, name or index but not by After Effects display names; the stdlib is a superset of spec 11 ([12](12-expressions.md)).
- A shape item's `enabled` is a literal boolean; the placeholder grammar has no ternary and no `indices` function; `$parent.*` resolves in `{{ }}` but not as a `$`-path segment ([13](13-components-themes-data.md)).
- `aces2`, HDR (`hlg`/`pq`), HEVC/AV1, the image and sequence formats, `encoder: "nvenc"` and `frameBlend: "flow"` are built although spec 17 phases them later; SKILL.md's "specified but not implemented" list is stale on those ([14](14-color-and-output.md), [15](15-property-index.md)).
