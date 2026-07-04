You are a monitoring specialist tasked with setting up a reverse proxy and an alerting system for a legacy application. The architectural specifications have been handed to you as an image file located at `/app/architecture_spec.png`.

Your objectives are as follows:

1. **Extract Specifications**: Analyze the image at `/app/architecture_spec.png`. It contains critical configuration values you will need:
   - `PROXY_PORT`: The port your reverse proxy should listen on.
   - `APP_1_PORT`: The port for backend Application 1.
   - `APP_2_PORT`: The port for backend Application 2.
   - `MONITOR_PORT`: The port your monitoring API should listen on.
   - `AUTH_TOKEN`: The bearer token required to access your monitoring API.
   - `THRESHOLD`: The number of 5xx HTTP errors within a single run that should trigger an alert.

2. **Directory Structure Setup**: 
   - Create the directory structure: `/home/user/telemetry/logs/` and `/home/user/telemetry/config/`.
   - Create a symbolic link at `/home/user/active_logs` that points to `/home/user/telemetry/logs/`.

3. **Reverse Proxy Implementation**:
   - Write and run a reverse proxy service (you may use Python, Node.js, or any available language) that listens on the `PROXY_PORT`.
   - All HTTP GET requests to `http://localhost:<PROXY_PORT>/app1/...` must be proxied to `http://localhost:<APP_1_PORT>/...` (stripping the `/app1` prefix).
   - All HTTP GET requests to `http://localhost:<PROXY_PORT>/app2/...` must be proxied to `http://localhost:<APP_2_PORT>/...` (stripping the `/app2` prefix).
   - The proxy must log every completed request to `/home/user/active_logs/proxy_access.log`. The log format must be a simple text line per request containing at least the HTTP status code returned to the client (e.g., "GET /app1/test HTTP/1.1 200" or just a line ending with "status: 200" or similar, as long as the status code is easily parseable as a 3-digit number).

4. **Monitoring Alert API**:
   - Write and run a monitoring service listening on the `MONITOR_PORT`.
   - It must expose an HTTP `GET /health` endpoint.
   - This endpoint must require an `Authorization` header in the format `Bearer <AUTH_TOKEN>`. If missing or incorrect, return HTTP 401 Unauthorized.
   - When called, the service should read `/home/user/active_logs/proxy_access.log`.
   - If the total number of 5xx class status codes (500-599) in the log file is strictly greater than the `THRESHOLD` value, the endpoint must return an HTTP 503 status code with a JSON payload: `{"alert_status": "CRITICAL"}`.
   - If the number of 5xx errors is less than or equal to the threshold, it must return an HTTP 200 status code with a JSON payload: `{"alert_status": "OK"}`.

You are responsible for leaving both the reverse proxy and the monitoring API running in the background. The automated verifier will spin up its own dummy backends on `APP_1_PORT` and `APP_2_PORT` and send HTTP requests to test your implementation. Ensure your services are robust and remain active.