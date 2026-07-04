You are acting as a Site Reliability Engineer. We have a mock microservice setup that has been failing due to missing environment configurations and a lack of process supervision. The services crash occasionally and fill up the disk with logs. 

Your task is to implement a Python-based user-space process supervisor that manages two specific services, injects the correct environment variables, handles log rotation, and reports uptime status.

Here are the requirements:

1. **Environment Setup**:
   Create an environment file at `/home/user/.service_env`. It must contain the following keys and values:
   `API_KEY=sre_monitor_99`
   `SERVICE_B_PORT=9090`

2. **The Supervisor Script**:
   Write a Python script at `/home/user/supervisor.py`. When executed, this script must:
   - Read `/home/user/.service_env` and apply these variables to the environment of the child processes it spawns.
   - Spawn two child processes using Python:
     - `/usr/bin/python3 /home/user/service_a.py`
     - `/usr/bin/python3 /home/user/service_b.py`
   - Monitor both processes. It should check their status every 1 second.
   - If either process terminates/crashes, the supervisor must immediately restart it and increment a global `restarts` counter.

3. **Log Rotation**:
   The stdout and stderr of BOTH child processes must be captured and written to `/home/user/logs/services.log`.
   You must implement log rotation for this file. The maximum file size should be exactly 1024 bytes (1 KB), and you should keep up to 3 backup files (e.g., `services.log.1`, `services.log.2`, `services.log.3`). You can use Python's built-in `logging.handlers.RotatingFileHandler` to manage this by piping the subprocess outputs to the logger.

4. **Uptime Status Reporting**:
   Every time the supervisor checks the process status (every 1 second), it must write its current state to `/home/user/monitor_status.json`.
   The JSON file must have exactly this structure:
   ```json
   {
       "service_a": "running",
       "service_b": "running",
       "restarts": 0
   }
   ```
   *Note: "running" should be updated to "dead" if the process is found dead before it is restarted. The `restarts` integer should represent the total number of times any service has been restarted by the supervisor since the supervisor started.*

5. **Final Execution**:
   Before you finish, start your supervisor script in the background so it continues running (e.g., using `nohup python3 /home/user/supervisor.py &`).

Ensure all directories exist (like `/home/user/logs/`) and permissions are standard. The system does not have root access, so use standard user-space commands.