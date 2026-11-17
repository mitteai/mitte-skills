# Cookbook 2: ten more complete documents

Continues `11-cookbook-1.md`; same rules (every file checks clean, expected warnings declared, JSON embedded from `examples/cookbook/`).

| # | Brief | Built from |
|---|---|---|
| 11 | HDR trailer card | HDR fills above white, `light.glow` and `light.bloom`, `output.hdr: pq` with `aces2` |
| 12 | slow-motion clip | `video` with `stretch: 400` and `frameBlend: flow`, `title.chapter` over it |
| 13 | custom shader look | `utility.shader` (WGSL) refracting a precomp, keyed `float` and `vec2` uniforms; GPU only |
| 14 | Lottie import to edit | a `comp` layer with `lottie`, placed, scaled, retimed with `stretch` and tweened |
| 15 | chunked long render | a 150 s crawl over `bg.grid`; the service chunks it across workers, bytes identical |
| 16 | explainer steps | three `explainer.step` instances on voice-over phrase times |
| 17 | kinetic quote | `kinetic.words` then `quote.card` on `editorial` |
| 18 | UI demo | `screen.demo` (laptop, cursor tour with click zooms) with a drawn screen in the slot, `ui.toast` |
| 19 | map route | `map.route`, `map.pin`, `callout.line` |
| 20 | 9:16 outro | `bg.gradient-mesh`, `social.frame`, `countdown`, `cta.subscribe` |

Chunked rendering (15): the service splits a variant of two minutes or more into chunks of whole 10 s encoder segments when it has two or more workers (`REXX_CHUNK_LOCAL`, `REXX_CHUNK_PEERS`), renders them on separate processes or boxes and assembles them; the file is byte-identical to a one-process render because every segment is encoded by its own encoder from its first frame. Locally: `rexx-engine render --segment 10 --plan 4`, then `--chunk i/4` per chunk, then `--assemble`. Nothing in the document changes; a PQ (HDR10) master cannot be chunked because its content light level is measured over the whole video.

<!-- gen:library-cookbook-2:start -->
### Cookbook 11: HDR trailer card: highlights above white, glow and bloom, delivered as HDR10 (PQ) with aces2

`SKILLS/library/examples/cookbook/11-hdr-trailer.motion.json`; theme `mitte/neon@1`; 1920 × 1080, 30 fps, 6 s.

Check: expected warnings `lint.expensive_effect`, `lint.text_outside_safe_area`. glow and bloom are the point of an HDR card. The title is set past the title-safe width on purpose (a trailer card).

```json
{
  "motion": 1,
  "theme": {"use": "mitte/neon@1"},
  "comps": {
    "main": {
      "size": [1920, 1080],
      "fps": 30,
      "duration": 6,
      "background": "#050507",
      "layers": [
        {
          "id": "haze",
          "type": "solid",
          "color": "#120A1E",
          "effects": [
            {
              "type": "generate.gradient",
              "params": {"type": "radial", "start": ["50%", "50%"], "end": ["100%", "50%"], "gradient": {"stops": [[0, "#2A1140"], [1, "#050507"]]}}
            }
          ]
        },
        {
          "id": "title",
          "type": "text",
          "text": "ECLIPSE",
          "style": {"font": "$theme.font.display", "size": "$theme.type.size.5", "fill": {"r": 4, "g": 1.2, "b": 3.5}, "tracking": 60},
          "origin": "center",
          "position": ["50%", "48%"],
          "effects": [{"type": "light.glow", "params": {"radius": 60, "intensity": 1.6}}]
        },
        {
          "id": "date",
          "type": "text",
          "text": "SUMMER 2027",
          "style": {"font": "$theme.font.body", "size": "$theme.type.size.1", "fill": "$theme.color.fg", "tracking": 300},
          "origin": "top",
          "align": {"to": "title", "y": "below", "gap": "$theme.space.5", "x": "center"}
        },
        {"id": "bloom", "type": "adjustment", "effects": [{"type": "light.bloom", "params": {"threshold": 1.0, "intensity": 0.8, "radius": 120}}]}
      ],
      "timeline": [
        {"target": "title/chars", "preset": "blurIn", "props": {"amount": 40}, "stagger": 0.06, "at": 0.3},
        {"target": "date", "preset": "trackIn", "at": 1.4},
        {"target": ["title", "date"], "preset": "fadeOut", "dur": 0.6, "at": 5.2}
      ]
    }
  },
  "output": {"format": "mp4", "codec": "hevc", "quality": "high", "hdr": "pq", "hdrPeak": 1000, "toneMap": "aces2"}
}
```

