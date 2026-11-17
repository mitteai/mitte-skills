# Cookbook 1: ten complete documents for common briefs

Every document below is a file under `examples/cookbook/` that `rexx-engine check` passes with zero errors (`scripts/skills-library-check.py`); the warnings each one expects are declared in its `meta.x-skills` and explained. Copy the file, swap the theme, text and assets, re-check. The JSON here is embedded from the files by `scripts/skills-library-index.py` (the `meta` block is left out). `12-cookbook-2.md` has the other ten.

| # | Brief | Built from |
|---|---|---|
| 01 | lower third over footage, two speakers | `lower-third.bar`, `lower-third.split`, a vignette grade, `safe: broadcast`, a 9:16 variant |
| 02 | title card on a looping background | `bg.gradient-mesh`, `title.card`, three aspect ratios |
| 03 | data story | `scenes` with `title.card`, `chart.bar` from `data`, `stat.row`, a kinetic takeaway, `transition.wipe`, `push`, `transition.shape` |
| 04 | social ad 9:16 with captions and an end card | footage, `title.kinetic` hook, `caption.pop`, `title.highlight` offer, `cta.endcard`, 1:1 and 16:9 variants |
| 05 | logo sting | `logo.sting` on `neon`, `particles.confetti` on a marker, `toneMap: soft` |
| 06 | captions from a transcript data asset | `caption.karaoke` reading `$data.@transcript.words`, a cover still, a podcast kicker |
| 07 | physics text drop | per-character `dynamic` bodies, floor and walls, an `explosion` force, `settle` back to the layout |
| 08 | particle bursts on beats | `bg.aurora`, `particles.burst-on-beat` on `@beat*` markers, `kinetic.words` |
| 09 | 3D title | `threeDPerChar` text flipping in under a spot light with shadows, a camera dolly with a focus pull |
| 10 | a label tracked onto footage | the demo tracking clip, a point track made by `rexx-engine track`, `position.track` |

<!-- gen:library-cookbook-1:start -->
### Cookbook 01: lower third over footage, two speakers, corporate theme

`SKILLS/library/examples/cookbook/01-lower-third.motion.json`; theme `mitte/corporate@1`; 1920 × 1080, 30 fps, 14 s; variants `vertical`; library: `mitte/lower-third.bar@1`, `mitte/lower-third.split@1`.

Check: expected warnings `lint.motion_blur_off_fast_motion`, `lint.offscreen_while_visible`. offscreen_while_visible on lower-third.bar's tick is a known lint false positive. motion_blur_off_fast_motion comes from lower-third.split's own exit slide.

```json
{
  "motion": 1,
  "theme": {"use": "mitte/corporate@1"},
  "assets": {"clip": {"src": "https://media.mitte.ai/u/p0/interview-16x9.mp4", "type": "video"}},
  "comps": {
    "main": {
      "size": [1920, 1080],
      "fps": 30,
      "duration": 14,
      "background": "#000000",
      "safe": "broadcast",
      "layers": [
        {"id": "clip", "type": "video", "asset": "clip", "fit": "cover", "fadeOut": 1.0},
        {"id": "grade", "type": "adjustment", "effects": [{"type": "stylize.vignette", "params": {"amount": -0.25}}]},
        {
          "id": "lt1",
          "type": "component",
          "use": "mitte/lower-third.bar@1",
          "in": 1.5,
          "props": {"name": "Ada Lovelace", "role": "Chief Analyst, Engine Co.", "hold": 3.5, "plate": "$theme.color.surface.a80"},
          "align": {"to": "safe", "x": "left", "y": "bottom"}
        },
        {
          "id": "lt2",
          "type": "component",
          "use": "mitte/lower-third.split@1",
          "in": 8,
          "props": {"name": "Grace Hopper", "role": "Rear Admiral", "hold": 3},
          "align": {"to": "safe", "x": "left", "y": "bottom"}
        }
      ]
    }
  },
  "variants": {"vertical": {"size": [1080, 1920], "safe": "reels", "override": {"lt1": {"props": {"role": "Chief Analyst"}}}}}
}
```

### Cookbook 02: title card on a looping gradient mesh, three aspect ratios

`SKILLS/library/examples/cookbook/02-title-card.motion.json`; theme `mitte/midnight@1`; 1920 × 1080, 30 fps, 6 s; variants `vertical`, `square`; library: `mitte/bg.gradient-mesh@1`, `mitte/title.card@1`.

