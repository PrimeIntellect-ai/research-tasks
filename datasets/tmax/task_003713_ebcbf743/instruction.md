You are a monitoring specialist tasked with setting up alerts and a metrics proxy for a proprietary storage appliance. 

The vendor has provided a legacy monitoring daemon located at `/app/storage_agent`. This is a stripped, compiled binary that queries the underlying storage hardware. However, the documentation has been lost. 

Your objectives are to:
1. Reverse-engineer `/app/storage_agent` to figure out the required environment variable and token needed to run it successfully. Once provided, the binary will run as a daemon listening on `127.0.0.1:9999` and will respond to `HTTP GET /raw` with a JSON payload containing disk quota and usage information (e.g., `{"disk_used_mb": 450, "disk_quota_mb": 500}`). 
2. Ensure this environment variable is permanently set in `/home/user/.bashrc` so that the agent can be restarted automatically in the future.
3. Write a Python service located at `/home/user/monitor.py` that acts as an intelligent reverse proxy and alert manager. This Python service must run continuously and bind to two distinct ports:
   - **HTTP Proxy/Metrics (Port 8080)**: 
     - A `GET /status` request must return the exact plaintext `UP`.
     - A `GET /metrics` request must proxy the data from the local `/app/storage_agent` (port 9999), translating the JSON response into Prometheus plaintext format. Specifically, it must return two lines:
       `storage_disk_used_mb <value>`
       `storage_disk_quota_mb <value>`
   - **TCP Alert Socket (Port 8081)**:
     - A raw TCP listener that accepts incoming connections.
     - When a connected client sends the exact string `CHECK\n`, the Python service must query the storage agent. 
     - If `disk_used_mb` is strictly greater than 90% of `disk_quota_mb`, it must reply with `ALERT\n`. Otherwise, it must reply with `OK\n`.

Run both `/app/storage_agent` and your `/home/user/monitor.py` in the background before completing the task. 
Use Python's standard libraries or basic packages (e.g., `requests`, `Flask`, `socket`) to build your service.