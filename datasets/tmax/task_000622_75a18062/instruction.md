You are an automation specialist tasked with fixing a broken sensor data ingestion pipeline and writing a robust data processing utility to analyze its output. 

There are two parts to this task:

### Part 1: Service Pipeline Integration
We have a microservice pipeline located in `/app/` that streams and archives sensor data. It consists of:
1.  **Redis**: Message broker.
2.  **Flask API (`/app/api.py`)**: Receives JSON payloads on port 5000 and pushes them to Redis.
3.  **Archiver (`/app/archiver.py`)**: Subscribes to Redis and appends data to a CSV.
4.  **Generator (`/app/generator.py`)**: Generates test data.

Currently, the services are misconfigured and cannot communicate. You must:
- Fix the environment variables in `/app/config/api.env` and `/app/config/archiver.env` so both services successfully connect to Redis (running on `127.0.0.1:6379`).
- Ensure the archiver is configured to write to `/app/data/raw_sensors.csv`.
- Start the Redis server, API, and Archiver in the background so the end-to-end flow works.

### Part 2: Algorithmic Data Processor
Once the data is archived, we need a CLI tool to process it. Create a script at `/home/user/process_metrics.py`. 

**Invocation:**
`python3 /home/user/process_metrics.py <input_data.csv> <metadata.csv>`

**Requirements:**
1.  **Read and Reshape:** The `<input_data.csv>` will be in a wide format: `timestamp, sensor_A, sensor_B, sensor_C`. Reshape this into a long format: `timestamp, sensor_id, value`. Drop any rows where `value` is empty.
2.  **Join:** Read `<metadata.csv>` which has columns `sensor_id, location, threshold`. Join this with your long-format data on `sensor_id`.
3.  **Rolling Statistics:** For each distinct `sensor_id`, sort the rows chronologically by `timestamp` (integer). Compute a rolling average of the `value` over a window of 3 periods (the current row and the up to 2 previous rows). *Note: For the first row of a sensor, the average is just its value. For the second row, the average of the two.* Round the rolling average to 2 decimal places.
4.  **Filter & Output:** Keep only rows where the newly computed rolling average is **strictly greater** than the sensor's `threshold` (from the metadata).
5.  Print the resulting rows to `stdout` as a strict JSON array of objects, ordered by `timestamp` ascending, then `sensor_id` ascending. Each object must have keys: `["timestamp", "sensor_id", "location", "value", "rolling_avg"]`.

Your script must be strictly reproducible and will be tested against thousands of fuzz inputs to ensure bit-exact equivalence with our reference implementation. Do not print anything else to stdout.