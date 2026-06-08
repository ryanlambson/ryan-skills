---
name: green-holmes-canva
description: >
  Green Holmes Canva workflow. Use this skill whenever Ryan asks to build a
  Canva design, populate a brand template, magic-resize a carousel for another
  platform, run a brand audit on social content, or apply the Claude+Canva
  playbook to Green Holmes social media. This skill provides the design
  execution layer that complements green-holmes-social (copy strategy) and
  green-holmes-waterfall (file workflow).
  Triggers: "magic resize", "canva", "resize for facebook", "resize for
  linkedin", "resize for tiktok", "create story from carousel", "brand audit",
  "use this template", "populate brand template", "canva workflow", "canva
  resize", "platform variants", "carousel to facebook ad", "carousel to
  linkedin", "design for [platform]".
---

# Green Holmes Canva Workflow

## Purpose

Turn one master 1080×1350 Instagram carousel into 10+ platform-specific
derivatives via Canva's resize and editing tools. Codify the working pattern
from the Day 1 (2.5 percent salt) brand-template build so every future
carousel ships faster, on brand, across all platforms.

## Dependencies

Always load `green-holmes-voice` alongside this skill. For copy structure,
also load `green-holmes-social` or `green-holmes-waterfall` depending on
the request shape.

## Core philosophy

Canva is the graphic designer. Claude is the creative strategist. Ryan is
the MVP — taste, context, quality control. Nothing ships without Ryan's
judgement.

Three principles lifted from the Claude+Canva playbook video and adapted
to Green Holmes:

1. **Master in the source-of-truth format, derive everything else.** The
   master design lives at 1080×1350 (Instagram carousel native). All other
   platforms are derivatives produced via resize and minor edits, not from
   scratch.

2. **Brand template before resize.** Save the master as a Canva Brand
   Template the first time you build a content type. Future builds start
   from the template. Layout fidelity stays consistent across the series.

3. **Debrief every published post.** After each carousel ships, feed the
   final exported PNGs and what worked back to Claude. Memory accumulates.
   Every brief gets sharper than the last.

## Reference files

Read these in order before resizing or building any social content:

1. `MAGIC_RESIZE_RECIPES.md` — Per-platform resize recipes. The primary
   working file. Covers Instagram Story, Facebook organic, Facebook ad,
   LinkedIn feed, LinkedIn carousel, TikTok carousel, X/Twitter post,
   Pinterest pin. Includes Day 1 carousel application table.

2. `CANVA_PLAYBOOK.md` *(planned)* — The seven plays from the Claude+Canva
   video adapted for Green Holmes. Path A (manual build) vs Path B
   (template search). When to use which.

3. `BRAND_AUDIT.md` *(planned)* — The 30-question Social Media Design
   Audit with current Green Holmes scoring and prioritised gaps.

4. `PLATFORM_SPECS.md` *(planned)* — Distilled platform specifications
   reference. Aspect ratios, safe zones, file types, character limits.

5. `DEBRIEF_TEMPLATE.md` *(planned)* — Post-publish debrief template
   to feed back to Claude after each post ships. Closes the learning loop.

## Workflow at a glance

For any social content request:

1. Identify the master format (default: Instagram carousel 1080×1350).
2. Build or select brand template via Canva MCP. If no template exists,
   ask Ryan to save one before proceeding (manual step in Canva UI).
3. Populate with content from green-holmes-content (Field Note source)
   or direct copy.
4. Run brand-qa subagent on the final design before any resize.
5. Resize for derivative platforms per `MAGIC_RESIZE_RECIPES.md`.
6. After publishing, run the debrief and update the relevant memory file.

## Canva MCP capabilities (verified working)

- `search-folders`, `list-folder-items`, `list-brand-kits`
- `start-editing-transaction`, `perform-editing-operations`
  (`replace_text`, `find_and_replace_text`, `format_text`,
  `position_element`, `resize_element`)
- `commit-editing-transaction`, `cancel-editing-transaction`
- `move-item-to-folder`
- `resize-design` (custom width/height — see recipes for limitations)
- `export-design` (PNG, JPG, PDF, MP4)
- `get-design-thumbnail` (per-page preview during edit)

## Canva MCP capabilities NOT available

- `search-brand-templates` (referenced in tool docs but not exposed in this
  connector — confirmed 28 April 2026)
- Direct Magic Resize via API. The `resize-design` tool changes canvas
  dimensions but does not auto-rearrange elements. For complex aspect
  changes (4:5 → 16:9), elements must be repositioned manually via
  `position_element` after resize, OR resize via Canva UI's Magic Resize
  before editing further. See `MAGIC_RESIZE_RECIPES.md`.

## Brand kit and folder

| Asset | ID |
|---|---|
| Brand kit "Green Holmes" | `kAG-fhL4weM` |
| GH Socials folder | `FAHGOnAXddA` |
| Day 1 carousel master | `DAHIMr9Z7eg` (filed in GH Socials) |
| Day 1 brand template source | `EAHIMstpEOg` |

## Hard rules for every Canva output

Off-white `#F5F1ED` background only. Soft black `#2C2C2C` type only. No
colour anywhere except in photography. No decorative shapes or icons. No
gradients. No drop shadows. Sentence case. Australian English. Sentence
case. No em or en dashes — only commas, full stops, or rephrase. Mechanism
first, never benefit-first.

When Canva's AI tools (Magic Media, Magic Write) suggest content that
violates these, override or skip. Hero imagery is FLUX via fal.ai by
default until proven otherwise — see `MAGIC_RESIZE_RECIPES.md` final
section.
