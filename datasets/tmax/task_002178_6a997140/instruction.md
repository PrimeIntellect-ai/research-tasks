You are a database administrator tasked with optimizing and repairing an SQLite database containing IoT sensor telemetry. 

The database file is located at `/home/user/sensor_data.db`. It contains two tables:
1. `devices` 
   - `id` (INTEGER PRIMARY KEY)
   - `name` (TEXT)
   - `location` (TEXT)
2. `telemetry`
   - `id` (INTEGER PRIMARY KEY)
   - `device_id` (INTEGER)
   - `ts` (DATETIME)
   - `payload` (TEXT) - This column contains a JSON string, e.g., `{"temp": 22.5, "humidity": 45.0}`.

Due to a recent hard crash, the index `idx_telemetry_device_ts` on the `telemetry` table has become corrupted, occasionally returning stale or out-of-order rows. 

Your task is to write a C program that repairs the database, performs a complex analytical query extracting data from the JSON payloads, and outputs the result to a CSV file.

Specifically, write your C code in `/home/user/analyze.c` and compile it to `/home/user/analyze`. When executed, the program must:
1. Connect to `/home/user/sensor_data.db` using the SQLite3 C API.
2. Execute a `REINDEX` command to fix the corrupted indexes.
3. Execute a query that:
   - Joins the `devices` and `telemetry` tables.
   - Extracts the `temp` numeric value from the JSON `payload` column.
   - Uses a window function to calculate the moving average of the temperature for each device. The moving average should be calculated over the current row and the 2 preceding rows (based on the `ts` ordering).
4. Write the results of this query to `/home/user/output.csv`.

The CSV file must have the following exact header and format:
`device_name,timestamp,temperature,moving_avg`
Where `moving_avg` is rounded to 2 decimal places. Ensure the query results are ordered alphabetically by `device_name`, and then chronologically by `timestamp`.

You may need to install SQLite3 development headers if they are not present. You can use standard standard library functions and `libsqlite3`.