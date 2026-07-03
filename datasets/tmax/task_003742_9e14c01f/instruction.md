You are an operations engineer triaging a severe incident in our data processing cluster. Our ingestion pipeline is crashing due to "poisoned" audio files that cause massive precision loss and NaN propagation in our legacy transcription service.

Your task involves several steps to mitigate this incident:

1. **Fix the Filter Skeleton**: We started building a Rust-based pre-filter at `/home/user/wav_filter` to drop these malicious files before they hit the transcription service. However, the developer left mid-incident, and the project currently fails to compile due to linker errors related to a legacy C object (`libwavcheck.a`) integrated into the project. Diagnose the compiler/linker errors and fix the build configuration so that `cargo build` succeeds.
2. **Implement the Detection Logic**: Complete the Rust program (`src/main.rs`). The compiled binary must accept a single argument (the path to a WAV file). It must parse the WAV file and detect the precision loss attack. The malicious files are encoded as 32-bit IEEE Float PCM, but they contain engineered anomalies in their sample data (specifically, injected `NaN` or `Infinity` values) that trigger the downstream crashes. Clean files are standard 16-bit PCM or valid normalized 32-bit float PCM.
    * If the file is malicious (contains `NaN` or `Infinity` samples), the program MUST exit with status code `1`.
    * If the file is clean, the program MUST exit with status code `0`.
3. **Verify**: Ensure your binary at `/home/user/wav_filter/target/debug/wav_filter` works perfectly. Our automated CI will test your executable against two hidden corpora: an "evil" corpus of poisoned files and a "clean" corpus of normal audio files.
4. **Transcribe Quarantine File**: We have isolated one of the triggering audio files from the incident at `/app/quarantine/incident_099.wav`. Interestingly, it contains a spoken message hidden in the noise. You must extract/transcribe the spoken English content from this audio file. Write the transcribed text to `/home/user/transcript.txt` (lowercase, no punctuation).

Constraints:
- You may use any standard Rust crates (e.g., `hound`, `byteorder`) by adding them to `Cargo.toml`.
- You can install any system packages required to transcribe the audio file (e.g., `ffmpeg`, `whisper.cpp`, or python transcription libraries).