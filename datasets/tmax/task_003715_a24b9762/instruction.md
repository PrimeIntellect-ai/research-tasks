You are an open-source maintainer reviewing a Pull Request for a new hybrid C/Python command parsing engine in your project. The PR is broken and needs your intervention to be merged.

The PR author attempted to introduce a C-based state machine (`libparser.so`) wrapped by Python to process incoming command strings, but there are three major issues you need to resolve in your terminal:

1. **Broken Build System**: The `Makefile` in `/home/user/parser_project/` fails to compile the C code into a shared library. The author forgot the correct compiler flags required to create a shared object (`.so`) that Python's `ctypes` can load. Fix the `Makefile` and successfully build `libparser.so`.
2. **Missing Input Sanitizer**: The parser is vulnerable to command injection. You must write a Python script at `/home/user/classifier.py` that takes a single file path as a command-line argument, reads its contents as a string, and decides whether to ACCEPT or REJECT it.
   - It must exit with code `0` (ACCEPT) for clean commands.
   - It must exit with code `1` (REJECT) for malicious commands (any command containing shell metacharacters: `;`, `|`, `&`, `$`, or the word `sudo`).
   - Your `classifier.py` script should also call the C library's `int parse_cmd(const char*)` function (which returns 0 on success) just to prove the library is loaded, though the security filtering must be done in Python.
3. **Audio Fixture Decoding**: The PR includes an audio test fixture at `/app/voicemail.wav`. This file contains a sequence of DTMF (Dual-tone multi-frequency) tones representing a numeric PIN. You must decode the DTMF sequence contained in the audio file and save the resulting digits to `/home/user/pin.txt`.

**Expected Deliverables:**
- A fixed `Makefile` that compiles `libparser.so` successfully.
- `/home/user/classifier.py` functioning exactly as specified.
- `/home/user/pin.txt` containing the decoded DTMF numeric string.

Our CI system will automatically verify your `classifier.py` against a hidden adversarial corpus to ensure 100% of clean inputs are accepted and 100% of malicious inputs are rejected.