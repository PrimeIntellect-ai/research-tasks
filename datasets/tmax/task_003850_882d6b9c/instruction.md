You are acting as a log analyst investigating error patterns in a system. Previous team members tried analyzing the log files using standard shell tools (like `grep` and `wc`), but their counts were completely wrong because the log messages frequently contain embedded newline characters, which break naive line-by-line processing.

Your task is to write a Python script at `/home/user/analyze_logs.py` that processes the log file `/home/user/system_logs.csv` and computes rolling statistics on error rates. Since the actual production log files are extremely large, your script must process the file in a streaming fashion (e.g., using Python's `csv` module or chunking) rather than loading the entire file into memory at once.

The input CSV file has the following columns: `timestamp,level,component,message`.
The `timestamp` is in ISO 8601 format (e.g., `2023-10-01T10:03:15Z`).
The `level` can be `INFO`, `WARNING`, or `ERROR`.
The `message` often contains multi-line text enclosed in quotes.

Your Python script must perform the following operations:
1. Parse the CSV file correctly, respecting embedded newlines in the `message` field.
2. Group the logs into 5-minute time buckets based on the `timestamp` (e.g., `2023-10-01T10:00:00Z` to `2023-10-01T10:04:59Z` belongs to the `2023-10-01T10:00:00Z` bucket).
3. Count the number of `ERROR` level logs in each 5-minute bucket.
4. Ensure continuous time buckets: Your output must include every 5-minute interval between the earliest and latest timestamp found in the file. If a 5-minute interval has no logs at all, its `error_count` is 0.
5. Compute a 3-bucket Simple Moving Average (SMA) of the `error_count`. For a given bucket $T$, the SMA is the average of the error counts for $T-2$, $T-1$, and $T$. For the first bucket, the SMA is just its own error count. For the second bucket, it is the average of the first two buckets.
6. Write the results to `/home/user/error_trends.csv` with the following headers: `bucket_start,error_count,sma_3`.

Requirements for `/home/user/error_trends.csv`:
- `bucket_start` must be formatted as an ISO 8601 string ending with 'Z' (e.g., `2023-10-01T10:00:00Z`).
- `error_count` must be an integer.
- `sma_3` must be formatted as a float with exactly two decimal places (e.g., `2.00`, `1.33`).
- The rows must be sorted chronologically by `bucket_start`.

Once you have written the script, execute it to generate the `error_trends.csv` file.