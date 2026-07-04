You are an automation specialist tasked with creating a robust data processing pipeline in Bash. We receive raw telemetry data from our IoT devices, but the data pipeline currently suffers from a known defect: some sensors occasionally inject embedded newlines into their text fields, which corrupts downstream line-by-line processing.

Your objective is to build a Bash pipeline that reads a raw CSV, applies a strict quality gate, performs time-based mathematical aggregation, and bulk-loads the result into a SQLite database. 

Here are your exact requirements:

1. **Input Data**: The input file is located at `/home/user/raw_telemetry.csv`. It does not have a header row. The columns are: `timestamp` (Unix epoch integer), `sensor_id` (string), `value` (float), and `notes` (string).
2. **Quality Gate**: Write a Bash script `/home/user/pipeline.sh` that processes this CSV. It must strictly filter out any malformed rows. Because of the embedded newline bug, you should simply silently drop any line that does not have exactly 4 comma-separated fields.
3. **Time-based Bucketing and Aggregation**:
   - For the valid rows, group the data into 1-hour buckets based on the `timestamp`. (A 1-hour bucket starts exactly at the hour, i.e., `bucket = (timestamp / 3600) * 3600`).
   - Calculate the mathematical average of the `value` column for each `sensor_id` within each 1-hour bucket.
   - The average must be rounded to exactly 2 decimal places.
4. **Database Bulk Export**:
   - Your script must create a SQLite database at `/home/user/metrics.db`.
   - Create a table named `hourly_aggregates` with the schema: `bucket_time` (INTEGER), `sensor_id` (TEXT), `avg_value` (REAL).
   - Bulk insert the aggregated results into this table.

The final state must be a populated SQLite database at `/home/user/metrics.db` containing only the cleanly aggregated data. You may use standard Unix utilities (like `awk`, `sed`, `grep`, `sqlite3`) inside your Bash script.