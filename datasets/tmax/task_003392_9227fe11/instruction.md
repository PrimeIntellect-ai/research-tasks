I am a developer working on a distributed mathematical audio transcription pipeline, and our CI build is completely broken. I need your help to debug and fix it, as well as implement a new security filter to prevent further pipeline crashes.

Here is the situation:

1. **Build Failures & Concurrency Issues**:
   The code is located in `/home/user/math_pipeline/`. If you run `pytest` there, it fails for two reasons:
   * A race condition in `processor.py` causes intermittent failures when concurrent worker threads update the shared `/home/user/math_pipeline/metrics.json` file. You need to fix this race condition (e.g., by adding proper file locking or thread synchronization) so the tests pass reliably.
   * A format parsing edge-case in `wav_parser.py`. The custom parser crashes when reading WAV files that have an 18-byte 'fmt ' chunk (instead of the standard 16 bytes). Fix the parser so it handles extra chunk data gracefully.

2. **Adversarial Audio Filter**:
   We are being hit by synthetic "adversarial" audio files that cause mathematical overflow errors in our downstream Fourier analysis. These malicious files contain extreme, non-physical synthetic discontinuities: specifically, an absolute difference between two consecutive 16-bit PCM audio samples that is strictly greater than `20000`. 
   You must create a script at `/home/user/math_pipeline/sanitizer.py`. It should take a single argument (the path to a WAV file).
   * If the file is CLEAN (no consecutive samples have an absolute difference > 20000), the script MUST exit with status code `0`.
   * If the file is EVIL (contains at least one pair of consecutive samples with an absolute difference > 20000), the script MUST exit with status code `1`.
   We have automated tests that will grade your `sanitizer.py` against a hidden corpus of clean and evil files.

3. **Audio Fixture Analysis**:
   Before the pipeline broke, one of our worker nodes crashed while processing a specific audio file. The file is located at `/app/mystery_signal.wav`. You need to determine what mathematical constant is spoken in this audio file.
   Write the numerical digits of the spoken constant (digits only, no spaces or punctuation) into a file at `/home/user/constant.txt`. You may use tools like `ffmpeg` or install a local transcription tool to analyze it.

Please fix the build, write the sanitizer, and extract the secret constant!