You are a monitoring specialist tasked with creating a custom storage and alert monitoring tool. You need to write a Go program that monitors specific storage paths, resolves directory symlinks, calculates disk usage, tests connectivity to the alert server, and generates email spools for quota violations.

Write a Go program at `/home/user/monitor.go` that performs the following steps:

1. **Directory Structure Management & Monitoring:**
   Scan the directory `/home/user/monitored_links/`. This directory contains symlinks pointing to various storage nodes.
   For each symlink found in this directory:
   - Resolve the symlink to its target path.
   - If the symlink is broken (points to a non-existent path), append the following exact line to `/home/user/monitor.log`:
     `ERROR: Broken link [symlink_name]` (e.g., `ERROR: Broken link broken_data`)
   - If the symlink is valid, calculate the total size (in bytes) of all files within the resolved target directory (non-recursive is fine for this task, just the files directly inside the target directory).

2. **Disk Quota Evaluation:**
   Check if the total size of the valid target directory exceeds the quota limit of 10,485,760 bytes (10 MB). 

3. **Connectivity Diagnostics:**
   If ANY valid directory exceeds the quota, your program must first attempt to verify connectivity to the local email relay server by attempting a TCP connection to `127.0.0.1:9025`.
   - If the connection fails (e.g., connection refused), append the following line to `/home/user/monitor.log` (only once per run, regardless of how many quotas are exceeded):
     `WARN: Email server unreachable`

4. **Email Alert Generation:**
   For every directory that exceeds the quota, create an alert file in `/home/user/mail_spool/`. The file must be named `alert_[symlink_name].txt` (e.g., `alert_user_data.txt`).
   The contents of this file must be exactly:
   ```
   To: admin@local
   Subject: Quota exceeded for [symlink_name]
   Size: [size_in_bytes]
   ```

Your task is complete when the Go program is written, successfully compiled or run (e.g., `go run /home/user/monitor.go`), and all resulting logs and spool files are generated correctly. Ensure your Go code handles errors robustly.