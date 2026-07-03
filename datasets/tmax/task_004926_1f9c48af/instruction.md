I need you to act as a data analyst and build a real-time CSV data processing pipeline. We have a multi-service environment running locally that simulates a high-throughput IoT sensor network. 

The environment consists of:
1. A Data Streamer Service (HTTP on `localhost:8080`) which serves a continuous stream of sensor data in CSV format at `http://localhost:8080/stream`.
2. A Redis instance (running on `localhost:6379`) used for storing the processed aggregations.
3. A Validation API (HTTP on `localhost:8081`) which you can use to check the status of your processing.

The CSV stream from `localhost:8080/stream` has the following columns:
`event_timestamp`, `sensor_id`, `temperature`, `status_code`

However, the data is messy:
- `event_timestamp` comes in multiple formats (e.g., ISO8601, UNIX epoch in seconds, and standard "YYYY-MM-DD HH:MM:SS").
- `status_code` can be 'OK', 'ERROR', or 'MAINTENANCE'.
- Some `temperature` values are empty or malformed.

Your task is to write a Python script at `/home/user/process.py` that streams this data (without loading the entire dataset into memory) and performs the following operations:
1. **Validation Checkpoint**: Drop any rows where `status_code` is not 'OK', or where `temperature` is not a valid float.
2. **Timestamp Alignment**: Parse all `event_timestamp` values and convert them to UNIX epoch timestamps (integers).
3. **Windowed Aggregation**: For each `sensor_id`, compute a rolling 60-second moving average of the `temperature`. The 60-second window is based on the event timestamps, not processing time.
4. **Data Sink**: For every valid row processed, push the latest computed moving average to Redis using the key format `sensor:{sensor_id}:avg` with the string representation of the float value (rounded to 2 decimal places).

Performance is critical. The stream contains over 2 million rows. Your script must process the data continuously with a minimal memory footprint (using generators or iterators) and high throughput. 

Once your script finishes processing the stream (the HTTP request will complete when the stream ends), output a local log file at `/home/user/processing_summary.json` containing:
- `total_valid_rows`: The number of rows successfully processed.
- `latest_timestamp`: The highest UNIX timestamp encountered.

You can start the multi-service environment by running `/app/start_services.sh`. Ensure your Python script connects to the services correctly.