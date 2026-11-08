# Troubleshooting

## "Voice sample too short"
Training needs at least 30 seconds of one person's voice in total.
Add more recordings, or record a longer one. 5 to 10 minutes gives a
clearly better voice.

## Training stops or the computer runs out of memory
VoiceForge already uses the safe profile (batch size 1, gradient
checkpointing, weights saved regularly). If it still stops:
- Close other heavy programs during training.
- Lower the epochs and resume later; weights are saved as it goes.
- Make sure nothing else is converting at the same time. One engine
  at a time is the design.

## The converted voice sounds like the original singer
Raise Voice strength (index rate) toward 1.0. Lower values keep more
of the source singer.

## Words sound unclear
Raise Clarity protect toward 0.3 to 0.4. Very high values can make
the voice sound thinner, so move in small steps.

## Engines not found
Run `bash scripts/setup_engines.sh` once, or point VoiceForge at an
existing install:
- VF_APPLIO_DIR: folder containing Applio's core.py
- VF_SVC_PYTHON: python of the engine venv (torch, demucs, applio)
- VF_TTS_PYTHON: python of the Kokoro venv

## Everything is slow
That is the CPU trade. Short clips convert in a few minutes on the
reference machine. Separation and conversion times grow linearly with
song length; training is the slowest part (about 1.5 minutes per
round for a small dataset).
