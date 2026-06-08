# Scripts guide — regulatory-fact-refresh

All scripts are Python 3. Dependencies: standard library, plus **PyYAML**
(registry read/write), and optionally **python-docx** (.docx input) and
**pdfminer.six** (.pdf input). Online verification is performed by the cognitive
layer's WebFetch, not by the scripts — the scripts handle parsing, comparison
against the registry and cached sources, and report generation.

## extract_claims.py — Phase A
```
python extract_claims.py --input DOC [--output claims.json]
```
Reads .md/.txt/.docx/.pdf; emits a JSON claims register. Categorisation is
heuristic (regex); review the register before relying on it.

## verify_claim.py — Phases B–C
```
python verify_claim.py --claims claims.json \
  --registry references/stale-citations.yaml \
  [--sources sources.json] [--output verified.json]
```
Assigns CURRENT / STALE / CHANGED-CONDITIONAL / UNVERIFIED. Registry hits are
deterministic. UNVERIFIED items are handed to the cognitive layer for live
WebFetch and the CHANGED-CONDITIONAL decision test on unknown patterns.
`--sources` accepts a JSON map `{source_id: text}` or a plain text file of
cached source content.

## generate_freshness_report.py — Phase D
```
python generate_freshness_report.py --claims verified.json \
  [--document NAME] [--output report.md]
```
Emits the Markdown freshness report, grouped CHANGED-CONDITIONAL, STALE,
UNVERIFIED, CURRENT.

## generate_md_patch.py — Phase E (default)
```
python generate_md_patch.py --claims verified.json [--output patch.md]
```
Side-by-side review patch for STALE and CHANGED-CONDITIONAL items. Never edits
the source. CHANGED-CONDITIONAL items show the statement-with-condition, never a
bare value swap.

## update_stale_registry.py
```
python update_stale_registry.py \
  --registry references/stale-citations.yaml --entry entry.json
```
Appends a verified entry. Refuses entries missing a primary_source or
verified_on, and refuses CHANGED-CONDITIONAL entries without a condition.

## docx tracked changes
Not handled here. Hand approved corrections to the **tracked-document-editor**
skill.

## Dependency note
SKILL.md frontmatter should gain a `compatibility` line noting PyYAML (and
optional python-docx / pdfminer.six) at the next clean rebuild. Deferred for now
to avoid creating a duplicate SKILL.md through the create-only Drive connector.
