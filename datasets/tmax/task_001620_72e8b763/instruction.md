You are an MLOps engineer responsible for analyzing experiment artifacts. A pipeline has dumped several experiment result logs into `/home/user/artifacts/`. Each file is a JSON containing the results of a specific model run, including a list of inference `latencies` (in milliseconds), the number of `successes` (correct predictions), and the `total_trials`.

Your task is to build a lightweight ETL pipeline script (in any language you choose) that processes these JSON files and outputs a summarized CSV report at `/home/user/processed_artifacts.csv`.

The CSV must have the following columns in exactly this order:
`experiment_id,posterior_prob,mean_latency,ci_lower,ci_upper`

For each experiment, compute the following metrics:
1. **Bayesian Posterior Probability (`posterior_prob`)**: We want to estimate the true success probability of the model. Use a Beta-Binomial conjugate model. Assume a prior of Beta(alpha=2, beta=10). Calculate the expected value (mean) of the posterior distribution given the `successes` and `total_trials` from the JSON.
2. **Mean Latency (`mean_latency`)**: The simple arithmetic mean of the `latencies` array.
3. **Bootstrap Confidence Interval (`ci_lower`, `ci_upper`)**: Use a bootstrap resampling method (resampling with replacement) with exactly 10,000 iterations to estimate the 95% confidence interval (2.5th and 97.5th percentiles) of the mean latency. 

Constraints & Formatting:
- Round all numerical outputs in the CSV to exactly 4 decimal places.
- Sort the final CSV rows alphabetically by `experiment_id`.
- Include the header row.
- If you use Python, set `numpy.random.seed(42)` before running your bootstrap to ensure deterministic output. If you use another language, the verification test will allow a small tolerance (+/- 0.05) for the bootstrap CI bounds.

The `artifacts` directory and its contents are already present on the system. Produce the final `/home/user/processed_artifacts.csv` file.