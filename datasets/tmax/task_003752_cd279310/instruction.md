You are tasked with fixing and deploying a configuration manager tracking system located in `/app/`. The system receives streaming configuration updates from various microservices, tracks changes over time, and exposes time-series metrics. 

The application consists of three services that must run together:
1. Nginx (acts as a reverse proxy, listening on port 8080)
2. A Python backend service (listening on port 5000)
3. Redis (listening on port 6379, used for state/cache)

Currently, the system is partially implemented and has several critical bugs:
1. **Unicode/JSON-Lines Bug:** The `/ingest` endpoint accepts POST requests with JSON-lines payload. However, the current naive parser in `app.py` breaks when configuration payloads contain multi-language text with unicode escape sequences (e.g., `\u00fc`). 
2. **Deduplication:** Multiple identical configuration states are often broadcasted. You must implement hash-based deduplication. Within any given minute bucket, if multiple incoming JSON lines have the exact same string value in the `"data"` field, they should only be counted as ONE change. You must hash the `"data"` field to track this.
3. **Time-based bucketing & Interpolation:** The `/metrics` endpoint should return minute-by-minute bucketing of configuration changes. If a minute has no changes, it must be imputed/interpolated with a count of `0`.
4. **Windowed Aggregation:** The `/metrics` endpoint must also return a `rolling_5m_count`, which is the sum of deduplicated changes over the last 5 minutes (the current minute plus the 4 preceding minutes).

**Your Tasks:**
1. Fix `nginx.conf` in `/app/nginx/` so that requests to `http://localhost:8080/` correctly proxy to the Python backend on port 5000.
2. Fix the Python backend (`/app/app.py`). You may use Flask or any standard framework (a basic `requirements.txt` is provided in `/app/`, you can install it in a venv or user site).
3. Implement the `/ingest` endpoint:
   - Method: POST
   - Body: JSON-lines. Each line is a JSON object with `"timestamp"` (ISO 8601 string, UTC) and `"data"` (string).
   - Action: Parse the unicode correctly, deduplicate by `"data"` hash per minute, and store the counts in Redis.
4. Implement the `/metrics` endpoint:
   - Method: GET
   - Query params: `start` and `end` (ISO 8601 strings, minute precision, e.g., `2023-10-01T12:00:00Z`).
   - Action: Return a JSON array of objects for EVERY minute from `start` to `end` (inclusive).
   - Format: `[{"minute": "2023-10-01T12:00:00Z", "changes": 1, "rolling_5m_count": 3}, ...]`
5. Start all three services (Redis, Nginx, Python app) so they are running in the background and listening on their respective ports.

Ensure the system is fully operational. An automated test will send a sequence of HTTP requests to `http://localhost:8080/ingest` and `http://localhost:8080/metrics` to verify your implementation.