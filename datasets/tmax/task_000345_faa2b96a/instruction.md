You are a performance engineer profiling memory access patterns in C++. Your goal is to orchestrate a reproducible benchmarking experiment to statistically compare cache-friendly (row-major) vs cache-unfriendly (column-major) multi-dimensional array manipulations.

Please complete the following steps:

1. Write a C++ program at `/home/user/benchmark.cpp` that:
   - Takes two command-line arguments: `N` (an integer for the matrix dimension $N \times N$) and `mode` (an integer: `0` for row-major traversal, `1` for column-major traversal).
   - Dynamically allocates a 1D array of size $N \times N$ to represent a 2D matrix.
   - Initializes the array with random integers between 1 and 100. To ensure reproducible computation, seed the `std::mt19937` RNG with the seed `42`.
   - Records the start time using `std::chrono::steady_clock`.
   - Computes the sum of all elements in the matrix. If `mode` is `0`, iterate with the outer loop over rows and inner loop over columns. If `mode` is `1`, iterate with the outer loop over columns and inner loop over rows.
   - Records the end time.
   - Prevents the compiler from optimizing away the sum by printing the final sum to `stderr`.
   - Prints ONLY the elapsed time in microseconds to `stdout`.

2. Create a bash orchestration script at `/home/user/pipeline.sh` that:
   - Compiles the C++ program using `g++ -O0 -std=c++11 /home/user/benchmark.cpp -o /home/user/benchmark` (it's crucial to use `-O0` to prevent loop interchange optimizations).
   - Runs a computation pipeline executing the benchmark 10 times for row-major (`mode` 0) and 10 times for column-major (`mode` 1) with $N = 4000$.
   - Captures the standard output (microseconds) of each run.
   - Uses `awk` or basic shell math to calculate the mean execution time for each mode across the 10 runs.
   - Generates a final report at `/home/user/results.txt` with exactly the following format:
     ```
     Row-major mean: <value> us
     Col-major mean: <value> us
     ```
     *(Replace `<value>` with the calculated integer mean).*

Run your pipeline script to generate the `/home/user/results.txt` file.