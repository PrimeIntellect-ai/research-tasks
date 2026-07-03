You are an operations engineer triaging a severe production incident. Our backend search service has been intermittently freezing, leading to a cascade of HTTP 504 Gateway Timeout errors for our users. 

The environment is a multi-service stack located in `/app/`:
- **Nginx** (Reverse Proxy) bound to `127.0.0.1:8080` (config at `/app/nginx/nginx.conf`)
- **Python API** (Flask + Gunicorn) bound to `127.0.0.1:5000` (source at `/app/api/app.py`)
- **Redis** (Data Store) bound to `127.0.0.1:6379` (config at `/app/redis/redis.conf`)

You can start the entire stack by running `/app/start.sh` and stop it via `/app/stop.sh`.

Your tasks:
1. **Analyze the Incident Pcap:** During the incident, we captured a packet trace located at `/home/user/incident.pcap`. Analyze this network capture to identify the specific HTTP request URL and query parameters that immediately preceded the barrage of 504 errors. 
2. **Log and Traceback Analysis:** Check the application logs in `/app/logs/api.log` and `/app/logs/nginx-error.log` to understand how the request from step 1 caused the service to lock up.
3. **Root Cause Fix:** Modify the Python API code (`/app/api/app.py`) to eliminate the blocking operation causing the timeouts. The API must still return the correct search results, but it must not lock up the server when provided with the problematic query.
4. **Service Configuration:** The Nginx proxy configuration may be dropping connections too quickly under mild load. Adjust `/app/nginx/nginx.conf` so that `proxy_read_timeout` is set to 10 seconds. Restart the stack.
5. **Regression Test:** Write a Python script at `/home/user/regression_test.py` that sends 50 sequential requests to `http://127.0.0.1:8080` using the problematic query identified in the pcap. The script must exit with code 0 if all requests succeed with HTTP 200 and exit with code 1 otherwise.
6. **Report:** Create a file at `/home/user/resolution.json` with the following exact schema:
```json
{
  "problematic_endpoint": "<The exact URL path and query string found in the pcap, e.g., /api/v1/search?q=...>",
  "root_cause_function": "<The name of the Redis command or Python function that blocked the thread>"
}
```

Ensure the services are running when you finish. A performance verifier will run against your stack. Your fixed endpoint must serve the problematic query with a 95th percentile latency of less than 100ms.