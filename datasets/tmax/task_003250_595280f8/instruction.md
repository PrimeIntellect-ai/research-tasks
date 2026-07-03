You are a data scientist tasked with cleaning a dataset of sensor readings and statistically validating a predictive model's output against the cleaned data. 

A dirty dataset containing recent IoT sensor readings is located at `/home/user/sensor_data.csv`. The predictive model expects the average temperature to be `21.5` degrees. Your job is to enforce a strict data schema, aggregate the clean data, calculate a 95% confidence interval for the mean temperature, and determine if the model's expectation is statistically plausible.

Please write and execute a Go program to perform this analysis. Create your Go project in `/home/user/analyzer`.

**Step 1: Data Schema Enforcement**
The CSV file has the following columns: `timestamp`, `sensor_id`, `temperature`, `humidity`.
Read the CSV and discard any rows that fail to meet **all** of these rules:
- `timestamp`: Must be a non-empty string.
- `sensor_id`: Must be an integer between `1` and `10` (inclusive).
- `temperature`: Must be a float between `-50.0` and `50.0` (inclusive).
- `humidity`: Must be a float between `0.0` and `100.0` (inclusive).
*Note: Any row with missing data, unparseable data types, or out-of-bounds values should be completely excluded from the analysis.*

**Step 2: Statistical Aggregation & Hypothesis Testing**
For the valid rows, calculate the sample mean and the sample standard deviation of the `temperature` column.
Then, calculate the 95% confidence interval for the mean temperature. 
Use the Normal distribution approximation (use a Z-value of `1.96`). 
Formula for Margin of Error: `1.96 * (sample_standard_deviation / sqrt(number_of_valid_rows))`

**Step 3: Model Validation & Reporting**
Determine if the model's expected temperature of `21.5` falls within your calculated 95% confidence interval `[ci_lower, ci_upper]`.
Your Go program must output the final results to a JSON file at `/home/user/report.json` with the following exact keys:
- `"valid_rows"`: (integer) The count of rows that passed schema enforcement.
- `"mean_temperature"`: (float) The sample mean.
- `"ci_lower"`: (float) The lower bound of the 95% confidence interval.
- `"ci_upper"`: (float) The upper bound of the 95% confidence interval.
- `"model_validated"`: (boolean) `true` if 21.5 is >= ci_lower and <= ci_upper, otherwise `false`.

Please round the float values in your JSON output to exactly 4 decimal places.

Once you have written your Go code, compile and run it to generate the `/home/user/report.json` file.