### Cookbook 12: a clip slowed 4x with optical-flow frame blending, a chapter title over it

`SKILLS/library/examples/cookbook/12-slow-mo-clip.motion.json`; theme `mitte/editorial@1`; 1920 × 1080, 30 fps, 8 s; library: `mitte/title.chapter@1`.

Check: no warnings. The demo tracking clip stands in for footage; frameBlend flow interpolates the in-between frames.

```json
{
  "motion": 1,
  "theme": {"use": "mitte/editorial@1"},
  "assets": {"clip": {"src": "library:mitte/demo/tracking-clip@1", "type": "video"}},
  "comps": {
    "main": {
      "size": [1920, 1080],
      "fps": 30,
      "duration": 8,
      "background": "#000000",
      "layers": [
        {"id": "slow", "type": "video", "asset": "clip", "fit": "cover", "stretch": 400, "frameBlend": "flow", "mute": true},
        {"id": "shade", "type": "solid", "color": "$theme.color.fg.a30"},
        {
          "id": "chapter",
          "type": "component",
          "use": "mitte/title.chapter@1",
          "in": 1.0,
          "props": {"number": "02", "kicker": "CHAPTER", "title": "Slower, clearer", "hold": 4},
          "origin": "center",
          "position": ["50%", "50%"]
        }
      ],
      "timeline": [{"target": "chapter", "preset": "fadeOut", "dur": 0.4, "at": 7.1}]
    }
  }
}
```

### Cookbook 13: a custom WGSL shader (utility.shader) refracts the whole scene like water; GPU only

`SKILLS/library/examples/cookbook/13-custom-shader-look.motion.json`; theme `mitte/soft@1`; 1920 × 1080, 30 fps, 6 s.

Check: expected warnings `effect.requires_gpu`. utility.shader runs on the GPU backend only; a CPU render leaves the layer unshaded (effect.requires_gpu). A CPU-side check reports the shader as GPU-only; render with --backend gpu (the service picks the GPU for it).

```json
{
  "motion": 1,
  "theme": {"use": "mitte/soft@1"},
  "comps": {
    "scene": {
      "size": [1920, 1080],
      "fps": 30,
      "duration": 6,
      "background": "$theme.color.bg",
      "layers": [
        {
          "id": "rings",
          "type": "repeat",
          "count": 5,
          "layout": {"type": "radial", "radius": 260, "startAngle": -90, "sweep": 360, "center": ["50%", "50%"]},
          "layer": {"type": "shape", "shape": "circle", "radius": 90, "fill": "$theme.color.palette.$index"}
        },
        {
          "id": "word",
          "type": "text",
          "text": "ripple",
          "style": {"font": "$theme.font.display", "size": "$theme.type.size.6", "fill": "$theme.color.fg"},
          "origin": "center",
          "position": ["50%", "50%"]
        }
      ],
      "timeline": [{"target": "rings.*", "preset": "popIn", "stagger": 0.08, "at": 0.2}, {"target": "word", "preset": "rise", "at": 0.6}]
    },
    "main": {
      "size": [1920, 1080],
      "fps": 30,
      "duration": 6,
      "background": "$theme.color.bg",
      "layers": [
        {
          "id": "surface",
          "type": "comp",
          "comp": "scene",
          "position": [960, 540],
          "effects": [
            {
              "id": "water",
              "type": "utility.shader",
              "params": {
                "code": "fn ring(p: vec2f, c: vec2f, age: f32, k: f32) -> f32 {\n  if (age <= 0.0) { return 0.0; }\n  let d = distance(p, c);\n  let r = age * 0.62;\n  let env = exp(-abs(d - r) * 7.0) * exp(-age * 0.75) * smoothstep(0.0, 0.08, age);\n  return sin((d - r) * 52.0) * env * k;\n}\nfn h(uv: vec2f, t: f32) -> f32 {\n  let asp = vec2f(rexx.size.x / rexx.size.y, 1.0);\n  let p = uv * asp;\n  var s = 0.0;\n  s += ring(p, params.drop1 * asp, t - 0.4, 1.0);\n  s += ring(p, params.drop2 * asp, t - 1.6, 0.9);\n  s += 0.06 * sin(p.x * 24.0 + t * 1.8) * sin(p.y * 20.0 - t * 1.3);\n  return s;\n}\nfn effect(uv: vec2f, t: f32) -> vec4f {\n  let e = vec2f(1.5, 0.0) / rexx.size;\n  let hx = h(uv + e.xy, t) - h(uv - e.xy, t);\n  let hy = h(uv + e.yx, t) - h(uv - e.yx, t);\n  let g = vec2f(hx, hy) * params.strength;\n  let c = textureSampleLevel(input, samp, uv + g, 0.0);\n  let n = normalize(vec3f(-g * 55.0, 1.0));\n  let l = normalize(vec3f(-0.35, -0.55, 0.75));\n  let hv = normalize(l + vec3f(0.0, 0.0, 1.0));\n  let spec = pow(max(dot(n, hv), 0.0), 90.0) * params.shine;\n  return vec4f(c.rgb + vec3f(spec), 1.0);\n}",
                "params": {
                  "strength": {"type": "float", "default": {"keys": [{"t": 0, "v": 0.0, "ease": "sine.out"}, {"t": 0.8, "v": 0.3}]}},
                  "shine": {"type": "float", "default": 1.2},
                  "drop1": {"type": "vec2", "default": [0.6, 0.5]},
                  "drop2": {"type": "vec2", "default": [0.3, 0.65]}
                }
              }
            }
          ]
        }
      ]
    }
  }
}
```

