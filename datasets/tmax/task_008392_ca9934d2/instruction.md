I'm working on an ETL pipeline for our time-series event data, but the current Go script is failing. The input is a CSV file located at `/home/user/input/events.csv`. The fields are `timestamp` (RFC3339 format), `event_id`, `severity`, and `message`.

We have a buggy Go script at `/home/user/process.go` that attempts to read this file, but it has several problems:
1. The script uses a basic line-by-line scanner, which corrupts or drops rows where the `message` field contains embedded newlines.
2. The data contains duplicate events (same `event_id`).
3. We need to implement time-based bucketing and stratified sampling, which are currently missing.

Please fix or rewrite the Go script `/home/user/process.go` to perform the following:
1. **Robust CSV Parsing:** Correctly read the CSV, properly handling fields with quoted embedded newlines.
2. **Deduplication:** Ignore any event that has an `event_id` we have already seen. Keep the first occurrence.
3. **Time-Based Bucketing:** Truncate the `timestamp` of each event to the start of its 1-hour interval (e.g., `2023-10-10T10:15:00Z` becomes `2023-10-10T10:00:00Z`).
4. **Stratified Sampling:** For each 1-hour interval, keep exactly ONE event per `severity` level. If there are multiple events for the same severity in a 1-hour bucket, keep the one that occurred earliest (based on the original un-truncated timestamp).
5. **Output:** Write the results to `/home/user/output.jsonl` as JSON Lines. Each line must be a JSON object with the keys `interval` (the 1-hour truncated timestamp in RFC3339), `event_id`, `severity`, and `message`.
6. **Sorting:** Sort the final output JSON lines chronologically by `interval`. If multiple severities exist in the same interval, sort those lines alphabetically by `severity`.

You must execute your Go script and ensure `/home/user/output.jsonl` is created with the exact correct format. Let me know when you are done.