You are a log analyst investigating intermittent system failures across a fleet of servers. You have received a raw, unordered, and partially corrupted telemetry log file located at `/home/user/sensor_logs.csv`.

The CSV has the following headers: `timestamp,server_id,cpu_temp,memory_mb,latency_ms`

However, the data has issues:
1. The rows are completely out of chronological order.
2. Some `cpu_temp` values are missing (empty strings).
3. Some `latency_ms` values are missing (empty strings).

Your task is to write a Go program at `/home/user/analyze.go` to process this data. The program must:
1. Parse the CSV and group the records by `server_id`.
2. Sort the records for each server chronologically by `timestamp` (integer Unix epoch).
3. Process the data for each server **in parallel** using goroutines.
4. **Impute/Interpolate missing values**:
   - For missing `cpu_temp` values, apply **linear interpolation** based on the nearest chronological preceding and succeeding valid temperatures for that server. (Assume the first and last records for any server always have valid `cpu_temp` values in this dataset).
   - For missing `latency_ms` values, replace them with the **mean latency** of all *valid* latency records for that specific server.
5. **Feature Extraction**: Calculate a new boolean feature `is_overheated` for every record, which is `true` if the (possibly interpolated) `cpu_temp` is strictly greater than 85.0.
6. **Aggregation**: For each server, calculate:
   - `max_temp`: The maximum `cpu_temp` (including interpolated values).
   - `avg_latency`: The average `latency_ms` across all records (after imputation).
   - `overheat_events`: The total number of records where `is_overheated` is true.

Finally, your Go program should write a summary report to `/home/user/server_summary.csv`.
The output CSV must have the following exact headers: `server_id,max_temp,avg_latency,overheat_events`
The rows in the output CSV must be sorted alphabetically by `server_id`.
Format all floating-point numbers (`max_temp` and `avg_latency`) to exactly 2 decimal places.

Compile and run your Go program to generate the output file.