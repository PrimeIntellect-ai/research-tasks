You are a data engineer tasked with building an ETL pipeline to correlate error logs from two different web applications (AppA and AppB) that are located in different timezones and use different log formats.

Your objective is to write a Bash script `/home/user/run_etl.sh` that processes these logs, finds similar error messages occurring within a short time window, logs its execution, and is scheduled to run periodically.

Here are the requirements:

1. **Input Files:**
   - AppA logs are located at `/home/user/app_a.log`. 
     Format: `YYYY-MM-DD HH:MM:SS TZ_OFFSET | ERROR_MESSAGE`
     Example: `2023-10-25 09:30:00 -0400 | Connection reset by peer`
   - AppB logs are located at `/home/user/app_b.log`.
     Format: `DD/MMM/YYYY:HH:MM:SS TZ_OFFSET - ERROR_MESSAGE`
     Example: `25/Oct/2023:13:31:00 +0000 - Connection was reset by peer`

2. **Data Processing (The ETL Logic):**
   - Parse and align the timestamps from both files into Unix epoch time.
   - Compare every error in AppA with every error in AppB.
   - A pair of errors is considered "correlated" if:
     a) Their timestamps are within 300 seconds (5 minutes) of each other (inclusive).
     b) The text of the error messages has a similarity ratio of 0.70 or higher. Use Python's `difflib.SequenceMatcher(None, msgA, msgB).ratio()` to compute the similarity score.
   - Output the correlated pairs to `/home/user/correlated_errors.csv`.
   - The CSV format must be exactly: `epoch_time_A,epoch_time_B,similarity_score,appA_error_msg,appB_error_msg`
   - Round the `similarity_score` to 2 decimal places.

3. **Pipeline Logging:**
   - Your script must append an execution log to `/home/user/etl_pipeline.log`.
   - The log entry must be in the format: `[YYYY-MM-DD HH:MM:SS UTC] PIPELINE SUCCESS - Processed <N> correlated pairs` (where `<N>` is the number of pairs found).

4. **Scheduling:**
   - Add a cron job for the `user` that executes `/home/user/run_etl.sh` at the top of every hour (i.e., minute 0 of every hour). Ensure your script is executable.

Ensure your Bash script handles the orchestrations, though you may use inline Python within your Bash script for the timestamp parsing or difflib similarity calculation.