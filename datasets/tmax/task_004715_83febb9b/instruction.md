You are a researcher working on spectroscopy signal data processing. You are experiencing non-reproducible results when running convergence testing and density estimation due to floating-point reduction order errors when processing large streams of data. You need to implement a robust statistical tool in C that computes bootstrap confidence intervals using a stable summation algorithm.

We have provided a vendored copy of the `pcg-c` random number generator library at `/app/pcg-c`. Unfortunately, the library's `Makefile` has been perturbed and contains a syntax error preventing compilation.

Your tasks are:
1. Identify and fix the perturbation in `/app/pcg-c/Makefile` (specifically, fix the broken `CFLAGS` definition that is missing a hyphen and `-fPIC` to allow static linking in other projects) and build the library using `make`.
2. Write a C program `/home/user/spectra_mean.c` that reads a sequence of raw 32-bit floating-point numbers (little-endian, standard IEEE 754 `float`) from standard input until EOF. You can assume there will be at least 10 and at most 1,000,000 floats.
3. Compute the exact mean of the loaded floating-point numbers. To eliminate reduction-order sensitivity, you **must** use the Kahan summation algorithm. Perform the summation and variables using `double` precision.
4. Compute a 95% bootstrap confidence interval for the mean. To do this:
   - Include `<pcg_variants.h>` from `/app/pcg-c/include`.
   - Seed the PCG32 random number generator using `pcg32_srandom(42u, 54u);` exactly once before the bootstrap loop.
   - Generate exactly 1000 bootstrap datasets. Each bootstrap dataset is created by drawing `N` samples with replacement from your original `N` floats. Use `pcg32_boundedrand(N)` to pick indices.
   - For each bootstrap dataset, compute its mean using Kahan summation (again, using `double` precision).
   - Sort the 1000 bootstrap means in ascending order.
   - Extract the 2.5th percentile (index 24) and the 97.5th percentile (index 974).
5. Print the results to standard output in the following exact format:
   `Original Mean: %.8f, 95%% CI: [%.8f, %.8f]\n`
6. Compile your program to `/home/user/spectra_mean`. Make sure it links correctly against the `pcg-c` library (e.g., `-I/app/pcg-c/include -L/app/pcg-c/src -lpcg_random`).

Your final executable must be completely deterministic and perfectly match an existing reference oracle for identical binary inputs.