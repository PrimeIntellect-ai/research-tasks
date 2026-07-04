You are a DevOps engineer analyzing an issue with a Bash script used to monitor application performance. 

The script `/home/user/process_logs.sh` is supposed to calculate the Root Mean Square (RMS) of request latencies (measured in nanoseconds) provided in a log file. However, it currently crashes with an assertion error when processing a recent batch of logs in `/home/user/latencies.txt`.

Your task involves three steps:

1. **Bug Identification & Fuzzing:** The script has a flaw related to how Bash handles arithmetic. To prove the root cause, create a file named `/home/user/crash_input.txt` containing exactly 3 lines, where each line is a positive integer. When `/home/user/process_logs.sh /home/user/crash_input.txt` is executed, it must trigger the internal assertion: "Assertion failed: sum_sq negative due to overflow".

2. **Script Repair:** Modify `/home/user/process_logs.sh` to fix the bug. 
   - You must eliminate the integer overflow while maintaining the script's exact output logic and scale (4 decimal places for the final square root). 
   - You must use `bc` or `awk` to repair the floating-point precision and large number handling for the intermediate sum of squares. 
   - Ensure the assertion check is removed or updated to correctly validate using `awk` or `bc` (since `sum_sq` will no longer overflow negatively, you can safely remove the negative check).

3. **Execution:** Once the script is fixed, run it against the original log file `/home/user/latencies.txt` and save the exact standard output to `/home/user/result.txt`.

**File details:**
- The log file `/home/user/latencies.txt` exists and contains 5 lines of large latency values.
- The script `/home/user/process_logs.sh` exists and is executable.