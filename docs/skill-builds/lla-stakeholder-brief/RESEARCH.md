# RESEARCH — lla-stakeholder-brief

Phase 2 of 4. Status: awaiting "research clear".

## Tier 1 — Internal knowledge

Structural decisions drafted from the known standard: SKILL.md with YAML frontmatter
(name, description), optional scripts/ references/ assets/, body under 500 lines,
progressive disclosure (templates and long examples pushed to references/). One bundled
deterministic script (conventions check). No Claude-only features required.

## Tier 2 — Reference library (ryan-skills repo, hts-lla-suite)

Google Drive SKILLS library not reachable this session (Drive connector not authorised);
substituted the live suite in this repo, which is the more current source. Patterns
extracted from `lla-citation-checker` and peers, to be reproduced:

- Frontmatter: folded multi-line description embedding trigger phrases AND negative
  triggers; `license: Proprietary. HTS internal use only.`; `metadata:` block with
  author / version / role / jurisdiction / set_skill.
- Body opens with the set-skill statement and the **Authoring Entity Lock** block
  (HTS entity + Applecross address).
- "Position in the pipeline" diagram showing where the skill sits relative to the
  drafters and the two-stage pre-delivery gate.
- Numbered sections, hard gates stated as refusals, worked examples, troubleshooting.
- Jurisdiction-agnostic framing (WA now, NSW-ready), consistent with suite direction.

Pipeline decision arising: brief drafts produced by this skill route through
`lla-writing-conventions` (mandatory, in-body) and the bundled conventions check script.
Full Stage 1/Stage 2 gates are NOT required for a short pre-lodgement email, but the
skill will offer `lla-citation-checker` if the email cites legislation beyond s.41/s.98.

## Tier 3 — Live web check (agentskills.io/specification, fetched 02-07-2026)

Spec confirmed current. Points affecting this build:

- `name`: ≤64 chars, lowercase/digits/hyphens, no leading/trailing/consecutive hyphens,
  **must match the parent directory name**. `lla-stakeholder-brief` complies.
- `description`: ≤1024 chars, must cover WHAT + WHEN with keywords. The suite's folded
  style complies; keep under 1024 (citation-checker's runs close to the limit — ours
  will be shorter).
- `metadata`: spec defines it as string→string map. DISCREPANCY: existing suite uses
  `set_skill: true` (bare boolean). Tolerated by Claude but off-spec; new skill will
  quote it (`set_skill: "true"`). Existing skills left untouched.
- `compatibility` field exists for environment needs; ours needs none (Python 3 stdlib
  only) so it is omitted per spec guidance.
- `allowed-tools` remains experimental; not used.
- SKILL.md ≤500 lines confirmed as current guidance; references one level deep only.
- Validation tool available (`skills-ref validate`); QA script will replicate its core
  checks so the gate runs without external installs.

## Discrepancies flagged

1. `set_skill: true` boolean vs spec string — resolved: quote the value in the new skill.
2. Drive reference library unavailable — resolved: live repo suite used instead; no gap
   identified that Drive material would fill.

No other conflict between Anthropic's current standard, the January 2026 PDF principles,
and house style was found.
