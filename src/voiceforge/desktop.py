"""VoiceForge desktop GUI v2 (Tkinter + ttk).

Professional layout: dark sidebar with section navigation, a header
bar, focused pages for each job, sliders for voice strength and
clarity, and a status bar. Jobs run in background threads; engines
still run one at a time so memory stays low.
"""
from __future__ import annotations

import contextlib
import io
import queue
import threading
import tkinter as tk
from tkinter import filedialog, messagebox, scrolledtext, ttk

BG = "#0a0a0b"
PANEL = "#101012"
CARD = "#141416"
FIELD = "#0d0d0f"
LINE = "#2a2a2e"
TXT = "#f5f5f4"
DIM = "#a3a3ab"
ACC = "#f5f5f4"
ACC2 = "#c8f542"
OK = "#34d399"


class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("VoiceForge - CPU Voice Cloning Studio")
        self.geometry("900x640")
        self.minsize(820, 560)
        self.configure(bg=BG)
        self.q: queue.Queue[str] = queue.Queue()
        self.sample_files: list[str] = []
        self.job_files: dict[str, str] = {}
        self._style()
        self._build()
        self.after(150, self._drain)

    # -- theme ---------------------------------------------------------
    def _style(self):
        st = ttk.Style(self)
        st.theme_use("clam")
        st.configure("TFrame", background=BG)
        st.configure("Panel.TFrame", background=PANEL)
        st.configure("Card.TFrame", background=CARD)
        st.configure("TLabel", background=BG, foreground=TXT, font=("Segoe UI", 10))
        st.configure("Panel.TLabel", background=PANEL, foreground=TXT)
        st.configure("Dim.TLabel", background=BG, foreground=DIM, font=("Segoe UI", 9))
        st.configure("PanelDim.TLabel", background=PANEL, foreground=DIM, font=("Segoe UI", 9))
        st.configure("Card.TLabel", background=CARD, foreground=TXT, font=("Segoe UI", 10))
        st.configure("CardDim.TLabel", background=CARD, foreground=DIM, font=("Segoe UI", 9))
        st.configure("H1.TLabel", background=PANEL, foreground=TXT, font=("Segoe UI", 17, "bold"))
        st.configure("H2.TLabel", background=BG, foreground=TXT, font=("Segoe UI", 15, "bold"))
        st.configure("CardH.TLabel", background=CARD, foreground=TXT, font=("Segoe UI", 12, "bold"))
        st.configure("TEntry", fieldbackground=FIELD, foreground=TXT,
                     bordercolor=LINE, padding=6)
        st.configure("Nav.TButton", background=PANEL, foreground=DIM,
                     font=("Segoe UI", 10), padding=(12, 8), borderwidth=0)
        st.map("Nav.TButton", background=[("active", "#151b36")])
        st.configure("NavActive.TButton", background="#26262b", foreground="#ffffff",
                     font=("Segoe UI", 10, "bold"), padding=(12, 8), borderwidth=0)
        st.configure("Accent.TButton", background=ACC, foreground="#0a0a0b",
                     font=("Segoe UI", 10, "bold"), padding=(14, 8), borderwidth=0)
        st.map("Accent.TButton", background=[("active", ACC2)])
        st.configure("TButton", background="#1c1c1f", foreground=TXT,
                     font=("Segoe UI", 10), padding=(12, 7), borderwidth=0)
        st.configure("TScale", background=CARD, troughcolor=FIELD)
        st.configure("Card.TCheckbutton", background=CARD, foreground=DIM,
                     font=("Segoe UI", 10))

    # -- layout --------------------------------------------------------
    def _build(self):
        side = ttk.Frame(self, style="Panel.TFrame", width=210)
        side.pack(side="left", fill="y")
        side.pack_propagate(False)
        ttk.Label(side, text="VoiceForge", style="H1.TLabel").pack(anchor="w", padx=16, pady=(16, 0))
        ttk.Label(side, text="CPU Voice Cloning Studio", style="PanelDim.TLabel").pack(anchor="w", padx=16)
        self.nav_btns: dict[str, ttk.Button] = {}
        pages = [("train", "Train voice"), ("sing", "Sing a song"),
                 ("speak", "Speak text"), ("convert", "Convert audio"),
                 ("separate", "Separate vocals"), ("voices", "My voices")]
        for key, label in pages:
            b = ttk.Button(side, text=label, style="Nav.TButton",
                           command=lambda k=key: self._show(k))
            b.pack(fill="x", padx=10, pady=2)
            self.nav_btns[key] = b
        ttk.Label(side, text="Offline engine ready\nNo GPU. Low RAM.\nYour voice stays on\nthis computer.\n\nv1.2.0",
                  style="PanelDim.TLabel").pack(side="bottom", anchor="w", padx=16, pady=14)

        right = ttk.Frame(self)
        right.pack(side="right", fill="both", expand=True)
        head = ttk.Frame(right)
        head.pack(fill="x", padx=20, pady=(14, 4))
        self.title_lbl = ttk.Label(head, text="Train voice", style="H2.TLabel")
        self.title_lbl.pack(side="left")
        ttk.Label(head, text="CPU mode   |   RAM safe", style="Dim.TLabel").pack(side="right")

        self.pages: dict[str, ttk.Frame] = {}
        content = ttk.Frame(right)
        content.pack(fill="both", expand=True, padx=20, pady=6)
        for key in ["train", "sing", "speak", "convert", "separate", "voices"]:
            f = ttk.Frame(content, style="Card.TFrame")
            f.place(relwidth=1, relheight=1)
            self.pages[key] = f
        self._page_train()
        self._page_sing()
        self._page_speak()
        self._page_convert()
        self._page_separate()
        self._page_voices()

        logf = ttk.Frame(right)
        logf.pack(fill="x", padx=20, pady=(2, 6))
        self.status = ttk.Label(logf, text="Idle. Jobs run one at a time to keep memory low.",
                                style="Dim.TLabel")
        self.status.pack(anchor="w")
        self.log = scrolledtext.ScrolledText(right, height=7, bg="#070708", fg="#c9c9cf",
                                             relief="flat", font=("Consolas", 9),
                                             insertbackground=TXT)
        self.log.pack(fill="x", padx=20, pady=(0, 12))
        self._show("train")

    def _show(self, key):
        titles = {"train": "Train voice", "sing": "Sing a song", "speak": "Speak text",
                  "convert": "Convert audio", "separate": "Separate vocals",
                  "voices": "My voices"}
        self.title_lbl.config(text=titles[key])
        self.pages[key].tkraise()
        for k, b in self.nav_btns.items():
            b.configure(style="NavActive.TButton" if k == key else "Nav.TButton")

    # -- small builders --------------------------------------------------
    def _card_label(self, parent, text, dim=False):
        ttk.Label(parent, text=text,
                  style="CardDim.TLabel" if dim else "Card.TLabel").pack(anchor="w", padx=16, pady=(10, 0))

    def _entry(self, parent, var):
        e = ttk.Entry(parent, textvariable=var)
        e.pack(fill="x", padx=16, pady=(2, 4))
        return e

    def _slider(self, parent, label, var, frm, to, fmt="{:.2f}"):
        row = ttk.Frame(parent, style="Card.TFrame")
        row.pack(fill="x", padx=16, pady=(4, 0))
        ttk.Label(row, text=label, style="CardDim.TLabel").pack(side="left")
        val = ttk.Label(row, text=fmt.format(var.get()), style="Card.TLabel")
        val.pack(side="right")
        s = ttk.Scale(parent, variable=var, from_=frm, to=to,
                      command=lambda v: val.config(text=fmt.format(float(v))))
        s.pack(fill="x", padx=16)
        return s

    # -- pages -----------------------------------------------------------
    def _page_train(self):
        f = self.pages["train"]
        self.v_name = tk.StringVar()
        self.v_epochs = tk.StringVar(value="60")
        ttk.Label(f, text="New voice", style="CardH.TLabel").pack(anchor="w", padx=16, pady=(14, 0))
        self._card_label(f, "Recordings of ONE person. Minimum 30 seconds total.\n5 minutes is good, 10 minutes is ideal.", dim=True)
        r = ttk.Frame(f, style="Card.TFrame"); r.pack(fill="x", padx=16, pady=(10, 0))
        ttk.Button(r, text="Choose recordings...", command=self._pick_samples).pack(side="left")
        self.sample_lbl = ttk.Label(r, text="No files chosen", style="CardDim.TLabel")
        self.sample_lbl.pack(side="left", padx=10)
        self._card_label(f, "Voice name")
        self._entry(f, self.v_name)
        self._card_label(f, "Training rounds (epochs)")
        self._entry(f, self.v_epochs)
        ttk.Button(f, text="Train this voice", style="Accent.TButton",
                   command=self._do_train).pack(anchor="w", padx=16, pady=14)

    def _page_sing(self):
        f = self.pages["sing"]
        self.s_voice = tk.StringVar()
        self.s_ir = tk.DoubleVar(value=1.0)
        self.s_pr = tk.DoubleVar(value=0.25)
        self.s_music = tk.BooleanVar(value=False)
        ttk.Label(f, text="Sing a song in a trained voice", style="CardH.TLabel").pack(anchor="w", padx=16, pady=(14, 0))
        r = ttk.Frame(f, style="Card.TFrame"); r.pack(fill="x", padx=16, pady=(10, 0))
        ttk.Button(r, text="Choose song...", command=lambda: self._pick_one("sing")).pack(side="left")
        self.sing_lbl = ttk.Label(r, text="No song chosen", style="CardDim.TLabel")
        self.sing_lbl.pack(side="left", padx=10)
        self._card_label(f, "Voice name")
        self._entry(f, self.s_voice)
        self._slider(f, "Voice strength (index rate)", self.s_ir, 0.0, 1.0)
        self._slider(f, "Clarity protect", self.s_pr, 0.0, 0.5)
        ttk.Checkbutton(f, text="Mix back over the music", variable=self.s_music,
                        style="Card.TCheckbutton").pack(anchor="w", padx=16, pady=(8, 0))
        ttk.Button(f, text="Make the song", style="Accent.TButton",
                   command=self._do_sing).pack(anchor="w", padx=16, pady=14)

    def _page_speak(self):
        f = self.pages["speak"]
        self.t_voice = tk.StringVar()
        ttk.Label(f, text="Speak text in a trained voice", style="CardH.TLabel").pack(anchor="w", padx=16, pady=(14, 0))
        self._card_label(f, "Text")
        self.text_box = tk.Text(f, height=5, bg=FIELD, fg=TXT, relief="flat",
                                font=("Segoe UI", 10), insertbackground=TXT)
        self.text_box.pack(fill="x", padx=16, pady=(2, 4))
        self._card_label(f, "Voice name")
        self._entry(f, self.t_voice)
        ttk.Button(f, text="Speak it", style="Accent.TButton",
                   command=self._do_speak).pack(anchor="w", padx=16, pady=14)

    def _page_convert(self):
        f = self.pages["convert"]
        self.c_voice = tk.StringVar()
        self.c_ir = tk.DoubleVar(value=1.0)
        self.c_pr = tk.DoubleVar(value=0.25)
        ttk.Label(f, text="Convert any audio into a trained voice", style="CardH.TLabel").pack(anchor="w", padx=16, pady=(14, 0))
        r = ttk.Frame(f, style="Card.TFrame"); r.pack(fill="x", padx=16, pady=(10, 0))
        ttk.Button(r, text="Choose audio...", command=lambda: self._pick_one("convert")).pack(side="left")
        self.conv_lbl = ttk.Label(r, text="No file chosen", style="CardDim.TLabel")
        self.conv_lbl.pack(side="left", padx=10)
        self._card_label(f, "Voice name")
        self._entry(f, self.c_voice)
        self._slider(f, "Voice strength (index rate)", self.c_ir, 0.0, 1.0)
        self._slider(f, "Clarity protect", self.c_pr, 0.0, 0.5)
        ttk.Button(f, text="Convert it", style="Accent.TButton",
                   command=self._do_convert).pack(anchor="w", padx=16, pady=14)

    def _page_separate(self):
        f = self.pages["separate"]
        ttk.Label(f, text="Separate vocals from music", style="CardH.TLabel").pack(anchor="w", padx=16, pady=(14, 0))
        r = ttk.Frame(f, style="Card.TFrame"); r.pack(fill="x", padx=16, pady=(10, 0))
        ttk.Button(r, text="Choose song...", command=lambda: self._pick_one("separate")).pack(side="left")
        self.sep_lbl = ttk.Label(r, text="No song chosen", style="CardDim.TLabel")
        self.sep_lbl.pack(side="left", padx=10)
        ttk.Button(f, text="Separate it", style="Accent.TButton",
                   command=self._do_separate).pack(anchor="w", padx=16, pady=14)

    def _page_voices(self):
        f = self.pages["voices"]
        ttk.Label(f, text="Trained voices on this computer", style="CardH.TLabel").pack(anchor="w", padx=16, pady=(14, 0))
        ttk.Button(f, text="Refresh list", command=self._do_voices).pack(anchor="w", padx=16, pady=10)
        self.voices_box = tk.Text(f, height=8, bg=FIELD, fg=TXT, relief="flat",
                                  font=("Consolas", 10))
        self.voices_box.pack(fill="x", padx=16)

    # -- plumbing --------------------------------------------------------
    def _drain(self):
        while not self.q.empty():
            msg = self.q.get()
            if msg == "__DONE__":
                self.status.config(text="Done.")
            elif msg.startswith("__VOICES__"):
                self.voices_box.delete("1.0", "end")
                self.voices_box.insert("end", msg[len("__VOICES__"):])
            else:
                self.log.insert("end", msg + "\n")
                self.log.see("end")
        self.after(150, self._drain)

    def _run(self, fn):
        self.status.config(text="Working... one engine at a time.")
        def job():
            buf = io.StringIO()
            try:
                with contextlib.redirect_stdout(buf):
                    fn()
            except Exception as e:
                print("ERROR:", e)
            self.q.put(buf.getvalue() or "Done.")
            self.q.put("__DONE__")
        threading.Thread(target=job, daemon=True).start()

    def _pick_samples(self):
        files = filedialog.askopenfilenames(
            title="Choose voice recordings",
            filetypes=[("Audio", "*.wav *.mp3 *.m4a *.ogg *.webm"), ("All", "*.*")])
        if files:
            self.sample_files = list(files)
            self.sample_lbl.config(text=f"{len(files)} file(s) chosen")

    def _pick_one(self, key):
        f = filedialog.askopenfilename(
            title="Choose audio",
            filetypes=[("Audio", "*.wav *.mp3 *.m4a *.ogg"), ("All", "*.*")])
        if f:
            self.job_files[key] = f
            lbl = {"sing": self.sing_lbl, "convert": self.conv_lbl,
                   "separate": self.sep_lbl}[key]
            lbl.config(text=f.split("/")[-1])

    # -- actions -----------------------------------------------------------
    def _need(self, ok, msg):
        if not ok:
            messagebox.showwarning("VoiceForge", msg)
        return ok

    def _do_train(self):
        name = self.v_name.get().strip()
        if not self._need(name and self.sample_files,
                          "Give a voice name and choose recordings first."):
            return
        def fn():
            from pathlib import Path
            from .dataset import prepare
            from .train import train
            ds = prepare(name, [Path(x) for x in self.sample_files])
            train(name, ds, epochs=int(self.v_epochs.get() or 60))
            print("Training complete. The voice is ready.")
        self._run(fn)

    def _do_sing(self):
        name = self.s_voice.get().strip()
        if not self._need(name and self.job_files.get("sing"),
                          "Choose a song and a trained voice first."):
            return
        def fn():
            from . import config
            from .sing import sing
            out = config.WORK_DIR / "desktop_song.wav"
            sing(self.job_files["sing"], name, out,
                 with_music=self.s_music.get(),
                 index_rate=float(self.s_ir.get()), protect=float(self.s_pr.get()))
            print("Song saved to", out)
        self._run(fn)

    def _do_speak(self):
        name = self.t_voice.get().strip()
        text = self.text_box.get("1.0", "end").strip()
        if not self._need(name and text, "Type text and a trained voice first."):
            return
        def fn():
            from . import config
            from .speak import speak
            out = config.WORK_DIR / "desktop_speak.wav"
            speak(text, name, out)
            print("Speech saved to", out)
        self._run(fn)

    def _do_convert(self):
        name = self.c_voice.get().strip()
        if not self._need(name and self.job_files.get("convert"),
                          "Choose a file and a trained voice first."):
            return
        def fn():
            from . import config
            from .convert import convert_file
            out = config.WORK_DIR / "desktop_converted.wav"
            convert_file(self.job_files["convert"], name, out,
                         index_rate=float(self.c_ir.get()),
                         protect=float(self.c_pr.get()))
            print("Converted file saved to", out)
        self._run(fn)

    def _do_separate(self):
        if not self._need(self.job_files.get("separate"), "Choose a song first."):
            return
        def fn():
            from .separate import separate
            v, b = separate(self.job_files["separate"])
            print("Vocals:", v)
            print("Instrumental:", b)
        self._run(fn)

    def _do_voices(self):
        def fn():
            from . import config
            logs = config.applio_dir() / "logs"
            names = []
            if logs.exists():
                names = sorted(d.name for d in logs.iterdir()
                               if d.is_dir() and list(d.glob("*.pth")))
            text = "\n".join(names) if names else "No trained voices yet."
            self.q.put("__VOICES__" + text)
            print(text)
        self._run(fn)


def launch() -> None:
    App().mainloop()
