You are an engineer investigating a long-running metrics daemon that has been crashing and consuming unbounded memory. 

You have been given access to the daemon's directory at `/home/user/metrics_app/`. The system consists of three components:
1. `/home/user/metrics_app/daemon.sh`: The main Bash script running the service.
2. `/home/user/metrics_app/helper/`: A directory containing C source code for a data processing helper.
3. `/home/user/metrics_app/legacy_submitter`: A compiled, undocumented binary that the bash script uses to submit metrics.

Your task is to debug and fix the system by completing the following steps:

1. **Fix Compiler/Linker Errors:** The Makefile in `/home/user/metrics_app/helper/` is broken. When you run `make`, it fails to link the math library. Fix the `Makefile` and compile the `process_data` binary so it is created at `/home/user/metrics_app/helper/process_data`.
2. **Reverse Engineer the Binary:** The `legacy_submitter` binary keeps failing with an opaque "Auth Error". Use reverse engineering tools (like `strings`, `ltrace`, or `strace`) to inspect `/home/user/metrics_app/legacy_submitter`. Determine the specific environment variable it expects for authentication and modify `daemon.sh` to export this environment variable with the correct value before calling it.
3. **Fix the Bash Memory Leak:** The `daemon.sh` script is designed to run continuously, but it has a severe memory leak. Find the string variable or array that grows unboundedly during the infinite `while` loop and fix it so it only stores the *latest* log entry instead of appending forever.
4. **Fix the Formula Implementation:** The `daemon.sh` script attempts to calculate the average of two variables, `VAL1` and `VAL2`. However, due to missing parentheses in the Bash arithmetic expansion, the formula is calculated according to standard order of operations (division before addition), yielding incorrect results. Correct the formula to properly calculate the average.

Once you have identified and fixed all issues, save your corrected script to `/home/user/metrics_app/daemon_fixed.sh`. Ensure it has executable permissions (`chmod +x`). 

**Verification requirements:**
- `/home/user/metrics_app/helper/process_data` must be successfully compiled.
- `/home/user/metrics_app/daemon_fixed.sh` must exist, be executable, contain the correct math formula (with parentheses), fix the memory leak (by assignment `=` instead of append `+=`), and export the correct environment variable for the legacy binary.