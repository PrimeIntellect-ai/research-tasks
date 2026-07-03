You are an automation specialist managing data pipelines. An existing cron-based ETL job that processes IoT sensor data has been failing midway and triggering blind retries, resulting in log files containing duplicate, out-of-order, and incomplete records. 

Your task is to write a robust data processing script using ONLY Bash, `awk`, `sed`, and standard coreutils. You may not use Python, Perl, Ruby, or other advanced scripting languages.

The raw data is located at `/home/user/data/raw_sensor.csv`. 
The file has no header. The columns are: `timestamp,sensor_id,temperature,humidity`
Example row: `2023-10-01T10:15:00Z,S1,22.5,45.0`

Write a shell script at `/home/user/process_etl.sh` that reads this file and performs the following pipeline exactly as specified:

1. **Deduplication & Alignment:** The file contains out-of-order rows and duplicates. Deduplicate records based on `timestamp` and `sensor_id`. If multiple rows have the same `timestamp` and `sensor_id`, keep only the **first** one encountered in the file. Then, sort the records chronologically by timestamp.
2. **Imputation (Forward Fill):** Due to network drops, some rows have missing `temperature` or `humidity` values (e.g., `2023-10-01T10:30:00Z,S1,,40.0` or `...,S1,22.5,`). For each `sensor_id`, forward-fill missing values using the most recent valid value for that sensor. (You can assume the first chronological record for a given sensor will never have missing values).
3. **Feature Extraction:** Calculate a new feature called `metric` using the formula: `metric = temperature + (humidity * 0.1)`.
4. **Windowed Aggregation:** For each `sensor_id`, calculate a rolling average of the `metric` over a window of the current record and the previous 2 records (a 3-record window). For the first record of a sensor, the average is just its own `metric`. For the second record, it's the average of the first two.
5. **Summary Aggregation:** Aggregate the data by day (extract `YYYY-MM-DD` from the timestamp) and `sensor_id`. Calculate the daily arithmetic mean of the rolling averages computed in step 4.

Your script must output the final aggregated data to `/home/user/data/daily_summary.csv`. 
The output must be sorted by Date ascending, then by Sensor ID ascending.
The output format must be exactly: `YYYY-MM-DD,sensor_id,daily_mean`
Round `daily_mean` to exactly 2 decimal places (e.g., `25.33`).

Make sure your script `/home/user/process_etl.sh` is executable and run it to generate the final output.