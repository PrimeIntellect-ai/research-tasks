You are a DevOps engineer debugging a legacy statistical analytics service. Recently, the service has started failing to process certain batches of data.

When the service calculates the sample variance for arrays with very large magnitudes but small differences, the naive variance formula ($E[X^2] - (E[X])^2$) suffers from catastrophic cancellation (precision loss), resulting in negative variances that crash the system.

You have been provided with the service logs at `/home/user/analytics.log`. 

Your task is to:
1. Analyze `/home/user/analytics.log` to identify all jobs that failed due to this numerical instability.
2. Extract the `job_id` and the input array for each failed job.
3. Write a script in any language of your choice that uses a numerically stable algorithm (such as Welford's algorithm, or by utilizing a high-precision arbitrary arithmetic library/built-in robust statistical functions) to calculate the correct **sample variance** (using $n-1$ degrees of freedom) for the extracted inputs.
4. Output the corrected results to a CSV file located exactly at `/home/user/fixed_variances.csv`.

**Constraints and Formats:**
- The output file `/home/user/fixed_variances.csv` must contain exactly the failed `job_id` and its corresponding correct sample variance, separated by a comma.
- Format each line as: `job_id,variance`
- Round the variance to exactly 6 decimal places (e.g., `0.025000`).
- Do not include headers in the CSV.
- Do not include jobs that completed successfully.