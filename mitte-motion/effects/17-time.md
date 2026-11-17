# Time

7 ids. Parameters: [91-catalogue-time.md](91-catalogue-time.md). Time effects read the layer (its source, masks and the effects above them in the stack) at other times. They declare those times; the renderer renders the layer at each and hands them in. Nothing is cached across frames, so a frame is the same in any order.

| Effect | Use it for | Neutral |
|---|---|---|
| `time.echo` | Motion trails: `count` copies at `t + i · echoTime` (default one frame earlier; negative = past), weighted `startingIntensity · decay^i`, combined by `operator` add/maximum/minimum/screen/compositeInBack/compositeInFront/blend. `count` ≤ 32 (lint warns above 8). | `count: 0` |
| `time.posterize` | Stop-motion feel: the layer's content (source, masks, earlier effects, their keys) is evaluated at `fps` steps (24; use 12 for "on twos"). It changes the upstream time rather than reading other frames. | — |
| `time.displacement` | Slit-scan: each pixel reads the layer at a time offset by the `map` layer's luma × `maxDisplacement` s (`mapSource`, `resolution` percent of a frame step, `stretch`); at most 32 steps each way. | `maxDisplacement: 0` |
| `time.frameBlend` | Frame blending inside the stack: `mode` mix (crossfade between the surrounding comp frames) or flow (optical flow interpolation, as the layer-level `frameBlend: "flow"`). | — |
| `time.strobe` | Flashes every `period` s for `duration` s (`randomStrobe` percent of periods at random): `strobe` operatesOnColorOnly (combines `color` by `operator` copy/add/subtract/multiply/difference/screen/lighten/darken, mixed by `blend`) or makesLayerTransparent; `seed`. Time-dependent. | `period: 0` |
| `time.difference` | Difference against the layer at `timeOffset` s (`target` null) or against a `target` layer at the same time: `contrast`, `absoluteDifference`, `alphaChannel` (9 modes). | — |
| `time.ccWideTime` | Average over `backwardSteps`…`forwardSteps` frames (0–45 each), `nativeMotionBlur`. | 0 / 0 |

Device: all CPU.

## Rules

- An echo of a layer whose **source is static and whose transform moves** shows nothing: effects run before the transform, so every echo is the same image (`lint.echo_static_source`). Precompose the moving layer and put the echo on the comp layer, as in After Effects.
- Each declared time is a full evaluation of the layer above the effect; an echo with `count` 8 costs about 9 layer renders per frame (`lint.expensive_effect` flags an echo that takes the layer over the frame budget; the registry's cap is 32).
- Other effects that read other times declare them the same way: `color.shadowHighlight` `temporalSmoothing`, `stylize.removeGrain` `temporalFiltering`, `matte.refine`/`matte.refineHard`/`matte.keyCleaner` chatter reduction, `key.ccWireRemoval` `frameOffset`.
- `time.posterize` quantizes the layer's **own** time, not the comp's: keys on the layer's effects above it step too; a tween on the layer's transform does not.

## Patterns

**Trails behind a moving precomp.** Comp `ball` with the moving shape; in `main` a comp layer `ballComp` with `time.echo` `echoTime` −0.04, `count` 6, `decay` 0.7, `operator: "add"`, and the comp layer's `blend: "add"`.

**Stop-motion text.** `time.posterize` `fps: 12` on a text layer whose animators move; pair it with `stylize.roughenEdges` boil (`evolution` keyed with a `steps(n)` ease) for the hand-made look.

**Strobe on a drop.** `time.strobe` `period` 0.25, `duration` 0.05 between two marker times by keying `blend` 0 → 100 → 0 (`blend` is the mix of the strobe colour; `period: 0` is off).

Full example: `examples/time-family.motion.json`.
