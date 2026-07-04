You are a data scientist tasked with cleaning and aggregating a messy dataset of IoT temperature sensor readings. 

The raw data is located at `/home/user/raw_sensors.csv` and contains the following columns: `sensor_id`, `timestamp` (in ISO8601 format, e.g., 2023-10-01T10:15:30Z), and `temperature` (a float).

Write a Python script to process this data according to the following pipeline requirements:

1. **Validation & Filtering (Quality Gate):** Parse the CSV. Ignore any rows where the temperature is missing, cannot be parsed as a float, or the timestamp is invalid.
2. **Time-based Bucketing:** Group the valid readings into 1-hour tumbling windows based on the timestamp (e.g., any time from `2023-10-01T10:00:00Z` to `2023-10-01T10:59:59Z` belongs to the `2023-10-01T10:00:00Z` bucket).
3. **Bucket Aggregation:** For each `sensor_id` and 1-hour bucket, calculate the mean `temperature`. 
4. **Outlier Rejection (Quality Gate):** If a bucket's mean temperature is strictly greater than 100.0 or strictly less than -50.0, discard this bucket completely. Append a line to `/home/user/dropped.log` in the format: `Dropped sensor {sensor_id} at {bucket}`.
5. **Rolling Statistics:** For each `sensor_id`, sort the remaining valid buckets chronologically. Calculate a 3-bucket rolling average of the mean temperatures (i.e., the average of the current bucket's mean and up to 2 strictly previous *valid* buckets for that sensor). 
6. **Output:** Save the final processed data to `/home/user/clean_sensors.jsonl` (JSON Lines format). Each line must be a JSON object with exactly these keys:
   - `"sensor_id"`: (string)
   - `"bucket"`: (string, ISO8601 format like `2023-10-01T10:00:00Z`)
   - `"mean_temp"`: (float, rounded to 2 decimal places)
   - `"rolling_avg"`: (float, rounded to 2 decimal places)

The output JSONL file should be sorted primarily by `sensor_id` (alphabetically) and secondarily by `bucket` (chronologically).

Run your script to produce the output files.