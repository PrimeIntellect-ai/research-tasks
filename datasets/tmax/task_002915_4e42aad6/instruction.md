You are an ETL data engineer debugging a pipeline failure. An unreliable upstream cron job retried multiple times, inserting duplicate records into your local SQLite database.

Your task is to write a Go program `/home/user/pipeline.go` that cleans this data and calculates rolling statistics.

Here is the setup:
- Database: `/home/user/warehouse.db`
- Table: `readings (ts INTEGER, sensor_id TEXT, value REAL)`

The table contains duplicate rows (same `ts` and `sensor_id`) because of the ETL retry bug.

Requirements for `/home/user/pipeline.go`:
1. Query the `warehouse.db` database.
2. Deduplicate the records: for any given `ts` and `sensor_id`, keep only one record (if values differ for the exact same timestamp and sensor, which they don't in this case, keeping any is fine).
3. Compute a 2-period rolling average for the `value` column, partitioned by `sensor_id` and ordered by `ts` ascending. 
   - The rolling average for the first record of a sensor is just its own `value`.
   - The rolling average for subsequent records is the average of the current `value` and the immediate previous `value` in time for that sensor.
4. Export the cleaned, enriched data to `/home/user/output.csv` with the headers: `ts,sensor_id,value,rolling_avg`.
5. Format `value` and `rolling_avg` to 1 decimal place. Order the CSV by `sensor_id` ascending, then `ts` ascending.

You will need to initialize a Go module and fetch the SQLite driver (e.g., `github.com/mattn/go-sqlite3`) in `/home/user/`.

Once you have written and executed the Go script, ensure `/home/user/output.csv` exists and is formatted correctly.