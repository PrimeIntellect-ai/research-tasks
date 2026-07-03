You are a performance engineer tasked with debugging and profiling a mathematical modeling pipeline. 

In `/home/user/mcmc_project`, there is a Python script `mcmc_integration.py`. This script performs MCMC sampling to evaluate a complex posterior distribution and then computes a numerical integral over the samples. However, the script frequently crashes with a `numpy.linalg.LinAlgError: Matrix is not positive definite` because the empirical covariance matrix used for the proposal distribution becomes near-singular during certain iterations, causing the Cholesky decomposition to fail.

Your task consists of three parts:

1. **Fix the Matrix Decomposition:** 
   Modify `/home/user/mcmc_project/mcmc_integration.py` so that it handles near-singular covariance matrices gracefully. Specifically, add a small "jitter" (a diagonal matrix with `1e-6` on the diagonal) to the covariance matrix immediately before the Cholesky decomposition is performed. Do not change the random seed or other logic.

2. **Data Collection via Bash:**
   Write a Bash script named `/home/user/mcmc_project/profile_runs.sh`. This script must run the fixed `mcmc_integration.py` exactly 30 times. The python script outputs a single floating-point number to standard output (the numerical integral result). Save these 30 results into `/home/user/mcmc_project/integral_samples.txt` (one number per line).

3. **Bootstrap Confidence Interval in Bash:**
   Extend your Bash script `profile_runs.sh` to calculate a 95% Bootstrap Confidence Interval for the mean of the 30 samples using pure Bash and standard Unix tools (`awk`, `sort`, `bc`, etc. - do not use Python or R for this step). 
   - Your bootstrap procedure must generate 1,000 resamples (sampling with replacement from the 30 values).
   - Calculate the mean of each resample.
   - Sort these 1,000 means.
   - Extract the 2.5th percentile (25th value) and 97.5th percentile (975th value).
   - Write the final confidence interval to `/home/user/mcmc_project/ci_output.txt` in exactly this format:
     `95% CI: [lower_bound, upper_bound]` (rounded to 4 decimal places).

Make sure `/home/user/mcmc_project/profile_runs.sh` is executable and run it so that the final output files are generated.