You are an data engineer tasked with building a resilient ETL pipeline for processing telemetry logs. 

You have been provided with a file at `/home/user/telemetry.jsonl`. Each line in this file is intended to be a JSON object containing application events, specifically featuring a `raw_log` string field. 

However, there are a few issues with the file:
1. Some lines contain malformed unicode escape sequences (e.g., `\u004` instead of a valid 4-hex-digit sequence) in metadata fields, which will cause standard JSON parsers like Python's `json.loads()` to crash.
2. The `raw_log` field contains unstructured text that looks like: `"[SYSTEM] latency=45ms timestamp=2023-11-01T10:00:00Z status=OK"`.

Your task is to write a Python script that processes this file and outputs a clean dataset with rolling aggregations, adhering to the following rules:

1. **Extraction**: Extract the `latency` (as an integer, excluding the "ms") and the `timestamp` from the `raw_log` field for every line. If a line cannot be parsed by a standard JSON parser due to malformed unicode, you must bypass the standard parser and extract the `latency` and `timestamp` using string manipulation or regular expressions directly on the line. Every line contains exactly one `latency=...ms` and `timestamp=...` pattern.
2. **Validation**: Filter the extracted records to include only those where `latency` is strictly greater than 0 and less than or equal to 5000. Discard any records that fail this constraint.
3. **Time Series Aggregation**: Sort the valid records chronologically by `timestamp`. Then, calculate a 3-event rolling average of the `latency`. (The rolling window should consider the current event and up to two previous valid events).
4. **Output**: Write the results to a CSV file at `/home/user/rolling_latency.csv`. The CSV must have exactly three columns with headers: `timestamp,latency,rolling_avg`. The `rolling_avg` must be rounded to exactly 2 decimal places (e.g., `100.00`, `33.33`).

Do not skip lines just because their JSON is broken; extract the data from them anyway.