You are an MLOps engineer tracking experiment artifacts. You need to analyze the error rates of our deployed models using data from two different tracking systems.

You have two files in `/home/user/`:
1. `/home/user/experiments.csv`: Contains metadata about model training runs (`run_id`, `model_type`, `deploy_status`).
2. `/home/user/metrics.json`: Contains production metrics for runs (`run_id`, `errors_detected`). 

There is a known issue in our pipeline: when joining these datasets, missing records in `experiments.csv` cause pandas to silently cast the integer `errors_detected` column to floats due to the introduction of NaNs. This breaks our strict downstream Bayesian modeling library which requires integer counts for Poisson distributions.

Your task:
Write and execute a Python script to process this data and generate a report.
1. Load both datasets and perform a left join from `metrics.json` to `experiments.csv` on `run_id`.
2. Filter the joined data to keep strictly the rows where `deploy_status` is exactly `"deployed"`. Drop any rows with missing values in `deploy_status` or `errors_detected`.
3. Ensure the `errors_detected` column is strictly an integer type (not a float).
4. **Bootstrap Analysis**: For runs where `model_type == 'beta'`, perform a bootstrap analysis to find the 95% confidence interval of the mean of `errors_detected`.
   - Set `numpy.random.seed(42)` exactly once, immediately before the bootstrap.
   - Draw 1000 bootstrap samples (with replacement), each of the same size as the filtered 'beta' dataset.
   - Calculate the mean of each sample.
   - Find the 2.5th and 97.5th percentiles of these means (using `numpy.percentile`).
5. **Bayesian Inference**: For runs where `model_type == 'alpha'`, calculate the exact posterior mean of the error rate.
   - Model the `errors_detected` as counts from a Poisson distribution.
   - Use a Gamma conjugate prior for the Poisson rate $\lambda$, with prior parameters shape $\alpha = 2$ and rate $\beta = 1$.
   - Calculate the posterior shape and rate parameters using the filtered 'alpha' data, and compute the analytical posterior mean.

Output your results as a JSON file at `/home/user/report.json` with the following keys and float values:
- `"bootstrap_lower"`: The 2.5th percentile of the bootstrap means.
- `"bootstrap_upper"`: The 97.5th percentile of the bootstrap means.
- `"posterior_mean"`: The analytical posterior mean for the alpha models.