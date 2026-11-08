<p align="center">
  <img src="assets/logo.png" width="120" alt="VoiceForge logo">
</p>

<h1 align="center">VoiceForge</h1>

<p align="center"><b>Clone any voice. Make it speak or sing. On a normal computer, with no GPU.</b></p>

<p align="center">
  <a href="https://github.com/Tcode-Motion/VoiceForge/actions/workflows/ci.yml"><img src="https://github.com/Tcode-Motion/VoiceForge/actions/workflows/ci.yml/badge.svg" alt="CI"></a>
  <a href="https://github.com/Tcode-Motion/VoiceForge/releases"><img src="https://img.shields.io/badge/release-v1.0.0.1-blue.svg" alt="Release v1.0.0.1"></a>
  <img src="https://img.shields.io/badge/python-3.10%2B-blue" alt="Python">
  <img src="https://img.shields.io/badge/platforms-Windows%20%7C%20macOS%20%7C%20Linux%20%7C%20Android%20%7C%20iOS-brightgreen" alt="Platforms">
  <img src="https://img.shields.io/badge/GPU-not%20required-success" alt="No GPU">
  <img src="https://img.shields.io/badge/RAM-4%20GB%20minimum-success" alt="Low RAM">
  <img src="https://img.shields.io/badge/network-fully%20offline-success" alt="Offline">
  <img src="https://img.shields.io/badge/license-MIT-green" alt="MIT">
</p>

---

## About

VoiceForge is an offline, CPU-first voice cloning studio built for everyday computers: laptops, mini PCs, or office desktops with a basic processor and as little as 4 GB of RAM.

Record a voice sample. Train a model locally on your own machine. Then make that voice speak typed text or sing any song with realistic timbre and melody. Everything executes on your own hardware. No cloud services, no remote servers, no subscriptions, and zero data leaves your device.

VoiceForge was designed, tested, and benchmarked on a modest 4 vCPU / 8 GB RAM / no-GPU hardware profile. Every single engineering decision follows from that constraint: if it runs well on minimal hardware, it runs blazingly fast everywhere.

> **Privacy by Design:** After the initial one-time engine installation, VoiceForge works completely with your internet connection severed. Your recordings, trained voice weights, and synthesized outputs remain strictly confidential on your local drive.

---

## Screenshots

<p align="center">
  <img src="assets/gui-web.png" width="440" alt="VoiceForge web GUI">
  <img src="assets/gui-desktop.png" width="440" alt="VoiceForge desktop app">
</p>

<p align="center"><i>The Web Studio (left) and the Native Desktop App for Windows, macOS, and Linux (right). Unified design system: dark aesthetic, responsive cards, drag-and-drop zones, real-time sliders, and live job terminal.</i></p>

<p align="center">
  <img src="assets/gui-phone.png" width="260" alt="VoiceForge mobile companion">
</p>

<p align="center"><i>The Android and iOS mobile companion apps bring the full studio to your smartphone with touch-first controls, streaming results over local Wi-Fi while your computer handles the CPU processing.</i></p>

---

## Core Capabilities

| Mode | Functionality |
|---|---|
| **Train** | Learns a voice from your audio recordings: 30 seconds minimum, 5 minutes recommended, 10 minutes for optimal fidelity. |
| **Sing** | Feed any song. Automatically isolates singing vocals, converts them to your target voice, and mixes back with original instrumentals. |
| **Speak** | Type any sentence or script and hear it spoken in the trained voice via Kokoro TTS + RVC. |
| **Convert** | Transform any existing voice recording, podcast, or dialogue into the trained voice with fine-grained index strength and clarity protection sliders. |
| **Separate** | Split songs into clean isolated vocals and backing instrumental tracks using Demucs (htdemucs). |

All capabilities are available across five interfaces: **Native Desktop GUI**, **Browser Web Studio**, **Interactive Terminal (TUI)**, **Scriptable CLI**, and **Mobile Companion Apps**.

---

## Why Choose VoiceForge?

