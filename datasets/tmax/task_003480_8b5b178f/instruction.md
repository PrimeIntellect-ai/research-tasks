You are a Database Reliability Engineer (DBRE) tasked with analyzing backup metadata logs to identify anomalously large database backups. Our logging pipeline recently changed, and the raw logs are now in a mixed-schema JSONL format. 

Your task is to write a Python script (and any necessary shell commands) to process these logs, analyze the backup sizes using SQL window functions, and output a paginated report of anomalies.

Here are the specific requirements:

1. **Reverse Engineer & Normalize the Data Model**
   Read the raw log file located at `/home/user/raw_backups.jsonl`. Every line is a JSON object, but the schema varies. You must extract the following normalized fields for each log entry:
   - `database_name`: found under either the `database` or `db` key.
   - `status`: found under either `status` or `state`. Normalize any value of `"ok"` to `"success"`.
   - `size_bytes`: found either directly as `size` or nested under `metrics.bytes`.
   - `timestamp`: found under either `ts` or `time`.

2. **Load Data into SQLite**
   Store the normalized records into a SQLite database at `/home/user/backups.db` in a table named `backup_runs`.

3. **Analytical Aggregation (Window Functions)**
   Using SQLite's SQL capabilities, calculate a moving average to find "anomalous" backups. 
   An anomalous backup is defined as:
   - Having a `status` of `"success"`.
   - Its `size_bytes` is strictly greater than `1.2` times the rolling average of the `size_bytes` of the **previous 3 successful backups** (excluding the current one) for that exact same `database_name`. 
   - Note: If there are fewer than 3 previous successful backups for a database, calculate the average using however many previous successful backups are available (1 or 2). If there are 0 previous successful backups, it cannot be considered an anomaly (rolling average is null/undefined).

4. **Result Sorting, Filtering, and Pagination**
   Filter the results to only include these anomalous backups.
   Sort the anomalies globally by `timestamp` strictly in **DESCENDING** order.
   Output a paginated JSON report to `/home/user/anomalies.json` representing **Page 1** of the results, where the **page size is 2**.

The final `/home/user/anomalies.json` must exactly match this format:
```json
{
  "page": 1,
  "page_size": 2,
  "total_anomalies": <total_number_of_anomalies_found_across_all_pages>,
  "data": [
    {
      "database_name": "...",
      "timestamp": "...",
      "size_bytes": 12345,
      "rolling_avg": 10287.5
    },
    ...
  ]
}
```
*Round the `rolling_avg` to exactly 1 decimal place in the output JSON.*

You have full freedom to use standard Python 3 libraries or install packages like `pandas` if desired, though the built-in `sqlite3` and `json` modules are sufficient.