You have inherited an unfamiliar C++ codebase located at `/home/user/signal_decoder`. This tool is designed to decode telemetry payloads (represented as hex strings) into human-readable logs. 

Unfortunately, the previous developer left the repository in a broken state. Your objective is to fix the codebase so that the compiled binary behaves exactly like the trusted reference binary located at `/app/oracle_decoder`.

Here is your workflow:

1. **Fix Compilation**: The project currently fails to compile. Diagnose and fix the compiler/linker errors in the repository so that `make` successfully produces the `/home/user/signal_decoder/signal_decoder` executable.
2. **Video Payload Extraction**: The system is known to crash or produce garbled output due to a race condition when processing a specific telemetry payload. This payload was recorded visually in `/app/signal.mp4`. 
   - The video consists of exactly 240 frames. 
   - Each frame is either pure black (bit `0`) or pure white (bit `1`). 
   - Extract the 240 bits (in frame order), group them into bytes (8 bits per byte, MSB first), and represent the resulting 30 bytes as a 60-character continuous hex string. 
   - This hex string is your "crash payload".
3. **Concurrency Debugging**: Feed the crash payload to your compiled `signal_decoder` via standard input. You should observe intermittent crashes or missing output due to a concurrency bug (race condition) in the parallel processing logic. Find and fix the thread synchronization issue in the C++ code.
4. **Git Bisection & Regression Fixing**: Even after the crash is fixed, the decoded output for some inputs will not perfectly match the `/app/oracle_decoder` due to a logic regression introduced somewhere in the repository's git history. 
   - Use `git bisect` alongside the `/app/oracle_decoder` to identify which commit introduced the logic error.
   - Fix the logic error in the current `main` branch so the output matches the oracle.

**Requirements**:
- The final program must compile successfully using `make` in `/home/user/signal_decoder`.
- The final executable must be located at `/home/user/signal_decoder/signal_decoder`.
- The executable must read a hex string from standard input and print the decoded ASCII output to standard output, matching `/app/oracle_decoder` identically for all possible valid hex inputs.
- Do not modify the oracle binary. 
- You may use any standard shell tools (`ffmpeg`, `git`, `g++`, `gdb`, etc.) to complete this task.