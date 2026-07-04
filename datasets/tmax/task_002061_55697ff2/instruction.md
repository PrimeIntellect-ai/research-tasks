You are a data engineer tasked with building an ETL pipeline to process a raw, messy log file. A previous ETL job failed and retried, resulting in duplicate records. Your task is to clean, normalize, and analyze this time-series data to detect anomalous spikes in system errors.

The input file is located at `/home/user/raw_logs.csv`. It contains four columns: `id` (a unique transaction ID), `ts` (timestamp), `level` (log level: INFO, WARN, or ERROR), and `msg` (the raw log message).

Your pipeline must perform the following steps:

1. **Deduplication**: Due to ETL retries, there are duplicate rows with the same `id`. You must deduplicate the dataset based on `id`. If there are multiple records for the same `id`, keep only the record with the *earliest* timestamp.
2. **Standardization**: Timestamps in the `ts` column are mixed (some are unix epochs in seconds, some are ISO8601 strings). Convert all timestamps to standard UTC ISO8601 strings in the format `YYYY-MM-DDTHH:MM:SSZ`. 
3. **Normalization/Tokenization**: Normalize the `msg` field for the deduplicated records by:
   - Converting the entire message to lowercase.
   - Replacing any valid IPv4 address with the token `<IP>`.
   - Replacing any hexadecimal string (only characters 0-9 and a-f) that is exactly 6 characters or longer with the token `<HEX>`.
4. **Time-Series Anomaly Detection**: Group the deduplicated, standardized records by hour (e.g., `2023-10-01T10:00:00Z`). Count the number of `ERROR` level logs in each hour. 
   - An hour is considered an **anomaly** if its `ERROR` count is strictly greater than `2.0 * (average ERROR count of the immediately preceding 2 hours)`. 
   - Note: If an hour has no `ERROR` logs, its count is 0. If there are fewer than 2 preceding hours in the dataset (i.e., the first and second hours of the dataset), they cannot be considered anomalies.

Write a script in any language you prefer to process this data. Once processed, your script must output a summary to exactly `/home/user/etl_output.json` conforming to the following JSON structure:

```json
{
  "total_deduplicated": <integer, the total number of records after deduplication>,
  "anomalous_hours": [
    "<string, hour timestamp of anomaly 1, e.g., 2023-10-01T12:00:00Z>",
    "<string, hour timestamp of anomaly 2>"
  ]
}
```
The `anomalous_hours` array should be sorted chronologically. Do not leave temporary files outside of `/tmp`.