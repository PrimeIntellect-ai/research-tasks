You are acting as a Cloud Architect. We are migrating a legacy background processing service that currently fails intermittently. The existing setup relies on a poorly configured cron job that often writes data to `/tmp` instead of the correct persistent volume due to missing environment variables.

Your task is to refactor this deployment entirely within the user space (`/home/user/migration`), utilizing user-level `systemd` for the worker process and `cron` for a new health-monitoring script.

Please perform the following steps:

1. **Prepare the Output Directory:**
   Create the directory `/home/user/migration/output`.
   Set its permissions to exactly `rwxr-x---` (750) so that only the owner and group can read/execute, and only the owner can write.

2. **Create the Systemd Service:**
   Create a user-level systemd service named `data-migrator.service` in `/home/user/.config/systemd/user/`.
   This service should:
   - Have a description of "Data Migrator Worker"
   - Execute the existing script `/home/user/migration/worker.py`
   - Explicitly define two environment variables within the unit file: `WORKER_DATA_DIR=/home/user/migration/output` and `NODE_ENV=production`

3. **Create the Systemd Timer:**
   Create a timer unit `data-migrator.timer` in `/home/user/.config/systemd/user/` that triggers the `data-migrator.service` every 5 minutes (e.g., `*:0/5`).
   Enable both the timer and the service (using `systemctl --user`).

4. **Create a Health Check Script:**
   Write a bash script at `/home/user/migration/health_check.sh`.
   The script must:
   - Check if the file `/home/user/migration/output/data.txt` exists.
   - If the file exists, append the exact string "STATUS: HEALTHY" to `/home/user/migration/metrics.log`.
   - If the file does not exist, append the exact string "STATUS: DEGRADED" to `/home/user/migration/metrics.log`.
   - Ensure the script is executable.

5. **Schedule the Health Check:**
   Configure the user's crontab to run `/home/user/migration/health_check.sh` every minute. Ensure that the cron entry explicitly sets `WORKER_DATA_DIR=/home/user/migration/output` on the same line or before the script execution, simulating an environment injection for the health check.

Do not use `sudo` or require root privileges. All operations must be performed as the default user.