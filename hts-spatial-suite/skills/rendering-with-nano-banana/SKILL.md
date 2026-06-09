---
name: rendering-with-nano-banana
description: >
  Renders a prepared SketchUp line-work view into a photorealistic image via Higgsfield
  Nano Banana, image-to-image. Use when Ryan says "render this in Nano Banana", "make this
  photorealistic", "generate the client visual", or "render this view". Chooses a tier
  (nano_banana_2 to iterate, nano_banana_pro for the final 4K), uploads the export as the
  conditioning image, and drives the Universal Prompt formula with layout-lock phrasing so
  the geometry is preserved. Falls back to manual Gemini Nano Banana if Higgsfield is
  unavailable. Do NOT use for modeling or for spec-grade output.
metadata:
  author: Ryan Lambson (HTS / Green Holmes)
  version: 1.0.0
  standard: agent-skills-1.0
  status: drafted
---

# Spatial Render

Take the line-work export to a sell-the-idea photoreal render while keeping the exact layout
the model defines. **Always image-to-image.** This skill never does pure text-to-image for a
known plan — a bare text prompt hallucinates geometry, which is the whole failure mode the
suite exists to avoid.

## Hard rule: condition on the image, always
For any known plan, the prepared line-work export is the conditioning image. If you have no
image (someone asks for a render with nothing to condition on), stop and route back to
`preparing-render-views` to produce one — do not text-to-image your way to a guessed venue.

## Tier choice
| Tier | Model | Use for |
|---|---|---|
| Iterate | `nano_banana_2` | Fast, cheap iteration with the client — try materials, lighting, framing |
| Final | `nano_banana_pro` | The hero deliverable: high fidelity, up to 4K |
| Budget | `nano_banana` | Cost-sensitive bulk passes |

Work the look on `nano_banana_2`, lock the winning prompt, then re-run it **unchanged except
model + resolution** on `nano_banana_pro` for the 4K final.

## Image-to-image handoff (Higgsfield)
1. Confirm the export PASSed `preparing-render-views`/`validate_export.py`.
2. Upload it as the conditioning image (Higgsfield `media_upload` → `media_confirm`).
3. Call `generate_image` with the chosen Nano Banana model and the uploaded image as the
   reference/input image, plus the assembled prompt.
4. Review with the user; iterate (see hygiene below); promote the winner to `nano_banana_pro`.

If unsure of a model's exact parameter names, check `models_explore` for the Nano Banana
entry before the first call.

**Fallback — manual Gemini Nano Banana** (if Higgsfield is unavailable): open Gemini's Nano
Banana, upload the *same* export as the image, paste the *same* assembled prompt. Same
image-to-image discipline; only the delivery channel changes.

## The Universal Prompt formula
Answer four anchors every time, then append the layout-lock. Full scaffold and three worked
examples live in `knowledge/materials-semantic-template.md`.

1. **Material palette** — exact finishes ("polished herringbone oak", "honed travertine", "brushed brass").
2. **Site / context** — location and surroundings ("rooftop bar overlooking the Swan River").
3. **Lighting / atmosphere** — time and mood ("blue-hour, warm 2700K festoon lights").
4. **Narrative / story** — how the space is used ("guests at the bar, relaxed Friday crowd").

Layout-lock (verbatim, always, for a known plan):
> "Preserve the exact spatial layout, wall boundaries, and camera perspective of the reference
> image; don't guess on the material set, look at my lines."

For layout-critical scenes, name the elements to lock (e.g. "table positions", "bar and railing
positions"). Use the **plan-to-iso** variant when converting a flat plan: "Convert my plan into
a 60-degree 3D isometric view while keeping the exact layout proportions and relationships."

**Assemble it deterministically** with `scripts/assemble_prompt.py` — pass the five slots
(`venue_type`, `materials`, `context`, `lighting`, `narrative`) and a `--tier`; it emits the
model name and the full prompt with the layout-lock appended verbatim, so the wording never drifts:
```
python scripts/assemble_prompt.py \
  --venue-type "full-service restaurant dining room" \
  --materials "herringbone oak, honed travertine feature wall, walnut joinery, brass pendants" \
  --context "a lively neighbourhood bistro on a brick corner" \
  --lighting "warm early-evening light, glowing filament pendants" \
  --narrative "diners mid-meal, servers moving through" \
  --tier iterate --extra-lock "table positions"
```

## Iteration hygiene
- **One variable at a time** — change material *or* lighting *or* framing per pass, never several.
  Otherwise you can't tell what helped.
- **Bad material memory** — if a material renders wrong repeatedly across iterations, start a
  fresh thread (clears the model's running memory) or fold the material detail explicitly into
  the main prompt's palette.
- **Promote, don't re-write** — the `nano_banana_pro` final reuses the exact winning
  `nano_banana_2` prompt; only model + resolution change.

## Examples + troubleshooting

### Example 1 — iterate materials on nano_banana_2
Upload `hero.png`; assemble the bistro prompt above on `--tier iterate`; render; the client wants
walnut not oak → change *only* the palette line; re-render. Lock the winner.

### Example 2 — final 4K on nano_banana_pro
Take the winning prompt verbatim, switch `--tier pro`, render `nano_banana_pro` at 4K. Deliver.

### Troubleshooting
- **Hallucinated geometry** (phantom pool, wrong door, flattened perspective) — the conditioning
  image was too clay-like. Go back to `preparing-render-views`, strengthen the line work / add a
  line overlay, re-export, re-render. Strengthen the layout-lock phrasing and name the elements
  to lock.
- **Materials keep coming back wrong** — fresh thread or explicit palette (see hygiene).
- **Layout drifts on a plan-to-iso** — use the plan-to-iso layout-lock variant and keep proportions explicit.
- **No image to condition on** — you're not ready to render; return to render-prep. Never
  text-to-image a known plan.
