You are a backup operator testing a restore automation pipeline. The pipeline involves a script that simulates restoring files from a backup and a monitoring system that verifies the restore status.

Currently, the automation script is failing. A wrapper script (`/home/user/run_wrapper.sh`), which simulates a cron environment by stripping environment variables, calls `/home/user/restore.py`. Because the environment (specifically `PATH` and `HOME`) is missing, `restore.py` fails to locate the `tar` command and defaults to writing its error output to `/tmp/fallback.log` instead of the required `/home/user/logs/restore.log`.

Your tasks are:

1. **Fix the Environment Wrapper:**
   Modify `/home/user/run_wrapper.sh` so that it correctly provides the necessary standard `PATH` (at minimum `/bin:/usr/bin`) and `HOME` (`/home/user`) to `/home/user/restore.py` when it executes it via `env -i`. Do NOT modify `restore.py`. Ensure that when `/home/user/run_wrapper.sh` is run, `restore.py` correctly executes `tar` and writes its completion message (which contains the word "SUCCESS") to `/home/user/logs/restore.log`.

2. **Create a Health-Check Reverse Proxy:**
   Write a Python 3 script at `/home/user/health_proxy.py` using only standard library modules (e.g., `http.server`, `urllib.request`). The script must:
   - Listen for HTTP GET requests on `127.0.0.1` port `9090`.
   - If a request is made to the exact path `/health`:
     - It must check the contents of `/home/user/logs/restore.log`.
     - If the file exists and contains the string `SUCCESS`, return an HTTP `200 OK` response with the body `OK`.
     - If the file does not exist or does not contain `SUCCESS`, return an HTTP `503 Service Unavailable` response with the body `FAIL`.
   - If a request is made to any other path (e.g., `/api/status`):
     - It must act as a reverse proxy, forwarding the exact GET request path to a backend server expected to be running at `http://127.0.0.1:8080`.
     - It must return the HTTP status code and body it receives from the backend server to the original client. (You do not need to handle POST requests or forward headers for this simple test).

Ensure the proxy script can be run directly via `python3 /home/user/health_proxy.py` and remains running in the foreground to serve requests.