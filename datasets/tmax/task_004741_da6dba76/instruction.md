You are a data engineer tasked with building a robust ETL pipeline for a fleet of IoT-enabled delivery vehicles.

Raw sensor data is continually dropped into `/home/user/raw_data/measurements.jsonl`. This file contains JSON Lines format records, but the ingestion system occasionally writes duplicate raw lines, and sensor dropouts mean that `speed` is sometimes recorded as `null`.

Your objective is to write and execute a Python script at `/home/user/etl_pipeline.py` that processes this data and loads it into an SQLite database. 

Your script must perform the following steps:
1. **Deduplication:** Read `/home/user/raw_data/measurements.jsonl` and remove exact duplicate lines. (Treat the entire raw JSON string as the deduplication key, effectively mimicking a hash-based deduplication of the payload).
2. **Imputation:** Parse the JSON data. For each `vehicle_id`, linearly interpolate any missing (`null`) `speed` values based on the time difference between the surrounding timestamps. (Assume the data can be sorted by `vehicle_id` and `ts`).
3. **Time-based Bucketing:** Group the cleaned data into 1-hour buckets based on the `ts` timestamp (truncate the minutes and seconds, e.g., `2023-10-01T10:15:00` becomes `2023-10-01 10:00:00`).
4. **Aggregation:** For each 1-hour bucket and `vehicle_id`, calculate the average `speed` (`avg_speed`) and the maximum `temp` (`max_temp`).
5. **Database Export:** Save the aggregated results into an SQLite database located at `/home/user/fleet_data.db` in a table named `hourly_stats`. The table must have the following columns: `bucket` (TEXT format 'YYYY-MM-DD HH:MM:SS'), `vehicle_id` (TEXT), `avg_speed` (REAL), and `max_temp` (REAL).

After writing and running the script successfully, you need to schedule it. 
Create a file named `/home/user/cron_schedule.txt` and write the exact crontab line required to schedule `/home/user/etl_pipeline.py` to run via `python3` at exactly the top of every hour (minute 0).

Constraints:
- Use Python 3. You may use `pandas` and standard libraries (`sqlite3`, `json`, etc.).
- Ensure your script creates the database and table if they do not exist, and clears the table before inserting to prevent duplicate runs from appending duplicate data during your tests.