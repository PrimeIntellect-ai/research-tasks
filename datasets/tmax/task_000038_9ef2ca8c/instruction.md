You are a data analyst reviewing a legacy ETL pipeline. We have raw sensor data and the aggregated daily summaries produced by the legacy system. We suspect the legacy system introduced a floating-point calculation error that biases the results. 

Your task is to write a Python script that acts as a new ETL verification pipeline. The script must do the following:

1. Read the raw data from `/home/user/raw_sensor_data.csv`. This file contains three columns: `date`, `sensor_id`, and `reading`.
2. Compute the exact true daily mean of the `reading` column for each `date`.
3. Read the legacy summaries from `/home/user/legacy_daily_summary.csv`. This file contains `date` and `legacy_mean`.
4. Merge the true daily means with the legacy means on the `date` column.
5. Calculate the absolute difference between the true daily mean and the legacy mean for each day.
6. Calculate the maximum absolute difference across all days (as a test of numerical accuracy).
7. Calculate the mean of these absolute differences.
8. Compute the 95% confidence interval for the mean absolute difference using a t-distribution (`scipy.stats.t.interval`). Use the standard error of the mean (SEM) of the absolute differences.
9. Save the results in a JSON file at `/home/user/report.json` with the following structure. All numerical values must be rounded to 4 decimal places.

```json
{
  "max_absolute_error": 0.0000,
  "mean_absolute_difference": 0.0000,
  "ci_lower": 0.0000,
  "ci_upper": 0.0000
}
```

Write and execute the Python script to complete this task. You may use `pandas`, `numpy`, and `scipy`.