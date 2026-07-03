You are a data engineer building an ETL pipeline to process telemetry data from IoT sensors. You need to write a Go application that reads a CSV file, performs statistical anomaly detection, and computes the linear trend of the normal data.

Here are your instructions:
1. Set up a Go module named `etl` in the directory `/home/user/etl`.
2. Read the input dataset at `/home/user/sensor_data.csv`. The file has a header row and two columns: `timestamp` (integer) and `value` (float).
3. Compute the mean and the population standard deviation of the `value` column across all rows in the dataset.
4. Classify each row into "anomaly" or "normal":
   - A row is an anomaly if the absolute difference between its `value` and the dataset's mean is strictly greater than 2 times the population standard deviation (`|value - mean| > 2 * stddev`).
5. Write all anomalous rows (keeping the same format, including the header) to `/home/user/anomalies.csv`.
6. For the "normal" rows, fit a Simple Linear Regression model to find the trend of `value` over `timestamp` (i.e., `value = slope * timestamp + intercept`). Use the standard Ordinary Least Squares (OLS) formulas.
7. Save the resulting regression coefficients to `/home/user/regression.json` with the exact JSON format: `{"slope": <float>, "intercept": <float>}`.
8. Run your Go program so that `/home/user/anomalies.csv` and `/home/user/regression.json` are generated successfully.

Ensure your code is precise with its mathematical calculations and handles the CSV and JSON formats correctly.