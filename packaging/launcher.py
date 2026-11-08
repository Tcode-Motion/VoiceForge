"""VoiceForge app launcher used by the packaged builds.

Opens the desktop GUI. If no display is available it falls back to
the web GUI on http://127.0.0.1:8760.
"""
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))


def main() -> None:
    try:
        from voiceforge.desktop import launch
        launch()
    except Exception:
        from voiceforge.webgui import serve
        serve()


if __name__ == "__main__":
    main()
