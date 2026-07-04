You are acting as a data scientist cleaning a noisy IoT sensor dataset.

You have been provided with a raw dataset at `/home/user/raw_telemetry.csv`. The CSV has no header and contains three columns: `timestamp` (integer), `user_id` (string), and `sensor_value` (float, but some are missing/blank).

Your task is to build a small data processing pipeline using **C** and `sqlite3`.

**Step 1: Write a C program**
Write a C program (save it as `/home/user/process.c` and compile it to `/home/user/process`) that reads `/home/user/raw_telemetry.csv` and outputs a processed CSV file to `/home/user/processed_telemetry.csv`. 
The program must perform the following operations in order:
1. **Masking:** Anonymize the `user_id`. Replace all characters in the `user_id` with `*` except for the last 4 characters. If the `user_id` has 4 or fewer characters, leave it completely unchanged. (e.g., `patient_8821` becomes `********8821`, `abc` remains `abc`).
2. **Gap-Filling:** Fill any missing (blank) `sensor_value` entries using "forward fill" (i.e., use the most recently observed valid `sensor_value`). You can assume the very first row always has a valid sensor value.
3. **Rolling Statistics:** Calculate a 3-period Simple Moving Average (SMA) on the gap-filled sensor values. For the first row, the SMA is just the first value. For the second row, the SMA is the average of the first and second values. From the third row onwards, the SMA is the average of the current value and the two previous values. (Assume all data is chronological and belongs to a single stream).

The output file `/home/user/processed_telemetry.csv` must have NO header and should be formatted as:
`timestamp,anon_id,filled_value,sma` (format floats to exactly 2 decimal places).

**Step 2: Database Bulk Import**
After generating `/home/user/processed_telemetry.csv`, use the `sqlite3` command-line tool to bulk import this file into a new SQLite database located at `/home/user/telemetry.db`.
- Create a table named `cleaned_data` with the schema: `ts INTEGER, anon_id TEXT, val REAL, sma REAL`.
- Bulk load the CSV data into this table.

All necessary tools (gcc, sqlite3) are available in the system.