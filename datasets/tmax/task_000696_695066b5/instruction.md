You are a log analyst investigating user behavior patterns. You have been given a raw JSON-lines log file located at `/home/user/raw_logs.jsonl`. 

However, the logging system had a bug, and some lines contain malformed JSON (specifically, broken unicode escape sequences that cause standard JSON parsers to fail). 

Your task is to process this file using standard Linux command-line tools (Bash, awk, sed, jq, etc.) to produce an aggregated summary and a database import script.

Here are the specific requirements:

1. **Clean and Validate**: Read `/home/user/raw_logs.jsonl` and filter out any lines that are not valid JSON. 
2. **Extract and Reshape**: For every valid JSON line, extract the `timestamp`, `user`, and `action` fields. Truncate the `timestamp` to the hour level (i.e., keep only the `YYYY-MM-DDTHH` part).
3. **Aggregate**: Calculate the total count of each unique combination of `(hour, user, action)`.
4. **CSV Output**: Save the aggregated results to `/home/user/summary.csv`.
   - The CSV must have a header: `hour,user,action,count`
   - The rows must be sorted chronologically by `hour` (ascending), then alphabetically by `user`, and finally by `action`.
   - All fields should be comma-separated.
5. **SQL Template Generation**: Generate a database import script at `/home/user/insert.sql`.
   - For every row in your aggregated summary (excluding the header), generate exactly one SQL INSERT statement.
   - The format must be exactly: `INSERT INTO hourly_stats (hour, username, action, event_count) VALUES ('<hour>', '<user>', '<action>', <count>);`
   - Order the INSERT statements in the same sorted order as the CSV.

Ensure that the final output files `/home/user/summary.csv` and `/home/user/insert.sql` have the exact correct formats, as they will be automatically verified.