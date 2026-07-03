You are an observability engineer tasked with tuning the data pipeline for a new dashboard. An application is constantly writing telemetry logs to `/home/user/telemetry.log`, but the dashboard system requires a specific CSV format containing only `memory_utilization` metrics. Furthermore, the telemetry log grows very quickly and needs to be aggressively rotated to prevent disk space issues.

You need to implement the parsing logic, the log rotation configuration, and the scheduled automation to tie it all together. Note that you do not have root access.

Please complete the following steps:

1. **Rust Parser (`/home/user/parser.rs`)**:
   Write a Rust program in `/home/user/parser.rs` (which you must compile to `/home/user/parser` using `rustc`). 
   The program must read `/home/user/telemetry.log`. The log lines have the format:
   `[TIMESTAMP] LEVEL - METRIC_NAME: METRIC_VALUE`
   Example: `[2023-10-31T08:15:30Z] INFO - memory_utilization: 76.5`
   
   Your program must extract only the lines where `METRIC_NAME` is exactly `memory_utilization`. 
   For each matching line, append a line to `/home/user/memory_dashboard.csv` in the format:
   `TIMESTAMP,METRIC_VALUE`
   (Do not include brackets or extra spaces. Example: `2023-10-31T08:15:30Z,76.5`).
   Because this is a standalone file, only use the Rust standard library (no external crates).

2. **Log Rotation Configuration (`/home/user/logrotate.conf`)**:
   Create a logrotate configuration file for `/home/user/telemetry.log` with the following exact specifications:
   - Rotate the log file if its size exceeds `100k`.
   - Keep exactly `4` back-up copies.
   - Compress the old log files.
   - Use the `copytruncate` directive so the application doesn't need to be restarted.
   - Do not use absolute paths for the `su` directive, or omit the `su` directive altogether since this will run as the user.

3. **Automation Script (`/home/user/process_metrics.sh`)**:
   Write a bash script at `/home/user/process_metrics.sh` (ensure it is executable) that performs the following actions in order:
   - Runs your compiled Rust parser (`/home/user/parser`).
   - Manually triggers logrotate for your configuration using a local state file to track rotation:
     `logrotate -s /home/user/logrotate.state /home/user/logrotate.conf`

4. **Scheduled Task**:
   Configure the current user's crontab so that `/home/user/process_metrics.sh` executes every 5 minutes. 
   *(Use the standard cron syntax: `*/5 * * * * /home/user/process_metrics.sh`)*.

Make sure your Rust code handles potential file I/O errors gracefully. The automated system will test your setup by appending fake logs to `/home/user/telemetry.log`, triggering your script, and verifying the CSV output and log rotation states.