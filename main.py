"""Publish this repository's entry image for make.fun's ai-excited-01 bounty.

Run it from the repository root:

    python3 main.py

entry.png is copied byte for byte to every destination that will take it, in
turn: /output/entry.png first (the path the judge reads), then output/entry.png
and entry_out.png beside the repository root as fallbacks. A destination that
refuses the write is reported and skipped, so one locked path never stops the
others, and every run produces the same bytes.

Exit status: 0 when at least one destination took the copy, 1 when none did,
2 when entry.png is missing or empty. Standard library only.
"""

from __future__ import annotations

import shutil
import sys
from pathlib import Path
from typing import Final, Sequence

SOURCE_NAME: Final[str] = "entry.png"
DESTINATIONS: Final[tuple[str, ...]] = (
    "/output/entry.png",
    "output/entry.png",
    "entry_out.png",
)


def source_path() -> Path:
    """The entry image sitting beside this script."""
    return Path(__file__).resolve().parent / SOURCE_NAME


def is_readable(path: Path) -> bool:
    """True when path is a file holding at least one byte."""
    return path.is_file() and path.stat().st_size > 0


def publish(source: Path, destination: str) -> bool:
    """Copy source to destination; report a refusal instead of raising."""
    target = Path(destination)
    try:
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(source, target)
    except OSError as error:
        reason = error.strerror or str(error)
        print(f"skipped {destination}: {reason}", file=sys.stderr)
        return False
    print(f"wrote {destination}")
    return True


def publish_all(source: Path, destinations: Sequence[str]) -> int:
    """Try every destination in order; how many copies landed."""
    written = 0
    for destination in destinations:
        if publish(source, destination):
            written += 1
    return written


def main() -> int:
    source = source_path()
    if not is_readable(source):
        print(f"{SOURCE_NAME} is missing or empty", file=sys.stderr)
        return 2
    if publish_all(source, DESTINATIONS) == 0:
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
