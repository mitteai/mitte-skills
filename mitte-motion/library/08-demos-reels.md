# Demo assets and the reels: what ships under `library:mitte/demo/…` and what each scene uses

> These are the engine's demonstrations: what each feature looks like when it runs. They are syntax to copy and ideas not to: a new piece picks its own palette, motifs, words and scene order, and an open brief that reproduces a reel scene has failed the brief.

Everything under `library/mitte/assets/demo/` ships in the engine image and is reachable offline as `library:mitte/demo/<stem>@1` (an asset `src`, a layer's `asset`, or the service's `doc_url` for a `.motion.json`). The documents are the playground's examples and three capability reels; they are the best source of constructs to copy because every one of them renders today. Scene-by-scene notes come from each document's `meta.notes`.

## Every file

| Reference (`library:mitte/demo/…@1`) | File | Size | What it is |
|---|---|---|---|
| `title-card` | `title-card.motion.json` | 3 KB | The playground's example document: `mitte/midnight@1`, a kicker, a two-line headline, a templated subtitle from `data`, an accent bar, two beat markers, `vertical` and `square` variants. Every `motion.*` tool example uses it or the lower third. |
| `lower-third` | `lower-third.motion.json` | 1 KB | The transparent example: no comp background, `mitte/lower-third.bar@1` on `mitte/clean@1` and a glowing accent dot, for ProRes 4444 / HEVC-alpha renders and Lottie, dotLottie and After Effects export. |
| `logo` | `logo.svg` | 665 B | The mitte mark as an SVG; `{ "src": "library:mitte/demo/logo@1", "type": "svg" }` for `fromSvg`, `logo.*` components, `particles.form-logo`. |
| `badge` | `badge.lottie` | 1 KB | A small dotLottie for `lottie` layers and Lottie import tests. |
| `tracking-clip` | `tracking-clip.mp4` | 276 KB | 960 × 540, 30 fps, 6 s: a bright tag moving over a textured plate (point track at `[240, 300]` in frame 0), a dark card drifting and rotating (planar, corners `[[510,180],[770,180],[770,360],[510,360]]`), inside a shaking camera (stabilize). Rendered from `tracking-clip-source.motion.json`. |
| `tracking-clip-source` | `tracking-clip-source.motion.json` | 4 KB | The clip's source document (`mitte/midnight@1`, a `scene` precomp inside a camera layer). |
| `classic-3d` | `classic-3d.motion.json` | 5 KB | 3D layers under a camera: cards in depth, a camera move, auto-orientation along a path; 4 s. |
| `data-story` | `data-story.motion.json` | 18 KB | A data-driven explainer in canonical form: chart shapes, counters and labels on a timeline; 10 s. |
| `glass-loop` | `glass-loop.motion.json` | 7 KB | A looping hero: blurred, refracted glass panels (`distort.glass`, `blur.gaussian`) over a `generate.meshGradient`; 8 s, loops cleanly. |
| `glow` | `glow.motion.json` | 6 KB | Deep-glow bloom on HDR-bright shapes and text in linear light (`light.glow` × 5, `light.bloom`, `color.tritone`, `key.unmult`, `generate.fractalNoise`), `toneMap: "soft"`; 3 s. |
| `kinetic-quote` | `kinetic-quote.motion.json` | 11 KB | Kinetic typography: a manifesto word by word with staggers, emphasis presets, grain and vignette adjustments, a rig null; 12 s. |
| `reels-presets` | `reels-presets.motion.json` | 7 KB | Exit, emphasis and loop presets on a 1080 × 1920 comp with Reels safe areas, two repeats; 4 s. |
| `text-on-path` | `text-on-path.motion.json` | 5 KB | Text set along a curve with a range animator and a mask; 4 s. |
| `trim-paths` | `trim-paths.motion.json` | 5 KB | Strokes revealed with trim paths and the draw presets; 3 s. |
| `showreel` | `showreel.motion.json` | 71 KB | The playground showpiece: six scenes, 25.2 s, below. |
| `p3-reel` | `p3-reel.motion.json` | 77 KB | The P3 reel: seven scenes, 24.3 s, below. |
| `p3-reel-2` | `p3-reel-2.motion.json` | 639 KB | The second P3 reel: five scenes, 20.4 s, below; its footage and data in `p3-reel-2/`. |
| `p3-reel-2/amp` | `p3-reel-2/amp.png` (+ `amp-source.motion.json`) | 29 KB | A transparent ampersand rendered from text (Abril Fatface) with `rexx-engine frames --transparent`, used as a traced-contour physics collider. |
| `p3-reel-2/courtyard` | `p3-reel-2/courtyard.mp4` (+ `courtyard-source.motion.json`, 102 KB) | 1.7 MB | Engine-made footage: a classic-3D courtyard of 240 lit tile cards filmed by a moving two-node camera, 1920 × 1080, 30 fps, 4.6 s. |
| `p3-reel-2/courtyard-cam` | `p3-reel-2/courtyard-cam.json` | 25 KB | Its camera solve from `rexx-engine track` (type `camera`, four floor picks; 155 points, 0.70 px mean reprojection). |
| `p3-reel-2/mass3d` | `p3-reel-2/mass3d.webm` (+ `mass3d-scene.json`) | 1.5 MB | A 3d-service clip with alpha (VP9): eight primitives tumbling, filmed through this document's exported camera path. |
| `p3-reel-2/bloom` | `p3-reel-2/bloom.json` | 4 KB | A hand-made Lottie (counter-rotating repeater petal rings and a pulsing heart) imported as footage. |
| `p4-reel` | `p4-reel.motion.json` | 51 KB | The P4 reel: five scenes with HDR highlights, 22.6 s, below. |
| `p4-reel/tumble` | `p4-reel/tumble.mp4` (+ `tumble-source.motion.json`) | 446 KB | Engine-made footage of 2D physics bodies thrown through a frame, rendered at 15 fps for the frame-blend comparison. |

