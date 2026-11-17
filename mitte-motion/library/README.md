# SKILLS / library: the complete reference of the rexx library for AI assistants

Everything an assistant needs to use and extend the mitte motion library: every theme and token, every preset, every component with every param and slot, the engine-backed captions and credits, transitions as components, the demo assets and reels, the synthesized sound pack and the font pack, recipes and twenty checked documents. Every claim was verified against engine 0.1.48 (`rexx-engine check`, canonical output, the normalizer source); where the code and spec 12 disagree, the page says `> **Spec gap:**` and documents the code.

<!-- gen:library-counts:start -->
Library version 2026.10.0: 10 themes, 9 presets, 103 components (15 groups), 206 example documents, 89 font families.
<!-- gen:library-counts:end -->

| Page | One line |
|---|---|
| `00-overview.md` | what the library is, reference syntax and versions, where the engine finds it, `library:` assets, the catalogue, diagnostics, checking a document locally |
| `01-themes.md` | the theme object and merge order, every token group and token, derived tokens and color modifiers, springs, textures, styles, brand kits, the ten themes compared and every value |
| `02-presets.md` | using presets, the three library packs, the built-in names, writing a preset, every rule the engine enforces |
| `03-components-using.md` | instances: `use`, `props`, `slots`, `in`/`out`, `collapse`; param validation; what normalization produces; placement; variants; repeats of instances; nesting; engine-backed components |
| `04-components-writing.md` | the definition format, every param type, structure switches, slots and forwarding, the `x-library` file and examples file, testing, review and versioning |
| `05-captions.md` | the four `caption.*` components: shared params, per-style defaults, the word-timings input, what the engine builds and what it does not yet |
| `06-credits.md` | the eight `credits.*` components: the sections document, shared style params, crawl speed and duration, what the engine builds |
| `07-transitions.md` | transitions as components in `scenes`, by hand, and how to write one; the 14 shipped transition components |
| `08-demos-reels.md` | every `library:mitte/demo/…` asset and the three reels scene by scene with the constructs to copy |
| `09-sound-fonts.md` | the planned sound pack (not shipped) and every font family with license, roles, scripts and build |
| `10-recipes.md` | fifteen briefs as patterns mapped to the components that ship and to the cookbook |
| `11-cookbook-1.md`, `12-cookbook-2.md` | twenty complete documents for common briefs, embedded from `examples/cookbook/`, each checked |
| `90-catalogue.md` | generated index of every entry (themes, presets, components by group) |
| `91-components-<group>.md` | generated: every component of a group with every param, slot, example, engine note and reviewer note (15 files: backgrounds, captions, credits, data, explainers, logo, lower-thirds, maps, music, overlays, particles, social, titles, transitions, ui) |
| `92-themes.md` | generated: every token of every theme |
| `93-presets.md` | generated: every preset with params and tweens |
| `examples/concepts/` | the documents the concept pages embed (13), `examples/cookbook/` the twenty cookbook documents, each with declared expected warnings; `04-library/` an example library entry |

## Scripts

- `scripts/skills-library-index.py` regenerates the `9x` pages and the generated sections (`<!-- gen:<name>:start/end -->`) in `README.md`, `01-themes.md`, `09-sound-fonts.md`, `11-cookbook-1.md`, `12-cookbook-2.md` from `library/index.json`, the library files, `library/README.md` and `fonts/pack.toml`; `--check` fails when anything is stale.
- `scripts/skills-library-check.py` runs `rexx-engine check` on every example (`REXX_ENGINE_BIN=<binary> python3 scripts/skills-library-check.py`); a document fails on any error; expected warnings are listed in `meta.x-skills.expectWarnings`; `meta.x-skills.library` points a document at another library directory and a sibling `<name>.assets.json` is passed as `--assets`.

## Spec gaps found (summary)

Each is detailed on the page named. Overview: every entry is `draft` and resolves; the tree differs from the spec's packaging sketch. Themes: `type.size.<n>` accepts any n; brand-kit fonts are declared as `brand.font.<n>` assets but not fetched by the service. Presets: percent `dur`/`at` only in built-ins. Components: the examples file uses `{ id, title, doc }`.pop`'s shadow and per-word pop, `[x, y]` positions and SRT/VTT input are not implemented. Transitions: the crossfade fallback (a layer with marker times or a `matte`) is an info, not a warning.
