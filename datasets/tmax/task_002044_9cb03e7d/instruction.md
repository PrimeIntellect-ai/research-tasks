You are a localization engineer managing a platform that logs user access to translated strings over time. The platform generates time-series logs in JSON-Lines format. Recently, a bug in the logging system caused Unicode characters in the `text` field to be double-escaped or inconsistently escaped (e.g., `\u00e9` instead of `é`). 

Additionally, due to retry mechanisms in the logging API, there are exact duplicate events in the logs.

Your task is to write a Python pipeline script at `/home/user/process_loc.py` to clean, deduplicate, and aggregate these time-series logs.

**Input Data:**
The raw logs are located in `/home/user/loc_logs/`. There are multiple `.jsonl` files.
Each line is a JSON object with the following schema:
`{"timestamp": "YYYY-MM-DDTHH:MM:SSZ", "loc_key": "string", "text": "string", "user_id": int}`

**Requirements for `/home/user/process_loc.py`:**
1. **Unicode Fixing:** Extract the `text` field and correctly unescape any Unicode escape sequences so that strings like `"M\\u00e9xico"` become `"México"`. 
2. **Hash-based Deduplication:** Generate an MD5 hash of the concatenated string: `<timestamp>|<loc_key>|<unescaped_text>`. Keep only the first occurrence of each hash.
3. **Time-Series Grouping:** Extract the "hour" from the timestamp (e.g., `"2023-10-01T14:30:00Z"` becomes `"2023-10-01T14"`).
4. **Aggregation:** Count the number of *unique* log events (after deduplication) per hour.
5. **Output:** Write the aggregated results to a CSV file at `/home/user/loc_aggregated.csv`. 
   - The CSV must have headers: `hour,unique_events`
   - The rows must be sorted chronologically by `hour`.
6. **Logging:** The script must write operational logs to `/home/user/pipeline.log`. It must append the following exact messages (one per line) during execution:
   - `PIPELINE_START`
   - `TOTAL_LINES: <N>` (where N is the total number of lines read across all files)
   - `DUPLICATES_REMOVED: <M>` (where M is the number of duplicates filtered out)
   - `PIPELINE_COMPLETE`

Run your script to produce `/home/user/loc_aggregated.csv` and `/home/user/pipeline.log`.