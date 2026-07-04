You are a data analyst dealing with a large batch of time series user activity logs.

In the directory `/app/data/`, there are 50 large CSV files named `activity_log_00.csv` to `activity_log_49.csv`. Each file contains the following columns:
- `timestamp`: An ISO 8601 formatted timestamp (e.g., `2023-10-01T14:32:11Z`)
- `user_id`: A string representing the user's email address
- `event_type`: A string representing the event category
- `duration_ms`: A float representing the duration of the event in milliseconds

We have a strict compliance requirement to anonymize all user IDs. A proprietary, stripped binary is provided at `/app/anonymizer`. This executable reads newline-separated plain-text `user_id` strings from standard input and prints the corresponding anonymized strings to standard output. Note that this binary introduces a slight artificial delay per invocation, so processing IDs one-by-one in a serial loop will be far too slow.

Your task is to create a highly optimized data processing pipeline that performs the following steps:
1. Stream through all the CSV files in `/app/data/`.
2. Filter the rows to keep only those where `event_type` is either `'video_stream'` or `'audio_stream'`.
3. Anonymize the `user_id` for the filtered rows using the `/app/anonymizer` binary.
4. Aggregate the data to compute summary statistics: calculate the sum of `duration_ms` for each anonymized `user_id`, aggregated by calendar day (extracted from the `timestamp` in `YYYY-MM-DD` format).
5. Save the aggregated results to `/home/user/daily_usage.parquet`. The Parquet file must have exactly three columns: `date` (string), `anon_user_id` (string), and `total_duration_ms` (float).

Write your full end-to-end processing pipeline in a single script located at `/home/user/run_pipeline.sh` (which can be a bash script that triggers Python, a standalone Python script with a shebang, or any other language of your choice). 

We will execute `/home/user/run_pipeline.sh` and evaluate it based on correct output and performance. Your implementation must be efficient. You should leverage batching, multi-format I/O, and parallel processing to ensure the script runs quickly.