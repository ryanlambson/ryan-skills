---
name: visualising-hospitality-spaces
description: >
  Master orchestrator for the hts-spatial-suite. Use whenever Ryan wants to turn a
  hospitality floor plan into a client-facing visualisation end to end — phrases like
  "turn this floor plan into a render", "visualise this venue to show the client",
  "take this DWG to a photoreal image", or "run the spatial pipeline". Routes the job
  through four stages (intake, model, render-prep, render) and hands off to the component
  skills modelling-hospitality-plans, preparing-render-views, and rendering-with-nano-banana. Loads the Trimble
  SketchUp MCP baseline skills first. Do NOT use for spec-grade or compliance-certified
  drawings, or for liquor-licensing PIA spatial work (that stays in hts-lla-suite).
metadata:
  author: Ryan Lambson (HTS / Green Holmes)
  version: 1.0.0
  standard: agent-skills-1.0
  status: drafted
---

# Spatial Pipeline — Orchestrator

Drive a hospitality floor plan from 2D to a sell-the-idea photoreal render, keeping a human
checkpoint at each stage hand-off. This skill owns the *routing and the hand-off artifacts*;
the three worker skills own the actual work. The output sells the concept — it is not a spec
or compliance document.

## What this system is NOT
- Not a spec/compliance tool. Renders sell the concept; they do not certify it. Refuse to
  present any output as a compliance or as-built document. Spec-grade checks are the deferred
  v2 `spatial-compliance` skill.
- Not a SketchUp tutorial. SketchUp mechanics come from the Trimble baseline skills, which
  win on *how to build and style in SketchUp* (see Authority hierarchy).
- Not for liquor-licensing PIA spatial work — that stays in `hts-lla-suite`.

## Trigger phrases → stage routing
| The user says… | Route |
|---|---|
| "turn this plan into a render", "visualise this venue", "run the spatial pipeline" | Full pipeline: intake → model → render-prep → render |
| "model this plan", "build the 3D from this DWG" | Stop after `modelling-hospitality-plans` |
| "set up the view for rendering", "export a clean line view" | Enter at `preparing-render-views` (model already exists) |
| "render this view", "make this photoreal", "I already have a view" | Enter at `rendering-with-nano-banana` (line-work image already exists) |
| Raster-only input (PDF/photo/sketch), "quick render of this sketch" | Express lane — skip precise modeling, go sketch → render-prep → render |

Always confirm the **jurisdiction** (US or AU; default AU) and the **end stage** before
starting, so the user only pays for the stages they want.

## Authority hierarchy
1. **Trimble SketchUp MCP baseline skills** — win on SketchUp mechanics (geometry, cleansing,
   solids, camera, styles, scenes). Never rebuild what they provide.
2. **This suite's knowledge modules** — win on the hospitality domain: `knowledge/hospitality-standards.md`
   (dimensional defaults) and `knowledge/materials-semantic-template.md` (semantic map + prompt formula).
3. **Jurisdiction block** inside `hospitality-standards.md` — US (ADA) or AU (NCC / AS 1428.1),
   selected per job. Figures are sane **DEFAULTS**, never certified compliance values.
4. **Source research doc** (`source/research-report.docx`) — conceptual reference only. Its
   Ruby/boolean code does NOT run on the Python, no-boolean Trimble MCP. Do not copy code from it.

## The four-stage pipeline
Each stage has a defined input, a defined output artifact, and a human checkpoint. Do not
advance until the artifact exists and the user approves it.

| Stage | Skill | In | Out (hand-off artifact) |
|---|---|---|---|
| 1. Intake | (this skill) | DWG/DXF/SKP, or PDF/sketch/photo | Cleaned, scaled import in the right lane + chosen jurisdiction |
| 2. Model | `modelling-hospitality-plans` | Cleaned plan | Tagged, watertight 3D SketchUp model (openings framed, no booleans) |
| 3. Render-prep | `preparing-render-views` | 3D model | Flat line-work PNG/JPG that locks the perspective (validated by `validate_export.py`) |
| 4. Render | `rendering-with-nano-banana` | Line-work image + prompt | Photoreal client render(s): `nano_banana_2` to iterate, `nano_banana_pro` for the final 4K |

Express lane: a raster-only input skips stage 2's precise modeling — route the sketch straight
into render-prep (to set framing/semantic colour) and render. Tell the user the geometry will
be only as accurate as their sketch.

## Pre-flight (before the first build_model)
Before any modeling, prime the Trimble MCP's own skills:
1. Call `list_skills` to see the current baseline + contextual set.
2. `read_skill` **every baseline** skill — at time of writing: `sketchup-sdk`,
   `sketchup-clean-geometry`, `sketchup-components`, `sketchup-assembly-structure`,
   `sketchup-camera`, `sketchup-styles`, `sketchup-solid-cleanup`.
3. `read_skill` the contextual skills the job needs — `sketchup-part-boundaries` (framed
   openings/abutment, the no-boolean pattern), `sketchup-scenes` (multi-view render sets),
   `sketchup-rounded-corners` (furniture close to camera).
   Re-run `list_skills` per project; the baseline set can change.

## Examples

### Example 1 — full DWG run (accurate lane)
> "Turn this restaurant DWG into a render to show the client. It's a Perth venue."
1. Intake: confirm AU jurisdiction; import the DWG; clean + scale via the Trimble baseline skills.
2. Model (`modelling-hospitality-plans`): extrude walls to ceiling height, frame the door and
   window openings by construction, tag (`A-WALL-INTR`, `A-DOOR`, `A-GLAZ`, `A-FURN`…),
   validate solids. Checkpoint: show the model, get sign-off.
3. Render-prep (`preparing-render-views`): apply the construction-drawing line style, set the
   hero camera (+ scenes for a set), export a flat PNG; run `validate_export.py`.
4. Render (`rendering-with-nano-banana`): upload the export, iterate materials on `nano_banana_2`,
   then final 4K on `nano_banana_pro` with the Universal Prompt + layout-lock.

### Example 2 — express sketch → render
> "I sketched this rooftop bar on my iPad — quick photoreal render."
1. Intake: raster only → express lane; confirm this is sell-the-idea, geometry follows the sketch.
2. Skip precise modeling. Go to render-prep to set framing/aspect and (optionally) a semantic
   colour pass over the sketch.
3. Render: `nano_banana_2` to iterate, with strong layout-lock phrasing ("look at my lines"),
   then `nano_banana_pro` for the final.

## Troubleshooting / failure modes
- **Wrong stage entered** — user has a model but asked to "render": skip to render-prep, don't re-model.
- **Missing MCP** — Trimble down → cannot model/style/export; stop and report. Higgsfield down →
  fall back to manual Gemini Nano Banana with the same image + prompt (see render skill).
- **Geometry not manifold at hand-off** — bounce back to `modelling-hospitality-plans`
  (`sketchup-solid-cleanup`) before render-prep; a leaky model muddies the line export.
- **Render hallucination** (phantom pools, wrong doors, flattened perspective) — almost always
  a render-prep problem: the export was too clay-like. Return to `preparing-render-views`,
  strengthen the line work, re-export, re-render. See that skill's line-work principle.
- **User wants compliance certainty** — refuse within this suite; explain figures are DEFAULTS
  and point to the v2 `spatial-compliance` path.
