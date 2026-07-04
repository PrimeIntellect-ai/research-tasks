You are a data engineer tasked with building an ETL pipeline to process raw IoT sensor data. 

You have been provided with a CSV file at `/home/user/raw_sensors.csv` containing raw, unaligned time series data from two sensors (`temp_A` and `press_B`). The sensors log data at irregular intervals and use different timestamp formats.

Your goal is to write a Python script (save it as `/home/user/etl_pipeline.py`) that performs the following steps when executed:

1. **Ingest and Parse Timestamps:**
   - Read `/home/user/raw_sensors.csv`.
   - The `timestamp` column contains mixed formats depending on the `sensor_id`:
     - `temp_A` uses Unix epoch time (integer, e.g., `1672531260`).
     - `press_B` uses ISO8601 strings (e.g., `"2023-01-01T00:02:00Z"`).
   - Convert all timestamps to standard UTC datetime objects.

2. **Time Series Alignment:**
   - Resample the data into exactly 5-minute intervals for both sensors, labeled by the *start* (left edge) of the bin (e.g., `2023-01-01 00:00:00` covers `00:00:00` up to `00:04:59`).
   - For bins with multiple readings, aggregate by taking the mean.
   - For bins with missing readings, use forward-fill (carry over the previous bin's value), but limit the forward-fill to a maximum of 1 consecutive bin (i.e., `limit=1`). If a value is still missing, leave it as NaN/null.
   - Restructure the data so that `temp_A` and `press_B` are separate columns.

3. **Anomaly Detection (on the aligned data):**
   - Check the aligned time series for the following anomalies:
     - **`temp_A`**: Identify any 5-minute bin where the aligned temperature is strictly greater than `85.0`. The reason string should be `"threshold_exceeded"`.
     - **`press_B`**: Identify any 5-minute bin where the absolute difference in pressure from the *immediately preceding* 5-minute bin is strictly greater than `10.0`. Do not calculate differences across NaNs if the previous bin was NaN. The reason string should be `"jump_exceeded"`.

4. **Output Generation:**
   - Save the aligned dataframe to `/home/user/aligned_data.parquet`. The index must be the UTC timestamp, and columns must be `temp_A` and `press_B` containing floats.
   - Save the anomalies to `/home/user/anomalies.json` as a JSON array of objects. Each object must have exactly this structure:
     `{"timestamp": "YYYY-MM-DDTHH:MM:SSZ", "sensor_id": "<sensor_name>", "reason": "<reason_string>"}`
     Sort the JSON array chronologically by timestamp, and then alphabetically by `sensor_id` if timestamps match.
   - Implement pipeline logging: Append a log message to `/home/user/etl.log` at the end of the script exactly matching this format: `[INFO] Pipeline finished. Anomalies detected: <N>`, where `<N>` is the total number of anomalies found.

Write and execute the script to complete the task.