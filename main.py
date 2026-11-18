#!/usr/bin/env python3
"""Entry program for news-image-20261118 (Python 3.13, standard library only).

The day's front page is baked into entry.png at build time: the grader runs
this program with no network, so the image it copies is the image the judge
sees. Copy it to the output directory the grader provides.
"""
import hashlib
import os
import shutil
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
SOURCE = HERE / "entry.png"
PNG_MAGIC = b"\x89PNG\r\n\x1a\n"


def main() -> int:
    out_dir = Path(os.environ.get("MAKEFUN_OUTPUT_DIR", "/output"))
    out_dir.mkdir(parents=True, exist_ok=True)
    data = SOURCE.read_bytes()
    if not data.startswith(PNG_MAGIC):
        print("entry.png is not a PNG file", file=sys.stderr)
        return 1
    target = out_dir / "entry.png"
    shutil.copyfile(SOURCE, target)
    # The grader runs the program twice and requires identical bytes both
    # times: confirm the copy matches the source before reporting success.
    if hashlib.sha256(target.read_bytes()).hexdigest() != \
            hashlib.sha256(data).hexdigest():
        print("copied entry.png does not match the source", file=sys.stderr)
        return 1
    print(f"wrote {target} ({len(data)} bytes)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
