# Perspective

7 ids. Parameters: [91-catalogue-perspective.md](91-catalogue-perspective.md). Lit bevels, 3D-ish shadows and the two mapping effects. None of them use the comp camera: they are 2D looks on the layer's own pixels (true 3D is `threeD: true` with a camera, spec 8).

| Effect | Use it for | Neutral |
|---|---|---|
| `perspective.bevelAlpha` | Signed-distance bevel of the alpha edge: `edgeThickness`, `lightAngle`, `lightColor`, `lightIntensity`. | `lightIntensity: 0` |
| `perspective.bevelEdges` | A rectangular bevel of the layer's edges (same four parameters). | `lightIntensity: 0` |
| `perspective.dropShadow3d` | Radial Shadow: a shadow cast from `lightSource` point3d at `projectionDistance`, `color`, `opacity`, `softness`, `render` regular/glassEdge, `colorInfluence`, `shadowOnly`, `resizeLayer`. | `opacity: 0` |
| `perspective.sphere` | Wrap the layer on a sphere (planets, globe logos): `rotation` angle3d (`[x, y, z]`; y spins it), `radius` px, `offset` point, `render` full/outside/inside, `light.intensity`/`color`/`height`/`direction`, `shading.ambient`/`diffuse`/`specular`/`roughness`/`metal`/`reflective`/`reflectionMap` (a layer read equirectangularly). Seen orthographically from the front; the texture is equirectangular. | — |
| `perspective.cylinder` | Wrap on an open cylinder: `radius` percent of the layer width (100 = once around), `position` point3d (z unused), `rotation` angle3d, `render`, `light.*`, `shading.*` as the sphere. | — |
| `perspective.ccEnvironment` | Reflection-map an `environment` layer (`environmentSource`, `mapping` spherical/probe/verticalCross, `filterEnvironment`, `height`) onto the layer's relief. | — |
| `perspective.3dGlasses` | Not implemented (P4): `effect.unavailable`. | — |

Device: all CPU.

## Patterns

**Spinning globe.** A square solid with an equirectangular map (an image layer scaled to the solid, or a `generate.*` texture) and `perspective.sphere` with `rotation` `[0, { keys 0 → 360 }, 0]` (animate the y component: write `"rotation": { "keys": [ { "t": 0, "v": [0, 0, 0] }, { "t": 6, "v": [0, 360, 0] } ] }`), `radius` 220, `light.direction` −45, `shading.specular` 30.

**Embossed logo.** `perspective.bevelAlpha` `edgeThickness` 6, `lightAngle` −60, `lightIntensity` 0.6, then `stylize.dropShadow`.

**Rotating label on a can.** `perspective.cylinder` `radius` 100, `rotation` y keyed, `render: "outside"` so the back face is hidden.

Full example: `examples/perspective-family.motion.json`.
