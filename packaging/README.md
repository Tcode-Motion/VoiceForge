# Packaging

Desktop apps are built with PyInstaller from
`packaging/voiceforge.spec` and the entry point
`packaging/launcher.py` (desktop GUI, web GUI fallback).

Local build:

```bash
pip install pyinstaller
pyinstaller packaging/voiceforge.spec --noconfirm
```

CI builds Windows, macOS and Linux on every release branch push and
attaches the packaged apps to the GitHub release automatically.
