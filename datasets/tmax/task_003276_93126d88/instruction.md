You are an automation specialist tasked with creating a real-time data processing workflow. We have a legacy system that sends raw binary sensor logs via HTTP POST requests, and we need to process this data on the fly.

Your task is to implement an HTTP server in Python listening on `127.0.0.1:9090` that processes these incoming requests and returns clean, normalized data.

Here are the requirements:
1. **The Legacy Binary:** We have a proprietary binary at `/app/sensor_decoder` that decodes the raw binary payloads. If you pipe raw binary data into its standard input, it outputs JSON lines to standard output. 
2. **The Server:** Create a Python HTTP server (listening on `127.0.0.1:9090`). It must accept POST requests to the `/process` endpoint. The server must verify an authorization header: `Authorization: Bearer secr3t_t0k3n`. 
3. **Data Processing Workflow:** For each request:
   - Pass the POST body (raw binary) through `/app/sensor_decoder`.
   - The output will be JSON objects with keys: `timestamp` (integer Unix epoch), `text_note` (string, multi-language), `sensor_val` (float or null), and `user_id` (string).
   - **Deduplication:** Remove exact duplicate rows based on the `timestamp`. If timestamps duplicate with different data, keep the first occurrence.
   - **Resampling & Gap-filling:** Ensure there is a record for every second between the minimum and maximum `timestamp` in the payload. Fill missing `sensor_val` using forward-fill (use the last known value). For newly created rows, set `text_note` to empty string `""` and `user_id` to `"SYSTEM"`.
   - **Data Masking:** Anonymize all `user_id` fields by replacing them with their SHA-256 hex digest.
   - **Unicode Processing:** Normalize all `text_note` fields to Unicode NFC form and convert them to lowercase.
4. **Response:** The server must respond with HTTP 200 OK and return the processed JSON lines (ordered by timestamp ascending), separated by newline characters.

Implement the server and start it in the background. Write logs to `/home/user/server.log` containing the number of records processed per request.