### Cookbook 14: a Lottie badge imported as a layer, placed, retimed and animated like any other layer, with a title beside it

`SKILLS/library/examples/cookbook/14-lottie-import.motion.json`; theme `mitte/soft@1`; 1920 × 1080, 30 fps, 5 s.

Check: expected warnings `convert.lottie_unsupported`. The demo badge carries an embedded image, which the importer drops (images inside a Lottie are not loaded).

```json
{
  "motion": 1,
  "theme": {"use": "mitte/soft@1"},
  "assets": {"badge": {"src": "library:mitte/demo/badge@1", "type": "lottie"}},
  "comps": {
    "main": {
      "size": [1920, 1080],
      "fps": 30,
      "duration": 5,
      "background": "$theme.color.bg",
      "layers": [
        {
          "id": "card",
          "type": "shape",
          "shape": "roundedRect",
          "size": [1100, 420],
          "radius": "$theme.radius.l",
          "fill": "$theme.color.surface",
          "origin": "center",
          "position": ["50%", "50%"],
          "styles": {"dropShadow": {"color": "#2B2440", "opacity": 14, "angle": 90, "distance": 24, "size": 64}}
        },
        {"id": "badge", "type": "comp", "origin": "center", "position": ["36%", "50%"], "scale": [220, 220], "stretch": 150, "lottie": "badge"},
        {
          "id": "title",
          "type": "text",
          "text": "Imported,\nthen edited",
          "style": {"font": "$theme.font.display", "size": "$theme.type.size.3", "fill": "$theme.color.fg"},
          "origin": "left",
          "position": ["48%", "50%"]
        }
      ],
      "timeline": [
        {"target": "card", "preset": "popIn", "ease": "$theme.spring.gentle", "at": 0.2},
        {"target": "badge", "preset": "popIn", "at": "<0.2"},
        {"target": "title/lines", "preset": "rise", "stagger": 0.1, "at": "<0.2"},
        {"target": "badge", "preset": "pulse", "at": 2.0},
        {"target": ["card", "badge", "title"], "preset": "fadeOut", "dur": 0.4, "at": 4.4}
      ]
    }
  }
}
```

### Cookbook 15: a 150 s piece (looping grid background with a long credits crawl) that the service chunks across workers; renders byte-identically in one process or in chunks

`SKILLS/library/examples/cookbook/15-chunked-long-render.motion.json`; theme `mitte/mono@1`; 1920 × 1080, 24 fps, 150 s; library: `mitte/bg.grid@1`, `mitte/credits.crawl@1`.

Check: expected warnings `lint.crawl_duration_mismatch`, `lint.text_outside_safe_area`, `lint.offscreen_while_visible`. The crawl sheet is taller than the frame; the whole-pixel speed changes the requested length slightly.

