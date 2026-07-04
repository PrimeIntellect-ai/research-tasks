You are an AI assistant helping a climate researcher organize and clean a large dataset of sensor measurements. 

The researcher has a massive, poorly formatted log file located at `/home/user/data/sensor_logs.csv`. The file is too large to load into memory all at once, so you must process it in a streaming fashion. 

The input CSV has the following columns:
`timestamp,sensor_id,metadata_json,raw_value`

Here are the issues you need to resolve:
1. **Typo correction:** Due to a logging bug, many `sensor_id` values are written with a typo, starting with `sensro_` instead of `sensor_` (e.g., `sensro_A12` should be `sensor_A12`). You need to fix this text error.
2. **Data extraction and calculation:** The `metadata_json` column contains a JSON string with calibration data and a status flag. For example: `{"calibration": {"offset": 2.5, "multiplier": 1.2}, "status": "active"}`.
   - You must calculate the `true_value` using the formula: `(raw_value + offset) * multiplier`.
3. **Filtering:** Only include rows where the JSON `status` field is exactly `"active"`. Discard all other rows (e.g., "maintenance", "offline").

Write a Python script at `/home/user/process_data.py` that reads `/home/user/data/sensor_logs.csv` line-by-line (or chunk-by-chunk) to keep memory usage low, processes the data according to the rules above, and writes the results to `/home/user/data/processed_measurements.csv`.

The output file `/home/user/data/processed_measurements.csv` must be a valid CSV with the following exact headers:
`timestamp,sensor_id,true_value`

The `true_value` should be rounded to exactly 2 decimal places. 

After writing the script, execute it so that `/home/user/data/processed_measurements.csv` is generated.