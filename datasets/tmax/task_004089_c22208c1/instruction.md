You are a support engineer investigating a bug in a data processing pipeline. A compiled binary utility called `math-worker` reads all text files in a given directory and processes simple mathematical byte streams. However, it is currently crashing silently (returning exit code 1) when processing the batch of files in `/home/user/data/`. 

The source code for the calculation logic resides in `/home/user/calc/calc.go`, but the `math-worker` binary itself is a black box and has been stripped of panic stack traces.

Perform the following diagnostic steps:

1. **System Call Tracing**: Use `strace` on the `math-worker` binary (located at `/home/user/math-worker`) to monitor its file operations when run against the `/home/user/data/` directory (command: `/home/user/math-worker run /home/user/data/`). Identify the exact file that causes the program to crash. Write ONLY the filename (e.g., `example.txt`, not the full path) to `/home/user/crash_file.txt`.

2. **Fuzz Testing**: The crash is due to a flaw in the `Calculate` function inside `/home/user/calc/calc.go`. Write a standard Go fuzz test named `FuzzCalculate` inside `/home/user/calc/calc_test.go` to programmatically expose the panic. Run your fuzz test to ensure it catches the out-of-bounds error.

3. **Intermediate State Tracing**: Trace the intermediate state of the `Calculate` function when it runs on the specific contents of the crashing file you identified in Step 1. Determine the exact integer value of the `accumulator` variable *immediately before* the panic occurs. Write this single integer value to `/home/user/accumulator.txt`.

Ensure your final outputs (`crash_file.txt`, `calc_test.go`, and `accumulator.txt`) are correctly placed in `/home/user/`.