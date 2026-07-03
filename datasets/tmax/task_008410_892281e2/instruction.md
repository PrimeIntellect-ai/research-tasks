You are helping a researcher organize their dataset. They have an SQLite database containing environmental sensor readings located at `/home/user/sensor_data.db`.

The database has a single table:
`readings(id INTEGER PRIMARY KEY, station_id TEXT, timestamp TEXT, payload TEXT)`

The `payload` column contains JSON strings with metric data, for example: `{"temperature": 22.4, "humidity": 45}`. 

The researcher has noticed two issues:
1. Some rows have corrupted payloads (either invalid JSON or containing JSON with `null` values for the metrics).
2. There is a corrupted index on the `timestamp` column. Standard queries using `ORDER BY timestamp` or filtering by `timestamp` sometimes return stale or missing rows because SQLite attempts to use this bad index.

Your task is to write and execute a Python script at `/home/user/process_data.py` that does the following:
1. Connects to `/home/user/sensor_data.db`.
2. Queries the data for `station_id = 'ST-01'` while completely bypassing the corrupted `timestamp` index (you must either force a full table scan, use the `NOT INDEXED` clause, or drop the corrupted index before querying).
3. Parses the JSON `payload`. You must ignore any row where the payload is invalid JSON or where either `temperature` or `humidity` is `null`.
4. Aggregates the data to calculate the maximum temperature and the average humidity per day (extract the date `YYYY-MM-DD` from the `timestamp` which is formatted as `YYYY-MM-DD HH:MM:SS`).
5. Exports the aggregated results to `/home/user/daily_summary.json`

The output file `/home/user/daily_summary.json` must exactly match this JSON array schema:
```json
[
  {
    "date": "YYYY-MM-DD",
    "max_temperature": 25.4,
    "avg_humidity": 42.15
  }
]
```
Note: Round `avg_humidity` to exactly 2 decimal places. Sort the JSON array chronologically by `date`.