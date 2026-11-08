"""Speak mode: type text (lyrics, a message, anything) and hear it in
a trained voice. Kokoro TTS speaks first, then the converter moves the
voice onto your trained model. Honest scope: this speaks text; making
a *melody* from lyrics alone needs a source tune (use Sing mode)."""
from __future__ import annotations

from pathlib import Path

from . import config, engines
from .convert import convert_file


def speak(text: str, model_name: str, dst: str | Path,
          base_voice: str = "af_heart", index_rate: float = 1.0) -> Path:
    raw = config.WORK_DIR / "tts_raw.wav"
    engines.kokoro_tts(text, raw, voice=base_voice)
    return convert_file(raw, model_name, dst, index_rate=index_rate)
