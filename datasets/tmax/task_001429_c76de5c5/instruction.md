You are an IT support technician investigating Ticket #4092. A critical internal Python script, `processor.py`, used for parsing legacy system logs has started failing silently. 

The developers have isolated the issue to a git repository located at `/home/user/ticket_4092`, but they don't know which commit introduced the bug. Furthermore, the test suite is broken because it relies on an authentication binary whose source code was lost.

Your objective is to find the exact commit that introduced the bug by combining binary analysis, intermediate state tracing, and git bisection.

Here are the specific details:

1. **Binary Reverse Engineering**: 
   Inside `/home/user/ticket_4092/`, there is an ELF executable named `auth_bin`. The original `processor.py` requires a hardcoded authentication key to run. This key is embedded somewhere inside `auth_bin`. You must reverse engineer or inspect `auth_bin` to recover this secret string (it is formatted as `AUTH_KEY_...`).

2. **Intermediate State Tracing**: 
   The `processor.py` script contains a class `LogProcessor` with a method `run(auth_key)`. When the bug occurs, the script does *not* throw an exception or return an error code. Instead, it gets stuck in an invalid intermediate state. You must write a Python test harness that instantiates `LogProcessor`, calls `run()` with the recovered key, and inspects the processor's `current_state` attribute. 
   - A successful run will leave `current_state` as `"FINISHED"`.
   - The buggy run will leave `current_state` as `"HALTED"`.
   Your test harness should exit with a status code of `0` if successful, and `1` if the state is `"HALTED"`.

3. **Git Bisection**:
   Use your test harness to perform an automated git bisection on the `/home/user/ticket_4092` repository. 
   - The commit tagged `v1.0` is known to be `good`.
   - The `HEAD` of the `main` branch is known to be `bad`.

Once you have identified the secret key and the exact commit hash that introduced the bug, write your findings to a file named `/home/user/resolution.log` with exactly the following format:
Line 1: <The recovered authentication key>
Line 2: <The full 40-character bad commit hash>