You are an observability engineer tasked with fixing a broken metrics dashboard setup on a Linux server.

Currently, there are two services running on the machine (in the background):
1. The Metrics API (`/home/user/api.py`), listening on `127.0.0.1:8081`.
2. The Dashboard UI (`/home/user/dashboard.py`), listening on `127.0.0.1:8082`.

Due to a recent network reconfiguration, the Dashboard UI is hardcoded to fetch metrics from `http://127.0.0.1:9090/`. However, the API was moved to port `8081`. You cannot modify the source code of either `api.py` or `dashboard.py`. You also do not have root access.

Your task is to restore the dashboard's functionality by implementing a robust, user-space port forwarding solution and process supervisor using Python:

1. **Write a Port Forwarder**: Create a Python script at `/home/user/proxy.py` that listens on `127.0.0.1:9090` and transparently forwards all TCP traffic to `127.0.0.1:8081`. It must handle multiple connections and bidirectional data transfer.

2. **Write a Process Supervisor**: Create a Python script at `/home/user/supervisor.py`. This script must:
   - Launch `/home/user/proxy.py` as a subprocess.
   - Monitor the proxy process.
   - Automatically restart the proxy process if it crashes or terminates.
   - Run infinitely. 

3. **Deploy Idempotently**: Write a deployment script at `/home/user/deploy.py` that:
   - Checks if `supervisor.py` is already running.
   - If not, starts `supervisor.py` in the background (detached from the script's execution).
   - If it is already running, ensures it doesn't spawn a duplicate instance.
   - Running `python3 /home/user/deploy.py` multiple times must be completely idempotent.

4. **Verify**: Once the setup is deployed, query the dashboard endpoint:
   `curl -s http://127.0.0.1:8082/`
   Save the exact JSON output to a log file at `/home/user/metrics.log`.

Requirements:
- Use standard Python libraries only (no external pip packages like `socat` wrappers).
- Do not use root privileges.
- Ensure all created Python scripts are executable.