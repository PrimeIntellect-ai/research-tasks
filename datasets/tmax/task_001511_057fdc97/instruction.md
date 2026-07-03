You are an engineer tasked with fixing a broken deployment of a custom storage monitoring daemon written in C, and setting up its surrounding infrastructure. The previous engineer left the job half-finished. 

Currently, the service fails to start because the C program crashes immediately upon execution.

Your objectives:
1. **Fix and Compile the Daemon:**
   - The source code is located at `/home/user/app/src/monitor.c`.
   - The program currently crashes (segfaults) when it runs because it tries to write to a log file in a directory that doesn't exist, without checking for `NULL` file pointers.
   - Fix the code so it safely handles the missing directory by either creating it (`/home/user/app/logs`) or safely failing with a descriptive error message instead of segfaulting.
   - Compile the fixed code to `/home/user/app/bin/monitor` using `gcc`. (Create the `bin` directory if needed).

2. **Backup Strategy:**
   - The daemon monitors `/home/user/data`. You need to ensure this directory is backed up.
   - Create a bash script at `/home/user/app/scripts/backup.sh` that creates a compressed tarball of the `/home/user/data` directory.
   - The archive must be saved in `/home/user/backups/` and named `data_backup_<timestamp>.tar.gz` (where timestamp is the Unix epoch time, e.g., `$(date +%s)`).
   - Make the script executable.

3. **Scheduled Tasks:**
   - Configure the user's crontab to run `/home/user/app/scripts/backup.sh` at the top of every hour (e.g., `0 * * * *`).

4. **Restore Script:**
   - Create a script at `/home/user/app/scripts/restore.sh` that takes exactly one argument (the path to a backup tarball).
   - The script should delete the current contents of `/home/user/data/` and extract the provided backup tarball into it.
   - Make the script executable.

5. **Log Rotation:**
   - Create a logrotate configuration file at `/home/user/app/config/logrotate.conf` to manage `/home/user/app/logs/monitor.log`.
   - It should rotate the log `daily`, keep `3` rotations, `compress` old logs, and `missingok`.

Run your fixed `monitor` program once manually to ensure it successfully creates the log file at `/home/user/app/logs/monitor.log`.