I have a messy dataset of sensor readings in a JSONL file located at `/home/user/raw_sensors.jsonl`. An old ETL job failed and retried a few times, so the file contains duplicate entries. Furthermore, the dataset aggregates data from different systems, so the timestamps and sensor names are not standardized.

I need you to write and run a Python script at `/home/user/process.py` that processes this data and produces a clean, aggregated CSV file.

Here are the requirements for processing:
1. **Normalization & Standardization**:
   - Standardize the `sensor` field by converting it to lowercase and replacing any spaces with underscores (e.g., "Temp A" becomes "temp_a").
   - Normalize the `time` field into integer Unix epoch seconds. The input `time` might be an ISO8601 string (e.g., "2023-01-01T12:15:30Z"), an integer representing Unix epoch seconds, or an integer representing Unix epoch milliseconds. 
2. **Deduplication**:
   - Because of the ETL retries, there are duplicate records. Deduplicate the records based on the standardized `sensor` name and the normalized integer epoch `time`. If multiple records have the same sensor and time, keep only the first one that appears in the file.
3. **Time-based Bucketing and Aggregation**:
   - Group the cleaned data into 1-hour buckets. A bucket is identified by the Unix epoch time (in seconds) of the start of the hour (i.e., time rounded down to the nearest multiple of 3600).
   - Calculate the average `value` for each sensor within each hourly bucket.
4. **Database Import and Export**:
   - Save the aggregated results into a SQLite database located at `/home/user/sensor_data.db`.
   - Create a table named `hourly_aggregates` with columns: `sensor_name` (TEXT), `bucket_time` (INTEGER), and `avg_value` (REAL).
   - Export the contents of the `hourly_aggregates` table into a CSV file at `/home/user/aggregated.csv`. The CSV should have a header row (`sensor_name,bucket_time,avg_value`) and the rows must be sorted by `sensor_name` ascending, then by `bucket_time` ascending. Round `avg_value` to 2 decimal places in the CSV.

Please write the script, execute it, and ensure `/home/user/aggregated.csv` is created exactly as specified.