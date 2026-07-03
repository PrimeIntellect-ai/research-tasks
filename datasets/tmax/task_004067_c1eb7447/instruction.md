You are a data scientist analyzing genetic mutation rates in a set of observed DNA sequences compared to a reference primer. 

Your task is to write a C program that calculates sequence alignments, uses MCMC to estimate the mutation rate, and computes bootstrap confidence intervals for the mean mutation count.

**Input Data:**
Assume there is a file located at `/home/user/sequences.txt` containing 50 DNA sequences, one per line. Each sequence is exactly 8 characters long.
The reference primer sequence is `ATGCGTAC`.

**Program Requirements:**
Write a C program at `/home/user/analyze.c` that performs the following steps:
1. **Sequence Alignment:** Read `/home/user/sequences.txt`. For each sequence, calculate the Hamming distance to the reference primer `ATGCGTAC`. This distance represents the number of mutations.
2. **MCMC Sampling:** Assume the Hamming distances follow a Poisson distribution with unknown parameter $\lambda$. Implement a Metropolis-Hastings MCMC sampler to estimate the posterior mean of $\lambda$.
   - **Prior:** Uniform distribution $\lambda \sim U(0, 8)$.
   - **Proposal Distribution:** Gaussian centered at the current $\lambda$ with standard deviation $\sigma = 0.5$. (Reject or clamp proposals outside [0, 8]).
   - **Iterations:** 10,000 total iterations, discarding the first 1,000 as burn-in.
   - Calculate the mean of the remaining 9,000 $\lambda$ samples.
3. **Bootstrap Confidence Interval:** To validate the MCMC estimate, implement a bootstrap resampling procedure.
   - Resample the original 50 Hamming distances *with replacement* 1,000 times.
   - For each resample, calculate the sample mean.
   - Determine the 95% Confidence Interval by finding the 2.5th and 97.5th percentiles of these 1,000 bootstrapped means.

**Output:**
Your C program must write the final calculated values to a file named `/home/user/results.txt` in the following format (rounding to 3 decimal places):
```
MCMC_Lambda_Mean: <value>
Bootstrap_CI_Lower: <value>
Bootstrap_CI_Upper: <value>
```

Compile and run your C program to produce the results file. You may use standard C libraries (`stdio.h`, `stdlib.h`, `math.h`, `string.h`, etc.). You do not need to use an external RNG library; standard `rand()` or `drand48()` is acceptable.