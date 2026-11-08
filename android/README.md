# VoiceForge for Android

VoiceForge for Android is a companion app that lets you control your VoiceForge studio directly from your smartphone or tablet over your local Wi-Fi network.

The heavy AI engines (RVC, Demucs, Kokoro TTS) run on your computer (CPU-only, no GPU required); the Android app provides an optimized touch-friendly client interface.

---

## Installation & Setup

### Method 1: Download Pre-built APK (Recommended)
1. Go to the [VoiceForge GitHub Releases](https://github.com/Tcode-Motion/VoiceForge/releases) page.
2. Download `VoiceForge-Android.apk` directly onto your Android device (or transfer via USB).
3. Tap the downloaded APK to install (enable "Install unknown apps" in Settings if prompted).

### Method 2: Build from Source
Requirements: Android SDK 34, JDK 17, Gradle 8.7+
```bash
cd android
gradle assembleDebug
```
The output APK will be generated at `app/build/outputs/apk/debug/app-debug.apk`.
Install to a connected Android device using ADB:
```bash
adb install app/build/outputs/apk/debug/app-debug.apk
```

---

## Connecting to Your Studio

1. On your computer (Windows, macOS, or Linux), start VoiceForge with local network access enabled:
   ```bash
   voiceforge gui --host 0.0.0.0 --port 8760
   ```
2. Find your computer's local network IP:
   - **Windows**: run `ipconfig` (look for IPv4 Address, e.g. `192.168.1.15`)
   - **macOS / Linux**: run `ip a` or `ifconfig`
3. Ensure your phone is connected to the same Wi-Fi network as your computer.
4. Open VoiceForge on your phone, enter your computer address (e.g. `http://192.168.1.15:8760`), and tap **Connect**.
5. You now have full access to Train, Sing, Speak, Convert, and Separate on your phone!
