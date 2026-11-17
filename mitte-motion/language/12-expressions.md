# 12. Expressions: the whole subset, every function and object the host provides

Scope: spec 11 in full, checked against `rexx-expr` (engine 0.1.48). An expression is a string in `expr` on any animatable property (effect parameters, mask paths, shape properties, source text, and the expression selector of text animators); it sees `value` (the property after base, loop and drivers) and returns the final value, which is then clamped to the property's range ([01](01-document.md) §10). Prefer drivers for wiggles, loops, following and audio (`lint.expr_prefer_driver`); use expressions for values derived from other properties, geometry, index, or custom math.

```jsonc
"rotation": { "value": 0, "expr": "time * 90" }
"position": { "keys": [ … ], "expr": "value + [0, Math.sin(time * 4) * 12]" }
"text":     { "value": "0", "expr": "Math.round(linear(time, 0, 2, 0, 1250)).toLocaleString()" }
```

Compiled at normalization: `expr.syntax`, `expr.unknown_name`, `expr.arity` (direct calls only), `expr.unknown_property`, `expr.cycle` are reported with line and column before any rendering. `motion.check` also evaluates every expression at every frame time of its layer's span (and motion-blur sample times), so runtime errors surface before a render.

## 1. Values and types

| Type | Notes |
|---|---|
| number | IEEE double. Literals: integers, decimals (`.06`, `3.`), exponents (`1e-3`), hex `0x1F`, octal `0o17`, binary `0b101`, `_` separators. A property receiving a non-finite number fails (`expr.non_finite`). |
| string | `'…'`, `"…"`, template literals `` `a ${x}` ``; ECMAScript escapes (`\n`, `\t`, `\xHH`, `\uHHHH`, `\u{…}`, line continuation); `length`, indexing and `slice` count **code points**; ≤ 1 MB |
| boolean | `true`, `false` |
| array | any values; vectors are arrays of numbers; ≤ 1,000,000 elements |
| object | string-keyed records from literals (`{ a: 1, "b-c": 2 }`); no prototypes |
| function | user and arrow functions, first-class (passable to `map`); call depth ≤ 64 (`expr.depth`); closures capture by reference, one binding per `for (let …)` iteration |
| null, undefined | reading a missing key gives `undefined`; a property receiving either fails (`expr.no_value`) |
| host objects | layers, comps, properties, keys, markers, paths: read-only handles. A property handle stays a handle in a variable or array and dereferences on use: `const P = thisComp.layer("a").position; P.numKeys; P.key(2); P[0]; P + [1, 0]` |

