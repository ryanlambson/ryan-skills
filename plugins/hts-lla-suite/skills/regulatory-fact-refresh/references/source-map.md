# Source map — regulatory-fact-refresh

Maps each claim type to its authoritative source *base*, not to a hardcoded deep
link. Specific URLs are resolved at verify time, because a hardcoded URL is
itself a fact that can go stale — the very thing this skill exists to catch.

| Claim type | Authoritative source (resolve live) |
|---|---|
| Legislative section (WA) | Consolidated Act at legislation.wa.gov.au |
| Legislative section (Cwlth) | Federal Register of Legislation (legislation.gov.au) |
| Regulation | The regulation as gazetted on the relevant legislation site |
| Planning scheme (LPS / clause) | Operative scheme text via the local government or WAPC |
| Director's policy / regulator guideline | DLGSC, LGIRS, WAPC or Health — current published version |
| Case citation | eCourts WA, AustLII or JADE (primary case-law repositories) |
| Strategic planning instrument | The council's current published Strategy or SCP |
| Industry / professional publication | The body's current published edition (e.g. NHMRC, ABS) |

## Resolution rules

- In deep-refresh mode, always resolve to the current consolidated or published
  version, not a cached snapshot.
- A regulator guideline (tier 4) is never the source for a statutory value
  (tiers 1–3); use it only to corroborate, and flag it if it conflicts with the
  Act.
- Never hardcode a deep URL into this file. Resolve it at run time and record the
  resolved URL in that run's freshness report, so the provenance travels with the
  output rather than rotting in the bundle.
