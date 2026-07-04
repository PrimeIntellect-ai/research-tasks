You are a log analyst for a global web platform. You have been tasked with investigating unusual traffic patterns from a dirty server access log file. The raw data contains multi-lingual search queries, irregular and missing timestamps, sensitive IP addresses, and user-agent strings.

Your objective is to write a Python script that cleans, transforms, and summarizes this data, and then set up a scheduled pipeline for it.

Here are your instructions:

1. **Input Data**: Read the file at `/home/user/raw_logs.jsonl`. Each line is a JSON object with keys: `time` (ISO 8601 string or null), `ip`, `query`, and `ua`.

2. **Data Cleaning & Transformation**:
    *   **Gap-filling**: Some `time` fields are `null`. Sort the logs sequentially as they appear in the file, and forward-fill any missing timestamps (use the most recent valid timestamp). Treat all times as UTC.
    *   **Data Masking**: Anonymize the IPv4 addresses in the `ip` field by replacing the last octet with `0` (e.g., `192.168.1.55` becomes `192.168.1.0`).
    *   **Unicode Processing**: The `query` field contains multi-language text with inconsistent encodings. Normalize the `query` text to **NFKC** form.
    *   **Feature Extraction**: 
        *   Calculate `query_length`: the integer number of characters in the normalized query.
        *   Determine `is_bot`: an integer `1` if the `ua` (user-agent) string contains the substring `"bot"` (case-insensitive), otherwise `0`.

3. **Resampling & Aggregation**:
    *   Resample the timeseries into exactly **1-hour** intervals, aligned to the top of the hour (e.g., `2023-10-01 10:00:00`), starting from the hour of the very first log entry to the hour of the very last log entry.
    *   For each 1-hour bin, calculate:
        *   `total_requests`: The total number of log entries in that hour.
        *   `bot_requests`: The sum of `is_bot` for that hour.
        *   `avg_query_length`: The mean of `query_length` for that hour (round to 2 decimal places).
    *   **Crucial**: If an hour has no logs (a gap in the timeseries), you must fill it. Set `total_requests=0`, `bot_requests=0`, and `avg_query_length=0.0`.

4. **Output Format**:
    *   Save the aggregated data to a CSV file at `/home/user/hourly_summary.csv`.
    *   The CSV must have a header row with exactly these columns: `hour,total_requests,bot_requests,avg_query_length`.
    *   Format the `hour` column as `YYYY-MM-DD HH:00:00`.

5. **Pipeline Scheduling**:
    *   Write a bash wrapper script at `/home/user/pipeline.sh` that executes your Python script. Ensure it is executable.
    *   Create a crontab file at `/home/user/my_cron` containing a single line that schedules `/home/user/pipeline.sh` to run at the **0th minute of every hour** (hourly).

Do not install any external Python packages other than `pandas` (if you choose to use it, it is already available in most environments, but you can `pip install pandas` if needed). Standard library tools are also completely fine.