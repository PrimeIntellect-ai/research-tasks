You are a log analyst investigating access patterns for a web server. 

You have been given a raw log file located at `/home/user/raw_logs.log`. This file contains web server access logs, but it has a few issues:
1. It contains mixed character encodings. Some lines contain invalid UTF-8 bytes that need to be replaced with the standard Unicode replacement character (U+FFFD) or ignored/stripped so the text can be processed as UTF-8.
2. The request paths contain varying numeric IDs, which makes aggregation difficult.
3. The logs are sparse. Some minutes have no traffic, but our downstream monitoring tools require a continuous time-series (gap-filling).

Your task is to write a script (in any language you choose) and execute it to process this log file and produce a continuous summary. 

Here are the requirements for your data processing pipeline:

1. **Clean & Decode**: Read `/home/user/raw_logs.log`, handling any invalid UTF-8 bytes gracefully.
2. **Tokenize & Normalize**: 
   - Extract the timestamp (down to the minute, ignoring seconds) and the request path. The log format is `[YYYY-MM-DD HH:MM:SS] IP METHOD PATH STATUS`.
   - Normalize the request path by converting it to lowercase and replacing any sequence of 1 or more digits with the literal string `[NUM]`. For example, `/api/v1/users/402/profile` becomes `/api/v[NUM]/users/[NUM]/profile`.
3. **Filter**: Only process logs for the specific 10-minute window from `2023-10-24 10:00:00` to `2023-10-24 10:09:59` inclusive.
4. **Resample & Aggregate**: 
   - Calculate the total number of requests per minute for each normalized path.
   - **Gap-filling**: For *every* normalized path that appears at least once in the entire 10-minute window, your final output must have exactly one row for *every* minute in that 10-minute window (from `10:00` to `10:09`). If there were no requests for a path in a specific minute, output a count of `0`.
5. **Output**: Save the aggregated results to `/home/user/summary.csv`. The CSV must have a header `time,path,count`. The `time` should be in `YYYY-MM-DD HH:MM` format. Sort the CSV chronologically by time, and then alphabetically by path.
6. **Scheduling**: We want to automate this in the future. Create a file at `/home/user/cron_schedule.txt` containing exactly one crontab line that would schedule a bash script `/home/user/run_pipeline.sh` to run every 5 minutes.

Ensure `/home/user/summary.csv` and `/home/user/cron_schedule.txt` are perfectly formatted as described.