You are an automation specialist responsible for establishing a new real-time telemetry processing pipeline for our industrial IoT sensor grid. Our edge devices send data in a proprietary packed format, and we need a service that decodes this data, cleans it, calculates time-based aggregates, and detects anomalies in real time.

We have provided a proprietary, stripped decoder binary located at `/app/sensor_decode`. You do not have the source code for this binary. You will need to figure out how to invoke it to decode the incoming raw hex payloads into a usable format (it outputs timestamp, sensor_id, and a float value).

Your objective is to write a network service (in any language you choose) that fulfills the following requirements:

1. **Service Endpoint**: 
   Bring up an HTTP server listening exactly on `127.0.0.1:9042`.
   The server must expose a `POST /api/v1/telemetry` endpoint.
   
2. **Authentication**:
   All requests must be authenticated using the header `Authorization: Bearer sec-iot-pipeline-8821`. Return a `401 Unauthorized` for invalid or missing tokens.

3. **Data Ingestion (Local-Remote Transfer)**:
   The POST request will contain a JSON payload with a batch of raw sensor readings:
   `{"stream_id": "alpha-grid", "payloads": ["<hex_string1>", "<hex_string2>", ...]}`

4. **Decoding & Processing Pipeline**:
   For each batch of payloads received:
   - Use `/app/sensor_decode` to convert the hex strings into raw data points.
   - Load the historical context data from `/home/user/data/historical_context.csv`. This file contains the last 1 hour of readings but has corrupted/missing `value` fields.
   - **Imputation**: Combine the historical data and the new batch. Perform linear interpolation to impute any missing `value` fields in the historical context based on surrounding timestamps.
   - **Time-based Bucketing**: Group the continuous stream of data points (historical + new batch) into strict 15-second tumbling windows (e.g., `10:00:00`, `10:00:15`), computing the mean `value` for each bucket.
   - **Rolling Aggregation**: Over these 15-second buckets, compute a 4-bucket (1-minute) trailing rolling average of the mean values.
   - **Anomaly/Changepoint Detection**: For the newly ingested buckets only, flag the bucket as an anomaly (`"is_anomaly": true`) if its mean value differs by more than 15.0% from its computed 1-minute rolling average. Otherwise, `"is_anomaly": false`.

5. **Response Format**:
   The HTTP response must return a `200 OK` status with a JSON array containing ONLY the time buckets that encompass the new data from the POST request, in chronological order:
   ```json
   [
     {
       "bucket_start_time": "2024-05-12T08:15:30Z",
       "mean_value": 42.5,
       "rolling_avg": 41.0,
       "is_anomaly": false
     }
   ]
   ```

You are completely free to use Python, Node.js, Go, or any other ecosystem, but you must configure all dependencies and start the long-running service so that our automated multi-protocol test suite can verify it via network requests.