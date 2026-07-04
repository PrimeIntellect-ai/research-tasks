You are acting as a Data Engineer building a data quality check step for an ETL pipeline. You have been provided with a raw daily transaction log in CSV format at `/home/user/transactions.csv`.

Your task is to write a Python script `/home/user/dq_check.py` that processes this data, performs statistical tests, and outputs data quality metrics.

The script must perform the following steps exactly as described:
1. Load the data from `/home/user/transactions.csv`.
2. Clean the data by filtering out any rows where the `amount` column is missing (null/NaN) or is strictly less than 0.
3. Calculate the sample mean of the cleaned `amount` column.
4. Perform bootstrap sampling to calculate the 95% confidence interval of the mean. 
   - You must use exactly `10000` bootstrap resamples.
   - Each resample must be the same size as the cleaned dataset, drawn with replacement.
   - Set the random seed by calling `numpy.random.seed(42)` exactly once, immediately before generating your random samples.
   - Calculate the mean of each of the 10,000 resamples.
   - Calculate the 2.5th and 97.5th percentiles of these sample means using `numpy.percentile` to get the lower and upper bounds of the 95% confidence interval.
5. Perform a 1-sample t-test to test the null hypothesis that the true mean of the transaction amounts is `150.0`. Use `scipy.stats.ttest_1samp`.
6. Save the results as a JSON file at `/home/user/dq_metrics.json` with the following structure:
```json
{
  "mean": 154.2345,
  "ci_lower": 151.1234,
  "ci_upper": 157.3456,
  "t_statistic": 2.3456,
  "p_value": 0.0123
}
```
Round all float values in the JSON output to exactly 4 decimal places.

Run your script to ensure `/home/user/dq_metrics.json` is generated correctly.