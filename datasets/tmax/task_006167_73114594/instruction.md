You are a data scientist tasked with cleaning a raw sensor dataset, running inference using a predefined linear model, validating its numerical accuracy against a baseline, and performing hypothesis testing.

You have been provided with two files:
1. `/home/user/raw_sensors.csv`: Raw sensor readings containing columns `timestamp`, `sensor_id`, `temp`, `pressure`, and `humidity`.
2. `/home/user/baseline_predictions.csv`: Baseline model predictions from a previous system, containing columns `timestamp`, `sensor_id`, and `power_output`.

Please write a script in any language of your choice to perform the following steps:

**1. ETL Pipeline Construction**
Process the `raw_sensors.csv` dataset in this exact order:
a) Remove any rows where `temp` is missing (NaN/null).
b) Remove any rows where `temp` is an outlier (defined strictly as `temp < -50` or `temp > 150`).
c) For the remaining data, fill any missing `pressure` values with the median `pressure` of that specific `sensor_id` (calculated only on the data remaining after steps a and b).
d) Fill any missing `humidity` values with the overall mean `humidity` of the remaining data.

**2. Model Architecture Reconstruction and Inference**
Reconstruct the following linear model to predict `power_output` based on the cleaned data:
`power_output = (0.5 * temp) + (0.2 * pressure) - (0.1 * humidity) + 5.0`
Compute the `power_output` for all rows in your cleaned dataset.

**3. Numerical Accuracy Testing**
Compare your computed `power_output` values against the `power_output` values in `/home/user/baseline_predictions.csv`. Match the records by `timestamp` and `sensor_id`. Compute the Mean Squared Error (MSE) between your predictions and the baseline predictions.

**4. Hypothesis Testing**
Perform an independent two-sided Welch's t-test (assuming unequal variances) to determine if there is a statistically significant difference in your computed `power_output` between sensors `S1` and `S2`. Calculate the t-statistic and the p-value.

**Output Generation**
Create a JSON file at `/home/user/results.json` containing the following exact keys:
- `"clean_row_count"`: The number of rows remaining after the ETL steps (integer).
- `"mean_power"`: The mean of your computed `power_output` across all cleaned rows (float, rounded to 4 decimal places).
- `"mse"`: The Mean Squared Error from step 3 (float, rounded to 4 decimal places).
- `"t_stat"`: The t-statistic from step 4 (float, rounded to 4 decimal places).
- `"p_value"`: The p-value from step 4 (float, rounded to 4 decimal places).

Ensure the file is strictly valid JSON.