---
name: lla-new-project-setup
description: >
  HTS new LGA project setup tool for the LLA GPT system. Use this skill
  whenever the user wants to create a new liquor licensing project for a new
  Local Government Area, set up a new LGA locality, onboard a new council area,
  start a project for a new jurisdiction, or asks "how do I set up a new LGA".
  Also trigger when the user mentions a council or LGA that is not the currently
  locked locality, or asks to duplicate or adapt the system for a different area.
  This skill prevents cross-contamination between LGA projects by enforcing
  correct setup from the start and producing a gap analysis of missing files
  before any work begins.
metadata:
  author: Hospitality Total Services (Aus) Pty Ltd
  version: 1.1.0
  category: project-management
---

# LLA New Project Setup — LGA Onboarding Workflow

## Purpose

This skill establishes a new LGA project correctly from the start, preventing
the cross-contamination and missing-file problems that occur when projects are
set up informally. Every new LGA project must pass through this workflow before
any PIA drafting begins.

---

## Pre-Delivery Gate Recap (MANDATORY)

Every project set up under this skill inherits the HTS two-stage
pre-delivery gate. Once project files are loaded and drafting begins, no
output ships until:

1. **Stage 1 — lla-citation-checker** audits every citation against its
   source (legislation, regulations, ILGA Guidelines / Director's Policies,
   case law, planning instruments, knowledge modules, data citations).
2. **Stage 2 — lla-compliance-checker** runs the HTS quality assurance
   checklists (source-of-truth, authority hierarchy, locality lock, content
   quality, harm assessment, legislative framework, drafting standards,
   document structure, common error prevention, and Stage 1 confirmation).

This skill is responsible for ensuring the project's file structure supports
both stages — i.e., every authority the drafters cite must have a project
file to resolve against. See the Required File Checklist below.

---

## Step 1 — Confirm the New LGA

Collect the following before doing anything else:

```
□ Full LGA name (official): e.g., "City of Joondalup"
□ LGA type: City / Town / Shire
□ Current gazetted Local Planning Scheme number and name
□ Is a new/draft scheme pending? (Y/N — if Y, obtain name)
□ Primary contact at the LGA planning department (if known)
□ First application type: Tavern / Hotel / Packaged Liquor / Small Bar / ETP
```

---

## Step 2 — Declare the Locality Lock

Generate the locality lock declaration for this project.
This text must be placed at the top of every system file in the new project:

```
## LOCALITY AUTHORITY (MANDATORY)

This Project is locked to the following locality:

- Local Government Area: [FULL LGA NAME]
- Planning Source of Truth: [LGA]_PLANNING_MASTER_PACK.md

### Enforcement Rules
- ONLY planning content contained in [LGA]_PLANNING_MASTER_PACK.md may be used.
- NO planning schemes, strategies, policies, or interpretations from any
  other LGA are permitted.
- If a required planning control is not present in [LGA]_PLANNING_MASTER_PACK.md,
  the system MUST stop and request the missing source.
- The locality must NEVER be inferred, substituted, or generalised.
```

---

## Step 3 — Required File Checklist

Produce a gap analysis against the full required file list.
Mark each file as PRESENT, MISSING, or NOT APPLICABLE:

### System Files (Universal — Copy from Master)
```
□ LLA_GPT_CORE_INSTRUCTIONS.md        — copy from master, update locality lock
□ SYSTEM_OPERATIONAL_INSTRUCTIONS.md  — copy from master, update locality lock
□ SYSTEM_QUICK_REFERENCE.md           — copy from master, update locality lock
□ SYSTEM_ERROR_PREVENTION.md          — copy from master, update locality lock
□ SYSTEM_README.md                    — generate new for this LGA
```

### Legislation (Universal — Copy from Master)
```
□ LEGISLATION_LCA1988_MASTER_INDEXED.md  — identical across all projects
```

### Director's Policies (Universal — Copy from Master)
```
□ DP_PIA_MasterCompendium.md   — identical across all projects
□ DP_Full_MasterCompendium.md  — identical across all projects
```

