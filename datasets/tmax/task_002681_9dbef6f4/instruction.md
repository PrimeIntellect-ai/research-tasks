You are an engineer tasked with repairing and setting up a robust test pipeline for a C-based audio processing tool. 

In `/home/user/src/` you will find `audio_filter.c`, a simple command-line utility designed to apply a 3-tap moving average filter to 16-bit PCM mono WAV files. Currently, the code has memory safety issues and undefined behaviors that cause it to crash or produce corrupted audio.

Your objectives are:
1. **Fix the C Code:** Identify and repair the memory safety bugs, out-of-bounds accesses, and uninitialized variables in `/home/user/src/audio_filter.c`. The filter logic itself should be a simple unweighted 3-tap causal moving average: `y[n] = (x[n] + x[n-1] + x[n-2]) / 3` (treating out-of-bounds prior samples as 0).
2. **Build and Test Pipeline:** Write a Bash script at `/home/user/build_and_test.sh` that sets up a polyglot build system. The script must:
   - Compile `audio_filter.c` with AddressSanitizer and UndefinedBehaviorSanitizer enabled.
   - Implement property-based testing: Generate at least 5 random raw data files of varying sizes (e.g., using `/dev/urandom`), wrap them in a dummy WAV header, and run the compiled filter on them to verify it does not crash or trigger sanitizer errors.
   - If all tests pass, recompile the tool with standard optimizations (`-O3`) into an executable named `/home/user/audio_filter_release`.
   - Run the release executable on the audio fixture provided at `/app/test_speech.wav` to produce the final output file `/home/user/filtered.wav`.

Constraints:
- Do not use external build tools like Make or CMake; rely entirely on Bash built-ins, coreutils, and `gcc` inside your `build_and_test.sh` script.
- Ensure your Bash script is executable and exits with a non-zero code if any step fails.
- The final output `/home/user/filtered.wav` must have the exact same format and length as the input, with the filter correctly applied.

Execute your script to produce `/home/user/filtered.wav`. An automated verification process will evaluate the quantitative accuracy of your output audio against a golden reference.