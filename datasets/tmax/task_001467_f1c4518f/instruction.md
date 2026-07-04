You are an AI assistant helping a researcher with a numerical simulation project. 

The researcher has written a Markov Chain Monte Carlo (MCMC) sampler in Python to estimate a posterior distribution. However, the simulation is producing wildly incorrect results because of a floating-point reduction stability issue. The log-likelihood function involves summing an array of extreme positive and negative values. Because the script uses Python's standard `sum()` function, catastrophic cancellation and reduction-order precision loss are destroying the signal.

Your task is to:
1. Fix the numerical instability in `/home/user/mcmc_sim.py`. Locate the line using standard `sum()` to aggregate the `data` array in the likelihood function, and replace it with Python's exact floating-point summation (`math.fsum()`). **Do not change any random seeds, iterations, or other logic.**
2. Run the modified `/home/user/mcmc_sim.py`. It will generate a file called `/home/user/posterior.txt` containing the MCMC samples.
3. The researcher has provided a baseline set of samples in `/home/user/ground_truth.txt`. Write a Python script to perform a 2-sample Kolmogorov-Smirnov (KS) test to compare your new `posterior.txt` samples against the `ground_truth.txt` samples. Use `scipy.stats.ks_2samp`.
4. Save the resulting p-value of the KS test, rounded to exactly 4 decimal places, into `/home/user/p_value.txt` (e.g., `0.1234`). The file should contain only this number.

All files are located in `/home/user/`.