### Case Law (Universal — Copy from Master)
```
□ Case_Precedent_Compendium.md  — identical across all projects
```

### Knowledge Modules (Universal — Copy from Master)
```
□ KNOWLEDGE_HarmMinimisation.md
□ KNOWLEDGE_AlcoholInformation.md
□ KNOWLEDGE_Tourism.md
□ KNOWLEDGE_EntertainmentNoise.md
□ KNOWLEDGE_FoodCulture.md
□ KNOWLEDGE_AlcoholAdvertising.md
```

### PIA Templates (Universal — Copy from Master)
```
□ PIA_TEMPLATE_TAVERN_RESTRICTED.md   — if Tavern application pending
□ PIA_TEMPLATE_HOTEL.md               — if Hotel application pending
□ PIA_TEMPLATE_PACKAGED_LIQUOR.md     — if Packaged Liquor pending
□ PIA_TEMPLATE_SMALL_BAR.md           — if Small Bar pending
□ PIA_TEMPLATE_RESTAURANT_ETP.md      — if ETP pending
```

### Locality-Specific Files (Must Be Sourced for This LGA) ⚠️
```
□ [LGA]_PLANNING_MASTER_PACK.md          — MUST BE CREATED (see Step 4)
□ Current Local Planning Scheme (PDF)    — source from LGA or DPLH
□ Local Planning Strategy (PDF)          — source from LGA
□ All applicable Local Planning Policies — source from LGA
□ Local Tourism Planning Strategy        — if applicable
□ Strategic Community Plan               — source from LGA
□ Public Health Plan                     — source from LGA
□ Settlement-specific strategies         — if applicable
□ Planning Document Index (LPP matrix)   — generate in Step 4
```

---

## Step 4 — Generate the Planning Master Pack

The `[LGA]_PLANNING_MASTER_PACK.md` is the most critical locality-specific
file. It must be built from the LGA's actual planning documents.

Read `references/PLANNING_MASTER_PACK_TEMPLATE.md` for the required structure.

### Building the Planning Master Pack

Requires the user to upload:
1. Current gazetted Local Planning Scheme (full text)
2. Local Planning Strategy
3. Key Local Planning Policies (especially: use table, activity centres, noise,
   signage, heritage, events, alfresco, liquor)

From these, extract and compile:
- Zoning table with use classes for all relevant zones
- Activity centre hierarchy and centre-specific provisions
- LPP trigger matrix (which policies apply to which applications)
- Amenity and noise framework
- Key definitions
- Any liquor-specific provisions

Output: `[LGA]_PLANNING_MASTER_PACK.md` — ready for upload to new project.

---

## Step 5 — Generate the Project README

Produce a `SYSTEM_README.md` for the new LGA project containing:
- Locality lock declaration (from Step 2)
- File directory specific to this project
- Workflow summary
- Key planning notes for this LGA

Use the Stirling `SYSTEM_README.md` as the structural template.
Replace ALL Stirling-specific content with the new LGA content.

---

## Step 6 — Cross-Contamination Check

Before declaring the project ready, verify:

```
□ No references to other LGAs in any system file
□ Locality lock declaration present at top of all system files
□ Planning Master Pack contains only this LGA's planning content
□ All file names use correct LGA identifier (not another LGA's name)
□ SYSTEM_README file directory lists correct file names
□ No Stirling, AMR, Rockingham, or other LGA content in planning files
```

If any contamination is found: correct before proceeding.

---

## Step 7 — Project Handover Summary

Produce a handover summary listing:
1. LGA confirmed and locked
2. Files present (can begin work)
3. Files missing (must be sourced before PIA drafting can begin)
4. **Pre-delivery gate readiness:** confirm `lla-citation-checker` and
   `lla-compliance-checker` are available in the workspace, and that the
   project's file structure resolves every authority the gate will check
   against
5. Recommended next steps
6. Estimated time to full project readiness

---

## Reference Files

- `references/PLANNING_MASTER_PACK_TEMPLATE.md` — blank template for building
  a new LGA Planning Master Pack


---

**System Version:** 1.1 — Two-stage pre-delivery gate wired
**Last Updated:** 21 May 2026
