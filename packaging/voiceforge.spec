# PyInstaller spec for the VoiceForge desktop app.
# Build: pyinstaller packaging/voiceforge.spec (from the repo root)
import sys
from pathlib import Path

root = Path(SPECPATH).parent

# The desktop app embeds the web studio with pywebview. Collect it
# when it is installed; without it the app falls back to the browser.
try:
    from PyInstaller.utils.hooks import collect_all

    wv_datas, wv_binaries, wv_hidden = collect_all("webview")
except Exception:
    wv_datas, wv_binaries, wv_hidden = [], [], []

icon_png = root / "assets" / "logo.png"
icon_ico = root / "assets" / "logo.ico"
icon_icns = root / "assets" / "logo.icns"

exe_icon = None
bundle_icon = None

if sys.platform.startswith("win"):
    exe_icon = str(icon_ico) if icon_ico.exists() else (str(icon_png) if icon_png.exists() else None)
elif sys.platform.startswith("darwin"):
    bundle_icon = str(icon_icns) if icon_icns.exists() else (str(icon_png) if icon_png.exists() else None)
    exe_icon = bundle_icon
else:
    exe_icon = str(icon_png) if icon_png.exists() else None

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
    icon=exe_icon,
)
app = BUNDLE(
    exe,
    name="VoiceForge.app",
    icon=bundle_icon,
    bundle_identifier="dev.voiceforge.app",
)
