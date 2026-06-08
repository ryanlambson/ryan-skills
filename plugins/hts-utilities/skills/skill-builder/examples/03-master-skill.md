# Example 3 — Master Skill Governing Sub-Skills

A skill that sits at the top of a domain and governs a family of sub-skills. The
shape of `lla-gpt` in Ryan's existing ecosystem.

## Brief (Phase 1)

**Skill name:** `[domain]-advisor` (e.g. `hospitality-licence-advisor` — verb-noun
master pattern)

**Trigger phrases:**
- Any reference to the domain (specific to the master)
- "[Domain] project" / "[Domain] strategy" / "[Domain] submission"
- "Start a [domain] project"

**Negative triggers:** Do not trigger for adjacent but distinct domains. The master
skill is *exclusive and fixed* to its territory.

**Core workflow:**
1. Authority lock (master skill identity and authoring entity)
2. Permitted scope (what work this skill governs)
3. Out-of-scope refusals (what this skill never does)
4. Sub-skill registry (which sub-skills are recognised, what they do)
5. Authority resolution across the family (when sub-skills conflict)
6. Common patterns enforced across all sub-skills (branding, citation discipline, QA)

**Gates:** Sub-skill outputs that violate master skill rules are rejected regardless
of which sub-skill produced them.

**Authority hierarchy (master-level):**
1. Legislation / source-of-truth standard for the domain
2. Master skill's "What this system is NOT" (the brand/scope lock)
3. Sub-skills' specific workflows
4. Reference materials

**Output type:** Governance — not a deliverable. Sub-skills produce deliverables; the
master enforces consistency.

**Bundled scripts:**
- `compliance_check.py` — domain-wide QA rules applied to any sub-skill output
- `cite_check.py` — citation discipline enforcement (no over-elevation of authority tiers)

**MCP / tool dependencies:** Document builder MCP if generating formal outputs.

**Distribution target:** Claude.ai (relies on multi-skill loading).

## Research (Phase 2)

- Tier 1: Internal knowledge of master/sub-skill pattern from `lla-gpt`
- Tier 2: Drive `SKILLS/lla-gpt/` and related sub-skills for the pattern in production
- Tier 3: Webscrape any domain-specific regulatory updates or new authoritative sources

## Outline (Phase 3)

```
[domain]-advisor/
├── SKILL.md  (~350 lines — long because master skills carry governance content)
├── scripts/
│   ├── compliance_check.py
│   └── cite_check.py
├── references/
│   ├── authority-hierarchy.md
│   ├── permitted-scope.md
│   └── citation-tiers.md
└── assets/
    └── house-style-tokens.json
```

Key sections in SKILL.md:

1. Title
2. **Authoring Entity Lock (MANDATORY)** — the signature master-skill opener
3. System Identity (numbered as "1.")
4. Permitted Scope of Work
5. Out-of-Scope Refusals
6. Authority Hierarchy (across the whole family)
7. Sub-Skill Registry (named sub-skills with one-line purpose each)
8. Cross-cutting Rules (branding, citation, QA — applied to all sub-skill outputs)
9. Compliance Gate

## Draft (Phase 4)

SKILL.md is at the upper end of the 500-line ceiling. Detail pushed to references/
where possible. The Authority Hierarchy section is kept in SKILL.md (not pushed to
references) because it's referenced in nearly every sub-skill decision.

QA gate passes after one revision: the description was too generic, didn't list enough
specific trigger phrases. Tightened with explicit phrases including "PIA", "Public
Interest Assessment", and the entity name.

## Output

`/mnt/user-data/outputs/[domain]-advisor.zip` + Drive backup. INDEX.md in Drive updated.

---

**Why this is a useful example:**

Shows the pattern Ryan already uses for `lla-gpt`. Master skills are heavier than
single-purpose skills because they carry governance for an entire family. The
Authority Lock at the top is the signature move — it makes the skill un-confusable
with anything else and binds all sub-skill output to a single accountability frame.

This is the shape to use when:
- The domain has legal or branding implications that need locking down
- Multiple sub-skills need consistent rules
- A single point of identity matters (e.g. authoring entity, professional standard)
- Sub-skills could otherwise drift into adjacent territory
