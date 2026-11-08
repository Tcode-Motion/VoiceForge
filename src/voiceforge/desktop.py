"""VoiceForge desktop app: the web studio in a native window.

The desktop app is not a separate interface. It starts the exact
same web studio the browser shows and opens it inside a native app
window (pywebview: Edge WebView2 on Windows, WKWebView on macOS,
WebKitGTK on Linux). Same design, same pages, pixel for pixel,
because it is literally the same page.

If pywebview is not installed, the studio opens in the default
browser instead, which shows the identical interface. Install the
windowed version with:  pip install "voiceforge[desktop]"
"""
from __future__ import annotations

import socket
import time
import webbrowser

HOST = "127.0.0.1"
PORT = 8760


def _port_busy(host: str, port: int) -> bool:
    s = socket.socket()
    s.settimeout(0.3)
    try:
        return s.connect_ex((host, port)) == 0
    finally:
        s.close()


def launch() -> None:
    from .webgui import start_server

    url = f"http://{HOST}:{PORT}"
    server = None
    if not _port_busy(HOST, PORT):
        server = start_server(HOST, PORT)
        time.sleep(0.4)

    try:
        import webview
    except ImportError:
        print("pywebview is not installed, opening the studio in your "
              "browser instead. Same interface, in a browser tab.")
        print('For the app window: pip install "voiceforge[desktop]"')
        webbrowser.open(url)
        try:
            while True:
                time.sleep(3600)
        except KeyboardInterrupt:
            pass
        finally:
            if server is not None:
                server.shutdown()
        return

    webview.create_window(
        "VoiceForge - CPU Voice Cloning Studio",
        url,
        width=1240,
        height=840,
        min_size=(980, 640),
        background_color="#0a0a0b",
    )
    webview.start()
    if server is not None:
        server.shutdown()
