You are a security researcher analyzing a suspicious data processing binary. We have recovered the source code (`/home/user/parser.cpp`) and a malicious payload (`/home/user/payload.dat`) that causes the program to become unresponsive, suspected to be a deliberate denial-of-service vulnerability triggered by a malicious data structure.

Your objectives:
1. **Environment Misconfiguration Repair**: The program currently segfaults or exits immediately on startup because it expects a specific environment variable pointing to its configuration file located at `/home/user/conf`. Identify the missing environment variable from the source code and ensure your subsequent steps run with this correctly set.
2. **Interactive Debugging & Fix**: Use `gdb` to trace the intermediate state of the program when processing `/home/user/payload.dat`. The program hangs in an infinite loop due to a specific sequence in the payload. Identify the bug in `/home/user/parser.cpp`, and modify the C++ code to fix it. The parser should gracefully handle 0-length chunks by breaking the processing loop instead of hanging, and then exit normally.
3. **Regression Test Construction**: Create a bash script at `/home/user/test_regression.sh` that:
   - Sets the correct environment variables.
   - Compiles `/home/user/parser.cpp` into `/home/user/parser` using `g++`.
   - Runs `/home/user/parser /home/user/payload.dat` with a timeout of 2 seconds (using the `timeout` command).
   - If the program completes successfully within the timeout (exit code 0), the script should print "PASS" to standard output and exit with code 0.
   - If the program times out or crashes, the script should print "FAIL" to standard output and exit with code 1. Make sure the script is executable.

The final system state should have a fixed, compilable `/home/user/parser.cpp` and a working executable regression test at `/home/user/test_regression.sh` that outputs `PASS`.