The service also exposes `library:mitte/demo/showreel@1` and friends as `doc_url` values, so a render can be started from a demo without pasting it.

## The showreel (`showreel.motion.json`, 25.2 s, 1080p30)

Scenes cut with layer transitions (`push`, `glitch`, `lightLeak`, `zoom`, `blurDissolve`), motion blur on (`shutterAngle` 180), `toneMap: "soft"`, a `grain` adjustment layer over everything in the main comp; no captions. Constructs to copy:

| Scene (dur) | What it shows | Constructs |
|---|---|---|
| `letters` (5.4) | four half-second word beats with background cuts, then the line assembles and MOTION becomes six rigid bodies that tumble, pile up, scatter in an explosion and settle back into the layout | per-word tweens from huge (`kinetic.slam`-style), whip in/out per letter, `trackIn` + zoom, 3D letter flips; physics: `dynamic` bodies on text, an `explosion` force at 3.5 s, `settle` back to the layout |
| `lit` (3.8) | four cards and a disc on a rotating 3D null under a spot light and a drifting point light, shadows on a floor, a two-node camera dollying in with a depth-of-field focus pull | `threeD` layers, `light` layers with shadows, `camera` with `depthOfField`, a rig null |
| `trail` (3.8) | an HDR orb on a bezier motion path with a spring, motion-blurred inside its own precomp so twelve one-frame `time.echo` copies join into a comet, under `light.glow` and a radial `stylize.chromatic`; a drifting `generate.turbulentNoise` plate tinted over time | HDR fills (> 1), `time.echo`, a precomp that blurs itself, `color.tint` keys |
| `morph` (3.6) | one path morphs circle → star → arch → heart → the mitte sparkle with automatic vertex matching, drawn by a gradient stroke with taper and a travelling wave, trimmed on with a rotating gap; a zig-zag ring and a breathing rounded square | path keys with morph, `gradientStroke`, `wiggly`, `trim`, `zigzag`, `roundCorners` |
| `motto` (5.0) | three per-character 3D text layers at different depths flipping in under a spot light with floor shadows, a point light drifting through colours, a camera focus pull from the near word to the far one | `threeDPerChar`, lights, camera DOF |
| `logo` (3.6) | the mitte mark assembles from its own paths: frame draws on with a trim, the sparkle pops in, the wordmark draws as a stroke then hands over to its fill | `fromSvg` with `drawOn`, fill fade |

