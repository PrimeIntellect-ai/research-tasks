You are a data scientist tasked with cleaning and analyzing a corrupted sensor dataset. The dataset is located at `/home/user/sensor_data.csv` and contains three columns: `timestamp`, `temperature` (Celsius), and `pressure` (hPa). 

The data acquisition pipeline had a bug, and some rows contain invalid measurements. Your task is to write a Go program to clean the data, perform a statistical analysis, and output the results to a JSON file.

Data Cleaning Rules:
1. Ignore any rows where `temperature` or `pressure` cannot be parsed as a float.
2. Discard rows where `temperature` is strictly less than -50.0 or strictly greater than 50.0.
3. Discard rows where `pressure` is strictly less than 900.0 or strictly greater than 1100.0.

Statistical Analysis:
After filtering the dataset, compute the following metrics on the valid data:
1. **Valid Records**: The total number of valid rows.
2. **Mean Temperature**: The arithmetic mean of the valid temperature values.
3. **Sample Covariance**: The sample covariance between temperature and pressure (using N-1).
4. **Pearson Correlation**: The Pearson correlation coefficient between temperature and pressure.
5. **95% Confidence Interval for Mean Temperature**: Calculate the lower and upper bounds of the 95% confidence interval for the mean temperature. Use the normal approximation formula: `Mean ± 1.96 * (Sample Standard Deviation / sqrt(N))` (using sample standard deviation with N-1).

Output Format:
Your Go program must output the results to a file located precisely at `/home/user/analysis_results.json`. The JSON file must have the following exact keys with their corresponding floating-point (or integer for count) values rounded to exactly 4 decimal places (except `valid_records` which is an integer):
```json
{
  "valid_records": 123,
  "temp_mean": 20.1234,
  "covariance": 15.6789,
  "correlation": 0.8123,
  "temp_ci_lower": 19.5678,
  "temp_ci_upper": 20.6789
}
```

Constraints:
- You must use Go to perform this analysis.
- Do not use any external math/statistics libraries beyond the standard library (e.g., `math`, `encoding/csv`, `encoding/json`).