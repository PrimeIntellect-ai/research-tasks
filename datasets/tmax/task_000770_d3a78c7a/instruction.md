**URGENT: 3AM PagerDuty Alert**

You are the on-call engineer for a critical scientific data pipeline. At 3:00 AM, the nightly batch processor started failing. The batch processor reads a large text file containing telemetry data (thousands of lines of floating-point numbers) and aggregates them. The process is crashing before completion.

**System State:**
- The source code for the batch processor is located at: `/home/user/engine/process.c`
- The input data file causing the crash is at: `/home/user/engine/input.txt`
- The build script is at: `/home/user/engine/build.sh`

**Your Tasks:**
1. **Isolate the Failure:** The input file has 1,000 lines. The crash is caused by a specific line in `input.txt`. Use delta debugging or test minimization techniques to find the exact 0-indexed line number that triggers the crash.
2. **Analyze the Root Cause:** The crash is an arithmetic exception (SIGFPE). Use logging, tracing, or a debugger (GDB) to determine why it's crashing. The issue is suspected to be precision loss leading to a division-by-zero error.
3. **Fix the Code:** Modify `/home/user/engine/process.c` to fix the precision loss issue so the program can successfully process the entire `input.txt` file without crashing and without altering the fundamental mathematical formula.
4. **Compile and Verify:** Use `/home/user/engine/build.sh` to recompile the binary to `/home/user/engine/process` and ensure it runs successfully against `input.txt`.
5. **Report:** Create a JSON file at `/home/user/fix_report.json` with the following exact schema:
   ```json
   {
       "crashing_line_index": <int>,
       "fixed_binary_path": "/home/user/engine/process"
   }
   ```

*Note: The system environment is standard Linux. You have access to GCC, GDB, Python, Bash, etc. Do not use root privileges.*