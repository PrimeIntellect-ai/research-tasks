You are a data scientist tasked with cleaning, merging, and aggregating factory sensor data. 

You have been provided with three data sources in `/home/user/`:
1. `temp_sensors.csv`: Contains temperature readings. Columns: `timestamp` (ISO8601), `machine_id`, `temperature`
2. `humidity_sensors.csv`: Contains humidity readings. Columns: `timestamp` (ISO8601), `machine_id`, `humidity`
3. `maintenance.db`: An SQLite database containing a table `maintenance_logs` with columns: `machine_id`, `last_service_date`, `status`

Your task is to write and execute a script (in the language of your choice) to process these datasets into a final analytical dataset. 

Perform the following operations:
1. **Database Export & Merge:** Extract the `maintenance_logs` data from the SQLite database. You will need to join this with the sensor data. Filter out and completely discard any records for machines where the `status` is `'DECOMMISSIONED'`.
2. **Time-Based Bucketing:** Truncate/floor the `timestamp` in the sensor CSVs to the start of the hour (e.g., `2023-10-01T01:45:00Z` becomes `2023-10-01T01:00:00Z`).
3. **Aggregation & Joins:** For each 1-hour bucket and each `machine_id`, compute the mean `temperature` and mean `humidity`. Join the temperature and humidity aggregates together. If a machine has a temperature reading but no humidity reading in a given hour (or vice versa), perform an inner join (only keep hours where a machine has BOTH temperature and humidity data).
4. **Rolling Statistics Computation:** For each machine, calculate a 3-hour rolling average of the aggregated hourly temperature (i.e., the mean of the current hour's average temperature and the previous 2 available hourly average temperatures for that machine). If fewer than 3 hours of history are available, compute the average over the available hours.
5. **Formatting:** Round all numeric outputs (mean temperature, mean humidity, rolling temperature) to exactly 2 decimal places.

**Output Specification:**
Save the final processed dataset to `/home/user/processed_data.json` as a JSON array of objects, sorted chronologically by `time_bucket`, then alphabetically by `machine_id`.

Each JSON object must have exactly these keys:
- `"time_bucket"`: The 1-hour floored timestamp string (e.g., `"2023-10-01T01:00:00Z"`)
- `"machine_id"`: The ID of the machine (e.g., `"M1"`)
- `"avg_temp"`: The mean temperature for that hour (number)
- `"avg_humidity"`: The mean humidity for that hour (number)
- `"rolling_3h_temp"`: The 3-hour rolling average temperature (number)
- `"status"`: The maintenance status of the machine (string)

Ensure your script handles all the steps properly, executes successfully, and creates the final file at the specified path.