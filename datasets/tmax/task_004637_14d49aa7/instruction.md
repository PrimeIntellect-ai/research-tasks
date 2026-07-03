You are a platform engineer maintaining a CI/CD pipeline for a custom C-based arithmetic evaluation tool. The tool is failing its pipeline checks due to memory leaks and incomplete test orchestration.

Your task is to fix the underlying issues in the C program, repair the build process, and write a Bash orchestration script that enforces specific constraints on the test cases and validates memory correctness.

Here is the setup in the `/home/user/pipeline` directory:

1. **`calc.c`**: A simple C program that takes three arguments (`arg1`, `arg2`, `operator`) and prints the result. It currently has a memory leak.
2. **`Makefile`**: A build file that lacks debugging symbols.
3. **`tests.txt`**: A CSV file containing test cases in the format `id,arg1,arg2,operator`.

You must accomplish the following steps:

**Step 1: Fix the C program and Makefile**
- Modify `calc.c` to fix the memory leak. Ensure that all dynamically allocated memory is properly freed before the program exits.
- Modify `Makefile` so that the `calc` binary is compiled with debugging symbols (`-g`).

**Step 2: Write the Test Orchestration Script**
Write a Bash script at `/home/user/pipeline/ci_test.sh` that performs the following tasks:
- Recompiles the `calc` binary using `make`.
- Reads `tests.txt` line by line.
- For each test case, executes the `calc` binary under `valgrind --leak-check=full`.
- **Constraint Parsing:** Capture the numeric output of `calc`. If the result is strictly greater than `50`, the test case violates the pipeline constraints and must be completely skipped (do not write it to the report).
- **Memory Profiling Verification:** For the test cases that satisfy the constraint (result <= 50), parse the `valgrind` output to determine if there were any memory leaks (look for "definitely lost: 0 bytes").
- Append the results to `/home/user/pipeline/ci_report.txt` in the exact following format:
  `[id] result=<value> status=<PASS|LEAK>`
  - Use `PASS` if valgrind reports 0 bytes definitely lost.
  - Use `LEAK` if valgrind reports > 0 bytes definitely lost.

**Step 3: Execute the Pipeline**
Run your script so that `/home/user/pipeline/ci_report.txt` is populated correctly. 

*Note: You do not need root access. Valgrind and make are available on the system. All test cases in `tests.txt` are valid integers and standard operators (`+`, `-`, `*`).*