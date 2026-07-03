You are a performance engineer tasked with debugging and fixing an unreliable C++ audio processing pipeline. 

The pipeline consists of a C++ program that reads an audio file, applies block-wise variance normalization, applies a FIR filter, and writes the output. However, the current implementation has several critical issues:

1. **Intermittent Failures:** The program uses multiple threads to process blocks of audio, but it occasionally produces corrupted audio or crashes. You need to identify and fix the concurrency bug causing this intermittent failure.
2. **Numerical Instability:** The variance calculation used for audio normalization suffers from catastrophic cancellation, occasionally resulting in negative variances and `NaN` values in the output audio. You must diagnose and replace it with a numerically stable algorithm (e.g., Welford's method or a robust two-pass approach).
3. **Missing Filter Coefficients (Binary Reverse Engineering):** The original filter coefficients were lost, and the current code uses a dummy array. However, a legacy shared object file `/home/user/libfilter.so` contains the original 8-tap `float` array exported under the symbol `taps_array`. You must inspect or decompile this binary to extract the exact 8 floating-point values and hardcode them into your fixed C++ program.

**Files provided:**
- `/app/audio/input.wav`: The input audio file (16-bit PCM, Mono, 16000 Hz).
- `/home/user/processor.cpp`: The buggy C++ source code.
- `/home/user/libfilter.so`: The compiled shared library containing the target filter taps.

**Your Objective:**
1. Fix the bugs in `/home/user/processor.cpp`.
2. Extract the correct filter taps from `/home/user/libfilter.so` and update the C++ code.
3. Compile your fixed program: `g++ -O3 -pthread /home/user/processor.cpp -o /home/user/processor`
4. Run your program: `/home/user/processor /app/audio/input.wav /home/user/output.wav`

The final output MUST be a valid WAV file located at `/home/user/output.wav`. 

Ensure your threading model safely processes all blocks, your math is strictly stable, and the exact filter taps are applied. The evaluation system will measure the Mean Squared Error (MSE) of your audio output against a pristine reference.