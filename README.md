<p align="center">
  <img src="assets/logo.png" width="130" alt="VoiceForge Logo">
</p>

<h1 align="center">VoiceForge</h1>

<p align="center">
  <b>The CPU-First, Privacy-Focused Voice Cloning Studio</b><br>
  <i>Clone any voice. Make it speak or sing. On standard consumer hardware, with no GPU and no cloud.</i>
</p>

<p align="center">
  <a href="https://github.com/Tcode-Motion/VoiceForge/actions/workflows/ci.yml"><img src="https://github.com/Tcode-Motion/VoiceForge/actions/workflows/ci.yml/badge.svg" alt="CI Status"></a>
  <a href="https://github.com/Tcode-Motion/VoiceForge/releases"><img src="https://img.shields.io/badge/release-v1.0.0.1-blue.svg?style=flat-square" alt="Release v1.0.0.1"></a>
  <img src="https://img.shields.io/badge/python-3.10%20%7C%203.11%20%7C%203.12-blue?style=flat-square" alt="Python Versions">
  <img src="https://img.shields.io/badge/platforms-Windows%20%7C%20macOS%20%7C%20Linux%20%7C%20Android%20%7C%20iOS-success?style=flat-square" alt="Supported Platforms">
  <img src="https://img.shields.io/badge/GPU-strictly%20optional-success?style=flat-square" alt="No GPU Required">
  <img src="https://img.shields.io/badge/RAM-4%20GB%20minimum-success?style=flat-square" alt="Low RAM">
  <img src="https://img.shields.io/badge/network-100%25%20offline-success?style=flat-square" alt="Offline Privacy">
  <img src="https://img.shields.io/badge/license-MIT-green?style=flat-square" alt="MIT License">
</p>

---

## Table of Contents

