You are an AI assistant acting as a localization engineer. You are managing the rollout of a new translation system and analyzing rendering latency telemetry.

You have a large JSON-Lines file located at `/home/user/telemetry.jsonl`. This file contains telemetry events streamed from client devices. However, a bug in an older client version causes it to occasionally emit malformed unicode escape sequences (like `\uZZZZ` or cut-off sequences), which will cause standard JSON parsers to fail. 

Your task is to write a Go program at `/home/user/processor/process.go` that does the following:

1. **Initialization**: Initialize a Go module in `/home/user/processor`. You may use standard libraries and any SQLite driver you prefer (e.g., `github.com/mattn/go-sqlite3` or `modernc.org/sqlite`).
2. **Large-file streaming & Error Handling**: Stream the `/home/user/telemetry.jsonl` file line-by-line to avoid loading the entire file into memory. Gracefully catch and skip any lines that fail JSON unmarshaling (due to the malformed unicode bug or otherwise), keeping a count of skipped lines.
3. **Filtering & Rolling Statistics**: Process only the valid JSON lines where the `locale` field is exactly `"es-MX"`. For these lines, compute a rolling average of the `latency_ms` field over a sliding window of the last `5` valid `es-MX` records. 
   - *Note on rolling average*: If there are fewer than 5 records processed so far, the average should be calculated over the available records (e.g., the 1st record's rolling average is just its own latency, the 2nd is the average of the 1st and 2nd, etc.).
4. **Database Bulk Export**: Bulk insert the processed `es-MX` records into a SQLite database located at `/home/user/telemetry.db`. 
   - Use a single transaction to insert all processed records efficiently.
   - The table must be named `es_mx_stats` and have the following schema:
     `id` (TEXT PRIMARY KEY), `timestamp` (TEXT), `latency_ms` (REAL), `rolling_avg_latency` (REAL).

**JSONL Schema Expected:**
```json
{"id": "uuid-string", "timestamp": "2023-10-01T10:00:00Z", "locale": "en-US", "latency_ms": 45.2}
```

Write, build, and run your Go program. Ensure the SQLite database `/home/user/telemetry.db` is correctly populated with the final records.