| Feature | VoiceForge | Cloud Voice Services (ElevenLabs, etc.) | Traditional GPU Tools |
|---|---|---|---|
| **GPU Required** | **No** (Standard CPU) | No (Vendor Servers) | Yes (NVIDIA CUDA 8GB+) |
| **Voice Data Privacy** | **100% Offline & Local** | Uploaded to third-party cloud | Local |
| **Recurring Cost** | **Free & Open Source** | Monthly Subscription / Credits | Free |
| **Internet Required** | **No** (Runs offline) | Mandatory | Usually optional |
| **Minimum Memory** | **4 GB RAM** | N/A | 16 GB to 32 GB RAM |
| **Runs on Laptops** | **Yes, by design** | N/A | Rare (Thermal / VRAM limits) |

---

## Download Pre-built Releases (v1.0.0.1)

Automated multi-platform binaries are compiled by CI and attached to each release on GitHub:

- **Windows**: `VoiceForge-Windows.zip` (Standalone desktop application with `VoiceForge.exe`).
- **macOS**: `VoiceForge-macOS.zip` (Native `VoiceForge.app` for Apple Silicon M-series and Intel Macs).
- **Linux**: `VoiceForge-Linux.tar.gz` (Standalone desktop binary for modern Linux distributions).
- **Android**: `VoiceForge-Android.apk` (Touch-friendly companion APK for Android 8.0+).
- **iOS**: `VoiceForge-iOS-simulator.zip` (Companion app for iOS Simulator; source project ready for Xcode device signing).
- **Python**: Wheel and source distribution packages for `pip install voiceforge`.

