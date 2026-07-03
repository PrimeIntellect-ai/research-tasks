You are a Site Reliability Engineer (SRE) investigating recurring crashes in a critical uptime monitoring service. The service, a C++ daemon that calculates weighted moving averages of server response times, has recently started crashing and generating core dumps.

Your task is to identify the regression and fix the issue.

You have been provided with a local Git repository of the service at `/home/user/uptime_monitor`. 

Perform the following steps:
1. The repository has a `test_input.txt` file and a `run_test.sh` script. Running `./run_test.sh` currently results in a crash (core dump). 
2. Use `git bisect` to find the exact commit that introduced the crash. The known good commit is the very first commit in the repository.
3. **Note:** While bisecting, you will encounter a commit where the build fails due to a dependency/header conflict introduced in the Makefile or source files. You must resolve this build issue temporarily during your bisection to successfully test that commit.
4. Analyze the core dump (or run the program in `gdb`) to identify the mathematical error causing the crash (e.g., division by zero, overflow) and the exact function name where it occurs.
5. Fix the bug in the current `HEAD` (the `master` branch) so that `make` succeeds and `./run_test.sh` runs without crashing and prints "Success".
6. Create a report file at `/home/user/debugging_report.txt` with exactly three lines:
   - Line 1: The full 40-character Git commit hash of the commit that introduced the bug.
   - Line 2: The exact name of the C++ function where the crash occurred.
   - Line 3: The output of `./run_test.sh` after you have fixed the bug.

Constraints:
- Do not change the underlying logic of the moving average, just fix the mathematical bug gracefully (e.g., if a weight is zero, skip it or handle it so it doesn't crash, but follow standard math principles—in this specific code, weights of 0 should be ignored in the calculation).
- Ensure your final state in the repository has the fixed code compiled and passing the test.