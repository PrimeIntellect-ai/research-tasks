You are a bioinformatics analyst processing simulated nanopore sequencing signals. We use a C program to read the signal values, apply a simple scaling filter, and compute the total spectral power using OpenMP for parallelization.

However, the provided code at `/home/user/signal_processor.c` produces wildly varying and incorrect results on each run. This non-reproducibility is caused by a data race during the floating-point accumulation (an improper reduction implementation). 

Your task is to:
1. Fix the OpenMP directive in `/home/user/signal_processor.c` so that it safely and correctly computes the `total_power` sum using OpenMP's built-in reduction clause. Do not change the mathematical logic or array sizes.
2. Compile the fixed C code to an executable named `/home/user/signal_processor`. You must use `gcc` with the `-O3` and `-fopenmp` flags.
3. Run the compiled executable with exactly 4 OpenMP threads (`OMP_NUM_THREADS=4`).
4. Save the standard output of the program to `/home/user/result.txt`.

Ensure your final `result.txt` contains only the numeric output printed by the program.