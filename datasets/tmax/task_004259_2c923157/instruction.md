You are a data engineer responsible for building a robust ETL pipeline. We have a batch of messy sensor data that needs to be cleaned, partitioned, and analyzed.

Your task is to write and execute a Go script (`/home/user/etl.go`) that performs the following steps:

1. **Read Data:** Read a CSV file located at `/home/user/data/sensors.csv`. The file has headers: `timestamp,sensor_id,temperature,pressure`.
2. **Schema Enforcement:** Filter out any invalid rows. A row is considered valid ONLY if:
   - It has exactly 4 columns.
   - `timestamp` is a non-empty string.
   - `sensor_id` is a valid integer between `1` and `3` (inclusive).
   - `temperature` and `pressure` are valid 64-bit floating-point numbers.
3. **Partitioned Storage:** For each *valid* row, write it as a JSON object to a JSON Lines (JSONL) file partitioned by the sensor ID.
   - The output directory structure must be: `/home/user/etl_output/sensor_{sensor_id}/valid.jsonl`
   - The JSON object must have keys: `"timestamp"` (string), `"sensor_id"` (int), `"temperature"` (float), `"pressure"` (float).
4. **Correlation Analysis:** Calculate the Pearson correlation coefficient between `temperature` and `pressure` across *all valid rows* combined.
5. **Metrics Logging:** Write the final correlation coefficient, rounded to exactly 4 decimal places (e.g., `0.1234`), to a file at `/home/user/metrics/correlation.txt`.

Constraints & Details:
- The data directory already exists and contains the CSV.
- You must create the `etl_output` and `metrics` directories.
- You must use Go to perform the core processing. 
- Do not use external Go packages for the math (standard library `math` and `encoding/csv`/`encoding/json` are sufficient).

Write the Go script, compile or run it, and ensure all output files are generated correctly.