You are an automation specialist tasked with building a robust mathematical data processing pipeline and API server. 

You have been provided with a legacy, undocumented binary at `/app/sensor_gen`. This binary generates synthetic sensor data in CSV format to its standard output. It takes a single integer argument, which is the number of records to generate (e.g., `/app/sensor_gen 5000`).

However, the generated CSV output is notoriously messy:
1. It contains a `metadata` column that occasionally contains quoted text with embedded newlines, which breaks naive line-by-line bash processing.
2. It occasionally contains duplicate rows (same `id`).
3. Some rows are completely missing sensor values.

Your task is to create a Python application that executes the binary to generate exactly `5000` records, processes the dataset in-memory, and exposes the mathematical results via a local HTTP API.

**Data Processing Requirements:**
1. **Cleaning:** Spawn `/app/sensor_gen 5000`, read the output, and correctly parse the CSV (accounting for embedded newlines). Deduplicate records based on the `id` column (keep the first occurrence). Drop any row where ANY of the sensor value columns (`sensor_A`, `sensor_B`, `sensor_C`) are empty or NaN.
2. **Reshaping:** The clean data is in wide format: `id, timestamp, sensor_A, sensor_B, sensor_C, metadata`. Reshape this into a long format dataset containing: `id`, `timestamp`, `sensor` (e.g., "sensor_A"), and `value` (float). 
3. **Sorting:** Sort the long-format data by `timestamp` ascending.
4. **Rolling Aggregation & Anomaly Detection:** For *each* sensor independently, iterate through the sorted values. Maintain a trailing rolling window of exactly **50** historical values (not including the current row). For every row from the 51st row onwards, calculate the rolling mean and sample standard deviation of the previous 50 values. 
5. **Changepoint Identification:** Flag a row as an anomaly if its absolute difference from the rolling mean is strictly greater than `3.0` times the rolling sample standard deviation.

**API Requirements:**
You must implement a Python HTTP server (e.g., using `http.server`, `Flask`, or `FastAPI` - whatever is available or you can install via pip) that listens on `127.0.0.1:8080`. 

Expose the following endpoints:
- `GET /status`: Returns a JSON object with `{"status": "ready", "total_clean_long_records": <integer>}` representing the total number of valid (non-dropped), deduplicated data points across all sensors.
- `GET /anomalies`: Returns a JSON array of all detected anomalies, sorted by `timestamp` ascending, then by `sensor` alphabetically. Each element must be formatted as: `{"id": <int>, "timestamp": <int>, "sensor": <str>, "value": <float>}`.

Your server must start up, process the data synchronously, and then begin listening on the port. Leave the server running in the background or foreground as your final action.