# VoiceForge for iOS

VoiceForge for iOS is a companion app that brings the VoiceForge studio experience to your iPhone and iPad.

The heavy AI audio processing runs entirely on your desktop or laptop computer; the iOS app connects to your computer over local Wi-Fi, offering a native mobile interface with dark styling and touch controls.

---

## Installation & Setup

### Option 1: Simulator Build (from GitHub Releases)
1. Download `VoiceForge-iOS-simulator.zip` from [VoiceForge Releases](https://github.com/Tcode-Motion/VoiceForge/releases).
2. Unzip the archive.
3. Open Terminal and install to your active iOS Simulator:
   ```bash
   xcrun simctl install booted VoiceForge.app
   xcrun simctl launch booted dev.voiceforge.app
   ```

### Option 2: Build from Source with Xcode (for Physical iPhone/iPad)
Requirements: macOS 13+, Xcode 15+, Homebrew

1. Install XcodeGen:
   ```bash
   brew install xcodegen
   ```
2. Generate the Xcode project:
   ```bash
   cd ios
   xcodegen generate
   ```
3. Open `VoiceForge.xcodeproj` in Xcode.
4. Select the `VoiceForge` target, go to **Signing & Capabilities**, and select your personal Apple ID or Development Team.
5. Connect your iPhone or iPad, select it as the run destination, and click **Run** (Command + R).

---

## Connecting to Your Studio

1. On your computer (Windows, macOS, or Linux), start VoiceForge with network listening:
   ```bash
   voiceforge gui --host 0.0.0.0 --port 8760
   ```
2. Find your computer's local IP address (e.g. `192.168.1.15`).
3. Connect your iOS device to the same local Wi-Fi.
4. Open VoiceForge on iOS, enter `http://192.168.1.15:8760`, and tap **Connect**.
5. When prompted, grant local network permission so the app can reach your computer.
