You are a Linux systems engineer tasked with implementing a hardened storage quota enforcement mechanism for a specific application directory. 

A rogue application frequently ignores application-level quotas and fills up disk space in `/home/user/app_data`. You need to create an automated, silent enforcer using Bash and user-level systemd services.

Perform the following tasks:

1. **Storage and Process Monitor Script:**
   Create a Bash script at `/home/user/enforcer.sh` and make it executable.
   The script must:
   - Calculate the total size of `/home/user/app_data` in kilobytes.
   - If the size exceeds 5000 KB (5 MB), it must identify any processes currently accessing or writing to files within `/home/user/app_data/`.
   - Send a `SIGKILL` (kill -9) to those processes.
   - For every process killed, append a log entry to `/home/user/enforcement.log` in exactly this format:
     `[YYYY-MM-DD HH:MM:SS] ACTION=KILL PID=<PID> DIR=/home/user/app_data EXCEEDED_QUOTA`
     (Replace `<PID>` with the actual process ID, and the timestamp with the current time).
   - Once the processes are killed, the script must delete all `.tmp` files inside `/home/user/app_data/` to free up space.

2. **Email Alert Spooling:**
   Instead of using a full MTA, we use a directory-based mail spooler. 
   If a process was killed, the script must create a text file in `/home/user/mail_spool/` named `alert_<PID>.eml`.
   The contents must be exactly:
   ```
   To: admin@local.domain
   From: monitor@local.domain
   Subject: Quota Alert - Process Terminated
   
   Process <PID> was terminated for exceeding the 5000KB limit in /home/user/app_data.
   ```
   (Replace `<PID>` with the actual terminated process ID).

3. **Scheduled Task Configuration:**
   Configure a user-level systemd timer to run this script automatically.
   - Create a service unit file at `/home/user/.config/systemd/user/enforcer.service` that executes `/home/user/enforcer.sh`.
   - Create a timer unit file at `/home/user/.config/systemd/user/enforcer.timer` that triggers the service every 1 minute.
   - Enable and start the timer for the current user.

Ensure your script handles edge cases (like no processes accessing the directory despite the size being large) gracefully.