You have inherited an unfamiliar, partially broken Go codebase for an audio forensics tool located in `/home/user/src/audio-forensics/`. This tool is designed to analyze WAV files, process them using Fast Fourier Transforms (FFT) in parallel, and use a custom clustering algorithm to detect hidden steganographic anomalies.

Unfortunately, the previous developer left behind several critical bugs:
1. **Concurrency bugs**: The program frequently crashes or produces non-deterministic results when processing audio chunks due to a race condition.
2. **Precision loss**: The FFT or signal accumulation math suffers from severe floating-point precision loss, causing the anomaly scores to be wildly inaccurate.
3. **Convergence failure**: The internal clustering algorithm (used to establish baseline noise profiles) often fails to converge, hitting the maximum iteration limit and returning garbage centroids.

Your tasks:
1. Debug and fix the Go codebase in `/home/user/src/audio-forensics/`.
2. Compile the fixed binary to `/home/user/audio-detector`.
   - The binary must accept a single argument (the path to a WAV file): `/home/user/audio-detector <path_to_wav>`
   - It must exit with code `0` if the audio is "clean" (no anomaly), and exit with code `1` if the audio is "evil" (contains an anomaly).
3. As part of the investigation, there is a specific piece of audio evidence located at `/app/evidence_042.wav`. Use any available transcription tools (you may install them if needed, e.g., `whisper-ctranslate2` or standard `whisper.cpp`) to recover the spoken content of this file. Save the transcribed text to `/home/user/transcript.txt`.

Ensure your compiled binary `/home/user/audio-detector` is robust, as it will be tested against a hidden adversarial corpus of clean and evil audio files. It must perfectly separate the two datasets based on the fixed analytical math.