- [Overview & Philosophy](#overview--philosophy)
- [Visual Interface Showcase](#visual-interface-showcase)
- [Comprehensive Compatibility Matrix](#comprehensive-compatibility-matrix)
- [Hardware & System Requirements](#hardware--system-requirements)
- [Masterclass: Recommendations for Best Voice Quality](#masterclass-recommendations-for-best-voice-quality)
- [Download Pre-Built Packages (v1.0.0.1)](#download-pre-built-packages-v1001)
- [Platform Setup Guides](#platform-setup-guides)
  - [Windows Setup (Executable & Source)](#1-windows-setup-guide)
  - [macOS Setup (Apple Silicon & Intel)](#2-macos-setup-guide-apple-silicon--intel)
  - [Linux Setup (Ubuntu, Debian, Fedora, Arch)](#3-linux-setup-guide)
  - [Android Companion App](#4-android-companion-app-setup)
  - [iOS Companion App](#5-ios-companion-app-setup)
  - [Local Network & Headless Studio](#6-local-network--headless-server-studio)
- [Core Modes & Capabilities](#core-modes--capabilities)
- [Scriptable CLI Reference](#scriptable-cli-reference)
- [Technical Architecture & Memory Engineering](#technical-architecture--memory-engineering)
- [Real-World Benchmarks](#real-world-benchmarks)
- [Troubleshooting & Common Questions](#troubleshooting--common-questions)
- [Ethics & Responsible Use](#ethics--responsible-use)
- [License](#license)

---

## Overview & Philosophy

**VoiceForge** is an open-source voice cloning studio engineered specifically for ordinary personal computers: laptops, mini PCs, budget desktops, and office workstations lacking dedicated gaming graphics cards.

Most modern AI voice tools require 12 GB+ of NVIDIA VRAM, complex CUDA driver toolchains, or expensive recurring monthly cloud subscriptions that compromise personal biometric privacy. VoiceForge turns that paradigm on its head:

1. **CPU-First Architecture:** Every model (RVC v2, Demucs htdemucs, Kokoro TTS, RMVPE, ContentVec) runs on standard CPU threads using optimized PyTorch and ONNX Runtime inference.
2. **100% Offline Privacy:** Your voice recordings, trained neural weights, and synthesized speech or songs never leave your machine. After a one-time setup, pull the ethernet cable or turn off Wi-Fi; VoiceForge functions identically.
3. **Flat 4 GB Memory Footprint:** Long songs are sliced into 30-second windows with micro-crossfades, and AI engines run in isolated, short-lived processes that completely unload from RAM before the next step begins.
4. **Studio-Ready Output:** Built-in FFmpeg mastering with high-pass filtering (70 Hz), presence EQ, dynamic compression, and automatic loudness normalization to -14 LUFS with a -1.5 dB True Peak ceiling.

> [!NOTE]
> VoiceForge is not a wrapper around external APIs. It is a fully self-contained local audio processing studio that orchestrates state-of-the-art open-source audio engines directly on your CPU.

---

## Visual Interface Showcase

VoiceForge provides an elegant, dark-mode user interface designed for maximum productivity and clarity.

### 1. Browser Web Studio (Universal Local Server)
Accessible from any modern browser on your desktop or across your local home network.

<p align="center">
  <a href="assets/gui-web.png" target="_blank">
    <img src="assets/gui-web.png" alt="VoiceForge Web Studio" width="95%" style="border-radius: 8px; border: 1px solid #30363d; box-shadow: 0 8px 24px rgba(0,0,0,0.5);">
  </a>
</p>

*Key Features: Sidebar navigation, drag-and-drop dropzones with instant waveform validation, in-browser microphone recording, interactive pitch and clarity sliders, and real-time job execution console.*

---

### 2. Native Desktop Application (Windows, macOS, Linux)
A standalone desktop window powered by an embedded runtime (pywebview) with native file-picker dialogues.

<p align="center">
  <a href="assets/gui-desktop.png" target="_blank">
    <img src="assets/gui-desktop.png" alt="VoiceForge Desktop Application" width="95%" style="border-radius: 8px; border: 1px solid #30363d; box-shadow: 0 8px 24px rgba(0,0,0,0.5);">
  </a>
</p>

*Key Features: Pixel-identical layout to the Web Studio, zero browser tab clutter, local file access, system tray integration, and native desktop notifications.*

---

### 3. Mobile Companion Apps (Android & iOS)
Transform your phone into a handheld studio controller while your computer does the heavy lifting.

<p align="center">
  <a href="assets/gui-phone.png" target="_blank">
    <img src="assets/gui-phone.png" alt="VoiceForge Mobile Companion" width="340" style="border-radius: 16px; border: 2px solid #30363d; box-shadow: 0 8px 24px rgba(0,0,0,0.6);">
  </a>
</p>

*Key Features: Touch-optimized controls, mobile microphone capture, real-time Wi-Fi synchronization to your desktop engine host, and mobile audio playback.*

---

## Comprehensive Compatibility Matrix

VoiceForge is engineered for universal compatibility across operating systems, processor architectures, and audio container formats.

### Operating System & Hardware Compatibility

| Platform | Supported Versions | Supported Architectures | Runtime Mode |
|---|---|---|---|
| **Windows** | Windows 10, Windows 11 | x86_64 (64-bit), ARM64 (emulated) | Standalone `.exe` or Python CLI/GUI |
| **macOS** | macOS 12 (Monterey) through macOS 15 (Sequoia) | Apple Silicon (M1/M2/M3/M4) & Intel Core i5/i7/i9 | Standalone `.app` bundle or Python CLI/GUI |
| **Linux** | Ubuntu 20.04+, Debian 11+, Fedora 38+, Arch, RHEL 8+ | x86_64, aarch64 (ARM64) | Standalone executable or Python CLI/GUI |
| **Android** | Android 8.0 (Oreo) through Android 15 (API 26 to 35) | ARM64 (v8a), ARM32 (v7a), x86_64 | Native APK client connecting to desktop host |
| **iOS / iPadOS** | iOS 16.0 through iOS 18+ | Apple A-series & M-series chips | Native Swift client connecting to desktop host |
| **Docker** | Any Linux/Windows container host | x86_64, aarch64 | Headless studio with Web GUI port exposure |

### Audio Format & Codec Support

VoiceForge handles virtually any audio recording without requiring manual format conversion:

- **Uncompressed Audio:** WAV (PCM 16-bit, 24-bit, 32-bit float), AIFF, AIFC.
- **Compressed Lossless:** FLAC, ALAC (Apple Lossless).
- **Compressed Lossy:** MP3 (VBR, CBR up to 320 kbps), M4A / AAC, OGG (Vorbis), OPUS, WMA.
- **Sample Rate Conversion:** Audio inputs at 16 kHz, 22.05 kHz, 32 kHz, 44.1 kHz, or 48 kHz are automatically resampled to high-fidelity 40 kHz using polyphase bandlimited interpolation.
- **Channel Handling:** Stereo and mono inputs are automatically parsed; multichannel tracks are converted to clean vocal channels without clipping.

### Language & Vocal Range Support

- **Sing & Convert Modes:** Universal across **all spoken and sung human languages** (English, Spanish, Mandarin, Japanese, Hindi, French, German, Korean, Bengali, Portuguese, etc.). The pitch tracking (RMVPE) and acoustic feature extraction (ContentVec) models track vocal timbre and melodic contours independently of spoken grammar.
- **Speak Mode (TTS):** Powered by Kokoro 82M. Exceptional accuracy and natural cadence in American and British English, with support for additional multilingual phonemes.

---

## Hardware & System Requirements

| Specification | Minimum (Functional) | Recommended (Optimal Experience) |
|---|---|---|
| **Processor (CPU)** | Dual-Core 2.0 GHz (x86_64 with AVX or ARM64) | 4 to 8 physical CPU cores (Intel 8th Gen+, AMD Ryzen 3000+, Apple M1+) |
| **System Memory (RAM)** | **4 GB RAM** (with active paging/swap file) | **8 GB to 16 GB RAM** |
| **Dedicated Graphics (GPU)** | **None required** (Zero VRAM needed) | Strictly optional (not utilized by default CPU builds) |
| **Free Storage Space** | 3.5 GB for base models and engine dependencies | 10 GB+ SSD space for training datasets and voice checkpoints |
| **Audio Hardware** | Any standard headphone / speaker output | Quality cardioid USB or XLR microphone for recording samples |
| **Network Connection** | Needed once for initial engine download | **100% Offline** for all training, synthesis, and conversion |

> [!TIP]
> **AVX / AVX2 Instruction Support:** Modern Intel and AMD processors manufactured after 2013 support AVX2, which speeds up Kokoro TTS and RVC inference significantly. On Apple Silicon (M1-M4), ARM NEON acceleration provides near-instantaneous feature extraction.

---

## Masterclass: Recommendations for Best Voice Quality

Voice cloning is a direct reflection of input data quality: **more clean voice in, more authentic voice out**. Follow these proven principles to create professional-grade vocal clones.

### 1. Recording Environment & Acoustics
- **Eliminate Room Reverberation:** Never record in empty rooms with bare walls or tiled floors. Record in a carpeted room, walk-in closet with clothes, or place blankets/pillows behind your microphone to absorb acoustic reflections.
- **Control the Noise Floor:** Turn off ceiling fans, air conditioning, and PC case fans nearby. A consistent background hum can degrade pitch tracking.
- **Distance & Pop Protection:** Maintain a distance of 15 to 20 cm (6 to 8 inches) from the microphone. Always use a pop filter or foam windscreen to prevent plosives ("p", "b", "t" sounds) from overloading the input.
- **Prevent Digital Clipping:** Set your recording input gain so that your loud speaking voice peaks between **-12 dB and -6 dB**. Never allow the audio meter to touch 0 dB (red line).

### 2. Dataset Duration vs. Clone Fidelity

| Recording Length | Expected Result | Recommended Usage |
|---|---|---|
| **Under 30 seconds** | Rejected by VoiceForge | Too little phoneme information to calculate feature centroids. |
| **30s to 2 minutes** | Recognizable, slightly robotic | Quick proof-of-concept testing, rough caricatures. |
| **5 minutes** | **Good, clear timbre reproduction** | Recommended standard for clear speech and conversational reading. |
| **10 to 15 minutes** | **Pristine, commercial studio quality** | Optimal fidelity: captures subtle breath, vibrato, and dynamic vocal inflections. |

### 3. Vocal Performance & Delivery
- **Speak in Natural Tone:** Speak naturally at your normal conversational pitch. Avoid whispering, shouting, or exaggerating intonation unless that specific caricature is desired.
- **Ensure Phonetic Diversity:** Do not repeat the same phrase over and over. Read diverse texts: newspaper articles, book chapters, or standard phonetically balanced pangrams (e.g., *"The quick brown fox jumps over the lazy dog"*).
- **Split into Bite-Sized Chunks:** Rather than submitting one giant 15-minute audio file, supply multiple 1-to-2 minute files. This allows VoiceForge's silence detection and chunking engine to build cleaner training slices.
- **Dry Voice Only:** Never train on audio containing background music, reverb, echo, auto-tune, or other speakers' voices.

### 4. Training Hyperparameters Guide
- **Epochs (Training Rounds):**
  - **40 epochs:** Fast prototype on CPU (~45 minutes for a 5-minute dataset).
  - **60 to 80 epochs:** The golden ratio for CPU training. Produces crisp acoustic identity without overfitting.
  - **100+ epochs:** Marginal gains on small datasets, risk of overfitting and raspiness.
- **Batch Size:** Locked to **1** by default in VoiceForge. This prevents RAM spikes and allows low-resource machines to train reliably.

### 5. Conversion Parameter Tuning (Sing & Convert Modes)

VoiceForge provides two critical sliders that control the converted vocal result:

- **Voice Strength (`--index-rate`, 0.0 to 1.0):**
  - Controls how strictly the output voice matches the trained voice model vs. retaining the original speaker's vocal traits.
  - **0.75 - 0.85 (Recommended for Singing):** Retains the emotional nuances, vibrato, and phrasing of the original singer while overlaying your voice timbre.
  - **0.90 - 1.0 (Recommended for Speech):** Maximum target voice replication.
- **Clarity Protection (`--protect`, 0.0 to 0.5):**
  - Protects voiced consonants, sibilants ("s", "sh", "ch"), and natural breath attacks from artificial distortion.
  - **0.25 (Default):** Crisp, balanced articulation.
  - **0.35 - 0.45:** Useful if the output voice has slight robotic buzz or artifacting around sharp words.
- **Pitch Shift (`--pitch`, semitones):**
  - Adjust when converting between different vocal ranges:
    - Female singer to Male target: `-12` (one octave down).
    - Male singer to Female target: `+12` (one octave up).
    - Same gender or similar vocal register: `0`.

---

## Download Pre-Built Packages (v1.0.0.1)

Official binaries are compiled and certified by GitHub Actions on clean runner environments:

| Package | Target Platform | Description | Direct Download |
|---|---|---|---|
| **Windows Desktop** | Windows 10/11 x64 | Self-contained desktop app with `VoiceForge.exe` | [VoiceForge-Windows.zip](https://github.com/Tcode-Motion/VoiceForge/releases/download/v1.0.0.1/VoiceForge-Windows.zip) |
| **macOS Desktop** | macOS 12+ (Apple Silicon & Intel) | Native `VoiceForge.app` with embedded UI | [VoiceForge-macOS.zip](https://github.com/Tcode-Motion/VoiceForge/releases/download/v1.0.0.1/VoiceForge-macOS.zip) |
| **Linux Desktop** | Linux x86_64 | Standalone binary with desktop support | [VoiceForge-Linux.tar.gz](https://github.com/Tcode-Motion/VoiceForge/releases/download/v1.0.0.1/VoiceForge-Linux.tar.gz) |
| **Android Companion** | Android 8.0+ (API 26-35) | Native APK with studio connection UI | [VoiceForge-Android.apk](https://github.com/Tcode-Motion/VoiceForge/releases/download/v1.0.0.1/VoiceForge-Android.apk) |
| **iOS Simulator** | iOS 16.0+ Simulator | Pre-compiled simulator build for Xcode | [VoiceForge-iOS-simulator.zip](https://github.com/Tcode-Motion/VoiceForge/releases/download/v1.0.0.1/VoiceForge-iOS-simulator.zip) |
| **Python Wheel** | Any OS with Python 3.10+ | Standard PyPI-compatible wheel | [Releases Page](https://github.com/Tcode-Motion/VoiceForge/releases/tag/v1.0.0.1) |

---

## Platform Setup Guides

<details open>
<summary><b><h3>1. Windows Setup Guide</h3></b></summary>

#### Option A: Standalone Desktop App (Recommended for Non-Developers)
1. Download [VoiceForge-Windows.zip](https://github.com/Tcode-Motion/VoiceForge/releases/download/v1.0.0.1/VoiceForge-Windows.zip).
2. Right-click the `.zip` file, select **Extract All...**, and extract to a folder (e.g., `C:\VoiceForge`).
3. Double-click `VoiceForge.exe` to launch the native desktop studio immediately.

#### Option B: Developer / Source Setup (PowerShell or CMD)
1. Ensure **Python 3.10, 3.11, or 3.12** is installed.
2. Install **FFmpeg** via Windows Package Manager:
   ```powershell
   winget install Gyan.FFmpeg
   ```
3. Clone the VoiceForge repository:
   ```powershell
   git clone https://github.com/Tcode-Motion/VoiceForge.git
   cd VoiceForge
   ```
4. Run the one-click Windows engine setup script:
   - In **PowerShell**:
     ```powershell
     powershell -ExecutionPolicy Bypass -File scripts\setup_engines.ps1
     ```
   - In **Command Prompt**:
     ```cmd
     scripts\setup_engines.bat
     ```
5. Install the VoiceForge package:
   ```powershell
   pip install -e .[desktop]
   ```
6. Start any interface:
   ```powershell
   voiceforge desktop    # Native desktop GUI
   voiceforge gui        # Browser Web Studio at http://127.0.0.1:8760
   voiceforge tui        # Terminal interactive menu
   ```
</details>

<details>
<summary><b><h3>2. macOS Setup Guide (Apple Silicon & Intel)</h3></b></summary>

#### Option A: Pre-built Desktop App
1. Download [VoiceForge-macOS.zip](https://github.com/Tcode-Motion/VoiceForge/releases/download/v1.0.0.1/VoiceForge-macOS.zip).
2. Extract the archive and drag `VoiceForge.app` into your `/Applications` directory.
3. Open `VoiceForge.app`.
   > [!NOTE]
   > If macOS displays *"App is from an unidentified developer"*, right-click `VoiceForge.app`, choose **Open**, and confirm. Alternatively, run:
   > ```bash
   > xattr -cr /Applications/VoiceForge.app
   > ```

#### Option B: Developer / Source Setup
1. Install prerequisites using Homebrew:
   ```bash
   brew install python@3.12 ffmpeg git
   ```
2. Clone repository and run engine setup:
   ```bash
   git clone https://github.com/Tcode-Motion/VoiceForge.git
   cd VoiceForge
   bash scripts/setup_engines.sh
   ```
3. Install VoiceForge:
   ```bash
   pip install -e .[desktop]
   ```
4. Launch:
   ```bash
   voiceforge desktop
   ```
</details>

<details>
<summary><b><h3>3. Linux Setup Guide</h3></b></summary>

#### Option A: Standalone Executable
1. Download [VoiceForge-Linux.tar.gz](https://github.com/Tcode-Motion/VoiceForge/releases/download/v1.0.0.1/VoiceForge-Linux.tar.gz).
2. Extract:
   ```bash
   tar -xzf VoiceForge-Linux.tar.gz
   cd VoiceForge
   ./VoiceForge
   ```

#### Option B: Source Installation
1. Install dependencies for your Linux distribution:
   - **Debian / Ubuntu / Mint:**
     ```bash
     sudo apt update && sudo apt install -y python3-pip python3-venv ffmpeg git
     ```
   - **Fedora / RHEL:**
     ```bash
     sudo dnf install -y python3-pip ffmpeg git
     ```
   - **Arch Linux / Manjaro:**
     ```bash
     sudo pacman -S python-pip ffmpeg git
     ```
2. Clone repository and install engines:
   ```bash
   git clone https://github.com/Tcode-Motion/VoiceForge.git
   cd VoiceForge
   bash scripts/setup_engines.sh
   pip install -e .[desktop]
   ```
3. Run:
   ```bash
   voiceforge gui
   ```
</details>

<details>
<summary><b><h3>4. Android Companion App Setup</h3></b></summary>

The Android companion application provides a touch-friendly interface while delegating all computational work to your computer over local Wi-Fi.

1. Download [VoiceForge-Android.apk](https://github.com/Tcode-Motion/VoiceForge/releases/download/v1.0.0.1/VoiceForge-Android.apk) directly onto your Android device.
2. Tap the downloaded APK to install (allow *"Install from unknown sources"* if prompted).
3. On your computer (Windows, macOS, or Linux), start VoiceForge with network listening:
   ```bash
   voiceforge gui --host 0.0.0.0 --port 8760
   ```
4. Check your computer's local IP address:
   - On Windows: run `ipconfig` (e.g. `192.168.1.15`).
   - On macOS / Linux: run `ip a` or `ifconfig`.
5. Open VoiceForge on your phone, type `http://<YOUR_COMPUTER_IP>:8760`, and tap **Connect**.
6. You can now record voice samples directly from your phone's microphone, train models, and play results.
</details>

<details>
<summary><b><h3>5. iOS Companion App Setup</h3></b></summary>

#### Option A: Run on iOS Simulator
1. Download [VoiceForge-iOS-simulator.zip](https://github.com/Tcode-Motion/VoiceForge/releases/download/v1.0.0.1/VoiceForge-iOS-simulator.zip) and extract it.
2. Install into an active iOS Simulator:
   ```bash
   xcrun simctl install booted VoiceForge.app
   xcrun simctl launch booted dev.voiceforge.app
   ```

#### Option B: Compile & Sign for Physical iPhone / iPad
Requirements: Mac with Xcode 15+ and Homebrew.
1. Install XcodeGen:
   ```bash
   brew install xcodegen
   ```
2. Generate the Xcode project:
   ```bash
   cd ios
   xcodegen generate
   open VoiceForge.xcodeproj
   ```
3. In Xcode, select the `VoiceForge` target, go to **Signing & Capabilities**, and select your personal Apple ID team.
4. Select your connected iPhone/iPad and press **Cmd + R** to install.
5. Connect your device to the same Wi-Fi as your computer and connect to `http://<YOUR_COMPUTER_IP>:8760`.
</details>

<details>
<summary><b><h3>6. Local Network & Headless Server Studio</h3></b></summary>

To host VoiceForge on a central home server, mini PC, or headless workstation and access it from any browser on your network:

```bash
voiceforge gui --host 0.0.0.0 --port 8760
```

Open `http://<SERVER_IP>:8760` from any browser on your iPhone, iPad, Android phone, Chromebook, or secondary laptop without installing any software on the client device.
</details>

---

## Core Modes & Capabilities

```
┌────────────────────────────────────────────────────────────────────────┐
│                          VOICEFORGE ENGINE MODES                       │
├─────────────┬──────────────────────────────────────────────────────────┤
│ 1. Train    │ Ingest speech recordings -> learn target voice weights  │
│ 2. Sing     │ Song input -> separate stems -> voice convert -> remix   │
│ 3. Speak    │ Text input -> Kokoro TTS -> RVC clone transfer -> output │
│ 4. Convert  │ Speech audio -> RVC voice transform -> output            │
│ 5. Separate │ Song input -> Demucs htdemucs -> isolated stems          │
└─────────────┴──────────────────────────────────────────────────────────┘
```

### 1. Train Voice
Ingests one or more clean voice recordings, verifies minimum duration (30 seconds mandatory threshold), extracts pitch contours via RMVPE and phonetic features via ContentVec, and trains an RVC v2 model on CPU with regular weights-only checkpoints.

### 2. Sing Mode
Feed any song (MP3, WAV, FLAC). VoiceForge splits the track into clean vocals and backing instruments with Demucs, transposes the vocals onto your trained voice model, applies your selected Index Strength, and seamlessly remixes the new voice over the original backing instrumentation.

### 3. Speak Mode
Type any sentence, paragraph, or script. Kokoro TTS (82M ONNX model) synthesizes natural spoken audio in under 2 seconds, which is immediately piped through your cloned voice model to produce realistic spoken dialogue in your voice.

### 4. Convert Mode
Transforms pre-recorded vocal clips, interviews, podcast segments, or game voice lines into your trained voice model. Provides fine-grained sliders for Pitch Shifting (-24 to +24 semitones), Feature Index Retrieval, and Consonant Protection.

### 5. Separate Mode
Standalone stem separator utilizing Demucs (htdemucs) running in small 7-second time slices to cleanly extract isolated acapellas and instrumentals without overflowing system memory.

---

## Scriptable CLI Reference

VoiceForge features a command-line interface suitable for scripting, automated batch processing, and headless operation.

```bash
# Add audio samples and build a voice dataset
voiceforge add-voice <VOICE_NAME> <FILES...>

# Train a voice model (specify epochs, default: 60)
voiceforge train <VOICE_NAME> [--epochs 60] [--dataset DIR]

# Create an AI song cover (with optional backing music remix)
voiceforge sing <SONG_FILE> --voice <VOICE_NAME> -o <OUTPUT_FILE> [--with-music] [--pitch 0]

# Synthesize speech from text in your voice
voiceforge speak "<TEXT>" --voice <VOICE_NAME> -o <OUTPUT_FILE>

# Convert dialogue or vocal audio into your voice
voiceforge convert <INPUT_FILE> --voice <VOICE_NAME> -o <OUTPUT_FILE> [--index-rate 0.85] [--protect 0.25] [--pitch 0]

# Separate a song into vocal and instrumental stems
voiceforge separate <SONG_FILE> [-o OUTPUT_DIR]

# List all trained voices available locally
voiceforge voices

# Launch graphical interfaces
voiceforge gui [--host 127.0.0.1] [--port 8760]
voiceforge desktop
voiceforge tui
```

### Parameter Reference Table

| Flag | Parameter | Default | Description |
|---|---|---|---|
| `--voice` | String | *Required* | Name of the trained voice model to apply. |
| `-o`, `--out` | File path | *Required* | Destination path for the mastered audio output. |
| `--epochs` | Integer | `60` | Number of training iterations over the dataset. |
| `--index-rate` | Float (0.0 to 1.0) | `0.85` | Retrieval strength of trained voice features. 1.0 = full clone timbre. |
| `--protect` | Float (0.0 to 0.5) | `0.25` | Consonant and breathing protection. Prevents robotic artifacts. |
| `--pitch` | Integer | `0` | Semitone pitch transposition (+12 octave up, -12 octave down). |
| `--with-music` | Flag | `False` | Mixes converted vocals back over the original instrumental track. |
| `--host` | IP Address | `127.0.0.1` | Network interface address for the Web Studio server. |
| `--port` | Integer | `8760` | TCP port for the Web Studio server. |

---

## Technical Architecture & Memory Engineering

VoiceForge is engineered around a fundamental principle: **Peak memory consumption must equal the single largest active stage, never the sum of all stages combined.**

```
[ Input Audio / Text ]
          │
          ▼
┌──────────────────────────────────────────────┐
│ STAGE 1: Source Separation                   │
│ Engine: Demucs (htdemucs)                    │
│ Memory Profile: 7s chunks, unloaded on exit  │
└──────────────────────┬───────────────────────┘
                       │
                       ▼
┌──────────────────────────────────────────────┐
│ STAGE 2: Acoustic Feature Extraction         │
│ Engines: RMVPE (Pitch) + ContentVec (HuBERT) │
│ Memory Profile: Streamed, zero-disk temp     │
└──────────────────────┬───────────────────────┘
                       │
                       ▼
┌──────────────────────────────────────────────┐
│ STAGE 3: Neural Voice Synthesis              │
│ Engine: Applio / RVC v2 (HiFi-GAN 40 kHz)    │
│ Memory Profile: 30s chunking with crossfades │
└──────────────────────┬───────────────────────┘
                       │
                       ▼
┌──────────────────────────────────────────────┐
│ STAGE 4: Broadcast Audio Mastering           │
│ Engine: FFmpeg Filtergraph                   │
│ Output: Highpass (70Hz) + EQ + -14 LUFS Norm │
└──────────────────────┬───────────────────────┘
                       │
                       ▼
               [ Mastered Audio ]
```

### Low-Resource Engineering Highlights:
- **Process Isolation:** Engines run in dedicated, short-lived subprocesses. When stem separation completes, the Demucs model completely frees its RAM before RVC is loaded.
- **Chunked Conversion Pipeline:** Songs of any length (from 30 seconds to 2 hours) are sliced into 30-second windows with 0.25-second crossfades. Peak RAM remains identical regardless of song duration.
- **Memory-Safe Training:** Batch size 1, gradient checkpointing, and weights-only checkpoint serialization ensure CPU training runs smoothly without system freeze or thrashing.
- **Dedicated Working Storage:** VoiceForge uses `~/.voiceforge/work/tmp` instead of `/tmp`, preventing out-of-disk crashes on systems that mount `/tmp` as a small RAM disk (tmpfs).

---

## Real-World Benchmarks

*Measured on standard reference hardware: 4 vCPU, 8 GB RAM, Intel Core i5 / AMD Ryzen 3 equivalent, NO GPU, CPU PyTorch runtime.*

| Workload | Input Length | Processing Time | Peak RAM Observed |
|---|---|---|---|
| **Voice Training (per epoch)** | 5 min dataset | ~90 seconds | 2.1 GB |
| **Speak Mode (Text-to-Speech + Clone)** | 1 sentence (~15 words) | ~45 seconds | 1.4 GB |
| **Voice Conversion** | 30 second speech clip | ~70 seconds | 1.8 GB |
| **Sing Mode (Vocal Separation + Clone + Remix)** | Full 3-minute song | ~4.5 minutes | 2.6 GB |
| **Stem Separation (Vocals + Instrumental)** | Full 3-minute song | ~95 seconds | 2.2 GB |

> [!NOTE]
> On modern processors (e.g. 8-core AMD Ryzen, Intel 12th/13th/14th Gen, or Apple Silicon M1-M4), processing speeds are **3x to 5x faster** across all benchmarks.

---

## Troubleshooting & Common Questions

<details>
<summary><b>Q: Do I need an NVIDIA graphics card or CUDA installed?</b></summary>
<b>No.</b> VoiceForge was created specifically to eliminate the requirement for discrete GPUs. All models run on CPU threads.
</details>

<details>
<summary><b>Q: Does any audio or voice data get transmitted to cloud servers?</b></summary>
<b>No.</b> After the initial one-time download of model weights during setup, VoiceForge operates 100% offline. There are zero analytics, no telemetry, and no external API calls.
</details>

<details>
<summary><b>Q: Error: "Voice sample too short (minimum 30 seconds required)"</b></summary>
A neural model requires sufficient acoustic data to map your vocal tract and formant patterns. Provide at least 30 seconds of speech. For optimal quality, 5 to 10 minutes is strongly recommended.
</details>

<details>
<summary><b>Q: The converted voice sounds muffled or raspy</b></summary>
1. Lower `--index-rate` slightly from `1.0` to `0.80` or `0.85`.
2. Raise `--protect` from `0.25` to `0.35`.
3. Check your original recording for background room echo or fan noise.
</details>

<details>
<summary><b>Q: The mobile companion cannot connect to the desktop studio</b></summary>
1. Verify both your computer and phone are connected to the exact same Wi-Fi network.
2. Launch the studio with network listening enabled: `voiceforge gui --host 0.0.0.0 --port 8760`.
3. Ensure port `8760` is not blocked by Windows Defender Firewall or your macOS firewall.
</details>

<details>
<summary><b>Q: How do I backup or transfer my trained voices to another machine?</b></summary>
Trained voice models are stored as portable files in `~/.voiceforge/models/<VOICE_NAME>/`. Each voice consists of a `.pth` model weights file and a `.index` feature retrieval file. Simply copy that folder to another computer's `~/.voiceforge/models/` directory; it will be recognized immediately.
</details>

---

## Ethics & Responsible Use

Voice cloning technology represents a significant creative breakthrough, but it must be exercised with responsibility:

1. **Consent is Mandatory:** Only clone your own voice or voices of individuals who have provided explicit, informed, and documented permission.
2. **No Deceptive Impersonation:** Do not use cloned voices to deceive, defraud, harass, or impersonate public figures, family members, or colleagues.
3. **Disclosure:** When sharing synthetic vocal tracks, AI song covers, or cloned audio publicly, clearly disclose that the audio was generated using AI voice cloning technology.

VoiceForge runs locally precisely so that your biometric vocal data remains under your sovereign control.

---

## License

VoiceForge is open-source software licensed under the [MIT License](LICENSE).

Third-party AI engines orchestrated by VoiceForge maintain their respective open-source licenses:
- **Applio / RVC v2:** MIT License
- **Demucs (htdemucs):** MIT License
- **Kokoro TTS:** Apache License 2.0
