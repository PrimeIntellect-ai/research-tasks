You are a Linux systems engineer responsible for hardening user-space configurations and establishing monitoring. You need to create a custom, self-contained file integrity monitoring script that tracks modifications, logs alerts with a built-in rotation mechanism, and is scheduled to run periodically.

Since you do not have root access, you must accomplish this using standard user-level Bash capabilities. 

Your objective is to complete the following phases:

**Phase 1: The Integrity Monitor Script**
Create a Bash script at `/home/user/monitor/integrity_monitor.sh`. 
The script must do the following when executed:
1. Target directory: `/home/user/protected_data`.
2. Compute the MD5 checksums of all regular files in the target directory (you can use standard tools like `find` and `md5sum`).
3. Compare these checksums against a baseline file located at `/home/user/monitor/baseline.md5`.
   - If `baseline.md5` does not exist, the script should simply create it (storing the current hashes) and exit without logging any alerts.
4. If `baseline.md5` exists, compare the current state against it. For every file that is newly created or whose MD5 hash has changed, prepare an alert line.
5. The alert format must be exactly: `[YYYY-MM-DD HH:MM:SS] ALERT: <full-file-path> modified or created` (e.g., `[2023-10-25 14:05:01] ALERT: /home/user/protected_data/config.ini modified or created`).
6. Update `baseline.md5` to reflect the new current state of the directory so subsequent runs don't re-alert on the same modification.

**Phase 2: Built-in Log Rotation**
Before writing any new alerts to `/home/user/monitor/alerts.log`, the script must check the size of the log file:
1. If `/home/user/monitor/alerts.log` contains **5 or more lines**, it must be rotated *before* the new alerts are appended.
2. The rotation scheme should maintain a maximum of 3 archived logs: `alerts.log.1`, `alerts.log.2`, and `alerts.log.3`.
3. Just like standard logrotate, `.2` becomes `.3`, `.1` becomes `.2`, and `alerts.log` becomes `alerts.log.1`. Any existing `.3` is overwritten/discarded. The new alerts are then written to a fresh `alerts.log`.

**Phase 3: Scheduling**
Schedule the script to run automatically every 5 minutes using the user's crontab.
1. The cron job must execute `/home/user/monitor/integrity_monitor.sh`.
2. Ensure you install this into the user's crontab (e.g., using the `crontab` command).

Ensure the script is executable (`chmod +x`). All necessary directories (`/home/user/monitor` and `/home/user/protected_data`) already exist.