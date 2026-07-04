You are a data engineer tasked with building an ETL pipeline to process messy IoT telemetry data. 

You have been provided with two input datasets in the `/home/user/raw_data/` directory:
1. `telemetry.csv`: A large file containing sensor readings. Columns: `timestamp` (string, mixed formats), `device_id` (string), `sensor_type` (string, e.g., 'temperature', 'humidity'), and `value` (float, contains missing values/NaNs). This file contains exact duplicate rows and out-of-order data.
2. `metadata.json`: A JSON array of device metadata. Format: `[{"device_id": "D1", "site": "SiteA", "alert_threshold": 80.5}, ...]`.

Your objective is to write and execute a Python script (`/home/user/etl.py`) that performs the following pipeline:

1. **Cleaning & Normalization:**
   - Read `telemetry.csv` and remove exact duplicate rows.
   - Parse the `timestamp` column (which mixes formats like 'YYYY-MM-DD HH:MM:SS' and 'MM/DD/YYYY HH:MM') and normalize it to UTC timezone-aware Datetime objects. 

2. **Imputation:**
   - Sort the telemetry data chronologically.
   - For missing `value`s (NaNs), perform linear interpolation grouped by `device_id` and `sensor_type`. 
   - If leading or trailing values are still missing after interpolation, fill them with `0.0`.

3. **Merging:**
   - Join the cleaned telemetry data with the device metadata from `metadata.json` using `device_id`.
   - Drop any records for devices that do not exist in `metadata.json`.

4. **Aggregation & Grouping:**
   - Group the data into 1-hour tumbling windows based on the normalized `timestamp`, as well as by `site` and `sensor_type`.
   - For each group, calculate:
     - `avg_value`: The mean of the `value`s (rounded to 2 decimal places).
     - `alert_count`: The total number of readings in that window where the imputed `value` was strictly greater than the `alert_threshold` for that device.

5. **Output:**
   - Write the aggregated results to `/home/user/output/summary.jsonl` (JSON Lines format).
   - Ensure the `/home/user/output/` directory exists.
   - Each line must be a JSON object with keys: `"window_start"` (ISO 8601 string, e.g., `"2023-10-01T12:00:00Z"`), `"site"`, `"sensor_type"`, `"avg_value"`, and `"alert_count"`.
   - Sort the final output by `window_start` (ascending), then `site` (ascending), then `sensor_type` (ascending).

You may install any necessary Python libraries (e.g., `pandas`, `numpy`) using `pip`. Provide the script, run it, and ensure the final output file is generated correctly.