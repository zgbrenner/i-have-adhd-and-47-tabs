#!/usr/bin/env python3
from __future__ import annotations

import shutil
import zipfile
from pathlib import Path, PurePosixPath

ROOT = Path(__file__).resolve().parents[1]
NAME = "i-have-adhd-and-47-tabs"
SOURCE = ROOT / NAME
DIST = ROOT / "dist"
OUTPUT = DIST / f"{NAME}.zip"
FIXED_TIME = (2026, 7, 21, 0, 0, 0)


def main() -> None:
    if not (SOURCE / "SKILL.md").is_file():
        raise SystemExit(f"Missing {SOURCE / 'SKILL.md'}")

    DIST.mkdir(parents=True, exist_ok=True)
    if OUTPUT.exists():
        OUTPUT.unlink()

    files = sorted(path for path in SOURCE.rglob("*") if path.is_file())
    with zipfile.ZipFile(OUTPUT, "w", compression=zipfile.ZIP_DEFLATED, compresslevel=9) as archive:
        for path in files:
            relative = PurePosixPath(NAME) / PurePosixPath(path.relative_to(SOURCE).as_posix())
            info = zipfile.ZipInfo(str(relative), FIXED_TIME)
            info.compress_type = zipfile.ZIP_DEFLATED
            info.external_attr = 0o644 << 16
            archive.writestr(info, path.read_bytes())

    shutil.copy2(OUTPUT, ROOT / f"{NAME}.zip")
    print(f"Built {OUTPUT.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
