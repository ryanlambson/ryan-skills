# Video transcript findings (source reference)

Ryan's synthesis of the workflow videos. Operative distillation lives in BRIEF.md; this is
the raw reference for filling figures and examples at Draft.

## 1. AI model building via MCP vs manual modeling + AI render
Two separate workflows across the videos:
- Workflow A (Nano Banana / D5 / Veras): AI does NOT build the model. Designer draws on iPad
  (Procreate/Morfolio) or models in SketchUp, exports a view, and uses Nano Banana strictly
  as a rendering engine — base image/sketch to photoreal/stylized output.
- Workflow B (Claude + SketchUp MCP): the AI builds the model. Claude translates natural
  language into API commands to generate geometry (walls, joists, Medeek assemblies) inside
  SketchUp. In the videos this used Ruby; our Trimble MCP is Python and has no booleans.

## 2. SketchUp export & style settings
- Style/edges: raw simple view — low-res (Dragonfly), basic grayscale, or raw model view.
  D5 can toggle AO + Outline for clean diagrammatic line views.
- Resolution/format: not locked; flat .png/.jpg exported from viewport or iPad.

## 3. Image-to-image conditioning & geometry faithfulness (KEY)
- Strictly image-to-image (+ text). User uploads the sketch/export and tells the AI to look
  at those exact lines and geometry.
- Bare grayscale model view → loose retention; Nano Banana flattens to one-point perspective
  and hallucinates (unwanted infinity pool, wrong doorways).
- Pencil line overlay / hand-drawn sketch over the model perspective → faithfulness jumps;
  line work locks the vanishing points; reproduction becomes "almost spot-on".

## 4. Prompt structure & perspective preservation
Universal Prompt questionnaire — answer four categories every time:
1. Material palette (e.g., "smooth white plaster", "monolithic concrete")
2. Site/landscape context (e.g., "rocky shoreline of a pristine lake in New Hampshire")
3. Lighting/atmosphere (e.g., "blue hour evening light, glowing windows")
4. Narrative/story (e.g., "kids swimming", "family arrived with a dog")
Layout-lock phrasing: "convert my landscape plan into a 60-degree 3D isometric model while
keeping the exact layout proportions and relationships"; "don't guess on the material set,
just look at my lines".

## 5. Additional tools in the chain
- Veras (EvolveLAB): SketchUp plugin embedding Nano Banana Pro; native material overrides,
  annotative sketch edits, render selections.
- Medeek extensions (Foundation/Wall/Truss): in the Claude MCP workflow, Claude feeds natural
  language into Medeek's Ruby API to generate framed, code-accurate engineering geometry.
- Google Veo (AI Kitchen/Labs): downstream video — Nano Banana stills become start/end frames
  for walkthroughs and seasonal transitions.
- Meshy AI / Tripo3D: image-to-3D — a Nano Banana 2D isometric becomes an editable 3D mesh.
- (Topaz and Hadaa were NOT in the source videos.)
