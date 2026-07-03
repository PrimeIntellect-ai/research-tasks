You are a log analyst investigating a recent system anomaly. 

We have a raw application log file located at `/home/user/data/logs.jsonl`. This file contains JSON-lines formatted events, but there's a problem: a bug in the logging library occasionally produced malformed unicode escape sequences (e.g., `\u12G4` where `G` is invalid hex). Standard rigid parsers might crash when hitting these lines.

Your task is to build a robust data processing pipeline to clean, validate, and aggregate this data. You may use standard CLI tools (like `jq`, `awk`, `grep`, `bash`) or write a script in a language like Python. 

Here are the requirements for your pipeline:

1. **Clean/Filter Invalid Data**: Discard any lines that are not valid JSON (such as those containing the malformed unicode escapes).
2. **Constraint Validation**: From the valid JSON lines, filter the dataset to include ONLY events that meet BOTH of these criteria:
   - `event_type` is exactly `"api_call"`
   - `status_code` is an integer between `200` and `599` (inclusive).
3. **Time-based Bucketing**: Extract the hour from the `timestamp` field. The `timestamp` is in ISO 8601 format (e.g., `2023-11-01T08:15:30Z`). The hour bucket format should be `YYYY-MM-DDTHH` (e.g., `2023-11-01T08`).
4. **Aggregation**: For each hour bucket, calculate:
   - `total_events`: The total number of valid `api_call` events.
   - `error_count`: The number of those events that are errors (defined as `status_code >= 400`).
5. **Output**: Write the aggregated results to a CSV file at `/home/user/report.csv`. 

The CSV must:
- Have the exact header: `hour,total_events,error_count`
- Be sorted chronologically by the `hour` column.
- Be comma-separated.

You must complete this task and ensure `/home/user/report.csv` is correctly formatted and contains the accurate aggregated metrics.