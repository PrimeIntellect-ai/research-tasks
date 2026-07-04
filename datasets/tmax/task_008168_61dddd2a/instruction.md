You are an engineer investigating a critical issue in a long-running in-memory Key-Value store service written in C++. The service has been exhibiting memory leaks and eventual crashes under high traffic. 

We suspect the regression was introduced recently. A local Git repository containing the service code is located at `/home/user/kvstore`. 

Your tasks are:
1. **Fuzz Testing:** The codebase includes a libFuzzer setup. Compile the fuzzer using the existing `Makefile` (it uses Clang and AddressSanitizer). Run the fuzzer to reliably reproduce the memory leak/crash.
2. **Git Bisection:** Use `git bisect` to identify the exact commit that introduced the memory leak. 
   - The initial commit of the repository is known to be "good".
   - The current `HEAD` is known to be "bad".
3. **Report the Bad Commit:** Write the full SHA-1 hash of the offending commit to a file named `/home/user/bad_commit_hash.txt`.
4. **Fix the Bug:** Diagnose the root cause of the memory leak in the C++ code, fix the issue on the `main` branch, and generate a Git patch file containing your fix. Save this patch file to `/home/user/fix.patch`.

Constraints:
- Do not alter the git history (no rebasing/resetting) prior to finding the bad commit.
- Your patch file must apply cleanly to the current `HEAD` and fix the bug without removing the core logic of the feature introduced in that commit.