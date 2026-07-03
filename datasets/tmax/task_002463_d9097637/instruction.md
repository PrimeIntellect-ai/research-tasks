You are an AI assistant helping a data scientist investigate floating-point reduction order errors using bootstrap confidence intervals.

We have a dataset of 100,000 single-precision floating-point numbers in `/home/user/data.txt`. The data contains a mix of very large and very small magnitudes, which can cause precision loss when summing them naively.

Your task is to orchestrate a small workflow that quantifies this error. 

1. Write a C program at `/home/user/bootstrap_sum.c` that does the following:
   - Reads `N = 100000` floats from a file passed as the first command-line argument (`argv[1]`).
   - Performs `B = 1000` bootstrap iterations to estimate the 95% confidence interval of the mean difference between two summation methods.
   - For each bootstrap iteration:
     a. Generate a resampled array of size `N` with replacement from the original data. Use the custom PRNG provided below to generate the random indices (`index = my_rand() % N`).
     b. Compute `mean_A`: the mean of the resampled array using standard sequential summation (sum elements from index 0 to N-1, then divide by N). Use `float` for the accumulator.
     c. Compute `mean_B`: sort the resampled array in **ascending order of their absolute values**, then sum sequentially from index 0 to N-1, and divide by N. Use `float` for the accumulator.
     d. Calculate the difference for this iteration: `diff = mean_A - mean_B`.
   - After all 1000 iterations, sort the `diff` values in ascending order.
   - Compute the 95% confidence interval using the percentile method. Specifically, use the 25th sorted value (index 24) for the lower bound and the 975th sorted value (index 974) for the upper bound.
   - Write this interval to `/home/user/ci_output.txt` in the exact format: `[lower, upper]` using `%f` for printing.

**Custom PRNG**:
To ensure exact cross-platform reproducibility, include and use this exact PRNG state and function for generating indices (do not use `<stdlib.h>`'s `rand()`):
```c
unsigned int my_seed = 42;
unsigned int my_rand() {
    my_seed = my_seed * 1664525 + 1013904223;
    return my_seed;
}
```
Reset `my_seed = 42` at the very beginning of your bootstrap loop (before iteration 0).

2. Write a bash script `/home/user/run_analysis.sh` that:
   - Compiles `bootstrap_sum.c` into an executable `bootstrap_sum` using `gcc` with `-O3` and `-lm`.
   - Executes `./bootstrap_sum /home/user/data.txt`.

Ensure all files are created correctly and permissions are set. Run your bash script to produce the final `ci_output.txt`.