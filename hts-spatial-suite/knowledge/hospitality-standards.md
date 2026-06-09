# Hospitality Standards (shared knowledge)

> Jurisdiction-swappable DEFAULTS for modeling. These are sane starting dimensions to make
> a model look right — they are **NOT certified compliance values**. Spec-grade verification
> is the v2 `spatial-compliance` skill. Select the block matching the job's market.
>
> Every figure below is a **DEFAULT for modeling**. Never present any of it as a compliance
> guarantee in client materials. Where a figure is a legal minimum it is labelled "(min)";
> treat minimums as floors to design *above*, not targets.

## How to use
1. Read the job's jurisdiction (US or AU). Default **AU** for HTS work unless told otherwise.
2. Pull clearances / room areas / spacings as modeling defaults only.
3. Round to tidy modeling values; keep openings and circulation at or above the minimums so
   the render reads as a real, usable space.
4. Never present these as compliance guarantees. If the client needs certification, that is
   the v2 `spatial-compliance` workflow, not this suite.

---

## US block — ADA 2010 Standards / IBC (imperial)

### Access & circulation
- Clear door opening width: **32 in (min)** (ADA 404.2.3).
- Accessible route clear width: **36 in (min)**, narrowing to 32 in at a point for ≤24 in
  (ADA 403.5.1).
- Clear floor space (one wheelchair, stationary): **30 × 48 in** (ADA 305).
- Wheelchair turning space: **60 in diameter circle**, or T-shaped turn (ADA 304.3).
- Ramp running slope (new build): **1:12 (max)**, with landings (ADA 405).
- Knee/toe clearance under counters & tables: **≥27 in high, 30 in wide, 17–25 in deep**
  (ADA 306).

### Service & dining surfaces
- Sales/service counter accessible portion: **36 in high (max)**; 36 in long for a parallel
  approach, or 30 in long with knee space for a forward approach (ADA 904.4).
- Accessible dining surface (table/bar) top height: **28–34 in above finish floor**; knee
  clearance ≥27 in (ADA 902).

### Sanitary
- Water closet clearance: **60 in wide × 56 in deep** (min), measured from side and rear
  walls; door swing may not overlap (ADA 604).

### Hotel guest-room areas (industry design defaults, imperial)
- Economy: **175–250 sq ft**. Midscale: **275–350 sq ft**. Upscale/standard: **300–400 sq ft**.
  Luxury standard room: **450–600 sq ft**. King suite: **350–450 sq ft**. Junior suite:
  **350–500 sq ft**; one-bedroom suite: **500+ sq ft**.
- Circulation around the bed: **36 in (min)**, **48 in** where two guests or luggage cross.

## AU block — NCC 2022 / AS 1428.1-2009 (metric)

### Access & circulation
- Clear door opening width: **850 mm (min)** (AS 1428.1, 2009 increase).
- Continuous accessible path / circulation clear width: **1000 mm (min)** (AS 1428.1).
- Passing space (where path < 1800 mm): **1800 × 2000 mm**, at intervals along the path.
- Wheelchair turning (90°–180°): **1540 mm wide × 2070 mm** in the direction of travel;
  turning circle **1540 mm diameter** (AS 1428.1).
- Ramp running slope: **1:14 (max)** for rises > 190 mm (1:20 preferred), with compliant
  landings (AS 1428.1).

### Service & dining surfaces
- Accessible counter / bench top height: **≤830–850 mm** (e.g. semi-recessed basin top
  830 mm under the 2009 amendment).
- Accessible dining surface: knee clearance and approach per AS 1428.1; model tops at
  **~720–850 mm** to read correctly.

### Sanitary
- Accessible sanitary compartment (toilet circulation space): **1900 mm wide × 2300 mm long**
  (AS 1428.1).

### Hotel guest-room areas (industry design defaults, metric)
- Budget: **16–23 m²**. Midscale: **25–32 m²**. Standard/upscale: **28–37 m²**. Luxury
  standard room: **42–55 m²**. King suite: **33–42 m²**.
- Circulation around the bed: **900 mm (min)**, **1200 mm** at crossing points.

---

## Dining / public zones (jurisdiction-light modeling defaults)

Industry space-planning rules of thumb — use to size a room to a target cover count, or to
sanity-check a supplied plan.

- Area per seat (whole dining room, incl. circulation): fine dining **18–20 sq ft / 1.7–1.9 m²**;
  casual **15–18 sq ft / 1.4–1.7 m²**; fast-casual **12–15 sq ft / 1.1–1.4 m²**; counter
  service **11–14 sq ft / 1.0–1.3 m²**.
- Per-person table width: **24 in (~600 mm)** casual; **28–30 in (~700–760 mm)** fine dining.
- Main service/circulation aisle: **44–48 in (~1100–1200 mm)** in practice (36 in / 915 mm is
  the ADA legal floor). Secondary between-table aisle: **24–36 in (~600–900 mm)**.
- Full server access between table edges: **~60 in (~1500 mm)** for full-service layouts.

## Hospitality tag structure (AIA-style starting point)
- `A-WALL-INTR` (interior walls), `A-WALL-EXTR` (exterior), `A-FLOR` (floors), `A-DOOR`,
  `A-GLAZ` (glazing/windows), `A-FURN` (furniture), `A-FFE` (fixtures/equipment),
  `A-CLNG` (ceiling).
- Tags go on **groups/components**; raw geometry stays **Untagged** (mirrors the Trimble
  `sketchup-assembly-structure` convention — tag the parent, not the loose faces).

---

## Sources (verified 2026-06-09; primary standards + industry design guides)
- ADA 2010 Standards — U.S. Access Board chapters: Accessible Routes (403/404), Clear Floor &
  Turning Space (304/305), Built-In Elements & Counters (902/904), Plumbing (604).
  https://www.access-board.gov/ada/ · https://www.ada.gov/law-and-regs/design-standards/2010-stds/
- ADA §403.5.1 clear width, §604 water closet clearance, §904 counters — corada / ada-compliance.com
  references. https://www.corada.com/documents/2010ADAStandards/403-5-1
- AS 1428.1-2009 *Design for access and mobility* — door 850 mm, path 1000 mm, turning
  1540 × 2070 mm, ramp 1:14, accessible sanitary 1900 × 2300 mm.
  https://store.standards.org.au/product/as-1428-1-2009 (figures via published summaries:
  ansr.net.au, Johnson Suisse "Understanding AS1428", accessed.com.au).
- Restaurant space planning (per-seat area, aisle/table spacing) — Toast, Superior Seating,
  gofoodservice ADA seating guide. https://pos.toasttab.com/blog/on-the-line/average-restaurant-square-footage
- Hotel guest-room areas by tier — Mingsun, SiteMinder, Innowave hospitality design guides.
  https://www.siteminder.com/r/hotel-room-sizes/

> NOTE: AS 1428.1 itself is paywalled (Standards Australia). Figures above are cross-checked
> against multiple published access-consultant summaries; confirm against the purchased
> standard before any spec-grade use (that is v2 `spatial-compliance`, not this suite).
