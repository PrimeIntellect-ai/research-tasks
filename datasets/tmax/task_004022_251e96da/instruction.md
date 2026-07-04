You are a log analyst investigating server performance patterns. I have a raw, messy log file located at `/home/user/raw_logs.txt`. It contains unstructured text describing server access, but it's riddled with duplicates, malformed lines, and missing server load metrics.

Your task is to write and execute a Go program (`/home/user/process_logs.go`) that performs the following steps:

1. **Extraction**: Parse the log lines to extract the Timestamp, Endpoint, Response Time (in ms), and Server Load. 
   Valid log lines look like this:
   `[2023-10-01T10:00:00Z] INFO - User accessed /api/v1/data | response_ms=45 load=0.55`
   Ignore any lines that do not match this basic structure or don't contain a `response_ms` value.

2. **Cleaning & Deduplication**: 
   - Remove exact duplicate log entries (where Timestamp, Endpoint, Response Time, and Load are identical).
   - Sort the remaining entries chronologically by Timestamp.

3. **Imputation**: 
   Some valid log lines are missing the `load` value (e.g., `load= ` or the field is empty). You must impute these missing values using simple averaging of the chronologically nearest preceding and succeeding valid load values. 
   - If a load is missing, calculate it as: `(closest_previous_valid_load + closest_next_valid_load) / 2.0`. 
   - Assume the first and last valid log entries will always have a valid load value.
   - Format imputed load values to exactly 2 decimal places.

4. **Export**: 
   Save the final processed data to `/home/user/clean_metrics.csv` as a CSV file with the following exact headers:
   `Timestamp,Endpoint,ResponseTimeMs,ServerLoad`

Write the Go script, compile/run it, and ensure the resulting `/home/user/clean_metrics.csv` is correctly formatted.