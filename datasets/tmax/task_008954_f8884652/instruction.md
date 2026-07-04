You are acting as a monitoring specialist setting up a user-space traffic relay, alert monitor, and log rotation system. You do not have root access, so all configurations must run in user space.

Complete the following three tasks:

1. **Port Forwarding Script:**
Write a bash script at `/home/user/start_forwarding.sh` that uses `socat` to forward traffic.
- It must listen on TCP port `8333` (bound to `127.0.0.1`).
- It must forward this traffic to TCP port `9333` (on `127.0.0.1`).
- It must log all data passing through (using `socat`'s verbose flag `-v` or `-x`) to `/home/user/raw_traffic.log` by redirecting standard error to this file.
- The script must be executable. 

2. **Alert Extraction Script:**
Write a Python script at `/home/user/alert.py`. 
- This script should read an existing log file specified as the first command-line argument (e.g., `/home/user/raw_traffic.log`).
- It should scan every line. If a line contains the exact string `BLOCKED_IP`, it should append the line `ALERT: A blocked connection was detected.` to the file `/home/user/blocked.log`.
- Make sure the script handles the file reading and appending robustly.

3. **Log Rotation Configuration:**
Create a `logrotate` configuration file at `/home/user/alert_rotate.conf` targeting the `/home/user/blocked.log` file.
The configuration must specify the following directives:
- Rotate daily (`daily`)
- Keep exactly 5 rotated backups (`rotate 5`)
- Compress old log files (`compress`)
- Do not output errors if the log is missing (`missingok`)
- Do not rotate the log if it is empty (`notifempty`)

Do not start the `socat` process or the `logrotate` process yourself; simply create the scripts and configuration files exactly as specified.