Visit the [Releases Page](https://github.com/Tcode-Motion/VoiceForge/releases) to download the latest builds.

---

## Cross-Platform Setup & Installation

### 1. Windows Setup Guide

#### Option A: Standalone Executable (Fastest)
1. Download `VoiceForge-Windows.zip` from Releases.
2. Extract the archive into a folder of your choice.
3. Double-click `VoiceForge.exe` to launch the native desktop window.

#### Option B: Source / Developer Installation
Prerequisites: Python 3.10 to 3.12, Git, and FFmpeg.

1. Open PowerShell and install FFmpeg (if not already installed):
   ```powershell
   winget install Gyan.FFmpeg
   ```
2. Clone the repository and enter the directory:
   ```powershell
   git clone https://github.com/Tcode-Motion/VoiceForge.git
   cd VoiceForge
   ```
3. Set up the local AI engines (Applio, Demucs, Kokoro):
   ```powershell
   powershell -ExecutionPolicy Bypass -File scripts\setup_engines.ps1
   ```
   *(Or double-click `scripts\setup_engines.bat` in Command Prompt).*
4. Install VoiceForge:
   ```powershell
   pip install -e .[desktop]
   ```
5. Launch your preferred interface:
   ```powershell
   voiceforge desktop    # Native desktop window
   voiceforge gui        # Web Studio (http://127.0.0.1:8760)
   voiceforge tui        # Terminal interactive menu
   ```

---

### 2. macOS Setup Guide (Apple Silicon & Intel)

#### Option A: Pre-built App
1. Download `VoiceForge-macOS.zip` from Releases.
2. Unzip and drag `VoiceForge.app` to your Applications folder.
3. Double-click to open. *(If macOS Gatekeeper shows an unverified developer warning, right-click and select Open, or run `xattr -cr /Applications/VoiceForge.app`).*

#### Option B: Source Installation
Prerequisites: Homebrew, Python 3.10+, and FFmpeg.

1. Install prerequisites via Homebrew:
   ```bash
   brew install python@3.12 ffmpeg git
   ```
2. Clone and navigate into the repository:
   ```bash
   git clone https://github.com/Tcode-Motion/VoiceForge.git
   cd VoiceForge
   ```
3. Run the one-time engine installer:
   ```bash
   bash scripts/setup_engines.sh
   ```
4. Install VoiceForge:
   ```bash
   pip install -e .[desktop]
   ```
5. Launch the studio:
   ```bash
   voiceforge desktop
   ```

---

### 3. Linux Setup Guide (Ubuntu, Debian, Fedora, Arch)

#### Option A: Pre-built Binary
1. Download `VoiceForge-Linux.tar.gz` from Releases.
2. Extract: `tar -xzf VoiceForge-Linux.tar.gz`
3. Execute `./VoiceForge` to start.

#### Option B: Source Installation
1. Install system packages:
   - **Debian / Ubuntu**: `sudo apt update && sudo apt install -y python3-pip python3-venv ffmpeg git`
   - **Fedora**: `sudo dnf install -y python3-pip ffmpeg git`
   - **Arch Linux**: `sudo pacman -S python-pip ffmpeg git`
2. Clone and install engines:
   ```bash
   git clone https://github.com/Tcode-Motion/VoiceForge.git
   cd VoiceForge
   bash scripts/setup_engines.sh
   ```
3. Install VoiceForge:
   ```bash
   pip install -e .[desktop]
   ```
4. Run:
   ```bash
   voiceforge gui
   ```

---

### 4. Android Companion App Setup

1. Download `VoiceForge-Android.apk` from the latest release.
2. Transfer or download onto your Android phone and install.
3. On your computer, launch VoiceForge to accept network connections:
   ```bash
   voiceforge gui --host 0.0.0.0 --port 8760
   ```
4. Look up your computer's local IP address (`ipconfig` on Windows, `ip a` on Linux/macOS).
5. Open VoiceForge on your phone, type `http://<YOUR_COMPUTER_IP>:8760`, and tap **Connect**.
6. The app provides a dedicated mobile interface with full recording, training, singing, and playback features.

---

### 5. iOS Companion App Setup

1. **Simulator**: Download `VoiceForge-iOS-simulator.zip`, extract, and install via `xcrun simctl install booted VoiceForge.app`.
2. **Physical Device Build**:
   ```bash
   cd ios
   brew install xcodegen
   xcodegen generate
   open VoiceForge.xcodeproj
   ```
   Assign your Apple Developer account under **Signing & Capabilities** and click **Run** to install to your connected iPhone/iPad.
3. Start the studio on your host computer (`voiceforge gui --host 0.0.0.0 --port 8760`) and connect using your host IP.

---

### 6. Local Network & Headless Server Sharing

VoiceForge includes a built-in zero-dependency HTTP server that can be accessed by any browser on your home or office network:
```bash
voiceforge gui --host 0.0.0.0 --port 8760
```
Open `http://<HOST_IP>:8760` from any phone, iPad, or Chromebook on the same Wi-Fi without installing anything on the client devices.

---

## Step-by-Step Quickstart Workflow

```bash
# 1. Ingest audio recordings into a training dataset
voiceforge add-voice alex voice_sample1.wav voice_sample2.mp3

# 2. Train the voice model (efficient CPU training with regular checkpoints)
voiceforge train alex --epochs 60

# 3. Create an AI song cover (splits vocals, transfers voice, remixes backing track)
voiceforge sing pop_song.mp3 --voice alex --with-music -o alex_cover.wav

# 4. Generate speech from typed text in your cloned voice
voiceforge speak "Hello! This voice was cloned locally with VoiceForge." --voice alex -o speech.wav

# 5. Convert existing voice recordings or podcasts
voiceforge convert interview.mp3 --voice alex --index-rate 0.90 -o converted.wav

# 6. Isolate vocals and instrumental tracks from any song
voiceforge separate hit_track.mp3 -o output_stems/
```

---

## Hardware Requirements & Real Benchmarks

| Component | Minimum Specification | Recommended Specification |
|---|---|---|
| **CPU** | Dual-core x86_64 or ARM64 | 4 or more CPU cores |
| **RAM** | 4 GB | 8 GB or more |
| **GPU** | None required | None required |
| **Storage** | 3 GB for base engines & models | 10 GB for multiple trained voices |
| **Operating System** | Windows 10+, macOS 12+, Linux | Same |

### Measured Benchmarks (Reference 4 vCPU / 8 GB RAM / No GPU Machine)

| Task | Execution Time |
|---|---|
| **Training per epoch (round)** | ~1.5 minutes |
| **Text-to-Speech sentence generation** | ~1 minute |
| **Voice conversion (6-second sample)** | ~40 seconds |
| **Sing mode (6-second song sample)** | ~1 minute |
| **Sing mode (full 48-second track)** | ~3 minutes |
| **Song stem separation (full track)** | ~1 minute |

---

## Technical Architecture & Low-Resource Design

VoiceForge acts as an intelligent, memory-conscious orchestrator for three proven open-source AI audio engines:

```
[ User Audio / Text ]
          │
          ├──> 1. Separate: Demucs (htdemucs) -> Vocals + Instrumental Stems
          │
          ├──> 2. Pitch & Features: RMVPE + ContentVec (HuBERT)
          │
          ├──> 3. Synthesize / Clone: Applio (RVC v2, HiFi-GAN, 40 kHz)
          │
          ├──> 4. Text-to-Speech: Kokoro TTS (82M ONNX model)
          │
          └──> 5. Mastering Chain: High-pass (70Hz) -> Presence EQ -> Compression -> -14 LUFS Loudness Normalization
```

### Why Peak RAM Stays Under 4 GB:
1. **Strict Process Isolation**: Engines are invoked as dedicated, short-lived subprocesses. When separation finishes, Demucs unloads entirely before RVC begins.
2. **Chunked Conversion Pipeline**: Audio files of arbitrary length are processed in sequential 30-second windows with micro-crossfades. Peak RAM remains constant whether processing a 10-second clip or a 2-hour recording.
3. **Optimized Training Profile**: Gradient checkpointing, batch size 1, and lean parameter architectures ensure smooth execution on laptops without swap thrashing.
4. **Mastering Output Guarantee**: Every audio file is mastered through FFmpeg with true peak limiting (-1.5 dB TP) and -14 LUFS loudness targeting, ready for immediate publishing.

---

## Voice Recording Best Practices

| Total Sample Duration | Expected Clone Quality |
|---|---|
| **Under 30 seconds** | Rejected (insufficient audio data to capture voice timbre) |
| **30s to 2 minutes** | Recognizable identity, raw intonation |
| **5 minutes** | Clear, expressive, high-accuracy vocal reproduction |
| **10 minutes (divided in short files)** | Best fidelity, natural cadence and vocal nuance |

### Recording Tips:
- Use a quiet room with minimal background noise and zero background music.
- Speak naturally with consistent microphone distance.
- Splitting speech into several 1 to 2 minute files produces higher quality than one long unedited recording.

---

## Frequently Asked Questions

**Do I need an NVIDIA GPU or CUDA?**
No. VoiceForge is purposefully built and optimized to run on standard CPUs without any discrete graphics card.

**Does my voice data ever leave my computer?**
Never. After downloading the open-source model weights during the initial setup, VoiceForge operates 100% offline. There are no tracking scripts, telemetry, or remote servers.

**Can it sing completely new melodies from typed lyrics?**
To sing a song, use Sing Mode with an existing music file: the melody, timing, and pitch contour are extracted from the original vocal track, while the vocal timbre is replaced with your voice. Speak Mode handles text-to-speech reading.

**What languages are supported?**
Singing and voice conversion work with any language spoken or sung in the source recording. Speak Mode leverages Kokoro TTS and is optimized for English, with additional multilingual voices available.

---

## Repository Structure

```
VoiceForge/
├── src/voiceforge/       # Core package: CLI, TUI, Web GUI, Desktop GUI, Pipeline
├── scripts/              # One-click engine installers (sh, ps1, bat)
├── packaging/            # PyInstaller spec and desktop app launcher
├── android/              # Native Android companion application (Kotlin/WebView)
├── ios/                  # Native iOS companion application (Swift/WKWebView)
├── docs/                 # Detailed usage, troubleshooting, and low-resource notes
├── assets/               # Brand logos, icons, and UI screenshots
└── .github/workflows/    # CI tests and automated release workflows
```

---

## Ethics & Responsible Use

Voice cloning is a powerful creative technology. Only clone voices you own or for which you have explicit, documented consent to use. VoiceForge is created as an offline tool specifically to empower personal creative privacy without handing sensitive biometric data to third-party cloud services.

---

## License

VoiceForge is licensed under the [MIT License](LICENSE). Third-party engines utilized by VoiceForge maintain their respective open-source licenses: Applio/RVC (MIT), Demucs (MIT), Kokoro TTS (Apache-2.0).
