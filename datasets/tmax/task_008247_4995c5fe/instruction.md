You are a data engineer tasked with building a robust Python ETL pipeline to process IoT sensor data. 

In the `/home/user/raw_data` directory, there are multiple `.jsonl` files (JSON Lines format) containing raw sensor readings. You need to write a Python script (e.g., `process_etl.py`) that reads these files in parallel, cleans the data, aligns timestamps, runs a validation gate, and detects changepoint anomalies.

Your pipeline must perform the following steps:

1. **Parallel Extraction**: Read all `.jsonl` files in `/home/user/raw_data` concurrently (using Python's `multiprocessing` or `concurrent.futures`).
2. **Cleaning & Normalization**:
   - Parse each JSON line. Expected fields: `ts` (ISO-8601 string), `sensor_id` (string), `value` (float).
   - Drop any records missing `ts`, `sensor_id`, or where `value` is `null` / missing.
   - Deduplicate records: if multiple records are exactly identical (same `ts`, `sensor_id`, and `value`), keep only one.
3. **Validation Checkpoint**:
   - Count the total number of invalid/dropped records (due to missing fields, NOT including exact duplicates removed).
   - Append a line to `/home/user/etl.log` strictly in this format: `VALIDATION_GATE: Dropped <N> invalid records.`
4. **Timestamp Alignment**:
   - Parse the `ts` string and convert it to an integer Epoch timestamp (seconds since 1970-01-01 00:00:00 UTC).
   - Round *down* (floor) the timestamp to the nearest second.
   - If multiple valid records exist for the same `sensor_id` at the exact same aligned second, average their `value`s to produce a single record per `sensor_id` per second.
5. **Changepoint/Anomaly Detection**:
   - For each `sensor_id`, sort the aligned records chronologically.
   - Calculate the absolute difference in `value` between consecutive aligned timestamps.
   - A "changepoint anomaly" occurs if the absolute difference is strictly greater than `10.0`.
6. **Output**:
   - Save the fully cleaned, deduplicated, aligned, and averaged dataset to `/home/user/clean_data.csv` (Headers: `timestamp,sensor_id,value`). Sort by `timestamp` ascending, then `sensor_id` ascending.
   - Save the detected anomalies to `/home/user/anomalies.json`. This should be a JSON array of objects, sorted by time, then sensor_id. Each object should have: `{"timestamp": <aligned_epoch_int>, "sensor_id": "<id>", "previous_value": <val>, "current_value": <val>, "difference": <absolute_diff>}`. (The timestamp corresponds to the *current* record where the changepoint was detected).

Ensure your script handles everything end-to-end and outputs the exact files requested.