You are an assistant helping a data scientist clean and analyze an IoT telemetry dataset. 

You have been provided with a dataset at `/home/user/data/telemetry.jsonl`. Each line is a JSON object representing a sensor reading, for example:
`{"ts": "2023-10-01T10:15:30Z", "device": "sensor_A", "val": 22.5}`

Your task is to write a Python script that processes this data and identifies anomalies. You may use `pandas` (which is installed). Perform the following transformations:

1. **Time-based bucketing**: Parse the `ts` column as a datetime and "floor" or round it down to the nearest hour (e.g., `2023-10-01T10:15:30Z` becomes `2023-10-01T10:00:00Z`).
2. **Aggregation**: For each `device` and hourly bucket, calculate the mean of the `val` readings. Let's call this `mean_val`.
3. **Windowed feature extraction**: Sort the data chronologically by the hourly bucket. For each `device`, calculate a rolling average of `mean_val` over a window of 3 hours (current hour and the previous 2 available hourly buckets for that device). Use a minimum period of 1. Let's call this `rolling_avg`.
4. **Anomaly detection**: An anomaly is defined as any hourly bucket where the absolute difference between `mean_val` and `rolling_avg` is strictly greater than 5.0.
5. **Multi-format writing**: Extract only the anomalous rows. Save these rows to a Parquet file at `/home/user/anomalies.parquet`. The output must contain exactly these columns: `device` (string), `hour` (datetime), `mean_val` (float), and `rolling_avg` (float). 

Ensure your script runs successfully and produces the file at `/home/user/anomalies.parquet`.