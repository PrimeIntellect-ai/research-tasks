I am a bioinformatics analyst working with a custom C sequence analysis tool that computes the spectral density of DNA sequences using FFT and runs a Monte Carlo simulation to estimate statistical significance. 

I have a vendored copy of the source code located at `/app/vendored/seq_analyzer`. However, there are two major issues:
1. The project currently fails to build. I suspect there is an issue with the `Makefile` (possibly a missing math library link).
2. The results of the Monte Carlo simulation are suffering from numerical instability. The `total_variance` in `mc_stats.c` is computed using a naive floating-point sum over thousands of iterations, causing catastrophic cancellation and non-reproducible results across different platforms.

Your task is to:
1. Fix the `Makefile` in `/app/vendored/seq_analyzer` so that the project compiles successfully using `make`.
2. Modify the `compute_mc_significance` function in `/app/vendored/seq_analyzer/mc_stats.c` to use standard **Kahan summation** for accumulating the `total_variance`. Do not change the logic of the inner loop computing `var`; only change how `var` is accumulated into `total_variance` using the Kahan summation algorithm. Use a compensation variable initialized to `0.0f`.
3. Build the project and place the final working executable exactly at `/home/user/seq_analyzer_fixed`.

The executable takes a single argument, a DNA sequence string (e.g., `ATGC...`), and prints a single float value representing the Monte Carlo significance. Ensure the final binary works correctly.