You are tasked with building a high-performance data ingestion and cleaning service in Rust for a fleet of legacy IoT sensors. We receive unstructured, noisy text logs that need to be parsed, deduplicated, filtered using a proprietary legacy algorithm, aggregated, and gap-filled.

Here is the setup:
1. **The Legacy Binary:** We have a proprietary binary located at `/app/sensor_filter_x64` (a stripped UPX-packed ELF executable). This binary takes a single float value as an argument and returns exit code `0` if the reading is valid, and `1` if it is an anomaly. You must use this binary (or reverse-engineer its logic to implement it natively in Rust for performance) to filter out anomalous readings.
2. **The Rust Service:** Write a Rust HTTP service (using standard frameworks like `actix-web`, `axum`, or `hyper`) listening on `127.0.0.1:8080`.
3. **The Endpoint:** Expose a `POST /ingest` endpoint that accepts a raw `text/plain` body containing newline-separated log lines.
4. **Log Format:** `[YYYY-MM-DDTHH:MM:SSZ] SENSOR_<ID> msg_id=<HEX> temp=<FLOAT>`
    * Example: `[2023-10-14T08:30:00Z] SENSOR_X msg_id=a1b2 temp=24.5`
5. **Data Processing Pipeline:**
    * **Extraction:** Parse the timestamp, sensor ID, message ID, and temperature.
    * **Deduplication:** Use the `msg_id` to deduplicate records (keep only the first occurrence of a `msg_id` across the entire payload).
    * **Filtering:** Process the remaining records in parallel. Drop any record where the temperature is flagged as an anomaly by `/app/sensor_filter_x64`.
    * **Bucketing & Aggregation:** Group the valid records by second. Calculate the average temperature for each second.
    * **Gap-Filling:** The output must have a continuous second-by-second timeline from the earliest valid timestamp to the latest valid timestamp in the payload. For any second with no valid readings, forward-fill the average temperature from the previous second.
6. **Output Format:** The endpoint must return `application/json` with the following structure:
    ```json
    [
      {"time": "2023-10-14T08:30:00Z", "avg_temp": 24.5},
      {"time": "2023-10-14T08:30:01Z", "avg_temp": 24.5},
      {"time": "2023-10-14T08:30:02Z", "avg_temp": 26.1}
    ]
    ```

Initialize your Rust project in `/home/user/sensor_service`. Ensure the server is built in release mode and running in the background when your task completes.