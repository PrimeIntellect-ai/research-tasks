You are acting as a log analyst investigating a recent series of microservice outages. We have captured raw binary telemetry logs, but our standard pipeline is down.

Your task is to write a Python script at `/home/user/analyze.py` to process the logs, aggregate the metrics, and identify anomalies using an opaque legacy scoring engine.

**1. Data Processing**
A raw log file is located at `/app/server_logs.csv` (schema: `timestamp,service_id,latency_ms,status_code`).
Write a Python script that reads this file and creates time-based buckets of exactly 5 minutes (300 seconds), starting from the very first timestamp in the file.
For each 5-minute bucket, compute the following summary statistics:
- `request_count`: Total number of log entries in the bucket.
- `p95_latency`: The 95th percentile of `latency_ms`.
- `error_rate`: The proportion of logs with `status_code >= 500`.

**2. Anomaly Scoring**
We have a stripped legacy binary located at `/app/anomaly_scorer` that evaluates aggregated metrics. 
You must pass your bucketed statistics to this binary to get an anomaly score.
The binary accepts CSV-formatted data via standard input with no header. The columns must be exactly:
`request_count,p95_latency,error_rate` (all formatted to 4 decimal places where applicable, except `request_count` which is an integer).
The binary will output a single floating-point anomaly score per line to standard output.

**3. Validation and Output**
An anomaly is defined as any bucket where the score returned by the binary is strictly greater than `0.8500`.
Generate a final CSV report at `/home/user/anomalies.csv` with the following header:
`bucket_start_timestamp,request_count,p95_latency,error_rate,anomaly_score`
Include only the anomalous buckets, sorted chronologically.

Ensure your script runs efficiently and handles missing buckets implicitly (if a 5-minute window has no logs, skip it). Do not use external libraries other than `pandas` or `numpy` (which you can install if needed).