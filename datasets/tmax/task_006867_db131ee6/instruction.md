You are an automation specialist managing a telemetry data pipeline. We receive sensor logs from our international branches. Unfortunately, the data extraction tools export these logs in different character encodings, and network retries often cause duplicate entries.

Your task is to build a Python-based workflow that cleans this data and detects a sudden anomaly (changepoint) in the sensor metrics.

The raw log files are located in `/home/user/logs/` (you will find them there):
1. `en_log.csv` - English logs, encoded in `UTF-8`
2. `jp_log.csv` - Japanese logs, encoded in `UTF-16LE`
3. `de_log.csv` - German logs, encoded in `ISO-8859-1`

Each CSV file has the following format (no header row):
`timestamp,metric_value,message`
(e.g., `2023-10-01T10:00:00Z,20.0,System OK`)

Write and execute a Python script to perform the following pipeline:

**Step 1: Data Ingestion and Decoding**
Read all three CSV files using their correct encodings. Convert all text to standard Python Unicode strings. 

**Step 2: Hash-based Deduplication**
Due to system quirks, duplicate messages exist. A row is considered a duplicate if the SHA-256 hash of the concatenated string `{timestamp}{message}` (no spaces or delimiters added between them) has already been seen in the dataset. 
Filter out any duplicates, keeping only the first occurrence you encounter while processing the files (order of files doesn't strictly matter for the first occurrence if they are identical, but process EN, then JP, then DE).

**Step 3: Sorting**
Sort the combined, deduplicated dataset chronologically by `timestamp` in ascending order.

**Step 4: Changepoint/Anomaly Detection**
We need to detect a sudden spike in the `metric_value`.
Calculate a trailing 3-record moving average for the metric (i.e., the average of the current record and the previous two records). If there are fewer than 3 records available (e.g., the first or second record), calculate the average using only the available records.
An "anomaly" is triggered at the *first* timestamp where this 3-record moving average strictly exceeds `50.0`.

**Step 5: Reporting**
Output your findings to `/home/user/anomaly_report.json` with exactly this JSON structure:
```json
{
  "total_unique_records": <integer>,
  "anomaly_timestamp": "<string>",
  "anomaly_moving_avg": <float, rounded to 2 decimal places>
}
```

Constraints:
- You must write the solution in Python.
- Store your final output in `/home/user/anomaly_report.json`.