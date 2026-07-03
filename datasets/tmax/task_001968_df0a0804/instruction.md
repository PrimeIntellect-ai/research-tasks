You are a log analyst investigating intermittent performance degradation and error spikes in a web application. The raw application logs are noisy, irregularly spaced, and too large to analyze line-by-line. You need to build an automated data processing pipeline to aggregate these logs, handle missing data periods, extract a stratified sample of interesting time slices, and set up the scheduling configuration.

Your task is to implement this pipeline.

**Step 1: Data Processing Script**
Write a Python script at `/home/user/process_logs.py` that processes the raw logs located at `/home/user/data/raw_logs.csv`. The CSV has three columns: `timestamp` (ISO8601), `level` (INFO, WARN, ERROR), and `response_ms` (float).

The script must perform the following time-series operations using `pandas`:
1. Parse the `timestamp` column as datetime (UTC) and set it as the index.
2. **Resample** the data into 5-minute intervals (bins should be labeled by their left edge, and closed on the left). 
3. For each 5-minute interval, calculate:
   - `total_requests`: The total number of log lines in that interval.
   - `error_count`: The number of log lines where `level == 'ERROR'`.
   - `avg_response_ms`: The mean `response_ms` for that interval.
4. **Gap-filling**: Some 5-minute intervals might have no logs at all. 
   - Ensure the time series is continuous from the minimum timestamp to the maximum timestamp in the dataset (at 5-minute frequency).
   - Fill missing `total_requests` and `error_count` with `0`.
   - For `avg_response_ms`, forward-fill (ffill) the previous interval's average, but with a limit of 1 (only fill a gap of up to 5 minutes). For any remaining `NaN` values in `avg_response_ms`, fill them with `0.0`.
5. **Stratified Sampling**: To focus the investigation, select exactly 6 intervals:
   - *Group A (Error Spikes):* Find all intervals where `error_count > 0`. Select the top 3 intervals with the highest `error_count`. If there are ties, break them by picking the earliest timestamp first.
   - *Group B (High Traffic, No Errors):* Find all intervals where `error_count == 0`. Select the top 3 intervals with the highest `total_requests`. Break ties by picking the earliest timestamp first.
6. Combine Group A and Group B, sort them chronologically (by timestamp ascending), and reset the index so `timestamp` is a column. Convert the timestamp to an ISO8601 string format (e.g., `2024-01-01T00:00:00Z`).
7. Save the final 6 rows to `/home/user/investigation_sample.json` as a JSON array of objects (`orient="records"`).

**Step 2: Pipeline Wrapper & Scheduling**
1. Create a bash script at `/home/user/pipeline.sh` that executes your Python script. Ensure it has execute permissions.
2. We need to schedule this pipeline to run automatically at the top of every hour (e.g., 00:00, 01:00, 02:00, etc.). You do not need to install this into the system crontab, but you must write the exact cron expression and command to a file named `/home/user/cron.txt`. The file should contain exactly one line in the standard crontab format scheduling `/home/user/pipeline.sh`.

Ensure that executing `/home/user/pipeline.sh` manually will generate the required `/home/user/investigation_sample.json` file.