```json
{
  "motion": 1,
  "theme": {"use": "mitte/midnight@1"},
  "comps": {
    "main": {
      "size": [1920, 1080],
      "fps": 30,
      "duration": 6,
      "background": "$theme.color.bg",
      "layers": [
        {"id": "bg", "type": "component", "use": "mitte/bg.gradient-mesh@1", "props": {"drift": 120, "period": 8}},
        {
          "id": "title",
          "type": "component",
          "use": "mitte/title.card@1",
          "in": 0.4,
          "props": {"kicker": "KEYNOTE 2027", "headline": "Motion for\neveryone", "subline": "One document, every format", "hold": 3.2},
          "origin": "center",
          "position": ["50%", "50%"]
        }
      ],
      "timeline": [{"target": "title", "preset": "fadeOut", "dur": 0.4, "at": 5.1}]
    }
  },
  "variants": {"vertical": {"size": [1080, 1920], "safe": "reels"}, "square": {"size": [1080, 1080], "safe": "square"}}
}
```

### Cookbook 03: data story: title, bar chart from data, three KPIs, takeaway, scenes with library transitions

`SKILLS/library/examples/cookbook/03-data-story.motion.json`; theme `mitte/clean@1`; 1920 × 1080, 30 fps, auto s; library: `mitte/chart.bar@1`, `mitte/stat.row@1`, `mitte/title.card@1`, `mitte/transition.shape@1`, `mitte/transition.wipe@1`.

Check: expected warnings `lint.missing_exit`, `lint.motion_blur_off_fast_motion`, `lint.offscreen_while_visible`. Scenes end on transitions by design. The built-in push and transition.shape move scenes and sweeps fast by design; the sweeps start offscreen.

```json
{
  "motion": 1,
  "theme": {"use": "mitte/clean@1"},
  "data": {
    "rows": [
      {"label": "Jan", "value": 12},
      {"label": "Feb", "value": 19},
      {"label": "Mar", "value": 24},
      {"label": "Apr", "value": 21},
      {"label": "May", "value": 33},
      {"label": "Jun", "value": 41}
    ],
    "kpis": [
      {"value": 41, "suffix": "K", "label": "Signups in June"},
      {"value": 98, "suffix": "%", "label": "Uptime"},
      {"value": 140, "suffix": "+", "label": "Countries"}
    ]
  },
  "comps": {
    "intro": {
      "size": [1920, 1080],
      "fps": 30,
      "duration": 3,
      "background": "$theme.color.bg",
      "layers": [
        {
          "id": "t",
          "type": "component",
          "use": "mitte/title.card@1",
          "in": 0.2,
          "props": {"kicker": "H1 2027", "headline": "Signups doubled", "subline": "Monthly signups, thousands", "hold": 1.5},
          "origin": "center",
          "position": ["50%", "50%"]
        }
      ]
    },
    "chart": {
      "size": [1920, 1080],
      "fps": 30,
      "duration": 7,
      "background": "$theme.color.bg",
      "layers": [
        {
          "id": "title",
          "type": "text",
          "text": "Signups, H1 2027 (thousands)",
          "style": {"font": "$theme.font.display", "size": "$theme.type.size.2", "fill": "$theme.color.fg"},
          "align": {"to": "safe", "x": "left", "y": "top"}
        },
        {
          "id": "chart",
          "type": "component",
          "use": "mitte/chart.bar@1",
          "in": 0.4,
          "props": {"series": "$data.rows", "max": 45, "highlight": "Jun", "hold": 3},
          "origin": "bottom",
          "align": {"to": "safe", "x": "center", "y": "bottom"}
        }
      ],
      "timeline": [{"target": "title", "preset": "rise", "at": 0.1}]
    },
    "kpis": {
      "size": [1920, 1080],
      "fps": 30,
      "duration": 5,
      "background": "$theme.color.bg",
      "layers": [
        {
          "id": "row",
          "type": "component",
          "use": "mitte/stat.row@1",
          "in": 0.2,
          "props": {"stats": "$data.kpis", "hold": 2.6},
          "origin": "center",
          "position": ["50%", "50%"]
        }
      ]
    },
    "outro": {
      "size": [1920, 1080],
      "fps": 30,
      "duration": 3,
      "background": "$theme.color.accent",
      "layers": [
        {
          "id": "t",
          "type": "text",
          "text": "Ship faster.",
          "style": {"font": "$theme.font.display", "size": "$theme.type.size.6", "fill": "$theme.color.accent.on"},
          "origin": "center",
          "position": ["50%", "50%"]
        }
      ],
      "timeline": [{"target": "t/words", "preset": "rise", "stagger": 0.1, "at": 0.2}, {"target": "t", "preset": "fadeOut", "dur": 0.4, "at": 2.5}]
    },
    "main": {
      "size": [1920, 1080],
      "fps": 30,
      "duration": "auto",
      "scenes": [
        {"comp": "intro", "dur": 3},
        {"transition": {"type": "mitte/transition.wipe@1", "dur": 0.7, "props": {"angle": 100}}},
        {"comp": "chart", "dur": 7},
        {"transition": {"type": "push", "dir": "up", "dur": 0.5}},
        {"comp": "kpis", "dur": 5},
        {"transition": {"type": "mitte/transition.shape@1", "dur": 0.8}},
        {"comp": "outro", "dur": 3}
      ],
      "layers": []
    }
  }
}
```

