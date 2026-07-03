You are a FinOps analyst tasked with optimizing cloud routing costs based on live telemetry data. You need to identify the most cost-effective, healthy availability zone that meets strict latency requirements, and then configure the system's routing environment to use it.

First, set up the local mock API gateway that provides the telemetry data:
1. Create a Python script at `/home/user/mock_service.py` with the following content (you can copy-paste this via your terminal):
```python
from http.server import BaseHTTPRequestHandler, HTTPServer
import json

class MockHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        self.end_headers()
        
        if self.path == '/zone1/cost_metrics':
            data = {"status": "up", "cost_per_10k_requests": 5.0, "latency_ms": 120}
        elif self.path == '/zone2/cost_metrics':
            data = {"status": "up", "cost_per_10k_requests": 8.0, "latency_ms": 45}
        elif self.path == '/zone3/cost_metrics':
            data = {"status": "up", "cost_per_10k_requests": 3.5, "latency_ms": 80}
        elif self.path == '/zone4/cost_metrics':
            data = {"status": "down", "cost_per_10k_requests": 1.0, "latency_ms": 10}
        else:
            self.send_response(404)
            data = {}
            
        self.wfile.write(json.dumps(data).encode())

    def log_message(self, format, *args):
        pass

if __name__ == '__main__':
    HTTPServer(('127.0.0.1', 8080), MockHandler).serve_forever()
```
2. Start this mock service in the background.

Next, complete the following objectives:

1. **Write an Analyzer Script:** 
   Write a Python script at `/home/user/analyzer.py` that queries the `/cost_metrics` endpoint for `zone1`, `zone2`, `zone3`, and `zone4` on `http://127.0.0.1:8080`.
   The script must determine the optimal zone. To be considered, a zone must have a `"status"` of `"up"` and a `"latency_ms"` strictly less than 100. Among the qualifying zones, choose the one with the lowest `"cost_per_10k_requests"`.
   
2. **Generate Routing Configuration:**
   Your script (`analyzer.py`) must automatically write the optimal zone's base URL to a JSON configuration file at `/home/user/optimal_route.json` in the exact following format:
   `{"target_url": "http://127.0.0.1:8080/<OPTIMAL_ZONE>"}`

3. **Environment Setup:**
   Create a shell environment profile at `/home/user/.finops_env`. This file should contain exactly one line exporting the optimal zone's base URL:
   `export DEFAULT_CLOUD_ZONE="http://127.0.0.1:8080/<OPTIMAL_ZONE>"`

4. **Connectivity Diagnostics:**
   Source your newly created `/home/user/.finops_env` file to load the variable. Then, using Python from the command line (or a short script), perform an HTTP GET request to the base URL stored in `$DEFAULT_CLOUD_ZONE` (e.g., `http://127.0.0.1:8080/zoneX`). Note that requesting the base URL on the mock service will return a 200 OK (with an empty JSON dictionary or fallback data, which is fine). 
   Write ONLY the HTTP status code (e.g., `200`) of this response to a file at `/home/user/connectivity_test.log`.

Make sure to leave all created files (`optimal_route.json`, `.finops_env`, `connectivity_test.log`, and `analyzer.py`) on the disk in `/home/user/` when you are finished.