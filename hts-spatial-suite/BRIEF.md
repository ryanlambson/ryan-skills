# BRIEF — hts-spatial-suite

Status: Phase 1 (Brief) + Phase 2 (Research) consolidated. Awaiting outline gate.
Author: Ryan Lambson (HTS / Green Holmes)
Date: 2026-06-09

A suite that turns a 2D hospitality floor plan into a photorealistic, client-facing
visualisation — built to *sell the concept*, not to certify it. The pipeline runs:
plan intake → 3D model in SketchUp (via the Trimble MCP) → clean line-work view →
Nano Banana image-to-image render.

---

## 1. Suite name and component skills

Suite: `hts-spatial-suite` (matches `hts-lla-suite` / `green-holmes-suite` convention).

Naming: verb-ing + noun (Anthropic's current recommendation). RESOLVED at gate.

| Skill | Role |
|---|---|
| `visualising-hospitality-spaces` | Orchestrator / entry point — routes a job through the stages and delegates |
| `modelling-hospitality-plans` | 2D plan → 3D SketchUp model |
| `preparing-render-views` | Style/camera/export tuned for Nano Banana |
| `rendering-with-nano-banana` | Higgsfield handoff + prompt formula |

Note: the orchestrator is the natural user-facing invocation ("visualise this venue") and
delegates to the three workers, the way `lla-gpt` fronts its suite.

## 2. Trigger phrases (per skill, refined at outline)

- "turn this floor plan into a render" → `visualising-hospitality-spaces`
- "model this plan in SketchUp" / "build the 3D from this DWG" → `modelling-hospitality-plans`
- "set up the view for rendering" / "export a clean line view" → `preparing-render-views`
- "render this in Nano Banana" / "make this photorealistic" → `rendering-with-nano-banana`
- "visualise this venue to show the client" → `visualising-hospitality-spaces`

## 3. Negative triggers

- Spec-grade / compliance-certified drawings (this suite is explicitly NOT for that — see v2).
- Liquor-licensing PIA spatial work (that stays in `hts-lla-suite`).
- General SketchUp modeling unrelated to hospitality visualisation.

## 4. Core workflow

1. INTAKE — accept DWG/DXF/SKP (primary) or PDF/sketch (express lane). Import/clean using
   the Trimble MCP's own baseline skills (`clean-geometry`, `solid-cleanup`).
2. MODEL — extrude walls and place openings by CONSTRUCTION (the Trimble MCP has no native
   booleans — no `subtract()`). Apply hospitality tagging + adaptive segment counts.
3. RENDER-PREP — apply a clean construction-drawing / outline style (NOT bare grayscale
   clay), set camera/scenes, export a flat PNG/JPG that locks perspective.
4. RENDER — feed the export to Higgsfield Nano Banana image-to-image (tiered: `nano_banana_2`
   to iterate, `nano_banana_pro` for the final 4K), driven by the Universal Prompt formula.

## 5. Gates and refusals

- Refuses to present a render as a compliance or spec document.
- `modelling-hospitality-plans` refuses boolean-subtraction patterns (unsupported by the MCP).
- `rendering-with-nano-banana` requires an image input (image-to-image); refuses pure text-to-image for
  a known plan, because bare prompts hallucinate geometry.

## 6. Authority hierarchy

1. Trimble SketchUp MCP baseline skills (geometry, camera, styles, solid-cleanup) — win on
   *how to build/style in SketchUp*. We do not rebuild what they provide.
2. This suite's knowledge modules — win on *hospitality domain* (dimensions, materials,
   prompt formula).
3. `knowledge/hospitality-standards.md` jurisdiction block — US (ADA) or AU (NCC / AS 1428.1),
   selected per job. Figures are sane DEFAULTS, not certified compliance values.
4. Research doc (`Training_Claude_for_Hospitality_3D_Modeling.docx`) — conceptual reference
   only; its Ruby/boolean code does NOT run on the Trimble (Python, no-boolean) MCP.

## 7. Output type

A photorealistic render (or set of renders) suitable for client presentation, plus the
intermediate SketchUp model and the clean line-work export.

## 8. Bundled scripts needed

Most actions run through MCP tools (Trimble `build_model`, Higgsfield `generate_image`), so
language-driven, not script-driven. Candidate deterministic helpers (decide at Draft):
- `assemble_prompt.py` — build the Universal Prompt string from the template + job inputs.
- `validate_export.py` — check the export style settings before render (edges/AO/format).

## 9. MCP / tool dependencies

- Trimble SketchUp MCP — REQUIRED (modeling + styling + export).
- Higgsfield MCP — render path (`nano_banana_2` / `nano_banana_pro`, image-to-image, 4K).
  Fallback: manual Gemini Nano Banana if Higgsfield unavailable.
- Google Drive — backup/distribution (used from Cowork).
- Web search — optional, to verify jurisdiction figures at fill-in time.

## 10. Distribution target

Agent Skills open standard, portable. Lives in GitHub. Backbone built here; built out and
backed up to a shared Google Drive folder structure from Cowork.

---

## Research findings folded in (Phase 2)

- Higgsfield exposes three Nano Banana tiers, all image-to-image, up to 4K:
  `nano_banana_2` (fast/iterate), `nano_banana_pro` (final), `nano_banana` (budget).
- Trimble MCP is Python, ships baseline skills covering cleansing/solid-validation/camera/
  styles/scenes — and has NO native boolean operations (openings by construction).
- Video transcripts: bare grayscale views make Nano Banana hallucinate (phantom pools,
  wrong doors, flattened perspective). Clean LINE work / pencil overlay locks vanishing
  points and gets "almost spot-on" geometry. Hence render-prep targets an outline /
  construction-drawing style, plus semantic colour, NOT clay.
- Universal Prompt formula: Material palette · Site/context · Lighting/atmosphere ·
  Narrative — plus layout-lock phrasing ("keep exact layout proportions and relationships",
  "don't guess on materials, look at my lines").

## Deferred to v2 (Ryan's "upgrade later")

- `spatial-compliance` — verified ADA / AS 1428.1 checks for spec-grade output.
- Post-processing: AI inpainting, Topaz-style upscaling, Hadaa/SmartPlanting landscaping.
- Google Veo walkthrough video from render stills (or Higgsfield video models).
- Meshy / Tripo3D: render → editable 3D mesh.
- Medeek extension intermediary for framed engineering geometry (from the MCP videos).
