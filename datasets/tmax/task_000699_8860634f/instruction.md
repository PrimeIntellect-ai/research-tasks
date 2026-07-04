You are an open-source maintainer reviewing a pull request for a C++ WebSocket server. The PR attempts to introduce a sanitization step for incoming text messages to prevent XSS and command injection, but the code does not compile and the logic is incomplete.

The original bug reporter submitted a voice memo detailing the exact security constraints that the sanitizer must enforce. This audio file is located at `/app/bug_report.wav`. 

Your tasks are:
1. Extract the sanitization rules from the voice memo (`/app/bug_report.wav`). You may use `ffmpeg` or other pre-installed audio tools to listen to or transcribe it.
2. Fix the broken C++ code in `/home/user/ws_server/sanitizer.cpp` and its `Makefile`. The build system uses `make`.
3. The compiled binary must be produced at `/home/user/ws_server/sanitize`. 
4. The binary must take a single command-line argument: the path to a text file containing a WebSocket message payload.
5. If the message violates ANY of the rules specified in the bug report, the binary must exit with status code `1` (rejected).
6. If the message is completely safe, the binary must exit with status code `0` and print the EXACT contents of the file to standard output, without any modifications.

Ensure your code handles various character encodings carefully, as specified in the audio file. We will run your compiled `sanitize` binary against a hidden evaluation suite of clean and malicious payloads to verify its correctness.