Cost note from the document: the echo precomp blurs itself rather than the echo layer (a time effect under motion blur re-renders the layer at every shutter sample). Scene layers may carry `motionBlur` (a whip or zoom transition sets it): an uncollapsed scene renders once per frame and only its movement blurs.

## The P3 reel (`p3-reel.motion.json`, 24.3 s)

Scenes joined by `push`, `blurDissolve`, `wipe`, `push`, `lightLeak`, `cut`; `lint.disable` lists eight codes that are the point of the piece (missing exits, fast motion without blur, expensive effects, short text, text outside safe, offscreen layers, crawl speed, linear spatial ease). Uses `mitte/particles.confetti@1` and `mitte/particles.embers@1`.

| Scene | What it shows | Constructs |
|---|---|---|
| `glass` (3.4) | a squircle glass pill and a glass orb slide across the serif word "liquid" and a rotating dashed ring, bending the letters | `distort.glass` (refraction, dispersion, frost, specular rim, shadow) over a `generate.meshGradient` |
| `plexus` (3.4) | a geodesic globe of 560 particles on a sphere shell joined by lines, triangles and points, breathing on noise, plus a sparse outer network, under an orbiting camera with particle depth of field and glow; the shell explodes at 2.55 s | `particles` with a `sphere` emitter, connecting lines (`lines`, `triangles`), `noise` field, camera DOF, `light.glow`; the hand-built form of `particles.plexus` |
| `form` (3.4) | a 187 × 106 Form grid flies in from a scatter, draws "ripple" through `sizeBy`, takes colour from a hidden ramp (`colorBy`), swims on noise and a wave, then explodes and falls | `grid` emitter, `assemble`, `sizeBy`/`colorBy` layer maps, `wave`, gravity, streak motion blur: the hand-built form of `particles.form-logo` |
| `dust` (3.4) | "ERODE" is wiped left to right while a layer emitter samples the wipe edge into 42,000 particles/s carried off by wind and curl turbulence | `layer` emitter on a wiped text layer, `wind`, `turbulence`: `particles.disintegrate` opened up |
| `eclipse` (3.6) | a banded gas giant (fractal noise through a gradient map wrapped by `perspective.sphere`) passes in front of a sun; `light.godrays3d` streams rays that the disc cuts into shadow wedges | `generate.fractalNoise` + `color.gradientMap` + `perspective.sphere`, a `light` following the sun, `light.godrays3d` |
| `forge` (2.9) | a glowing tapered line welds across the frame; a path emitter riding its trim head throws sparks that shed glowing embers | `path` emitter on a trimmed stroke, aux `streaklet` particles, `particles.embers` |
| `finale` (4.2) | the forge keeps moving under a liquid-glass pane that sweeps in the logo card; the mark assembles in ink from its own paths and `particles.confetti` fires on the sparkle | the `transition.glass-swipe` construct as its own scene with zero tint, `drawOn`, `particles.confetti` on a marker |

Notes from the document: the swipe's tint is zero because `#FFFFFF14` composited in linear light reads as a grey slab on a dark scene; the Form maps are static layers (an animated map costs a frame of checkpoint memory per frame).

## The second P3 reel (`p3-reel-2.motion.json`, 20.4 s)

Physics, tracking and footage from other tools; `push`, `wipe`, `blurDissolve`, `push` between scenes.