### Cookbook 04: social ad 9:16: hook, footage with captions, offer, CTA end card; 1:1 and 16:9 variants

`SKILLS/library/examples/cookbook/04-social-ad-9x16.motion.json`; theme `mitte/bold@1`; 1080 × 1920, 30 fps, 15 s; variants `square`, `landscape`; library: `mitte/caption.pop@1`, `mitte/cta.endcard@1`, `mitte/title.highlight@1`, `mitte/title.kinetic@1`.

Check: expected warnings `lint.duration_mismatch`, `lint.missing_exit`, `lint.text_outside_safe_area`, `lint.tween_overlap`. Caption instances end at their last word; the audio asset is a placeholder offline. cta.endcard lays its line out for 16:9 (no size param) and overlaps its own button pulse: component limitations on 9:16.

```json
{
  "motion": 1,
  "theme": {"use": "mitte/bold@1"},
  "assets": {
    "plate": {"src": "https://media.mitte.ai/u/p0/plate-city-9x16.mp4", "type": "video"},
    "vo": {"src": "https://media.mitte.ai/u/p0/vo-fathom.wav", "type": "audio"},
    "logo": {"src": "library:mitte/demo/logo@1", "type": "svg"}
  },
  "lint": {"platform": "tiktok"},
  "comps": {
    "main": {
      "size": [1080, 1920],
      "fps": 30,
      "duration": 15,
      "background": "#000000",
      "safe": "tiktok",
      "layers": [
        {"id": "plate", "type": "video", "asset": "plate", "fit": "cover", "mute": true, "out": 12},
        {"id": "grade", "type": "adjustment", "effects": [{"type": "stylize.vignette", "params": {"amount": -0.35}}], "out": 12},
        {
          "id": "hook",
          "type": "component",
          "use": "mitte/title.kinetic@1",
          "in": 0.2,
          "props": {"headline": "Stop editing. Start shipping.", "hold": 1.2},
          "origin": "center",
          "position": ["50%", "40%"]
        },
        {
          "id": "captions",
          "type": "component",
          "use": "mitte/caption.pop@1",
          "in": 3.0,
          "props": {
            "words": [
              {"text": "Every", "start": 0.0, "end": 0.3},
              {"text": "edit", "start": 0.3, "end": 0.6},
              {"text": "becomes", "start": 0.7, "end": 1.1},
              {"text": "a", "start": 1.1, "end": 1.2},
              {"text": "video", "start": 1.2, "end": 1.6},
              {"text": "in", "start": 2.0, "end": 2.15},
              {"text": "minutes.", "start": 2.15, "end": 2.8},
              {"text": "Not", "start": 3.3, "end": 3.5},
              {"text": "days.", "start": 3.5, "end": 4.1}
            ],
            "position": "safe-center"
          }
        },
        {
          "id": "offer",
          "type": "component",
          "use": "mitte/title.highlight@1",
          "in": 8,
          "props": {"lead": "First month", "phrase": "free", "hold": 2.2},
          "origin": "center",
          "position": ["50%", "50%"]
        },
        {
          "id": "end",
          "type": "component",
          "use": "mitte/cta.endcard@1",
          "in": 11.5,
          "props": {"logo": "logo", "line": "Try it today", "button": "Get started", "url": "mitte.ai", "duration": 3.5}
        },
        {"id": "voice", "type": "audio", "asset": "vo", "in": 3.0, "fadeOut": 0.5}
      ]
    }
  },
  "variants": {
    "square": {"size": [1080, 1080], "safe": "square", "lint": {"platform": "none"}, "override": {"captions": {"props": {"lines": 1}}}},
    "landscape": {"size": [1920, 1080], "safe": "youtube", "lint": {"platform": "youtube"}}
  }
}
```

