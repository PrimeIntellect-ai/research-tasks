You are a monitoring specialist tasked with setting up a local alerting pipeline for a microservices architecture. Due to a recent incident where services dropped connections silently, you need to create an automated script that checks log files, integrates with a local CI/CD testing setup, and uses strict environment configurations.

Your task has three phases: Configuration, Pipeline Scripting, and CI/CD Hook Setup.

**Phase 1: Environment Configuration**
Create a shell profile file at `/home/user/.monitor_profile`. It must contain exactly these two exported environment variables:
- `LOG_DIR=/home/user/service_logs`
- `ALERT_THRESHOLD=10`

**Phase 2: Text Processing & Alerting Pipeline**
Create a bash script at `/home/user/monitor_repo/alert_pipeline.sh`. The script must do the following:
1. Source the `/home/user/.monitor_profile` file to load the environment variables.
2. Iterate through all subdirectories in `$LOG_DIR`. Each subdirectory represents a service (the name of the subdirectory is the service name).
3. Inside each service directory, read the `app.log` file.
4. Using text processing tools (`awk`, `grep`, `sed`, etc.), calculate the failure rate for that service. The failure rate is the percentage of lines containing the exact strings `[ERROR]` or `[TIMEOUT]` relative to the total number of lines in that file. Calculate this as an integer percentage (e.g., if there are 15 errors in 100 lines, the rate is 15). Round down to the nearest integer.
5. If the calculated failure rate is greater than or equal to `$ALERT_THRESHOLD`, write an alert to `/home/user/active_alerts.log`.
6. The format of the alert must be exactly: `ALERT: <service_name> failure rate at <X>%`.
7. Ensure the alerts in `/home/user/active_alerts.log` are sorted alphabetically by service name.
8. Ensure the script is executable.

**Phase 3: CI/CD Pipeline Construction**
We need to ensure the alerting script is validated before any code commits. 
1. Initialize a Git repository in `/home/user/monitor_repo`.
2. Create a Git `pre-commit` hook at `/home/user/monitor_repo/.git/hooks/pre-commit`.
3. The hook must execute a bash syntax check (`bash -n alert_pipeline.sh`) on the script. If the syntax check fails, the hook must exit with code 1. If it passes, it must exit with code 0.
4. Make sure the hook is executable.

To complete the task, run your `/home/user/monitor_repo/alert_pipeline.sh` script once so it generates the `/home/user/active_alerts.log` file.