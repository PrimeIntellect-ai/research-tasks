You are a security researcher analyzing an incident where a suspicious audio file caused a crash in an audio processing service. 

You have been provided with an adversarial audio file located at `/app/suspicious.wav`. This file contains a hidden high-frequency payload (noise) that triggers a vulnerability in our downstream processing pipeline. 

Your task consists of two parts:

1. **Investigate the Payload**: We know the malicious payload relies on high-frequency energy. You need to write a Python script `/home/user/fix_audio.py` that reads `/app/suspicious.wav`, applies a low-pass filter to remove the malicious high-frequency payload, and writes the sanitized audio to `/home/user/clean.wav`.
   - Use a 5th-order Butterworth low-pass filter.
   - Set the cutoff frequency to 4000 Hz.
   - Ensure you handle the audio data correctly (preserve the original sample rate, and ensure the output is a valid 16-bit PCM WAV file).
   - You may use standard Python libraries like `scipy`, `numpy`, and `soundfile` or `wavfile`.

2. **Validation**: Your filtered audio `/home/user/clean.wav` will be evaluated by an automated testing suite that compares it against a strictly mathematically defined reference filter. You must implement the filter accurately to minimize the Mean Squared Error (MSE) between your output and the reference.

Ensure that your `fix_audio.py` script is self-contained and successfully generates `/home/user/clean.wav` when run.