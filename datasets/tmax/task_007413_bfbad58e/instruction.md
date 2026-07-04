You are a log analyst investigating patterns across a distributed system. You have been given three different log files from various microservices, each using a different timestamp format and containing different fields. Your goal is to build a Go-based data pipeline that reads these logs, normalizes their timestamps, merges them into a chronologically sorted stream, groups the events by trace ID, and calculates summary statistics for each trace.

Input Data:
The logs are located in `/home/user/raw_logs/`:

1. `auth.log`: Format is `YYYY/MM/DD HH:MM:SS | trace_id | status`.
   Example: `2023/10/01 10:00:00 | T100 | SUCCESS`
   Note: The time is in UTC.

2. `db.log`: Format is `EpochSeconds | trace_id | query_time_ms`.
   Example: `1696154402 | T100 | 45`

3. `api.log`: Format is `RFC3339 | trace_id | endpoint | http_status_code`.
   Example: `2023-10-01T10:00:01Z | T100 | /users | 200`

Pipeline Requirements:
Write a Go program at `/home/user/process_logs.go` that:
1. Parses all three files concurrently (pipeline DAG).
2. Aligns all timestamps to a standard time format.
3. Merges the events and sorts them chronologically.
4. Groups the events by `trace_id`.
5. Computes the following summary statistics for each trace:
   - `trace_id`: The ID of the trace.
   - `duration_ms`: Total duration of the trace in milliseconds (Difference between the latest and earliest timestamp in the trace).
   - `max_db_query_ms`: The maximum `query_time_ms` across all `db.log` events for this trace (0 if no DB events).
   - `has_error`: Boolean. True if the trace has any `auth.log` event with status `FAIL`, or any `api.log` event with an `http_status_code` >= 400. Otherwise, false.

Output Requirements:
The Go program must output the results to a JSON file at `/home/user/trace_summary.json`. 
The JSON should be an array of objects, sorted alphabetically by `trace_id` ascending.
Example output format:
```json
[
  {
    "trace_id": "T100",
    "duration_ms": 3000,
    "max_db_query_ms": 45,
    "has_error": false
  }
]
```

Run your Go program to generate the required output file.