You are acting as a security researcher analyzing a custom data exfiltration tool used by a threat actor. The actor has been exfiltrating audio recordings from compromised systems by encoding them into a proprietary binary format. 

We have recovered the source code for their tools: `/app/encoder.cpp` and `/app/decoder.cpp`, as well as a sample original audio file they were testing with, located at `/app/suspicious_payload.wav`.

Your objective is to fix these programs so we can reliably decode their payloads. Currently, the toolchain is broken:
1. `decoder.cpp` fails to compile due to missing dependencies and type errors.
2. Even after fixing the build, the decoder crashes (segfaults) when processing files created by the encoder.
3. The encoder itself seems to have a serialization bug—it incorrectly packs the audio data structs, writing memory addresses instead of actual PCM data in one of its serialization routines.

Your tasks:
1. Diagnose and fix the build failures in `/app/decoder.cpp`.
2. Analyze the crash in `decoder.cpp` (using `gdb` or core dumps) and patch the memory/buffer management issue.
3. Fix the serialization logic in `/app/encoder.cpp` so that it correctly packs the WAV data without corrupting it.
4. Compile both tools using `g++`.
5. Run your fixed encoder on `/app/suspicious_payload.wav` to produce an encoded binary file.
6. Run your fixed decoder on that binary file to reconstruct the audio.
7. Save the final reconstructed audio file exactly at `/home/user/recovered.wav`.

The recovered audio must be functionally identical to the original payload. An automated system will compare `/home/user/recovered.wav` against `/app/suspicious_payload.wav` using Mean Squared Error (MSE) on the audio samples. Ensure the audio header and data are intact.