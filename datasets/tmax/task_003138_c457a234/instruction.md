As a configuration manager, you need to monitor the frequency of configuration changes across your infrastructure to detect potential deployment storms. 

You have been provided with an audit log file at `/home/user/config_audit.log`. 

The log file contains entries in the following format:
`[YYYY-MM-DD HH:MM:SS] <Username> CONFIG_UPDATE: Changed parameter '<ParamName>' on server '<ServerName>'`

Your task is to write a Python script (you can name it `/home/user/process_audit.py` and run it) to process this log file and generate a time-series aggregation.

Specifically, you need to:
1. Extract the timestamps using a regular expression.
2. Group the configuration changes into hourly buckets (e.g., `2023-11-01 14:00:00`).
3. Fill in any missing hourly buckets between the earliest and latest timestamps in the log with a count of `0`.
4. Calculate a rolling 3-hour sum of the change counts (i.e., the sum of changes in the current hour and the previous 2 hours).
5. Save the output to `/home/user/hourly_rolling_stats.csv`.

The output CSV must have exactly these headers: `hour_bucket,change_count,rolling_3h_sum`.
The `hour_bucket` should be formatted as `YYYY-MM-DD HH:00:00`.

Example output format:
```csv
hour_bucket,change_count,rolling_3h_sum
2023-11-01 08:00:00,2,2
2023-11-01 09:00:00,1,3
2023-11-01 10:00:00,0,3
2023-11-01 11:00:00,3,4
```

You may use standard Python libraries or `pandas` to accomplish this. The final state of the system should include the generated `hourly_rolling_stats.csv` file.