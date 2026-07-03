You are a Database Reliability Engineer. We have recovered a backup of our telemetry database (`/home/user/backup.db`), but the data ingestion pipeline had a flaw. It occasionally inserted duplicate rows for the same `sensor_id` and `epoch_time` when retrying failed batches. In these cases, the row with the higher `id` contains the correct, most up-to-date reading, while the lower `id` rows are stale.

Your task is to write a C program that cleanses this data using analytical queries and calculates the change in readings over time.

Requirements:
1. Write a C program at `/home/user/filter_and_analyze.c`.
2. Connect to the SQLite database `/home/user/backup.db`. The table is named `sensor_data` with columns: `id INTEGER PRIMARY KEY, sensor_id INTEGER, epoch_time INTEGER, reading REAL`.
3. Write a query using SQLite window functions to:
   - Filter out the stale rows (keep only the row with the maximum `id` for each `sensor_id` and `epoch_time` combination).
   - For the corrected data, calculate the previous reading for each sensor ordered by `epoch_time` (using the `LAG` window function).
   - Calculate the difference between the current reading and the previous reading (`reading - prev_reading`).
4. Output the results to a CSV file at `/home/user/report.csv` with the exact header: `sensor_id,epoch_time,reading,prev_reading,difference`.
5. Exclude rows where there is no previous reading (i.e., the first reading for each sensor).
6. Order the final CSV output by `sensor_id` ASC, then `epoch_time` ASC.
7. Format all floating-point numbers (`reading`, `prev_reading`, `difference`) to exactly 1 decimal place.
8. Compile your program (e.g., to `/home/user/filter_and_analyze`), ensuring you link against the SQLite3 library. You may need to install the SQLite3 development headers using your package manager if they are missing.
9. Execute your compiled program so that `/home/user/report.csv` is generated.

Do not modify the original `/home/user/backup.db` database. All logic must be handled via the C program and its SQL queries.