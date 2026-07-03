You are a performance engineer profiling a Bayesian inference application. The core of the application relies on an MCMC sampler that calculates an inverse covariance matrix. Unfortunately, the current implementation fails with a `LinAlgError` when evaluating highly collinear inputs (near-singular matrices).

Your task is to fix the sampler, run it on a provided dataset, perform convergence testing, and calculate bootstrap confidence intervals on the results.

Here is your workflow:

1. **Fix the Sampler**: 
   The script `/home/user/mcmc_sampler.py` contains a function `run_mcmc(data, iterations)`. It currently calculates `inv_cov = np.linalg.inv(cov)`.
   Modify this file to replace `np.linalg.inv(cov)` with the pseudo-inverse: `np.linalg.pinv(cov, rcond=1e-5)`.

2. **Run Analysis**:
   Create a new script at `/home/user/analysis.py`. In this script:
   - Load the dataset `/home/user/data.npy`.
   - Call `run_mcmc(data, iterations=6000)` from the fixed `mcmc_sampler.py`.
   - The function returns a tuple: `(samples, acceptance_rate)`. Ensure your script prints the acceptance rate (this acts as a basic convergence test; it should be > 0.1).
   - Discard the first `1000` samples as burn-in. You will be left with `5000` samples. Each sample has 3 dimensions.

3. **Bootstrap Confidence Intervals**:
   In `/home/user/analysis.py`, use bootstrap resampling to estimate the 95% confidence interval for the *posterior mean* of each of the 3 dimensions.
   - Set the numpy random seed to `42` *exactly once* right before your bootstrap loop.
   - Perform `1000` bootstrap iterations.
   - For each iteration, sample `5000` rows *with replacement* from the post-burn-in MCMC samples. Calculate the mean of these resampled rows across each dimension.
   - After the loop, calculate the 2.5th and 97.5th percentiles (using `np.percentile`) of these 1000 bootstrap means to get the `ci_lower` and `ci_upper` bounds for each dimension.
   - Calculate the overall posterior mean directly from the 5000 post-burn-in samples.

4. **Output Results**:
   Save your final metrics to `/home/user/results.json`. The JSON file must have the following exact structure, with floats rounded to 4 decimal places:
   ```json
   {
     "dim_0": { "mean": 0.0000, "ci_lower": 0.0000, "ci_upper": 0.0000 },
     "dim_1": { "mean": 0.0000, "ci_lower": 0.0000, "ci_upper": 0.0000 },
     "dim_2": { "mean": 0.0000, "ci_lower": 0.0000, "ci_upper": 0.0000 }
   }
   ```

Run your script to generate the final `results.json` file.