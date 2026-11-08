"""Thin, memory-careful wrappers around the three engines.

Each engine runs as its own short-lived process and exits before the
next stage starts, which keeps peak RAM at one engine at a time.

* Applio (RVC)  : training + voice conversion
* Demucs        : vocal / instrumental separation (htdemucs)
* Kokoro        : text-to-speech front end for the Speak mode
"""
from __future__ import annotations

import subprocess
import sys
from pathlib import Path

from . import config


def _run(cmd: list[str], cwd: str | None = None) -> None:
    print("  $", " ".join(str(c) for c in cmd[:6]), "...")
    proc = subprocess.run([str(c) for c in cmd], cwd=cwd, env=config.offline_env())
    if proc.returncode != 0:
        raise RuntimeError(f"Engine failed ({proc.returncode}): {cmd[1] if len(cmd)>1 else cmd}")


def applio(*args: str) -> None:
    _run([config.svc_python(), "core.py", *args], cwd=str(config.applio_dir()))


def demucs_two_stems(src: Path, out_dir: Path) -> tuple[Path, Path]:
    """Separate into (vocals, no_vocals) with a small segment window."""
    out_dir.mkdir(parents=True, exist_ok=True)
    _run([config.svc_python(), "-m", "demucs", "--two-stems", "vocals",
          "-n", "htdemucs", "--segment", str(config.DEMUCS_SEGMENT),
          "-o", str(out_dir), str(src)])
    base = out_dir / "htdemucs" / Path(src).stem
    return base / "vocals.wav", base / "no_vocals.wav"


KOKORO_SNIPPET = r"""
import sys, soundfile as sf
from kokoro import KPipeline
text, voice, out = sys.argv[1], sys.argv[2], sys.argv[3]
pipe = KPipeline(lang_code="a")
audio = None
for _, _, a in pipe(text, voice=voice, speed=1.0):
    audio = a if audio is None else __import__("numpy").concatenate([audio, a])
sf.write(out, audio, 24000)
print("tts ok:", out)
"""


def kokoro_tts(text: str, out: Path, voice: str = "af_heart") -> Path:
    out.parent.mkdir(parents=True, exist_ok=True)
    proc = subprocess.run(
        [config.tts_python(), "-c", KOKORO_SNIPPET, text, voice, str(out)],
        env=config.offline_env(), capture_output=True, text=True)
    if proc.returncode != 0:
        raise RuntimeError("Kokoro TTS failed: " + proc.stderr[-400:])
    return out
