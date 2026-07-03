You are a network engineer analyzing a bizarre data exfiltration method used by a threat actor. During a traffic inspection, you intercepted two files:
1. `/app/key_audio.wav` - An intercepted VoIP audio stream.
2. `/app/obfuscated_encoder.py` - A highly obfuscated Python script used by the malware to encode network payloads before transmitting them.

Your analysis shows that the malware uses a custom encoding scheme, and the encryption key is transmitted out-of-band via the VoIP audio stream. 

Your objectives are:
1. Extract the encryption key from `/app/key_audio.wav`. The audio contains a synthesized voice speaking a sequence of digits.
2. Reverse engineer and audit `/app/obfuscated_encoder.py` to deduce the exact encoding algorithm used. Note that the obfuscated script might have intentional or unintentional flaws (CWEs) like weak custom cryptography.
3. Write a clean, functional Python script at `/home/user/clean_encoder.py` that implements the exact same encoding algorithm. 

Your script `/home/user/clean_encoder.py` must:
- Read plaintext from `stdin` until EOF.
- Use the numeric key you transcribed from the audio file.
- Output the resulting encoded text to `stdout` exactly as the malware's encoder would.

We will verify your solution by fuzzing `/home/user/clean_encoder.py` with random inputs and asserting that its output is bit-for-bit identical to our hidden reference oracle.