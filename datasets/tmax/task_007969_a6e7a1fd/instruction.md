As an automation specialist, you need to build a robust Python data pipeline that processes a messy sensor log file, performs validation and aggregation, and writes the output to a cleaner format.

I have a CSV file located at `/home/user/data/sensor_readings.csv`. 
The CSV has the following columns: `timestamp`, `sensor_id`, `temperature`, `status`, `notes`.
Some fields in the `notes` column contain embedded newlines enclosed in quotes.

Write a Python script (and execute it) that reads this CSV and does the following:
1. **Validation & Filtering**:
   - Sort the records chronologically by `timestamp` (ascending).
   - Keep only rows where `status` is exactly `"OK"`.
   - Keep only rows where `temperature` can be parsed as a float between `-50.0` and `150.0` (inclusive).
   - **Crucial step:** Silently drop any row where the `notes` field contains a newline character (`\n`). Do not log anything for these dropped rows.
2. **Aggregation**:
   - For the valid rows that remain, calculate a rolling average of the `temperature` using a window size of 3 (the current valid reading and the up to 2 previous valid readings).
   - If fewer than 3 valid readings have been processed so far, average the available valid readings.
   - Round the average to exactly 2 decimal places.
3. **Output**:
   - Save the processed data to `/home/user/output/processed_sensors.jsonl` in JSON Lines format (one JSON object per line).
   - Each JSON object must have the following keys:
     - `"timestamp"` (string)
     - `"sensor_id"` (string)
     - `"temp_rolling_avg"` (float, the computed rolling average)
     - `"notes"` (string)

Ensure that the directory `/home/user/output/` exists before writing.