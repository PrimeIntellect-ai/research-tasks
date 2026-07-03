You are an infrastructure monitoring specialist tasked with setting up an auto-remediating health check and alerting system for a secure local web service. 

Your objective is to build out a custom monitoring toolchain using Python and bash that fulfills the following requirements:

1. **Directory & Link Management (Idempotent Setup)**
   Write an idempotent Python script named `/home/user/setup_env.py` that, when run, does the following without failing if the resources already exist:
   - Creates a base directory `/home/user/monitor_alert_sys` with subdirectories: `logs`, `certs`, `docroot`, and `alerts`.
   - Generates a self-signed RSA TLS certificate (`server.key` and `server.crt`) in the `certs` directory using `openssl` (via subprocess) or a Python crypto library.
   - Creates a dummy status file at `/home/user/system_status.json` containing exactly `{"status": "ok"}`.
   - Creates a symbolic link at `/home/user/monitor_alert_sys/docroot/health.json` pointing to `/home/user/system_status.json`.

2. **Web Server Setup & TLS Configuration**
   Write a Python script `/home/user/monitor_alert_sys/server.py` that acts as a secure web server.
   - It must serve files from `/home/user/monitor_alert_sys/docroot/`.
   - It must bind to `127.0.0.1` on port `8443`.
   - It must wrap its socket with TLS using the certificate and key generated in the `certs` directory.

3. **Process/Lifecycle Management**
   Write a Python script `/home/user/monitor_alert_sys/service_manager.py` that takes one argument (`start`, `stop`, or `status`) to manage `server.py` as a background daemon (simulating a basic container engine).
   - `start`: Launches `server.py` in the background, writing its PID to `/home/user/monitor_alert_sys/server.pid`.
   - `stop`: Reads the PID from the file, terminates the process, and removes the PID file.
   - `status`: Checks if the process matching the PID is currently running.

4. **Connectivity Diagnostics & Alerting**
   Write a Python script `/home/user/monitor_alert_sys/alert_monitor.py` that:
   - Attempts to perform an HTTPS GET request to `https://127.0.0.1:8443/health.json` (it must ignore self-signed certificate warnings).
   - If the request succeeds and returns HTTP 200, it exits cleanly.
   - If the request fails (connection refused, timeout, etc.), it must:
     a) Write a file `/home/user/monitor_alert_sys/alerts/latest_alert.txt` with the exact text: `ALERT: Service down`
     b) Automatically invoke `/home/user/monitor_alert_sys/service_manager.py start` to remediate the outage.

**Execution Steps to Complete:**
Once your scripts are written, you must perform the following actions in order:
1. Run `setup_env.py`.
2. Start the service using `service_manager.py start`.
3. Stop the service using `service_manager.py stop` (to simulate an unexpected crash).
4. Run `alert_monitor.py` (which should detect the outage, log the alert, and recover the service).
5. Generate a final verification file at `/home/user/final_report.json` with this exact structure:
```json
{
  "alert_file_content": "<read the exact content of latest_alert.txt>",
  "service_recovered": <true if the server is running on port 8443 again, false otherwise>
}
```

Ensure the server remains running at the end of your workflow so it can be verified.