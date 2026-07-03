You are a capacity planner analyzing the resource usage of a newly developed internal microservice. The development team has provided a prototype of the service, but you need to orchestrate a test environment, simulate client connections through a proxy/forwarder, and automate the performance and resource monitoring.

The prototype service is located at `/home/user/target_app.py`. When executed (`python3 /home/user/target_app.py`), it runs an HTTP server on `127.0.0.1:9090` with a `/compute` endpoint that simulates an expensive operation.

Your objective is to complete the following multi-phase task:

**Phase 1: Environment & Port Forwarding**
1. Modify your shell profile (`/home/user/.bashrc`) to include the environment variable `CAPACITY_TARGET_PORT=8080`.
2. The service runs on port 9090, but clients must connect via port 8080 to simulate a sidecar proxy. Start a port forwarding process (you may use `socat` or write a quick Python script) that listens on `127.0.0.1:8080` and forwards all TCP traffic to `127.0.0.1:9090`. 

**Phase 2: Automation & Monitoring Script**
Write a Python script at `/home/user/capacity_planner.py` that performs the following:
1. Reads the `CAPACITY_TARGET_PORT` environment variable to know which port to connect to.
2. Identifies the Process ID (PID) of the running `/home/user/target_app.py` process.
3. Sends exactly 20 sequential HTTP GET requests to `http://127.0.0.1:<PORT>/compute`.
4. While the requests are being processed, continuously monitors the Resident Set Size (RSS) memory usage of the `target_app.py` process.
5. Calculates the average latency (response time) per request in milliseconds.
6. Writes the final results to `/home/user/capacity_report.json` in the exact following JSON format:
```json
{
  "total_requests": 20,
  "avg_latency_ms": 105.4,
  "peak_rss_bytes": 24500120
}
```
*(Note: Replace the numbers with your script's actual computed values. The `total_requests` must be exactly 20. `peak_rss_bytes` should be an integer).*

**Phase 3: Execution & Cleanup**
1. Start the `/home/user/target_app.py` service in the background.
2. Start your port forwarder in the background.
3. Run your `/home/user/capacity_planner.py` script to generate the report.
4. Once the report is generated, safely terminate (kill) both the `target_app.py` process and the port forwarding process to free up the ports.

Ensure the final JSON file is correctly populated at `/home/user/capacity_report.json` and no background processes from this task remain running when you are finished.