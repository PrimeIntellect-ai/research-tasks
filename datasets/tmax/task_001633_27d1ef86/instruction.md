You are a performance engineer tasked with debugging and finalizing a high-performance C++ replacement for an old, slow query processor. 

We have a buggy implementation of the new processor located at `/home/user/fast_parser.cpp`. It processes a custom text-based instruction format from standard input and prints the computed state to standard output. However, it crashes or produces incorrect results on certain edge cases.

Recently, a QA engineer sent an audio bug report demonstrating a sequence that causes the parser to fail completely. The audio file is located at `/app/issue_report.wav`.

Your objectives are:
1. **Transcribe the bug report:** Use whatever tools you need (e.g., `ffmpeg`, `whisper.cpp`, or other available speech-to-text tools) to transcribe `/app/issue_report.wav`. The engineer dictates a specific sequence of parsing commands that triggers the crash.
2. **Construct a Regression Test:** Save the exact sequence dictated in the audio to `/home/user/regression_input.txt`. Use this to reproduce the bug in `/home/user/fast_parser.cpp`.
3. **Debug and Fix:** Analyze the traceback or use `gdb`/`valgrind` to diagnose why the C++ code fails on this edge case (and potentially others). Fix the format parsing logic in `/home/user/fast_parser.cpp`.
4. **Compile the Final Version:** Compile your fixed code into an executable at `/home/user/fast_parser_fixed`. 

Your final executable must be bit-for-bit perfectly equivalent in behavior to our reference oracle binary, located at `/app/bin/oracle_parser`. The automated verification suite will aggressively random-fuzz your compiled binary against the oracle with thousands of combinations of inputs to ensure complete equivalence. 

Make sure your code handles invalid formats, boundary conditions, and all query types precisely as the oracle does.