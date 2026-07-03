You are tasked with fixing a broken user-level storage monitoring setup and configuring its logging mechanism. 

Currently, a mock storage monitoring service fails to start reliably because it attempts to run before the local filesystems are fully mounted. Furthermore, the actual monitoring script is missing, and the log rotation hasn't been configured, which will eventually fill up the disk.

Perform the following steps:

1. **Fix the Systemd Service:**
   Edit the file `/home/user/.config/systemd/user/storage-monitor.service`. Under the `[Unit]` section, add a dependency so that this service only starts after the local filesystems are mounted. Use the standard systemd target for local filesystems (`local-fs.target`).

2. **Write the Monitoring Script:**
   Create a bash script at `/home/user/monitor.sh` and make it executable.
   The script must do the following:
   - Read the mock fstab file located at `/home/user/mock_fstab`.
   - Extract the mount points (the second column).
   - For each mount point that *currently exists* as a directory on the actual filesystem, use `df` to find its usage percentage (e.g., `15%`).
   - Append a line to `/home/user/storage-monitor.log` in the exact format: `[YYYY-MM-DD HH:MM:SS] <mount_point>: <usage_percentage>` (e.g., `[2023-10-25 14:00:00] /: 42%`).

3. **Configure Log Rotation:**
   Create a logrotate configuration file at `/home/user/logrotate.conf` specifically for `/home/user/storage-monitor.log`.
   It must enforce the following rules:
   - Rotate the log file if its size exceeds 100 bytes.
   - Keep exactly 5 rotated backups.
   - Compress the rotated files.
   - Missing log files should not cause an error.

4. **Test the Setup:**
   - Run your `/home/user/monitor.sh` script.
   - Append 150 bytes of dummy text to `/home/user/storage-monitor.log` to trigger the size threshold (e.g., `head -c 150 /dev/urandom | base64 >> /home/user/storage-monitor.log`).
   - Run logrotate as a user with your config file to ensure it rotates properly: 
     `logrotate -s /home/user/logrotate.state /home/user/logrotate.conf`

Ensure all specified files exist at the exact paths provided and have the requested configurations.