You are a monitoring specialist tasked with setting up a health check and alert system for custom application mount points. Since you are operating in a restricted environment, you will build a Python automation script to act as the monitoring daemon.

Your task is to write a Python script at `/home/user/storage_monitor.py` that processes a mock `fstab` configuration, evaluates disk quotas, checks file security, and generates an alert log.

Here are the requirements for your script:

1. **Read Configuration:**
   - Parse the custom fstab file located at `/home/user/fstab_config`. It uses the standard fstab format: `<device> <mountpoint> <fstype> <options> <dump> <pass>`. Lines starting with `#` or empty lines should be ignored.
   - Read the quota definitions from a JSON file at `/home/user/quota_config.json`. This file maps mountpoint paths (keys) to their maximum allowed byte size (values).

2. **Perform Health Checks:**
   Iterate through every mountpoint extracted from `/home/user/fstab_config` and perform the following checks:
   - **Existence:** Check if the mountpoint directory exists.
   - **Quota:** If it exists, calculate the total size of all files within the mountpoint directory (and all its subdirectories) in bytes using file sizes (e.g., `os.path.getsize`). If the total size exceeds the limit defined in `quota_config.json`, flag a quota alert.
   - **Security:** If the directory exists, check the permissions of every file inside it. If any file is world-writable (has the write bit set for "others"), flag a security warning.

3. **Generate Alert Log:**
   Append the results of your checks to the log file exactly at `/home/user/alerts.log`. The log entries must strictly follow these formats (do not add extra text, quotes, or change the capitalization):
   - If a mountpoint does not exist:
     `[CRITICAL] Mountpoint <mountpoint> defined in fstab_config does not exist.`
   - If a mountpoint exceeds its quota:
     `[ALERT] Mountpoint <mountpoint> exceeded quota. Current: <size> bytes, Limit: <limit> bytes.`
   - If a file is world-writable (log this for *every* world-writable file found, order doesn't matter):
     `[WARN] Mountpoint <mountpoint> contains world-writable file: <filepath>`

4. **Execution:**
   - Write the script to `/home/user/storage_monitor.py`.
   - Run your script using Python so that `/home/user/alerts.log` is generated.
   - Ensure you process the directories exactly as listed in the `fstab_config`.

You must execute the script and verify that `/home/user/alerts.log` is created with the correct alerts before completing the task.