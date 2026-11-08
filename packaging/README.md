# Packaging VoiceForge Desktop

VoiceForge Desktop bundles the entire studio (HTML/JS frontend, audio pipeline, and Python runtime) into a standalone native desktop application for Windows, macOS, and Linux.

The packaging engine uses PyInstaller with `packaging/voiceforge.spec` and entry point `packaging/launcher.py`. When `pywebview` is present, it renders in an embedded native window; otherwise it falls back smoothly to your default web browser.

---

## Local Build Instructions

### Prerequisites
Install packaging dependencies:
```bash
pip install pyinstaller pywebview pillow
```

### Build Commands

#### Windows:
```powershell
pyinstaller packaging\voiceforge.spec --noconfirm
Compress-Archive -Path dist\VoiceForge.exe -DestinationPath VoiceForge-Windows.zip
```

#### macOS:
```bash
pyinstaller packaging/voiceforge.spec --noconfirm
cd dist && zip -qr ../VoiceForge-macOS.zip VoiceForge.app
```

#### Linux:
```bash
pyinstaller packaging/voiceforge.spec --noconfirm
cd dist && tar -czf ../VoiceForge-Linux.tar.gz VoiceForge
```

---

## Automated CI/CD Builds
GitHub Actions automatically builds desktop binaries for Windows, macOS, and Linux on every release branch or tag push, and attaches them directly to the GitHub Release.
