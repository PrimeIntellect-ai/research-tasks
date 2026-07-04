You are an observability engineer tasked with tuning and automating the deployment of a local connectivity-monitoring dashboard. The system will track internal services, and you need to set up the configuration, the monitoring agent, process supervision, and the deployment script. 

All your work must be done in `/home/user/`.

Create the following files to complete the observability pipeline:

1. **Dashboard Configuration Script (`/home/user/update_dash.py`)**:
   An idempotent Python script that takes a JSON file path as a command-line argument.
   - It must read the JSON file.
   - Add a user object `{"username": "obs_admin", "group": "obs_group"}` to the `users` list, only if a user with the username "obs_admin" does not already exist.
   - Ensure the strings `"127.0.0.1:8001"` and `"127.0.0.1:8002"` are present in the `monitored_targets` list (without creating duplicates).
   - Write the modified JSON back to the same file.

2. **Metrics Collector (`/home/user/check_targets.py`)**:
   A Python script that indefinitely checks the TCP connectivity of the targets listed in the `monitored_targets` array of `/home/user/dashboard.json`.
   - Every 2 seconds, attempt a TCP socket connection (with a 1-second timeout) to each target.
   - Write the connectivity results as a JSON dictionary to `/home/user/status.json` (e.g., `{"127.0.0.1:9090": "DOWN", "127.0.0.1:8001": "UP", ...}`).
   - *Crash Simulation*: To test our restart policies, at the very beginning of each 2-second loop iteration, check if a file named `/home/user/crash_now` exists. If it does, delete the file and immediately exit the script with exit code 1.

3. **Process Supervisor (`/home/user/supervise.py`)**:
   A Python script that acts as a process supervisor for `check_targets.py`.
   - It should launch `python3 /home/user/check_targets.py` as a subprocess.
   - If the subprocess exits with a non-zero exit code, the supervisor must immediately restart it.
   - Append a line to `/home/user/supervise.log` containing exactly the word `RESTARTED` every time it restarts the subprocess.
   - *Restart Policy*: If the subprocess crashes and is restarted 3 times within any rolling 10-second window, the supervisor itself must exit with code 2.

4. **Deployment Pipeline (`/home/user/deploy.sh`)**:
   A bash script that orchestrates the deployment.
   - Make sure it executes `python3 /home/user/update_dash.py /home/user/dashboard.json`.
   - Start `/home/user/supervise.py` in the background (using python3).
   - Save the PID of the backgrounded supervisor process to `/home/user/supervisor.pid`.
   - Make sure `deploy.sh` is executable.

The initial `/home/user/dashboard.json` file has already been created for you. A background service is running on port 8001, but port 8002 is inactive. You must execute `./deploy.sh` to start the system before completing the task.