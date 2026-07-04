As a FinOps analyst, you are managing a custom "cloud cost analyzer" daemon. The daemon is notoriously unstable—it occasionally crashes or hangs without updating its heartbeat file. Since we don't have root access or systemd in this environment, you need to write a custom Bash-based process supervisor to manage it.

Your task is to write and configure a Bash supervisor script that monitors and automatically restarts the cost analyzer.

Here are the requirements:

1. **Configuration File**: 
   Create a configuration file at `/home/user/.config/finops/supervisor.conf` with the following key-value pairs (format `KEY="value"`):
   - `TARGET_CMD="/home/user/cost_analyzer.py"`
   - `HEARTBEAT_FILE="/home/user/heartbeat.txt"`
   - `LOG_FILE="/home/user/supervisor.log"`
   - `MAX_RESTARTS=3`

2. **Supervisor Script**:
   Write a Bash script at `/home/user/supervisor.sh`. The script must:
   - Source the configuration file.
   - Enforce idempotency: Ensure only one instance of the supervisor can run at a time by using a PID file at `/home/user/supervisor.pid`.
   - Start the `TARGET_CMD` in the background.
   - Continuously monitor the target process every 2 seconds:
     a) Check if the target process is still running.
     b) Check if the `HEARTBEAT_FILE` has been modified within the last 5 seconds. (The analyzer updates this file when healthy).
   - If the process is dead OR the heartbeat is stale (>5 seconds old), the supervisor must:
     - Forcefully kill the target process (if it's stuck).
     - Append a log entry to `LOG_FILE` in the exact format: `[YYYY-MM-DD HH:MM:SS] Restarted target process`
     - Restart the target process.
   - Keep track of the number of restarts. Once `MAX_RESTARTS` is reached, the supervisor must forcefully kill the target process, log `[YYYY-MM-DD HH:MM:SS] Max restarts reached, exiting` to `LOG_FILE`, and then exit.

3. **Testing**:
   - We have provided `/home/user/cost_analyzer.py` and set its behavior to crash continuously via `/home/user/cost_analyzer_behavior.txt`.
   - Make your supervisor script executable and run it in the background: `bash /home/user/supervisor.sh &`.
   - Wait for it to complete its restart cycle and exit (this should take less than 15 seconds given the continuous crashes).

Verify that your `LOG_FILE` contains exactly 3 restart messages and 1 exit message. Leave the `supervisor.log` and `supervisor.sh` in place for verification.