You are an AI assistant acting as a Data Scientist. We have received a raw dataset from our IoT sensors, but it contains missing values, anomalies, and noise. You need to build a reproducible Python pipeline to clean this data and extract some statistical insights.

The dataset is located at `/home/user/sensor_data.csv`. It contains four columns: `timestamp`, `sensor_A`, `sensor_B`, and `sensor_C`.

Please write a Python script at `/home/user/clean_pipeline.py` that performs the following exact steps in order:

1. **Load and Impute**: Load the CSV. Impute any missing values (NaNs) in the sensor columns using linear interpolation (`df.interpolate(method='linear')`).
2. **Correlation Analysis**: Compute the Pearson correlation matrix for the three sensors. Identify the pair of sensors that have the highest absolute correlation coefficient.
3. **Anomaly Detection via Residuals**:
   - Let X be the sensor from the highest correlated pair with the lexicographically smaller name (e.g., if the pair is 'sensor_A' and 'sensor_B', X is 'sensor_A').
   - Let Y be the other sensor in the pair.
   - Fit a simple linear regression model $Y = mX + c$ using ordinary least squares.
   - Calculate the residuals: $residual = Y - (mX + c)$.
   - Calculate the standard deviation of these residuals (use sample standard deviation, ddof=1).
   - Filter the dataset by removing any rows where the absolute residual is strictly greater than 3 times the standard deviation of the residuals.
4. **Hypothesis Testing**: Using the cleaned dataset from step 3, split the data chronologically into two halves. The first half should contain the first `N // 2` rows (where N is the number of rows after removing anomalies), and the second half should contain the remaining rows. Perform a Welch's t-test (two-sided, unequal variance) on the `sensor_C` values between these two halves.
5. **Reporting**: The script must save a JSON file at `/home/user/cleaning_summary.json` containing the following keys and values:
   - `"correlated_pair"`: A list of the two highly correlated sensor names, sorted alphabetically (e.g., `["sensor_A", "sensor_B"]`).
   - `"correlation_coefficient"`: The Pearson correlation coefficient of this pair (computed in step 2), rounded to 4 decimal places.
   - `"removed_anomalies_count"`: The integer number of rows removed during the anomaly detection step.
   - `"t_test_p_value"`: The p-value from the Welch's t-test on `sensor_C`, rounded to 4 decimal places.

Run your script to ensure `/home/user/cleaning_summary.json` is generated correctly.