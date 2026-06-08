---
name: regulatory-fact-refresh
description: >
  Verifies whether regulatory facts in a document are still current against
  primary sources and reports staleness without silently changing anything. Use
  when asked to check a document for currency, run a freshness check, verify
  citations against the current legislation, refresh the citations in a PIA or
  DA report, ask what has changed since a draft date, or confirm that patron
  caps, thresholds, distances, fees or definitions are still right. Covers WA
  liquor (Liquor Control Act), planning (LPS, SPP, LPP), food safety and other
  regulatory domains. Do NOT use for editorial polish, spelling or grammar,
  drafting new content, plagiarism checks, or general web research, and never
  invent a value when no primary source exists.
metadata:
  author: Ryan Lambson
  version: "0.1-draft"
  role: regulatory-currency-verification
---

# Regulatory Fact Refresh (draft v0.1)

Checks the regulatory facts in a document against their primary sources and
reports which are current, stale, conditionally changed, or unverifiable. It
proposes corrections but never applies them without explicit approval, and never
swaps a value silently.

## When to use

Triggers: "check this for currency", "run a freshness check", "verify these
citations against the current legislation", "refresh the citations in [doc]",
"has anything changed since [date]", "are these patron caps / thresholds /
distances still right".

## When NOT to use

- Editorial polish, spelling, grammar, style.
- Drafting new content (this skill is verification only).
- Plagiarism or originality checks.
- General web research or news — use web search directly.
- Commercial facts with no primary source (e.g. visitor numbers) — flag as
  UNVERIFIED, never invent.
- Internal documents treated as authorities — they are sources to be checked,
  never cited as authority (no circular verification).

## Workflow — five phases, hard gates between each

Phase A — Extract. Scan the input for verifiable regulatory facts and
categorise each (numerical thresholds, section references, regulation
references, case citations, planning-instrument references, regulator names and
contacts, policy or guideline names with version dates, use-class
classifications, trading hours, fees, distances, dates). Output: a JSON claims
register (scripts/extract_claims.py).

Phase B — Map to primary source. For each claim, identify the authoritative
source per references/authority-hierarchy.md.

Phase C — Verify. Cached-first: check the local cached source if present;
WebFetch the live primary source only in explicit deep-refresh mode. Compare
claimed value against current value (scripts/verify_claim.py).

Phase D — Report. Assign each claim one of four statuses (below). Output:
scripts/generate_freshness_report.py.

Phase E — Apply (gated). Only on explicit approval. Default output is a
side-by-side .md patch (scripts/generate_md_patch.py). For tracked-changes
.docx, hand the approved corrections to the tracked-document-editor skill; do
not apply docx revisions here. Never substitute a value automatically.

Gate between D and E: stop and wait for an explicit "go" before applying.

## The four-state status model

Full definitions and the decision test live in references/status-model.md. In
brief:

- CURRENT — claimed value matches the authoritative value at every relevant
  tier. No action.
- STALE — a single in-force instrument supersedes the claimed value
  unconditionally, nothing keeping the old value valid. Correction proposed as a
  tracked suggestion, never an auto-swap.
- CHANGED-CONDITIONAL — the authoritative position has moved, but whether this
  document needs editing depends on a condition: not yet commenced or
  proclaimed; a lower-tier instrument still carries the old value; or the new
  value is a ceiling or eligibility that needs an application or condition to
  bind this subject. Report the change, the condition, and that which fact
  governs is a human judgement. Never auto-corrected.
- UNVERIFIED — no primary source located, or the only source is over 12 months
  old with no live check possible. Flag and stop; never guess.

Decision test (STALE vs CHANGED-CONDITIONAL): if any of (a) the change is not
yet in force, (b) a lower-tier instrument still carries the old value, or (c)
the new value is a ceiling or eligibility requiring an application or condition,
then CHANGED-CONDITIONAL; otherwise STALE.

## The no-scalar-swap rule

Apply (Phase E) never substitutes one value for another. It may only insert the
verified current statement together with its condition, as a tracked suggestion
for approval, or flag the location and leave it. Deciding which fact governs a
given document is a legal judgement and stays with the user.

## Authority hierarchy

Summary; full version in references/authority-hierarchy.md. Highest to lowest:
legislation as gazetted; regulations; operative planning schemes; director's
policies and regulator guidelines; court and tribunal decisions; strategic
planning instruments; industry or professional-body publications; internal
documents (sources to be verified, never authorities). Same-tier conflict: more
recent prevails. Cross-tier: higher prevails.

## Scripts

| Script | Purpose |
|---|---|
| scripts/extract_claims.py | .docx/.md/.pdf to categorised JSON claims register |
| scripts/verify_claim.py | Identify primary source and fetch current value; cached-first, WebFetch on deep refresh |
| scripts/generate_freshness_report.py | Claims register to the four-state report table |
| scripts/generate_md_patch.py | STALE and CHANGED-CONDITIONAL items to a side-by-side .md patch |
| scripts/update_stale_registry.py | Append verified patterns to references/stale-citations.yaml in the promotable schema |

Full invocation patterns in references/scripts-guide.md. All scripts are Python
3, standard library plus WebFetch — no docx revision machinery here.

## The stale-citations registry

references/stale-citations.yaml is the hard-baked, cross-domain master registry,
seeded only with entries verified against a primary source. Each entry carries:
id, jurisdiction, domain, instrument, provision(s), old value, new value,
status, condition (for CHANGED-CONDITIONAL), primary source, verification date.

Updating: scripts/update_stale_registry.py writes verified entries to the
bundled file in the promotable schema. To persist beyond the session and reach
LLA outputs, the entry is promoted into lla-citation-checker's
references/stale-citations-registry.md and that set skill is re-packaged and
re-installed (the propagation-reminder skill flags this step). Runtime never
reads the registry from Google Drive.

## Worked example — WA Small Bar capacity

Input claim: "Small Bar ... patron numbers capped at 120."

- A: extract "120 patrons" as a numerical threshold tied to a small-bar licence.
- B: primary sources are (i) Liquor Control Act 1988 (WA) ss.41A and 41B; (ii)
  LPS No. 1 Schedule 1 'Small Bar' definition.
- C: verify against the current consolidated Act and the cached LPS No. 1.
- D: status CHANGED-CONDITIONAL. The statutory ceiling rose from 120 to 150
  (Liquor Control Amendment Act 2025 s.9, amending ss.41A and 41B), but a
  venue's licensed capacity stays 120 until a Form 11 increase is granted on a
  safety assessment, and LPS No. 1 Schedule 1 may still read 120 pending a
  scheme amendment.
- E (if approved): insert the verified statement with its condition as a tracked
  suggestion — e.g. "the statutory maximum is now 150 under the Liquor Control
  Act 1988; this venue's licensed cap remains 120 unless and until an increase
  is applied for and granted." Never a bare 120-to-150 swap.

## Refusals and gates

- Refuses to apply an update without showing the primary source for the new
  value.
- Refuses to update silently; every change is presented for explicit approval.
- Refuses subjective or stylistic edits; factual corrections only.
- Refuses to mark a claim CURRENT if the only source is over 12 months old with
  no live check possible.
- Refuses to verify a case citation against anything other than a primary
  case-law database.
- Requires an explicit "go" before moving from Report (D) to Apply (E).

## Status

Draft v0.1. Reference files (authority-hierarchy.md, status-model.md,
stale-citations.yaml, source-map.md, scripts-guide.md) and the five scripts are
the next build step. QA gate to be run before packaging.