**Return conversion**: a number for 1D properties (and each separated dimension); an array of the right length for vectors (shorter is padded with the current value's components, longer is `expr.result_type`); a string for `text`; `[r, g, b, a]` **sRGB-encoded** 0–1 floats for colours (HDR may exceed 1; the engine converts at the boundary, so After Effects colour expressions port unchanged); a path from `createPath` for paths; a boolean or 0/1 for checkboxes; for enums the value's string or its 1-based index (`effect("blend")("mode") == 3` and `== "screen"` both work).

**What `value` is**: a number (1D, or a separated dimension), an array (vectors), a plain string (`text`; span styles are read through `.style`/`getStyleAt`), a read-only `{ type, from, to, stops: [[pos, [r,g,b,a]], …], opacityStops, midpoints }` for gradients, a path handle for paths (its calls return fresh arrays). Expressions never see track or physics references (they are keys or bake samples by then).

## 2. Grammar

A subset of ECMAScript 2020. A program is a list of statements; the result is the value of the last expression statement (After Effects' rule) or the argument of a top-level `return`.

Statements: block, `var`/`let`/`const` declarations, `function` declarations, `if`/`else`, `for (;;)`, `for … of`, `while`, `do … while`, `switch`/`case`/`default`, `return`, `break`, `continue`, expression statements, empty `;`. Expressions: comma, assignment `= += -= *= /= %=`, arrow functions (`x => …`, `(a, b) => { … }`), `? :`, `??`, `||`, `&&`, `== != === !==`, `< > <= >=`, `+ -`, `* / %`, `**` (right-associative), unary `! - + typeof`, prefix/postfix `++`/`--`, calls, `.name`, `[expr]`, `?.name`, literals (numbers, strings, templates, `true`, `false`, `null`, `undefined`), array literals (trailing comma ok), object literals (`{ a, "b": 1, 2: x }`), parentheses. Comments `// …` and `/* … */`. Automatic semicolon insertion as in ECMAScript. Two ECMAScript errors kept: `-2 ** 2` (parenthesize) and `??` mixed with `||`/`&&` without parentheses.

**Not in the grammar** (syntax errors): `class`, `new`, `this`, `delete`, `in`, `instanceof`, `void`, labels, bitwise operators (`& | ^ ~ << >> >>>`), spread/rest `...`, destructuring, getters/setters, regular-expression literals, `async`/`await`, `yield`, `import`/`export`, `with`, `try`/`catch`/`throw`.

**Scoping**: `let`/`const` block-scoped; `var` and function declarations function-scoped and hoisted. Assigning to an undeclared name **at the top level** is rewritten to a `var` declaration (info `lint.expr_implicit_var`; the circulating After Effects idiom `amp = .06;` works); inside a function it is `expr.undeclared`. Library names may be shadowed by local declarations.

## 3. Vector arithmetic

| Expression | Result |
|---|---|
| `[1, 2] + [10, 20]` | `[11, 22]` |
| `[1, 2, 3] - [1, 1]` | `[0, 1, 3]` (the shorter operand is padded with 0) |
| `[1, 2] + 2` | `[3, 2]` (a scalar is a 1-vector, After Effects' behaviour) |
| `[10, 20] * 2`, `2 * [10, 20]`, `[10, 20] / 2`, `-[1, 2]` | per component |
| `[1, 2] * [3, 4]` | `expr.vector_op` (use `mul` per component, or `map`) |
| `"a" + 1`, `"x" + [1, 2]` | string concatenation (`"x1,2"`) |

`add(a, b)`, `sub(a, b)`, `mul(v, s)`, `div(v, s)` are the explicit forms. `==`/`===` compare numeric vectors by value; other arrays and objects by identity (`lint.expr_array_equality`).

## 4. The object model

### 4.1 Globals

| Name | Meaning |
|---|---|
| `time` | the comp time (seconds) of this evaluation, including motion-blur sub-samples |
| `value` | this property's pre-expression value |
| `thisProperty`, `thisLayer`, `thisComp` | handles; `thisLayer`'s members may be used bare (`index`, `inPoint`, `transform`, `effect(…)`, `position`) |
| `colorDepth` | always `32` |
| `this_comp`, `this_layer`, `this_property` | legacy aliases |

### 4.2 Comp objects (`thisComp`, `comp(id)`)

| Member | Meaning |
|---|---|
| `comp(idOrName)` | another comp of the document, read-only (its layers' properties may be evaluated) |
| `.layer(idOrNameOrIndex)` | a layer: a string matches ids then names; a number is a **1-based index in After Effects order, 1 = topmost** (the last element of `layers`), so `thisComp.layer(index - 1)` is "the layer above me"; out of range: `expr.no_layer` |
| `.layer(otherLayer, relIndex)` | the layer `relIndex` positions from `otherLayer` (negative = above) |
| `.numLayers`, `.width`, `.height`, `.duration`, `.frameDuration` (`1/fps`), `.pixelAspect`, `.name`, `.bgColor` (`[r,g,b,a]`), `.displayStartTime` (the comp's `start`) | |
| `.marker` | the comp's markers (§4.5) |

### 4.3 Layer objects (`thisLayer`, `thisComp.layer(…)`, `parent`)

| Member | Meaning |
|---|---|
| `.name`, `.id` (the stable id; not in After Effects), `.repeatIndex` (0-based index in its `repeat`, −1 otherwise), `.index` (1-based After Effects order) | |
| `.inPoint`, `.outPoint` (comp seconds), `.startTime` (the layer's `offset`) | |
| `.hasParent`, `.parent` | |
| `.width`, `.height` | the source size: comp size for comp layers; image/video size; solid size; the **comp size** for text and shape layers (as After Effects): use `sourceRectAtTime` for content bounds |
| `.active` (time in `[inPoint, outPoint)`), `.enabled` | |
| `.transform` | `.anchorPoint` (alias `.anchor`), `.position`, `.xPosition`/`.yPosition`/`.zPosition` (separated), `.scale`, `.rotation` (alias `.zRotation`), `.xRotation`, `.yRotation`, `.orientation`, `.opacity`, `.skew`, `.skewAxis`; all also directly on the layer |
| `.effect(idOrNameOrIndex)` | an effect handle; called with a parameter name, id or 1-based index it returns that parameter property: `effect("glow")("radius")`, `effect("Slider Control")("Slider")`, `effect(1)(1)`; `.active`; After Effects display names `"Slider"`, `"Angle"`, `"Point"`, `"3D Point"`, `"Color"`, `"Checkbox"`, `"Layer"`, `"Menu"` are accepted |
| `.mask(idOrNameOrIndex)` | `.maskPath`, `.maskFeather`, `.maskOpacity`, `.maskExpansion` (After Effects names) or the spec names |
| `.content(idOrName)` | a shape item of the layer's `contents`, by `id`, then `name`, or 1-based index (`content(2)`); chainable into groups (`content("badge").content("ring").size`). Members are the item's numeric, vector and colour fields by their spec names (`size`, `position`, `roundness`, `start`/`end`/`offset`, `width`, `opacity`, `color`), evaluated at the reading time. After Effects display names ("Rectangle 1", "Size") do not resolve: give items an `id`. An unknown item is `expr.unknown_property`. |
| `.text.sourceText` | the text (a string with `.style`, §4.7) |
| `.marker` | layer markers |
| `.sourceRectAtTime(t = time, includeExtents = false)` | `{ top, left, width, height }` of the content in layer space: text ink bounds (with `includeExtents` the full line boxes incl. ascent/descent); shape path bounds (with extents incl. stroke width) |
| `.toComp(p, t = time)`, `.fromComp(p, t)` | layer ↔ comp space through parents (3D: without camera projection) |
| `.toWorld(p, t)`, `.fromWorld(p, t)` | layer ↔ world (3D) |
| `.toCompVec`, `.fromCompVec`, `.toWorldVec`, `.fromWorldVec` | direction vectors (no translation) |
| `.fromCompToSurface(p, t)` | a comp point projected onto the layer's surface (3D) |
| `.audioActive` | whether the layer has audible audio at `time` |
| `.source` | the nested comp for comp layers; `null` for footage |

### 4.4 Property objects

Every property handle (`thisProperty`, `thisLayer.position`, `effect("x")("y")`, …):

| Member | Meaning |
|---|---|
| `.value` | the value at `time` |
| `.valueAtTime(t)` | the value at comp time `t`; on `thisProperty` (or the same property by path) the **pre-expression** value, so self-reference never recurses |
| `.velocity`, `.velocityAtTime(t)` | derivative in units per second per dimension (central difference over 1 ms on the evaluated value) |
| `.speed`, `.speedAtTime(t)` | the length of the velocity (spatial: speed along the path) |
| `.numKeys`, `.key(i)` (1-based `{ time, value, index }`; `expr.no_key` out of range), `.nearestKey(t)` | |
| `.propertyIndex`, `.name`, `.propertyGroup(n = 1)` | |
| `.wiggle(freq, amp, octaves = 1, ampMult = 0.5, t = time)` | the same algorithm and seeding as the `wiggle` driver |
| `.temporalWiggle(freq, amp, octaves, ampMult, t)` | the value sampled at a wiggled time |
| `.smooth(width = 0.2, samples = 5, t = time)` | box-averaged over `width` seconds |
| `.loopOut(type = "cycle", numKeyframes = 0)`, `.loopIn(…)`, `.loopOutDuration(type, duration = 0)`, `.loopInDuration(…)` | the `loop` semantics ([02](02-keys-and-eases.md) §9); `numKeyframes` counts segments |
| `.points()`, `.inTangents()`, `.outTangents()`, `.isClosed()`, `.pointOnPath(pct, t)`, `.tangentOnPath(pct, t)`, `.normalOnPath(pct, t)` | path properties only; `pct` 0–1 of the path length |

The bare globals `wiggle`, `temporalWiggle`, `smooth`, `loopOut`, `loopIn`, `loopOutDuration`, `loopInDuration`, `valueAtTime`, `velocityAtTime`, `speedAtTime`, `key`, `numKeys`, `nearestKey`, `propertyGroup` act on `thisProperty`.

### 4.5 Markers (`thisComp.marker`, `thisLayer.marker`)

`.numKeys`; `.key(i)` (1-based by time: `{ time, duration, comment (= the marker's name), index }`); `.key("name")` (missing: `expr.no_key`); `.nearestKey(t)`.

### 4.6 Effects

`effect("id")` (or by name or 1-based index) is an effect handle; `effect("id")("param")` or `.param("param")` a parameter property; `.active` its enabled state. The expression-control effects exist to be read this way: Slider, Angle, Point, 3D Point, Color, Checkbox, Dropdown Menu, Layer Control (returns a layer).

### 4.7 Text

`text.sourceText` is a string with a read-only `.style`: `.font`, `.fontSize`, `.fillColor`, `.strokeColor`, `.strokeWidth`, `.tracking`, `.leading`, `.isFauxBold`, `.isAllCaps` (the first span's style); `.getStyleAt(charIndex, t = time)`. Style setters (`setFontSize`, …) are not supported.

## 5. Functions

### 5.1 Interpolation, math, conversion

| Function | Meaning |
|---|---|
| `linear(t, tMin, tMax, v1, v2)`, `linear(t, v1, v2)` | clamped map (`t` in [0, 1] for the short form); `v1`/`v2` may be vectors |
| `ease(…)`, `easeIn(…)`, `easeOut(…)` | same signatures; cubic-beziers (0.333, 0, 0.667, 1), (0.333, 0, 1, 1), (0, 0, 0.667, 1): approximations of After Effects' unpublished curves |
| `interp(name, t, tMin, tMax, v1, v2)` | extension: any catalog ease by name (`interp("expo.out", time, 0, 1, 0, 500)`) |
| `clamp(v, lo, hi)` | per component |
| `length(v)`, `length(a, b)`, `normalize(v)`, `dot(a, b)`, `cross(a, b)` (3D) | |
| `add`, `sub`, `mul`, `div` | §3 |
| `lookAt(from, to)` | a 3D orientation `[x, y, z]` in degrees pointing from `from` to `to` |
| `degreesToRadians(d)`, `radiansToDegrees(r)` | |
| `timeToFrames(t = time + thisComp.displayStartTime, fps = 1/thisComp.frameDuration, isDuration = false)`, `framesToTime(frames, fps)` | |
| `timeToTimecode(t, timecodeBase = 30, isDuration = false)`, `timeToCurrentFormat(t)` | timecode strings |
| `hslToRgb([h, s, l, a])`, `rgbToHsl([r, g, b, a])`, `hexToRgb("#ff3366")` | 0–1 components |
| `posterizeTime(fps)` | from here on, `time` and every time-dependent call are quantized down to multiples of `1/fps` (`posterizeTime(12)`: on twos at 24); `posterizeTime(0)` freezes `time` at the layer's in point |
| `createPath(points, inTangents = [], outTangents = [], isClosed = true)` | builds a path value |

`Math`: `abs acos asin atan atan2 ceil cos cosh exp floor hypot log log10 log2 max min pow round sign sin sinh sqrt tan tanh trunc`, constants `PI E SQRT2 SQRT1_2 LN2 LN10 LOG2E LOG10E`. `Math.random` is **not** provided (`expr.math_random`: use `random()`).

### 5.2 Random and noise

| Function | Meaning |
|---|---|
| `seedRandom(seed, timeless = false)` | sets the seed for later `random`/`gaussRandom` calls in this evaluation; with `timeless = false` the sequence also depends on the evaluation tick (motion-blur sub-samples differ, values change per frame), with `true` it is the same at every time |
| `random()`, `random(max)`, `random(min, max)` | uniform; scalars or vectors (per component) |
| `gaussRandom(…)` | same signatures, normally distributed (90 % within the range) |
| `noise(x)` | smooth gradient noise in [−1, 1] for a number or a 2D/3D vector; deterministic, the input is the seed |

The default seed before any `seedRandom` is `hash(layer id, property path)`, so two layers with identical expressions differ and the same layer repeats on every render; the generator is a counter-based hash over `(seed, tick, call counter)`, so evaluation order cannot change results.

### 5.3 Strings, numbers, arrays, objects

- Strings: `length`, `charAt`, `charCodeAt`, `codePointAt`, `at`, `indexOf`, `lastIndexOf`, `includes`, `startsWith`, `endsWith`, `slice`, `substring`, `substr`, `toUpperCase`, `toLowerCase`, `toLocaleUpperCase`, `toLocaleLowerCase`, `localeCompare`, `trim`, `trimStart`/`trimLeft`, `trimEnd`/`trimRight`, `padStart`, `padEnd`, `repeat`, `split(separator, limit?)`, `replace(pattern, replacement)` (first occurrence, string patterns only), `replaceAll`, `concat`, `valueOf`, `toString`; `String(x)`.
- Numbers: `toFixed(digits)`, `toPrecision(digits)`, `toString(radix = 10)`, `toLocaleString(locale = "en-US", { minimumFractionDigits, maximumFractionDigits, useGrouping })` with the bundled locales en-US, en-GB, de-DE, fr-FR, es-ES, it-IT, pt-BR, nl-NL, sv-SE, pl-PL, tr-TR, ru-RU, ja-JP, zh-CN, ko-KR, ar-SA, hi-IN; `Number(x)`, `parseInt(s, radix)`, `parseFloat(s)`, `isNaN`, `isFinite`.
- Arrays: `length`, `map`, `filter`, `reduce`, `reduceRight`, `forEach`, `some`, `every`, `find`, `findIndex`, `findLast`, `findLastIndex`, `indexOf`, `lastIndexOf`, `includes`, `at`, `slice`, `splice`, `concat`, `flat`, `join`, `reverse` (a copy), `push`, `pop`, `shift`, `unshift` (local arrays), `fill`, `sort(compareFn)` (stable); `Array(n)`, `Array.isArray`, `Array.from({ length: n }, fn)`.
- Objects: `Object.keys`, `Object.values`, `Object.entries`, `hasOwnProperty`; `JSON.stringify` (debugging text).

### 5.4 Expression selector variables

Inside a text animator's `expression` selector the program runs once per unit and returns the amount in percent (or a vector per axis): `textIndex` (1-based), `textTotal`, `selectorValue` (the amount from the previous selectors, a scalar). A runtime error there is a warning and reads 0; a budget overrun still fails the frame.

## 6. Determinism and budgets

No wall clock, network, files, environment or machine locale. Every evaluation starts from a fresh scope (no persistent globals). Budgets: 100,000 VM steps per evaluation (`expr.budget`), call depth 64 (`expr.depth`), 16 MB heap (`expr.memory`), 5 × 10⁸ steps per check or render (`limit.expr_total`). Floating point: doubles without fused multiply-add, `Math` from a pinned pure-Rust libm. Within one frame each (property, time) is evaluated once; literal accessors are static dependencies that order evaluation; static cycles are `expr.cycle` at normalization, dynamic ones at evaluation. Reading one's own value at another time through `valueAtTime` is not a cycle.

**Runtime errors fail the render** (`expr.runtime`, `expr.budget`, `expr.no_layer`, `expr.no_key`, `expr.no_value`, `expr.non_finite`, `expr.vector_op`, `expr.result_type`, `expr.depth`, `expr.memory`) with comp, layer, property, time, line and column; there is no silent fallback to the pre-expression value. Write the fallback yourself (`thisComp.numLayers > 3 ? … : value`). The one exception is the expression selector (above). Expressions on **path properties** are not evaluated by the renderer today (warning `render.unsupported`; the keyed or static path is used).

## 7. Idioms that work unchanged

| Idiom | Expression |
|---|---|
| wiggle | `wiggle(2, 25)`; one dimension: `[value[0], wiggle(1, 40)[1]]` |
| endless loop | `loopOut("cycle")`, `loopOut("pingpong")`, `loopOut("offset")` |
| constant rotation | `time * 120` |
| follow the leader | `thisComp.layer(index - 1).transform.position.valueAtTime(time - 0.1)` |
| offset by index | `value + [0, (index - 1) * 80]` |
| counting numbers | `Math.round(linear(time, 0, 2, 0, 1250)).toLocaleString()` |
| auto-sizing box (on a rect's size) | `var r = thisComp.layer("title").sourceRectAtTime(); [r.width + 48, r.height + 24]` |
| look at a target | `lookAt(position, thisComp.layer("target").position)` |
| slider-driven value | `effect("Slider Control")("Slider") * 10` |
| step every N frames | `posterizeTime(8); wiggle(3, 20)` |
| distance-based fade | `linear(length(position, thisComp.layer("focus").position), 0, 600, 100, 0)` |
| typewriter (on source text) | `text.sourceText.slice(0, Math.floor(linear(time, 0, 2, 0, text.sourceText.length)))` |
| inertial bounce | the classic Dan Ebberts form (implicit top-level `amp = .06; freq = 3; decay = 6;` …) runs unchanged |

**Not supported**: ExtendScript (`app`, `$`, `File`, `system`), `Date`, `Math.random`, `eval`, `Function`, `new`, regular expressions, `sampleImage`, `footage()`/`sourceData`, text style setters, `thisProject`, `essentialProperty`, persistent globals, bitwise operators.

## 8. Examples

`examples/12-expressions.json`: the object model in use (comp and layer lookups by id and index, `sourceRectAtTime`, property keys and velocity, markers, effect controls read through `thisComp.layer('ctl').effect(…)(…)`, `text.sourceText`), the interpolation and math library, seeded randomness and `noise`, `posterizeTime`, `createPath` on a mask, string and array methods, an expression selector, and the classic inertial bounce. Checks with 0 errors; `lint.expr_implicit_var` infos are the expected result of the inertial-bounce idiom, and `lint.expr_prefer_driver` the expected nudge on the plain `wiggle(2, 25)`.
