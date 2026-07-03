You are acting as a release manager preparing a deployment for our new "Telemetry Processing Pipeline". We have a multi-service architecture that needs to be glued together and finalized before the release.

The pipeline consists of three components located in `/home/user/app/`:
1.  A Redis message broker (already installed on the system, but needs configuration).
2.  An `ingest-api` (Python API) that receives telemetry payloads via HTTP POST, validates an authorization token, and pushes the payload to Redis.
3.  A `data-worker` (Python background process) that reads from Redis, translates the payload into a specific processed format, and appends it to a log file.

Your task is to set up, configure, and start these services so they work together seamlessly.

**Requirements:**

1.  **Dependency Management:** Create a virtual environment at `/home/user/app/venv` and install necessary Python packages (e.g., `flask`, `redis`).
2.  **Redis Setup:** Configure and start a local Redis server listening on port `6379`.
3.  **API Implementation (`ingest-api`):**
    *   Write a Python web server in `/home/user/app/ingest.py`.
    *   It must listen on `127.0.0.1:8080`.
    *   It must expose a `POST /telemetry` endpoint.
    *   It must require an `Authorization: Bearer` header. The accepted token is `rel-mgr-token-992`. If invalid, return a 401 status.
    *   The payload will be JSON: `{"device_id": "string", "metric": float}`.
    *   Upon successful authorization, the API must push this exact JSON string to a Redis list named `telemetry_queue` and return a 200 OK with `{"status": "queued"}`.
4.  **Worker Implementation (`data-worker`):**
    *   Write a Python worker script at `/home/user/app/worker.py`.
    *   It should continuously block and pop items from the Redis `telemetry_queue`.
    *   For each item, translate the JSON data into a simple comma-separated string format: `DEVICE:<device_id>,METRIC:<metric>`.
    *   Append this string (plus a newline) to `/home/user/app/processed_telemetry.log`.
5.  **Service Startup:** Start both the API and the worker process in the background so they are running and ready to process requests. Ensure the Redis server is also running.

Once complete, leave the services running. The automated test will send HTTP requests to your API and verify the output in the log file.