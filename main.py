#!/usr/bin/env python3
"""Copy the bundled newspaper front page to the grader's output directory.

The entry image (entry.png) ships in this repository next to this script.
This program simply copies it to $MAKEFUN_OUTPUT_DIR/entry.png
(default /output/entry.png). Standard library only, no network access,
deterministic: the same input bytes are written on every run.
"""

import os
import shutil
import sys

ENTRY_NAME = "entry.png"


def main() -> int:
    here = os.path.dirname(os.path.abspath(__file__))
    source = os.path.join(here, ENTRY_NAME)
    if not os.path.isfile(source):
        print(f"error: bundled image not found: {source}", file=sys.stderr)
        return 1
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
    dest = os.path.join(out_dir, ENTRY_NAME)
    try:
        os.makedirs(out_dir, exist_ok=True)
        shutil.copyfile(source, dest)
    except OSError as exc:
        print(f"error: could not write {dest}: {exc}", file=sys.stderr)
        return 1
    # Sanity-check the copy: same size as the bundled image, and a valid PNG.
    if os.path.getsize(dest) != os.path.getsize(source):
        print(f"error: size mismatch after copy: {dest}", file=sys.stderr)
        return 1
    with open(dest, "rb") as fh:
        if fh.read(8) != b"\x89PNG\r\n\x1a\n":
            print(f"error: {dest} is not a PNG file", file=sys.stderr)
            return 1
    print(f"wrote {dest} ({os.path.getsize(dest)} bytes)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
