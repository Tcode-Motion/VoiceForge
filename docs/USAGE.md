# VoiceForge Usage Guide

VoiceForge provides four interfaces to the same underlying audio engines:
a Desktop GUI, a Web Studio, an Interactive Terminal (TUI), and a scriptable CLI.

---

## 1. Web Studio
Start the local server:
```bash
voiceforge gui
```
Open `http://127.0.0.1:8760` in any web browser.

To allow other devices (such as your phone, tablet, or another laptop on your Wi-Fi) to connect:
```bash
voiceforge gui --host 0.0.0.0 --port 8760
```

The Web Studio features:
- **Train Voice**: Drop WAV/MP3 files or record directly in the browser via microphone.
- **Sing Mode**: Upload a song, select your trained voice, adjust pitch shift and index rate, and choose whether to mix back the original backing track.
- **Speak Mode**: Type any text and hear it spoken in your cloned voice via Kokoro TTS + RVC.
- **Convert Mode**: Transform speech or dialogue audio clips into your target voice.
- **Separate Mode**: Split any song into clean isolated vocals and instrumental stems.
- **Voices Library**: Inspect, test, and manage all your trained voice models.

---

## 2. Desktop GUI
Launch the native desktop window:
```bash
voiceforge desktop
```
Runs the studio inside a native window (powered by pywebview). If pywebview is not installed, it automatically launches the studio in your default browser.

---

## 3. Terminal Menu (TUI)
For keyboard-driven terminal workflows:
```bash
voiceforge tui
```
Provides an interactive numbered menu to add voice samples, train models, run conversions, and split tracks.

---

## 4. Scriptable CLI Reference

### Add Voice Sample
Ingests and validates raw audio recordings for a new voice:
```bash
voiceforge add-voice <VOICE_NAME> <AUDIO_FILES...>
```
Example:
```bash
voiceforge add-voice tanmoy sample1.wav sample2.mp3 sample3.m4a
```
*Note: A minimum of 30 seconds of clean speech is required. 5 to 10 minutes is recommended.*

### Train Voice Model
Trains a voice model on CPU with low-RAM parameters:
```bash
voiceforge train <VOICE_NAME> [--epochs 60] [--dataset DIR]
```
Example:
```bash
voiceforge train tanmoy --epochs 80
```

### Voice Conversion (Speech to Voice)
Converts any speech or vocal audio into your trained voice:
```bash
voiceforge convert <INPUT_AUDIO> --voice <VOICE_NAME> -o <OUTPUT_AUDIO> [OPTIONS]
```
Options:
- `--index-rate 0.0..1.0`: Feature retrieval strength (default: 0.85). 1.0 is full target voice clone; lower values retain more original vocal nuances.
- `--protect 0.0..0.5`: Consonant and breath protection (default: 0.25). Higher protects clarity and articulation.
- `--pitch <SEMITONES>`: Pitch adjustment (e.g. `+12` for female to male, `-12` for male to female).

### Sing Mode (Song Cover Generator)
Automatically separates vocals, converts them to your voice, and optionally mixes with the backing track:
```bash
voiceforge sing <SONG_FILE> --voice <VOICE_NAME> -o <OUTPUT_FILE> [--with-music] [--pitch 0]
```
Example:
```bash
voiceforge sing song.mp3 --voice tanmoy -o cover.wav --with-music
```

### Speak Mode (Text to Voice)
Synthesizes speech from typed text, then transfers your trained voice onto it:
```bash
voiceforge speak "<TEXT>" --voice <VOICE_NAME> -o <OUTPUT_FILE>
```
Example:
```bash
voiceforge speak "Welcome to VoiceForge, the offline voice cloning studio." --voice tanmoy -o speech.wav
```

### Stem Separation
Splits any audio file into clean vocals and instrumental tracks:
```bash
voiceforge separate <SONG_FILE> [-o OUTPUT_DIR]
```

### List Voices
Lists all available trained models and their status:
```bash
voiceforge voices
```

---

## 5. Storage Locations
- **Trained Models**: `~/.voiceforge/models/<VOICE_NAME>/` (portable `.pth` weights + `.index` feature index)
- **Work Directory**: `~/.voiceforge/work/` (temporary stems, segmented chunks, and processing cache)
- **Engine Binaries**: `~/.voiceforge/engines/` (Applio, Demucs, Kokoro, and virtual environments)

### Environment Variable Overrides
- `VF_HOME`: Base configuration directory (default: `~/.voiceforge`)
- `VF_MODELS_DIR`: Directory where trained voice models are stored
- `VF_WORK_DIR`: Working and temporary file directory
- `VF_APPLIO_DIR`: Path to the Applio root directory
- `VF_SVC_PYTHON`: Path to the Python executable with Torch, Demucs, and Applio dependencies
- `VF_TTS_PYTHON`: Path to the Python executable with Kokoro TTS dependencies
