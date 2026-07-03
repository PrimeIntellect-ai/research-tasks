You are a log analyst investigating user activity patterns. 

You have been given two datasets:
1. `/home/user/logs/server_events.jsonl`: A JSON-lines log file containing raw server events. However, the system that generated these logs had a bug, and some lines contain malformed unicode escape sequences (e.g., `\u00ZZ`) that will break standard JSON parsers.
2. `/home/user/data/user_metadata.csv`: A CSV file mapping `user_id` to their respective geographical `region`.

Your task is to build a robust data processing pipeline that does the following:

1. **Clean and Validate (Constraint-based validation):** Read `server_events.jsonl`. Safely ignore or drop any line that is not valid JSON (due to the unicode bug or otherwise). Furthermore, drop any parsed JSON object that does not contain both a `user_id` (integer) and an `event_type` (string).
2. **Join and Aggregate:** Join the valid event records with the `user_metadata.csv` file using `user_id`. Calculate summary statistics: the count of each `event_type` grouped by `region`. 
3. **Format Output:** Save the aggregated statistics to exactly `/home/user/summary_report.json`. The output must be a standard JSON object where the top-level keys are regions, and the values are objects mapping `event_type` to the total count (e.g., `{"NA": {"login": 5, "click": 2}, "EU": {"login": 3}}`).
4. **Orchestrate and Schedule:** Wrap your processing logic into a single executable shell script at `/home/user/run_pipeline.sh`. Then, schedule this script to run at the top of every hour (minute 0) using the current user's `crontab`.

Ensure your output JSON strictly matches the requested schema and that the cron job is correctly installed.