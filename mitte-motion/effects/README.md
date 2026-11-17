# SKILLS/effects: every effect, custom shaders, particles, physics, tracking

The complete reference for an AI assistant writing motion documents: the 245-id effect registry with every parameter, the `utility.shader` WGSL contract, particle layers, 2D physics and tracking. Sources of truth: the engine (`rexx-engine effects`, the `rexx-fx`, `rexx-particles`, `rexx-physics`, `rexx-track` crates) first, then spec 7, 9, 18, 19; where they disagree the code is documented and the difference is flagged as `> **Spec gap:**`.

| Page | What it covers |
|---|---|
| [01-effects-basics.md](01-effects-basics.md) | The effect instance, every parameter kind and its JSON form, groups, colour and precision, bounds and `expand`, time and seeds, reading other layers and the backdrop rules, phases, every `effect.*` diagnostic, CPU vs GPU, neutral values. |
| [10-blur-sharpen.md](10-blur-sharpen.md) | The 16 blur and sharpen effects: what each is for, patterns. |
| [11-light-glow.md](11-light-glow.md) | The 11 light effects: glow, bloom, rays, flares, leaks, energy, neon, the CC lights. |
| [12-color.md](12-color.md) | The 34 colour effects: levels, curves, grade, LUTs, maps, the CC and legalizer rows. |
| [13-generate.md](13-generate.md) | The 27 generators, the noise family and the audio-driven generators. |
| [14-distort.md](14-distort.md) | The 35 distortions, `distort.glass` and the backdrop rules. |
| [15-stylize.md](15-stylize.md) | The 44 stylize effects: shadows, outlines, glitch, halftone, dither, grain, print and CRT looks. |
| [16-keying-matte.md](16-keying-matte.md) | The 20 keyers and matte tools. |
| [17-time.md](17-time.md) | The 7 time effects: echo, posterize time, displacement, strobe, difference. |
| [18-transition.md](18-transition.md) | The 18 transition effects (`completion` 0 = visible, 100 = hidden). |
| [19-perspective.md](19-perspective.md) | The 7 perspective effects: bevels, 3D shadow, sphere, cylinder, environment. |
| [20-utility-controls.md](20-utility-controls.md) | The 8 expression controls, the 18 utility effects, the 38 blend-mode names. |
| [30-shader.md](30-shader.md) | `utility.shader` in depth: the instance, the exact prologue and bindings, `uv`/`t`/`rexx`/`params`/`input`/`inputN`/`samp`, premultiplied colour, the sandbox and every `effect.shader_invalid` reason, budgets, CPU boxes, limits. |
| [31-shader-gallery.md](31-shader-gallery.md) | Seven shaders (tint, ripple, CRT, chromatic aberration, two-input blend, time-driven noise, a mask from a second layer), each checked on the GPU backend and rendered. |
| [40-particles-layer-emitters.md](40-particles-layer-emitters.md) | The particles layer, systems, every emitter type and field, emission and bursts. |
| [41-particles-properties-physics.md](41-particles-properties-physics.md) | Particle properties, sprites and textures, physics (gravity, air, turbulence, attractors, vortices, bounce, fields), the aux system. |
| [42-particles-render-lines-form-presets.md](42-particles-render-lines-form-presets.md) | Render settings, connecting lines, Form fields, explode and assemble, the 16 presets with their props, determinism, limits, what is not implemented, export. |
| [50-physics-world-bodies.md](50-physics-world-bodies.md) | The physics world, bodies, every collider kind (hull, decompose, alpha contours, masks, animated mattes), text bodies, static and kinematic bodies. |
| [51-physics-forces-joints.md](51-physics-forces-joints.md) | Impulse, explosion, the fields (wind with turbulence, attractor, vortex, drag), the joints (hinge, rope, spring, weld, chain). |
| [52-physics-handoff-bake-art-direction.md](52-physics-handoff-bake-art-direction.md) | The keyframe-to-physics hand-off, the bake and the keys form, settle, seeds and variations, locking a take, limits, every `physics.*` diagnostic, export. |
| [60-tracking-tool.md](60-tracking-tool.md) | `motion.track`: the six track types, every request field, items, options, corrections, output, diagnostics, worked requests. |
| [61-tracking-files.md](61-tracking-files.md) | The track file: envelope, flags, the sample layout per type, camera extras, the 26 face landmarks, determinism and caching. |
| [62-tracking-documents.md](62-tracking-documents.md) | Attaching graphics: `track` on a property, `pin`, `stabilize`, camera `solve` and anchors, face tracks, the document diagnostics. |
| [90-catalogue.md](90-catalogue.md) | Generated index of all 245 ids: After Effects equivalent, phase, status, tiling, inputs, time, device, note. |
| `91-catalogue-<category>.md` | Generated: every parameter of every effect (type, default, range, animatable, doc), per category (`blur`, `light`, `color-1/2`, `generate-1/2`, `distort-1/2`, `stylize-1/2`, `keying`, `time`, `transition`, `perspective`, `utility`). |

`examples/` holds one checked document per page (`<family>-family.motion.json`, `shader-*.motion.json`, `particles-*.motion.json`, `physics-*.motion.json`, `tracking-*.motion.json`) and, under `examples/assets/`, the three track files the tracking examples use. `scripts/skills-effects-check-examples.sh` checks every example with `rexx-engine check` (shader examples with `--backend gpu`, tracking examples through an assets manifest) and renders one GPU frame of each shader with `--render`; `scripts/skills-effects-catalogue.py` regenerates the `90-`/`91-` pages from `rexx-engine effects` (`--check` diffs them).
