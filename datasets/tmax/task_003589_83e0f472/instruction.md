You are an operations engineer triaging an incident with our audio processing pipeline. A core component, written in C, performs adaptive noise cancellation on incoming audio streams. Recently, it has been failing on specific edge-case audio files.

We have a workspace at `/app/` containing:
1. `nlms_filter.c` - The source code for the adaptive filter.
2. `input.wav` - A sample 16-bit mono audio file that triggers the failures.
3. `memory.core` - A memory dump from a previous crashed instance in production.

Your objectives:
1. **Memory Dump Analysis**: Extract the 16-character calibration key from `/app/memory.core`. The key is stored as an ASCII string prefixed with `CALIB_KEY=`. You will need to pass this exact 16-character string as the third argument to the filter program.
2. **Boundary Condition Repair**: The current `nlms_filter.c` crashes with a segmentation fault (or heap corruption) when processing `input.wav`. Identify and fix the off-by-one error responsible for the crash.
3. **Numerical Instability Diagnosis**: Even when the crash is fixed, the filter fails to converge, exhibiting numerical instability (the output audio becomes pure clipping/static). The current implementation uses standard Least Mean Squares (LMS). Modify the weight update rule to use Normalized Least Mean Squares (NLMS) to prevent divergence. Specifically, normalize the update by the power of the input sample: `(x * x + 1e-6)`.
4. **Integration**: Compile your fixed `nlms_filter.c` into an executable named `/app/nlms_filter` (use `gcc -O2`). 
5. Run the compiled executable to process `/app/input.wav`, producing `/app/output.wav`. 
   Command format: `./nlms_filter /app/input.wav /app/output.wav <extracted_calib_key>`

A successful run will produce an `output.wav` where the adaptive filter successfully converges and suppresses the noise without blowing up.