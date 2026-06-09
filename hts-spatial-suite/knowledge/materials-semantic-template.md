# Materials & Semantic Template (shared knowledge)

Two jobs in one file:
1. A SketchUp material/colour palette applied before export, acting as a SEMANTIC MAP that
   tells Nano Banana what each surface is.
2. The Universal Prompt scaffold that drives `rendering-with-nano-banana`.

> STATUS: starter. Expand the palette and add worked prompt examples at Draft.

---

## 1. Semantic colour → material map

Apply a simple, flat base colour/low-res texture per surface in SketchUp. The colour is a
tag the render engine reads; it then renders the real material. Keep it readable, not clay.

| Surface role | SketchUp base cue | Renders as (prompt support) |
|---|---|---|
| Timber floor | warm brown, subtle grain | herringbone / plank oak, satin finish |
| Stone/feature wall | mid grey, slight texture | honed stone or microcement |
| Glazing | pale blue, transparent | clear glass, accurate reflections |
| Joinery / cabinetry | distinct mid tone, colour-by-material edges | matte timber veneer, fine reveals |
| Soft furnishing | muted accent colour | velvet / boucle upholstery |
| Metal trim | cool grey | brushed brass or black steel |

Principle from the videos: don't make the engine guess — the base colour plus the prompt's
material palette together lock the look.

---

## 2. Universal Prompt scaffold

Anchor the AI by answering four categories every time, then add the layout lock.

1. MATERIAL PALETTE — exact finishes ("smooth white plaster", "polished herringbone oak",
   "brushed brass", "grey velvet").
2. SITE / CONTEXT — location and surroundings ("rooftop bar overlooking the Swan River").
3. LIGHTING / ATMOSPHERE — time/mood ("golden-hour afternoon, warm 2800K accent lamps").
4. NARRATIVE / STORY — how the space is used ("guests at the bar, soft evening buzz").

Layout-lock lines (always include for a known plan):
- "Preserve the exact spatial layout, wall boundaries, and camera perspective of the
  reference image."
- "Don't guess on the material set — look at my lines."
- (Plan-to-iso variant) "Convert my plan into a 60-degree 3D isometric view while keeping
  the exact layout proportions and relationships."

### Fill-in template
> A professional interior photograph of a [VENUE TYPE]. [MATERIAL PALETTE]. [SITE/CONTEXT].
> [LIGHTING/ATMOSPHERE]. [NARRATIVE]. Render in 4K, photorealistic. Preserve the exact
> spatial layout, wall boundaries, and camera perspective of the reference image; don't
> guess on materials, look at my lines.

The five bracket slots map one-to-one onto the fields `assemble_prompt.py` takes
(`venue_type`, `materials`, `context`, `lighting`, `narrative`), so a worked example below
is also a literal test case for that script.

---

## 3. Worked examples

Each example pairs (a) the SketchUp semantic base colours applied before export, with (b) the
finished Universal Prompt string. Use as templates — swap the bracket content, keep the
layout-lock sentence verbatim.

### Example A — boutique hotel guest suite (AU, midscale ~30 m²)
Semantic base: floor warm brown (plank), feature wall behind bed mid-grey, joinery distinct
walnut tone, glazing pale-blue transparent, bedding/soft furnishings muted sage, trim cool grey.

> A professional interior photograph of a boutique hotel king guest suite. Polished
> wide-plank European oak floor, smooth warm-white plaster walls, a fluted walnut headboard
> wall, brushed-brass fixtures, sage-green velvet bench and linen bedding, floor-to-ceiling
> clear glazing with fine black-steel frames. Calm urban hotel room overlooking a leafy
> Perth street. Soft golden-hour afternoon light, warm 2800K bedside lamps just switched on.
> A turned-down bed and a guest's coat over the bench — quiet end-of-day arrival. Render in
> 4K, photorealistic. Preserve the exact spatial layout, wall boundaries, and camera
> perspective of the reference image; don't guess on the material set, look at my lines.

### Example B — full-service restaurant dining room (US, casual-fine)
Semantic base: floor warm brown (herringbone), stone feature wall mid-grey textured, banquette
muted terracotta, joinery mid walnut, metal trim cool grey, glazing pale blue.

> A professional interior photograph of a full-service restaurant dining room. Herringbone
> oak floor, honed travertine feature wall, matte walnut joinery with fine reveals, terracotta
> boucle banquettes, black-steel and brass pendant lights, clear glazing to the street. A
> lively neighbourhood bistro on a brick-lined corner. Warm early-evening light, glowing
> filament pendants, candle-lit tables. Diners mid-meal, servers moving through, soft ambient
> buzz. Render in 4K, photorealistic. Preserve the exact spatial layout, table positions, wall
> boundaries, and camera perspective of the reference image; don't guess on the material set,
> look at my lines.

### Example C — rooftop bar (AU, hero exterior-edge view)
Semantic base: deck warm grey-brown timber, bar front mid stone, planters green, metal trim
black, glazing/balustrade pale-blue transparent.

> A professional photograph of a rooftop cocktail bar at dusk. Spotted-gum timber decking,
> a microcement bar front, brushed-brass bar rail, black-steel pergola, lush green planters,
> frameless glass balustrade. A rooftop terrace overlooking the Swan River and Perth city
> skyline. Blue-hour evening, warm 2700K festoon lights and glowing back-bar, city lights
> beginning to twinkle. Guests at the bar with cocktails, relaxed Friday-evening crowd.
> Render in 4K, photorealistic. Preserve the exact spatial layout, bar and railing positions,
> and camera perspective of the reference image; don't guess on the material set, look at my
> lines.

> Iteration note: these are `nano_banana_2` iteration prompts. For the final, re-run the
> winning prompt on `nano_banana_pro` at 4K, changing nothing but the model and resolution
> (one variable at a time — see `rendering-with-nano-banana`).
