Can you help me clean and merge a couple of messy time-series datasets? I'm preparing IoT sensor data for analysis. 

There are two files in my home directory:
1. `/home/user/sensor_data.csv` - Contains raw, high-frequency sensor readings.
   - Columns: `timestamp`, `sensor_id`, `temperature`, `humidity`
   - The `timestamp` is in ISO8601 format (e.g., `2023-10-01T10:15:30Z`).
2. `/home/user/maintenance.csv` - Contains hourly maintenance logs for the sensors.
   - Columns: `hour`, `sensor_id`, `status`
   - The `hour` is in ISO8601 format representing the start of the hour (e.g., `2023-10-01T10:00:00Z`).

Here is what I need you to do:

**Step 1: Constraint-based Validation**
Filter the records in `sensor_data.csv` to remove invalid readings. A reading is valid ONLY if:
- `temperature` is a number between `-20.0` and `50.0` (inclusive).
- `humidity` is a number between `0.0` and `100.0` (inclusive).
- None of the fields are missing or empty.
Drop any rows that do not meet these criteria.

**Step 2: Time-based Bucketing and Aggregation**
For the valid readings, truncate (floor) the `timestamp` to the nearest hour. Group the data by this floored `hour` and `sensor_id`. Calculate the average `temperature` and average `humidity` for each group. Round these averages to exactly 2 decimal places.

**Step 3: Joining with Maintenance Logs**
Perform a LEFT JOIN of your aggregated sensor data with `maintenance.csv` using the floored `hour` and `sensor_id`. If a sensor does not have a status in the maintenance file for that hour, fill the `status` column with the string `"unknown"`.

**Step 4: Output**
Write the final dataset to `/home/user/cleaned_merged.csv`. 
The CSV must have the following headers: `hour,sensor_id,avg_temperature,avg_humidity,status`.
Ensure the output is sorted chronologically by `hour` (ascending), and then alphabetically by `sensor_id` (ascending).