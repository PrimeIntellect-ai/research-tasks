You are a data analyst tasked with building a mini-ETL feature engineering script. 

You have been provided with a time-series dataset of sensor readings located at `/home/user/sensor_data.csv`. The CSV has three columns: `timestamp` (integer), `sensor_id` (string), and `value` (float).

Your objective is to write and execute a Python script that processes this data through the following pipeline steps:

1. **Sort**: Ensure the data is sorted chronologically by `timestamp` for each `sensor_id`.
2. **Rolling Statistics**: Compute a rolling mean of the `value` column for each `sensor_id` using a window size of 3 and `min_periods=1`.
3. **Feature Extraction**: Create a new feature named `diff_from_rolling` by subtracting the rolling mean from the original `value`.
4. **Normalization**: For each `sensor_id` independently, apply Min-Max normalization to the `diff_from_rolling` feature so that its values scale exactly between 0.0 and 1.0. Name this feature `norm_diff`. (If the max and min are equal for a sensor, set all `norm_diff` values to 0.0).
5. **Aggregation**: Calculate the overall mean of the `norm_diff` feature for each `sensor_id`.

Finally, save these aggregated summary statistics to a JSON file located at `/home/user/summary.json`. The JSON file must contain a single dictionary where the keys are the `sensor_id`s and the values are the mean `norm_diff` rounded to exactly 4 decimal places.

Example of expected `/home/user/summary.json` format:
```json
{
  "sensor_A": 0.4000,
  "sensor_B": 0.4071
}
```

Please write the Python code to perform this task and execute it to generate the final JSON file.