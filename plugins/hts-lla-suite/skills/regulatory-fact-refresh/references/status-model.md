# Status model — regulatory-fact-refresh

Every extracted claim is assigned exactly one of four statuses in Phase D. The
status determines what Phase E (Apply) may do. The model is deliberately
four-state rather than three, because the most consequential regulatory facts
are often mid-transition, and a three-state CURRENT/STALE/UNVERIFIED model is
forced to mislabel them.

## The four statuses

### CURRENT
The claimed value matches the authoritative value at every relevant tier.
Apply: no action.

### STALE
A single in-force instrument supersedes the claimed value, unconditionally, and
nothing keeps the old value valid (no commencement lag, no lower-tier instrument
still carrying it, no application or condition required).
Apply: propose the correction as a tracked suggestion, with the primary source.
Never an automatic substitution.

### CHANGED-CONDITIONAL
The authoritative position has moved, but whether this document needs editing
depends on a condition. Triggered by any of:
- (a) the change is not yet commenced or proclaimed (passed or assented but not
  in force);
- (b) a lower-tier instrument still carries the old value (e.g. a planning
  scheme not yet amended — "scheme lag");
- (c) the new value is a ceiling or eligibility that requires an application or
  condition to bind this particular subject (e.g. a statutory maximum a specific
  licence must apply to take up).
Apply: report the change, the condition, and that deciding which fact governs
this document is a human judgement. Never auto-corrected. If approved, insert
the verified statement together with its condition as a tracked suggestion.

### UNVERIFIED
No primary source could be located, or the only available source is over 12
months old and no live check was possible.
Apply: flag and stop. Never guess, never invent a value.

## The decision test (STALE vs CHANGED-CONDITIONAL)

Ask, in order:
1. Is the change actually in force (commenced / proclaimed)? If not →
   CHANGED-CONDITIONAL (a).
2. Does any lower-tier instrument still carry the old value? If yes →
   CHANGED-CONDITIONAL (b).
3. Is the new value a ceiling or eligibility that needs an application or
   condition to bind this subject? If yes → CHANGED-CONDITIONAL (c).
If none apply and a single in-force instrument unconditionally supersedes the
old value → STALE.

## Why this matters — worked illustration

The WA small bar capacity is CHANGED-CONDITIONAL on both (b) and (c): the
statutory ceiling rose from 120 to 150, but a venue's licensed cap stays 120
until a Form 11 increase is granted (c), and LPS No. 1 Schedule 1 may still read
120 pending a scheme amendment (b). A three-state model would tag this STALE and
suggest swapping 120 to 150 — a false statement about the venue. The fourth
state exists to prevent exactly that error.
