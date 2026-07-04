You are tasked with resolving a simulated configuration and storage runaway issue, similar to a scenario where microservices miscommunicate and spam logs, overwhelming a system. Since you do not have root access or Docker, you will build and harden a user-space monitoring solution using Python and standard Linux commands.

Please perform the following steps:

1. **Directory and Link Structure Management:**
   - Create a base directory: `/home/user/app_data/`
   - Create a versioned log directory inside it: `/home/user/app_data/logs_v1/`
   - Create a symbolic link at `/home/user/app_data/current_logs` that points to `/home/user/app_data/logs_v1/`.

2. **The Rogue Service:**
   Create a Python script at `/home/user/rogue_service.py` with the following exact code. This simulates a runaway process writing excessive data:
   ```python
   import time
   import os

   log_dir = "/home/user/app_data/current_logs"
   os.makedirs(log_dir, exist_ok=True)
   chunk = b"A" * 1024 * 1024  # 1 MB chunk

   try:
       while True:
           with open(os.path.join(log_dir, f"spam_{time.time()}.log"), "wb") as f:
               f.write(chunk)
           time.sleep(1)
   except KeyboardInterrupt:
       pass
   ```

3. **Storage Monitor & Process Management (Your Coding Task):**
   Write a Python script at `/home/user/storage_monitor.py`. This script must act as a daemon monitoring the log directory.
   - It should continuously (every 0.5 seconds) calculate the total size of all files within the directory referenced by the symlink `/home/user/app_data/current_logs`.
   - If the total size strictly exceeds 5 Megabytes (5 * 1024 * 1024 bytes), the script must:
     a) Find the process ID (PID) of the running `rogue_service.py` process.
     b) Terminate the `rogue_service.py` process (using `SIGTERM` or `SIGKILL`).
     c) Write a single line to `/home/user/alerts.log` exactly matching this format:
        `ALERT: Quota exceeded. Rogue PID <PID> killed.` (replace `<PID>` with the actual integer PID).
     d) Exit itself with a status code of 0.

4. **Execution:**
   - Start `/home/user/rogue_service.py` in the background.
   - Start `/home/user/storage_monitor.py` in the background.
   - Wait until the monitor detects the quota violation, kills the rogue service, and writes the alert log. 

Make sure the final state of the system satisfies all conditions before you finish. Do not leave the rogue process running.