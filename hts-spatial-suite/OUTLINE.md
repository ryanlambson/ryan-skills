# OUTLINE — hts-spatial-suite

Phase 3 artifact. Approve this and the next step is Phase 4 Draft + QA (in Cowork).

## Folder structure (GitHub-ready)

```
hts-spatial-suite/
├── README.md                         # repo-level only (NEVER inside a skill folder)
├── BRIEF.md                          # the contract
├── OUTLINE.md                        # this file
├── visualising-hospitality-spaces/
│   └── SKILL.md                      # orchestrator (master)
├── modelling-hospitality-plans/
│   └── SKILL.md
├── preparing-render-views/
│   └── SKILL.md
├── rendering-with-nano-banana/
│   └── SKILL.md
└── knowledge/                        # shared across skills (see open question below)
    ├── hospitality-standards.md
    └── materials-semantic-template.md
```

OPEN STRUCTURAL QUESTION (for gate): the Agent Skills standard wants each skill
self-contained, so cross-skill references aren't strictly portable. Options:
(a) keep shared `knowledge/` at suite root and install the suite as a unit (simplest), or
(b) copy each knowledge module into the `references/` of the skills that use it (portable
but duplicated). Recommendation: (a) for now, since the suite installs together.

## Per-skill section structure

### visualising-hospitality-spaces (orchestrator)
1. One-paragraph purpose
2. What this system is NOT
3. Trigger phrases → stage routing
4. Authority hierarchy (Trimble baseline skills first)
5. The four-stage pipeline (intake → model → render-prep → render) with hand-offs
6. Pre-flight: load Trimble baseline skills via `list_skills` / `read_skill`
7. Examples (2 worked: full DWG run; express sketch→render)
8. Troubleshooting / failure modes

### modelling-hospitality-plans
1. Purpose
2. Input formats + the two lanes (accurate-model vs express)
3. Construction rules: openings by framing, NO booleans; hospitality tagging; adaptive segments
4. Lean-on map: which Trimble baseline skills do what (don't rebuild)
5. Worked example: import DWG → walls → framed doorway
6. Troubleshooting (non-manifold, ground-plane normal, scale)

### preparing-render-views
1. Purpose
2. The line-work principle (clean outline, NOT clay; why)
3. Style/edge/AO/alpha settings + the Trimble style preset to use
4. Camera + multi-scene views for a render set
5. Export settings (format, flat image)
6. Example + troubleshooting (muddy edges, floating furniture)

### rendering-with-nano-banana
1. Purpose
2. Tier choice: nano_banana_2 (iterate) vs nano_banana_pro (final 4K)
3. Image-to-image handoff via Higgsfield (+ manual Gemini fallback)
4. The Universal Prompt formula + layout-lock phrasing
5. Iteration hygiene (fresh thread on bad material memory; one variable at a time)
6. Examples (2) + troubleshooting (hallucinated geometry → add line overlay)

## Shared knowledge modules
- `hospitality-standards.md` — jurisdiction-swappable room/clearance/dining defaults (US + AU).
- `materials-semantic-template.md` — texture/colour/material template doubling as the
  Nano Banana semantic map + the Universal Prompt scaffold.

## Bundled scripts (decide at Draft)
- `assemble_prompt.py` — Universal Prompt assembler.
- `validate_export.py` — pre-render export-setting check.

## QA criteria this suite is tested against
- Standard skill-builder structural + content + portability checks.
- Plus: no boolean-subtraction code anywhere in `modelling-hospitality-plans`.
- Plus: `rendering-with-nano-banana` never instructs pure text-to-image for a known plan.
- Plus: every dimensional figure tagged as DEFAULT, never as certified compliance.
