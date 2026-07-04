You are tasked with building a real-time ETL stream processing server in Python. We have an incoming stream of user event data that needs to be enriched, masked, and stratified before downstream consumption.

Requirements:
1. Build a Python HTTP server listening on `127.0.0.1:9090`.
2. Expose a POST endpoint at `/api/v1/process`. The endpoint will receive large payloads of JSON lines (JSONL), representing user events.
3. You must process the incoming payload as a stream (to handle large files efficiently).
4. For each JSON object:
   - **Data Masking:** Obfuscate the `email` field completely by replacing its value with exactly `***@***.***`.
   - **Data Enrichment (Join/Merge):** We have a proprietary legacy hashing executable located at `/app/legacy_hasher`. It is a compiled stripped binary. You must pass the `user_id` field from the JSON object as a command-line argument to this binary (e.g., `/app/legacy_hasher <user_id>`). It will output a hexadecimal string to stdout. Add this output to the JSON object under a new key called `secure_token`.
   - **Data Sampling/Stratification:** Only retain and output records where the first character of the generated `secure_token` is an alphabetic character (`a-f`). Drop the rest.
5. Return the retained, enriched, and masked JSON lines in the HTTP response body as a JSONL stream.
6. **Pipeline Logging:** Whenever a request is completed, append a single line to `/home/user/etl_metrics.log` in the exact format: `PROCESSED:<total_received_rows>|RETAINED:<total_returned_rows>`.

Start your server in the background so it is ready to receive requests.