"""Chunked voice conversion: the low-RAM core of VoiceForge.

The input is split into 30-second chunks. Each chunk is converted in
its own engine process, so the engine's memory is freed after every
chunk and peak RAM stays flat for a 1-minute clip or a 1-hour song.
Chunks are joined with 0.25 s crossfades and finished with the clarity
mastering chain.
"""
from __future__ import annotations

from pathlib import Path

from . import audioutil, config, engines


def convert_file(src: str | Path, model_name: str, dst: str | Path,
                 index_rate: float = 1.0, protect: float = 0.25,
                 pitch: int = 0, chunk_seconds: int = config.CHUNK_SECONDS,
                 master: bool = True) -> Path:
    src = Path(src)
    dst = Path(dst)
    pth, idx = config.resolve_model(model_name)
    work = config.WORK_DIR / "convert"
    work.mkdir(parents=True, exist_ok=True)
    wav = work / f"{src.stem}_44k.wav"
    audioutil.to_wav(src, wav, sr=44100)
    dur = audioutil.duration(wav)
    parts: list[Path] = []
    t = 0.0
    i = 0
    while t < dur:
        seg = min(float(chunk_seconds), dur - t)
        chunk = work / f"chunk_{i:03d}.wav"
        out = work / f"chunk_{i:03d}_vc.wav"
        audioutil.slice_audio(wav, t, seg, chunk)
        engines.applio(
            "infer", "--input-path", str(chunk), "--output-path", str(out),
            "--pth-path", str(pth), "--index-path", str(idx),
            "--index-rate", str(index_rate), "--protect", str(protect),
            "--pitch", str(pitch), "--f0-method", "rmvpe",
            "--export-format", "WAV",
        )
        parts.append(out)
        t += seg
        i += 1
    joined = work / f"{src.stem}_joined.wav"
    audioutil.join_crossfade(parts, joined, config.CROSSFADE_SECONDS)
    if master:
        audioutil.master(joined, dst, config.MASTER_FILTER)
    else:
        audioutil.to_wav(joined, dst, sr=44100)
    print(f"Converted {dur:.0f}s in {len(parts)} chunk(s) -> {dst}")
    return dst
