"""Train a voice model with the low-RAM profile.

Defaults that let training survive on ~8 GB RAM with no GPU:
batch size 1, gradient checkpointing, rmvpe pitch (lighter than
crepe), weights saved regularly so an interruption never loses
everything, and only the newest full checkpoint kept.
"""
from __future__ import annotations

from pathlib import Path

from . import config, engines


def train(name: str, dataset_dir: Path, epochs: int = 60) -> tuple[Path, Path]:
    cores = "2"
    engines.applio(
        "preprocess", "--model-name", name, "--dataset-path", str(dataset_dir),
        "--sample-rate", str(config.TRAIN_SAMPLE_RATE), "--cpu-cores", cores,
        "--cut-preprocess", "Simple", "--chunk-len", "3.0",
        "--overlap-len", "0.0", "--normalization-mode", "post",
    )
    engines.applio(
        "extract", "--model-name", name, "--f0-method", "rmvpe",
        "--cpu-cores", cores, "--sample-rate", str(config.TRAIN_SAMPLE_RATE),
        "--embedder-model", "contentvec", "--include-mutes", "2",
    )
    engines.applio(
        "train", "--model-name", name, "--vocoder", "HiFi-GAN",
        "--checkpointing", "--save-every-epoch", "5", "--save-only-latest",
        "--save-every-weights", "--total-epoch", str(epochs),
        "--sample-rate", str(config.TRAIN_SAMPLE_RATE),
        "--batch-size", str(config.TRAIN_BATCH_SIZE), "--pretrained",
    )
    engines.applio("index", "--model-name", name, "--index-algorithm", "Auto")
    pth, idx = config.applio_model_files(name)
    # Copy into the VoiceForge model store for portability.
    store = config.MODELS_DIR / name
    store.mkdir(parents=True, exist_ok=True)
    import shutil
    shutil.copy2(pth, store / pth.name)
    shutil.copy2(idx, store / idx.name)
    print(f"Voice '{name}' trained: {pth.name}")
    return store / pth.name, store / idx.name