```json
{
  "motion": 1,
  "theme": {"use": "mitte/mono@1"},
  "data": {
    "sections": [
      {"kind": "card", "role": "Directed by", "names": ["Ana Ruiz"]},
      {"kind": "card", "role": "Produced by", "names": ["Ida Park", "Noa Weiss"], "join": "and"},
      {"kind": "heading", "text": "Cast"},
      {
        "kind": "pairs",
        "rows": [
          {"role": "Mara", "names": ["Lena Holt"]},
          {"role": "Joe", "names": ["Sam Li"]},
          {"role": "Fisherman", "names": ["Diego McAllister"]},
          {"role": "The Mayor", "names": ["Ola Nowak"]}
        ]
      },
      {"kind": "heading", "text": "Crew"},
      {
        "kind": "pairs",
        "rows": [
          {"role": "Director of Photography", "names": ["Ida Park"]},
          {"role": "Editor", "names": ["Noa Weiss"]},
          {"role": "Sound", "names": ["Kai Berg"]},
          {"role": "Colour", "names": ["Mia Lund"]}
        ]
      },
      {
        "kind": "grid",
        "title": "Visual Effects",
        "names": ["A. One", "B. Two", "C. Three", "D. Four", "E. Five", "F. Six", "G. Seven", "H. Eight"],
        "columns": 0
      },
      {"kind": "list", "title": "Special Thanks", "names": ["The people of Alfama", "Café Central", "North Light Fund"]},
      {"kind": "song", "title": "Night Drive", "lines": ["Written by K. Moss", "Performed by The Vales"]},
      {"kind": "text", "text": "Filmed on location in Lisbon, Portugal."},
      {"kind": "legal", "text": "© 2027 North Light Films. All Rights Reserved."}
    ]
  },
  "comps": {
    "main": {
      "size": [1920, 1080],
      "fps": 24,
      "duration": 150,
      "background": "$theme.color.bg",
      "layers": [
        {"id": "grid", "type": "component", "use": "mitte/bg.grid@1", "in": 0, "out": 150, "props": {"cell": 120, "speed": 10, "glow": 10}},
        {
          "id": "roll",
          "type": "component",
          "use": "mitte/credits.crawl@1",
          "in": 2,
          "out": 148,
          "props": {"sections": "$data.sections", "duration": 140, "font": "$theme.font.mono", "size": 30, "width": "70%"}
        }
      ]
    }
  },
  "output": {"format": "mp4", "codec": "h264", "quality": "high"}
}
```

### Cookbook 16: explainer: three numbered steps sequenced on voice-over phrase markers, clean theme

`SKILLS/library/examples/cookbook/16-explainer-steps.motion.json`; theme `mitte/clean@1`; 1920 × 1080, 30 fps, 16 s; library: `mitte/explainer.step@1`.

Check: no warnings. Instances take numeric `in` values (the markers are kept for the voice-over phrase times): a marker `in` on a component instance miscomputes its default `out` in engine 0.1.48 (see 03-components-using.md).

```json
{
  "motion": 1,
  "theme": {"use": "mitte/clean@1"},
  "assets": {"vo": {"src": "https://media.mitte.ai/u/p0/vo-explainer.wav", "type": "audio"}},
  "comps": {
    "main": {
      "size": [1920, 1080],
      "fps": 30,
      "duration": 16,
      "background": "$theme.color.bg",
      "markers": [{"t": 1.0, "name": "step1"}, {"t": 5.5, "name": "step2"}, {"t": 10.0, "name": "step3"}],
      "layers": [
        {"id": "voice", "type": "audio", "asset": "vo", "fadeOut": 0.5},
        {
          "id": "head",
          "type": "text",
          "text": "How it works",
          "style": {"font": "$theme.font.display", "size": "$theme.type.size.3", "fill": "$theme.color.fg"},
          "align": {"to": "safe", "x": "left", "y": "top"}
        },
        {
          "id": "s1",
          "type": "component",
          "use": "mitte/explainer.step@1",
          "in": 1.0,
          "props": {"n": 1, "title": "Connect your data", "body": "Link your warehouse in two clicks; nothing to install.", "hold": 13.5},
          "origin": "top-left",
          "position": ["12%", "26%"]
        },
        {
          "id": "s2",
          "type": "component",
          "use": "mitte/explainer.step@1",
          "in": 5.5,
          "props": {"n": 2, "title": "Describe the video", "body": "One sentence per scene. The assistant writes the document.", "hold": 9},
          "origin": "top-left",
          "position": ["12%", "48%"]
        },
        {
          "id": "s3",
          "type": "component",
          "use": "mitte/explainer.step@1",
          "in": 10.0,
          "props": {"n": 3, "title": "Render everywhere", "body": "16:9, 9:16 and 1:1 from one check.", "connector": false, "hold": 4.5},
          "origin": "top-left",
          "position": ["12%", "70%"]
        }
      ],
      "timeline": [{"target": "head", "preset": "rise", "at": 0.2}, {"target": "head", "preset": "fadeOut", "dur": 0.4, "at": 15.4}]
    }
  }
}
```

