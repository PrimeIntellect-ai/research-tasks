You are a monitoring specialist setting up a custom alert management environment. You need to configure a service file, set up the required directory structure using a script, and write a process-checking automation script. 

Please complete the following steps:

1. **Fix the Service Configuration**:
   There is a systemd-style configuration file located at `/home/user/monitoring/alert-monitor.service`. It currently fails because it tries to start before the log aggregator is ready. 
   Edit `/home/user/monitoring/alert-monitor.service` and add the following two lines immediately under the `[Unit]` section header:
   `After=log-aggregator.service`
   `Requires=log-aggregator.service`

2. **Directory Structure & Links Script**:
   Write a Bash script at `/home/user/monitoring/setup-env.sh` that does the following when executed:
   - Creates the directories `/home/user/monitoring/logs` and `/home/user/monitoring/alerts/active` (ensure parent directories are created if they don't exist).
   - Creates a symbolic link at `/home/user/monitoring/latest_alert_dir` that points directly to the `/home/user/monitoring/alerts/active` directory.
   - Ensure the script has executable permissions (`chmod +x`).

3. **Task Automation Script**:
   Write a Bash script at `/home/user/monitoring/check-process.sh` that serves as a pre-flight check for your alerts:
   - It must use `pgrep` to check if a process with the exact name `dummy-aggregator` is currently running.
   - If the process is running, the script must print exactly `Aggregator is running` to standard output and exit with a status code of `0`.
   - If the process is NOT running, the script must print exactly `Aggregator is missing` to standard output and exit with a status code of `1`.
   - Ensure the script has executable permissions (`chmod +x`).

Do not run the `setup-env.sh` script; the automated test will execute it to verify its behavior. Simply create the files and set the correct permissions.

*Note: You do not need root access to complete these tasks. All files should be placed within the `/home/user/` directory as specified.*