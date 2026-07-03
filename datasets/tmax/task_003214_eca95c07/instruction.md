You are a log analyst investigating performance patterns across multiple servers. 

You have been given a dataset `/home/user/server_logs.csv` containing performance metrics. The file has the following columns: `timestamp`, `server_id`, `cpu_usage`, and `log_message`.

However, the current pipeline is dropping or mangling records. This is because some `log_message` fields are enclosed in double quotes and contain embedded newline characters. Furthermore, some `cpu_usage` values are missing (represented by empty strings) due to transient monitoring failures.

Your task is to write a Python script `/home/user/analyze.py` that does the following:
1. Accurately parses `/home/user/server_logs.csv` without dropping rows containing embedded newlines in the `log_message` field.
2. Groups the records by `server_id`.
3. Processes each `server_id`'s data in parallel using Python's `multiprocessing` module.
4. For each `server_id`, sorts the records by `timestamp` (ascending).
5. Imputes any missing `cpu_usage` values using forward-fill (carry forward the last known value). If the very first value for a server is missing, default it to `0.0`.
6. Calculates a rolling 3-period moving average of the imputed `cpu_usage` (the average of the current measurement and the up to 2 previous measurements). For the first measurement, the average is just that measurement. For the second, it is the average of the first and second.
7. Writes the results to `/home/user/rolling_metrics.csv` with the exact columns: `timestamp,server_id,rolling_cpu`. The `rolling_cpu` values must be rounded to exactly 2 decimal places (e.g., `13.33`). The output must be sorted by `timestamp` ascending, then `server_id` ascending.

Ensure your script runs successfully and produces the expected output.