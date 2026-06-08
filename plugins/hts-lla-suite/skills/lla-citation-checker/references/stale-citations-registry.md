# Stale Citations Registry

**Status:** Living registry — grows with each HTS project
**Last updated:** 5 June 2026 (v1.1 — added WA small bar capacity 120→150)
**Maintainer:** HTS / lla-citation-checker

This file lists known stale citations across NSW and WA liquor licensing. When the `apply_stale_registry.py` script finds a citation that matches an entry below, it raises a WARN (with the suggested current reference) or a FAIL (if the cited authority has been outright repealed).

Status codes:
- **STALE-RENUMBERED** — the section / clause number has changed; substance unchanged → WARN
- **STALE-REPEALED** — the authority has been repealed or replaced → FAIL
- **STALE-SUPERSEDED** — a newer Guideline / policy / instrument has superseded → WARN
- **STALE-UNCONFIRMED** — possible stale but not yet verified → WARN with note

## Registry

| Citation | Status | Replacement | Notes |
|---|---|---|---|
| `*Liquor Act 2007* (NSW), s.48` | STALE-UNCONFIRMED | Possibly `*Liquor Act 2007* (NSW), s.72I` | December 2025 consolidation under the Vibrancy Reforms may have renumbered the overall-impact test from s.48 to s.72I. ILGA Guideline 6 (March 2025) and Bar 333 decision (Sept 2025) still cite s.48. Substantive test unchanged. Verify at lodgement against legislation.nsw.gov.au. |
| `small bar` ... `120` | STALE-SUPERSEDED | `150 persons (patrons plus staff) at any one time` | 2025 amendments to the *Liquor Control Act 1988* (WA), ss.41A/41B, increased the small bar maximum capacity from 120 to 150 persons (patrons **plus** staff) at any one time. Any HTS small bar PIA/DA/SoRPE stating a "120" cap, or framing 150 as patrons-only, is stale. Existing small bars may apply via Form 11 (fee waived) to lift 120→150 subject to a safe-capacity assessment. Verify at legislation.wa.gov.au. WARN on any "120" appearing within a small bar capacity context. |

## How to add an entry

1. Confirm the staleness against the primary source (legislation.nsw.gov.au, legislation.wa.gov.au, ilga.nsw.gov.au).
2. Add a row to the table with the citation pattern (use a substring that uniquely identifies the cited section in any natural-language phrasing), the status code, the replacement reference, and source-cited notes.
3. Increment the "Last updated" date.
4. Commit to the lla-citation-checker skill folder and re-distribute to all HTS projects.

## Future v1.1+ refinement

Per the OUTLINE review, this registry may be split into per-jurisdiction files (e.g., `stale-nsw.md`, `stale-wa.md`) once the registry exceeds ~30 entries. For v1.0, a single file is sufficient.

## Suspected items not yet added

These are candidates flagged during research but not yet confirmed:

- ILGA Guideline 6 itself may be re-issued in 2026 to reflect the s.48 → s.72I renumbering. Check publication dates on each new lodgement.
- The Sydney CBD Entertainment Precinct map may shift if City of Sydney designates an SEP affecting Circular Quay. Track via the L&GNSW Sydney CBD precincts page.
- The "Director's Policy" framework in WA was due for review per LGIRS. If a new WA Director's Policy compendium is issued, all current Director's Policy references will need recasting.
- The 2025 WA *Liquor Control Act 1988* amendment package also adjusted small bar trading on Christmas Day / Good Friday / Anzac Day (s.98AA) — confirm whether any HTS trading-hours templates still recite the pre-2025 position.
