You are a security researcher analyzing a new malware variant that uses audio files for command-and-control communication. The malware extracts hidden commands from WAV files using a specific steganographic algorithm and an embedded XOR key.

You have been provided with the following artifacts:
1. `/app/signal.wav`: An intercepted audio transmission. The spoken content in this file contains a 4-digit PIN code that the malware uses as a secondary encryption key. You will need to transcribe this audio to find the PIN.
2. `/app/malware.dmp`: A process memory dump taken right before the malware crashed. The 4-byte hexadecimal XOR key used by the steganography algorithm is stored in this dump in plain text, prefixed by the string `XOR_KEY_SIG=`.
3. `/app/tools/`: A directory containing a helpful analysis script `analyze_wav.py`. However, its `requirements.txt` has conflicting dependency versions (e.g., conflicting `numpy` and `scipy` versions).

Your tasks:
1. **Transcribe the audio:** Recover the 4-digit PIN spoken in `/app/signal.wav`. (You can use `ffmpeg`, `whisper`, or any available tools).
2. **Extract the Key:** Extract the 4-byte XOR key from `/app/malware.dmp`.
3. **Resolve Dependencies:** Fix the dependency conflicts in `/app/tools/requirements.txt` so you can install them in a virtual environment and use the tools if needed.
4. **Reconstruct the Decoder:** Write a standalone Python script at `/home/user/decode.py` that takes exactly two arguments: the path to a WAV file and a 4-digit PIN. 
   
   The script must implement the malware's exact decoding logic:
   - Read the audio data as 16-bit PCM (mono).
   - Extract the Least Significant Bit (LSB) of the first 256 audio frames.
   - Pack these 256 bits into 32 bytes (big-endian).
   - XOR each of the 32 bytes with the 4-byte XOR key (repeating the key cyclically).
   - XOR the resulting 32 bytes with the 4-digit PIN (treated as a 32-bit integer, big-endian).
   - Print the final 32 bytes to standard output as a lowercase hex string.

Your final goal is to ensure `/home/user/decode.py` perfectly mimics the malware's extraction logic. We will test your script by fuzzing it with thousands of random WAV files and comparing its output to our known-good reference decoder.