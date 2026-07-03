You are a monitoring specialist tasked with setting up a lightweight storage alert system for user-level mounts.

In `/home/user/storage_fstab`, there is a custom configuration file mapping mount symlinks to their assigned disk quotas. The file format is space-separated:
`<mount_symlink_path> <quota_in_MB>`

Example of `/home/user/storage_fstab`:
```
/home/user/mnt/logs 10
/home/user/mnt/data 50
```

These paths (like `/home/user/mnt/logs`) are symlinks pointing to actual underlying storage directories.

Your task is to write a Python script at `/home/user/check_quotas.py` that does the following:
1. Parses `/home/user/storage_fstab`.
2. For each line, resolves the symlink to its actual underlying real directory path.
3. Calculates the total size of all files within that real directory (including subdirectories). To calculate size in MB, sum the byte sizes of all files, then divide by `1048576` (which is 1024 * 1024).
4. Compares the calculated size (in MB) against the quota (in MB).
5. If the calculated size strictly exceeds the quota, write an alert to `/home/user/quota_alerts.log`.

The format of each line in `/home/user/quota_alerts.log` must be EXACTLY:
`[ALERT] Symlink: <symlink_path> | RealDir: <real_path> | Quota: <quota>MB | Actual: <actual_size>MB`

Where:
- `<actual_size>` is formatted to exactly 2 decimal places (e.g., `12.50`).
- `<quota>` is the integer from the fstab file.

For example:
`[ALERT] Symlink: /home/user/mnt/logs | RealDir: /home/user/real_logs | Quota: 10MB | Actual: 12.00MB`

Ensure you run the script so that `/home/user/quota_alerts.log` is generated before you complete the task.