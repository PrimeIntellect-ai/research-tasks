You are a localization engineer analyzing translation performance logs from a distributed ETL job. The ETL job pushes translation records to an external API and logs the result. Because the ETL job automatically retries on timeout, the logs often contain duplicate attempts for the same translation task.

Your goal is to parse these noisy logs, deduplicate the records, and compute a rolling average of translation latencies for the French locale (`fr-FR`).

The log file is located at `/home/user/etl_translation_logs.txt`.

Perform the following using Python:
1. Parse the file. Use Regular Expressions to extract the timestamp, Task ID, Target locale, and Latency from lines that match this general pattern (ignoring garbage/error lines):
   `[TIMESTAMP] | Task:[ID] | Target:[LOCALE] | Latency:[LATENCY]ms`
   Note that the timestamps come in two formats: ISO 8601 (`YYYY-MM-DDTHH:MM:SSZ`) and US format (`MM/DD/YYYY HH:MM:SS`). Both represent UTC times.
2. Deduplicate the records: If multiple log entries exist for the same Task ID, keep ONLY the entry with the most recent (latest) timestamp.
3. Filter for records where the Target locale is `fr-FR`.
4. Sort the remaining records chronologically by their timestamps.
5. Compute a 3-record rolling average of the latency. For each record, the rolling average is the mean latency of the current record and up to 2 previous records (i.e., window size of 3).
6. Save the output to `/home/user/fr_rolling_stats.csv`.

The output CSV must have exactly these headers: `TaskID,TimestampUTC,RollingAvgLatency`
The `TimestampUTC` must be formatted as `%Y-%m-%dT%H:%M:%SZ`.
The `RollingAvgLatency` must be rounded to exactly 2 decimal places.

Do not use external libraries like `pandas`; stick strictly to standard library modules (like `re`, `datetime`, `csv`, `collections`, etc.).