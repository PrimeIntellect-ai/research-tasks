You are an automation specialist tasked with processing messy, decentralized IoT sensor data. You have two incoming data streams saved as CSV files with different schemas and timestamp formats. You need to write a Python script that unifies, cleans, validates, and deduplicates this data into a standardized JSON Lines (JSONL) format.

**Input Files:**
1. `/home/user/data/stream_alpha.csv`
   - Columns: `timestamp`, `device_id`, `sensor_value`, `error_code`
   - Timestamp format: `YYYY/MM/DD HH:MM:SS` (Local time, assume UTC-4 for parsing, but output must be UTC)
2. `/home/user/data/stream_beta.csv`
   - Columns: `ts`, `dev`, `val`, `err`
   - Timestamp format: Unix Epoch (seconds since 1970-01-01 00:00:00 UTC)

**Processing Requirements:**
1. **Timestamp Alignment:** Parse all timestamps and convert them to strict ISO 8601 format in UTC: `YYYY-MM-DDTHH:MM:SSZ`.
2. **Constraint-based Validation:** Filter out and discard any rows that violate the following mathematical constraints:
   - The sensor value (mathematical float) must be within the physical limits: `-50.0 <= value <= 150.0`.
   - The error code must be exactly `0`. Any row with an error code `> 0` or `< 0` indicates a malfunction and must be dropped.
3. **Hash-based Deduplication:** 
   - Some sensors send redundant data. You must deduplicate the records.
   - For each valid row, compute an MD5 hash of the following exact string format: `{device_id}_{rounded_value}` where `rounded_value` is the sensor value rounded to exactly 1 decimal place (e.g., `DEV01_45.2`).
   - If multiple rows yield the same MD5 hash, keep **only** the row with the earliest (oldest) timestamp. Discard the newer duplicates.
4. **Final Formatting & Sorting:**
   - Sort the resulting deduplicated dataset primarily by `timestamp` (oldest first), and secondarily by `device_id` (alphabetical ascending).
   - Save the output to `/home/user/output/clean_sensors.jsonl`.
   - Each line in the output must be a valid JSON object with exactly these keys: `{"timestamp": "...", "device_id": "...", "sensor_value": <float_rounded_to_1_decimal>, "hash": "..."}`.

Write a Python script to perform this data processing pipeline and run it. The final file `/home/user/output/clean_sensors.jsonl` will be checked by an automated system.