You are an AI assistant helping a researcher analyze simulated experimental data.

The researcher has generated a dataset stored in an HDF5 file at `/home/user/data.h5`. This file contains two datasets:
- `X`: A 100x10 feature matrix.
- `y`: A 100-element 1D array of observed values.

Your task is to write a Bash script `/home/user/run_analysis.sh` that orchestrates a Python script `/home/user/analyze.py` to perform the following analysis:

1. **Data I/O & Matrix Decomposition**: Read `X` and `y` from `/home/user/data.h5`. Compute the Singular Value Decomposition (SVD) of `X` to find the Moore-Penrose pseudoinverse, and use it to compute the Ordinary Least Squares (OLS) estimate of the weights, $w_{ols}$.
2. **MCMC Sampling**: Write a custom Metropolis-Hastings MCMC sampler in Python to sample from the posterior distribution of the weights $w$ (a 10-dimensional vector). 
   - Assume a Gaussian likelihood for $y$ with known standard deviation $\sigma = 0.5$.
   - Assume a standard normal prior for each weight in $w$: $w_i \sim \mathcal{N}(0, 1)$.
   - Initialize the MCMC sampler at $w = w_{ols}$.
   - Use a Gaussian proposal distribution centered at the current $w$ with a standard deviation of 0.05 for each dimension.
   - Run the sampler for exactly 10,000 iterations. Set the numpy random seed to `42` right before starting the MCMC loop to ensure reproducibility.
3. **Hypothesis Testing**: Discard the first 2,000 samples as burn-in. Using the remaining 8,000 samples, evaluate the posterior probability of the hypothesis $H_1: w_0 > 1.0$. (i.e., calculate the fraction of samples where the first element of $w$ is strictly greater than 1.0).
4. **Output**: The Python script should print this probability to standard output. The Bash script `/home/user/run_analysis.sh` should execute the Python script and redirect its output into the file `/home/user/hypothesis_test.txt`.

Make sure `/home/user/run_analysis.sh` is executable and cleanly runs the entire pipeline.