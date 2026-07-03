Wake up, we have a P1 incident. It's 3:00 AM and our primary telemetry ingest node just crashed. 

Here is the situation:
1. The service ran out of disk space, corrupting the main SQLite database. A junior engineer tried to fix it but accidentally deleted the database file entirely from the attached loop device image.
2. The legacy ingestion API is dead, but our downstream systems are hard down until they can fetch the data that was buffered in that database.
3. The data inside the database is encoded using a proprietary format. The only thing that knows how to decode it is a legacy C binary located at `/app/decoder.bin`. Unfortunately, the binary is stripped and occasionally segfaults on malformed inputs, so we can't just wrap it in a subprocess blindly.

Your mission:
1. **Deleted File Recovery**: We have a backup of the partition image at `/app/telemetry_data.img` (an ext4 image). The deleted files were `/telemetry.db` and `/telemetry.db-wal`. Recover them.
2. **Database Recovery**: Reconstruct the corrupted SQLite database. The database has a table `telemetry` with columns `id` (INTEGER), `timestamp` (INTEGER), and `encoded_payload` (TEXT). Write a Python script to extract the intact rows. Use assertion-based intermediate validation to ensure the schema matches exactly before processing.
3. **Reverse Engineering / Fuzz Testing**: Analyze `/app/decoder.bin` (which reads from stdin and writes JSON to stdout). Fuzz test it to determine its encoding algorithm. Re-implement the decoding algorithm in Python to guarantee stability. 
4. **Service Restoration**: Bring up an HTTP server in Python listening on `127.0.0.1:9000`. 
    - Endpoint: `GET /api/v1/record/<id>`
    - Response: HTTP 200 with JSON payload matching `{"id": <id>, "timestamp": <timestamp>, "decoded_data": "<result_from_python_decoder>"}`. If the ID is not found, return HTTP 404.

Constraints:
- You must write the replacement API in Python.
- Do not rely on `/app/decoder.bin` at runtime for the HTTP API; you must reimplement its logic.
- Ensure the server is running as a daemon or in the background before you finish.