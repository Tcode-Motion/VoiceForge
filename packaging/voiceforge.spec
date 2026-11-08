# PyInstaller spec for the VoiceForge desktop app.
# Build: pyinstaller packaging/voiceforge.spec (from the repo root)
from pathlib import Path

root = Path(SPECPATH).parent

a = Analysis(
    [str(root / "packaging" / "launcher.py")],
    pathex=[str(root / "src")],
    binaries=[],
    datas=[(str(root / "assets" / "logo.png"), "assets")],
    hiddenimports=["voiceforge.webgui", "voiceforge.desktop"],
    hookspath=[],
    runtime_hooks=[],
    excludes=[],
    noarchive=False,
)
pyz = PYZ(a.pure)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.datas,
    [],
    name="VoiceForge",
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=False,
    console=False,
    icon=str(root / "assets" / "logo.png"),
)
app = BUNDLE(
    exe,
    name="VoiceForge.app",
    icon=str(root / "assets" / "logo.png"),
    bundle_identifier="dev.voiceforge.app",
)