### Cookbook 05: logo sting on neon with confetti on the resolve, soft tone map

`SKILLS/library/examples/cookbook/05-logo-sting.motion.json`; theme `mitte/neon@1`; 1920 × 1080, 30 fps, 5 s; library: `mitte/logo.sting@1`, `mitte/particles.confetti@1`.

Check: expected warnings `lint.too_many_simultaneous_moves`, `lint.expensive_effect`. logo.sting's six sparkles and its glow and bloom are the component's own; the confetti burst is the point.

```json
{
  "motion": 1,
  "theme": {"use": "mitte/neon@1"},
  "assets": {"logo": {"src": "library:mitte/demo/logo@1", "type": "svg"}},
  "comps": {
    "main": {
      "size": [1920, 1080],
      "fps": 30,
      "duration": 5,
      "background": "$theme.color.bg",
      "markers": [{"t": 0.9, "name": "resolve"}],
      "layers": [
        {
          "id": "sting",
          "type": "component",
          "use": "mitte/logo.sting@1",
          "in": 0.2,
          "props": {"logo": "logo", "width": 460, "tagline": "made with motion", "glow": 2.8, "hold": 2.4},
          "origin": "center",
          "position": ["50%", "50%"]
        },
        {"id": "boom", "type": "component", "use": "mitte/particles.confetti@1", "props": {"at": "@resolve", "amount": 220, "origin": ["50%", "60%"]}}
      ]
    }
  },
  "output": {"format": "mp4", "codec": "h264", "quality": "high", "toneMap": "soft"}
}
```

### Cookbook 06: karaoke captions from a transcript data asset over a podcast still, 1:1

`SKILLS/library/examples/cookbook/06-captions-from-transcript.motion.json`; theme `mitte/mono@1`; 1080 × 1080, 30 fps, 8 s; library: `mitte/caption.karaoke@1`.

Check: expected warnings `lint.missing_exit`, `lint.text_outside_safe_area`. 06-captions-from-transcript.assets.json maps `transcript` to transcript.words.json beside it (the service fetches the https URL). The caption box is larger than the safe band on purpose.

```json
{
  "motion": 1,
  "theme": {"use": "mitte/mono@1"},
  "assets": {
    "cover": {"src": "https://media.mitte.ai/u/p0/podcast-cover.jpg", "type": "image"},
    "vo": {"src": "https://media.mitte.ai/u/p0/vo-fathom.wav", "type": "audio"},
    "transcript": {"src": "https://media.mitte.ai/u/p0/vo-fathom.words.json", "type": "data"}
  },
  "comps": {
    "main": {
      "size": [1080, 1080],
      "fps": 30,
      "duration": 8,
      "background": "$theme.color.bg",
      "safe": "square",
      "layers": [
        {"id": "cover", "type": "image", "asset": "cover", "fit": "cover", "box": [1080, 1080]},
        {"id": "shade", "type": "solid", "color": "$theme.color.bg.a40"},
        {
          "id": "show",
          "type": "text",
          "text": "THE MOTION HOUR",
          "style": {"font": "$theme.font.display", "size": "$theme.type.size.1", "fill": "$theme.color.accent", "tracking": 200},
          "align": {"to": "safe", "x": "center", "y": "top"}
        },
        {
          "id": "captions",
          "type": "component",
          "use": "mitte/caption.karaoke@1",
          "in": 0.5,
          "props": {"words": "$data.@transcript.words", "group": {"maxWords": 4, "maxChars": 22}, "position": "safe-bottom", "lines": 2}
        },
        {"id": "voice", "type": "audio", "asset": "vo", "in": 0.5, "fadeOut": 0.5}
      ],
      "timeline": [{"target": "show", "preset": "trackIn", "at": 0.2}]
    }
  }
}
```

