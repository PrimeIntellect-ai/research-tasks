You are an automation specialist tasked with building a data processing pipeline to clean and normalize raw sensor data. 

You have been provided with a directory of raw CSV files located at `/home/user/input_data/`. These files contain readings from multiple sensors but suffer from data quality issues:
1. Duplicate records.
2. Inconsistent timestamp formats (some are UNIX epoch integers, some are ISO8601 strings).
3. Missing temperature values.

Write a Python script at `/home/user/pipeline.py` and run it to process the data according to the following rules:

1. **Ingest and Combine**: Read all CSV files in `/home/user/input_data/` and combine them.
2. **Hash-Based Deduplication**: Create a new column named `record_hash`. The value should be the MD5 hex digest of the exact string concatenation of the original `timestamp` and `sensor_id` fields (e.g., if timestamp is `"1633046400"` and sensor_id is `"A"`, the hash input is `"1633046400A"`). Remove duplicate rows based on `record_hash`, keeping the first occurrence.
3. **Timestamp Normalization**: Convert all `timestamp` values to a consistent ISO8601 UTC string format: `YYYY-MM-DDTHH:MM:SSZ` (e.g., `2021-10-01T00:00:00Z`). Assume UNIX epoch integers are in seconds and represent UTC times.
4. **Sorting**: Sort the deduplicated dataset first by `sensor_id` (ascending), then by the normalized `timestamp` (ascending).
5. **Interpolation**: The `temperature` column has missing values (empty strings or NaNs). Impute these missing values using linear interpolation, applied independently within each `sensor_id` group based on the sorted order.
6. **Output**: Save the cleaned dataset to `/home/user/output_data/clean_data.csv`. The output CSV must contain the following columns in this exact order: `record_hash`, `timestamp`, `sensor_id`, `temperature`, `humidity`. Ensure `temperature` and `humidity` are formatted to one decimal place (e.g., `20.0`).

The `/home/user/output_data/` directory must be created if it does not exist. Run your script to produce the final `clean_data.csv`.