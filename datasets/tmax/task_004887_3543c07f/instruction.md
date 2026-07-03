As a data scientist, you have received two large telemetry datasets from different server monitoring systems that need to be cleaned, aligned, merged, and loaded into a SQLite database. 

You must write a C++ program (`/home/user/process_telemetry.cpp`) to perform the data processing, and then use shell commands to load the result into the database.

Here are the details of the input files (already generated for you):
1. `/home/user/telemetry_a.csv`
   - Columns: `ts_iso,machine_id,cpu_temp`
   - `ts_iso` is an ISO8601 string (e.g., `2023-11-01T14:30:01.450Z`). Note: some rows may have a malformed `ts_iso` string (e.g., missing the 'T' or 'Z', or random text).
   - `machine_id` is a string (e.g., `m1`).
   - `cpu_temp` is a float.

2. `/home/user/telemetry_b.csv`
   - Columns: `ts_unix_ms,machine_id,ram_usage`
   - `ts_unix_ms` is an integer representing Unix epoch time in milliseconds.
   - `machine_id` is a string.
   - `ram_usage` is a float.

Your tasks:
1. **Timestamp Alignment & Merging (C++)**: 
   - Parse the timestamps from both files and convert them to Unix epoch seconds (truncate the milliseconds; do NOT round up).
   - Ignore any rows in `telemetry_a.csv` with malformed ISO8601 strings (i.e., strings that cannot be cleanly parsed as standard ISO8601).
   - Group the data by 1-second intervals (Unix epoch seconds) and `machine_id`.
   - Calculate the average `cpu_temp` and average `ram_usage` for each `(epoch_sec, machine_id)` group.
   - If a group only has data from one file, use `0.0` for the missing metric's average.
   - Output the merged data to `/home/user/merged_output.csv` with no header row. The format must be: `epoch_sec,machine_id,avg_cpu_temp,avg_ram_usage`. Format the averages to 1 decimal place.

2. **Pipeline Logging (C++)**:
   - Write a JSON log file to `/home/user/processing_log.json` tracking the pipeline execution. It must contain the exact following keys:
     - `"valid_rows_a"`: Integer count of successfully parsed rows from telemetry_a.
     - `"invalid_rows_a"`: Integer count of rows dropped from telemetry_a due to malformed timestamps.
     - `"rows_b"`: Integer count of rows read from telemetry_b.
     - `"merged_groups"`: Integer count of unique `(epoch_sec, machine_id)` groups written to the output.

3. **Database Bulk Import**:
   - Create a SQLite3 database at `/home/user/telemetry.db`.
   - Create a table named `merged_telemetry` with the schema: `epoch_sec INTEGER, machine_id TEXT, avg_cpu_temp REAL, avg_ram_usage REAL`.
   - Use the `sqlite3` CLI tool to bulk import `/home/user/merged_output.csv` into the `merged_telemetry` table.

Compile your C++ program using g++ (C++17 is available). You are free to use any standard C++ libraries. No external C++ libraries (like Boost) are needed or available.