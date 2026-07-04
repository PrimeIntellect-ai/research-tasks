You are an observability engineer tuning the dashboard metrics pipeline for a new application. We need to implement a local telemetry generator, manage its lifecycle via systemd, set up log rotation, and write a script to simulate a rolling deployment of configuration versions.

Your task is to implement this pipeline entirely within `/home/user/observability` and configure it for the local user.

Step 1: Telemetry Generator
Create a Python script at `/home/user/observability/telemetry_generator.py`. This script must:
- Read a version string from `/home/user/observability/version.txt`. If the file doesn't exist, default to "v0.0".
- Run an infinite loop where, every 0.1 seconds, it appends a single line of JSON to `/home/user/observability/logs/telemetry.log`.
- The JSON must have the exact keys: `timestamp` (current epoch float), `cpu` (a random integer between 0 and 100), and `version` (the version read from the file when the script started).
- Ensure the output is flushed immediately so logs appear in real-time.

Step 2: Service Management
Create a user-level systemd service file at `/home/user/.config/systemd/user/telemetry.service`.
- The service should execute your `telemetry_generator.py` using Python 3.
- It should restart automatically on failure.
- Set the working directory to `/home/user/observability`.
(Note: You do not need to start or enable the service via `systemctl` if the environment's systemd daemon is not running, but the `.service` file must be perfectly formatted and placed in the correct location.)

Step 3: Log Rotation
Create a logrotate configuration file at `/home/user/observability/logrotate.conf` specifically for the `telemetry.log` file.
- It should trigger rotation if the file size exceeds `1k` (1 kilobyte).
- It should keep exactly 3 backups (rotations).
- It should compress the rotated files.
- It must not require root access.

Step 4: Rolling Deployment Orchestrator
Write a Python script at `/home/user/observability/deploy.py` to simulate a staged deployment of new dashboard target versions. The script must do the following in order:
1. Define a list of versions to deploy: `["v1.0", "v1.1", "v1.2"]`.
2. For each version:
   a. Overwrite `/home/user/observability/version.txt` with the current version string.
   b. Terminate any currently running `telemetry_generator.py` processes (you can use `pkill -f telemetry_generator.py` or `killall` to simulate a service restart).
   c. Launch `telemetry_generator.py` in the background.
   d. Sleep for 2 seconds (to allow logs to accumulate).
   e. Force logrotate to run using your config file, storing its state file locally at `/home/user/observability/logrotate.state`. Example: `logrotate -f -s /home/user/observability/logrotate.state /home/user/observability/logrotate.conf`.

Step 5: Execution
Run your `deploy.py` script so that it executes the full rolling deployment simulation.

After completing the task, the final system state should have:
- The generated scripts and configuration files in their specified locations.
- `version.txt` containing `v1.2`.
- Multiple log files in `/home/user/observability/logs/` (e.g., `telemetry.log`, `telemetry.log.1.gz`, etc.) showing the rotations.