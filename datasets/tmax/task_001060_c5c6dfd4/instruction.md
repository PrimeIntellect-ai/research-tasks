You are a data engineer tasked with building an ETL pipeline to process time-series sensor data from a fleet of industrial IoT devices. The data arrives as CSV files, but the data lake is currently being polluted by corrupted records, malformed timestamps, and malicious payloads from compromised sensors.

Your objectives are:

1. **Information Extraction (Calibration):**
   There is a scanned calibration certificate located at `/app/calibration.png`. You must extract the global calibration offset value from this image. It will be printed somewhere in the text as `OFFSET=...`. You will need this value for normalization.

2. **Data Sanitization (The Filter):**
   Create an executable bash script at `/home/user/filter.sh` that reads a CSV from `stdin` and writes valid rows to `stdout`. It must log any rejected rows to `stderr`.
   A valid row must meet ALL the following conditions:
   - Format: `timestamp,sensor_id,value`
   - `timestamp`: Must be a valid ISO8601 format (e.g., `2023-10-12T14:30:00Z`).
   - `sensor_id`: Must be exactly 8 alphanumeric characters.
   - `value`: Must be a valid floating-point number between `-50.0` and `150.0` inclusive.
   - Headers (if present) should be ignored or passed through unaltered (do not fail the header).

3. **Data Aggregation (The Pipeline):**
   Create an executable bash script at `/home/user/etl.sh` that takes a directory of CSV files as its first argument and an output file path as its second.
   The script must:
   - Stream all CSV files in the input directory through your `filter.sh`.
   - Normalize the valid `value`s by ADDING the calibration offset you extracted from `/app/calibration.png`.
   - Deduplicate rows (if multiple rows have the exact same timestamp and sensor_id, keep only the first one encountered).
   - Group the time-series data by `sensor_id` and the hour of the timestamp (e.g., `2023-10-12T14`).
   - Calculate the average normalized value for each group.
   - Sort the output chronologically by the hour, then by `sensor_id`.
   - Write the output to the specified output file in the format: `YYYY-MM-DDTHH,sensor_id,avg_value` (avg_value rounded to 2 decimal places).

Ensure your scripts are robust. Your `filter.sh` will be rigorously tested against a hidden corpus of clean and malicious/corrupt data.