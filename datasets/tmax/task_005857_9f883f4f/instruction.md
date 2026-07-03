You are an edge computing engineer deploying a local configuration management system on an IoT gateway device. The device will receive configuration updates via a local Git repository push. Whenever a new configuration is pushed, the device must back up its current state before applying the new settings. You also need to schedule a periodic synchronization task.

Your objective is to implement the backup logic, configure the Git repository with a hook, set up secure permissions, and schedule the sync job. 

Perform the following tasks on the system:

1. **Directory Setup & Permissions:**
   - Create the directory `/home/user/scripts`.
   - Create the directory `/home/user/backups`.
   - Set the permissions of `/home/user/backups` so that *only* the owner has read, write, and execute access (equivalent to `700`). Group and others must have no access.
   - The system already has a directory at `/home/user/device_data` containing current state files.

2. **Backup Script:**
   - Write a Python script at `/home/user/scripts/edge_backup.py`.
   - This script must use Python's built-in `tarfile` module to create a compressed gzip archive (`.tar.gz`) of the entire `/home/user/device_data` directory.
   - The output archive must be saved exactly at `/home/user/backups/state_backup.tar.gz`.
   - Ensure this script is executable.

3. **Git Hub Configuration & Hook:**
   - Initialize a bare Git repository at `/home/user/edge_config.git`.
   - Create a `post-receive` hook inside this repository (`/home/user/edge_config.git/hooks/post-receive`).
   - The `post-receive` hook *must be written in Python* (using `#!/usr/bin/env python3` or similar shebang).
   - The hook must print exactly "Deployment received, backing up..." to standard output.
   - The hook must then execute the `/home/user/scripts/edge_backup.py` script (e.g., using `subprocess` or `os.system`).
   - Make sure the hook is executable.

4. **Scheduled Task:**
   - Create a text file at `/home/user/cron.txt` containing a cron expression to run the script `/home/user/scripts/sync_data.sh` exactly every 15 minutes (e.g., at minute 0, 15, 30, and 45 of every hour). (Note: you do not need to create `sync_data.sh`).
   - Install this cron schedule for the current user using the `crontab` command (i.e., load `/home/user/cron.txt` into the user's crontab).

Ensure all paths and permissions strictly follow these instructions, as they will be tested automatically by triggering a push to the Git repository and inspecting the resulting files, permissions, and crontab.