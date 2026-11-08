"""Small ffmpeg-based audio helpers (no heavy dependencies)."""
from __future__ import annotations

import subprocess
from pathlib import Path


def run(cmd: list[str], **kw) -> subprocess.CompletedProcess:
    return subprocess.run(cmd, check=True, capture_output=True, text=True, **kw)


def duration(path: str | Path) -> float:
    out = run([
        "ffprobe", "-v", "error", "-show_entries", "format=duration",
        "-of", "csv=p=0", str(path),
    ]).stdout.strip()
    return float(out)


def to_wav(src: str | Path, dst: str | Path, sr: int = 44100) -> Path:
    dst = Path(dst)
    run(["ffmpeg", "-y", "-v", "error", "-i", str(src),
         "-ar", str(sr), "-ac", "1", str(dst)])
    return dst


def slice_audio(src: str | Path, start: float, length: float,
                dst: str | Path) -> Path:
    dst = Path(dst)
    run(["ffmpeg", "-y", "-v", "error", "-ss", str(start), "-t", str(length),
         "-i", str(src), str(dst)])
    return dst


def master(src: str | Path, dst: str | Path, chain: str) -> Path:
    """Apply the clarity mastering chain and write a 44.1 kHz file."""
    dst = Path(dst)
    run(["ffmpeg", "-y", "-v", "error", "-i", str(src),
         "-af", chain, "-ar", "44100", str(dst)])
    return dst


def to_mp3(src: str | Path, dst: str | Path, bitrate: str = "192k") -> Path:
    dst = Path(dst)
    run(["ffmpeg", "-y", "-v", "error", "-i", str(src),
         "-codec:a", "libmp3lame", "-b:a", bitrate, str(dst)])
    return dst


def join_crossfade(parts: list[Path], dst: str | Path,
                   crossfade: float = 0.25) -> Path:
    """Join wav parts with short crossfades (keeps joins click-free)."""
    dst = Path(dst)
    if len(parts) == 1:
        run(["ffmpeg", "-y", "-v", "error", "-i", str(parts[0]), str(dst)])
        return dst
    cmd = ["ffmpeg", "-y", "-v", "error"]
    for p in parts:
        cmd += ["-i", str(p)]
    filt = ""
    last = "[0:a]"
    for i in range(1, len(parts)):
        out = f"[x{i}]"
        filt += f"{last}[{i}:a]acrossfade=d={crossfade}:c1=tri:c2=tri{out};"
        last = out
    filt = filt.rstrip(";")
    cmd += ["-filter_complex", filt, "-map", last, str(dst)]
    run(cmd)
    return dst
