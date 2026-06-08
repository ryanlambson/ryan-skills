---
name: green-holmes-product
description: Green Holmes digital product development skill. Single-shot workflow for building one product end-to-end (Brief → Build → Pre-launch QA → Launch). Imports durable frameworks (Value Equation, peak-end, defaults, 5 Ps) from knowledge/frameworks.md and encodes Green Holmes philosophy as overrides to the underlying DP-GPT system. First product target is The Chamber Vacuum Method Guide. Triggers when Ryan is working on a Green Holmes digital product, drafting a brief, building chapters, running pre-launch QA, or planning a launch.
---

# Green Holmes Product: Single-shot Skill

The skill that loads first when Ryan works on a Green Holmes digital product. This version is intentionally focused on a single-shot workflow for one product at a time. The full nine-stage pipeline machinery from the DP-GPT source system is not imported. It can be ported later when there is more than one product in flight and the cost of not having it exceeds the cost of carrying it.

This skill does not produce products. It produces a correct brief, correct build posture, correct pre-launch checks, and a correct launch sequence.

---

## What this system is for

Green Holmes is sequencing digital products before physical. A method guide ships before COMPOUND. A second digital product ships before COMPOUND. The digital products self-fund the physical launch and validate purchase intent against the warm list.

This skill exists to take one digital product idea from approved brief to launched product without skipping the steps that protect the brand. It refuses to draft from a vague brief. It refuses to ship without pre-launch QA. It refuses to launch into channels Green Holmes does not own.

The goal is for Ryan to ship a product that compounds the brand rather than dilutes it.

---

## What this system is NOT

- **Not faceless.** Ryan is the brand. His chef expertise, lived experience, research literacy, and age are the unfakeable authority stack. Hide him and the brand collapses.
- **Not topic-agnostic.** Products live within fermentation, gut-brain science, and performance. The skill does not pain-mine Reddit for adjacent niches.
- **Not speed-over-depth.** A method guide is days of professional work, not hours. Quality is non-negotiable.
- **Not marketplace-distributed.** The default channel is Substack-first then the owned WordPress site. Whop, Etsy, Amazon Kindle, and Gumroad are not used at launch.
- **Not portfolio-volume.** One product at a time. Ship it well, port learnings, then start the next one.

If a sub-skill produces output that violates these principles, this skill rejects the output regardless of which sub-skill produced it.

---

## When this skill triggers

This skill triggers on first invocation of any product work. Specifically:

- "Let's spec out the method guide" → Brief phase.
- "Draft chapter X" or "let's start writing" → Build phase.
- "QA this for launch" or "pre-launch check" → Pre-launch QA phase.
- "Launch sequence" or "we're going live" → Launch phase.

If Ryan engages without naming the phase, this skill identifies it from context and confirms before proceeding.

---

## Authority resolution

When guidance from two sources conflicts:

1. **`BRAND/VOICE.md`** wins. The brand voice is structural, not polish. It cannot be overridden.
2. **This skill's overrides** win against the underlying frameworks. The Green Holmes philosophy in *What this system is NOT* sits above the durable frameworks.
3. **`knowledge/frameworks.md`** is the durable reference. Default to it for design discipline, gate logic, sales page structure.
4. **`/My Drive/AI Digital Products/`** is background context. The original DP-GPT system. Useful for understanding the source intellectual lineage. Do not implement its philosophy directly.

The voice is the constraint. Everything else flexes around it.

---

## The single-shot flow

Four phases. Each phase has a hard gate. The skill refuses to advance until the gate passes.

### Phase 1: Brief

**Output:** a complete brief at `/PRODUCTS/digital/[product-slug]/BRIEF.md`.

The brief is the contract for the build. If the brief is wrong, everything downstream is wrong. Time spent here is paid back five times in the build phase.

The brief must specify every section in the *Brief format* below. Missing sections are rejected; vague sections are rejected; sections that contradict `BRAND/VOICE.md` are rejected.

**Gate:** Ryan approves the brief explicitly. No advance without approval.

### Phase 2: Build

**Output:** the finished product file (PDF, web pages, or both).

