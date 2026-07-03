You are an AI assistant helping a data scientist build an automated data cleaning and anomaly detection pipeline.

We have historical sensor data stored in a wide format in SQLite databases, and we need to deploy a microservice that processes this data, extracts features, detects anomalies using a proprietary compiled oracle, and writes the results back.

Your task is to implement an HTTP REST service in Python that orchestrates this ETL and analysis pipeline.

Here are the requirements for your service:
1. **Server Setup**: Run an HTTP server on `0.0.0.0:8000`. You can use Flask, FastAPI, or standard library.
2. **Endpoint**: Expose a `POST /process` endpoint that accepts JSON payloads in the format: `{"db_path": "/path/to/database.sqlite"}`.
3. **Data Extraction & Reshaping**: 
   - Connect to the SQLite database specified by `db_path`.
   - The database contains a table `wide_readings` with columns: `timestamp` (integer), and several sensor columns (e.g., `s0`, `s1`, `s2`, ... `sN`) containing float values.
   - Bulk export this data and reshape it from wide format to a long format with columns: `timestamp`, `sensor_id`, `value`.
   - Clean the data by dropping any rows where `value` is NULL.
4. **Feature Extraction**:
   - For each sensor (ordered by `timestamp` ascending), compute the first-order difference of the values (i.e., $diff_i = value_i - value_{i-1}$).
   - The difference for the first timestamp of each sensor should be `0.0`.
5. **Parallel Anomaly Detection**:
   - We have been provided a proprietary stripped ELF binary at `/app/detect_outliers` which acts as an anomaly detection oracle.
   - For each unique `sensor_id`, you must invoke this binary. To speed things up, process multiple sensors in parallel using Python's multiprocessing or concurrent.futures.
   - The `/app/detect_outliers` binary reads floats from standard input (one per line) and prints `1` (anomaly) or `0` (normal) to standard output (one per line), corresponding exactly to the inputs.
   - Pass the computed `diff` values for each sensor to the binary via stdin, and read the predictions from stdout.
6. **Data Loading**:
   - Filter the long-format data to keep ONLY the records that the binary flagged as anomalies (`1`).
   - Bulk import these anomalous records into a new table in the same SQLite database named `anomalies`. The table should have columns: `timestamp` (INTEGER), `sensor_id` (TEXT), and `diff_value` (REAL).
7. **Response**: 
   - Once complete, the endpoint must return a JSON response: `{"status": "success", "anomalies_inserted": <count>}` where `<count>` is the total number of records inserted into the `anomalies` table.

Please implement and start this service. Do not exit your script; it must stay running to accept requests.