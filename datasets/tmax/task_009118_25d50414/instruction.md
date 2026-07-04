You are a data engineer tasked with building a robust, streaming ETL pipeline in Rust. 

You have been provided with a large dataset of raw electrical sensor readings at `/home/user/sensor_data.csv`. The file is massive, so your solution must stream the data line-by-line rather than loading the entire file into memory at once.

The CSV has the following headers: `timestamp,sensor_id,voltage,current`

Your objective is to create a Rust application in `/home/user/etl_pipeline` that processes this CSV file and performs the following tasks:

1. **Constraint-based Data Validation**: 
   - Discard any row where `voltage` is less than `0.0` or `current` is less than `0.0`.
   - Discard any row where `sensor_id` is empty.
   - Discard any row where any field is missing or cannot be parsed as its respective type (`timestamp` is a String, `sensor_id` is a String, `voltage` is f64, `current` is f64).
   - Keep a count of total discarded (invalid) rows.

2. **Feature Extraction**:
   - For valid rows, calculate a new field: `power = voltage * current`.

3. **Anomaly Detection**:
   - We define a power spike anomaly as any valid reading where `power > 5000.0`.

4. **Multi-stage Routing and Output**:
   - Write all valid, NON-anomalous rows as JSON Objects (JSONL format) to `/home/user/clean_data.jsonl`.
   - Write all valid, ANOMALOUS rows as JSON Objects (JSONL format) to `/home/user/anomalies.jsonl`.
   - The JSON objects must have the following keys: `"timestamp"`, `"sensor_id"`, `"voltage"`, `"current"`, `"power"`.
   - Write the total count of discarded (invalid) rows as a single integer to `/home/user/invalid_count.txt`.

Write the Rust code, compile it (e.g., using `cargo`), and run it against the provided `/home/user/sensor_data.csv` file. Make sure the output files are exactly as specified.