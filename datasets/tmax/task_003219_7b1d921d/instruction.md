You are tasked with organizing the project files for our new file-management microservice. The lead architect left an audio memo with the path sanitization requirements, but she has since gone on vacation. 

Your objectives are:

1. **Audio Requirements:**
   An audio note from the architect is located at `/app/architect_notes.wav`. You need to transcribe this audio (you may install tools like `ffmpeg` or Python libraries like `SpeechRecognition` or `whisper` to do this locally in the workspace) to find the exact rules for path sanitization.

2. **Fix the Rust Validator:**
   There is a fast path-parsing utility written in Rust located at `/home/user/project/fast_path/`. The previous developer left it with a borrow checker error. Debug and fix `src/main.rs` so that it compiles using `cargo build`.

3. **Python REST API & Classifier:**
   Build a Python script `/home/user/classifier.py` that acts as a classifier for incoming file organization payloads. 
   - The script must accept a single command-line argument: the path to a JSON file.
   - The JSON file will contain a dictionary with a key `"paths"`, which is a list of strings representing file paths to be moved.
   - Your script must read the JSON file, validate *every* path in the `"paths"` list against the rules transcribed from the audio, and optionally utilize the compiled Rust utility to assist in parsing or validation.
   - **Exit Status:** If *all* paths in the JSON payload are clean and valid, the script must exit with status `0`. If *any* path violates the architect's rules, the script must exit with status `1`.

4. **Testing setup:**
   Write a property-based test file at `/home/user/test_classifier.py` using the Python `hypothesis` library to generate arbitrary file paths and assert that your classifier logic does not crash.

Constraints:
- You must write your main classifier in Python 3.
- Use the standard exit codes (0 for accept, 1 for reject) for your `classifier.py`.
- Do not modify the test corpus directories if you find them.