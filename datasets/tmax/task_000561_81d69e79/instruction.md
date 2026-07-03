You are a bioinformatics analyst working on a C++ sequence processing pipeline. We are looking for periodic signals (like the period-3 signal in coding regions) across a large set of DNA sequences by computing their average power spectrum using a Discrete Fourier Transform (DFT).

Currently, there is a bug in our tool located at `/home/user/compute_spectrum.cpp`. To speed up processing, a previous developer parallelized the accumulation of the power spectra using OpenMP. However, they used `float` precision and `#pragma omp atomic` for the reduction. This causes floating-point reduction order variations: the exact order of summation changes with every run, leading to non-reproducible results due to floating-point rounding differences. Furthermore, single precision `float` is causing the results to drift significantly from our double-precision reference dataset.

Your task:
1. Modify `/home/user/compute_spectrum.cpp` to fix these issues:
   - Upgrade all relevant sequence processing, DFT mathematics, and accumulations from single precision (`float`) to double precision (`double`).
   - Remove the race conditions and non-deterministic floating-point reduction order. You must ensure that the summation is strictly deterministic and perfectly reproducible, regardless of the number of threads used (e.g., by storing intermediate results and performing a sequential reduction, or using deterministic OpenMP array reductions if carefully implemented).
2. Compile your fixed program to `/home/user/compute_spectrum` (ensure you link OpenMP, e.g., `-fopenmp`).
3. Run your program. It will read `/home/user/sequences.txt` and output `/home/user/avg_spectrum.txt`.
4. We have a reference dataset at `/home/user/reference_spectrum.txt`. The output in `avg_spectrum.txt` must match `reference_spectrum.txt` exactly (the reference was generated using strictly sequential double-precision math).
5. Create a regression testing script at `/home/user/check_stability.sh` that:
   - Runs `/home/user/compute_spectrum` 5 times sequentially.
   - Calculates the SHA256 checksum of `/home/user/avg_spectrum.txt` after each run.
   - Verifies that all 5 runs produced the *exact same* checksum (proving numerical stability and determinism).
   - Exits with code 0 if all 5 runs are identical, and code 1 if there is any variation.
   - Ensure the script has executable permissions.

Please leave the final fixed code, the compiled binary, and the stability test script in `/home/user/`.