You are acting as a tier-3 support engineer. A client's audio diagnostic system has been crashing and producing mathematically impossible measurements. They have provided a corrupted log file and a buggy C program that parses raw audio signals and computes statistical metrics. 

You need to perform the following steps to collect diagnostics and fix the algorithmic issues:

1. **Format Parsing Edge-Case Repair & Numerical Instability Diagnosis**:
   The client provided the source code for their signal analyzer in `/home/user/audio_analyzer.c`. This program reads raw 16-bit PCM audio data from a file, parses a custom 32-byte header (which recently started receiving corrupted length headers due to a database/WAL journal failure upstream), and computes the Root Mean Square (RMS) and Variance of the signal. 
   Currently, the program:
   - Fails to parse headers where the length field (bytes 4-7, little-endian) is `-1` (0xFFFFFFFF), which is an edge-case indicating the stream length is unknown and should be read until EOF.
   - Suffers from catastrophic cancellation (numerical instability) when calculating the variance of audio streams with a large DC offset.
   
   Your task is to debug and fix `/home/user/audio_analyzer.c`. Update the parser to handle the `-1` length edge case (read until EOF instead of allocating a massive array and crashing). Update the variance calculation to use Welford's online algorithm or a robust two-pass algorithm to prevent precision loss. Compile your fixed program to `/home/user/audio_analyzer_fixed`.

2. **Diagnostic Collection**:
   The client has uploaded a diagnostic audio recording under `/app/diagnostic_recording.wav`. Note: This is a standard WAV file. You must use a tool like `ffmpeg` to convert it to raw 16-bit PCM (no header) and prepend the custom 32-byte header (the first 4 bytes are "DIAG", the next 4 bytes are 0xFFFFFFFF, followed by 24 null bytes) to create `/home/user/test_input.bin`.
   
   Run your fixed `/home/user/audio_analyzer_fixed` on `/home/user/test_input.bin`. Save the standard output exactly as it is to `/home/user/diagnostic_output.txt`.

3. **Regression Test Construction**:
   Create a bash script at `/home/user/run_regression.sh` that compiles the C program, generates a synthetic test signal with a massive DC offset (to test numerical stability), runs the fixed analyzer, and asserts the variance is strictly positive and accurate.

Ensure that `/home/user/audio_analyzer_fixed` reads from a file path provided as its first argument and prints two lines to stdout:
```
RMS: [value]
Variance: [value]
```
Format values to 6 decimal places.