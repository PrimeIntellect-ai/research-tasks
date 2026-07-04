You are a log analyst investigating anomalous patterns from a set of IoT sensors. You've noticed that your current log ingestion pipeline is silently dropping records. Upon investigation, you discovered that some sensor messages contain embedded newlines within double-quoted CSV fields, breaking standard line-by-line parsing tools.

Your task is to write a custom C program to robustly parse the CSV, sanitize the data, perform gap-filling (resampling), and compute rolling statistics. 

Here are the requirements:

1. **Input**: A malformed CSV file located at `/home/user/sensor_logs.csv` with the header: `timestamp,sensor_id,value,message`
   - `timestamp`: Integer (Unix epoch seconds).
   - `sensor_id`: Integer.
   - `value`: Float.
   - `message`: A double-quoted string. **Crucially**, this string may contain literal newline characters (`\n`).

2. **Data Cleaning**: 
   - Parse the CSV correctly despite embedded newlines in the `message` field.
   - Replace any newline characters *inside* the quoted `message` field with a single space character (` `).
   - Retain the surrounding double quotes in the output.

3. **Gap-Filling (Resampling)**:
   - Sensors are expected to report once every second.
   - If a sensor misses one or more seconds (i.e., the timestamp jumps by more than 1), you must insert synthetic rows to fill the gap sequentially.
   - The synthetic rows must copy the `value` from the last known reading of that specific `sensor_id`.
   - The `message` field for all synthetic rows must be exactly `""` (empty string with double quotes).

4. **Rolling Statistics**:
   - Compute a simple moving average of the `value` column for each `sensor_id` over a rolling window of the last **3** data points (including the current point). 
   - This window includes both real and gap-filled synthetic data points.
   - If fewer than 3 data points are available for a sensor so far, compute the average using the available points.

5. **Output**: 
   - Write the processed data to `/home/user/processed_logs.csv`.
   - The output must include the header: `timestamp,sensor_id,value,rolling_avg,message`
   - Format `value` and `rolling_avg` to exactly two decimal places (e.g., `10.00`).
   - The output must be sorted by `timestamp` ascending. If multiple sensors share the same timestamp, sort by `sensor_id` ascending.

Write your C code in `/home/user/log_processor.c`.
Compile it using `gcc -O3 -o /home/user/log_processor /home/user/log_processor.c`.
Run your compiled program to generate the output file.