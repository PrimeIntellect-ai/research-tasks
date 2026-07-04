You are a log analyst investigating a coordinated pattern of failures across our distributed infrastructure. We suspect that certain time windows experience highly correlated errors across our Web, API, and Database tiers. 

You need to analyze three distinct, large log files. Each uses a different format and timestamp standard. 

The logs are located in `/home/user/logs/`:
1. `web_server.log` (CSV): `timestamp,ip,status_code,response_time` 
   - Timestamp is in ISO 8601 format (e.g., `2023-10-25T14:30:00Z`).
   - A failure is defined as `status_code >= 500`.
2. `api_gateway.jsonl` (JSON Lines): `{"ts": <epoch_milliseconds>, "client": "<ip>", "endpoint": "<path>", "error": <boolean>}`
   - Timestamp is Unix epoch in *milliseconds*.
   - A failure is defined as `"error": true`.
3. `db_query.log` (Plain text): `[YYYY-MM-DD HH:MM:SS] user=<user> duration_ms=<ms> status=<OK|ERROR>`
   - Timestamp is enclosed in brackets, in UTC.
   - A failure is defined as `status=ERROR`.

**Your objective:**
1. Parse and align the timestamps from all three files into a unified UTC timeline (Unix epoch seconds).
2. Filter the records to only include "failures" as defined above.
3. Group the combined failures into fixed (tumbling) 60-second windows. A window starting at epoch second `T` (where `T` is a multiple of 60) covers the interval `[T, T+60)`.
4. Calculate the total number of failures across all three systems for each 60-second window.
5. Identify the top 10 windows with the highest total combined failures. If there is a tie in the number of failures, sort those tied windows by their timestamp in ascending order.
6. Write the results to `/home/user/top_failure_windows.csv` with exactly two columns: `window_start_epoch,total_failures`. Include a header row.

*Note: The log files are generated dynamically upon your environment's startup. You should write a Python script to process the data efficiently, as loading everything into memory inefficiently might slow you down.*