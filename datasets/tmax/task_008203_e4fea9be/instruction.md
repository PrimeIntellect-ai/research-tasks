You are an operations engineer triaging a nightly batch job failure. The job processes a list of values but has been crashing midway through, failing to complete.

The source code and inputs are located in `/home/user/nightly/`.
- `process.c` contains the source code for the batch processing tool.
- `inputs.txt` contains the list of inputs being processed.

Your tasks are:
1. Identify the specific input value from `inputs.txt` that is causing the program to crash. The crash is due to a numerical instability (precision loss leading to a fatal arithmetic error).
2. Modify `process.c` to fix the floating-point precision issue so that it can successfully process the problematic input without crashing. (Hint: Consider upgrading the precision of the calculation to avoid catastrophic cancellation).
3. Recompile the program using `gcc -o process process.c -lm`.
4. Run your fixed program using the previously crashing input as the sole argument.
5. Save the output of the fixed program for that specific input to `/home/user/nightly/solution.txt`.

Ensure the resulting value in `solution.txt` is the exact output printed by the fixed program (which prints to 2 decimal places).