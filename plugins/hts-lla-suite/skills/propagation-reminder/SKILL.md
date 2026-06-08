---
name: propagation-reminder
description: >
  Reminds you to propagate an approved correction into the hard-baked
  registries and affected files once it has been verified, approved, and its
  targets located. Use when a fact-refresh run produces an approved STALE or
  CHANGED-CONDITIONAL finding, or when you ask "what updates are pending", "what
  do I need to propagate", or "remind me what to re-distribute". Produces a
  propagation checklist and maintains a pending-updates ledger. The LLA citation
  registry is the first application, but the skill is domain-agnostic. Do NOT
  use to make the edits itself, to verify facts, or as a background or scheduled
  alarm — a skill acts only when invoked.
metadata:
  author: Ryan Lambson
  version: "0.1-draft"
  role: propagation-reminder
---

# Propagation Reminder (draft v0.1)

A bridge skill for one specific gap: when an essential regulatory correction is
found and approved, the change does not reach downstream outputs by itself. The
stale-citations registries are hard-baked into their skill bundles, so a
correction reaches all future outputs only once the updated set skill is
re-distributed. This skill makes that step impossible to forget.

## What this skill is — and is not

It is a prompt at the decision point, not an alarm clock. A skill has no
background process, no scheduler, and no memory of its own between sessions. It
cannot ping you later. What it can do is fire the moment a correction is
approved-and-located within a conversation, or answer on demand, and hand back a
precise checklist of what must be propagated and where.

## When it fires

1. Inside a regulatory-fact-refresh run: the instant a STALE or
   CHANGED-CONDITIONAL finding is verified against a primary source, approved,
   and its target file(s) identified.
2. On demand, when you ask what propagation is outstanding.

## What it produces — the propagation checklist

For each approved correction, a directive containing:

- The correction: claim, old value, new value or condition, and status
  (STALE or CHANGED-CONDITIONAL).
- Primary source and verification date.
- Targets, in order (see below), each with its fold-back step.
- A one-line ledger entry to append to PENDING_PROPAGATION.md.

## Propagation targets (in order)

1. regulatory-fact-refresh/references/stale-citations.yaml — the cross-domain
   master registry. Add or update the entry here first.
2. lla-citation-checker/references/stale-citations-registry.md — the LLA
   enforcement set skill that every LLA output is gated through. Promote the
   LLA-relevant entry here, then re-package and re-install the set skill across
   the LLA projects. This is the step that reaches all future outputs.
3. Any in-flight or already-lodged draft that contains the stale fact — listed
   explicitly so it is not missed.

## The pending-updates ledger

PENDING_PROPAGATION.md sits in this skill's bundle. Append an entry when a
correction is approved-and-located; strike it through when re-distribution is
confirmed. Persistence caveat: edits made during a run live in the ephemeral
sandbox copy. To make the ledger durable, fold the updated file back into the
canonical bundle — the same deliberate discipline the registries use. For a
ledger that gates regulatory lodgements this is a feature: changes are reviewed,
versioned events, never silent.

## What it does NOT do

- It does not edit any registry, skill, or draft. It tells you what to edit.
- It does not verify facts. That is regulatory-fact-refresh.
- It does not notify, schedule, or run in the background.
- It does not mark a correction propagated until re-distribution is confirmed.

## Worked example — WA Small Bar capacity

regulatory-fact-refresh verifies that the small bar statutory ceiling rose from
120 to 150 (Liquor Control Amendment Act 2025 s.9, amending ss.41A and 41B),
status CHANGED-CONDITIONAL: a venue's licensed cap stays 120 until a Form 11
increase is granted, and LPS definitions may lag. The entry is approved. This
skill then returns:

- Add the CHANGED-CONDITIONAL entry to the master registry.
- Promote it to lla-citation-checker's registry; re-package; re-install across
  LLA projects.
- Flag the Witchcliffe brief and any other live draft stating "120".
- Ledger line: "2026-06-03 — WA small bar 120/150 ceiling (CHANGED-CONDITIONAL)
  — master: done / set skill: PENDING / drafts: Witchcliffe."

## Status

Draft v0.1. Scaffolded alongside regulatory-fact-refresh. Name, trigger
phrasing, and whether to keep the LLA framing or broaden it further are open for
review.
