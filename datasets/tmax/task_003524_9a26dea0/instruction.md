You are an automation specialist managing an ETL pipeline for IoT temperature sensors. 

Our current cron-based ETL job has a major flaw: when it retries after a partial failure, it appends duplicate data. Additionally, our new sensors use various character encodings and timestamp formats, causing the pipeline to break.

Your task is to create and run a robust, idempotent Python ETL script that processes historical sensor data.

Here is the setup:
1. Raw data files are located in `/home/user/remote_inbox/` (simulating a remote drop folder).
2. The pipeline must process these files in parallel (e.g., using Python's `multiprocessing` or `concurrent.futures`) to speed up execution.
3. You must handle the following data inconsistencies:
   - `sensor_alpha.csv`: UTF-8 encoding. Timestamps are ISO8601 (e.g., `2023-10-01T10:00:00Z`).
   - `sensor_beta.csv`: UTF-16 encoding. Timestamps are Unix epochs (e.g., `1696154400`).
   - `sensor_gamma.csv`: ISO-8859-1 (latin1) encoding. Timestamps are `DD-MM-YYYY HH:MM:SS` in UTC (e.g., `01-10-2023 10:00:00`).
4. **Idempotency & Deduplication:** The raw data contains intentional duplicate rows (simulating retry pollution). You must deduplicate records so that there is only one unique record per `sensor_id` and `timestamp`. If there are exact duplicates, keep any one of them.
5. **Aggregation:** For each sensor, sort the deduplicated data chronologically. Calculate a rolling average of the `temperature` column using a window of the **current record and the 2 previous records** (a 3-record rolling average). 
6. **Output:** Combine the results for all sensors and write them to a single CSV file at `/home/user/output/clean_aggregates.csv`.
   - The CSV must have exactly these columns: `sensor_id`, `timestamp_utc`, `temp_rolling_avg`.
   - `timestamp_utc` must be formatted strictly as `%Y-%m-%d %H:%M:%S`.
   - `temp_rolling_avg` must be rounded to exactly 2 decimal places.
   - The final CSV should be sorted primarily by `sensor_id` (alphabetically) and secondarily by `timestamp_utc` (chronologically).

Write your Python script to `/home/user/etl_job.py`, run it to generate the output file, and ensure the output directory exists. You may install standard data processing libraries like `pandas` if needed.