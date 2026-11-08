"""VoiceForge configuration and low-resource profile.

Everything in VoiceForge is tuned for machines with NO GPU and as little
as 4 GB of RAM:

* Engines run one at a time and are unloaded between stages, so peak
  memory is the largest single stage, never the sum of all stages.
* Training uses batch size 1 with gradient checkpointing and saves
  weights-only checkpoints.
* Long audio is converted in chunks (default 30 s) joined with short
  crossfades, so peak RAM stays flat no matter how long the song is.
* Source separation (Demucs) runs with a small segment window.
* Text-to-speech uses Kokoro (an 82M-parameter ONNX model) which is
  fast on a plain CPU and is chained into the voice converter.

Engine locations are resolved in this order:
  1. Environment variables VF_APPLIO_DIR, VF_SVC_PYTHON, VF_TTS_PYTHON
  2. ~/.voiceforge/engines/... (created by scripts/setup_engines.sh)
"""
from __future__ import annotations

import os
from pathlib import Path

HOME = Path.home()
VF_HOME = Path(os.environ.get("VF_HOME", HOME / ".voiceforge"))
ENGINES_DIR = VF_HOME / "engines"
MODELS_DIR = Path(os.environ.get("VF_MODELS_DIR", VF_HOME / "models"))
WORK_DIR = Path(os.environ.get("VF_WORK_DIR", VF_HOME / "work"))

# --- Low-resource profile -------------------------------------------------
TRAIN_BATCH_SIZE = 1
TRAIN_SAMPLE_RATE = 40000
CHUNK_SECONDS = 30           # conversion chunk length
CROSSFADE_SECONDS = 0.25     # crossfade when joining chunks
DEMUCS_SEGMENT = 7           # seconds per separation window
MIN_SAMPLE_SECONDS = 30      # minimum voice sample to train
GOOD_SAMPLE_SECONDS = 300    # recommended: 5 minutes
BEST_SAMPLE_SECONDS = 600    # ideal: 10 minutes
MASTER_FILTER = (
    "highpass=f=70,"
    "equalizer=f=3000:t=q:w=1.2:g=2.5,"
    "equalizer=f=6500:t=q:w=1.4:g=2,"
    "acompressor=threshold=0.6:ratio=2.5:attack=10:release=180,"
    "loudnorm=I=-14:TP=-1.5:LRA=11"
)


def applio_dir() -> Path:
    env = os.environ.get("VF_APPLIO_DIR")
    if env:
        return Path(env)
    return ENGINES_DIR / "applio"


def svc_python() -> str:
    """Python of the voice-conversion engine venv (torch, demucs, applio)."""
    env = os.environ.get("VF_SVC_PYTHON")
    if env:
        return env
    for cand in [
        ENGINES_DIR / "svc-venv" / "Scripts" / "python.exe",
        ENGINES_DIR / "svc-venv" / "bin" / "python",
        ENGINES_DIR / "svc-venv" / "python.exe",
    ]:
        if cand.exists():
            return str(cand)
    return str(ENGINES_DIR / "svc-venv" / ("Scripts/python.exe" if os.name == "nt" else "bin/python"))


def tts_python() -> str:
    """Python of the TTS engine venv (kokoro). Falls back to svc python."""
    env = os.environ.get("VF_TTS_PYTHON")
    if env:
        return env
    for cand in [
        ENGINES_DIR / "tts-venv" / "Scripts" / "python.exe",
        ENGINES_DIR / "tts-venv" / "bin" / "python",
        ENGINES_DIR / "tts-venv" / "python.exe",
    ]:
        if cand.exists():
            return str(cand)
    return svc_python()


def offline_env() -> dict:
    """Environment that keeps every engine fully offline and quiet."""
    env = dict(os.environ)
    # Some systems mount /tmp as a tiny tmpfs. Engines must never depend
    # on it: all temp files live on the data volume under the work dir.
    tmp_dir = WORK_DIR / "tmp"
    tmp_dir.mkdir(parents=True, exist_ok=True)
    env.update({
        "TMPDIR": str(tmp_dir),
        "HF_HUB_OFFLINE": "1",
        "TRANSFORMERS_OFFLINE": "1",
        "HF_HUB_DISABLE_TELEMETRY": "1",
        "GRADIO_ANALYTICS_ENABLED": "No",
        "TOKENIZERS_PARALLELISM": "false",
        # Keep BLAS/thread pools from ballooning RAM on small machines.
        "OMP_NUM_THREADS": os.environ.get("OMP_NUM_THREADS", "2"),
    })
    return env


def model_files(name: str) -> tuple[Path, Path]:
    """Return (pth, index) for a trained voice in the VoiceForge model store."""
    d = MODELS_DIR / name
    pths = sorted(d.glob("*.pth"))
    idxs = sorted(d.glob("*.index"))
    if not pths or not idxs:
        raise FileNotFoundError(
            f"Voice model '{name}' is not trained yet (looked in {d})."
        )
    return pths[-1], idxs[-1]


def applio_model_files(name: str) -> tuple[Path, Path]:
    """Return (pth, index) from Applio's own logs folder for a voice."""
    d = applio_dir() / "logs" / name
    pths = sorted(d.glob(f"{name}_*e_*s.pth"))
    idxs = sorted(d.glob("*.index"))
    if not pths or not idxs:
        raise FileNotFoundError(f"No trained Applio model for '{name}' in {d}.")
    return pths[-1], idxs[-1]


def resolve_model(name: str) -> tuple[Path, Path]:
    try:
        return applio_model_files(name)
    except FileNotFoundError:
        return model_files(name)
