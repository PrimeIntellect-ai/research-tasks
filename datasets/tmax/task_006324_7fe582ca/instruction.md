You are a performance engineer tasked with profiling and optimizing a scientific computing pipeline. 

In `/home/user/`, you have a C program named `align_fit.c`. This program calculates simplified sequence alignment scores for a set of DNA primers and performs a linear regression (fitting a curve of primer length vs. alignment score). However, the program runs significantly slower than expected, and we suspect a bottleneck.

Your task is to:
1. Compile `/home/user/align_fit.c` with GCC profiling enabled.
2. Run the compiled executable.
3. Use `gprof` to analyze the execution profile. Identify the name of the function that consumes the most exclusive time. Write *only* the exact name of this function into `/home/user/bottleneck.txt`.
4. Fix the bottleneck. Open or edit `/home/user/align_fit.c` and completely remove the call to the bottleneck function from the `score_alignment` function (you do not need to delete the function definition, just its invocation).
5. Recompile the optimized program with standard optimizations (`-O2`) and without profiling.
6. Run the optimized executable and redirect its standard output to `/home/user/regression_result.txt`. This output represents the reproducible pipeline's regression fit.
7. Perform a regression test: Compare the contents of `/home/user/regression_result.txt` against `/home/user/expected_result.txt` (which contains the known good regression output). If they match exactly, write the word `PASS` to `/home/user/test_status.txt`. If they do not match, write `FAIL`.

Ensure all requested output files (`bottleneck.txt`, `regression_result.txt`, and `test_status.txt`) are created in `/home/user/` with the exact specified formats.