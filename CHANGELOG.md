# Changelog

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
