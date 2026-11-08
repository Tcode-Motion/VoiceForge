"""Sing mode: put a song's singing into a trained voice.

Pipeline: separate the song into vocals + instrumental, convert only
the vocals (chunked, low RAM), then either return clean vocals or mix
the converted voice back over the instrumental.
"""
from __future__ import annotations

from pathlib import Path

from . import audioutil, config
from .convert import convert_file
from .separate import separate


def sing(song: str | Path, model_name: str, dst: str | Path,
         with_music: bool = False, index_rate: float = 1.0,
         protect: float = 0.25) -> Path:
    dst = Path(dst)
    vocals, backing = separate(song)
    conv = config.WORK_DIR / "sing_vocals.wav"
    convert_file(vocals, model_name, conv,
                 index_rate=index_rate, protect=protect)
    if not with_music:
        return conv if dst == conv else _move(conv, dst)
    mixed = config.WORK_DIR / "sing_mix.wav"
    from .audioutil import run
    run(["ffmpeg", "-y", "-v", "error", "-i", str(conv), "-i", str(backing),
         "-filter_complex", "[0:a][1:a]amix=inputs=2:duration=first:weights=1 0.7",
         str(mixed)])
    audioutil.master(mixed, dst, config.MASTER_FILTER)
    return dst


def _move(src: Path, dst: Path) -> Path:
    import shutil
    dst.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(src, dst)
    return dst
