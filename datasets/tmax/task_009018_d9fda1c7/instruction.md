You are an automation specialist tasked with building a robust data processing pipeline for IoT telemetry data.

We have a corrupted JSON-Lines file located at `/home/user/raw_telemetry.jsonl`. This file contains sensor readings, but the system that generated it had a bug, resulting in invalid UTF-8 bytes and intermittent missing data.

Your goal is to write and execute a Python script that processes this file step-by-step and produces a clean summary. 

**Pipeline Requirements:**

1. **Character Encoding Handling:**
   Read `/home/user/raw_telemetry.jsonl`. The file contains invalid UTF-8 characters. You must read the file using standard UTF-8 decoding but configured to **ignore** invalid bytes.

2. **Parsing & Validation:**
   Parse each line as JSON. 
   - Each valid JSON object represents a reading with keys: `"sensor"`, `"temp"`, and `"hum"`. 
   - If a line still fails to parse as valid JSON after ignoring invalid UTF-8 bytes, skip that line entirely.
   - **Constraint Validation:** The `"temp"` value must be between `-50.0` and `80.0` (inclusive). If `"temp"` is missing, `null`, or outside this range, **drop** the entire record.

3. **Interpolation / Imputation:**
   The `"hum"` (humidity) field is frequently `null` (missing). 
   You must impute missing `"hum"` values using **Forward Fill** (use the most recent successfully validated record's `"hum"` value, regardless of the sensor). 
   - If the very first valid record is missing its `"hum"` value, default it to `50.0`.
   - Forward fill happens *after* the parsing and constraint validation steps (i.e., do not inherit humidity from a record that was dropped due to invalid temperature).

4. **Summary Statistics:**
   After cleaning and imputing the data, calculate the average `"temp"` and average `"hum"` for each `"sensor"`.

5. **Output:**
   Write the aggregated results to a CSV file at `/home/user/summary.csv`.
   - The CSV must have exactly this header row: `sensor,avg_temp,avg_humidity`
   - The rows must be sorted alphabetically by the `sensor` name.
   - The numeric averages must be rounded to exactly 2 decimal places (e.g., `21.00`).

Ensure your Python script runs successfully and creates the requested file. Do not wrap the final CSV output in quotes unless necessary.