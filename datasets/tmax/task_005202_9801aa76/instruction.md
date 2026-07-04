You are a data scientist cleaning a large time-series dataset of IoT sensor readings. The dataset is provided as a CSV file and is expected to be too large to fit entirely into memory, so you should process it using a streaming or chunking approach.

The input file is located at `/home/user/sensor_data.csv`.
It has the following columns: `timestamp,device_id,temperature`
The timestamps are in ISO8601 format (e.g., `2023-10-01T10:05:12Z`) and are mostly chronologically ordered, but there may be slight out-of-order anomalies.

Your task is to process this file and generate a cleaned CSV at `/home/user/cleaned_dev_42.csv` with the following requirements:

1. **Filter**: Only include rows where `device_id` is exactly `dev_42`.
2. **Align and Aggregate**: Resample the data into 1-minute intervals. The new timestamp should be the start of that minute (e.g., `2023-10-01T10:05:00Z`). If there are multiple readings for `dev_42` within the same minute, calculate the mean of their temperatures.
3. **Gap Filling**: 
   - If there are missing 1-minute intervals between two actual data points, and the number of missing minutes is between 1 and 5 (inclusive), forward-fill these missing minutes with the average temperature of the last known minute.
   - If the number of missing minutes between two actual data points is strictly greater than 5, **do not** fill any of those missing minutes (leave the gap empty).
4. **Output Format**:
   - The output CSV must have a header: `timestamp,device_id,avg_temperature`
   - The `timestamp` must be the aligned 1-minute interval (ending in `00Z`).
   - The `device_id` will always be `dev_42`.
   - The `avg_temperature` must be formatted to exactly 2 decimal places (e.g., `23.50`).
   - The output rows must be strictly sorted by `timestamp` in ascending order.

Write a script in the language of your choice to perform this processing and save the output.