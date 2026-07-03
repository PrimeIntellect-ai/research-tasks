You are a support engineer investigating a recurring crash in our audio telemetry pipeline. The pipeline crashes sporadically due to floating-point precision loss triggering an assertion failure deep inside a legacy proprietary library. 

You have been given two artifacts to start your investigation:
1. `/app/voicemail.wav`: A voicemail from the original library author. You must transcribe this audio to find the exact numerical threshold at which the legacy library asserts a precision failure.
2. `/app/crash.dmp`: A raw memory dump from the last crashed process. The crash dump contains the directory paths to the test corpora (a set of known "clean" telemetry files and known "evil" telemetry files that cause the crash). 

Your objective is to build a pre-flight validator that can sanitize incoming telemetry files *before* they are sent to the legacy library.

**Instructions:**
1. **Extract Corpora Paths:** Analyze `/app/crash.dmp` to extract the hidden file paths for the "evil" and "clean" test corpora. The paths are absolute and begin with `/app/corpora/`.
2. **Determine the Threshold:** Transcribe `/app/voicemail.wav` to find the exact decimal value of the precision loss threshold.
3. **Build the Sanitizer:** Write a C program at `/home/user/audio_sanitizer.c` and compile it to an executable at `/home/user/audio_sanitizer`.

**Sanitizer Specification:**
- The compiled executable must accept exactly one argument: the absolute path to a telemetry file.
    `./audio_sanitizer <file_path>`
- Telemetry files are binary files containing an unknown number of raw, 32-bit single-precision floating-point numbers (little-endian IEEE 754).
- The sanitizer must simulate the pipeline's accumulation to track precision loss.
- Initialize `float float_sum = 0.0f;` and `double double_sum = 0.0;`.
- For each float `x` read from the file:
  - Add `x` to `float_sum`.
  - Add `(double)x` to `double_sum`.
  - Check the absolute difference: `fabs((double)float_sum - double_sum)`.
  - If the absolute difference strictly exceeds the threshold found in the voicemail, the program must immediately terminate with **exit code 1** (rejecting the file as "evil").
- If the program reaches the end of the file without the difference ever exceeding the threshold, it must terminate with **exit code 0** (accepting the file as "clean").

Your sanitizer will be tested against the hidden test corpora. To succeed, it must reject 100% of the files in the evil corpus and accept 100% of the files in the clean corpus.