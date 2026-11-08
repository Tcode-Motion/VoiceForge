# Security Policy

## Supported versions

| Version | Supported |
|---|---|
| 1.2.x | Yes |
| Older | No |

## Reporting a problem

If you find a security problem in VoiceForge, please report it
privately by email to majumdertanmoy510@gmail.com. Do not open a
public issue for security problems. You will get a reply within a
few days, and a fix or a clear explanation as fast as practical.

## How VoiceForge handles your data

- **Fully offline after setup.** The one-time engine installer
  downloads open-source engines. After that, VoiceForge runs with
  HuggingFace offline mode and telemetry disabled, and needs no
  network at all.
- **Your voice stays yours.** Recordings, trained models and outputs
  live only in your VoiceForge folders (default ~/.voiceforge).
  Nothing is uploaded, shared or phoned home.
- **Local web GUI.** The web interface binds to 127.0.0.1 by
  default. Do not expose it to the public internet; if you open it
  to your local network for the phone apps, only do so on a network
  you trust.
- **Only clone voices you own or have permission to use.** This is
  a licence condition of responsible use, and it matters.

## Scope notes

VoiceForge drives three external engines (Applio/RVC, Demucs,
Kokoro). Vulnerabilities in those engines should also be reported
to their upstream projects.