### Cookbook 07: letters fall as rigid bodies, pile up, an explosion scatters them, they settle back into the layout

`SKILLS/library/examples/cookbook/07-physics-text-drop.motion.json`; theme `mitte/bold@1`; 1920 × 1080, 30 fps, 6 s.

Check: expected warnings `lint.text_outside_safe_area`, `lint.offscreen_while_visible`. Letters that are thrown against the walls leave the safe area; that is the piece.

```json
{
  "motion": 1,
  "theme": {"use": "mitte/bold@1"},
  "comps": {
    "main": {
      "size": [1920, 1080],
      "fps": 30,
      "duration": 6,
      "background": "$theme.color.bg",
      "motionBlur": {"shutterAngle": 180},
      "physics": {
        "gravity": [0, 2600],
        "world": {"floor": 1000, "walls": ["left", "right"]},
        "seed": 4,
        "vary": {"velocity": 80, "spin": 60, "rotation": 0, "position": 0},
        "forces": [{"type": "explosion", "at": 2.2, "center": [960, 760], "strength": 700, "radius": 900, "spin": 200}]
      },
      "layers": [
        {
          "id": "word",
          "type": "text",
          "text": "GRAVITY",
          "style": {"font": "$theme.font.display", "size": 220, "weight": 800, "fill": "$theme.color.fg"},
          "origin": "center",
          "position": ["50%", "45%"],
          "motionBlur": true,
          "body": {
            "type": "dynamic",
            "per": "chars",
            "shape": "hull",
            "inset": 2,
            "restitution": 0.25,
            "friction": 0.6,
            "start": 0.8,
            "settle": {"at": 3.6, "dur": 0.9, "to": "layout", "ease": "back.out(1.4)", "stagger": {"each": 0.06, "from": "start"}}
          }
        },
        {"id": "floorLine", "type": "shape", "shape": "rect", "size": [1920, 4], "fill": "$theme.color.line", "origin": "center", "position": [960, 1002]}
      ],
      "timeline": [{"target": "word", "preset": "fadeIn", "dur": 0.3, "at": 0}, {"target": ["word", "floorLine"], "preset": "fadeOut", "dur": 0.4, "at": 5.5}]
    }
  }
}
```

### Cookbook 08: particle bursts on beat markers over an aurora background, kinetic words on the beat

`SKILLS/library/examples/cookbook/08-particle-burst.motion.json`; theme `mitte/neon@1`; 1920 × 1080, 30 fps, 6 s; library: `mitte/bg.aurora@1`, `mitte/kinetic.words@1`, `mitte/particles.burst-on-beat@1`.

Check: expected warnings `lint.text_too_short_on_screen`, `lint.expensive_effect`. One word per beat is the look; the aurora and bursts are full-frame effects.

```json
{
  "motion": 1,
  "theme": {"use": "mitte/neon@1"},
  "comps": {
    "main": {
      "size": [1920, 1080],
      "fps": 30,
      "duration": 6,
      "background": "$theme.color.bg",
      "markers": [
        {"t": 0.5, "name": "beat1"},
        {"t": 1.0, "name": "beat2"},
        {"t": 1.5, "name": "beat3"},
        {"t": 2.0, "name": "beat4"},
        {"t": 2.5, "name": "beat5"},
        {"t": 3.0, "name": "beat6"}
      ],
      "layers": [
        {"id": "sky", "type": "component", "use": "mitte/bg.aurora@1", "props": {"intensity": 60, "period": 8}},
        {"id": "bursts", "type": "component", "use": "mitte/particles.burst-on-beat@1", "props": {"markers": "@beat*", "amount": 120}},
        {
          "id": "words",
          "type": "component",
          "use": "mitte/kinetic.words@1",
          "in": 0.5,
          "props": {"words": ["Loud", "ideas", "deserve", "motion."], "beat": 0.5, "hold": 1.6}
        }
      ]
    }
  },
  "output": {"toneMap": "soft"}
}
```

### Cookbook 09: 3D title: per-character 3D text flipping in under a spot light with floor shadows and a camera dolly with focus pull

`SKILLS/library/examples/cookbook/09-3d-title.motion.json`; theme `mitte/midnight@1`; 1920 × 1080, 30 fps, 6 s.

