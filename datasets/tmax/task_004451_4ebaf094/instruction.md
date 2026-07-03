You are acting as a capacity planner who needs to set up an automated resource monitoring and alerting system. Because you do not have root access, you must configure this system entirely in user space. 

Your goal is to build a Python-based monitoring stack supervised by `supervisord`, which reads configurations via symlinks, analyzes resource usage, and sends email alerts to a local mock SMTP server when thresholds are breached.

Follow these steps exactly:

1. **Directory and Configuration Structure:**
   Create the following directory structure:
   - `/home/user/capacity_planner/configs/`
   - `/home/user/capacity_planner/logs/`
   - `/home/user/capacity_planner/bin/`

   Inside `/home/user/capacity_planner/configs/`, create a file named `prod.json` with the following exact JSON content:
   ```json
   {
     "cpu_max": 90,
     "mem_max": 80,
     "alert_email": "alerts@capacity.local"
   }
   ```
   Create a symlink at `/home/user/capacity_planner/active_config` that points to `/home/user/capacity_planner/configs/prod.json`.

2. **Simulated Metrics Data:**
   Create a file at `/home/user/capacity_planner/simulated_metrics.csv` with the following contents:
   ```csv
   timestamp,cpu_usage,mem_usage
   1600000001,45,60
   1600000002,95,70
   1600000003,50,85
   1600000004,99,99
   1600000005,20,30
   ```

3. **Mock SMTP Server:**
   Write a Python script at `/home/user/capacity_planner/bin/mock_smtp.py`. This script should:
   - Run an SMTP server listening on `127.0.0.1` port `8025`.
   - Instead of routing emails, it must append the exact raw body (payload) of every incoming email as a new line to `/home/user/capacity_planner/logs/emails.log`. Strip out all email headers; only write the exact body content.

4. **Resource Monitor Script:**
   Write a Python script at `/home/user/capacity_planner/bin/monitor.py`. This script should:
   - Read thresholds from the JSON file pointed to by the symlink `/home/user/capacity_planner/active_config`.
   - Read `/home/user/capacity_planner/simulated_metrics.csv` line by line (skip the header).
   - For every line, if `cpu_usage` > `cpu_max` OR `mem_usage` > `mem_max`, it must send an email via SMTP to `127.0.0.1:8025`.
   - The email "To" address must be the `alert_email` from the config.
   - The email body must be exactly: `ALERT: timestamp={timestamp}, cpu={cpu}, mem={mem}` (replace variables with the values from the row).
   - Process one row every 1 second (use `time.sleep(1)` between rows) to simulate real-time monitoring.
   - Exit gracefully when the file is fully processed.

5. **Process Supervision:**
   Create a supervisord configuration file at `/home/user/capacity_planner/supervisord.conf`.
   Configure it to:
   - Run in the foreground or as a daemon (your choice, but ensure it manages the processes).
   - Define a program `smtp` that runs `mock_smtp.py`. Set `autorestart=true`.
   - Define a program `monitor` that runs `monitor.py`. Set `autorestart=false`.
   - Direct standard output and standard error for both programs to files inside `/home/user/capacity_planner/logs/`.

6. **Execution:**
   Install `supervisor` via pip if necessary (`pip install supervisor`).
   Start the supervisor using your configuration: `supervisord -c /home/user/capacity_planner/supervisord.conf`.
   Wait for at least 6 seconds to ensure the monitor processes the entire CSV file and the emails are logged. Ensure the final outputs are properly flushed to `/home/user/capacity_planner/logs/emails.log`.