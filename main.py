#!/usr/bin/env python3
"""Copy the bundled front-page image to the output directory.

The entry image is drawn once, ahead of time, by draw_frontpage.py and
shipped in this repository as entry.png. This program only copies it to
$MAKEFUN_OUTPUT_DIR/entry.png (default /output), checks that the bytes
are a whole PNG, and confirms the copy matches the source byte for byte,
so both graded runs write identical output.

Standard library only; no network access.
"""

import hashlib
import os
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
SOURCE = HERE / "entry.png"
PNG_MAGIC = b"\x89PNG\r\n\x1a\n"


def digest(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def main() -> int:
    out_dir = Path(os.environ.get("MAKEFUN_OUTPUT_DIR", "/output"))
    out_dir.mkdir(parents=True, exist_ok=True)

    data = SOURCE.read_bytes()
    if data[:8] != PNG_MAGIC:
        print("error: entry.png does not start with the PNG magic bytes",
              file=sys.stderr)
        return 1

    target = out_dir / "entry.png"
    target.write_bytes(data)

    copied = target.read_bytes()
    if digest(copied) != digest(data):
        print("error: copied file differs from entry.png", file=sys.stderr)
        return 1

    print(f"wrote {target}: {len(copied)} bytes, sha256 {digest(copied)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
