You are a support engineer diagnosing a system failure. A critical diagnostic script was accidentally deleted by a junior technician. The filesystem has been overwritten, but we captured a raw dump of the relevant partition before the server went down completely. 

The dump is located at `/home/user/backup.img`.

Your tasks are as follows:
1. **Recover the Script**: Inspect the raw dump file to recover the deleted script. The original script was bookended by the exact strings `# DIAGNOSTIC_SCRIPT_START` and `# DIAGNOSTIC_SCRIPT_END`. Extract the code between these markers.
2. **Diagnose and Fix**: The recovered script has a known flaw that caused it to crash the diagnostics service. It contains a mathematical loop/recursion that fails to terminate properly due to floating-point precision errors (e.g., checking for exact equality with floats). Fix the termination condition so that the loop ends where it mathematically should (when the decrementing value reaches `0`). 
3. **Precision Repair**: Because of floating-point arithmetic artifacts, the raw calculation is slightly off. Modify the script to round the final result to exactly 2 decimal places before printing. You may rewrite the script in any language you prefer, as long as the mathematical logic remains the same.
4. **Execute**: Run the fixed script and save the final numerical output to `/home/user/diagnostic_result.txt`.

Ensure the resulting text file contains only the correctly computed number.