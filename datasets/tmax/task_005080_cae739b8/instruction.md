You are an assistant helping a backup operator test a simulated restore process. We need a Python script to automate the verification of restored mount points based on a mock fstab file and generate rotation-managed log files.

Please write and execute a Python script at `/home/user/verify_restores.py` that performs the following steps:

1. Reads the mock fstab file located at `/home/user/backup_data/fstab.mock`.
2. Parses the file to find all entries where the file system type (the third column) is exactly `ext4`. Ignore any comments or empty lines.
3. For each `ext4` mount point (the second column), simulate a verification process by generating logs:
   - Construct a log file name by taking the mount point path and replacing all forward slashes (`/`) with underscores (`_`). For example, `/var/log` becomes `_var_log`.
   - The log file must be placed in `/home/user/logs/`, e.g., `/home/user/logs/_var_log.log`.
   - Configure a Python `logging` instance with a `RotatingFileHandler` for this file. Set `maxBytes=60` and `backupCount=2`.
   - The log formatter must output *only* the message itself (no timestamps, log levels, or extra spaces).
   - Write the exact message `VERIFIED: <mount_point>` to the logger 12 times using `logger.info()`.
4. After processing all ext4 entries and writing the logs, the script must count the total number of log files (including backups like `.log.1`, `.log.2`) generated for each mount point in `/home/user/logs/`.
5. Finally, write a JSON summary to `/home/user/summary.json` containing a dictionary that maps the original mount point string to the integer count of its log files.

Ensure the script runs successfully and `/home/user/summary.json` is generated with the correct contents.

Note: You do not need to create the `/home/user/backup_data/fstab.mock` file or the `/home/user/logs/` directory; assume they already exist and are properly populated.