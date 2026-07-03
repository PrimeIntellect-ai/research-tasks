You are a cloud architect preparing to migrate legacy virtualization services to a new infrastructure. Before migrating, you need to analyze the disk usage of the existing virtual machine images, monitor if they exceed our migration storage quota, and set up proper log rotation for the monitoring tool.

Your task is to implement this monitoring and logging setup:

1. Write a Go program located at `/home/user/vm_monitor.go`. This program must:
   - Scan the directory `/home/user/legacy_vms` for any files with the `.qcow2` extension.
   - For each `.qcow2` file, determine its "virtual size" in bytes. You must use the `qemu-img info --output=json` command via Go's `os/exec` package and parse the JSON output to extract the `virtual-size` field.
   - Calculate the total virtual size of all `.qcow2` files in the directory.
   - Check if this total exceeds the strict migration quota of 50 Gigabytes (exactly 53687091200 bytes).
   - Append a single line to the log file `/home/user/migration_storage.log` in the exact following format:
     `[YYYY-MM-DD HH:MM:SS] TOTAL_VIRTUAL_BYTES=<total_bytes> EXCEEDS_QUOTA=<true|false>`
     *(Note: use the current local time for the timestamp).*

2. Create a local logrotate configuration file at `/home/user/logrotate.conf` that manages `/home/user/migration_storage.log`. It must be configured to:
   - Rotate daily.
   - Keep exactly 3 rotated backups.
   - Compress the rotated logs.
   - Create a new log file after rotation.

3. Execute the workflow to simulate its operation:
   - Run your Go program once (e.g., `go run /home/user/vm_monitor.go`).
   - Force a log rotation using your custom configuration. Since you do not have root access, use a local state file:
     `logrotate -f -s /home/user/lr.state /home/user/logrotate.conf`
   - Run your Go program a second time.

By the end of this task, you should have the Go script, the logrotate config, the active log file, and one compressed rotated log file.