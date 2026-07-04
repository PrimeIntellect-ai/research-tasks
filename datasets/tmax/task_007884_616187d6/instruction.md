You are a data analyst tasked with building an automated time-series processing pipeline. 

You have a directory `/home/user/incoming_data/` containing several CSV files from different IoT sensors. Each file is named `sensor_<id>.csv` (e.g., `sensor_1.csv`). The CSVs have two columns: `timestamp` and `reading`. However, the timestamp formats are inconsistent:
- `sensor_1.csv` uses Unix epoch time (e.g., `1672531200`).
- `sensor_2.csv` uses `MM/DD/YYYY HH:MM:SS` string formats (e.g., `01/01/2023 01:15:00`).

Your task is to write a Python script `/home/user/process_pipeline.py` that does the following:
1. **Timestamp Alignment & Parsing:** Read all CSV files in `/home/user/incoming_data/`. Parse the timestamps and align them to a standard UTC format.
2. **Sorting & Grouping:** Truncate each timestamp down to the hour (e.g., `2023-01-01 01:15:00` becomes `2023-01-01 01:00:00`). Sort the combined data chronologically and group it by `sensor_id` (extracted from the filename) and the hourly timestamp bucket. Calculate the average `reading` for each sensor per hour.
3. **Database Bulk Import:** Export the aggregated results into a SQLite database at `/home/user/metrics.db`. Create a table named `hourly_aggregates` with columns: `sensor_id` (TEXT), `hour_bucket` (TEXT format 'YYYY-MM-DD HH:MM:SS'), and `avg_reading` (REAL). Replace the table if it exists.
4. **Pipeline Logging:** Use Python's built-in `logging` module to append to `/home/user/pipeline.log`. When the script finishes, it should log a single INFO line: `Successfully processed <N> total rows.`, where `<N>` is the total number of raw rows read across all files before aggregation.

After writing the script, execute it so the database and log file are generated.

Finally, we need to schedule this pipeline. Create a crontab definition file at `/home/user/pipeline.cron` that schedules `/usr/bin/python3 /home/user/process_pipeline.py` to run at minute 15 of every hour. (You only need to create the file containing the cron expression, do not attempt to install it into the system cron daemon).