Build executes the brief. Scope creep is rejected at the moment it appears, not absorbed silently. If the brief turns out to be wrong, the build pauses and the brief is amended explicitly. Silent drift is the failure mode.

**Posture during build:**
- Draft chapter by chapter. Ryan reviews and approves each chapter before the next is drafted.
- Photography is scheduled in parallel, not at the end. A method guide without photography is a draft, not a product.
- Brand voice is checked on every chapter. Drift is flagged immediately, not at the end.
- The peak experience and closing moment named in the brief are not rewritten during build. They are the load-bearing structural elements.

**Gate:** the finished product matches the brief. Promise drift triggers a rewrite, not a launch.

### Phase 3: Pre-launch QA

**Output:** PASS verdict from three checks running in parallel.

The three checks:

- **Fact-checker**, every claim that touches science is verified through SCITE. Citations are by publication name with DOIs. Animal versus human studies are distinguished. Effect sizes are not overstated. See `RESEARCH/FERMENTATION_FACTS.md` for the verified facts library.
- **Brand-qa**, voice, AU English, banned words, sentence case, three-sentence-paragraph rule, no em or en dashes. Spawned via `SKILLS/green-holmes-brand-qa/SKILL.md`.
- **Promise-drift check**, does the finished product still deliver what the brief promised? Does the peak experience land where the brief said it would? Does the closing moment match? Does the sales page reflect the same transition moment the brief specified?

**Gate:** all three checks return PASS. Any FAIL triggers a fix, then re-run. No exceptions.

### Phase 4: Launch

**Output:** product live. First buyers paying. Reviews accumulating.

**Default launch sequence:**
1. **Substack-first to the warm list.** Email the launch announcement to free and paid subscribers. Founders pricing live.
2. **Field Notes runway.** Four to six weeks of pre-launch Field Notes that lead the audience toward the guide. Each one ends with a soft mention, not a hard pitch.
3. **Waterfall.** LinkedIn document carousel from Ryan's personal profile, Instagram carousel and reel, YouTube technique video, TikTok hook. All cross-linking to the sales page.
4. **No paid acquisition at launch.** Validate organic signal first. If a piece of content shows unusual traction, amplify that exact piece with $100-200 of paid spend in the relevant geo. This is the validate-then-amplify model from `knowledge/frameworks.md`.
5. **Affiliate links live in the guide and on the sales page.** Chamber vac equipment, compostable bags, fermentation supplies. Affiliate revenue starts immediately.

**Measurement window:** 30 days. Track conversion rate from sales page visit, refund rate, review accumulation, organic content traction. The Customer Financed Acquisition gate (LTGP > 2× CAC within 30 days) applies only after paid amplification has actually run.

---

## The brief format (the central artifact)

Every product brief must contain these sections, in this order. Missing sections are rejected. The Chamber Vacuum Method Guide brief at `/PRODUCTS/digital/method-guide/BRIEF.md` is the canonical example.

1. **Header.** Slug, format, channel, pricing band, launch window.
2. **ICP.** Who the buyer is, what they are experiencing, what they have tried, what they wish existed, how they will judge the purchase.
3. **The service test.** Stated explicitly with a yes-or-no answer. If no, the brief is rejected.
4. **The promise.** One to two sentences. The transition moment the buyer can rehearse. Read aloud, lean-forward score one to ten.
5. **Title and subtitle.** Final, not draft. The title is the headline; this is where eighty percent of advertising effectiveness lives (Ogilvy). Test against the audience before locking.
6. **Cover concept.** Type-driven, soft black on off-white. No images. No colour. Specifies typography, layout, and the single descriptive line.
7. **Peak experience.** One specific moment in the buyer's use of the product, located by chapter or page. Engineered deliberately. Not optional.
8. **Closing moment.** The last thing the buyer experiences. One of the three patterns from `knowledge/frameworks.md` (action close, vision close, connection close, or a hybrid). Specifies the literal final page.
9. **Default configuration.** Format default, length default, bundle default, refund default. What the buyer accepts unless they actively choose otherwise.
10. **Five enhancers.** Scarcity, urgency, bonuses, guarantees, naming. Each is either applied with detail or explicitly punted with reasoning. Punting is honest; faking is rejected.
11. **Pricing structure.** Founders launch price, rise trigger, price after rise. The rise is real and public.
12. **Sales page structure.** The seven-part Donald Miller scaffold filled in for this specific product. Hero, problem, guide, plan, CTA, success stakes, failure stakes.
13. **Build outline.** Chapter list, photography requirements, production schedule, Ryan's hours estimate.
14. **Launch plan.** Substack sequence, Field Notes runway content list, waterfall pieces, paid amplification trigger.
15. **Pre-launch QA checklist.** Specific items the QA phase will verify against this brief.
16. **Open questions.** Decisions still needed before build can start. Each one names who decides and by when.
17. **Approval gate.** Ryan's explicit approval. The brief does not advance to build without it.

