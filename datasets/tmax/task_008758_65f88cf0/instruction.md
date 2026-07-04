You are a data scientist working on genomic model fitting. You need to evaluate two candidate primers against a dataset of target sequences to determine which has a significantly better alignment profile, while ensuring your statistical pipeline is numerically stable and highly parallel.

I have provided a dataset of 500 DNA target sequences at `/home/user/targets.txt` (one sequence per line).
The two candidate primers are:
- Primer A: `ATGCGTGA`
- Primer B: `TCGATCCA`

Write a Rust program to perform the following analysis. Initialize a Cargo project at `/home/user/primer_analysis` and write your code there. You may use the `rayon` crate for parallelization and the `rand` and `rand_chacha` crates for random number generation.

1. **Sequence Alignment**:
   For a given primer and a target sequence, the alignment score is the maximum number of matching characters between the primer and any contiguous substring of the target of the exact same length (no gaps). 
   Calculate the alignment score for Primer A and Primer B against all 500 targets.

2. **Bootstrap Confidence Intervals & Parallel Computing**:
   Generate 10,000 bootstrap resamples (each of size 500, sampled *with replacement* from the 500 computed alignment scores) for Primer A, and separately 10,000 for Primer B. 
   - Calculate the mean score for each resample.
   - You **must** parallelize the bootstrap resampling loop using `rayon` (e.g., `into_par_iter()`).
   - Use `rand_chacha::ChaCha8Rng` initialized with `SeedableRng::seed_from_u64(42)` to drive your sampling. **Important**: Because you are doing this in parallel, standard random sampling might lose determinism. To keep the output deterministic for verification, pre-generate your 10,000 resample index arrays sequentially using the seeded RNG, OR just use the exact dataset properties if you can compute it analytically. Actually, please do the following exactly: 
   Instantiate `ChaCha8Rng::seed_from_u64(42)`. Generate a flat array of `10,000 * 500` random `usize` indices (using `rng.gen_range(0..500)`). Use this single flat array to construct the 10,000 resamples for Primer A, and then generate *another* flat array of `10,000 * 500` indices for Primer B. Then use `rayon` to compute the means of these pre-defined resamples in parallel.
   - Find the 95% confidence intervals (the 2.5th percentile and 97.5th percentile of the bootstrap means, meaning the 250th and 9750th sorted values, 0-indexed).

3. **Numerical Stability**:
   Calculate the sample variance of the 10,000 bootstrap means for Primer A and Primer B. To prevent catastrophic cancellation, you **must** implement Welford's online algorithm for computing the variance.

4. **Statistical Hypothesis Comparison**:
   Calculate the p-value for the null hypothesis that the mean of Primer A is less than or equal to the mean of Primer B. 
   Compute this as the proportion of the 10,000 bootstrap pairs (using the matched index $i$ from 0 to 9999) where `mean_A[i] <= mean_B[i]`.

Output your final metrics to `/home/user/results.txt` in the following format exactly (rounded to 4 decimal places):
```
CI_A_LOWER=...
CI_A_UPPER=...
CI_B_LOWER=...
CI_B_UPPER=...
VAR_A=...
VAR_B=...
P_VALUE=...
```

Run your Rust program so that the output file is generated.