You are an IT support technician responding to an escalated ticket. 

**Ticket Details:**
The data processing bash script `/home/user/calculate_risk.sh` is crashing midway through processing `/home/user/data.csv`. The script processes rows of numerical data by calling an undocumented, closed-source compiled binary, `/home/user/math_helper`. 

When the script hits certain mathematical edge cases in the data, `math_helper` crashes with a core dump (Floating point exception), halting the entire batch process. We do not have the source code for `math_helper`.

**Your Objective:**
1. **Analyze the Binary:** Use binary analysis or string extraction techniques on `/home/user/math_helper` to determine the exact mathematical edge condition that causes it to crash.
2. **Implement Assertion-Based Validation:** Modify `/home/user/calculate_risk.sh` to pre-validate the inputs before passing them to `math_helper`. If a row triggers the crash condition, the script should NOT call `math_helper`. Instead, it must append the string `SKIPPED: A,B,C` (where A, B, and C are the respective row values) to `/home/user/skipped.log` and continue processing the next row.
3. **Write a Regression Test:** Create a bash script at `/home/user/regression.sh` that runs `/home/user/calculate_risk.sh` and asserts that the script completes successfully with an exit code of 0. It should print `PASS` to stdout if successful, and `FAIL` otherwise.

**Constraints & Requirements:**
- Do not modify `/home/user/data.csv` or `/home/user/math_helper`.
- The final state must contain the modified `/home/user/calculate_risk.sh`, the newly generated `/home/user/skipped.log`, and the runnable test `/home/user/regression.sh`.
- Ensure `/home/user/regression.sh` is executable and run it to verify your fix.