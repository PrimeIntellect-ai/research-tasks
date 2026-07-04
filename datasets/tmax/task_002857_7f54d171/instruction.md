You are acting as a data engineer for an industrial IoT company. We receive high-frequency sensor telemetry from legacy factory equipment, but the data is noisy, sometimes duplicated, and occasionally contains corrupted characters due to mixed encodings.

Your task is to write a highly efficient C program that processes a raw sensor data file, cleans it, applies validation constraints, computes a windowed aggregation, and outputs the cleaned dataset.

**Input File:**
A CSV file located at `/home/user/raw_sensor_data.csv`.
It has the following header:
`timestamp_ms,sensor_id,temperature,humidity,status_message`
- `timestamp_ms`: integer (long)
- `sensor_id`: string (max 10 chars)
- `temperature`: float
- `humidity`: float
- `status_message`: string (max 50 chars)

**Processing Requirements:**
You must write a C program at `/home/user/cleaner.c` and compile it to `/home/user/cleaner`. When executed without arguments, it should read `/home/user/raw_sensor_data.csv` and generate `/home/user/cleaned_sensor_data.csv` following these rules strictly in this order:

1. **Character Encoding Sanitization:** The `status_message` field sometimes contains non-ASCII bytes. Replace any byte value greater than 127 (or less than 0 if signed) in `status_message` with a question mark (`?`).
2. **Constraint Validation:** Drop any row where `temperature` is outside the range `[-50.0, 150.0]` (inclusive) OR `humidity` is outside the range `[0.0, 100.0]` (inclusive).
3. **Deduplication:** There are duplicate transmissions. If a row has the exact same `timestamp_ms` AND `sensor_id` as a previously *seen and valid* row, drop it. (A row is "seen and valid" if it passed the constraint validation). 
4. **Windowed Aggregation:** For each `sensor_id`, calculate a rolling average of the `temperature` over the last 3 valid, non-duplicate readings (including the current row). If a sensor has fewer than 3 readings so far, average the available readings.
5. **Output Format:** Write the passing rows to `/home/user/cleaned_sensor_data.csv` with a new header:
   `timestamp_ms,sensor_id,temperature,humidity,rolling_avg_temp,status_message`
   - Format floats `temperature` and `humidity` to exactly 1 decimal place (`%.1f`).
   - Format `rolling_avg_temp` to exactly 2 decimal places (`%.2f`).
   - Fields must be comma-separated without trailing commas or spaces.

Write the C code, compile it using `gcc`, and execute it to produce the final `cleaned_sensor_data.csv` file.