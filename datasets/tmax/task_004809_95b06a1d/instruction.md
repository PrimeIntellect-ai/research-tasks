A legacy audio processing pipeline we use for transcribing and analyzing ultrasonic telemetry signals has broken. A regression was introduced somewhere in the last 200 commits of our local Git repository located at `/home/user/telemetry_repo`. The script `process_audio.sh` is supposed to extract peak frequency windows from WAV files, but it's currently suffering from floating-point precision errors (it truncates values instead of rounding them properly, causing subsequent query lookups to fail).

Your task is to:
1. Repair the environment: The repository currently fails to run because the `bc` calculator scale environment variable `MATH_SCALE` is misconfigured in the global `.bashrc`. Fix it so the default precision is exactly 6 decimal places.
2. Bisect the repository: Use `git bisect` to find the exact commit that introduced the floating-point truncation regression in `process_audio.sh` (where `awk` was replaced with a flawed `bc` command). You can test the commits against the provided reference audio file `/app/telemetry_sample.wav`.
3. Create a minimal reproducible example and fix: Write a standalone Bash script at `/home/user/fixed_extractor.sh` that takes an input frequency string and an offset, and correctly performs the floating-point addition to 6 decimal places with proper rounding (fixing the bug found in the bisected commit).

The script `/home/user/fixed_extractor.sh` must:
- Accept exactly two arguments (e.g., `145.234` and `0.005`).
- Output the exact floating point result of their sum, rounded to 6 decimal places.
- Be implemented entirely in Bash using `bc` or `awk`.

Finally, run the fixed logic over `/app/telemetry_sample.wav` using your corrected environment, and save the single highest peak frequency extracted to `/home/user/peak_result.txt`.