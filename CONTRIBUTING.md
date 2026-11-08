# Contributing to VoiceForge

VoiceForge has one hard rule: **it must stay runnable on a plain CPU
with 4 GB of RAM.** Every change is judged against the reference
machine (4 vCPU, 8 GB RAM, no GPU).

Guidelines:
- The `voiceforge` package itself uses the standard library only.
  Heavy engines stay in their own environments (see
  `scripts/setup_engines.sh`).
- Never load two engines in the same process. Run each stage as a
  subprocess and let it exit.
- Keep audio processing chunked; peak memory must not grow with file
  length.
- Test with `VF_APPLIO_DIR`, `VF_SVC_PYTHON` and `VF_TTS_PYTHON`
  pointing at a local engine install.
- No em dash characters in docs or UI text (project style rule).

Pull requests welcome: open an issue first for big changes.
