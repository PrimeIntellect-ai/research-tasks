You are an IT support technician. We have an escalated ticket from the Data Science team regarding a legacy mathematical data transformation tool. 

The original tool was written years ago, and we only have the stripped binary left, located at `/app/legacy_transform`. This tool takes an array of floats from standard input, applies a proprietary non-linear transformation iteratively until convergence, and outputs the resulting array to standard output. 

Recently, the team tried to write a multi-threaded replacement in C to speed up processing. Their source code is located at `/home/user/new_transform.c`. However, they are experiencing several issues:
1. The new multi-threaded code occasionally produces garbage or inconsistent results (suspected race condition).
2. For some inputs, the iteration fails to converge and loops infinitely or produces NaNs.
3. Even when it finishes, the outputs often differ from the legacy binary, showing a discrepancy in the data transformation logic.
4. They had to downgrade a specific math library dependency to build it, but they left conflicting headers in `/usr/local/include/math_utils` which is confusing the compiler. (You need to clean up the include path to use the system default math library).

Your task:
1. Fix the dependency conflict so the code compiles with standard `gcc -pthread -O3 -lm`.
2. Debug and resolve the race conditions in the multi-threaded implementation in `/home/user/new_transform.c`.
3. Fix the convergence failure logic so it properly matches the mathematical properties of the legacy binary.
4. Ensure your compiled binary exactly matches the output of the legacy binary for all inputs.

The input format is a stream of space-separated floating-point numbers on standard input.
The output format is a stream of space-separated floating-point numbers on standard output, printed to 6 decimal places.

Compile your final fixed program to `/home/user/new_transform`. Our verification system will fuzz your executable against the legacy binary to ensure 100% bit-exact output equivalence.