#!/usr/bin/env python3
"""
assemble_prompt.py — Build the Universal Prompt for Nano Banana from template + inputs.

Ensures consistent layout-lock phrasing and one-to-one mapping to the template in
knowledge/materials-semantic-template.md.

Usage:
  python scripts/assemble_prompt.py \
    --venue-type "full-service restaurant dining room" \
    --materials "herringbone oak, honed travertine feature wall, walnut joinery, brass pendants" \
    --context "a lively neighbourhood bistro on a brick corner" \
    --lighting "warm early-evening light, glowing filament pendants" \
    --narrative "diners mid-meal, servers moving through" \
    --tier iterate \
    [--extra-lock "table positions"] \
    [--plan-to-iso]

Output:
  - model name (nano_banana_2 or nano_banana_pro)
  - full prompt with layout-lock appended verbatim
"""

import argparse
import sys


LAYOUT_LOCK_STANDARD = (
    "Preserve the exact spatial layout, wall boundaries, and camera perspective of the "
    "reference image; don't guess on the material set, look at my lines."
)

LAYOUT_LOCK_PLAN_TO_ISO = (
    "Convert my plan into a 60-degree 3D isometric view while keeping the exact layout "
    "proportions and relationships; don't guess on the material set, look at my lines."
)


def assemble_prompt(
    venue_type: str,
    materials: str,
    context: str,
    lighting: str,
    narrative: str,
    tier: str = "iterate",
    extra_lock: str = "",
    plan_to_iso: bool = False,
) -> tuple[str, str]:
    """
    Build the Universal Prompt from the five anchors + layout-lock.

    Args:
        venue_type: e.g. "full-service restaurant dining room"
        materials: e.g. "herringbone oak, honed travertine, walnut joinery, brass pendants"
        context: e.g. "a lively neighbourhood bistro on a brick corner"
        lighting: e.g. "warm early-evening light, glowing filament pendants"
        narrative: e.g. "diners mid-meal, servers moving through"
        tier: "iterate" (nano_banana_2) or "pro" (nano_banana_pro)
        extra_lock: optional extra elements to lock e.g. "table positions, bar and railing"
        plan_to_iso: use the plan-to-iso layout-lock variant

    Returns:
        (model_name, prompt) tuple
    """

    # Map tier to model name
    model_map = {
        "iterate": "nano_banana_2",
        "2": "nano_banana_2",
        "pro": "nano_banana_pro",
        "final": "nano_banana_pro",
    }
    model_name = model_map.get(tier.lower(), "nano_banana_2")

    # Choose layout-lock variant
    layout_lock = LAYOUT_LOCK_PLAN_TO_ISO if plan_to_iso else LAYOUT_LOCK_STANDARD

    # Append extra lock elements if provided
    if extra_lock:
        # Insert the extra elements right after "exact spatial layout"
        if plan_to_iso:
            layout_lock = (
                "Convert my plan into a 60-degree 3D isometric view while keeping the exact layout "
                "proportions and relationships, " + extra_lock.lower() + "; "
                "don't guess on the material set, look at my lines."
            )
        else:
            layout_lock = (
                "Preserve the exact spatial layout, " + extra_lock.lower() + ", wall boundaries, "
                "and camera perspective of the reference image; don't guess on the material set, "
                "look at my lines."
            )

    # Build the prompt
    prompt = (
        f"A professional interior photograph of a {venue_type}. {materials}. {context}. "
        f"{lighting}. {narrative}. Render in 4K, photorealistic. {layout_lock}"
    )

    return model_name, prompt


def main():
    parser = argparse.ArgumentParser(
        description="Assemble a Universal Prompt for Nano Banana rendering.",
    )
    parser.add_argument("--venue-type", required=True, help="Venue type (e.g. 'boutique hotel king guest suite')")
    parser.add_argument("--materials", required=True, help="Material palette (exact finishes)")
    parser.add_argument("--context", required=True, help="Site/context and surroundings")
    parser.add_argument("--lighting", required=True, help="Lighting/atmosphere and mood")
    parser.add_argument("--narrative", required=True, help="Narrative/story — how the space is used")
    parser.add_argument(
        "--tier",
        default="iterate",
        choices=["iterate", "2", "pro", "final"],
        help="Nano Banana tier: iterate (nano_banana_2) or pro (nano_banana_pro)",
    )
    parser.add_argument(
        "--extra-lock",
        default="",
        help="Extra elements to lock (e.g. 'table positions, bar and railing')",
    )
    parser.add_argument(
        "--plan-to-iso",
        action="store_true",
        help="Use the plan-to-isometric layout-lock variant",
    )
    parser.add_argument(
        "--json",
        action="store_true",
        help="Output as JSON {model, prompt}",
    )

    args = parser.parse_args()

    model_name, prompt = assemble_prompt(
        venue_type=args.venue_type,
        materials=args.materials,
        context=args.context,
        lighting=args.lighting,
        narrative=args.narrative,
        tier=args.tier,
        extra_lock=args.extra_lock,
        plan_to_iso=args.plan_to_iso,
    )

    if args.json:
        import json
        print(json.dumps({"model": model_name, "prompt": prompt}))
    else:
        print(f"Model: {model_name}\n")
        print(f"Prompt:\n{prompt}")

    return 0


if __name__ == "__main__":
    sys.exit(main())
