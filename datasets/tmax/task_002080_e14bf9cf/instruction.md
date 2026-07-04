You are a security researcher analyzing a suspicious C++ network service. We intercepted the source code, but the threat actors left it in an incomplete state and it is highly unstable. Your objective is to compile it, fix the environment misconfigurations preventing it from running, trace its dependencies, and patch a critical concurrency bug that causes it to crash under specific payloads.

Here is your workspace setup in `/home/user/workspace`:
- `server.cpp`: The source code of the suspicious service.
- `Makefile`: For building the binary.
- `client.py`: A script we wrote to simulate traffic to the service.
- `lib/libobfuscator.so`: A shared library required by the server.

Your tasks are:
1. **Environment Repair**: Build the server by running `make`. When you run `./server`, it will fail to start. Diagnose and fix the environment misconfiguration preventing the binary from loading its required shared library.
2. **System Call Tracing**: The server silently hangs or exits on startup because it is looking for a specific configuration file. Use system call tracing tools (`strace`) to discover the exact absolute path of the configuration file it is trying to read. Create this file and write the exact word `ENABLE` into it so the server proceeds to bind to port 9090.
3. **Crash Diagnosis & Fixing**: Once the server is running, execute `python3 client.py` in another terminal. The script sends normal payloads, followed by a malicious cancellation payload (`"ABORT_SEQ"`). The server will crash (Aborted/Core dumped). 
   - Use `gdb` or logging to analyze the crash. The issue is a concurrency bug where an exception thrown inside a detached thread is unhandled, calling `std::terminate`.
   - Modify `server.cpp` to catch this exception gracefully inside the thread. When the exception is caught, print exactly `[SECURITY] Caught malicious abort` to standard output. Do not change the overall architecture of the threading model.
4. **Verification Log**: Create a report at `/home/user/workspace/investigation.txt` with exactly three lines:
   - Line 1: The name of the environment variable you had to modify to fix the shared library issue.
   - Line 2: The absolute path of the configuration file the server was looking for.
   - Line 3: The exact C++ exception type (e.g., `std::invalid_argument`) that was originally thrown and caused the crash.

Recompile the server, ensure it stays alive through the entirety of `client.py`'s execution, and ensure the report is formatted correctly.