You are an AI assistant helping a data engineer clean up after an ETL pipeline failure.

An upstream ETL job failed midway and was blindly retried, resulting in duplicated records. Furthermore, the raw export came from a legacy system that outputs files in UTF-16LE encoding. 

Your task is to process this raw data file, remove duplicates, and calculate a time-series metric.

The raw data is located at: `/home/user/raw_etl_dump.dat`
It contains a header: `timestamp,device_id,value`

Perform the following steps:
1. Decode the file from UTF-16LE to UTF-8.
2. Remove exact duplicate rows (ensure the header remains intact and appears exactly once).
3. Sort the data chronologically (by `timestamp` ascending) and group by `device_id`.
4. Calculate a rolling average (simple moving average) of the `value` column for each `device_id`. The window size is 3 (i.e., the current reading and the up to 2 preceding readings for that specific device). If fewer than 3 readings are available for a device, average the available readings.
5. Round the rolling average to exactly 2 decimal places (e.g., `12.50`, `33.33`).

Save the final output to `/home/user/clean_rolling_avg.csv` with the following requirements:
- File must be UTF-8 encoded.
- Header must be: `device_id,timestamp,value,rolling_avg`
- Rows must be sorted primarily by `device_id` (alphabetically, ascending) and secondarily by `timestamp` (chronologically, ascending).