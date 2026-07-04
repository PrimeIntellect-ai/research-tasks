You are a data analyst dealing with international IoT sensor logs. You have been given a messy dataset containing timestamps, numeric readings, and multi-lingual status messages. The dataset has missing entries (gaps) and contains occasional system anomalies.

Your task is to write and execute a Python script to process this data. The raw data is located at `/home/user/sensor_data.csv`.

Perform the following data processing steps:
1. Load the CSV file and parse the `timestamp` column as datetime objects.
2. Resample the entire dataset to a strict 1-hour (`1H`) frequency, starting exactly from the earliest timestamp in the data to the latest.
3. Handle missing data (gaps) created by the resampling:
   - For the `value` column, fill missing values using linear interpolation.
   - For the `status_msg` column, fill missing values with an empty string `""`.
4. Detect anomalies: An anomaly is defined as any hour where the newly interpolated (or original) `value` is strictly greater than `80.0`.
5. For every anomalous row detected, process the `status_msg` to count the number of non-ASCII characters (any character where its Unicode code point is `> 127`).
6. Export the detected anomalies to a JSON file at `/home/user/anomalies.json`. The file must contain a JSON array of objects, one for each anomaly, with exactly these keys:
   - `"timestamp"`: The timestamp as a string in the format `"YYYY-MM-DD HH:MM:SS"`.
   - `"value"`: The numeric value, rounded to 2 decimal places.
   - `"non_ascii_count"`: The integer count of non-ASCII characters in the status message.

Ensure that any required Python packages (like pandas) are installed in your environment before running your script.