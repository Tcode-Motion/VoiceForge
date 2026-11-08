# Examples

Train a voice from three short recordings and use it:

```bash
voiceforge add-voice demo part1.wav part2.wav part3.wav
voiceforge train demo --epochs 60
voiceforge speak "This is my own voice, made on my own computer" --voice demo -o demo_speak.wav
voiceforge sing any_song.mp3 --voice demo -o demo_vocals.wav
voiceforge sing any_song.mp3 --voice demo --with-music -o demo_cover.wav
```