### Cookbook 17: kinetic quote on the editorial theme: words land one per beat, then the quote card with attribution

`SKILLS/library/examples/cookbook/17-kinetic-quote.motion.json`; theme `mitte/editorial@1`; 1920 × 1080, 30 fps, 10 s; library: `mitte/kinetic.words@1`, `mitte/quote.card@1`.

Check: expected warnings `lint.offscreen_while_visible`, `lint.text_outside_safe_area`, `lint.text_too_short_on_screen`. One word per beat is the look. quote.card's dash and attribution sit outside its canvas before they align: a lint false positive inside the component; the quote's text, linted where the instance puts it in the frame, runs past the title-safe box at the bottom.

```json
{
  "motion": 1,
  "theme": {"use": "mitte/editorial@1"},
  "comps": {
    "main": {
      "size": [1920, 1080],
      "fps": 30,
      "duration": 10,
      "background": "$theme.color.bg",
      "layers": [
        {
          "id": "words",
          "type": "component",
          "use": "mitte/kinetic.words@1",
          "in": 0.3,
          "props": {"words": ["Taste", "is", "a", "verb."], "beat": 0.55, "hold": 1.0, "tilt": 2}
        },
        {
          "id": "quote",
          "type": "component",
          "use": "mitte/quote.card@1",
          "in": 4.2,
          "props": {"quote": "Taste is a verb. You practise it every time you cut.", "attribution": "Ana Ruiz, editor", "hold": 3.4},
          "origin": "center",
          "position": ["50%", "50%"]
        }
      ],
      "timeline": [{"target": "quote", "preset": "fadeOut", "dur": 0.4, "at": 9.4}]
    }
  }
}
```

### Cookbook 18: product demo: a laptop with a screen recording slot, a cursor tour with click zooms, a toast

`SKILLS/library/examples/cookbook/18-ui-demo.motion.json`; theme `mitte/soft@1`; 1920 × 1080, 30 fps, 10 s; library: `mitte/screen.demo@1`, `mitte/ui.toast@1`.

Check: expected warnings `lint.missing_exit`, `lint.offscreen_while_visible`. screen.demo holds the device until its duration; the fade on the instance is the exit. device.laptop's camera dot is reported offscreen by lint (false positive inside the component).

```json
{
  "motion": 1,
  "theme": {"use": "mitte/soft@1"},
  "comps": {
    "main": {
      "size": [1920, 1080],
      "fps": 30,
      "duration": 10,
      "background": "$theme.color.bg",
      "layers": [
        {
          "id": "demo",
          "type": "component",
          "use": "mitte/screen.demo@1",
          "in": 0.3,
          "props": {
            "device": "laptop",
            "duration": 9,
            "fit": 46,
            "float": 6,
            "moves": [
              {"t": 0.0, "x": 1280, "y": 800},
              {"t": 1.2, "x": 1800, "y": 420, "click": true, "zoom": 1.6},
              {"t": 3.0, "x": 1800, "y": 420},
              {"t": 3.8, "x": 900, "y": 1000, "click": true, "zoom": 1},
              {"t": 5.2, "x": 1500, "y": 700, "click": true, "zoom": 1.8},
              {"t": 6.8, "x": 1500, "y": 700}
            ]
          },
          "slots": {
            "screen": [
              {"id": "app", "type": "solid", "color": "#FFFFFF", "size": [2560, 1600]},
              {"id": "bar", "type": "shape", "shape": "rect", "size": [2560, 120], "fill": "$theme.color.accent", "origin": "top-left", "position": [0, 0]},
              {
                "id": "appTitle",
                "type": "text",
                "text": "Projects",
                "style": {"font": "$theme.font.display", "size": 120, "fill": "$theme.color.fg"},
                "origin": "top-left",
                "position": [160, 260]
              },
              {
                "id": "btn",
                "type": "shape",
                "shape": "roundedRect",
                "size": [520, 140],
                "radius": 70,
                "fill": "$theme.color.accent",
                "origin": "center",
                "position": [1800, 420]
              },
              {
                "id": "btnLabel",
                "type": "text",
                "text": "New video",
                "style": {"font": "$theme.font.body", "size": 64, "fill": "$theme.color.accent.on"},
                "origin": "center",
                "position": [1800, 420]
              }
            ]
          }
        },
        {
          "id": "toast",
          "type": "component",
          "use": "mitte/ui.toast@1",
          "in": 6.0,
          "props": {"message": "Render started", "hold": 2},
          "origin": "top",
          "align": {"to": "safe", "x": "center", "y": "top"}
        }
      ],
      "timeline": [{"target": "demo", "preset": "fadeOut", "dur": 0.4, "at": 9.3}]
    }
  }
}
```

