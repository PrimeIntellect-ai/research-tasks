You are a bioinformatics analyst studying structural DNA motifs that have been mapped to continuous numerical genomic signals. You need to analyze a matrix of these signals to find the dominant structural component and estimate its stability.

You have been provided a dataset of genomic signals at `/home/user/genomic_signals.txt`. This file contains a 50x20 matrix (50 sequences, 20 positional signal values each), with space-separated double-precision floats.

Write a C program at `/home/user/analyze_motifs.c` that performs the following pipeline:

1. **Signal Processing (Smoothing):** Read the 50x20 matrix. Apply a 3-point moving average filter to each row independently. For a row $x$, the smoothed value $y_i = (x_{i-1} + x_i + x_{i+1}) / 3$. 
   - For the left boundary ($i=0$), use $y_0 = (x_0 + x_0 + x_1) / 3$.
   - For the right boundary ($i=19$), use $y_{19} = (x_{18} + x_{19} + x_{19}) / 3$.

2. **Matrix Decomposition (SVD):** Compute the Singular Value Decomposition (SVD) of the 50x20 smoothed matrix to find its largest singular value ($\sigma_1$). You must use the GNU Scientific Library (GSL) for this.

3. **Bootstrap Confidence Intervals:** To estimate the stability of this dominant motif, perform 1000 bootstrap iterations. 
   - Initialize the GSL Mersenne Twister RNG (`gsl_rng_mt19937`) with the seed `42`.
   - In each iteration, create a new 50x20 matrix by sampling 50 rows from the *smoothed* matrix with replacement (use `gsl_rng_uniform_int(r, 50)` to pick row indices).
   - Compute the largest singular value for this resampled matrix.
   - Sort the 1000 singular values in ascending order.
   - Determine the 95% confidence interval using the 2.5th and 97.5th percentiles (0-indexed: index 24 and index 974).

Compile your program and run it. Your program must output the results to a log file at `/home/user/motif_results.txt` in the exact following format (values rounded to 4 decimal places):

```
Smoothed Sigma1: [Value]
Bootstrap 95% CI: [[Lower], [Upper]]
```

Make sure your C program compiles with `gcc -O2 /home/user/analyze_motifs.c -lgsl -lgslcblas -lm -o /home/user/analyze_motifs`.