You are a performance engineer optimizing an audio processing pipeline for an edge device. The system extracts proprietary metadata from custom audio files and runs queries against a local database. The previous engineer attempted to rewrite the proprietary C-based extraction tool into a pure Bash script (with a tiny C helper) to avoid cross-compilation overhead, but left the company before finishing.

Your objectives:
1. **Audio Fixture Analysis**: There is an audio file at `/app/voicemail.wav`. Use standard tools (like `ffmpeg` or `whisper` if available, or any other method) to find the spoken passcode in this file. 
2. **Git Forensics & Secret Recovery**: An encrypted zip file `/app/repo.zip` contains the Git repository of the project. Extract it using the spoken passcode from the audio file. Once extracted, search the Git history to recover the latest version of `parser.sh` and the secret API token used for local database queries. The script was deleted in a commit titled "revert bash experiment". Restore `parser.sh` to `/home/user/parser.sh`.
3. **Build Failure Diagnosis**: Inside the restored repository directory, there is a C helper tool in `src/`. It currently fails to compile using `make`. Diagnose and fix the build failure (it may be missing standard library links or have a syntax error) so that the executable `chunker` is successfully built.
4. **Query Result Debugging & Corrupted Input Handling**: The recovered `parser.sh` contains a bug. When it encounters a corrupted file header (magic number mismatch), it currently crashes instead of returning the expected JSON error payload. Additionally, the SQLite query it runs against `/app/meta.db` contains a bad JOIN that produces duplicate rows. Fix `parser.sh` so that it handles corrupted inputs gracefully and correctly queries the database.
5. **Bit-Exact Fuzz Equivalence**: Your final script at `/home/user/parser.sh` must be BIT-EXACT equivalent to the legacy binary oracle located at `/app/legacy_oracle`. It must accept exactly one argument (the path to an input file) and output identical JSON to stdout as the oracle would for ANY arbitrary input file (valid or corrupted).

Requirements:
- Your final implementation must be located at `/home/user/parser.sh` and be executable.
- Do not modify the oracle at `/app/legacy_oracle`.
- You may use the compiled `chunker` tool within your script if necessary.
- Ensure your script exits with the same exit codes as the oracle.