You are tasked with investigating a memory leak in a long-running Bash service. The service is version-controlled in a Git repository located at `/home/user/app`. Recently, the service has been crashing due to out-of-memory (OOM) errors after running for an extended period. 

Your goals are:
1. **Find the regression**: Use Git bisection or delta debugging techniques to identify the exact commit that introduced the memory leak in `daemon.sh`. The service is supposed to clear its internal item cache when the number of items reaches 10, but a boundary condition or logic error was introduced that prevents this cleanup, causing the array to grow indefinitely.
2. **Record the bad commit**: Write the full Git commit hash of the *first bad commit* (the one that introduced the bug) to `/home/user/leak_commit.txt`.
3. **Fix the bug**: Checkout the `main` branch (the latest commit) and fix the off-by-one or logic error in `daemon.sh`. Ensure that the array `ITEMS` is correctly reset to empty `()` whenever its size is greater than or equal to 10. Do not change the overall structure of the script, only fix the conditional logic responsible for the cleanup.

The `daemon.sh` script is designed to run continuously, but for testing purposes, you can source it or run it and monitor its memory usage or internal array size. 

Ensure that your final fixed version of `daemon.sh` is saved in `/home/user/app/daemon.sh` on the `main` branch.