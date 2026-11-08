"""Prepare a training dataset from one or more voice recordings.

Rules (shown in the app as well):
* Minimum total voice: 30 seconds. Recordings under this are rejected
  with a clear message instead of training a useless model.
* Recommended: 5 minutes. Ideal: 10 minutes, in small chunks.
* Recordings are loudness-normalised and cut into 3-second slices,
  which is what the RVC trainer consumes best on low-RAM machines.
"""
from __future__ import annotations

from pathlib import Path

from . import audioutil, config


def total_seconds(files: list[str | Path]) -> float:
    return sum(audioutil.duration(f) for f in files)


def prepare(name: str, files: list[str | Path]) -> Path:
    total = total_seconds(files)
    if total < config.MIN_SAMPLE_SECONDS:
        raise ValueError(
            f"Voice sample too short: {total:.0f}s. "
            f"Minimum is {config.MIN_SAMPLE_SECONDS}s; "
            f"{config.GOOD_SAMPLE_SECONDS//60} minutes is recommended, "
            f"{config.BEST_SAMPLE_SECONDS//60} minutes is ideal."
        )
    ds_dir = config.WORK_DIR / "datasets" / name
    ds_dir.mkdir(parents=True, exist_ok=True)
    merged = config.WORK_DIR / f"{name}_merged.wav"
    parts = []
    for i, f in enumerate(files):
        w = config.WORK_DIR / f"{name}_in{i}.wav"
        audioutil.to_wav(f, w, sr=config.TRAIN_SAMPLE_RATE)
        parts.append(w)
    if len(parts) == 1:
        merged = parts[0]
    else:
        audioutil.join_crossfade(parts, merged, crossfade=0.05)
    # Gentle loudness normalisation, then slice into 3 s chunks.
    norm = config.WORK_DIR / f"{name}_norm.wav"
    audioutil.master(merged, norm, "loudnorm=I=-16:TP=-2:LRA=11")
    dur = audioutil.duration(norm)
    n = 0
    t = 0.0
    while t + 1.0 < dur:
        seg = min(3.0, dur - t)
        audioutil.slice_audio(norm, t, seg, ds_dir / f"{name}_{n:04d}.wav")
        n += 1
        t += 3.0
    print(f"Dataset '{name}': {total:.0f}s of voice -> {n} slices in {ds_dir}")
    return ds_dir
