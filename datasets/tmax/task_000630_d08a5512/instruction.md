You are a monitoring specialist tasked with implementing a reliable supervision and backup policy for a critical filesystem metrics worker. 

The worker script is located at `/home/user/worker.py`. When it runs, it continuously writes data to the directory `/home/user/data` and records its process ID (PID) in `/home/user/app.pid`. 

Currently, the worker has crashed. The `/home/user/app.pid` contains a stale PID, and the worker is no longer running.

Your task is to write a robust Python script at `/home/user/supervise.py` that enforces our monitoring and backup policy. When executed, your script must perform the following actions:

1. **Process Checking**: Read the PID from `/home/user/app.pid`. Check if a process with this PID is currently running.
2. **Healthy State**: If the process is running, the script should simply exit with a status code of 0 without doing anything else.
3. **Recovery State**: If the process is NOT running (or the PID file is missing/invalid), the script must execute the following recovery steps exactly in this order:
    a. **Backup**: Create a compressed tarball archive of the entire `/home/user/data` directory and save it exactly to `/home/user/backup/data_archive.tar.gz`.
    b. **Alert**: Append the exact string `ALERT: Worker down. Backup created.` on a new line to `/home/user/alerts.log`.
    c. **Restart**: Launch `/home/user/worker.py` in the background (so it continues running after your supervisor script exits). Use Python's `subprocess` module to start it asynchronously. The worker script will automatically overwrite the stale PID in `app.pid`.

**Action Required**:
1. Write the `/home/user/supervise.py` script according to the specifications above. 
2. Ensure you handle missing files and exceptions robustly.
3. **Run your script once**. Since the worker is currently down, running your script should successfully trigger the backup, log the alert, and start the worker process.

Note: You do not have root access. All paths must be exactly as specified.