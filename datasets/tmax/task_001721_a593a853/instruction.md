You are a data engineer responsible for analyzing server reliability. You have been provided with a raw log file at `/home/user/server_logs.csv`.

Your task is to build a mini ETL pipeline, store the data efficiently, and perform a Bayesian update to estimate the failure probability of a specific server.

Follow these exact steps:

1. **ETL & Storage**: 
   - Parse the `/home/user/server_logs.csv` file.
   - Filter the records to keep ONLY the rows where `server_id` is exactly `SRV-001`.
   - Transform the `latency_ms` column into a new `latency_sec` column (by dividing the milliseconds by 1000).
   - Load this transformed data into an SQLite database located at `/home/user/metrics.db`.
   - The table must be named `server_metrics` and have the following schema: `timestamp` (TEXT), `latency_sec` (REAL), `status` (TEXT).

2. **Bayesian Inference**:
   - Write a Python script at `/home/user/infer.py` that connects to the `/home/user/metrics.db` SQLite database.
   - We want to estimate the probability of failure for `SRV-001`. Treat each log entry as an independent Bernoulli trial where `status == 'FAIL'` is a "success" (in statistical terms) and `status == 'OK'` is a "failure".
   - Use a Beta-Binomial conjugate model. Your prior belief about the failure probability is modeled as a Beta distribution with parameters `alpha = 2` and `beta = 10`.
   - Update this prior using the exact counts of 'FAIL' and 'OK' statuses for `SRV-001` retrieved from your SQLite database.
   - Calculate the posterior mean of the failure probability.

3. **Output**:
   - The Python script should output the result to a file at `/home/user/result.json`.
   - The file must contain the posterior mean rounded to exactly 4 decimal places in the following JSON format:
     `{"posterior_mean": <value>}`

Execute your pipeline so that `metrics.db` and `result.json` are generated correctly.