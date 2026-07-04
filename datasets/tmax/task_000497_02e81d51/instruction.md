You are a data engineer building a lightweight ETL pipeline. 

You have been provided with a raw log file located at `/home/user/raw_logs.txt`. The log file contains API request records. Most lines look like this:
`[2023-10-12 10:14:02] GET /api/v1/users | status: 200 | latency_ms: 45.23`

However, some log lines are corrupted or missing data, resulting in latency values like `NaN`, `null`, or just empty strings.

Your task is to create a Bash script at `/home/user/etl_pipeline.sh` that performs the following steps:
1. Creates a Python virtual environment at `/home/user/venv`.
2. Installs the `numpy` and `scipy` packages into this virtual environment.
3. Parses `/home/user/raw_logs.txt` to extract only the valid numerical latency values (ignoring lines with `NaN`, `null`, or non-numerical/missing latencies). 
4. Computes the sample mean and the 95% confidence interval for the mean of these valid latency values using a t-distribution. You should write a short Python snippet executed via the virtual environment's Python interpreter to do the math.
5. Saves the results to `/home/user/metrics.json` in the following exact JSON format, with all floating point values rounded to exactly two decimal places:
```json
{
  "mean": 45.12,
  "ci_lower": 44.01,
  "ci_upper": 46.23
}
```

Ensure your bash script is executable (`chmod +x /home/user/etl_pipeline.sh`) and run it so that `/home/user/metrics.json` is generated.