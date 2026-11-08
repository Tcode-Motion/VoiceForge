# VoiceForge engine setup for Windows (PowerShell)
# Builds the three local engines under ~/.voiceforge/engines
# Everything is CPU-only and open source.
# Requirements: git, python (3.10-3.12), ffmpeg

$ErrorActionPreference = "Stop"
$EnginesDir = Join-Path $HOME ".voiceforge\engines"
if (-not (Test-Path $EnginesDir)) {
    New-Item -ItemType Directory -Path $EnginesDir -Force | Out-Null
}
Set-Location $EnginesDir

Write-Host "[1/4] Cloning Applio (RVC training + conversion)..." -ForegroundColor Cyan
if (-not (Test-Path "applio")) {
    git clone --depth 1 https://github.com/IAHispano/Applio.git applio
}

Write-Host "[2/4] Setting up Engine venv (torch CPU, demucs, applio dependencies)..." -ForegroundColor Cyan
if (-not (Test-Path "svc-venv")) {
    python -m venv svc-venv
}
$SvcPip = Join-Path $EnginesDir "svc-venv\Scripts\pip.exe"
$SvcPython = Join-Path $EnginesDir "svc-venv\Scripts\python.exe"

& $SvcPip install --upgrade pip
& $SvcPip install torch torchaudio --index-url https://download.pytorch.org/whl/cpu
& $SvcPip install demucs soundfile numpy scipy faiss-cpu onnxruntime
Push-Location "applio"
& $SvcPip install -r requirements.txt
Pop-Location

Write-Host "[3/4] Setting up TTS venv (Kokoro ONNX, fast on CPU)..." -ForegroundColor Cyan
if (-not (Test-Path "tts-venv")) {
    python -m venv tts-venv
}
$TtsPip = Join-Path $EnginesDir "tts-venv\Scripts\pip.exe"
& $TtsPip install --upgrade pip
& $TtsPip install kokoro soundfile

Write-Host "[4/4] Downloading Applio pretrained assets (hubert, rmvpe)..." -ForegroundColor Cyan
Push-Location "applio"
& $SvcPython core.py prerequisites
Pop-Location

Write-Host "Done! Engines are installed in $EnginesDir" -ForegroundColor Green

