"""VoiceForge command line.

Examples:
  voiceforge add-voice tanmoy sample1.wav sample2.wav
  voiceforge train tanmoy --epochs 60
  voiceforge convert song.mp3 --voice tanmoy -o song_mine.wav
  voiceforge sing song.mp3 --voice tanmoy --with-music -o cover.wav
  voiceforge speak "Hello, this is my voice" --voice tanmoy -o hello.wav
  voiceforge separate song.mp3
  voiceforge voices
  voiceforge gui        # web GUI on http://127.0.0.1:8760
  voiceforge desktop    # desktop GUI (Tkinter)
  voiceforge tui        # terminal menu
"""
from __future__ import annotations

import argparse
import sys
from pathlib import Path

from . import __version__, config


def _add_common(p):
    p.add_argument("--voice", required=True, help="trained voice name")
    p.add_argument("--index-rate", type=float, default=1.0,
                   help="how strongly the output copies the trained voice (0-1)")
    p.add_argument("--protect", type=float, default=0.25,
                   help="protects clear consonants / pronunciation (0-0.5)")


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(prog="voiceforge",
                                 description="CPU-first voice cloning studio")
    ap.add_argument("--version", action="version", version=f"VoiceForge {__version__}")
    sub = ap.add_subparsers(dest="cmd", required=True)

    p = sub.add_parser("add-voice", help="prepare a dataset from recordings")
    p.add_argument("name")
    p.add_argument("files", nargs="+")

    p = sub.add_parser("train", help="train a voice model (low-RAM profile)")
    p.add_argument("name")
    p.add_argument("--epochs", type=int, default=60)
    p.add_argument("--dataset", help="existing dataset folder (skip add-voice)")

    p = sub.add_parser("convert", help="convert any audio into a trained voice")
    p.add_argument("input")
    p.add_argument("-o", "--output", required=True)
    _add_common(p)
    p.add_argument("--pitch", type=int, default=0)

    p = sub.add_parser("sing", help="make a song sing in a trained voice")
    p.add_argument("input")
    p.add_argument("-o", "--output", required=True)
    p.add_argument("--with-music", action="store_true",
                   help="mix the converted voice back over the instrumental")
    _add_common(p)

    p = sub.add_parser("speak", help="speak typed text in a trained voice")
    p.add_argument("text")
    p.add_argument("-o", "--output", required=True)
    p.add_argument("--voice", required=True)
    p.add_argument("--base-voice", default="af_heart")

    p = sub.add_parser("separate", help="split a song into vocals + instrumental")
    p.add_argument("input")

    sub.add_parser("voices", help="list trained voices")
    sub.add_parser("gui", help="start the web GUI")
    sub.add_parser("desktop", help="start the desktop GUI")
    sub.add_parser("tui", help="start the terminal menu")

    args = ap.parse_args(argv)
    try:
        if args.cmd == "add-voice":
            from .dataset import prepare
            prepare(args.name, [Path(f) for f in args.files])
        elif args.cmd == "train":
            from .dataset import prepare  # noqa: F401  (kept for symmetry)
            from .train import train
            ds = Path(args.dataset) if args.dataset else (
                config.WORK_DIR / "datasets" / args.name)
            if not ds.exists():
                print("No dataset found. Run add-voice first.", file=sys.stderr)
                return 2
            train(args.name, ds, epochs=args.epochs)
        elif args.cmd == "convert":
            from .convert import convert_file
            out = convert_file(args.input, args.voice, args.output,
                               index_rate=args.index_rate,
                               protect=args.protect, pitch=args.pitch)
            print(out)
        elif args.cmd == "sing":
            from .sing import sing
            out = sing(args.input, args.voice, args.output,
                       with_music=args.with_music,
                       index_rate=args.index_rate, protect=args.protect)
            print(out)
        elif args.cmd == "speak":
            from .speak import speak
            out = speak(args.text, args.voice, args.output,
                        base_voice=args.base_voice)
            print(out)
        elif args.cmd == "separate":
            from .separate import separate
            v, b = separate(args.input)
            print("vocals:", v)
            print("instrumental:", b)
        elif args.cmd == "voices":
            logs = config.applio_dir() / "logs"
            names = sorted(d.name for d in logs.iterdir()
                           if d.is_dir() and list(d.glob("*.pth"))) \
                if logs.exists() else []
            store = sorted(d.name for d in config.MODELS_DIR.iterdir()) \
                if config.MODELS_DIR.exists() else []
            all_names = sorted(set(names) | set(store))
            print("\n".join(all_names) if all_names else "No trained voices yet.")
        elif args.cmd == "gui":
            from .webgui import serve
            serve()
        elif args.cmd == "desktop":
            from .desktop import launch
            launch()
        elif args.cmd == "tui":
            from .tui import menu
            menu()
    except (ValueError, FileNotFoundError, RuntimeError) as e:
        print("Error:", e, file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
