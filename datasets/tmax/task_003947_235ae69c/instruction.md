You are a data analyst evaluating the inference performance of two different machine learning models. You have been provided with two CSV files containing benchmark latency data:
- `/home/user/model_v1.csv`
- `/home/user/model_v2.csv`

Each file has two columns: `request_id` and `latency_ms`. 
The data contains missing values (empty strings or NaNs) and extreme outliers (e.g., negative latencies from logging errors, or massive spikes from cold starts).

Your task is to write a Python script at `/home/user/compare_models.py` that performs the following steps:
1. Load both CSV files.
2. For each dataset separately, handle missing values and outliers:
   - Drop any rows where `latency_ms` is missing.
   - Filter out invalid and outlier latencies by keeping only rows where `0 <= latency_ms <= P99`, where `P99` is the 99th percentile of the valid latencies for that specific model.
3. Perform a Welch's two-sample t-test (assuming unequal variances) to compare the cleaned latencies of `model_v1` against `model_v2`.
4. Calculate the 95% confidence interval for the difference in means (`mean(v1) - mean(v2)`).
5. Output the results to a JSON file located at `/home/user/report.json` with the following exact keys and format, rounding all numerical values to exactly 4 decimal places:
   ```json
   {
       "t_stat": 1.2345,
       "p_value": 0.1234,
       "ci_lower": -0.5678,
       "ci_upper": 2.3456
   }
   ```

You will likely need to install external packages like `pandas` and `scipy` using pip before running your script. Ensure the final JSON output matches the requested structure exactly.