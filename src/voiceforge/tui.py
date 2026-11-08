"""VoiceForge terminal menu (TUI). Pure standard library."""
from __future__ import annotations

from pathlib import Path

BANNER = r"""
 __   __   _          ___                      
 \ \ / /__(_)__ ___  | __|__ _ _ __ _ ___      
  \ V / _ \ / _/ -_) | _/ _ \ '_/ _` / -_)     
   \_/\___/_\__\___| |_|\___/_| \__, \___|     
                                  |___/  v1.0
  CPU-first voice cloning. No GPU needed.
"""


def _ask(prompt: str, default: str = "") -> str:
    s = input(f"{prompt} [{default}]: " if default else f"{prompt}: ").strip()
    return s or default


def menu() -> None:
    print(BANNER)
    while True:
        print("""
  1) Add a voice sample (prepare dataset)
  2) Train a voice
  3) Convert audio into a voice
  4) Sing: make a song in a voice
  5) Speak: type text, hear it in a voice
  6) Separate a song (vocals / instrumental)
  7) List trained voices
  0) Quit
""")
        choice = input("Choose: ").strip()
        try:
            if choice == "0":
                print("Bye.")
                return
            elif choice == "1":
                from .dataset import prepare
                name = _ask("Voice name")
                files = _ask("Recording files (space separated)").split()
                prepare(name, [Path(f) for f in files])
            elif choice == "2":
                from .train import train
                from . import config
                name = _ask("Voice name")
                epochs = int(_ask("Epochs", "60"))
                train(name, config.WORK_DIR / "datasets" / name, epochs=epochs)
            elif choice == "3":
                from .convert import convert_file
                src = _ask("Input audio")
                voice = _ask("Voice name")
                out = _ask("Output file", "converted.wav")
                convert_file(src, voice, out)
                print("Done:", out)
            elif choice == "4":
                from .sing import sing
                src = _ask("Song file")
                voice = _ask("Voice name")
                out = _ask("Output file", "song_mine.wav")
                music = _ask("Mix back over music? (y/n)", "n").lower() == "y"
                sing(src, voice, out, with_music=music)
                print("Done:", out)
            elif choice == "5":
                from .speak import speak
                text = _ask("Text to speak")
                voice = _ask("Voice name")
                out = _ask("Output file", "speak.wav")
                speak(text, voice, out)
                print("Done:", out)
            elif choice == "6":
                from .separate import separate
                v, b = separate(_ask("Song file"))
                print("vocals:", v)
                print("instrumental:", b)
            elif choice == "7":
                from .cli import main as cli_main
                cli_main(["voices"])
            else:
                print("Unknown choice.")
        except (ValueError, FileNotFoundError, RuntimeError) as e:
            print("Error:", e)
