You are an open-source maintainer reviewing a broken Pull Request for a C-based audio processing library called `libwav-safe`. 

The PR attempts to add a robust WAV file validator and a SQLite-based logging system, but the contributor left it in a broken state. 

Here is what you need to do to fix the PR and prepare it for merge:

1. **Audio Fixture & Schema Migration**: The contributor forgot to document the new database schema, but left an audio note at `/app/voicemail.wav`. Extract the audio file's metadata (specifically the `artist` tag) using standard tools like `ffmpeg` or `ffprobe`. This tag contains a comma-separated list of the column names required for the v2 SQLite schema. 
Create a bash script `/home/user/migrate.sh` that creates a SQLite database at `/home/user/metadata.db` with a table named `audio_logs` containing the exact columns specified in the metadata (all as `TEXT` types).

2. **Fix the WAV Validator**: At `/home/user/wav_validator.c`, the contributor started writing a C program to validate WAV files, but it currently accepts malformed files. Modify `wav_validator.c` so that it correctly parses a WAV file and performs property-based validation on the header. It must:
   - Check that the first 4 bytes are exactly `RIFF`.
   - Check that bytes 8-11 are exactly `WAVE`.
   - Ensure the `fmt ` chunk exists and has a sensible size.
   - Return exit code `0` if the WAV file is valid and strictly adheres to the standard header format.
   - Return exit code `1` if the file is malformed, corrupted, or not a true WAV file.

3. **Build System**: Create a `Makefile` at `/home/user/Makefile` that compiles `wav_validator.c` into an executable named `wav_validator` using `gcc` with `-Wall -Werror`. 

4. **Package/Dependencies**: Ensure any required dependencies for compiling and SQLite manipulation are installed locally.

The success of your task will be evaluated by an automated test suite that will run your compiled `/home/user/wav_validator` against a hidden adversarial corpus. It must accept 100% of clean WAV files (exit code 0) and reject 100% of malformed/evil WAV files (exit code 1).