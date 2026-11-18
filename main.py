#!/usr/bin/env python3
"""Place the day's picture where the judge reads it.

The entry is one image. art/entry.html is its design source and entry.png is
the rendered 1024x1024 frame that sums up 18 November 2026: the Shenzhen
summit, strikes in the Gulf, the Kerch bridge, Nvidia's quarter and the day's
markets. The program's only job is to put those exact bytes at
<output>/entry.png, identically on both runs.
"""

import os
import shutil
import sys
from pathlib import Path

IMAGE = "entry.png"
PNG_MAGIC = b"\x89PNG\r\n\x1a\n"
MAX_BYTES = 1_048_576


def check_image(path: Path) -> str | None:
    """Say what is wrong with the picture, or None when the gate would take it."""
    data = path.read_bytes()
    if not data.startswith(PNG_MAGIC):
        return f"{path.name} is not a PNG (first bytes {data[:8]!r})"
    if len(data) > MAX_BYTES:
        return f"{path.name} is {len(data)} bytes, over the {MAX_BYTES} the bounty takes"
    width = int.from_bytes(data[16:20], "big")
    height = int.from_bytes(data[20:24], "big")
    if width > 1024 or height > 1024:
        return f"{path.name} is {width}x{height}, over 1024 on a side"
    return None


def output_dir() -> Path:
    """The directory the run writes to: MAKEFUN_OUTPUT_DIR, else /output."""
    configured = os.environ.get("MAKEFUN_OUTPUT_DIR")
    return Path(configured) if configured else Path("/output")


def main() -> int:
    root = Path(__file__).resolve().parent
    source = root / IMAGE
    if not source.is_file():
        print(f"{IMAGE} is missing beside {Path(__file__).name}", file=sys.stderr)
        return 1
    problem = check_image(source)
    if problem:
        print(problem, file=sys.stderr)
        return 1

    destination = output_dir() / IMAGE
    destination.parent.mkdir(parents=True, exist_ok=True)
    shutil.copyfile(source, destination)

    if destination.read_bytes() != source.read_bytes():
        print(f"{destination} does not hold the image's bytes", file=sys.stderr)
        return 1

    print(f"{destination}: {destination.stat().st_size} bytes")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
