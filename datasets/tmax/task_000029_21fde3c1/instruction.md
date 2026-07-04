You are a QA engineer tasked with setting up a secure testing environment for a mathematical expression evaluation service. The service has been vulnerable to command injection and malformed expressions, so we need a strict sanitiser.

Your tasks are:

1. **Audio Transcription & Environment Setup**: 
   There is an audio file at `/app/qa_instructions.wav` containing instructions from the QA lead regarding a secret environment variable needed for the test build system. Transcribe this audio (you may install tools like `ffmpeg` or `whisper` to help). Based on the audio, create a script `/home/user/env_setup.sh` that exports the exact environment variable and value mentioned.

2. **Parser and Sanitiser Construction**:
   Write a strict parser in Bash at `/home/user/math_filter.sh`. This script must take a single file path as its argument, read the expression inside, and validate it. 
   Because regex alone is insufficient to prevent all logic errors, you *must* implement a character-by-character state machine in Bash that enforces the following rules:
   - Allowed characters: digits (`0-9`), spaces, `+`, `-`, `*`, `/`, `(`, `)`.
   - Parentheses must be perfectly balanced at the end of the string, and the parenthesis depth must never drop below zero.
   - Operators (`+`, `-`, `*`, `/`) cannot be consecutive (e.g., `5 + * 2` is invalid).
   - If the expression is completely valid, the script must exit with status code `0` and print the evaluated result (using `bc` or arithmetic expansion).
   - If the expression violates ANY rule or contains malicious payloads, the script must exit with status code `1` and print nothing.

3. **Adversarial Verification**:
   Your `/home/user/math_filter.sh` will be evaluated against an adversarial corpus of "evil" inputs located in `/app/corpus/evil/` and "clean" inputs in `/app/corpus/clean/`. Your script must reject 100% of the evil corpus (exit 1) and accept 100% of the clean corpus (exit 0).

Ensure your script is executable (`chmod +x /home/user/math_filter.sh`).