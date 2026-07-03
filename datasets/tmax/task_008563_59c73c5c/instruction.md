You are a data scientist tasked with cleaning a large dataset of sensor readings and analyzing numerical precision issues. 

The raw data is located in `/home/user/raw_data/`. It consists of multiple CSV files containing sensor readings. The columns in each CSV are:
- `timestamp`: Integer (seconds since epoch)
- `sensor_id`: String (e.g., "sensor_A", "sensor_B")
- `value`: Float

Part 1: Numerical Accuracy Testing
You need to demonstrate the impact of floating-point precision loss when aggregating this data. For each `sensor_id` across the entire dataset (before any cleaning), calculate:
1. The **exact sum** of the `value` column using Python's `math.fsum()` to preserve precision.
2. The **naive float32 sum**. To compute this, iterate through the values, cast each individual value to `numpy.float32`, and accumulate the sum in a `numpy.float32` variable (e.g., `np.float32(current_sum) + np.float32(value)`).

Calculate the absolute difference (error) between the exact sum and the naive sum for each sensor.

Part 2: Data Cleaning and Aggregation
1. Filter the dataset by removing any rows where `value` is anomalous. An anomalous value is strictly less than `0.0` or strictly greater than `100000.0`.
2. Group the cleaned data by `sensor_id` and **day**. A day is defined as a contiguous 86400-second window, starting from timestamp `0` (e.g., Day 0 is timestamps `0` to `86399`, Day 1 is `86400` to `172799`).
3. Calculate the average `value` for each group (using standard float64 pandas mean).
4. Save the resulting aggregated data as a Parquet file at `/home/user/aggregated.parquet`. It should contain the columns: `sensor_id`, `day` (integer), and `mean_value` (float).

Part 3: Reporting
Create a summary report formatted as a JSON file at `/home/user/summary.json`. The keys should be the `sensor_id`s, and the values should be objects containing:
- `exact_sum`: Float (from Part 1, rounded to 4 decimal places)
- `absolute_error`: Float (from Part 1, rounded to 4 decimal places)
- `cleaned_row_count`: Integer (the number of valid, non-anomalous rows for this sensor from Part 2)

Example of `/home/user/summary.json`:
```json
{
  "sensor_A": {
    "exact_sum": 1000050.1234,
    "absolute_error": 12.5021,
    "cleaned_row_count": 4500
  },
  "sensor_B": { ... }
}
```

Ensure all dependencies are installed, process the data efficiently, and generate the requested outputs.