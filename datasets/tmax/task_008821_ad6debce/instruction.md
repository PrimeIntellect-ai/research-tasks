You are a security researcher analyzing a suspicious C++ network service provided as source code in a Git repository at `/home/user/suspicious_daemon`. The service was reported to have an intermittent crash (segmentation fault) under load, which generates a core dump.

Your objectives are:
1. **Reproduce and Bisect**: The crash is intermittent but can be triggered by running the compiled binary multiple times. The current `main` branch `HEAD` is broken, but `HEAD~15` is known to be stable. Use `git bisect` to find the first commit that introduced the crash. Write the full 40-character commit hash of the bad commit to `/home/user/bad_commit.txt`.
2. **Core Dump Analysis**: Obtain a core dump from the crash (you may need to configure `ulimit -c unlimited`). Analyze the core dump using `gdb` to identify the crashing function. Write the exact name of the C++ function where the segmentation fault occurs (just the function name, e.g., `trigger_payload`) to `/home/user/crash_func.txt`.
3. **Patch the Vulnerability**: Analyze the code in the crashing function on the `main` branch to understand the root cause (a concurrency bug). Fix the C++ code in `service.cpp` so that the race condition is resolved and the binary no longer crashes. Ensure the code compiles successfully using `g++ -pthread service.cpp -o service`.

Verification will check:
- The exact commit hash in `/home/user/bad_commit.txt`.
- The exact function name in `/home/user/crash_func.txt`.
- That the patched `service` binary can run 500 times concurrently without crashing.