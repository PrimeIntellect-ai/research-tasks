You are a monitoring specialist setting up alerts for a staged deployment pipeline. Recently, the deployment has been failing because "Service B" attempts to start before "Service A" has finished writing its configurations (similar to a missing `After=` dependency in systemd, but occurring in our custom deployment framework). 

The deployment framework writes its output to `/home/user/deploy.log`.

Your task is to build a simple monitoring and log rotation mechanism to catch this specific error.

1. **Environment Setup**:
   Create a shell environment file at `/home/user/.alert_env`. 
   This file must export exactly one environment variable named `ALERT_CODE` with the value `DEP_FAIL_01`.

2. **Alert Monitor Script**:
   Write a Python script at `/home/user/check_deploy.py`. 
   This script must:
   - Read `/home/user/deploy.log`.
   - Look for any line containing the exact substring `ERROR: Missing dependency config`.
   - If found, it should read the `ALERT_CODE` environment variable.
   - For every occurrence of the error in the log, it must append a line to `/home/user/alerts.log` in the exact format: `[<ALERT_CODE>] Alert triggered: Dependency not ready`. (Replace `<ALERT_CODE>` with the actual value from the environment variable).

3. **Log Rotation Script**:
   Since `alerts.log` might grow indefinitely, write a bash script at `/home/user/rotate_alerts.sh` to perform custom log rotation.
   The script must:
   - Check the number of lines in `/home/user/alerts.log`.
   - If the file has strictly more than 5 lines, rename it to `/home/user/alerts.log.bak` (overwriting any existing `.bak` file) and create a new, empty `/home/user/alerts.log`.
   - If it has 5 lines or fewer, do nothing.

Ensure all scripts are executable. Do not run the scripts yourself; our automated testing suite will execute them sequentially in a clean bash session to verify your solution.