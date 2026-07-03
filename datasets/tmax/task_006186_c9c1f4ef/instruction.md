You are a security researcher analyzing a suspicious system event. A background service recently crashed, and you need to create a minimal reproducible example (MRE) to trigger the crash in a controlled debug mode to reveal the underlying vulnerability.

You have been provided with two files:
1. `/home/user/service.log` - A messy, interspersed log file containing output from multiple concurrent process IDs (PIDs).
2. `/home/user/analyzer` - The compiled C++ binary of the service that crashed.

Your task:
1. **Log Timeline Reconstruction**: Parse `/home/user/service.log` to identify the PID that encountered a `FATAL: SEGFAULT`. Reconstruct the timeline for *that specific PID* to find the exact three consecutive string inputs it processed right before it crashed.
2. **Binary Inspection**: The `/home/user/analyzer` binary contains a hidden environment variable used by developers to enable debug mode. Use standard Linux CLI tools to inspect the binary and find an environment variable string that begins with `ANALYZE_DBG_`.
3. **MRE Creation**: Write a C++ program at `/home/user/trigger.cpp` that:
   - Sets the hidden environment variable you found to the value `"1"`.
   - Uses `execv` or `system()` to execute `/home/user/analyzer` passing the three inputs you recovered from the logs as command-line arguments.
4. **Execution**: Compile your C++ program to `/home/user/trigger`. Run it and redirect its standard output to `/home/user/solution.txt`.

Ensure your C++ program is self-contained. The final state must have the correct output written to `/home/user/solution.txt`.