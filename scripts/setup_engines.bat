@echo off
setlocal enabledelayedexpansion
echo VoiceForge Engine Setup for Windows
set "ENG=%USERPROFILE%\.voiceforge\engines"
if not exist "%ENG%" mkdir "%ENG%"
cd /d "%ENG%"

echo [1/4] Cloning Applio...
if not exist applio git clone --depth 1 https://github.com/IAHispano/Applio.git applio

echo [2/4] Setting up svc-venv...
if not exist svc-venv python -m venv svc-venv
call svc-venv\Scripts\pip.exe install --upgrade pip
call svc-venv\Scripts\pip.exe install torch torchaudio --index-url https://download.pytorch.org/whl/cpu
call svc-venv\Scripts\pip.exe install demucs soundfile numpy scipy faiss-cpu onnxruntime
cd applio
call ..\svc-venv\Scripts\pip.exe install -r requirements.txt
cd ..

echo [3/4] Setting up tts-venv...
if not exist tts-venv python -m venv tts-venv
call tts-venv\Scripts\pip.exe install --upgrade pip
call tts-venv\Scripts\pip.exe install kokoro soundfile

echo [4/4] Downloading pretrained assets...
cd applio
call ..\svc-venv\Scripts\python.exe core.py prerequisites
cd ..

echo Done! Engines installed in %ENG%
