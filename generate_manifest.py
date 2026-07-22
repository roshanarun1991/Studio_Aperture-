"""
Scans the /images/<category> folders, compresses/resizes each photo into
a web-optimized copy, and writes images/manifest.json (which the website
reads to build its galleries and hero slideshow automatically).

Usage:
    python3 generate_manifest.py

Run this any time you add, remove, or rename photos in the images folders,
then refresh the site in your browser.

Requires Pillow for image optimization (one-time install):
    pip install Pillow
If Pillow isn't installed, the script still works — it just skips
optimization and uses your original files directly (slower to load, but
nothing breaks).
"""

import json
import os
import re

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
IMAGE_DIR = os.path.join(BASE_DIR, "images")
OPTIMIZED_DIR = os.path.join(IMAGE_DIR, "_optimized")

CATEGORIES = [
    "hero", "about",
    "portrait", "weddings", "landscape", "street", "fashion", "product",
]

VALID_EXT = (".jpg", ".jpeg", ".png", ".webp", ".gif", ".avif")

# Common camera/phone formats that browsers can't display directly.
# iPhones save as HEIC by default — this is the #1 reason photos "don't show up."
UNSUPPORTED_EXT = (
    ".heic", ".heif", ".tif", ".tiff", ".bmp",
    ".cr2", ".cr3", ".nef", ".arw", ".dng", ".raf", ".rw2",
)

# Longest edge in pixels for each category — plenty sharp for web display
# while cutting file size dramatically versus a raw camera photo.
MAX_DIMENSIONS = {
    "hero": 2000,       # full-bleed background, needs to stay large
    "about": 1400,
    "portrait": 1600,
    "weddings": 1600,
    "landscape": 1600,
    "street": 1600,
    "fashion": 1600,
    "product": 1600,
}
JPEG_QUALITY = 82

try:
    from PIL import Image, ImageOps
    HAVE_PILLOW = True
except ImportError:
    HAVE_PILLOW = False


def natural_key(name):
    # Sorts "photo2" before "photo10" instead of alphabetically
    return [int(t) if t.isdigit() else t.lower() for t in re.split(r"(\d+)", name)]


def optimize_image(src_path, dst_path, max_dim):
    """Resize + compress one image. Returns (original_bytes, new_bytes)."""
    original_size = os.path.getsize(src_path)

    with Image.open(src_path) as img:
        img = ImageOps.exif_transpose(img)  # respect phone camera rotation
        if img.mode in ("RGBA", "P"):
            img = img.convert("RGB")

        w, h = img.size
        longest = max(w, h)
        if longest > max_dim:
            scale = max_dim / longest
            img = img.resize((round(w * scale), round(h * scale)), Image.LANCZOS)

        img.save(dst_path, "JPEG", quality=JPEG_QUALITY, optimize=True)

    return original_size, os.path.getsize(dst_path)


def main():
    manifest = {}
    skipped_by_cat = {}
    total_before = 0
    total_after = 0

    if not HAVE_PILLOW:
        print("⚠️  Pillow isn't installed, so photos will NOT be compressed —")
        print("   the site will use your original files as-is (slower to load).")
        print("   Fix: run  pip install Pillow  then re-run this script.\n")

    for cat in CATEGORIES:
        folder = os.path.join(IMAGE_DIR, cat)
        if not os.path.isdir(folder):
            manifest[cat] = []
            continue

        all_files = [f for f in os.listdir(folder) if not f.startswith(".")]
        valid_files = [f for f in all_files if f.lower().endswith(VALID_EXT)]
        skipped = [f for f in all_files if f.lower().endswith(UNSUPPORTED_EXT)]
        valid_files.sort(key=natural_key)

        if skipped:
            skipped_by_cat[cat] = skipped

        if not HAVE_PILLOW:
            manifest[cat] = [f"images/{cat}/{f}" for f in valid_files]
            continue

        out_folder = os.path.join(OPTIMIZED_DIR, cat)
        os.makedirs(out_folder, exist_ok=True)

        # Clear old optimized files so removed/renamed photos don't linger
        for f in os.listdir(out_folder):
            os.remove(os.path.join(out_folder, f))

        optimized_paths = []
        max_dim = MAX_DIMENSIONS.get(cat, 1600)

        for i, filename in enumerate(valid_files, start=1):
            src = os.path.join(folder, filename)
            dst_name = f"{i:02d}.jpg"
            dst = os.path.join(out_folder, dst_name)
            try:
                before, after = optimize_image(src, dst, max_dim)
                total_before += before
                total_after += after
                optimized_paths.append(f"images/_optimized/{cat}/{dst_name}")
            except Exception as e:
                print(f"   ! Couldn't process images/{cat}/{filename}: {e}")

        manifest[cat] = optimized_paths

    out_path = os.path.join(IMAGE_DIR, "manifest.json")
    with open(out_path, "w") as f:
        json.dump(manifest, f, indent=2)

    print("Manifest updated -> images/manifest.json\n")
    for cat, files in manifest.items():
        print(f"  {cat:<10} {len(files)} image(s)")

    if HAVE_PILLOW and total_before:
        saved_pct = round((1 - total_after / total_before) * 100)
        print(f"\nCompressed {total_before/1_000_000:.1f} MB -> "
              f"{total_after/1_000_000:.1f} MB ({saved_pct}% smaller)")

    if skipped_by_cat:
        print("\n⚠️  SKIPPED — these files exist but browsers can't display their format:")
        for cat, files in skipped_by_cat.items():
            for f in files:
                print(f"   - images/{cat}/{f}")
        print("\n   Convert them to .jpg or .png and re-run this script. If these came")
        print("   from an iPhone: Settings > Camera > Formats > \"Most Compatible\"")
        print("   makes future photos save as .jpg automatically.")

    print("\nRefresh the site in your browser to see the changes.")
    print("Remember: if this site is on GitHub Pages, you must also commit and")
    print("push the images/ folder (including images/_optimized/ and")
    print("manifest.json) — running this script only updates your local files.")


if __name__ == "__main__":
    main()