| Scene | What it shows | Constructs |
|---|---|---|
| `fiesta` (4.0) | three strings of letter pennants, each a body hinged to the next and hung from the frame on two chain joints; they drop into their sag, a gusting wind with curl turbulence whips them, an impulse kicks the middle | `hinge` joints (limits ±50°), `chain`, `wind` + `turbulence`, `impulse`; depth without a camera: a far string scaled/blurred/tinted, a blurred copy as a wall shadow, a defocused foreground copy |
| `pour` (4.0) | 396 beads rain onto an ampersand image whose collider is its traced alpha contour; a wind cancels gravity, an inverse-square attractor coats the glyph, a vortex spins the coat | 400 `dynamic` shape bodies with radial gradient fills, a `static` image body with `shape: decompose`, `attractor`, `vortex` |
| `patio` (4.0) | engine-made courtyard footage camera-solved by `rexx-engine track`; PATIO letters stand on the solved floor, pop up, spin, cast shadows through a shadow catcher; a sun disc pinned to a solved point | `track` with a camera solve (`cam.floor`, `cam.slab` anchors), `acceptsShadows: "only"`, 3D text on footage |
| `mass` (4.0) | a 3d-service clip (eight tumbling primitives filmed through this comp's exported camera, ProRes 4444 → VP9 alpha) between the engine's grid floor and glowing 3D title | `rexx-engine convert --to camera`, a 2D `video` layer with alpha between 3D layers, exposure/vibrance/glow grade |
| `bloomscene` (4.4) | a hand-made Lottie flower, wrapped in a plain comp, as a turning kinematic body with an animated matte collider; a rain of per-character text bodies lands on the opening petals and is flung off | `lottie` footage, `kinematic` body with `shape: decompose` traced per frame, text bodies, motion blur |

Engine issues the document records (unfixed): a `lottie` comp layer used as a body gets a content-box collider (hence the wrapper comp); large textured 3D solids rendered unlit in an earlier build; `chain` links take no `settle`, so `physics.unsettled_at_end` is disabled in `lint.disable`.

## The P4 reel (`p4-reel.motion.json`, 22.6 s)

Every scene carries highlights above SDR white so one document is delivered three ways: SDR (`toneMap: "soft"`), HDR10 (`output: { "hdr": "pq", "hdrPeak": 1000, "toneMap": "aces2" }`) and HLG. Joined by `maskWipe` (circle from the sun), `whip`, `fadeThrough`, `blurDissolve`.

| Scene | What it shows | Constructs |
|---|---|---|
| `dawn` (4.6) | a classic-3D run on the GPU: seven pillar cards and the letters of DAWN on a lit floor, a parallel sun light with shadows whose diffusion softens as it climbs, an HDR sun card (radial gradient 16/9/4 at the core) with inverse-square glow, a dolly with a focus pull, 650 additive motes | `light` (parallel, `castsShadows`), HDR gradients, camera DOF, additive particles |
| `ripple` (4.4) | the whole scene refracted by a hand-written WGSL shader (`utility.shader`, GPU only): raindrop rings from `vec2` uniforms, a height field, per-channel refraction, a Blinn-Phong specular at 3.5× white, caustics; the `strength` uniform keyed from 0 | `utility.shader` with `vec2`/`float` uniforms on a precomp |
| `flow` (4.6) | engine-made footage slowed 4× (`stretch` 400) with `frameBlend: "flow"` (optical flow) against a `mix` split by a slanted divider | `video` with `stretch` + `frameBlend`, `transition.linearWipe` effect as the divider |
| `galaxy` (4.4) | 102,000 GPU particles born 4.5 s before the scene (preroll) in a vortex whose strength fades with radius, spiral arms by differential rotation, a faster core, streak motion blur, additive HDR glow, a camera pushing in and tilting | `particles` with `preroll`, `vortex`, GPU sprite draw |
| `neon` (4.6) | a 7×-white neon tube draws itself along a bezier wave, a path emitter sheds sparks from its tip, three stacked glows and a bloom, a dashed ring draws and rotates, the tube's path morphs into loops (index-matched) | HDR strokes, `trim`, path emitter, `light.glow` × 3 + `light.bloom`, path morph with `match: "index"` |

Notes from the document: `--backend gpu` renders in 77 s against 213 s on the CPU (which leaves the shader scene unshaded, `effect.requires_gpu`); the SDR master is chunk-rendered byte-identically (`--segment 6`, `--plan 4` / `--chunk i/4` / `--assemble`); the PQ master cannot be chunked (its content light level is measured over the whole video). Engine issues recorded: 3D particle DOF inside a classic-3D run with camera DOF blotches other cards; a path morph with `match: "auto"` collapses mid-interpolation; a shape layer with two sibling groups each with a fill draws only the first; the camera `orbit` sugar produces no position in 0.1.46.

## Using a demo as a starting point

Fetch it through `doc_url: "library:mitte/demo/title-card@1"` with `motion.check` (`canonical: true` returns the expanded form) or open the file in the repository; keep the comp sizes, swap `theme.use`, replace text and assets, and re-check. The reels are large (`p3-reel-2` is 639 KB of mostly physics bodies) and lean on GPU, physics and tracking features other SKILLS areas document; copy one scene at a time.
