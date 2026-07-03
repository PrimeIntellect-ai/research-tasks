You are a data scientist tasked with cleaning up a dataset corrupted by an ETL retry bug. Our sensor network pipeline recently experienced intermittent failures. When the ETL job retried, it produced duplicate records. Furthermore, network outages caused missing data points.

Your objective is to build a Python data pipeline that cleans, imputes, and enriches this dataset.

**Initial Setup:**
1. Create a Python virtual environment at `/home/user/venv`.
2. Install necessary data processing libraries (e.g., `pandas`) into this environment.
3. The raw data is located at `/home/user/raw_sensor_data.csv`.

**Data Processing Requirements:**
Write a Python script (e.g., `/home/user/process_sensors.py`) using your virtual environment to perform the following operations:

1. **Deduplication:** Sort the data by `sensor_id` and `timestamp`. Due to the ETL bug, there are multiple records with the same `sensor_id` and `timestamp` but potentially conflicting `temperature` values. Keep the *first* occurrence (based on the original file order) and drop the subsequent duplicates for the same sensor and timestamp.
2. **Resampling & Imputation:** For each `sensor_id`, resample the time series to a strict 1-hour frequency (`1H`), starting from the minimum timestamp and ending at the maximum timestamp for that specific sensor. Fill missing `temperature` values using **linear interpolation**. However, you must limit the interpolation: do not fill gaps that are larger than 3 consecutive hours (i.e., maximum 3 consecutive NaNs can be filled).
3. **Rolling Statistics:** Compute a 4-hour rolling average of the `temperature` for each sensor (this includes the current hour and the previous 3 hours). The rolling window should require a minimum of 2 valid (non-null) observations to produce a value; otherwise, it should be null/NaN.
4. **Formatting:** Round both `temperature` and `rolling_avg_temp` to exactly 2 decimal places.

**Output Specification:**
Save the final processed data to `/home/user/cleaned_sensor_stats.csv`.
- The file must be a CSV with a header.
- Required columns: `sensor_id`, `timestamp`, `temperature`, `rolling_avg_temp`.
- The `timestamp` column must be formatted as `YYYY-MM-DD HH:MM:SS`.
- The output must be sorted by `sensor_id` ascending, then by `timestamp` ascending.
- Any remaining null/NaN values should be output as empty strings in the CSV.

Write and execute the script to generate the final output file.