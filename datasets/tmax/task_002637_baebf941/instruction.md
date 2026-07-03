You are a log analyst investigating anomalous traffic patterns. We have a proprietary high-performance log collection service provided as a compiled binary at `/app/log_emitter`. When executed, this binary streams a day's worth of simulated traffic logs to standard output in JSON-Lines (JSONL) format.

However, the upstream collector had a bug: it occasionally inserted invalid unicode escape sequences (e.g., `\uZZZZ` or truncated escapes) into the `user_agent` field. Standard JSON parsers will break when reading this stream.

Your task is to write a Python pipeline script at `/home/user/pipeline.py` that executes `/app/log_emitter`, captures its stdout, and performs the following data processing steps:

1. **Validation & Cleaning**: Parse the JSONL stream. You must gracefully clean or bypass the invalid unicode escape sequences so the records can be parsed successfully. Dropping the corrupted lines entirely is NOT allowed; you must salvage the JSON (e.g., by stripping or fixing the invalid escapes).
2. **Data Masking**: Anonymize the `client_ip` field in every log entry by replacing the final octet with a zero (e.g., `192.168.1.45` becomes `192.168.1.0`).
3. **Time-based Bucketing**: Group the parsed log entries into 60-second tumbling time buckets using the integer `timestamp` field.
4. **Reshaping & Aggregation**: For each 1-minute bucket, calculate:
   - The number of unique masked IP addresses.
   - The frequency of each `endpoint` accessed. The possible endpoints are `/login`, `/data`, and `/health`. Reshape this into three separate counts per bucket.
5. **Distance Computation**: For each bucket, compute the Euclidean distance between the bucket's endpoint frequency vector `[count_login, count_data, count_health]` and the baseline expected vector `[15, 45, 10]`.

Finally, your script must output a CSV file at `/home/user/anomalies.csv` with exactly the following columns (with header):
`bucket_start_timestamp,unique_ips,distance`

The `bucket_start_timestamp` should be the integer start time of the bucket. The `distance` should be rounded to 4 decimal places.

Ensure your pipeline processes the data efficiently. An automated verifier will evaluate the numeric accuracy of your computed Euclidean distances against a ground-truth reference implementation.