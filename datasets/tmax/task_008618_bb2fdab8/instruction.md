You are a data engineer managing an ETL pipeline for time-series sensor data. Recently, a bug in the pipeline scheduler caused several extraction jobs to retry unexpectedly. This resulted in duplicate records spread across multiple file formats in the raw data directory.

Your task is to write and execute a Python script that reads the raw data, deduplicates the time-series records, computes daily aggregates, and outputs a clean summary.

**Input Data:**
The raw data is located in `/home/user/time_series_in/`.
You will find two files:
1. `batch_alpha.csv` (CSV format)
2. `batch_beta.jsonl` (JSON Lines format)

Both files contain the following fields/columns:
- `timestamp`: An ISO8601 formatted datetime string (e.g., "2023-10-01T10:00:00Z").
- `sensor_id`: A string representing the sensor (e.g., "S1").
- `value`: A float representing the sensor reading.
- `etl_run_id`: An integer representing the run ID of the ETL job.

**Processing Requirements:**
1. **Deduplication:** Because of the retries, there are duplicate records for the exact same `timestamp` and `sensor_id`. To resolve duplicates, you must keep **only** the record with the highest `etl_run_id`.
2. **Aggregation:** After deduplication, calculate the daily average `value` for each `sensor_id`. The "day" should be extracted from the `timestamp` (i.e., the `YYYY-MM-DD` portion).
3. **Output:** 
   - Write the aggregated results to a CSV file located at `/home/user/time_series_out/daily_averages.csv`. Create the output directory if it does not exist.
   - The output CSV must have exactly three columns in this order: `date`, `sensor_id`, `avg_value`.
   - `date` must be in `YYYY-MM-DD` format.
   - `avg_value` must be rounded to exactly 2 decimal places (e.g., `15.00`, `12.34`).
   - The output must include a header row.
   - The rows must be sorted in ascending order first by `date`, then by `sensor_id`.

Write the Python script, execute it, and ensure the final output file matches the exact specifications.