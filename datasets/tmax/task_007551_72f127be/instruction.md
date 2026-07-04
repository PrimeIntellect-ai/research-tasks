You are an ETL Data Engineer. We have a pipeline that processes server logs, but our current job periodically fails and retries, causing duplicate records in our downstream analytical tables. 

Your task is to write a robust Python ETL script that parses raw logs, calculates specific statistics, reshapes the data, ensures idempotency (no duplicates on retry), and is scheduled to run continuously.

Here are your requirements:

1. **Log Parsing**:
   Raw logs are continuously dropped into `/home/user/data/raw/`. 
   The files are plain text, and each line follows this exact format:
   `[YYYY-MM-DD HH:MM:SS] REQ:<request_id> USER:<user_id> TIME:<response_time_in_ms>ms`
   *Example:* `[2023-10-25 14:32:01] REQ:req_992 USER:usr_5 TIME:45ms`
   You must use Python and regular expressions to extract `timestamp`, `request_id`, `user_id`, and `response_time`.

2. **Data Transformation & Rolling Statistics**:
   Using `pandas`, process the extracted data:
   - Sort the data chronologically by `timestamp`.
   - Calculate a **rolling 3-request average** of `response_time` for each `user_id` (window size 3, min_periods 1). Name this metric `rolling_avg_time`.

3. **Reshaping (Wide-Long-Wide)**:
   To simulate our complex internal schema requirements:
   - First, melt/unpivot the DataFrame into a *long format* with columns: `request_id`, `user_id`, `timestamp`, `metric_name`, `value`. The `metric_name` should be either `response_time` or `rolling_avg_time`.
   - Next, pivot it back into a *wide format* with columns: `request_id`, `user_id`, `timestamp`, `response_time`, `rolling_avg_time`.

4. **Idempotency (Handling Retries/Duplicates)**:
   The script must append processed records to a Parquet file located at `/home/user/data/processed/master.parquet`. 
   However, if the script is run multiple times on the same raw files, it **must not** produce duplicate rows for the same `request_id` in the output Parquet file. Implement a deduplication or upsert strategy using `request_id` as the unique key. If `master.parquet` doesn't exist, create it.

5. **Scheduling**:
   Save your Python script as `/home/user/etl_pipeline.py`.
   Create a bash wrapper `/home/user/run_etl.sh` that executes the Python script. Make sure the wrapper is executable.
   Schedule this wrapper to run **every 5 minutes** using the current user's `cron`.

**Constraints & Notes**:
- Use Python 3 and standard data libraries (`pandas`, `pyarrow` or `fastparquet`). You can install dependencies using pip.
- Do not remove the raw files after processing; your script must handle idempotency natively.