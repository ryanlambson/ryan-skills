# HANDOFF — hts-spatial-suite (read this first)

This package is the backbone of a skill suite. A previous session completed the Brief,
Research, Outline, naming, and skeletons. Your job is Phase 4 (Draft) → QA → wrap as a
plugin → commit to the connected GitHub. **Do not re-open settled decisions** — they are
below.

---

## Paste this into the new Cowork session to start

> We're continuing a skill-suite build, `hts-spatial-suite`. I've uploaded the handoff
> package. Read `HANDOFF.md`, then `BRIEF.md` and `OUTLINE.md` — they hold every locked
> decision, so don't re-open settled scope.
>
> The suite turns a 2D hospitality floor plan into a sell-the-idea photoreal render via the
> Trimble SketchUp MCP (build the model) and Higgsfield Nano Banana (render). Four skills,
> verb-ing named, already scaffolded as skeletons.
>
> Do this in order:
> 1. Invoke the `skill-builder` skill. Run Phase 4 (Draft) then the QA gate on each of the
>    four SKILL.md files, following the agreed OUTLINE and honouring the HARD CONSTRAINTS in
>    HANDOFF.md. Flag any deviation from the outline.
> 2. Fill the `[VERIFY]` figures in `knowledge/hospitality-standards.md` against primary
>    sources (US ADA + AU NCC / AS 1428.1). Add 2-3 worked prompt examples to
>    `knowledge/materials-semantic-template.md`. Decide on the two candidate scripts.
> 3. Run a live end-to-end smoke test: build a small hospitality room via the Trimble MCP
>    (load its baseline skills first), apply a clean line-work style, export a flat image,
>    and render image-to-image through Higgsfield `nano_banana_2` then `nano_banana_pro`.
>    Fold what works back into the skills.
> 4. Wrap the suite as a plugin with `create-cowork-plugin` (manifest + `skills/` layout),
>    then commit to the connected GitHub repo.
>
> Confirm these connectors/skills are active first: Trimble SketchUp MCP, Higgsfield MCP,
> GitHub, `skill-builder`, `create-cowork-plugin` (and Google Drive only if used for assets).

---

## Locked decisions (do not re-litigate)
- Output = client visualisations to SELL the concept, not spec/compliance drawings.
- Markets = both US and AU; jurisdiction is a swappable knowledge block.
- Modeling = Trimble SketchUp MCP (Python). NO native booleans — openings by construction.
- Render = Higgsfield Nano Banana, image-to-image, tiered nano_banana_2 then nano_banana_pro
  (4K). Manual Gemini is the fallback only.
- Inputs = DWG/DXF/SKP primary (accurate lane); sketch/viewport = express lane.
- Naming = verb-ing + noun (Anthropic recommendation), AU spelling.
- Shared knowledge = single copy at suite root `knowledge/` (suite installs as a unit).
- v1 scope = full pipeline. Compliance-check + post-processing (inpaint/upscale/landscaping/
  Veo video/Meshy 3D/Medeek) = v2.

## Hard constraints (QA must enforce)
1. No boolean-subtraction code anywhere in `modelling-hospitality-plans` — frame openings.
2. `rendering-with-nano-banana` always conditions on an image; never pure text-to-image for a
   known plan.
3. Render-prep targets clean line-work / construction-drawing style, NOT bare grayscale clay
   (bare clay makes Nano Banana hallucinate; line work locks perspective).
4. Every dimensional figure is a DEFAULT for modeling, never presented as certified compliance.
5. Trimble baseline skills win on SketchUp mechanics — do not rebuild cleansing/camera/styles.

## What's built (backbone)
- `BRIEF.md`, `OUTLINE.md` — contract + structure.
- Four skeleton skills: `visualising-hospitality-spaces` (orchestrator),
  `modelling-hospitality-plans`, `preparing-render-views`, `rendering-with-nano-banana`.
- `knowledge/hospitality-standards.md`, `knowledge/materials-semantic-template.md` (starters).
- `README.md` (repo-level), `source/` (research report + video findings).

## What's left (your work)
- Draft all four SKILL.md bodies from the stubs; pass QA.
- Fill `[VERIFY]` figures; add worked prompt examples; decide scripts (`assemble_prompt.py`,
  `validate_export.py`).
- Smoke test the live chain; correct skills from real results.
- Plugin wrap + GitHub commit. Move build artifacts (BRIEF/OUTLINE/HANDOFF/source) OUTSIDE the
  shipped plugin boundary when wrapping.

## Reference
- `source/research-report.docx` — conceptual only; its Ruby/boolean code does NOT run on the
  Python, no-boolean Trimble MCP.
- `source/video-transcript-answers.md` — the render-faithfulness and Universal Prompt findings.
