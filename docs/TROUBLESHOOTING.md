# Troubleshooting

## "Voice sample too short"
Training needs at least 30 seconds of one person's voice in total.
Add more recordings, or record a longer one. 5 to 10 minutes gives a
clearly better voice.

## Training stops or the computer runs out of memory
VoiceForge already uses the safe profile (batch size 1, gradient
checkpointing, weights saved regularly). If it still stops:
- Close other heavy programs during training.
- Lower the epochs and resume later; weights are saved as it goes.
- Make sure nothing else is converting at the same time. One engine
  at a time is the design.

## The converted voice sounds like the original singer
Raise Voice strength (index rate) toward 1.0. Lower values keep more
of the source singer.

## Words sound unclear
Raise Clarity protect toward 0.3 to 0.4. Very high values can make
the voice sound thinner, so move in small steps.

## Engines not found
Run the engine setup script for your operating system:
- Windows (PowerShell): `powershell -ExecutionPolicy Bypass -File scripts\setup_engines.ps1`
- Windows (Command Prompt): `scripts\setup_engines.bat`
- macOS / Linux: `bash scripts/setup_engines.sh`

Or point VoiceForge at an existing installation via environment variables:
- `VF_APPLIO_DIR`: folder containing Applio's `core.py`
- `VF_SVC_PYTHON`: path to the engine Python executable (torch, demucs, applio)
- `VF_TTS_PYTHON`: path to the Kokoro TTS Python executable

## FFmpeg not found or audio decoding fails
VoiceForge uses FFmpeg for audio mastering and stem conversion:
- Windows: `winget install Gyan.FFmpeg` or download from ffmpeg.org and add the `bin` folder to your PATH.
- macOS: `brew install ffmpeg`
- Ubuntu / Debian: `sudo apt install ffmpeg`
- Arch Linux: `sudo pacman -S ffmpeg`

## Mobile companion cannot connect to the studio
- Verify both your computer and phone are connected to the same local Wi-Fi network.
- Start the studio with: `voiceforge gui --host 0.0.0.0 --port 8760`
- Find your computer's local IP address (`ipconfig` on Windows or `ip a` / `ifconfig` on Linux/macOS, e.g. `192.168.1.15`).
- Ensure port 8760 is not blocked by Windows Defender Firewall or macOS firewall.
- On the phone app, enter `http://<YOUR_COMPUTER_IP>:8760` and tap Connect.

## macOS: "App is damaged or cannot be opened"
Because pre-built binaries are not notarized with an Apple Developer certificate, macOS Gatekeeper may show a warning:
- Right-click (or Control-click) `VoiceForge.app` and choose **Open**.
- Or run in terminal: `xattr -cr /Applications/VoiceForge.app`

## Everything is slow
That is the CPU trade-off. Short clips convert in a few minutes on the
reference machine. Separation and conversion times grow linearly with
song length; training is the slowest part (about 1.5 minutes per
round for a small dataset).
