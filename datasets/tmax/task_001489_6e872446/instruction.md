You are a data analyst tasked with processing noisy telemetry data from a fleet of delivery drones.

The raw data is located at `/home/user/telemetry_data.csv`.
It has the following columns:
- `timestamp`: ISO8601 UTC string (e.g., `2023-10-01T10:01:00Z`)
- `device_id`: String identifier
- `speed_kmh`: Float, speed of the drone
- `battery_mv`: Integer, battery voltage in millivolts
- `temp_c`: Float, temperature in Celsius

You need to write a Python script that processes this CSV file according to the following pipeline:

1. **Cleaning and Deduplication:**
   - Remove any exactly duplicated rows. Keep only the first occurrence.
   - Remove any rows where `speed_kmh` is negative (< 0).
   - Remove any rows where `battery_mv` is missing/empty.

2. **Normalization:**
   - Create a new column `battery_pct` based on `battery_mv`.
   - The formula is: `(battery_mv - 3200) / 1000 * 100`.
   - Cap the resulting `battery_pct` so it does not exceed 100.0 and does not drop below 0.0.

3. **Rolling Statistics:**
   - For each `device_id`, calculate a rolling average of the `speed_kmh` using a window size of 3 measurements.
   - The measurements must be ordered by `timestamp` ascending.
   - Use a minimum period of 1 (meaning the first row will just be its own speed, the second row the average of the first two, etc.).
   - Name this column `rolling_speed`.

4. **Time-based Bucketing and Aggregation:**
   - Group the cleaned and enriched data into 15-minute tumbling windows based on the `timestamp` (e.g., `10:00:00` to `10:14:59`, `10:15:00` to `10:29:59`).
   - For each 15-minute interval and `device_id`, calculate:
     - `max_temp`: The maximum `temp_c` in the window.
     - `avg_rolling_speed`: The mean of the `rolling_speed` values in the window.
     - `battery_drop`: The difference between the maximum `battery_pct` and the minimum `battery_pct` within the window.

5. **Logging:**
   - Your script must create a log file at `/home/user/pipeline.log`.
   - It must write at least one line indicating the total number of rows dropped during the cleaning phase (duplicates + invalid).

6. **Output:**
   - Save the final aggregated data to `/home/user/processed_telemetry.csv`.
   - The CSV must contain the following columns in order: `interval_start`, `device_id`, `max_temp`, `avg_rolling_speed`, `battery_drop`.
   - `interval_start` must be an ISO8601 string in UTC (e.g., `2023-10-01T10:00:00Z`).
   - Sort the output primarily by `interval_start` ascending, and secondarily by `device_id` ascending.
   - Round `max_temp`, `avg_rolling_speed`, and `battery_drop` to exactly 2 decimal places.

Write and execute the necessary Python code to complete this task.