You are acting as a build engineer managing artifacts for a text processing system. Your team is developing a lightweight, high-performance C utility called `reverser` that reads a string from standard input, reverses it, and prints it to standard output.

However, the current build and testing pipeline is broken, and we need you to fix it and implement proper validation scripts using Bash.

All your work will take place in `/home/user/project`.

Here are your tasks:

1. **Repair the Makefile:**
   The C source file `/home/user/project/reverser.c` and a `/home/user/project/Makefile` exist. The Makefile is currently broken (it fails to build the `reverser` binary correctly due to syntax/flag errors). Fix the `Makefile` so that running `make` successfully compiles the C code into an executable named exactly `reverser` in the same directory.

2. **Implement Property-Based Testing in Bash:**
   Create a Bash script at `/home/user/project/prop_test.sh`. This script must:
   - Generate 50 random alphanumeric strings (each between 10 and 50 characters long).
   - For each string, feed it via stdin to `./reverser`, capture the output, and feed that output back into `./reverser` again.
   - Assert the property that reversing a string twice yields the exact original string.
   - If all 50 tests pass, the script must write exactly the text `PROPERTY TEST PASSED` to `/home/user/project/test_results.log`.
   - If any test fails, it should write `PROPERTY TEST FAILED` to the log and exit.

3. **Implement a Performance Benchmark in Bash:**
   Create a Bash script at `/home/user/project/benchmark.sh`. This script must:
   - Generate a single payload text file containing exactly 50,000 'A' characters at `/home/user/project/payload.txt`.
   - Run the `./reverser` binary 100 times, redirecting the contents of `payload.txt` into the binary's stdin each time (ignore the output).
   - Once the 100 runs are complete, append exactly the text `BENCHMARK COMPLETED` to `/home/user/project/benchmark.log`.

Constraints:
- Make sure `prop_test.sh` and `benchmark.sh` have executable permissions.
- Do not use any external frameworks (like Python or Node.js) for testing; stick to Bash shell built-ins and standard POSIX/coreutils (e.g., `tr`, `fold`, `head`, `cat`).