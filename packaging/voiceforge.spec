# PyInstaller spec for the VoiceForge desktop app.
# Build: pyinstaller packaging/voiceforge.spec (from the repo root)
from pathlib import Path

root = Path(SPECPATH).parent

# The desktop app embeds the web studio with pywebview. Collect it
# when it is installed; without it the app falls back to the browser.
try:
    from PyInstaller.utils.hooks import collect_all

    wv_datas, wv_binaries, wv_hidden = collect_all("webview")
except Exception:
    wv_datas, wv_binaries, wv_hidden = [], [], []

a = Analysis(
    [str(root / "packaging" / "launcher.py")],
    pathex=[str(root / "src")],
    binaries=wv_binaries,
    datas=[(str(root / "assets" / "logo.png"), "assets")] + wv_datas,
    hiddenimports=["voiceforge.webgui", "voiceforge.desktop"] + wv_hidden,
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
