You are an observability engineer tasked with fixing and completing a custom metrics collection agent for a local application.

We have a wrapper script at `/home/user/run_all.sh` that concurrently starts a mock application (`/home/user/mock_app.py`) and our metrics collector (`/home/user/metrics_agent.py`). 

Currently, the observability setup is failing due to a startup dependency issue and incomplete implementation. The `metrics_agent.py` script crashes because it tries to connect to the application's socket before the application has finished initializing it. Additionally, the metrics agent is missing the logic to calculate storage usage and retrieve network routing information.

Your task is to fix and complete `/home/user/metrics_agent.py` to do the following:

1. **Fix the Startup Dependency:** Modify `metrics_agent.py` so that it waits for the socket file `/home/user/app_storage/app.sock` to exist before proceeding. It should poll for this file (checking every 1 second, up to a maximum of 15 seconds) rather than failing instantly.
2. **Implement Storage Monitoring:** Complete the `get_storage_bytes()` function in the script. It must calculate and return the total size (in bytes) of all files inside the `/home/user/app_storage` directory (including the socket and any log files created by the app).
3. **Implement Routing Configuration Monitoring:** Complete the `get_default_gateway()` function. It must execute the `ip route` command, parse its output, and return the IP address of the default gateway as a string.
4. **Output:** Once the socket is detected and the metrics are gathered, the script writes a JSON payload to `/home/user/dashboard.json`. Ensure the final JSON strictly matches this schema:
   ```json
   {
     "storage_bytes": <integer>,
     "default_gateway": "<string>",
     "status": "active"
   }
   ```

You can test your work by executing `/home/user/run_all.sh`. Do not modify `run_all.sh` or `mock_app.py`. Modify only `/home/user/metrics_agent.py`.