You are tasked with setting up a test orchestration script from scratch to compile and test a mathematical constraint checker. The C program is provided but currently uncompiled, and it encodes its output using Base64. 

Write a Bash script at `/home/user/build_and_test.sh` that performs the following end-to-end tasks:

1. **Compilation**: Create the directory `/home/user/bin`. Compile the provided C source file at `/home/user/src/math_check.c` into an executable named `/home/user/bin/math_check`. 
   *Note*: The C code utilizes functions from the standard math library, so you must ensure it is linked correctly during compilation.

2. **Test Fixture Setup**: Generate a test fixture file at `/home/user/test_data.txt` containing the integers 1 through 20, one number per line.

3. **End-to-End Test Orchestration & Decoding**: 
   Iterate over each integer `N` from your test fixture file. For each `N`:
   - Execute `/home/user/bin/math_check N`. The program will output a Base64-encoded string.
   - Decode this Base64 output to retrieve the raw integer value `R`.
   
4. **Constraint Satisfaction & Logging**:
   - Check if the decoded integer `R` satisfies the mathematical constraint: $R = N^2 + 15$.
   - If the constraint is satisfied, append exactly `[N] PASS` to the log file `/home/user/test_report.log`.
   - If the constraint is not satisfied (or if the execution fails), append exactly `[N] FAIL` to the log file.
   - (e.g., the line for N=1 should be `[1] PASS`)

Ensure your Bash script is executable. You should execute your script to verify that it generates the correct `/home/user/test_report.log` file.