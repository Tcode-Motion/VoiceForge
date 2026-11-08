"""Vocal separation with small windows (low RAM)."""
from __future__ import annotations

from pathlib import Path

from . import config, engines


def separate(src: str | Path, out_dir: str | Path | None = None) -> tuple[Path, Path]:
    src = Path(src)
    out = Path(out_dir) if out_dir else config.WORK_DIR / "separate" / src.stem
    return engines.demucs_two_stems(src, out)
