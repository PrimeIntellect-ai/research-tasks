You are acting as a support engineer collecting diagnostics for a failing multithreaded audio processing utility.

We have received reports that our new C-based audio analysis tool, `process_audio`, frequently deadlocks under high contention and occasionally crashes with a segmentation fault. 

Here is what you need to do:
1. Navigate to the Git repository at `/home/user/audio_tool`. 
2. Analyze the `process_audio.c` source code. There are concurrency issues (a race condition / deadlock) and an off-by-one boundary error in the chunking logic causing the crashes. Fix these issues so the program runs reliably and produces the correct output.
3. The tool relies on an XOR decoding key to parse metadata from the audio files. A junior developer recently messed up the encoding logic and accidentally committed, then removed, the secret decoding key in the Git history. Use Git history forensics to find this secret key, and restore the correct decoding logic in `process_audio.c` (you might need to fix the serialization/encoding function).
4. Compile your fixed version to `/home/user/audio_tool/process_audio` (ensure it's executable).
5. Run your fixed tool on the provided diagnostic recording located at `/app/diagnostic_recording.wav` to extract the hidden diagnostic token. Write the extracted diagnostic token to `/home/user/diagnostic_token.txt`.

Your final compiled executable `/home/user/audio_tool/process_audio` must be functionally identical to our reference implementation. Our automated systems will fuzz your executable against an oracle binary using random inputs to ensure exact bit-for-bit output equivalence.