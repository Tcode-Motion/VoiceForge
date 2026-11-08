<p align="center">
  <img src="assets/logo.png" width="120" alt="VoiceForge logo">
</p>

<h1 align="center">VoiceForge</h1>

<p align="center"><b>Clone any voice. Make it speak or sing. On a normal computer, with no GPU.</b></p>

<p align="center">
  <img src="https://img.shields.io/badge/python-3.10%2B-blue" alt="Python">
  <img src="https://img.shields.io/badge/GPU-not%20required-success" alt="No GPU">
  <img src="https://img.shields.io/badge/RAM-4%20GB%20minimum-success" alt="Low RAM">
  <img src="https://img.shields.io/badge/network-fully%20offline-success" alt="Offline">
  <img src="https://img.shields.io/badge/license-MIT-green" alt="MIT">
</p>

## About

VoiceForge is a voice cloning studio built for ordinary machines: a
laptop or mini PC with a plain CPU and as little as 4 GB of RAM. Record
a short sample of a voice, train a model locally, then make that voice
speak typed text or sing any song. Everything runs on your own
computer. Nothing is uploaded anywhere, ever. VoiceForge was designed,
tested and benchmarked on a 4 vCPU / 8 GB RAM / no-GPU machine, and
every design decision follows from that constraint.

## Features

- **Train a voice** from recordings: 30 seconds minimum, 5 minutes
  recommended, 10 minutes ideal. Drag, drop, done.
- **Sing mode**: give it any song, it separates the singing from the
  music, converts the singing into your trained voice, and can mix it
  back over the original music.
- **Speak mode**: type lyrics, a message, anything, and hear it spoken
  in the trained voice.
- **Convert mode**: turn any voice recording into the trained voice,
  with sliders for voice strength and clarity.
- **Separate mode**: split any song into clean vocals and instrumental.
- Four interfaces: a **web GUI**, a **desktop GUI**, a **terminal menu
  (TUI)**, and a scriptable **CLI**.
- Packaged apps are built by CI: **Windows (.exe)**, **macOS (.app)**,
  **Linux (binary)**, plus **Android** and **iOS** companion apps that
  run the studio UI and talk to the engine on your computer.

## Screenshots

<p align="center">
  <img src="assets/gui-web.png" width="430" alt="VoiceForge web GUI">
  <img src="assets/gui-desktop.png" width="430" alt="VoiceForge desktop GUI">
</p>

<p align="center"><i>The web GUI (left) and the desktop GUI (right). Same engine, same jobs, plus Convert, Separate and a voice library.</i></p>

## Quick start

```bash
# 1. Install the engines (one time; Applio/RVC, Demucs, Kokoro, all CPU builds)
bash scripts/setup_engines.sh

# 2. Install VoiceForge itself (standard library only, no dependencies)
pip install .

# 3. Make a voice
voiceforge add-voice myvoice recording1.wav recording2.wav
voiceforge train myvoice --epochs 60

# 4. Use it
voiceforge sing favourite_song.mp3 --voice myvoice --with-music -o my_cover.wav
voiceforge speak "Hello, this song is in my own voice" --voice myvoice -o hello.wav
voiceforge convert interview.mp3 --voice myvoice -o interview_mine.wav

# 5. Or open a GUI
voiceforge gui        # web app at http://127.0.0.1:8760
voiceforge desktop    # desktop window
voiceforge tui        # terminal menu
```

## Guidelines: getting a good voice

| Sample length | Result |
|---|---|
| Under 30 seconds | Rejected (too little to learn a voice) |
| 30 seconds to 2 minutes | Recognisable, rough |
| 5 minutes | Good |
| 10 minutes, in small chunks | Best |

- Record in a quiet room, natural talking voice, no music behind you.
- Small chunks (a few minutes each) beat one long noisy file.
- Voice strength (index rate) 1.0 copies the trained voice fully;
  0.85 is gentler. Clarity protect around 0.25 keeps words crisp.
- More clean voice in, more of you out. This is the whole secret.

## How it works

VoiceForge is a careful conductor for three proven open-source
engines, each run as a short-lived process so only one is ever in
memory:

| Stage | Engine | Job |
|---|---|---|
| Separate | Demucs (htdemucs) | Splits a song into vocals and instrumental |
| Train + convert | Applio (RVC v2) | Learns a voice and converts singing or speech onto it |
| Speak | Kokoro TTS (82M, ONNX) | Turns typed text into natural speech, then RVC moves it onto your voice |

## Built for low-end machines

Most voice tools assume a gaming GPU. VoiceForge assumes the opposite
and is engineered around it (details in
[docs/LOW_RESOURCE.md](docs/LOW_RESOURCE.md)):

- **Chunked conversion**: long audio is converted in 30-second
  chunks, each in a fresh process, joined with crossfades. Peak RAM
  stays flat for a 1-minute clip or a 1-hour concert.
- **One engine at a time**: engines load, work, and exit before the
  next stage starts.
- **Memory-safe training**: batch size 1, gradient checkpointing,
  weights-only checkpoints saved regularly.
- **Small separation windows**: Demucs runs with a 7-second segment.
- **Right-sized models**: RMVPE pitch tracking, ContentVec features,
  and an 82M-parameter TTS that is fast on CPU.
- **Safe temp location**: engines never depend on a small system
  temp folder.

## Honest scope

- Speak mode **speaks** text in your voice. It does not invent a
  melody: to sing, use Sing mode with a real song so the tune and
  timing come from the original singer.
- Quality follows the sample. More clean voice in, more of you out.
- Training is the slow part on CPU (about 1.5 minutes per round on
  the reference machine). A short song conversion takes a few minutes.
- The Android and iOS apps are companions: they run the studio
  interface and connect to the VoiceForge engine on your computer
  (same network). The heavy engines stay on the computer, which is
  what keeps the phone apps small and fast.

## Project layout

```
src/voiceforge/     the studio (CLI, TUI, web GUI, desktop GUI, pipeline)
scripts/            one-time engine installer
docs/               usage, low-resource design notes, troubleshooting
packaging/          PyInstaller spec for the desktop apps
android/            Android companion app (Kotlin, WebView)
ios/                iOS companion app (Swift, WKWebView)
.github/workflows/  CI tests + app builds + release automation
```

## Contributing

Contributions are welcome. Read [CONTRIBUTING.md](CONTRIBUTING.md)
and the [Code of Conduct](CODE_OF_CONDUCT.md) first. The one hard
rule: VoiceForge must stay runnable on a plain CPU with 4 GB of RAM.

## Security

See [SECURITY.md](SECURITY.md) for the security policy and how to
report a problem. Short version: VoiceForge runs fully offline after
setup; your voice data never leaves your machine.

## Changelog

See [CHANGELOG.md](CHANGELOG.md). If something breaks, start with
[docs/TROUBLESHOOTING.md](docs/TROUBLESHOOTING.md).

## License

MIT. See [LICENSE](LICENSE). The engines VoiceForge drives keep their
own licenses: Applio/RVC (MIT), Demucs (MIT), Kokoro (Apache-2.0).

## Ethics

Only clone voices you own or have clear permission to use. VoiceForge
runs locally precisely so your voice data never has to leave your
machine.
