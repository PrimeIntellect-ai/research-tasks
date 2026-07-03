You are tasked with diagnosing and bisecting a mathematical precision regression in a Rust application. 

A containerized application recently started producing incorrect simulation results in production. You have been provided with:
1. The container's crash log at `/home/user/container_crash.log`.
2. The exact failing production binary extracted from the container at `/home/user/prod_bin`.
3. The application's source code repository at `/home/user/math_repo`, which contains exactly 200 commits.

Your objectives:
1. **Container Log Inspection & Syscall Tracing**: The binary requires a configuration file to run, but the location and expected format of this file are undocumented. Inspect the container log to determine the failure parameters. Then, use system call tracing (`strace`) on `/home/user/prod_bin` to figure out exactly which configuration file the application attempts to read. Create this file and populate it with the parameters found in the log to reproduce the issue.
2. **Precision Loss Tracking & Bisection**: The failure is due to a precision loss regression introduced somewhere in the Git repository's history (a developer likely swapped double-precision floats for single-precision). Use `git bisect` on `/home/user/math_repo` to find the exact commit hash that introduced the bug.
   * *Hint: The correct commit will output the expected result found in the container log. The bad commit will diverge significantly.*
3. **Reporting**: Once you find the exact commit hash that introduced the regression, write the full, 40-character commit hash to `/home/user/bad_commit.txt`.

Ensure your final answer is correct and isolated in `/home/user/bad_commit.txt`.