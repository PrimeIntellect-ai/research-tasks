You are an automation specialist tasked with building a data processing pipeline for server metric logs.

You have a raw log file located at `/home/user/raw_sensors.log`. This file contains unstructured system logs where sensor readings are embedded in the text. You need to extract this data, reshape it, and normalize the time series.

Please create a Python script that performs the following steps:
1. **Extraction**: Parse `/home/user/raw_sensors.log` to extract the timestamp, metric name, and value. The lines look like this: `2023-10-01 10:01:15 - System check: metric=temperature val=45.2`. Ignore any lines that do not match this pattern.
2. **Reshaping**: Convert the long-format data into a wide-format structure where each unique metric (`cpu`, `memory`, `temperature`) has its own column.
3. **Resampling**: Resample the time series into fixed 5-minute intervals starting exactly at `2023-10-01 10:00:00` and ending at `2023-10-01 10:20:00` (inclusive).
   - Use left-closed intervals (e.g., the `10:00:00` bin includes data from `10:00:00` up to, but not including, `10:05:00`).
   - If multiple readings for the same metric fall into the same 5-minute bin, aggregate them by taking the **mean**.
4. **Gap-Filling**: 
   - Forward-fill (`ffill`) any missing values from previous bins.
   - If a metric has no previous data to forward-fill (e.g., missing in the first bin), fill it with `0.0`.
5. **Output**: Round all metric values to 1 decimal place. Save the final processed data to `/home/user/processed_metrics.csv`.

The output CSV must strictly have the following columns in this exact order: `timestamp,cpu,memory,temperature`.
The `timestamp` column should be in the format `YYYY-MM-DD HH:MM:SS`.

Write and execute the Python code to perform this task.