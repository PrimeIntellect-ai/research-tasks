You are a Data Scientist tasked with building an automated data cleaning and integration pipeline. 

We have two raw datasets that are generated daily:
1. `/home/user/reviews_raw.jsonl`: A JSON-lines file containing user reviews. Unfortunately, the system generating this file has a bug where Unicode escape sequences are double-escaped (e.g., `\\\\u2764` instead of `\\u2764` or actual characters), causing standard JSON parsers to output literal backslashes rather than the intended multi-language characters and emojis. Additionally, the `timestamp` field in this file is wildly inconsistent (e.g., `DD-MMM-YYYY HH:MM:SS`, `YYYY/MM/DD HH:MM:SS`, `DD-MM-YYYY HH:MM:SS`).
2. `/home/user/server_logs.csv`: A CSV file containing user activity logs. The timestamps here are stored in a column named `log_epoch` as Unix epoch seconds.

Your objective is to write and execute a Python script (`/home/user/pipeline.py`) that performs the following:
1. **Unicode & Regex:** Read the JSON-lines file and fix the double-escaped Unicode. You must decode these sequences into actual Unicode characters (e.g., the ❤️ emoji, accented letters like `ó`). 
2. **Timestamp Alignment:** Parse the inconsistent timestamps in the JSONL file and convert them to Unix epoch seconds (UTC). 
3. **Merge/Join:** Join the cleaned review data with the server logs. A review matches a server log if they have the same `user_id` AND the review's epoch timestamp is within exactly 300 seconds (5 minutes) of the `log_epoch` (inclusive). If a review matches multiple logs, pick the earliest `log_epoch`. Only include reviews that have a matching server log (Inner Join).
4. **Output Generation:** Write the joined data to `/home/user/merged_output.jsonl`. Each line must be a valid JSON object with EXACTLY these keys:
   - `user_id` (integer)
   - `review_timestamp_iso` (string, the review's timestamp in strict ISO 8601 UTC format: `YYYY-MM-DDTHH:MM:SSZ`)
   - `text_decoded` (string, the fully decoded unicode text)
   - `log_action` (string, the `action` value from the matching server log)

Additionally, this pipeline needs to be automated. 
1. Create a bash wrapper script at `/home/user/run_pipeline.sh` that executes your Python script. Ensure it has execute permissions.
2. We need to schedule this to run every day at 2:30 AM. Since you don't have root access to install the actual crontab, simply write the exact cron expression and the absolute command to a file named `/home/user/crontab.txt`. The format must be standard cron syntax: `[minute] [hour] [day] [month] [weekday] [command]`.

Note: Assume all input timestamps are in UTC. You may use standard Python libraries, as well as `pandas` if desired.