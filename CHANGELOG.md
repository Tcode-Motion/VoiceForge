# Changelog

## 1.0.0.1 (2026-11-08)

- Fixed GitHub Release CI workflow:
  - macOS desktop build: bundled Pillow dependency and native `.icns` asset so PyInstaller icon conversion succeeds on macOS.
  - Windows desktop build: bundled native `.ico` icon and set matrix `fail-fast: false` to ensure builds continue independently.
  - Android APK build: upgraded to `android-actions/setup-android@v4` with clean `platform-tools` and `build-tools;34.0.0` packages to avoid the deprecated `tools` package error.
  - iOS companion build: added missing `info.path: VoiceForge/Info.plist` and explicit `VoiceForge/Info.plist` to prevent XcodeGen decoding failures.
  - Cross-platform release packaging: automatically publishes Windows (.zip), macOS (.zip), Linux (.tar.gz), Android APK, iOS simulator (.zip), and Python distribution wheel/sdist packages.
- Platform Setup & Engine installation scripts:
  - Added native Windows PowerShell script (`scripts/setup_engines.ps1`) and Command Prompt batch script (`scripts/setup_engines.bat`).
  - Updated engine path resolution in `src/voiceforge/config.py` to support Windows paths (`Scripts/python.exe`) as well as POSIX paths (`bin/python`).
- Expanded README and documentation:
  - Detailed cross-platform setup instructions for Windows, macOS, Linux, Android, iOS, and Web/Docker.
  - Comprehensive CLI usage examples, engine architecture, benchmarks, and troubleshooting steps.


## 1.3.0

- Desktop app rebuilt: it now opens the web studio itself inside a
  native app window (pywebview), so the desktop look is the web look,
  pixel for pixel, on Windows, macOS and Linux. Without pywebview it
  opens the same studio in the browser.
- Web GUI is now phone friendly: navigation becomes a top bar on
  small screens instead of disappearing.
- Android companion restyled in the studio palette with a proper app
  icon; iOS companion restyled dark with a waveform brand header and
  an app icon.
- README expanded with screenshots for web, desktop and phone.

## 1.2.1 (2026-11-08), first GitHub release
- Repository completed: professional README, Code of Conduct,
  Security policy, issue and PR templates.
- CI: tests on every push; release workflow builds Windows, macOS
  and Linux desktop apps (PyInstaller), the Android companion APK
  and the iOS companion (unsigned simulator), and publishes them
  as a GitHub release.
- Android and iOS companion apps added (studio interface; engines
  stay on the computer).

## 1.2.1 fixes
- Fix: engines no longer depend on /tmp (some systems mount it as a
  tiny tmpfs and jobs died with disk-full errors). Temp files now
  live under the VoiceForge work folder.
- Fix: web GUI dropzones now show the chosen file name correctly.
- Fix: desktop GUI voice list updates on the UI thread (it could
  throw "main thread is not in main loop"); the internal done marker
  no longer leaks into the log.


## 1.2.0 (2026-11-08)
- Premium redesign of both GUIs: near-black surfaces, hairline
  borders, one restrained lime accent, white primary actions, real
  SVG iconography (no emoji), custom sliders and toggle switches,
  grouped sidebar (Create / Library), engine status card.
- New minimal logo: dark tile, white voice bars, one lime bar.


## 1.1.0 (2026-11-08)
- Web GUI rebuilt: sidebar navigation (Train, Sing, Speak, Convert,
  Separate, Voices), header status pills, voice-strength and clarity
  sliders, live job console with progress state and in-page playback.
- Desktop GUI rebuilt: ttk pro theme, sidebar navigation, one page per
  job, sliders, status bar and log console.
- New web/desktop jobs: Convert and Separate are now in the GUIs too,
  plus a Voices list.
- Docs: troubleshooting guide added.

## 1.0.0 (2026-11-08)
- First release. CLI, terminal menu, web GUI, desktop GUI.
- Chunked low-RAM conversion, memory-safe training profile, Demucs
  separation, Kokoro speak mode, 30-second sample minimum.
