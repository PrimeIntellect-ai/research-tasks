You are acting as a Data Scientist cleaning a raw dataset of server metrics.

We have a dataset located at `/home/user/raw_data.csv` containing the following columns:
`timestamp`, `cpu_usage`, `memory_usage_mb`, `disk_io_errors`

Your task is to write a Python script `/home/user/clean_and_bootstrap.py` that performs an ETL process, creates a new feature, and computes bootstrap statistics to test the numerical properties of the CPU usage. 

Specifically, your script must:
1. **ETL / Cleaning**: Read `/home/user/raw_data.csv`. Filter out any rows where `cpu_usage` is missing (e.g., `'NULL'`, empty, or `NaN`), strictly less than `0.0`, or strictly greater than `100.0`.
2. **Feature Engineering**: For the cleaned dataset, create a new column `memory_ratio` which is `memory_usage_mb` divided by `16000.0` (representing total RAM in MB).
3. **Sampling / Bootstrap**: Using the cleaned `cpu_usage` array, perform a bootstrap to estimate the mean.
   - You **must** use `numpy` and set `numpy.random.seed(42)` exactly once before your bootstrap loop.
   - Perform exactly `1000` bootstrap iterations. In each iteration, draw a sample of the same size as the cleaned data, with replacement, and calculate the mean.
   - Calculate the overall bootstrap mean, and the 95% confidence interval (using the 2.5th and 97.5th percentiles of the bootstrap means using `numpy.percentile`).
4. **Reporting**: Calculate the mean of your newly engineered `memory_ratio` column across the cleaned dataset. Export your final metrics as a JSON file to `/home/user/metrics_report.json`.

The output file `/home/user/metrics_report.json` must have exactly the following keys, with float values rounded to exactly 4 decimal places (except the integer count):
```json
{
  "cleaned_row_count": <integer>,
  "mean_memory_ratio": <float>,
  "cpu_usage_bootstrap_mean": <float>,
  "cpu_usage_95_ci_lower": <float>,
  "cpu_usage_95_ci_upper": <float>
}
```

Do not create any other files. You may use standard data science libraries like `pandas` and `numpy`.