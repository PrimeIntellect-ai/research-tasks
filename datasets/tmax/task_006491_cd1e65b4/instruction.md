I am a performance engineer tasked with profiling a parallel scientific data processing pipeline. We need to measure the baseline variance of our density estimation routine using OpenMP. 

There is an HDF5 file located at `/home/user/data/particles.h5`. It contains a single 1D dataset named `/x_coords` consisting of 1,000,000 double-precision floats (values strictly between 0.0 and 100.0).

Please do the following:

1. **Write a C++ Program (`/home/user/src/density_omp.cpp`)**:
    - Use the HDF5 C++ API to read the `/x_coords` dataset into memory.
    - Use OpenMP to parallelize the computation of a 100-bin histogram over the range `[0.0, 100.0]`. (Bin 0: `[0, 1)`, Bin 1: `[1, 2)`, etc.).
    - Write the resulting 100 integer bin counts to `/home/user/results/histogram.out` (one integer per line).
    - Measure ONLY the wall-clock time taken by the parallel histogram computation (excluding HDF5 I/O and writing to disk). 
    - Print the time to `stdout` strictly in this format: `Compute Time: <X> ms` (where `<X>` is the floating point milliseconds).

2. **Compile the Program**:
    - Compile it to `/home/user/bin/density_omp`.
    - Use `-O3`, `-fopenmp`, and link the necessary HDF5 libraries.

3. **Write a Benchmark & Bootstrap Script (`/home/user/bin/benchmark.sh`)**:
    - Write a bash script using only standard shell tools (bash, awk, shuf, etc. - no Python/R).
    - The script should run `/home/user/bin/density_omp` exactly 50 times, extracting the compute times.
    - Implement a Bootstrap procedure in `awk`/bash with $B=1000$ resamples (sampling with replacement from the 50 observations) to compute the sampling distribution of the *mean*.
    - Calculate the 95% Confidence Interval (2.5th and 97.5th percentiles) of the mean compute time.
    - Output this confidence interval to `/home/user/results/ci.txt` exactly in the format: `Mean CI: [lower, upper]` (rounded to 2 decimal places).

Create the necessary directories if they don't exist. Ensure `benchmark.sh` is executable and run it to produce the final `ci.txt` and `histogram.out` files.