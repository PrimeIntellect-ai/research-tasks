You are a log analyst investigating patterns in scientific sensor telemetry. The raw data stream has been captured in a file located at `/home/user/sensor_logs.csv`. The data is noisy, contains re-transmitted duplicates with different transaction IDs, and mixes different measurement units.

Your task is to write a Python script that processes this CSV file, normalizes the mathematical values, deduplicates the records using a specific hash-based strategy, and monitors its own execution by writing a pipeline log.

### Input Data Format
`/home/user/sensor_logs.csv` has the following columns:
`tx_id,timestamp_ms,sensor_type,value,unit`

### Processing Rules
1. **Mathematical Normalization**:
   - `TEMP` sensors: If the unit is `F`, convert to Celsius using `C = (F - 32) * 5 / 9`. If `C`, leave as is.
   - `PRESSURE` sensors: If the unit is `PSI`, convert to kilopascals (kPa) using `kPa = PSI * 6.89476`. If `kPa`, leave as is.
   - For any other sensor type or if the value cannot be parsed as a float, consider the row **malformed**.

2. **Hash-Based Deduplication**:
   - Multiple transmissions of the same reading may exist. To deduplicate, calculate the SHA-256 hash of a specifically formatted string representing the normalized reading.
   - String format: `"{sensor_type}:{normalized_value}:{timestamp_rounded}"`
     - `normalized_value` must be the normalized float value rounded to exactly 2 decimal places (e.g., `23.45`).
     - `timestamp_rounded` must be `timestamp_ms` mathematically rounded to the nearest integer multiple of 1000 (e.g., `1625000499` becomes `1625000000`, `1625000500` becomes `1625001000`).
   - If the SHA-256 hash of this string has already been seen in the file (processing top to bottom), the current row is a duplicate. Keep only the *first* occurrence.

3. **Output Generation**:
   - Write the cleaned, normalized, and deduplicated records to `/home/user/clean_sensors.csv`.
   - The output CSV must have the columns: `tx_id,timestamp_ms,sensor_type,normalized_value` (where `normalized_value` is rounded to 2 decimal places).

4. **Pipeline Logging**:
   - During execution, write exactly one summary line to `/home/user/pipeline.log` at the end of the script.
   - The format must exactly match: `[INFO] Processed <N> valid rows, dropped <M> duplicates, dropped <K> malformed.`
   - `<N>` is the number of rows successfully written to `clean_sensors.csv`.
   - `<M>` is the number of valid rows dropped due to hash deduplication.
   - `<K>` is the number of malformed rows dropped (invalid unit, unknown sensor type, or non-numeric value).

Write and execute a Python script to perform this exact pipeline.