You are a performance engineer tasked with debugging and fixing a C-based telemetry parsing pipeline that has been crashing in production. The pipeline processes timestamps, but it suffers from a subtle timezone bug and a fatal crash when encountering corrupted data.

Your goals are to diagnose the build failure, analyze a memory dump, extract critical context from an audio voicemail, and implement a robust fix.

Here is the current state of the system and your objectives:

1. **Audio Analysis:** The lead engineer left a voicemail at `/app/alert.wav`. You need to transcribe or listen to this audio file to find the required timezone offset (in hours) that must be applied to all telemetry timestamps.
2. **Memory Dump Analysis:** The previous version of the parser crashed, leaving a memory dump at `/app/crash.dump`. Analyze this dump and extract the 16-character "poison" string that caused the crash. The string is known to start with `POISON_`.
3. **Build Diagnosis:** The source code is located in `/home/user/pipeline/`. Currently, running `make` fails due to syntax and configuration errors. Diagnose and fix the build failures so that it compiles to the executable `/home/user/pipeline/parser`.
4. **Implementation & Regression Fix:** Modify `/home/user/pipeline/parser.c` to read newline-separated strings from standard input (`stdin`) and write to standard output (`stdout`). 
    - If a line contains the 16-character poison string exactly, the program must output `[DROPPED]\n`.
    - If a line is a valid timestamp in the format `YYYY-MM-DD HH:MM:SS`, parse it, apply the timezone offset (in hours) extracted from the audio file, and output the adjusted timestamp in the exact same format `YYYY-MM-DD HH:MM:SS\n`. (Assume the input timestamps are UTC, and handle standard calendar rollovers for days/months/years appropriately).
    - If a line does not match the timestamp format and does not contain the poison string, output `[ERROR]\n`.

The final executable must be located at `/home/user/pipeline/parser`. Automated tests will verify your program by fuzzing it with thousands of inputs against a secure, hidden oracle implementation to ensure exact bit-for-bit equivalence on `stdout`.