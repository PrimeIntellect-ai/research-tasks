I need your help debugging a multi-threaded Python audio processing service we use to filter out noise from speech recordings. Currently, the service has several critical issues: it occasionally deadlocks under high load, its memory usage grows indefinitely (memory leak), and it produces `NaN` values (numerical instability) when processing certain high-frequency signals.

The codebase is located at `/home/user/audio_service/`. You will find the main script `processor.py` there. It reads an audio file, chunks it, processes it using a custom frequency-domain filter across multiple threads, and writes the output.

Here is what you need to do:
1. **Analyze the Audio Trigger**: We captured a specific audio file that consistently triggers the numerical instability. It is located at `/app/trigger_signal.wav`. Use this to reproduce the `NaN` outputs. You'll need to use speech recognition (e.g., Whisper) to transcribe the spoken numbers in this audio file, as the sequence of numbers forms a passcode needed to decrypt a memory dump left by the previous engineer at `/home/user/audio_service/crash.dmp.enc`.
2. **Memory Dump Analysis & Git Forensics**: Decrypt the memory dump and analyze it to find the source of the memory leak (a data structure holding onto references). Furthermore, the custom filter relies on a calibration constant that was accidentally removed in a recent commit. Dig through the Git repository in `/home/user/audio_service/` to recover this constant and restore it in the code.
3. **Fix the Issues**: 
   - Correct the formula implementation in the filter to prevent numerical instability (division by near-zero values during normalization).
   - Fix the multi-threading deadlock (likely an issue with lock ordering or queue joining).
   - Resolve the memory leak.
4. **Produce the Final Program**: Save your fixed, single-threaded or safely multi-threaded implementation as `/home/user/audio_service/fixed_processor.py`. It must accept two command-line arguments: an input WAV file path and an output WAV file path. 

Your implementation must be bit-exact equivalent in its mathematical filtering output to our reference oracle, which you don't have access to, but it follows the exact same logic as the intended code with the bugs fixed and the correct calibration constant applied.