#!/usr/bin/env python3
"""
validate_export.py — Check that a SketchUp line-work export is ready for Nano Banana.

Validates format, resolution, aspect ratio, opacity, and presence of line-work content
(not bare clay). Ensures the export passes the hard requirements before rendering.

Usage:
  python scripts/validate_export.py export.png --tier pro --aspect 16:9
  python scripts/validate_export.py hero.png --tier iterate --aspect 1:1

Exit codes:
  0 = PASS (export ready)
  1 = FAIL (export not ready; report which checks failed)
"""

import argparse
import sys
from pathlib import Path

try:
    from PIL import Image
    import numpy as np
except ImportError:
    print("ERROR: PIL and numpy required. Install: pip install Pillow numpy")
    sys.exit(1)


def validate_format(image_path: Path) -> tuple[bool, str]:
    """Check that the file is PNG or JPG (flat raster, not SVG/PDF)."""
    suffix = image_path.suffix.lower()
    if suffix not in [".png", ".jpg", ".jpeg"]:
        return False, f"Format {suffix} not supported; use PNG or JPG"
    return True, "Format: OK"


def validate_opacity(image: Image.Image) -> tuple[bool, str]:
    """Check that the image is opaque (not alpha-channel)."""
    if image.mode == "RGBA":
        # Check if alpha is actually used (not all 255)
        if image.getextrema()[3] != (255, 255):  # Alpha channel is not solid
            return False, "Image has transparency (alpha channel). Export as flat PNG (no alpha)."
    return True, "Opacity: solid background (OK)"


def validate_resolution(image: Image.Image, tier: str) -> tuple[bool, str]:
    """Check minimum resolution for the tier."""
    width, height = image.size
    long_edge = max(width, height)

    min_long_edge = 2048 if tier == "pro" else 1024
    if long_edge < min_long_edge:
        return False, f"Resolution too low: {long_edge}px (min {min_long_edge}px for {tier} tier)"

    return True, f"Resolution: {width}×{height} (OK for {tier} tier)"


def validate_aspect(image: Image.Image, aspect_str: str) -> tuple[bool, str]:
    """Check that the image aspect matches the declared aspect."""
    width, height = image.size
    declared_a, declared_b = map(int, aspect_str.split(":"))

    actual_ratio = width / height if height != 0 else 0
    expected_ratio = declared_a / declared_b if declared_b != 0 else 0

    # Allow 1% tolerance
    if abs(actual_ratio - expected_ratio) > 0.01:
        return False, (
            f"Aspect mismatch: {width}:{height} ~= {actual_ratio:.2f}, "
            f"but you declared {aspect_str} ~= {expected_ratio:.2f}"
        )

    return True, f"Aspect: {aspect_str} (OK)"


def validate_line_content(image: Image.Image) -> tuple[bool, str]:
    """
    Check that the image contains line-work structure (not bare clay or blank).

    A line-work export has defined edges: high variance in local pixel neighborhoods,
    indicating crisp lines rather than smooth gradients (clay).
    Blank/near-white images have very low variance.
    """

    # Convert to grayscale for edge detection
    gray = image.convert("L")
    pixels = np.array(gray)

    # Check mean brightness to reject blank/very light images
    mean_brightness = np.mean(pixels)
    if mean_brightness > 240:
        return False, "Image reads as blank or near-white (no visible line-work)"

    # Compute Laplacian edge strength (high where there are edges)
    # Simple approximation: compute local variance
    if pixels.shape[0] > 2 and pixels.shape[1] > 2:
        # Approximate edge strength via horizontal/vertical differences
        dh = np.abs(np.diff(pixels, axis=0)).mean()
        dv = np.abs(np.diff(pixels, axis=1)).mean()
        edge_strength = (dh + dv) / 2
    else:
        edge_strength = 0

    # A line-work export should have noticeable edges (edge_strength > ~20);
    # bare clay is smooth (< 10).
    if edge_strength < 10:
        return (
            False,
            f"Image reads as smooth/clay (edge strength {edge_strength:.1f}, expected >20). "
            "Apply crisp outlines and re-export."
        )

    return True, f"Line-content: OK (edge strength {edge_strength:.1f})"


def main():
    parser = argparse.ArgumentParser(
        description="Validate a SketchUp line-work export before Nano Banana rendering."
    )
    parser.add_argument("image_path", type=Path, help="Path to the export PNG/JPG")
    parser.add_argument(
        "--tier",
        default="pro",
        choices=["iterate", "pro"],
        help="Nano Banana tier (iterate=nano_banana_2, pro=nano_banana_pro)",
    )
    parser.add_argument(
        "--aspect",
        default="16:9",
        help="Expected aspect ratio (e.g. 16:9, 1:1, 4:3)",
    )
    parser.add_argument(
        "--verbose",
        action="store_true",
        help="Print detailed results for each check",
    )

    args = parser.parse_args()

    # Verify file exists
    if not args.image_path.exists():
        print(f"ERROR: File not found: {args.image_path}")
        return 1

    # Load image
    try:
        image = Image.open(args.image_path)
    except Exception as e:
        print(f"ERROR: Could not open image: {e}")
        return 1

    # Run checks
    checks = [
        ("Format", validate_format(args.image_path)),
        ("Opacity", validate_opacity(image)),
        ("Resolution", validate_resolution(image, args.tier)),
        ("Aspect", validate_aspect(image, args.aspect)),
        ("Line-content", validate_line_content(image)),
    ]

    # Report
    all_pass = True
    for name, (passed, message) in checks:
        status = "✓ PASS" if passed else "✗ FAIL"
        print(f"{status}: {name} — {message}")
        if not passed:
            all_pass = False

    print()
    if all_pass:
        print(f"✓ PASS: {args.image_path.name} is ready for rendering on {args.tier} tier.")
        return 0
    else:
        print(f"✗ FAIL: {args.image_path.name} is not ready. Fix the issues above and re-export.")
        return 1


if __name__ == "__main__":
    sys.exit(main())
