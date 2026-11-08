#!/usr/bin/env bash
# VoiceForge engine setup: builds the three local engines under
# ~/.voiceforge/engines. Everything is CPU-only and open source.
# Needs: git, python3.12, ffmpeg. Downloads happen only in this step;
# VoiceForge itself runs fully offline afterwards.
set -e
ENG="$HOME/.voiceforge/engines"
mkdir -p "$ENG"
cd "$ENG"

echo "[1/4] Applio (RVC training + conversion)"
[ -d applio ] || git clone --depth 1 https://github.com/IAHispano/Applio.git applio

echo "[2/4] Engine venv (torch CPU, demucs, applio deps)"
[ -d svc-venv ] || python3 -m venv svc-venv
./svc-venv/bin/pip install --upgrade pip
./svc-venv/bin/pip install torch torchaudio --index-url https://download.pytorch.org/whl/cpu
./svc-venv/bin/pip install demucs soundfile numpy scipy faiss-cpu onnxruntime
( cd applio && ../svc-venv/bin/pip install -r requirements.txt )

echo "[3/4] TTS venv (Kokoro, 82M ONNX model, fast on CPU)"
[ -d tts-venv ] || python3 -m venv tts-venv
./tts-venv/bin/pip install --upgrade pip
./tts-venv/bin/pip install kokoro soundfile

echo "[4/4] Applio pretrained assets (hubert, rmvpe, base voices)"
( cd applio && ../svc-venv/bin/python core.py prerequisites )

echo "Done. Engines live in $ENG"
