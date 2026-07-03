You are tasked with debugging a failing build for a mathematical data processing pipeline in `/home/user/project`.

The pipeline consists of a C program (`compute.c`) that reads quadratic equation coefficients ($a, b, c$) from `input.txt` and computes their real roots. A test script (`test.sh`) compiles the program, runs it, and compares its output against `expected.txt`.

Currently, the test script fails because the output of the C program does not match the expected results. The original developer suspects there is an error in the mathematical formula implemented in `compute.c`.

Your task is to:
1. Inspect the test logs or run `/home/user/project/test.sh` to see the failure.
2. Identify and fix the mathematical bug in `/home/user/project/compute.c`.
3. Run `/home/user/project/test.sh` to ensure it outputs "BUILD SUCCESS" and exits with code 0.

You must leave the fixed `compute.c` in `/home/user/project/compute.c`, and the successful build should generate a correct `output.txt` file matching `expected.txt`.