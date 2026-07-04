You are a developer tasked with debugging a failing build and an intermittently crashing C program that performs mathematical operations in parallel.

You have a project located at `/home/user/math_project` containing:
- `calc.c`: A multi-threaded C program that reads a file of mathematical operations and computes a global sum.
- `Makefile`: The build script.
- `data.txt`: An input file with 1000 mathematical operations.

Currently, the project has several issues:
1. **Build Failure Diagnosis**: Running `make` fails. Identify the missing flags or errors in the `Makefile` and fix it so the program compiles successfully.
2. **Intermittent Failure Reproduction & Delta Debugging**: Once compiled, running `./calc data.txt` intermittently crashes with a segmentation fault or arithmetic exception. Use your debugging skills to isolate the exact single line in `data.txt` that triggers this crash. Save this exact line (e.g., `123 ADD 5 10`) to `/home/user/math_project/crash_line.txt`.
3. **Code Fix**: Modify `calc.c` to handle the problematic condition gracefully. If the invalid operation is encountered, the program should skip it (treat its result as 0) instead of crashing.
4. **Verification**: Once fixed, compile and run the program against `data.txt`. Save the program's console output (which should be in the format `Total: <number>`) to `/home/user/math_project/final_result.txt`.

Ensure your fixes are robust and the project builds correctly with just `make` in the `/home/user/math_project` directory.