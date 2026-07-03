You are tasked with finding a regression in a C library using `git bisect`.

The repository is located at `/home/user/signal_lib`. 
It contains a library that computes a precise mathematical series in `signal_calc.c`. 
The function signature is `double compute_series(int iterations);`.

Recently, a precision loss bug was introduced. When running `compute_series(10000)`, the expected result is approximately `1.644934` (with an error of less than `1e-5`). However, on the `main` branch (HEAD), the result diverges significantly due to an internal precision loss bug introduced in one of the past 100 commits. The commit `HEAD~100` is known to be good.

There is a catch: your current terminal environment has been misconfigured by a global profile script that exports `CFLAGS="-ffast-math"`. If you compile the code with this flag, *all* commits will exhibit precision loss, completely ruining your bisection. 

Your tasks:
1. Write a C-based regression test that links against `signal_calc.c`, calls `compute_series(10000)`, and exits with `0` if the result is correct (within `1e-5` of `1.644934`) and `1` if the precision loss is detected.
2. Repair/bypass the environment misconfiguration during your build process.
3. Use `git bisect` (or a script) to find the exact commit hash that introduced the internal precision loss bug.
4. Write the full 40-character commit hash of the *first bad commit* to `/home/user/bad_commit.txt`.

Do not modify the files in the repository commits, just find the bad commit.