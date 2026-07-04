You are a log analyst investigating patterns in a system's event logs. You have been provided with a JSON-lines log file at `/home/user/app_logs.jsonl`. 

The log file contains system events, but it has some issues that need to be handled carefully:
1. **Malformed JSON**: Some lines contain invalid JSON (such as broken unicode escape sequences). Your script must catch `JSONDecodeError` (or equivalent) for these lines. Do not stop processing. Instead, write the exact raw malformed lines to a quarantine file at `/home/user/quarantine.jsonl`.
2. **Duplicate Events**: Due to retry mechanisms, some events were logged multiple times. Deduplicate the events based *only* on the `payload` field. If multiple events have the exact same `payload` object (same keys and values), keep only the first one you encounter and ignore the rest. `event_id`, `timestamp`, and `response_time` should be ignored for the purpose of deduplication.
3. **Mixed Timestamps**: The `timestamp` field can be either an ISO8601 string (e.g., `"2023-10-01T10:15:00Z"`) or a UNIX epoch integer (e.g., `1696157100`). All times should be interpreted as UTC.

Your objective is to write a Python script that processes this file to produce hourly aggregations:
- Bucket the valid, deduplicated events by hour (based on their UTC timestamp).
- For each hour, calculate the total number of events (`event_count`) and the average response time (`avg_response_time`) from the `response_time` field.
- Round the `avg_response_time` to exactly 2 decimal places.
- Write the aggregated results to a CSV file at `/home/user/hourly_stats.csv`.

The output CSV must have the following exact headers and format:
```csv
hour,event_count,avg_response_time
2023-10-01T10:00:00Z,2,150.00
```
Sort the rows in the CSV by the `hour` column in ascending order. 

Ensure that your solution is robust, processes the data efficiently, and correctly outputs the two required files: `/home/user/quarantine.jsonl` and `/home/user/hourly_stats.csv`.