Check: expected warnings `lint.expensive_effect`. Shadows plus depth of field cost about 0.5 s per frame at 1080p: the point of the piece.

```json
{
  "motion": 1,
  "theme": {"use": "mitte/midnight@1"},
  "comps": {
    "main": {
      "size": [1920, 1080],
      "fps": 30,
      "duration": 6,
      "background": "$theme.color.bg",
      "renderer3d": "classic",
      "motionBlur": {"shutterAngle": 180},
      "layers": [
        {
          "id": "cam",
          "type": "camera",
          "cameraType": "twoNode",
          "focalLength": 50,
          "transform": {"position": {"keys": [{"t": 0, "v": [960, 420, -2600], "ease": "power2.inOut"}, {"t": 5, "v": [960, 480, -1900]}]}, "pointOfInterest": [960, 540, 0]},
          "dof": {"enabled": true, "focusOn": "title", "aperture": 40, "blurLevel": 80}
        },
        {"id": "ambient", "type": "light", "kind": "ambient", "intensity": 35},
        {
          "id": "key",
          "type": "light",
          "kind": "spot",
          "intensity": 120,
          "coneAngle": 70,
          "castsShadows": true,
          "transform": {"position": [700, -200, -900], "pointOfInterest": [960, 540, 0]}
        },
        {
          "id": "floor",
          "type": "solid",
          "color": "$theme.color.surface",
          "size": [4000, 3000],
          "threeD": true,
          "material": {"acceptsShadows": true, "diffuse": 70},
          "transform": {"position": [960, 760, 600], "rotationX": 90}
        },
        {
          "id": "title",
          "type": "text",
          "text": "DEPTH",
          "threeD": true,
          "threeDPerChar": true,
          "style": {"font": "$theme.font.display", "size": 260, "fill": "$theme.color.fg"},
          "origin": "center",
          "material": {"castsShadows": "on"},
          "transform": {"position": [960, 640, 0]}
        },
        {
          "id": "sub",
          "type": "text",
          "text": "a title filmed through the comp camera",
          "style": {"font": "$theme.font.mono", "size": 30, "fill": "$theme.color.muted"},
          "origin": "bottom",
          "align": {"to": "safe", "x": "center", "y": "bottom"}
        }
      ],
      "timeline": [
        {"target": "title/chars", "preset": "flipIn", "stagger": 0.08, "at": 0.3},
        {"target": "sub", "preset": "fadeIn", "at": 1.2},
        {"target": ["title", "sub"], "preset": "fadeOut", "dur": 0.5, "at": 5.3}
      ]
    }
  }
}
```

### Cookbook 10: a label tracked onto moving footage (the demo tracking clip), two steps: motion.track then this document

`SKILLS/library/examples/cookbook/10-tracked-title.motion.json`; theme `mitte/midnight@1`; 960 × 540, 30 fps, 6 s.

Check: no warnings. tracking-clip.track.json beside this file was made by `rexx-engine track` on the demo clip (point item `tag` at [240, 300]); 10-tracked-title.assets.json maps the `tk` asset to it so the check runs offline.

```json
{
  "motion": 1,
  "theme": {"use": "mitte/midnight@1"},
  "assets": {
    "clip": {"src": "library:mitte/demo/tracking-clip@1", "type": "video"},
    "tk": {"src": "https://media.mitte.ai/u/p0/tracking-clip.track.json", "type": "track"}
  },
  "comps": {
    "main": {
      "size": [960, 540],
      "fps": 30,
      "duration": 6,
      "background": "#000000",
      "layers": [
        {"id": "clip", "type": "video", "asset": "clip", "box": [960, 540], "fit": "cover"},
        {
          "id": "tag",
          "type": "text",
          "text": "TAG · tracked",
          "style": {"font": "$theme.font.display", "size": 28, "fill": "#FFFFFF"},
          "origin": "center",
          "position": {"track": {"asset": "tk", "item": "tag", "layer": "clip", "offset": [90, -60], "smooth": 0.15, "lost": "hold"}},
          "effects": [{"id": "shadow", "type": "stylize.dropShadow", "params": {"opacity": 60, "distance": 4, "softness": 12}}],
          "motionBlur": true
        }
      ],
      "timeline": [{"target": "tag", "preset": "popIn", "at": 0.5}]
    }
  }
}
```

<!-- gen:library-cookbook-1:end -->
