As an automation specialist, I need you to build a multi-service data processing workflow that ingests, decodes, and aggregates a live stream of text data. 

We have a legacy telemetry simulator deployed in our environment at `/app/simulator.py`. When a service connects to it via TCP on `localhost:9000`, it streams raw text logs. However, the legacy system mixes character encodings. Each line sent over the TCP socket is structured as a comma-separated format: `timestamp_ms,encoding_type,payload`. The `encoding_type` will be one of `utf-8`, `iso-8859-1`, or `shift_jis`. The `payload` is the raw byte string of the log message encoded in that format.

I need you to build a streaming ETL pipeline with the following components:

1. **Redis Cache:**
   Ensure a local Redis instance is running on `localhost:6379`. (You can install/start it as a background service).

2. **Stream Processor (`/home/user/processor.py`):**
   Write a Python script that continuously connects to `localhost:9000`, reads the incoming lines, and parses them. 
   - It must decode the `payload` using the specified `encoding_type`. If an unknown encoding or decoding error occurs, drop the line.
   - It must extract all alphanumeric words (case-insensitive, split by standard whitespace) from the decoded payload.
   - It must calculate a tumbling windowed aggregation of the top 5 most frequent words every 10 seconds (based on the `timestamp_ms` provided in the stream, not system time).
   - At the end of each 10-second window, it should save a JSON array of the top 5 words (e.g., `["error", "system", "timeout", "network", "retry"]`) to Redis under the key `window_top_words`.

3. **HTTP API (`/home/user/api.py`):**
   Write a Python web server (e.g., using Flask or FastAPI) that listens on `0.0.0.0:8080`.
   - It must expose an endpoint: `GET /top-words`.
   - This endpoint must require a Bearer token for authorization. The token must be exactly `SecretAutomationToken2024`.
   - If authorized, it fetches the current value of `window_top_words` from Redis and returns it as a JSON payload: `{"top_words": [...]}`.
   - If unauthorized, return a 401 status code.

To complete the task:
- Start the Redis service.
- Start the `/app/simulator.py` service in the background (it requires python3).
- Run your `processor.py` in the background.
- Run your `api.py` in the background.
- Leave all services running so they can be verified via automated HTTP requests.