You are an IT support technician investigating a sporadic bug reported in ticket #9981. A legacy C application located at `/home/user/legacy_tool` occasionally crashes when processing user inputs.

Your objectives are:

1. **Fuzz Testing**: The application takes a single command-line string argument. Find the specific input condition that causes the tool to crash. (Hint: The bug is triggered when the input starts with a specific 4-letter uppercase prefix and exceeds a certain length). 

2. **Memory Dump Analysis**: When the application crashes, it traps the signal and writes a simulated memory dump to `/home/user/mem.dump` before exiting. You must analyze this binary file, extract the leaked internal support token (which follows the format `SUPPORT-TOKEN-...`), and save exactly this token string to `/home/user/token.txt`.

3. **Regression Test Construction**: Write a C program at `/home/user/regression.c` that acts as a regression test. 
   - It must execute `/home/user/legacy_tool` with an input that is guaranteed to trigger the crash.
   - It must check the exit status of the executed tool.
   - If the tool successfully crashes (exits with code 139 or terminated by SIGSEGV), your regression test must exit with code `0` (Success: bug reproduced).
   - If the tool does NOT crash, your regression test must exit with code `1` (Failure: bug not reproduced).
   - Compile your test to `/home/user/regression`.

Ensure your final token is correct and your compiled regression test works reliably.