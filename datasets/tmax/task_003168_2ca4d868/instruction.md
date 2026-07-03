You are a Linux systems engineer tasked with hardening the configuration of a user-space service and setting up its monitoring. Since you do not have root privileges, all configurations must be handled within the user's home directory (`/home/user`).

Please perform the following tasks:

1. **Environment Hardening:**
   The service requires a strict security mode to be enabled via the environment. Append the environment variable `APP_SECURE_MODE=strict` to `/home/user/.bashrc` so that it loads for interactive shells.

2. **Service Configuration File:**
   Create a configuration file at `/home/user/app_config.ini` with exactly the following parameters:
   - A `[security]` section with `tls_enabled = true` and `max_connections = 50`.
   - A `[logging]` section with `path = /home/user/app_logs/service.log`.

3. **User-Space Log Rotation:**
   The service logs heavily, so we need to set up log rotation. Since you lack root access to modify `/etc/logrotate.d/`, create a user-specific logrotate configuration file at `/home/user/logrotate.conf` that targets the log file `/home/user/app_logs/service.log`. 
   Configure it to:
   - Rotate daily.
   - Keep exactly 7 back-logged copies.
   - Compress the rotated logs.
   - Ensure the new log file is created with `0600` permissions (read/write for the user only).
   - *Note: Ensure the directory `/home/user/app_logs/` exists.*

4. **Health Check Script:**
   Write a monitoring script at `/home/user/monitor.sh` (make sure it is executable). 
   This script must:
   - Check the contents of `/home/user/app_logs/service.log`.
   - If the log file does not exist, or if the log contains the exact string "CRITICAL_ERROR", the script should write the exact text `STATUS: UNHEALTHY` to `/home/user/health.txt`.
   - If the log file exists and does NOT contain "CRITICAL_ERROR", it should write the exact text `STATUS: HEALTHY` to `/home/user/health.txt`.
   - The script can be written in Bash, Python, or any standard scripting language available on a standard Linux system.

Ensure all file paths, names, and permissions match these instructions exactly so the automated systems can verify your configuration.