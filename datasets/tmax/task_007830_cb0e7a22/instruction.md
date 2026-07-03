You are an automation specialist managing data ingestion pipelines. You need to write a Python script that unifies time-series sensor data from two different factory lines, normalizes the format, removes exact duplicates using hash-based deduplication, and saves the final result as a Parquet file.

You are given two input files in `/home/user/inputs/`:
1. `/home/user/inputs/factory_1.csv`: Contains data in a **wide format**. Columns are `timestamp`, and various sensor names like `Temp_A`, `Temp_B`, `Humidity_A`. 
2. `/home/user/inputs/factory_2.json`: Contains data in a **long format**. An array of objects with keys `time` (timestamp), `sensor` (sensor name), and `reading` (sensor value).

Write a Python script at `/home/user/process_pipeline.py` that does the following:

1. **Read & Reshape:** Load both files. Convert the CSV data from wide format to long format so that both datasets conceptually share three core columns: timestamp, sensor ID, and the reading value.
2. **Normalize Data:**
   - Standardize the column names to `timestamp`, `sensor_id`, and `value`.
   - Ensure all `timestamp` values are standardized to UTC and formatted as strictly ISO 8601 strings in the format `YYYY-MM-DDTHH:MM:SSZ` (e.g., `2023-10-01T12:00:00Z`).
   - Convert all `sensor_id` strings to entirely lowercase (e.g., `Temp_A` becomes `temp_a`).
   - Ensure `value` is cast to a float.
3. **Hash-Based Deduplication:** 
   - Combine the datasets.
   - For every row, create a new column called `record_hash`.
   - The value of `record_hash` must be the MD5 hash (hexadecimal digest) of a string formatted exactly as: `"{timestamp}_{sensor_id}_{value:.2f}"`.
     *(Example string to hash: `"2023-10-01T10:00:00Z_temp_a_25.40"`)*
   - Drop any duplicate rows based on the `record_hash` column. Keep the first occurrence.
4. **Sort & Export:**
   - Sort the resulting dataset first by `timestamp` (ascending), then by `sensor_id` (ascending).
   - Save the finalized DataFrame to `/home/user/unified_sensors.parquet` with the columns `timestamp`, `sensor_id`, `value`, and `record_hash`.

You may need to install standard Python data processing libraries like `pandas` and `pyarrow` or `fastparquet` using pip. Execute your script to generate the final output file before completing the task.