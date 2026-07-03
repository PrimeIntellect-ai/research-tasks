You are a data scientist tasked with building an automated data cleaning and anomaly detection pipeline for a set of IoT temperature sensors. 

The raw data is located in `/home/user/input/sensor_data.csv` and contains three columns: `timestamp` (ISO 8601 format), `sensor_id` (string), and `temperature` (float). The data has irregular sampling intervals, missing gaps, and occasional extreme outliers.

Your goal is to write and execute a Python script (save it as `/home/user/process_pipeline.py`) that performs the following exact sequence of steps:

1. **Load Data**: Read the CSV file.
2. **Resampling**: Group the data by `sensor_id`. For each sensor, resample the time series to a strict 1-minute frequency. If there are multiple readings in a single minute, take the average. If there are missing minutes, create empty rows for them.
3. **Interpolation**: Fill gaps in the 1-minute time series using linear interpolation. Only interpolate gaps up to a maximum of 5 consecutive minutes (if a gap is larger, leave the remaining NaNs).
4. **Anomaly Detection**: 
    - Calculate a trailing 10-minute rolling mean and rolling standard deviation for each sensor (use `min_periods=3`, meaning at least 3 valid prior/current points are needed; otherwise rolling stats are NaN).
    - Identify anomalies: A point is an anomaly if the absolute difference between its `temperature` and the rolling mean is strictly greater than `3 * rolling_std`. (Do not flag if rolling_std is NaN or 0).
    - Save all detected anomalies to `/home/user/output/anomalies.json`. The JSON should be a list of dictionaries, each containing exactly: `{"timestamp": "YYYY-MM-DD HH:MM:00", "sensor_id": "...", "temperature": ...}`. Sort the list chronologically, then alphabetically by sensor_id.
5. **Imputation**: In the resampled dataframe, replace the identified anomaly temperatures with `NaN`. Then, apply a forward fill (`ffill`) to impute these newly created NaNs.
6. **Hourly Aggregation**: Resample the cleaned 1-minute data to a 1-hour frequency. For each hour and sensor, calculate the `mean`, `min`, and `max` temperature. 
7. **Export**: Save the aggregated hourly statistics to `/home/user/output/hourly_stats.csv`. The CSV should have columns: `timestamp`, `sensor_id`, `mean_temp`, `min_temp`, `max_temp`. Sort by `timestamp` ascending, then `sensor_id` ascending. Format floats to 2 decimal places.

**Environment setup:**
- You will need to install any necessary Python libraries (e.g., `pandas`, `numpy`) in the user environment (`pip install --user`).
- Create the output directory `/home/user/output` before writing files.

Ensure your pipeline runs successfully and produces the two required output files.