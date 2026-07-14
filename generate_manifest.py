"""
Scans the /images/<category> folders and writes images/manifest.json,
which the website reads to automatically build its galleries.

Usage:
    python3 generate_manifest.py

Run this any time you add, remove, or rename photos in the images folders,
then refresh the site in your browser (or Live Server will refresh itself
if "Auto Save" / auto-refresh is on).
"""

import json
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
IMAGE_DIR = os.path.join(BASE_DIR, "images")

CATEGORIES = [
    "hero", "about",
    "portrait", "weddings", "landscape", "street", "fashion", "product",
]

VALID_EXT = (".jpg", ".jpeg", ".png", ".webp")


def natural_key(name):
    # Sorts "photo2" before "photo10" instead of alphabetically
    import re
    return [int(t) if t.isdigit() else t.lower() for t in re.split(r"(\d+)", name)]


def main():
    manifest = {}

    for cat in CATEGORIES:
        folder = os.path.join(IMAGE_DIR, cat)
        if not os.path.isdir(folder):
            manifest[cat] = []
            continue

        files = [
            f for f in os.listdir(folder)
            if f.lower().endswith(VALID_EXT) and not f.startswith(".")
        ]
        files.sort(key=natural_key)
        manifest[cat] = [f"images/{cat}/{f}" for f in files]

    out_path = os.path.join(IMAGE_DIR, "manifest.json")
    with open(out_path, "w") as f:
        json.dump(manifest, f, indent=2)

    print("Manifest updated -> images/manifest.json\n")
    for cat, files in manifest.items():
        print(f"  {cat:<10} {len(files)} image(s)")
    print("\nRefresh the site in your browser to see the changes.")


if __name__ == "__main__":
    main()
