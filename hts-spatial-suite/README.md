# hts-spatial-suite

Turns 2D hospitality floor plans into photorealistic, client-facing visualisations —
built to sell the concept, not to certify it.

Pipeline: **plan intake → 3D model (Trimble SketchUp MCP) → clean line-work view →
Nano Banana image-to-image render (Higgsfield)**.

## Skills
- `visualising-hospitality-spaces` — orchestrator; routes a job through the four stages.
- `modelling-hospitality-plans` — 2D plan → 3D SketchUp model (construction-based, no booleans).
- `preparing-render-views` — clean outline style, camera, export tuned for Nano Banana.
- `rendering-with-nano-banana` — Higgsfield Nano Banana handoff + Universal Prompt formula.

## Shared knowledge
- `knowledge/hospitality-standards.md` — jurisdiction-swappable defaults (US ADA / AU NCC + AS 1428.1).
- `knowledge/materials-semantic-template.md` — material/colour template + prompt scaffold.

## Status
Backbone (Brief + Outline + skeletons). Phase 4 Draft + QA pending — to be completed in
Cowork, then backed up to the shared Google Drive `SKILLS/` structure.

## Dependencies
Trimble SketchUp MCP (required) · Higgsfield MCP (render; manual Gemini fallback) ·
Google Drive (backup) · web search (optional, jurisdiction figure verification).

## Authority
Trimble baseline skills win on SketchUp mechanics; this suite's knowledge wins on
hospitality domain. The source research doc is conceptual only — its Ruby/boolean code
does not run on the Python, no-boolean Trimble MCP.