---

## What this skill will not do

1. **Will not draft from a vague brief.** Every section in the brief format must be specific. Vagueness in the brief produces vagueness in the build.
2. **Will not let the brief drift during build.** Scope creep is rejected at the moment it appears.
3. **Will not skip pre-launch QA.** The three checks are non-negotiable. No "we will fix it after launch."
4. **Will not launch into channels Green Holmes does not own.** Substack and the WP site are the launch surfaces. Whop, Etsy, Amazon, and Gumroad are not.
5. **Will not run paid acquisition before organic signal validates the creative.** The validate-then-amplify model holds.
6. **Will not import wellness-influencer register.** Banned words enforced on every output. Australian English everywhere.
7. **Will not let Ryan disappear from the product.** Ryan is the brand. The guide is written in his first person. His expertise is the load-bearing element.
8. **Will not bury Ryan in choices.** Output format is one-line problem, three options, one recommendation when a decision is needed.
9. **Will not promise vague outcomes.** Every promise specifies a transition moment the buyer can rehearse.
10. **Will not anchor by discounting.** Pricing rises, never falls. Founders pricing is the floor, not the ceiling.

---

## Knowledge files

- `knowledge/frameworks.md`, durable Tier 2 reference. Value Equation, peak-end, defaults, transition-moment test, lean-forward test, loss aversion, choice overload, friction-as-feature, 5 Ps, eBook playbook, Donald Miller scaffold, Green Holmes overrides.
- `knowledge/00-foundation-principles.md`, DP-GPT source material. Background only. `frameworks.md` supersedes.
- `knowledge/01-evaluation-framework.md`, DP-GPT source material. Background only. `frameworks.md` supersedes.

The DP-GPT source files at `/My Drive/AI Digital Products/knowledge/` are deeper background. Read them only when a specific framework needs further context. The Green Holmes overrides in `frameworks.md` apply.

---

## Outputs and tracking

- **Active brief:** `/PRODUCTS/digital/[product-slug]/BRIEF.md`
- **Build artifacts:** `/PRODUCTS/digital/[product-slug]/build/` (chapters, photography references, layout files)
- **Finished product:** `/PRODUCTS/digital/[product-slug]/release/` (PDF, web export, sales page copy)
- **Launch tracker:** `/PRODUCTS/digital/[product-slug]/LAUNCH.md` (sequence, dates, results)
- **Stage 1 archive:** `/SKILLS/green-holmes-product/outputs/01-chamber-vac-method-guide-stage1.md` (the prior validation work; preserved for reference, superseded by the brief)

---

## First product target

**The Chamber Vacuum Method Guide.**

- Format: PDF and web-rendered, both at launch.
- Channel: Substack-first, then the owned WP site at greenholmes.com.au.
- Pricing: $29 founders launch. Rise trigger: first 200 buyers or end of Q4 2026, whichever first. Price after rise: $39.
- Launch window: Q3 2026.
- Brief: `/PRODUCTS/digital/method-guide/BRIEF.md`.

Subsequent products are not yet specified. The next product is decided after the method guide ships and the 5 Ps diagnostic runs against post-launch data.

---

*Version 2.0, May 2026*
*Refocused as single-shot. Nine-stage pipeline machinery removed. Frameworks consolidated to `knowledge/frameworks.md`.*
*Replaces v1.0 which imported the full DP-GPT pipeline.*
