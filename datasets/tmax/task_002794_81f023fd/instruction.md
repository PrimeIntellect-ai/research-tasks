You are an analyst investigating a faulty ETL pipeline that occasionally produces duplicate event records upon retries. You need to process a mixed-language event log to compute deduplicated system performance metrics.

You are provided with an event log file at `/home/user/etl_events.jsonl`. Each line is a JSON object with the following keys:
- `ts`: A timestamp string. Note that these are emitted by distributed systems in various time zones and formats (e.g., `2023-10-25 10:00:00Z`, `2023-10-25 06:00:00-04:00`, `2023-10-25T19:02:00+09:00`).
- `lang`: A language code (e.g., "zh", "ja", "en").
- `val`: A float representing a metric (e.g., process time).
- `msg`: A text string containing the log message in the respective language.

Write a Python script to process this file according to the following requirements:

1. **Timestamp Alignment**: Convert all `ts` values to UTC. Format them strictly as `YYYY-MM-DDTHH:MM:SSZ`.
2. **Deduplication**: The ETL retry bug causes duplicate records. A record is considered a duplicate if it shares the **exact same UTC timestamp** and the **exact same `msg` string** as a record seen earlier in the file. Drop all subsequent duplicates (keep the first one).
3. **Filtering**: Keep only the records where the `msg` field contains the specific Unicode substring `"失敗"` (which means "failure" in Japanese/Chinese).
4. **Sorting**: Sort the remaining records chronologically by their UTC timestamp. If timestamps are identical, sort alphabetically by `msg`.
5. **Rolling Statistics**: For the filtered, sorted sequence, calculate a rolling average of the `val` field using a window of up to 3 records (the current record and up to 2 preceding records in the sequence).
6. **Output**: Write the results to `/home/user/rolling_stats.csv`. The CSV must have exactly the following headers: `utc_time,lang,msg,val,rolling_avg`. The `rolling_avg` must be rounded to exactly two decimal places (e.g., `10.00`, `12.50`).

Ensure your code handles Unicode properly and completes the execution. Do not use external libraries other than standard Python libraries and `pandas` if desired.