I need you to fix a broken network monitoring setup for me. We have a Python script that acts as an automated alert generator, but it is currently failing due to path issues (simulating a cron execution environment) and missing text processing logic.

Here is the current setup (assume these directories and files already exist or need to be created by you if missing):
- Source directory: `/home/user/monitor`
- Backup directory: `/home/user/backup`
- Logs directory: `/home/user/monitor/logs`
- Simulated network state file: `/home/user/monitor/ss_output.txt`

Your tasks are:
1. **Backup**: Before modifying anything, copy the existing script `/home/user/monitor/check_network.py` to `/home/user/backup/check_network.py.bak`. Set the backup file's permissions to exactly `0400` (read-only for the owner).

2. **Fix and Complete the Script**: Modify `/home/user/monitor/check_network.py` using Python to accomplish the following:
   - Read the `/home/user/monitor/ss_output.txt` file. You must use a Python `subprocess` call combining `grep` and `awk` to extract the name of the process listening on port `8080`.
   - The script must generate a timestamp formatted exactly as `YYYY-MM-DD HH:MM:SS` in the `Asia/Tokyo` timezone.
   - The script must write an alert line to the absolute path `/home/user/monitor/logs/alert.log`. (Do not use relative paths like `.` or `logs/`, as this script is invoked from different working directories via cron).
   - The alert line must be formatted exactly as: `[<TIMESTAMP>] ALERT: Port 8080 is bound by process <PROCESS_NAME>`
   - After writing the file, the Python script must set the permissions of `/home/user/monitor/logs/alert.log` to exactly `0444`.

You can test your script by running `python3 /home/user/monitor/check_network.py` from any directory (e.g., from `/home/user`).

The simulated network state file (`/home/user/monitor/ss_output.txt`) will look like this:
```
State    Recv-Q    Send-Q       Local Address:Port       Peer Address:Port    Process
LISTEN   0         4096         127.0.0.1:6379           0.0.0.0:*            users:(("redis-server",pid=112,fd=4))
LISTEN   0         4096         0.0.0.0:8080             0.0.0.0:*            users:(("nginx",pid=555,fd=6))
LISTEN   0         4096         0.0.0.0:22               0.0.0.0:*            users:(("sshd",pid=99,fd=3))
```

Ensure your `awk`/`grep` pipeline extracts specifically `"nginx"` (with or without the quotes, but exactly as the process name appears). When you are done, run the script once so the alert file is generated.