### Cookbook 19: a route draws over a map image, a pin drops at the destination, a callout names a stop

`SKILLS/library/examples/cookbook/19-map-route.motion.json`; theme `mitte/clean@1`; 1920 × 1080, 30 fps, 9 s; library: `mitte/callout.line@1`, `mitte/map.pin@1`, `mitte/map.route@1`.

Check: no warnings. The map image is a placeholder asset offline (asset.unmaterialized info).

```json
{
  "motion": 1,
  "theme": {"use": "mitte/clean@1"},
  "assets": {"map": {"src": "https://media.mitte.ai/u/p0/map-lisbon.jpg", "type": "image"}},
  "comps": {
    "main": {
      "size": [1920, 1080],
      "fps": 30,
      "duration": 9,
      "background": "$theme.color.bg",
      "layers": [
        {
          "id": "route",
          "type": "component",
          "use": "mitte/map.route@1",
          "in": 0.2,
          "props": {
            "map": "map",
            "route": "M 240 620 C 500 300, 900 760, 1360 280",
            "from": [240, 620],
            "to": [1360, 280],
            "fromLabel": "Porto",
            "toLabel": "Lisbon",
            "draw": 3,
            "hold": 4.5
          },
          "origin": "center",
          "position": ["50%", "50%"]
        },
        {
          "id": "pin",
          "type": "component",
          "use": "mitte/map.pin@1",
          "in": 3.6,
          "props": {"at": ["76%", "38%"], "label": "Lisbon", "sub": "Arrive 18:40", "hold": 3.5}
        },
        {
          "id": "stop",
          "type": "component",
          "use": "mitte/callout.line@1",
          "in": 5.2,
          "props": {"at": ["47%", "55%"], "title": "Coimbra", "body": "Coffee stop, 20 min", "dx": -240, "dy": -160, "hold": 2.6}
        }
      ]
    }
  }
}
```

### Cookbook 20: 9:16 outro: countdown, a subscribe CTA, a platform frame with handle and progress

`SKILLS/library/examples/cookbook/20-countdown-end-card.motion.json`; theme `mitte/bold@1`; 1080 × 1920, 30 fps, 9 s; library: `mitte/bg.gradient-mesh@1`, `mitte/countdown@1`, `mitte/cta.subscribe@1`, `mitte/social.frame@1`.

Check: expected warnings `lint.missing_exit`, `lint.text_outside_safe_area`, `lint.text_too_short_on_screen`. The frame's progress bar runs to the end by design; the countdown's digits hold one beat each (shorter than a word's reading time) and its GO punches past the frame, as a countdown does.

```json
{
  "motion": 1,
  "theme": {"use": "mitte/bold@1"},
  "lint": {"platform": "shorts"},
  "comps": {
    "main": {
      "size": [1080, 1920],
      "fps": 30,
      "duration": 9,
      "background": "$theme.color.bg",
      "safe": "shorts",
      "layers": [
        {"id": "bg", "type": "component", "use": "mitte/bg.gradient-mesh@1", "props": {"period": 6}},
        {"id": "frame", "type": "component", "use": "mitte/social.frame@1", "props": {"handle": "@mitte", "platform": "shorts", "duration": 9}},
        {
          "id": "count",
          "type": "component",
          "use": "mitte/countdown@1",
          "in": 0.4,
          "props": {"go": "GO", "hold": 1.0},
          "origin": "center",
          "position": ["50%", "42%"]
        },
        {
          "id": "sub",
          "type": "component",
          "use": "mitte/cta.subscribe@1",
          "in": 5.0,
          "props": {"channel": "mitte motion", "initial": "m", "hold": 2.0},
          "origin": "center",
          "position": ["50%", "58%"]
        }
      ]
    }
  }
}
```

<!-- gen:library-cookbook-2:end -->
