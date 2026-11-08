# VoiceForge on low-resource machines: design notes

VoiceForge targets computers with no GPU and 4 to 8 GB of RAM. These
are the techniques it uses, and why.

## 1. Sequential stages, one engine in memory
Separation, feature extraction, training, conversion and TTS each run
as separate short-lived processes. When a stage ends, its memory is
fully returned to the OS. Peak RAM equals the largest single stage.

## 2. Chunked inference with crossfades
Conversion splits input into 30-second chunks. Each chunk is converted
in a fresh engine process and freed. Chunks join with 0.25-second
triangular crossfades, which removes clicks at the seams. Memory use
is constant in the length of the audio; time grows linearly.

## 3. Gradient checkpointing and batch size 1 for training
Training recomputes activations instead of storing them (gradient
checkpointing), trading a little speed for a large memory cut. Batch
size 1 keeps the working set minimal on CPU.

## 4. Weights-only checkpoints, saved often
Full GAN checkpoints (generator + discriminator + optimiser) are the
memory and disk peak of RVC training. VoiceForge saves compact
inference weights regularly and keeps only the newest full checkpoint,
so a crash or power cut never loses the whole run.

## 5. Small separation segments
Demucs normally holds a long window of audio. VoiceForge sets the
segment to 7 seconds, which caps the separation working set while
keeping quality for vocal work.

## 6. Small, CPU-shaped models
- RMVPE for pitch: accurate for singing, much lighter than CREPE-full.
- ContentVec (HuBERT) features at 40 kHz training rate.
- Kokoro TTS: 82M parameters, ONNX runtime, designed to run in real
  time on CPUs; int8 builds exist for even smaller footprints.

## 7. Thread discipline
OpenMP/BLAS thread pools are capped (OMP_NUM_THREADS=2 by default).
On small machines, uncapped pools duplicate buffers and can use more
memory than the model itself.

## 8. Offline by construction
All engine processes run with HF_HUB_OFFLINE=1 and telemetry disabled.
After the one-time setup download, VoiceForge needs no network at all.

## Tuning knobs
- VF_HOME: where engines, models and work files live.
- Chunk length: convert.py CHUNK_SECONDS via config (30 s default;
  lower it if RAM is under 4 GB).
- Epochs: more rounds help up to a point; 40 to 100 is the useful
  range for 5 to 10 minutes of voice.
