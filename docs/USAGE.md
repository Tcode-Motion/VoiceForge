# VoiceForge usage

## Web GUI
`voiceforge gui`, then open http://127.0.0.1:8760
Three cards: Train a voice (drop files or record in the browser),
Make a song, Speak. Results play in the page and can be downloaded.

## Desktop GUI
`voiceforge desktop`
Same three jobs with file pickers and a live log.

## Terminal menu
`voiceforge tui`
Numbered menu covering every job.

## CLI reference
- `voiceforge add-voice NAME files...` validate and slice a sample
  (30 s minimum, enforced).
- `voiceforge train NAME [--epochs N] [--dataset DIR]`
- `voiceforge convert INPUT --voice NAME -o OUT [--index-rate 0..1]
  [--protect 0..0.5] [--pitch N]`
  - index-rate: how strongly the output copies the trained voice.
    0.85 is gentle, 1.0 is full strength.
  - protect: higher protects clear consonants and pronunciation.
- `voiceforge sing INPUT --voice NAME -o OUT [--with-music]`
- `voiceforge speak "text" --voice NAME -o OUT`
- `voiceforge separate INPUT` prints vocals and instrumental paths.
- `voiceforge voices` lists trained voices.

## Where things live
- Models: ~/.voiceforge/models/NAME/ (portable .pth + .index)
- Work files: ~/.voiceforge/work/
- Engines: ~/.voiceforge/engines/ (Applio, svc-venv, tts-venv)
Override engine locations with VF_APPLIO_DIR, VF_SVC_PYTHON and
VF_TTS_PYTHON environment variables.
