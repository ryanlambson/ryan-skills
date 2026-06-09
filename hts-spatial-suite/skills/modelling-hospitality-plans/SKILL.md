---
name: modelling-hospitality-plans
description: >
  Builds a 3D SketchUp model of a hospitality space from a 2D floor plan, via the Trimble
  SketchUp MCP. Use when Ryan says "model this plan in SketchUp", "build the 3D from this
  DWG/DXF", "extrude these walls", or "turn this floor plan into a model". Imports the plan,
  uses the Trimble baseline skills for cleansing and solid validation, extrudes walls, and
  places doors and windows by CONSTRUCTION (the Trimble MCP has no native boolean
  operations, so no subtract()). Applies a hospitality tag structure and adaptive segment
  counts for curves. Do NOT use for rendering (see rendering-with-nano-banana) or for spec-grade
  compliance modeling.
metadata:
  author: Ryan Lambson (HTS / Green Holmes)
  version: 1.0.0
  standard: agent-skills-1.0
  status: drafted
---

# Spatial Plan-to-Model

Convert a cleaned 2D hospitality plan into a tagged, watertight 3D model ready for
render-prep. Dimensions come from `knowledge/hospitality-standards.md` as **DEFAULTS** — sane
starting values to make the model read right, never presented as certified compliance.

## Input formats and the two lanes
- **Accurate-model lane** — vector input: **DWG / DXF / SKP**. Real geometry and scale, so the
  model is dimensionally trustworthy. This is the lane for client work that has CAD behind it.
- **Express lane** — raster input: **PDF render, photo, iPad sketch**. No reliable scale; do
  NOT pretend to precise-model it. Hand straight to `preparing-render-views` / `rendering-with-nano-banana`
  and tell the user the geometry will only be as accurate as the sketch.
- Mixed input: trace the vector where you have it; treat the rest as express.

Confirm the **jurisdiction** (US/AU, default AU) at the start — it selects the default
clearances, door widths, and room areas you'll model to.

## Construction rules (critical)

### 1. NO booleans — frame every opening by construction
The Trimble MCP has **no native boolean operations** — there is no `subtract()`, no cutter
solids, no `intersect`. Confirmed by the baseline `sketchup-part-boundaries` skill ("the
connector has no native boolean operations, so overlap is resolved by construction").

Build openings the way a framer does — as the *gaps left between solid pieces*:
- A wall with a doorway = build it as separate wall segments that stop at the jambs (a piece
  each side of the opening, plus a header/lintel piece above), leaving the door gap empty.
- A window = sill piece below, head piece above, jamb pieces each side, glass as its own thin
  group in the hole (tag `A-GLAZ`).
- Never model a full wall and try to cut a hole in it. There is no cut.

Defer to `sketchup-part-boundaries` (and its `references/stud-wall-framing.md`) for the exact
abutment maths on corners, T-intersections, and rough openings — do not reinvent it here.

### 2. Ground-plane normal
Reverse any face whose normal points **down** before push-pull, or the extrusion goes the wrong
way and you get inverted, non-manifold solids. Verify normals after `clean_geometry`.

### 3. Active-context nesting
Put geometry into a **group or component**, never loose at the model root. This keeps each room
element selectable and lets the baseline skills validate it in isolation.

### 4. Hospitality tag structure (AIA-style)
Tag the **groups/components**, leave raw geometry **Untagged** (mirrors `sketchup-assembly-structure`):
`A-WALL-INTR`, `A-WALL-EXTR`, `A-FLOR`, `A-DOOR`, `A-GLAZ`, `A-FURN`, `A-FFE`, `A-CLNG`.
Full list in `knowledge/hospitality-standards.md`.

### 5. Adaptive segment count
Scale curve segment count to radius — enough that a curved bar or banquette reads as smooth at
the hero camera, not so many that the model bloats. See `sketchup-rounded-corners` for the
performance-vs-smoothness budget when furniture sits close to camera.

## Lean-on map (do not rebuild)
| Need | Trimble baseline skill |
|---|---|
| Clean extrudable geometry, coplanar-edge decisions, `clean_geometry` passes | `sketchup-clean-geometry` |
| Watertight / solid validation before hand-off | `sketchup-solid-cleanup` |
| Framed openings, abutment, stud-wall rough openings (the no-boolean pattern) | `sketchup-part-boundaries` |
| Repeated items — chairs, stools, pickets, windows, tables | `sketchup-components` |
| Selectable sub-assemblies (a bar, a banquette run, a bathroom pod) | `sketchup-assembly-structure` |
| Rounded/bullnose edges on close-camera furniture | `sketchup-rounded-corners` |

This suite owns only the *hospitality* layer on top: which defaults to use, how to tag, and
that openings are framed not cut.

## Worked example — import DWG → walls → framed doorway (AU)
1. Pre-flight: `list_skills`; `read_skill` all baseline + `sketchup-part-boundaries`.
2. Import the DWG; clean and confirm scale (a 3000 mm wall should read 3000 mm). Reverse any
   down-facing floor faces.
3. Floor: trace the slab outline into a group, push-pull up to slab thickness, tag `A-FLOR`.
4. Walls: trace each wall run **as segments that stop at every opening**. For a doorway, default
   the clear opening to **850 mm** (AU min) and frame: left jamb piece, right jamb piece, header
   above to ceiling height (default ~2700 mm). Push-pull each to wall height. Tag `A-WALL-INTR`.
5. Door + glazing: thin group in each gap, tag `A-DOOR` / `A-GLAZ`.
6. Group the room as a selectable assembly; run `sketchup-solid-cleanup` until every
   geometry-bearing group is a closed solid.
7. Hand off the tagged, watertight model to `preparing-render-views`.

## Troubleshooting
- **Non-manifold groups** — orphan arc-curve edges (common on rounded/lofted shapes). Run the
  `sketchup-clean-geometry` four-pass, then `sketchup-solid-cleanup`. Don't proceed to render
  with leaky solids — they smear the line export.
- **Inverted extrusion** — face normal pointed down before push-pull; reverse and redo.
- **Wrong import scale** — DWG units mismatch; re-import with the right unit and re-verify a
  known dimension before modeling anything else.
- **Openings not "closing"** — you tried to cut a hole. Stop: there are no booleans. Rebuild the
  wall as framed segments around the gap (rule 1).
- **Raster input only** — you're in the wrong lane; this is express, not precise modeling.
  Route to render-prep/render and set expectations on geometric accuracy.
