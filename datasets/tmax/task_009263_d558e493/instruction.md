You are an infrastructure engineer tasked with fixing a broken monitoring pipeline and automating its provisioning. 

We have a local setup in `/home/user/infra`. A simulated "remote" API runs locally on port 8080. You need to create a port-forwarding proxy, set up a health monitor, and fix a wrapper script that is failing due to cron-like environment constraints.

Here is the current state (which you must assume exists):
- `/home/user/infra/api.py`: A Python script that runs a simple HTTP server on `127.0.0.1:8080`.
- `/home/user/infra/config.json`: Contains `{"target_port": 9090, "log_path": "logs/health.log"}`.
- `/home/user/infra/run_monitor.sh`: A bash script designed to be run by a job scheduler. To simulate a strict cron environment, this script clears most environment variables, changes the working directory to `/`, and then executes `python3 /home/user/infra/monitor.py`.
- `/home/user/infra/logs/`: A directory for log files.

Your tasks:

1. **Create a Port Forwarder**: 
   Write a Python script at `/home/user/infra/proxy.py` that listens on `127.0.0.1:9090` and forwards all TCP traffic to `127.0.0.1:8080`. This script must run indefinitely and handle multiple sequential connections robustly (error handling for broken pipes/connections is required).

2. **Write the Health Monitor**:
   Write a Python script at `/home/user/infra/monitor.py`. It must:
   - Read the port and log path from `/home/user/infra/config.json`.
   - Make an HTTP GET request to `http://127.0.0.1:<target_port>/health`.
   - Append a line to the configured log file. The line must be exactly `STATUS: OK` if the request succeeds with an HTTP 200, or `STATUS: FAIL` if it fails or the connection is refused.
   - **Crucially:** Because `run_monitor.sh` runs from the `/` directory, relative paths (like reading `config.json` or writing to `logs/health.log`) will fail or write to the wrong location. Your `monitor.py` must intelligently resolve its own directory to ensure it reads the config and writes the logs to the correct absolute path inside `/home/user/infra/`.

3. **Create a Provisioning Automation Script**:
   Create a bash script at `/home/user/provision.sh`. When executed, this script must:
   - Start `/home/user/infra/api.py` in the background.
   - Start `/home/user/infra/proxy.py` in the background.
   - Wait 2 seconds to ensure services are up.
   - Execute `/home/user/infra/run_monitor.sh`.
   
Ensure your `provision.sh` leaves the background processes running and exits with code 0. Do not modify `/home/user/infra/run_monitor.sh` directly; handle the environment constraints within your Python script.