---
name: preparing-render-views
description: >
  Prepares a SketchUp model for Nano Banana rendering by producing a clean line-work view,
  not a bare clay render. Use when Ryan says "set up the view for rendering", "export a
  clean line view", "get this ready for Nano Banana", or "prep the render view". Applies a
  construction-drawing / outline style, ambient occlusion for grounding, alpha-plane fixes,
  a framed camera, and optional multi-scene views, then exports a flat PNG/JPG that locks
  the perspective. Leans on the Trimble baseline skills sketchup-styles, sketchup-camera,
  and sketchup-scenes. Do NOT use for the modeling step or the render call itself.
metadata:
  author: Ryan Lambson (HTS / Green Holmes)
  version: 1.0.0
  standard: agent-skills-1.0
  status: drafted
---

# Spatial Render-Prep

Turn a finished model into the **line-work export** that makes Nano Banana faithful to the
real geometry. This stage is the single biggest lever on render quality: get the line work
right and the render "almost spot-on"; ship clay and the render hallucinates.

## The line-work principle (why this stage exists)
From the workflow videos (`source/video-transcript-answers.md`): a **bare grayscale clay**
view makes Nano Banana hallucinate — it flattens to one-point perspective and invents geometry
(phantom infinity pools, wrong doorways). A **clean outline / construction-drawing** view does
the opposite: the crisp edges **lock the vanishing points and the structure**, so reproduction
jumps to faithful.

So the target is: **clean outline edges + semantic colour**, NOT
- bare grayscale clay (no edges to lock perspective), and NOT
- a dense black wireframe (too noisy — the engine can't read the surfaces).

Semantic colour comes from `knowledge/materials-semantic-template.md`: a flat base colour per
surface that tells the engine what each surface *is*, which the render then realises.

## Style / edge / AO / alpha settings
Apply via the Trimble `sketchup-styles` baseline skill — it owns Styles, RenderingOptions and
ShadowInfo. Ask it for the **"construction drawing look"** preset (it lists this as an explicit
preset trigger), then tune:
- **Edges**: crisp outline ON; profiles light, not heavy. Prefer colour-by-material edges over
  dense black. Avoid extension/endpoint jitter and sketchy edge styles (they read as noise).
- **Faces**: shaded-with-textures using the flat semantic base colours (so each surface carries
  its material cue), background a plain neutral.
- **Ambient occlusion**: ON — it grounds furniture and gives the engine contact shadows so
  objects don't float.
- **Alpha / transparent planes**: turn AO and shadow-casting OFF on glazing and other
  transparent groups, or they cast phantom shadows and confuse the export.
- Keep shadows soft/subtle — enough to ground, not so hard they bake dramatic darks the render
  then has to fight.

## Camera and multi-scene views
- Frame a **hero camera** with `sketchup-camera` (it does the bounding-box eye/target maths;
  use the *interior* FOV profile for rooms). One strong, honest perspective beats a wide
  distorted one.
- For a render *set* (multiple angles / a walk-around), add scenes with `sketchup-scenes`
  — mind its `add_layer = HIDE` gotcha and set a per-scene camera for each. Each scene exports
  as its own line-work image and renders independently.

## Export settings
- Format: **flat PNG** (or JPG) from the viewport — a single raster, no transparency in the
  final file. PNG preferred for crisp edges.
- Resolution / aspect: match the render tier you're feeding. Long edge ≥ **2048 px** for a
  `nano_banana_pro` final, ≥ **1024 px** for `nano_banana_2` iteration. Pick the aspect now
  (e.g. 16:9 hero) and keep it consistent through render.
- **Validate before hand-off**: run `scripts/validate_export.py <export.png> --tier pro --aspect 16:9`.
  It checks format, resolution, aspect, an opaque (non-alpha) background, and that the image
  actually carries line content rather than reading as blank or bare clay. Don't pass a file to
  the render skill until `validate_export.py` says PASS.

## Example + troubleshooting

### Example — hero line view for a restaurant
1. Apply `sketchup-styles` "construction drawing look"; set crisp outline edges + flat semantic
   colours; AO on; AO/shadows off on the window glazing.
2. `sketchup-camera` interior FOV, framed on the bar and banquette run.
3. Export a 2400×1350 (16:9) PNG.
4. `python scripts/validate_export.py hero.png --tier pro --aspect 16:9` → PASS.
5. Hand the PNG to `rendering-with-nano-banana`.

### Troubleshooting
- **Muddy / noisy edges** — edge style too heavy or sketchy. Drop profile weight, switch off
  extensions/endpoints, prefer colour-by-material edges. Re-export; `validate_export.py`
  `line-content` should still PASS but the image should read clean.
- **Floating furniture** — AO off or too weak. Turn AO on (grounds contact). Re-export.
- **Reads as clay (validate_export FAIL on line-content)** — not enough edge structure. Increase
  outline edges / reduce face shading toward the line-work look, re-export.
- **Phantom shadows on glass** — AO/shadow-casting still on a transparent plane; disable per the
  alpha rule above.
- **Aspect mismatch downstream** — set the export aspect to the render aspect *here*; don't let
  the render crop or stretch.
